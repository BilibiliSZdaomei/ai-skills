from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


ARCHETYPES: dict[str, dict[str, object]] = {
    "website": {
        "tag": "网站项目",
        "summary": "面向访问者的内容或品牌网站。",
        "tree_lines": [
            "app/",
            "components/",
            "content/",
            "docs/",
            "lib/",
            "public/",
            "scripts/",
            "styles/",
            "tests/",
        ],
        "directories": [
            "app",
            "components",
            "content",
            "docs",
            "lib",
            "public",
            "scripts",
            "styles",
            "tests",
        ],
    },
    "fullstack-app": {
        "tag": "全栈项目",
        "summary": "包含前端与后端的可持续演进产品仓库。",
        "tree_lines": [
            "apps/",
            "  web/",
            "    app/",
            "    components/",
            "    lib/",
            "    public/",
            "  api/",
            "    app/",
            "      routers/",
            "      services/",
            "      models/",
            "      schemas/",
            "packages/",
            "  shared/",
            "docs/",
            "infra/",
            "scripts/",
            "tests/",
        ],
        "directories": [
            "apps/web/app",
            "apps/web/components",
            "apps/web/lib",
            "apps/web/public",
            "apps/api/app/routers",
            "apps/api/app/services",
            "apps/api/app/models",
            "apps/api/app/schemas",
            "packages/shared",
            "docs",
            "infra",
            "scripts",
            "tests",
        ],
    },
    "api-service": {
        "tag": "接口项目",
        "summary": "以接口与服务边界为中心的后端仓库。",
        "tree_lines": [
            "app/",
            "  core/",
            "  models/",
            "  routers/",
            "  schemas/",
            "  services/",
            "docs/",
            "scripts/",
            "tests/",
        ],
        "directories": [
            "app/routers",
            "app/services",
            "app/models",
            "app/schemas",
            "app/core",
            "docs",
            "scripts",
            "tests",
        ],
    },
    "automation-tool": {
        "tag": "自动化项目",
        "summary": "以任务编排、同步、脚本与作业为中心的自动化仓库。",
        "tree_lines": [
            "src/",
            "  core/",
            "  integrations/",
            "  jobs/",
            "config/",
            "data/",
            "docs/",
            "scripts/",
            "tests/",
        ],
        "directories": [
            "src/core",
            "src/jobs",
            "src/integrations",
            "config",
            "data",
            "docs",
            "scripts",
            "tests",
        ],
    },
    "library-package": {
        "tag": "组件库",
        "summary": "供其他项目复用的包、SDK 或公共能力仓库。",
        "tree_lines": [
            "src/",
            "docs/",
            "examples/",
            "scripts/",
            "tests/",
        ],
        "directories": [
            "src",
            "docs",
            "examples",
            "scripts",
            "tests",
        ],
    },
    "internal-tool": {
        "tag": "内部工具",
        "summary": "面向内部运营、管理或控制台场景的工具仓库。",
        "tree_lines": [
            "apps/",
            "  web/",
            "  api/",
            "packages/",
            "  shared/",
            "docs/",
            "scripts/",
            "tests/",
        ],
        "directories": [
            "apps/web",
            "apps/api",
            "packages/shared",
            "docs",
            "scripts",
            "tests",
        ],
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold README, project structure, and Obsidian note.")
    parser.add_argument("--project-name", required=True, help="Project display name.")
    parser.add_argument("--project-path", required=True, help="Absolute local project path.")
    parser.add_argument("--archetype", choices=sorted(ARCHETYPES.keys()), required=True, help="Project archetype.")
    parser.add_argument("--zone", default="workspace", help="Project zone label.")
    parser.add_argument("--repo-name", help="GitHub repo slug.")
    parser.add_argument("--github-owner", default="BilibiliSZdaomei", help="GitHub owner.")
    parser.add_argument("--summary", default="", help="One-line summary.")
    parser.add_argument("--write-readme", action="store_true", help="Generate README.md if missing.")
    parser.add_argument("--create-structure", action="store_true", help="Create recommended directories.")
    parser.add_argument("--write-obsidian-note", action="store_true", help="Create the Obsidian project note.")
    parser.add_argument("--obsidian-root", default="D:\\Documents\\笔记", help="Obsidian vault root.")
    parser.add_argument("--notes-root-name", default="项目介绍", help="Root folder name for project notes.")
    parser.add_argument("--force", action="store_true", help="Overwrite generated files.")
    parser.add_argument("--dry-run", action="store_true", help="Only print the plan.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    return parser.parse_args()


def repo_url(owner: str, repo_name: str | None) -> str:
    if not repo_name:
        return ""
    return f"https://github.com/{owner}/{repo_name}"


def structure_tree(archetype: str) -> str:
    return "\n".join(ARCHETYPES[archetype]["tree_lines"])


def build_readme(args: argparse.Namespace) -> str:
    info = ARCHETYPES[args.archetype]
    summary = args.summary.strip() or info["summary"]
    github_url = repo_url(args.github_owner, args.repo_name)
    github_line = github_url if github_url else "待创建"
    return f"""# {args.project_name}

## 项目简介

{summary}

## 当前定位

- 项目类型：`{args.archetype}`
- 项目分区：`{args.zone}`
- 本地路径：`{args.project_path}`
- GitHub 仓库：{github_line}

## 推荐开发架构

这个项目按 `{args.archetype}` archetype 初始化，目标是先保证结构清晰，再给后续全栈扩展留下空间。

```text
{structure_tree(args.archetype)}
```

## 开发原则

- 先把目录边界定清楚，再开始堆代码。
- 把业务代码、脚本、文档、测试拆开，不要混在根目录。
- 所有重要决策优先写进 README 和 Obsidian 项目介绍。
- 每次达到稳定节点后做 Git 提交，保证可回退。

## 启动前待确认

- [ ] 具体技术栈
- [ ] 核心页面或接口范围
- [ ] 第一阶段里程碑
- [ ] 部署方式

## 里程碑建议

1. 完成最小可运行骨架
2. 明确核心功能闭环
3. 接入 GitHub 与部署流程
4. 补测试、文档和后续扩展计划
"""


def build_obsidian_note(args: argparse.Namespace) -> str:
    info = ARCHETYPES[args.archetype]
    summary = args.summary.strip() or info["summary"]
    today = date.today().isoformat()
    github_url = repo_url(args.github_owner, args.repo_name)
    tags = ["项目", "开发", info["tag"]]
    tag_lines = "\n".join(f"  - {tag}" for tag in tags)
    github_line = github_url if github_url else "待创建"
    return f"""---
标题: {args.project_name}
项目名: {args.project_name}
项目代号: {args.repo_name or '待定'}
项目类型: {args.archetype}
项目状态: 构思中
项目分区: {args.zone}
架构类型: {args.archetype}
本地路径: {args.project_path}
GitHub仓库: {github_line}
技术栈: []
标签:
{tag_lines}
创建日期: {today}
更新时间: {today}
---

# 项目介绍

## 一句话说明

{summary}

## 要解决的问题

- 待补充

## 推荐架构

- 当前按 `{args.archetype}` archetype 初始化
- 目录结构已同步到项目 README
- 后续具体框架选型可以在此处继续细化

## 本地与远端

- 本地路径：`{args.project_path}`
- GitHub 仓库：{github_line}

## 里程碑

1. 完成项目骨架
2. 明确 MVP 范围
3. 完成首次可运行版本
4. 接入部署与回退流程

## 关键决策

- 待补充

## 待确认问题

- 技术栈最终选型
- 数据层是否需要
- 是否需要部署到现有服务器
"""


def write_text(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_text(plan: dict[str, object]) -> str:
    lines = [
        f"project_path: {plan['project_path']}",
        f"archetype: {plan['archetype']}",
        "actions:",
    ]
    for action in plan["actions"]:
        lines.append(f"- {action}")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    project_path = Path(args.project_path)
    notes_root = Path(args.obsidian_root) / args.notes_root_name
    note_path = notes_root / args.project_name / "项目介绍.md"
    readme_path = project_path / "README.md"

    actions: list[str] = []

    if args.create_structure:
        for relative in ARCHETYPES[args.archetype]["directories"]:
            actions.append(f"create directory {project_path / relative}")

    if args.write_readme:
        actions.append(f"write README {readme_path}")

    if args.write_obsidian_note:
        actions.append(f"write Obsidian note {note_path}")

    plan = {
        "project_path": str(project_path),
        "archetype": args.archetype,
        "actions": actions,
    }

    if args.dry_run:
        if args.format == "json":
            print(json.dumps(plan, indent=2, ensure_ascii=False))
        else:
            print(render_text(plan))
        return 0

    project_path.mkdir(parents=True, exist_ok=True)

    if args.create_structure:
        for relative in ARCHETYPES[args.archetype]["directories"]:
            (project_path / relative).mkdir(parents=True, exist_ok=True)

    if args.write_readme:
        write_text(readme_path, build_readme(args), args.force)

    if args.write_obsidian_note:
        write_text(note_path, build_obsidian_note(args), args.force)

    if args.format == "json":
        print(json.dumps(plan, indent=2, ensure_ascii=False))
    else:
        print(render_text(plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
