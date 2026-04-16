from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    ".next",
    ".venv",
    "venv",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
}

GITHUB_REMOTE_RE = re.compile(
    r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+?)(?:\.git)?$",
    re.IGNORECASE,
)


def run_git(repo: Path, *args: str) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=str(repo),
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def find_repositories(roots: list[Path]) -> list[Path]:
    repos: list[Path] = []
    seen: set[str] = set()

    for root in roots:
        if not root.exists():
            continue

        for current_dir, dirnames, _filenames in os.walk(root):
            dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
            current_path = Path(current_dir)
            git_dir = current_path / ".git"

            if git_dir.exists():
                resolved = str(current_path.resolve())
                if resolved not in seen:
                    seen.add(resolved)
                    repos.append(current_path)
                dirnames[:] = []

    return sorted(repos)


def parse_remotes(raw_output: str) -> dict[str, dict[str, str]]:
    remotes: dict[str, dict[str, str]] = {}
    for line in raw_output.splitlines():
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        name = parts[0]
        url = parts[1]
        kind = parts[2].strip("()")
        remotes.setdefault(name, {})[kind] = url
    return remotes


def extract_github_repo(url: str | None) -> str | None:
    if not url:
        return None
    match = GITHUB_REMOTE_RE.search(url)
    if not match:
        return None
    return f"{match.group('owner')}/{match.group('repo')}"


def inspect_repo(repo: Path) -> dict[str, object]:
    branch_code, branch_out, _branch_err = run_git(repo, "branch", "--show-current")
    status_code, status_out, _status_err = run_git(repo, "status", "--porcelain")
    remote_code, remote_out, _remote_err = run_git(repo, "remote", "-v")
    head_code, _head_out, _head_err = run_git(repo, "rev-parse", "--verify", "HEAD")

    remotes = parse_remotes(remote_out if remote_code == 0 else "")
    origin = remotes.get("origin", {})
    origin_fetch = origin.get("fetch")
    origin_push = origin.get("push")

    warnings: list[str] = []
    if remote_code != 0 or not remotes:
        warnings.append("no remotes configured")
    if "origin" not in remotes:
        warnings.append("missing origin remote")
    if len(remotes) > 1:
        warnings.append("multiple remotes configured")
    if origin_fetch and origin_push and origin_fetch != origin_push:
        warnings.append("origin fetch and push differ")
    if head_code != 0:
        warnings.append("no commits yet")

    clean = status_code == 0 and status_out == ""
    if not clean:
        warnings.append("working tree not clean")

    return {
        "path": str(repo),
        "branch": branch_out if branch_code == 0 and branch_out else "(none)",
        "has_commits": head_code == 0,
        "clean": clean,
        "github_repo": extract_github_repo(origin_fetch or origin_push),
        "remotes": remotes,
        "warnings": warnings,
    }


def format_table(rows: list[dict[str, object]]) -> str:
    headers = ["path", "branch", "clean", "github_repo", "warnings"]
    rendered_rows: list[list[str]] = []

    for row in rows:
        rendered_rows.append(
            [
                str(row["path"]),
                str(row["branch"]),
                "yes" if row["clean"] else "no",
                str(row["github_repo"] or "-"),
                "; ".join(row["warnings"]) if row["warnings"] else "-",
            ]
        )

    widths = [len(header) for header in headers]
    for rendered in rendered_rows:
        for index, value in enumerate(rendered):
            widths[index] = max(widths[index], len(value))

    def render_line(values: list[str]) -> str:
        return " | ".join(value.ljust(widths[index]) for index, value in enumerate(values))

    separator = "-+-".join("-" * width for width in widths)
    lines = [render_line(headers), separator]
    for rendered in rendered_rows:
        lines.append(render_line(rendered))
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan local folders for Git repositories.")
    parser.add_argument(
        "--roots",
        nargs="+",
        default=[r"D:\AI"],
        help="One or more roots to scan.",
    )
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default="table",
        help="Output format.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    roots = [Path(root) for root in args.roots]
    repos = find_repositories(roots)
    rows = [inspect_repo(repo) for repo in repos]

    if args.format == "json":
        json.dump(rows, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0

    print(format_table(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
