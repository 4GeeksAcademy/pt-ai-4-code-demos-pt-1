# Step 04 — Migrate handler to FastAPI

**Prerequisite:** Step 03 (unit tests) must be completed first. Those tests verify the tag module produces correct output, so we can refactor the handler with confidence.

## Reasoning

The current handler uses Python's stdlib `BaseHTTPRequestHandler` with manual regex query-param parsing (`re.sub(r'^[/?]{0,2}', '', self.path)` + `parse.parse_qs`), raw `json.loads()` with no validation, and no structured error responses. Deployed on Vercel, bad input produces an HTML traceback rather than a useful error.

FastAPI gives us, with very little code:

| Concern | Current approach | FastAPI approach |
|---------|-----------------|-----------------|
| **Input parsing** | Manual regex + `parse.parse_qs` | `Query()` parameter with type annotation |
| **JSON validation** | `json.loads()` — crashes on malformed input | Pydantic model — automatic 400 with clear message |
| **Error responses** | HTML tracebacks (Vercel default) | Structured JSON via exception handlers |
| **API docs** | Nothing | Automatic `/docs` (Swagger) and `/openapi.json` |
| **CORS** | Manual header setting | Built-in `CORSMiddleware` |
| **Test client** | Awkward to mock `BaseHTTPRequestHandler` | `TestClient` — natural pytest integration |
| **Health endpoint** | Not present | Trivial `@app.get("/health")` |

FastAPI also **eliminates the need for a separate input-validation step** (old Step 06), since Pydantic models enforce types, bounds, and structure automatically.

This step must **not change the image output** — the tag-generation module (consolidated in Step 02, tested in Step 03) stays untouched. Only the HTTP handler layer changes.

## Work

1. If not already present from Step 01, add `fastapi` to the project dependencies.
2. Create a new handler file (e.g., `backend/handler.py` or `backend/api/index.py`):
   - Define Pydantic models for the input tag and the query parameter.
   - Create a FastAPI app with a `GET /` endpoint that deserializes `?q=`, validates it, calls the existing `concat_tags` from the tag module, and returns a `Response(content=..., media_type="image/png")`.
   - Add a `GET /health` endpoint returning `{"status": "ok"}`.
   - Add CORS middleware (allow the frontend origin).
   - Add a catch-all exception handler that returns structured JSON errors instead of HTML.
3. Write tests FIRST (before removing the old handler):
   - Using FastAPI's `TestClient`, test valid requests return 200 with `image/png`.
   - Test missing/invalid `?q=` returns 400 with structured JSON.
   - Test `/health` returns 200 with `{"status": "ok"}`.
   - Run the same pixel-sampling assertions from Step 03 to verify image output is identical.
4. Once tests pass, update `vercel.json` to point at the new FastAPI handler. Vercel detects ASGI apps automatically when a module exposes an `app` variable.
5. Run the full test suite to confirm no regressions.
6. **Optional:** Add a dev-mode startup command (`uvicorn handler:app --reload`) so local development doesn't need Vercel emulation.
7. Delete the old `backend/app.py` (the `BaseHTTPRequestHandler` file).

## Verification

- `curl "http://localhost:8000/?q=[{\"text\":\"hello\",\"bg\":\"#40a6ceff\",\"color\":\"#ffffffff\"}]"` returns a valid PNG
- `curl "http://localhost:8000/?q=not-json"` returns `{"detail": ...}` with status 400
- `curl "http://localhost:8000/health"` returns `{"status": "ok"}`
- All Step 03 tests still pass (same image output)
- The frontend still renders tags correctly (verify API URL still works or update it)