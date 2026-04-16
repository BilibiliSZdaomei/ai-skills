---
name: github-project-launchpad
description: Standardize the user's Windows project placement, local Git initialization, GitHub repository creation or linkage, remote hygiene, and safe version rollback for new or adopted projects. Use when starting a new project, deciding where it should live under D:\AI, auditing existing local or GitHub repos, connecting an existing folder to GitHub, or preparing reliable upload, pull, modify, and rollback workflows.
---

# GitHub Project Launchpad

## Overview

Use this skill as the repo-governance entrypoint for the user's projects. It decides where a project should live, whether Git or GitHub setup is missing, how to connect the local folder to the right remote, and how to keep rollback safe for a beginner workflow.

Route specialist work as soon as the path is clear:

- Use `$yeet` for staged commit, push, and PR flows.
- Use `$git-flow-skill` for feature, release, hotfix, and branch-recovery work.
- Use `$github-review-hygiene` or the GitHub plugin for review-heavy repository and PR triage.
- Use the Obsidian skills when the work becomes deeper vault maintenance instead of project bootstrap.

## Workflow

1. Inspect before changing anything.
   - Run `python scripts/scan_local_repos.py --roots D:\AI --format table`
   - Read [references/project-zones.md](./references/project-zones.md)
   - Read [references/github-estate.md](./references/github-estate.md) when current repo inventory or existing remote quirks matter
2. Decide project placement.
   - Honor an explicit user path unless it clearly conflicts with the zone rules
   - Default new code-first apps, websites, and prototypes to the `workspace` zone unless a more specific zone fits better
   - Never silently invent a new top-level root outside the known `D:\AI` zones
3. Classify the repo task and pick a project archetype.
   - new local folder that needs Git
   - existing local folder that needs GitHub
   - existing repo that needs remote cleanup
   - existing repo that needs a safer rollback strategy
   - website
   - fullstack-app
   - api-service
   - automation-tool
   - library-package
   - internal-tool
   - Read [references/project-archetypes.md](./references/project-archetypes.md) before choosing
4. Use dry-run first for any setup that creates folders, initializes Git, changes remotes, creates a GitHub repo, or pushes.
   - `python scripts/bootstrap_project_repo.py --project-name my-project --zone workspace --dry-run`
5. Scaffold project materials after the path and archetype are decided.
   - `python scripts/scaffold_project_assets.py --project-name my-project --project-path D:\AI\vscode\my-project --archetype fullstack-app --zone workspace --write-readme --write-obsidian-note --create-structure --dry-run`
   - Read [references/obsidian-project-notes.md](./references/obsidian-project-notes.md) before changing vault structure
6. Apply the bootstrap and scaffolding only after the plan looks correct.
7. Hand off day-2 work to the specialist skill that best matches the next step.

## Project Zone Rules

- `workspace` -> `D:\AI\vscode\<project-name>`
  Use for most standalone coding projects, websites, apps, prototypes, and experiments.
- `personal-web` -> the personal-web root from `references/project-zones.md`
  Use for personal site, self-hosting, VPS, reverse proxy, domain, and server-related work.
- `codex-infra` -> `D:\AI\Codex\<project-name>`
  Use for Codex or OpenClaw tooling, agent infrastructure, orchestration, and developer-platform helpers.
- `integration` -> the integration root from `references/project-zones.md`
  Use for connectors, API bridges, remote-control systems, and external system integration work.
- `system-ops` -> the system-ops root from `references/project-zones.md`
  Use for Windows setup, desktop automation, local machine optimization, and device-management utilities.
- `memory-skill` -> `D:\AI\agent-memory\repos\<project-name>`
  Use for durable memory, shared skills, and repositories that belong to the AI tooling substrate.
- If none of these fits cleanly, stop and explain the tradeoff instead of choosing a random root.

## GitHub Rules

