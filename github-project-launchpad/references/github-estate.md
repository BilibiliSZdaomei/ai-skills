# Current GitHub Estate

Snapshot prepared on `2026-04-16`.

## GitHub Account

- Connected GitHub app account: `BilibiliSZdaomei`
- GitHub CLI `gh`: installed
- GitHub CLI `gh auth status`: not authenticated at snapshot time

## GitHub Repositories

| Repo | Visibility | Default branch | Local path |
| --- | --- | --- | --- |
| `BilibiliSZdaomei/Ethan` | public | `main` | `D:\AI\vscode\Ethan` |
| `BilibiliSZdaomei/ai-memory` | public | `sync/memory` | `D:\AI\agent-memory\repos\ai-memory` |
| `BilibiliSZdaomei/ai-skills` | public | `sync/generated-skills` | `D:\AI\agent-memory\repos\ai-skills` |

## Local Git Repositories Detected

- `D:\AI\agent-memory\repos\ai-memory`
- `D:\AI\agent-memory\repos\ai-skills`
- `D:\AI\Codex`
- `D:\AI\vscode\Ethan`

## Hygiene Notes

- `Ethan` has one expected GitHub remote named `origin`.
- `Ethan` also has an extra remote with a human sentence as the remote name pointing to an internal BYD DevOps manual repository.
- Do not treat that extra remote as a standard pattern for new repositories.
- `D:\AI\Codex` is already a Git repo locally but has no commits and no GitHub remote yet.
- The memory and skill repos use sync-style default branches and should be treated as infrastructure repos, not copied as the default branch model for normal app projects.

## Implications For New Projects

1. New normal projects should default to `main`, not the sync branches used by `ai-memory` and `ai-skills`.
2. New projects should get exactly one authoritative GitHub remote named `origin` unless the user asks for a more complex setup.
3. Creating GitHub repos through `gh` is currently blocked until `gh auth login` is completed.
