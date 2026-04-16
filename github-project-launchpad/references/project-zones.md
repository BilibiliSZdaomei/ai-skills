# Project Zones

Use these roots when deciding where a new project should live under `D:\AI`.

## Decision Table

| Zone | Root | Use for | Default? |
| --- | --- | --- | --- |
| `workspace` | `D:\AI\vscode` | Most standalone coding projects, apps, sites, prototypes | Yes |
| `personal-web` | `D:\AI\个人站+服务器` | Personal site, VPS, domains, self-hosting, reverse proxy | No |
| `codex-infra` | `D:\AI\Codex` | Codex/OpenClaw tooling, agent infrastructure, orchestration | No |
| `integration` | `D:\AI\远程对接` | External integrations, remote control, API bridges | No |
| `system-ops` | `D:\AI\电脑优化` | Local machine optimization, desktop automation, device ops | No |
| `memory-skill` | `D:\AI\agent-memory\repos` | Memory repos, reusable skills, AI substrate projects | No |

## Selection Rules

1. Prefer `workspace` for normal code projects unless the project is clearly about servers, integrations, Codex infra, or memory tooling.
2. Keep each long-lived project in one clear home. Avoid creating the same project twice in different roots.
3. Avoid new top-level folders under `D:\AI` unless the user explicitly wants a new category.
4. Favor explicit, human-readable folder names. Do not add date prefixes or temporary suffixes to long-lived project folders.
5. For public-facing websites that are also deployment experiments, prefer `personal-web` over `workspace`.

## Naming Rules

- Local folder name can stay user-friendly.
- GitHub repo name should default to a lowercase ASCII slug when possible.
- If the local folder name is Chinese or contains unusual punctuation, derive a clean repo slug or ask for one.
- Keep one GitHub repo per long-lived project unless the user wants a mono-repo or a split frontend/backend design.

## Safe Defaults

- Default branch: `main`
- Default visibility: `private`
- Default remote protocol for this environment: `https`
- Default remote name: `origin`
