# Step 02 — Consolidate duplicate tag-generation logic

## Reasoning

The core tag-generation functions (`make_tag`, `add_margin`, `get_text_dimensions`, `concat_tags`, `hex_to_rgba`) are **duplicated** across two files:

| File | Role |
|------|------|
| `backend/app.py` | The deployed Vercel handler — has its own copy of all functions |
| `backend/backend/images/tag.py` | An older module with its own copy, plus a `COLORS` enum and commented-out `__main__` block |

The copies have **subtle differences** that mean they are not interchangeable:

| Difference | `app.py` | `tag.py` |
|-----------|----------|----------|
| `bg` / `color` type | Accepts `str` (hex) or `tuple` | Only accepts `tuple` |
| Text positioning | `anchor="mm"` (center) | Manual `(cap.width, (height - text_h)//2 + 8)` offset |
| `make_tag` return | Returns `Image.Image` | Same, but type hints differ |
| `COLORS` enum | Not present | Present with 8 named colors |

This is a maintenance time bomb: a fix in one file won't propagate to the other, and the different text positioning means they'd produce different output for the same input.

**Goal:** A single source of truth for tag-generation functions, imported by both the Vercel handler and any other consumer.

## Work

1. Decide where the shared module should live (recommend: `backend/tag_maker/__init__.py` or a flat `backend/tag_maker.py`).
2. Move `make_tag`, `add_margin`, `get_text_dimensions`, `hex_to_rgba`, and `concat_tags` into the shared module.
3. Decide which of the divergent behaviors to keep (e.g., which text- positioning approach is correct, and whether to keep hex string support).
4. Update `app.py` to import from the shared module instead of defining its own copies.
5. Decide what to do with `tag.py` — either delete it or make it a thin re-export / compatibility shim.
6. Decide whether to keep the `COLORS` enum (and if so, where).
7. **Do not** change the observable behavior of the API — verify the handler still produces the same image output.