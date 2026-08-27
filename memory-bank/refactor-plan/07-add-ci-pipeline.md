# Step 07 — Add CI pipeline

**Note:** Step 06 (input validation & error handling) has been subsumed by Step 04 (FastAPI migration) — Pydantic models handle validation automatically.

## Reasoning

With tests written and the codebase cleaned up, the project needs a CI pipeline to enforce quality going forward. Currently:

- No automated test runs on push/PR
- No linting checks (Python or JavaScript)
- No type-checking enforcement
- No build verification for the frontend

Without CI, any of the previous steps could be silently undone by a future commit.

**Goal:** A GitHub Actions (or equivalent) pipeline that runs tests and linting on every push and pull request.

## Work

1. Create `.github/workflows/ci.yml`.
2. Add a job for the backend:
   - Install Python + dependencies
   - Run `pytest`
   - (Optional) Run `ruff` or `flake8` linting
3. Add a job for the frontend:
   - Install Node + dependencies
   - Run `vue-tsc --build --force` (type checking)
   - Run `vite build` (build verification)
   - (Optional) Run vitest tests if added
4. Verify the pipeline passes on the current branch.