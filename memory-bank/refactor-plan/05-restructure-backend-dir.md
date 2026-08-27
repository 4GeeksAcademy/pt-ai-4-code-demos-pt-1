# Step 05 — Restructure backend directory layout

## Reasoning

The current directory layout under `backend/` is confusing:

```
backend/
  app.py              # Vercel handler (entry point)
  backend/             # Nested package directory
    __init__.py        # Empty
    images/
      tag.py           # Duplicate tag logic
      cap.png, body.png, ...
  tests/
    __init__.py        # Empty
  oops.py              # Standalone hex conversion utility
```

Problems:
- `backend/backend/` nesting adds unnecessary depth and is easy to trip over
- The image assets (`cap.png`, `body.png`, etc.) live inside the nested `backend/images/` but are referenced by `os.getcwd()` paths in `app.py`
- `oops.py` is a loose utility with no home
- There's a `README.md` in the backend dir that may overlap with the project root

A flatter, clearer structure makes the project easier to navigate and maintain.

**Goal:** A clean backend directory where it's obvious where the handler, shared logic, tests, and assets live.

## Work

1. Design the target directory structure (proposed):
   ```
   backend/
     handler.py             # Vercel entry point (renamed from app.py)
     tag_maker.py           # Consolidated tag generation module
     oops.py                # Keep or merge utilities
     images/
       cap.png, body.png, ...
     tests/
       test_tag_maker.py
       __init__.py
     requirements.txt
     vercel.json
   ```
2. Move files accordingly, updating import paths.
3. Update the Vercel config (`vercel.json`) if the handler path changes.
4. Update any path references in the code to use reliable paths (e.g., `__file__`-relative instead of `os.getcwd()`).
5. Remove the nested `backend/backend/` directory.
6. Remove the empty `backend/tests/__init__.py` if keeping the test dir — or repurpose it.