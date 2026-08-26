# Data Persistence Safety Rules

> Scope: localStorage reads, writes, quotas, and serialization.

## Rules

1. **Always wrap `localStorage` access in try/catch** — Safari private mode and
   full storage can throw `QuotaExceededError` or `SecurityError`. Catch and
   surface via a user-facing fallback (e.g. "Storage full — export notes").

2. **Check available quota before writing** — Use `navigator.storage.estimate()`
   when available. If remaining space is below 5 KB, warn the user rather than
   silently failing.

3. **Serialize with a versioned schema** — Store a single JSON blob under a
   well-known key (e.g. `"pt-notes:v1"`) that includes a `version` field. Never
   read unversioned/raw data. This lets you migrate safely later.

   ```typescript
   // Good
   const STORAGE_KEY = "pt-notes:v1";
   interface StoreV1 { version: 1; notes: Note[]; updatedAt: number; }

   // Bad — brittle, no migration path
   localStorage.setItem("notes", JSON.stringify(notes));
   ```

4. **Always validate deserialized data at the boundary** — After reading from
   localStorage, run the result through a Zod schema or a type guard. Silently
   discard (or log) malformed entries instead of crashing.

   ```typescript
   // Good
   const raw = localStorage.getItem(STORAGE_KEY);
   if (!raw) return [];
   const parsed = JSON.parse(raw);
   const result = storeSchema.safeParse(parsed);
   return result.success ? result.data.notes : [];
   ```

5. **Debounce persisted writes** — Avoid writing on every keystroke. Debounce
   saves (e.g. 500 ms) and batch updates to reduce contention with the main
   thread.

6. **Never store secrets in localStorage** — No auth tokens, API keys, or PII.
   localStorage has no expiration and is accessible by any JavaScript on the
   origin.

7. **Keep a single source of truth in memory** — Read from localStorage once on
   app boot into a React state/context. All mutations go through state, then
   persist to localStorage. Do not treat localStorage as an intermediate data
   store during normal operations.