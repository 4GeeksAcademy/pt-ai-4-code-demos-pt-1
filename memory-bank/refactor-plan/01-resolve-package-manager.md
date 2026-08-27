# Step 01 — Resolve package manager conflict & clean up dependencies

## Reasoning

The project currently has **three** package management files:
- `requirements.txt` — only lists `pillow==10.3.0`
- `Pipfile` — lists `python`, `fastapi`, `pillow`, `imgkit`
- `pyproject.toml` (Poetry) — lists `python`, `fastapi`, `pillow`, `imgkit`, `flask`, `sanic`

This is confusing and unsustainable. Worse, `pyproject.toml` declares dependencies on **FastAPI, Flask, Sanic, and imgkit** — none of which are actually used anywhere in the code. The deployed handler uses `http.server.BaseHTTPRequestHandler` (stdlib), not any framework.

Having multiple sources of truth means:
- A new contributor doesn't know which package manager to use
- CI/deployment could pull unnecessary dependencies
- `pip install -r requirements.txt` works but misses any future non-Pillow deps
- The `poetry.lock` is out of sync with reality

**Goal:** Settle on a single package manager and a dependency list that reflects what the code actually needs.

## Work

1. Choose one package manager (recommend: a simple `requirements.txt` or `pyproject.toml` with minimal build system — the code only needs Pillow).
2. Remove unused dependency files (`Pipfile`, `Pipfile.lock` if it exists, decide on Poetry vs not).
3. Prune the dependency list to only what's actually imported (`pillow`).
4. Update any README installation instructions if needed.

> **Note:** This step is purely about metadata and config files — no application code changes.