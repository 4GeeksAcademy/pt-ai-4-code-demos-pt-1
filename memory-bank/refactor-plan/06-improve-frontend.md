# Step 06 — Improve frontend code quality

## Reasoning

The frontend works but has several quality issues that should be addressed while we're improving the project:

1. **Hardcoded production API URL** — `stores/tags.js` points directly at `https://discord-tagger.vercel.app/`. This breaks local development and makes it impossible to test against a local backend.
2. **No loading / error states** — If the API is down, the user sees a broken image with no feedback.
3. **`$emit` string events** — `TagEditor.vue` uses string-based `$emit('tagChanged', ...)` with inline `@change` handlers that manually reconstruct the tag object. This is fragile and verbose.
4. **No frontend tests** — Like the backend, there's no test coverage.
5. **Deprecated / unmaintained deps** — `vuedraggable` v4 may have compatibility concerns with Vue 3.4+.
6. **`dot-components` via git+https PAT** — Private GitHub dependency with a PAT embedded in `package.json` is a security and reliability risk.

**Goal:** A more maintainable, resilient frontend that works in development mode and doesn't crumble when the API is unreachable.

## Work

1. Make the API URL configurable (env var or Vite proxy).
2. Add loading state and error handling to the tag preview image.
3. Refactor `TagEditor.vue` to use `v-model` or explicit props/emits more cleanly.
4. Add frontend tests (vitest + vue-test-utils) for the Pinia store and at least one component.
5. Audit dependencies — consider replacing `vuedraggable` and `dot-components` if they're causing issues.
6. Verify the frontend still works end-to-end.