- Default GitHub owner: `BilibiliSZdaomei`
- Default branch: `main`
- Prefer one authoritative GitHub remote named `origin`
- Match the repo name to the project slug unless the user explicitly chooses a different public name
- Default new repos to `private` unless the user explicitly asks for `public`
- Default remote protocol to `https` for this beginner workflow because the current repos already use it and `gh` can manage credentials cleanly
- Only switch to `ssh` when the user asks for it or the environment is already standardized on SSH
- Never overwrite an existing `origin` silently; call out mismatches first
- Treat extra remotes as exceptions to inspect, not a pattern to copy

## Architecture Rules

- Do not start with a random flat folder dump.
- Choose the simplest archetype that still leaves room for the project to grow.
- For normal public-facing websites, prefer a website structure aligned with modern Next.js app-router conventions.
- For fullstack products, prefer a monorepo-style split such as `apps/web`, `apps/api`, and `packages/shared`, with the API side organized into multiple modules instead of one giant file.
- For API-first projects, keep routing, schemas, services, and tests separate.
- For automations, separate reusable core logic from entry scripts and job runners.
- Write the chosen architecture into `README.md` so future changes still have a reference baseline.

## Required Checks

Before creating or linking a GitHub repo:

- Run `gh --version`
- Run `gh auth status`
- If `gh` is not authenticated, stop and tell the user to run `gh auth login`
- Inspect `git status -sb`
- Inspect existing remotes
- Confirm the local target path, GitHub repo name, visibility, and whether the first push should happen now or later

Before scaffolding docs and notes:

- Confirm or infer the project archetype
- Confirm whether the folder is empty or already contains code
- Avoid overwriting an existing `README.md` unless the user asked for a rewrite
- Keep the Obsidian project note under the shared project-note root and use Chinese properties by default

Before giving rollback guidance:

- Prefer branch restore, `git revert`, or switching to a known good commit over destructive history rewriting
- Use `git reset --hard` only if the user explicitly requests it and the risk is understood
- Tell the user whether the rollback affects only code or also tracked data and deployment state

## Scripts

- Inventory local repos:
  - `python scripts/scan_local_repos.py --roots D:\AI --format table`
  - Use `--format json` when another script or tool needs structured output
- Plan or bootstrap a repo:
  - `python scripts/bootstrap_project_repo.py --project-name my-site --zone personal-web --dry-run`
  - Add `--create-dir` if the folder does not exist yet
  - Add `--create-github` only after `gh auth status` passes
  - Add `--link-origin` when the GitHub repo already exists and the local folder only needs the remote wired up
  - Add `--initial-commit` when the folder already contains a stable starting point
  - Add `--push` only when a commit exists and the user wants the first upload immediately
- Scaffold README, folders, and Obsidian note:
  - `python scripts/scaffold_project_assets.py --project-name my-site --project-path D:\AI\vscode\my-site --archetype website --zone workspace --write-readme --write-obsidian-note --create-structure --dry-run`
  - Use `--summary` to seed the one-line project explanation
  - Use `--force` only when you intentionally want to overwrite generated files
  - The default Obsidian root is the main vault documented in `references/obsidian-project-notes.md`
  - The default project-note root is the Chinese folder defined in `references/obsidian-project-notes.md`

## Output Expectations

For every repo-governance request, return:

- recommended local path or detected current path
- recommended GitHub repo name and visibility
- recommended project archetype and why
- whether `gh` auth blocks GitHub creation
- the exact script or commands to run
- any hygiene risks such as multiple remotes, missing `origin`, dirty working tree, nested repo risk, or unsafe rollback assumptions

## Example Requests

- `Use $github-project-launchpad to decide where this new website project should live and prepare GitHub setup.`
- `Use $github-project-launchpad to turn this local folder into a Git repo and create the matching GitHub repo.`
- `Use $github-project-launchpad to audit my local repos under D:\AI and tell me which ones need cleanup.`
- `Use $github-project-launchpad to wire this existing GitHub repo to the current folder without breaking rollback safety.`
