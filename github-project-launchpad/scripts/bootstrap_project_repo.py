from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


ZONE_ROOTS = {
    "workspace": Path(r"D:\AI\vscode"),
    "personal-web": Path("D:\\AI\\\u4e2a\u4eba\u7ad9+\u670d\u52a1\u5668"),
    "codex-infra": Path(r"D:\AI\Codex"),
    "integration": Path("D:\\AI\\\u8fdc\u7a0b\u5bf9\u63a5"),
    "system-ops": Path("D:\\AI\\\u7535\u8111\u4f18\u5316"),
    "memory-skill": Path(r"D:\AI\agent-memory\repos"),
}


def slugify_repo_name(value: str) -> str:
    candidate = re.sub(r"[\s_]+", "-", value.strip())
    candidate = re.sub(r"[^A-Za-z0-9.-]+", "-", candidate)
    candidate = re.sub(r"-{2,}", "-", candidate)
    return candidate.strip("-.").lower()


def run_command(command: list[str], cwd: Path | None = None, check: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip() or "command failed"
        raise RuntimeError(f"{' '.join(command)}: {stderr}")
    return result


def detect_nested_repo(path: Path) -> Path | None:
    result = run_command(["git", "rev-parse", "--show-toplevel"], cwd=path)
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip())


def get_origin_url(path: Path) -> str | None:
    result = run_command(["git", "remote", "get-url", "origin"], cwd=path)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def build_remote_url(owner: str, repo_name: str, protocol: str) -> str:
    if protocol == "ssh":
        return f"git@github.com:{owner}/{repo_name}.git"
    return f"https://github.com/{owner}/{repo_name}.git"


def require_binary(binary: str) -> None:
    if shutil.which(binary) is None:
        raise RuntimeError(f"required binary not found: {binary}")


def ensure_gh_auth() -> None:
    require_binary("gh")
    status = run_command(["gh", "auth", "status"])
    if status.returncode != 0:
        raise RuntimeError("gh is installed but not authenticated; run 'gh auth login' first")


def github_repo_exists(owner: str, repo_name: str) -> bool:
    result = run_command(["gh", "repo", "view", f"{owner}/{repo_name}"])
    return result.returncode == 0


def git_has_commits(path: Path) -> bool:
    result = run_command(["git", "rev-parse", "--verify", "HEAD"], cwd=path)
    return result.returncode == 0


def git_is_dirty(path: Path) -> bool:
    result = run_command(["git", "status", "--porcelain"], cwd=path, check=True)
    return result.stdout.strip() != ""


def current_branch(path: Path) -> str:
    result = run_command(["git", "branch", "--show-current"], cwd=path, check=True)
    return result.stdout.strip() or "main"


def validate_project_name(name: str) -> None:
    if not name.strip():
        raise RuntimeError("project name cannot be empty")
    if "\\" in name or "/" in name:
        raise RuntimeError("project name must be a single folder name, not a path")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap a local project repo and optional GitHub remote.")
    parser.add_argument("--project-name", required=True, help="Project folder name.")
    parser.add_argument("--project-path", help="Explicit local path. Overrides --zone.")
    parser.add_argument(
        "--zone",
        choices=sorted(ZONE_ROOTS.keys()),
        default="workspace",
        help="Project zone when --project-path is not provided.",
    )
    parser.add_argument("--repo-name", help="GitHub repo name. Defaults to a slugified project name.")
    parser.add_argument("--github-owner", default="BilibiliSZdaomei", help="GitHub owner.")
    parser.add_argument(
        "--visibility",
        choices=["private", "public"],
        default="private",
        help="Visibility for newly created GitHub repos.",
    )
    parser.add_argument(
        "--remote-protocol",
        choices=["https", "ssh"],
        default="https",
        help="Remote URL protocol.",
    )
    parser.add_argument("--create-dir", action="store_true", help="Create the project directory if missing.")
    parser.add_argument("--create-github", action="store_true", help="Create the GitHub repository if missing.")
    parser.add_argument("--link-origin", action="store_true", help="Add origin when the GitHub repo already exists.")
    parser.add_argument("--initial-commit", action="store_true", help="Create an initial commit from current files.")
    parser.add_argument("--initial-commit-message", default="chore: initialize repository", help="Commit message.")
    parser.add_argument("--push", action="store_true", help="Push the current branch after setup.")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan without changing anything.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    return parser.parse_args()


