# ADR 001: Prototype-First Approach

## Status
Accepted

## Context
The project had clear safety rules but no existing code. We needed to decide whether to build infrastructure first (Zod, error boundaries, quota checks) or get a working UI visible quickly.

## Decision
We used a **prototype-first** approach:
1. Got a working CRUD app up with minimal types and raw localStorage.
2. Added tags and markdown rendering (high-value features) next.
3. Backfilled the safety infrastructure (Zod schemas, versioned storage, discriminated union state, tried/catched storage access, quota warnings).
4. Finished with search/filter, export, and polish.

## Consequences
- Working UI was visible after the first build phase, enabling early iteration.
- Infrastructure was retrofitted without changing the user-facing API — a smooth migration.
- Some code was rewritten during backfill (e.g. `useNotesStore` from a simple hook to a context provider with discriminated unions), but the component API surface remained stable.