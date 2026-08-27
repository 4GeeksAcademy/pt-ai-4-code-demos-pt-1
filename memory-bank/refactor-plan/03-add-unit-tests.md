# Step 03 — Add unit tests for the tag module

## Reasoning

The project has **zero test coverage**. The `backend/tests/` directory exists but only contains an empty `__init__.py`. This means:

- Every refactor is blind — there's no safety net to catch regressions
- The two divergent copies of tag logic could silently have different behavior and nobody would know
- Edge cases (empty text, very long text, unusual hex colors, many tags) are untested
- The wrapping logic in `concat_tags` has never been verified

Adding tests early (right after consolidating the logic) ensures the consolidation step was correct and gives a safety net for all subsequent steps.

**Goal:** Basic test coverage for the consolidated tag module, especially the image-generation functions and the concat wrapping logic.

## Work

1. Choose a test framework (recommend: `pytest` given it's the standard for Python).
2. Create `backend/tests/test_tag_maker.py` (or appropriate name matching the module).
3. Write tests for:
   - `hex_to_rgba` — valid hex, with/without `#`, edge cases
   - `add_margin` — correct dimensions, color fill
   - `get_text_dimensions` — basic smoke test (hard to assert exact values without font pinning)
   - `make_tag` — returns an image of expected min dimensions, uses correct background color (pixel sampling)
   - `concat_tags` — single tag, multiple tags, wrapping behavior, gap parameter
4. Write a test that verifies the API handler (`app.py`) returns a valid PNG with expected Content-Type.
5. Add the test dependency to the package config.
6. Verify tests pass.