# Refactor plan

This directory contains the planned steps for refactoring this project.  Steps will be in seperate files, and will be named `{0-padded index}-{step name in kebab case}.md`.

## Index

| Step | Reason |
|------|--------|
|[01 — Resolve package manager conflict](./01-resolve-package-manager.md)|3 competing package files (`requirements.txt`, `Pipfile`, `pyproject.toml`), unused deps (FastAPI, Flask, Sanic, imgkit). Settle on one.|
|[02 — Consolidate duplicate tag logic](./02-consolidate-tag-logic.md)|`make_tag` / `concat_tags` duplicated in `app.py` and `backend/images/tag.py` with subtle differences in text positioning and type handling. Single source of truth needed.|
|[03 — Add unit tests](./03-add-unit-tests.md)|Zero test coverage — no safety net for refactoring. Tests for tag generation, concat wrapping, hex parsing.|
|[04 — Migrate handler to FastAPI](./04-migrate-to-fastapi.md)|Replace fragile `BaseHTTPRequestHandler` + manual regex parsing with FastAPI — automatic input validation via Pydantic, structured errors, OpenAPI docs, CORS, and a testable client. Tests must be written **before** the migration to prevent regressions.|
|[05 — Restructure backend directory](./05-restructure-backend-dir.md)|Nested `backend/backend/` is confusing, assets referenced by `os.getcwd()` is fragile, `oops.py` is homeless. Flatten and clean up.|
|[06 — Improve frontend quality](./06-improve-frontend.md)|Hardcoded production API URL breaks local dev, no loading/error states, string-typed emits, no frontend tests, unmaintained deps.|
|[07 — Add CI pipeline](./07-add-ci-pipeline.md)|No automated test runs, no linting, no type-checking enforcement. CI locks in the improvements from all previous steps.|