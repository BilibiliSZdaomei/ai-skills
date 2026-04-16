# Project Archetypes

Use these archetypes to avoid inventing a folder structure from scratch each time.

## Selection Rules

1. Choose the smallest archetype that still matches the likely growth path.
2. If the user says "personal website", default to `website`.
3. If the user wants frontend plus backend, user accounts, dashboards, APIs, or future scaling, default to `fullstack-app`.
4. If the project mainly exposes endpoints or integrations, default to `api-service`.
5. If the project is mainly scheduled jobs, scripts, or data sync, default to `automation-tool`.
6. If the project is reusable code for other projects, default to `library-package`.
7. If the project is an internal dashboard or admin console with backend logic, default to `internal-tool`.

## Archetypes

### website

Use for landing pages, blogs, personal websites, and content-first sites.

Recommended structure:

```text
app/
components/
content/
lib/
public/
styles/
docs/
scripts/
tests/
```

Reasoning:

- Mirrors current Next.js App Router folder conventions and project-organization guidance.
- Leaves room for content, UI components, utilities, and deployment docs without over-engineering.

### fullstack-app

Use for products with a real frontend and backend that should grow cleanly.

Recommended structure:

```text
apps/
  web/
    app/
    components/
    lib/
    public/
  api/
    app/
      routers/
      services/
      models/
      schemas/
packages/
  shared/
docs/
infra/
scripts/
tests/
```

Reasoning:

- Keeps frontend and backend separate but still inside one repo.
- Uses a multi-file API layout inspired by FastAPI's bigger-application guidance.
- Makes it easy to add shared types, utilities, docs, and deployment assets later.

### api-service

Use for backend-heavy repos without a first-party web UI.

Recommended structure:

```text
app/
  routers/
  services/
  models/
  schemas/
  core/
tests/
docs/
scripts/
```

### automation-tool

Use for scripts, scheduled jobs, ETL, sync pipelines, and internal automations.

Recommended structure:

```text
src/
  core/
  jobs/
  integrations/
config/
data/
docs/
scripts/
tests/
```

### library-package

Use for reusable packages, SDKs, utilities, and shared logic.

Recommended structure:

```text
src/
tests/
examples/
docs/
scripts/
```

### internal-tool

Use for internal dashboards, operational panels, and admin tools.

Recommended structure:

```text
apps/
  web/
  api/
packages/
  shared/
docs/
scripts/
tests/
```

## Primary Sources

- Next.js App Router project structure guidance:
  - https://nextjs.org/docs/app/getting-started/project-structure
- FastAPI larger-application multiple-file guidance:
  - https://fastapi.tiangolo.com/tutorial/bigger-applications/