def render_text(plan: dict[str, object]) -> str:
    lines = [
        f"project_path: {plan['project_path']}",
        f"repo_name: {plan['repo_name']}",
        f"remote_url: {plan['remote_url']}",
        f"create_github: {plan['create_github']}",
        f"link_origin: {plan['link_origin']}",
        "actions:",
    ]
    for action in plan["actions"]:
        lines.append(f"- {action}")
    if plan["warnings"]:
        lines.append("warnings:")
        for warning in plan["warnings"]:
            lines.append(f"- {warning}")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    validate_project_name(args.project_name)

    repo_name = args.repo_name or slugify_repo_name(args.project_name)
    if not repo_name:
        raise RuntimeError("could not derive a safe repo name; pass --repo-name explicitly")

    project_path = Path(args.project_path) if args.project_path else ZONE_ROOTS[args.zone] / args.project_name
    remote_url = build_remote_url(args.github_owner, repo_name, args.remote_protocol)
    actions: list[str] = []
    warnings: list[str] = []

    if project_path.exists():
        if not project_path.is_dir():
            raise RuntimeError(f"target path is not a directory: {project_path}")
    else:
        if not args.create_dir:
            raise RuntimeError(f"target path does not exist: {project_path}; re-run with --create-dir")
        actions.append(f"create directory {project_path}")

    nested_repo = detect_nested_repo(project_path) if project_path.exists() else None
    if nested_repo and nested_repo.resolve() != project_path.resolve():
        raise RuntimeError(f"target path is inside another git repository: {nested_repo}")

    is_git_repo = nested_repo is not None and nested_repo.resolve() == project_path.resolve()
    if not is_git_repo:
        actions.append("initialize local git repository with main branch")

    origin_url = get_origin_url(project_path) if is_git_repo else None
    if origin_url and origin_url != remote_url:
        warnings.append(f"existing origin differs from target remote: {origin_url}")

    if args.create_github or args.link_origin:
        require_binary("git")
        ensure_gh_auth()
        exists_on_github = github_repo_exists(args.github_owner, repo_name)
        if args.create_github and not exists_on_github:
            actions.append(f"create GitHub repo {args.github_owner}/{repo_name} ({args.visibility})")
        elif args.create_github and exists_on_github:
            warnings.append(f"GitHub repo already exists: {args.github_owner}/{repo_name}")
        if args.link_origin and not exists_on_github:
            raise RuntimeError("cannot link origin because the GitHub repo does not exist yet")
        if not origin_url:
            actions.append(f"add origin remote {remote_url}")

    if args.initial_commit:
        actions.append(f"create initial commit '{args.initial_commit_message}'")

    if args.push:
        actions.append("push current branch to origin")

    plan = {
        "project_path": str(project_path),
        "repo_name": repo_name,
        "remote_url": remote_url,
        "create_github": args.create_github,
        "link_origin": args.link_origin,
        "actions": actions,
        "warnings": warnings,
    }

    if args.dry_run:
        if args.format == "json":
            json.dump(plan, sys.stdout, indent=2, ensure_ascii=False)
            sys.stdout.write("\n")
        else:
            print(render_text(plan))
        return 0

    if not project_path.exists():
        project_path.mkdir(parents=True, exist_ok=True)

    require_binary("git")
    if not is_git_repo:
        init_result = run_command(["git", "init", "-b", "main"], cwd=project_path)
        if init_result.returncode != 0:
            run_command(["git", "init"], cwd=project_path, check=True)
            run_command(["git", "checkout", "-b", "main"], cwd=project_path, check=True)

    origin_url = get_origin_url(project_path)

    if args.create_github or args.link_origin:
        exists_on_github = github_repo_exists(args.github_owner, repo_name)
        if args.create_github and not exists_on_github:
            visibility_flag = "--private" if args.visibility == "private" else "--public"
            run_command(
                ["gh", "repo", "create", f"{args.github_owner}/{repo_name}", visibility_flag],
                check=True,
            )
            exists_on_github = True
        if not origin_url:
            run_command(["git", "remote", "add", "origin", remote_url], cwd=project_path, check=True)
        elif origin_url != remote_url:
            raise RuntimeError(f"origin already points somewhere else: {origin_url}")

    if args.initial_commit:
        if not git_is_dirty(project_path):
            warnings.append("no local changes to commit")
        else:
            run_command(["git", "add", "-A"], cwd=project_path, check=True)
            run_command(["git", "commit", "-m", args.initial_commit_message], cwd=project_path, check=True)

    if args.push:
        if not git_has_commits(project_path):
            raise RuntimeError("cannot push before a commit exists")
        if not get_origin_url(project_path):
            raise RuntimeError("cannot push without origin configured")
        branch = current_branch(project_path)
        run_command(["git", "push", "-u", "origin", branch], cwd=project_path, check=True)

    final_plan = {
        **plan,
        "warnings": warnings,
    }

    if args.format == "json":
        json.dump(final_plan, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print(render_text(final_plan))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
