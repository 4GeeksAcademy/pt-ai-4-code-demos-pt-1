# Devlog — Notes App

This document chronicles how the Notes App was built: the workflow, how the memory bank guided decisions, and how the agent safety rules were applied at each phase.

---

## Overview

The Notes App is a single-page note-taking application built with **React + Vite + TypeScript (strict) + TailwindCSS 4**. Notes are persisted in `localStorage` with Zod runtime validation, versioned schemas, and debounced writes.

The entire build was driven by two knowledge sources:

1. **The memory bank** (`/memory-bank/`) — product context, conventions, and architecture decision records (ADRs).
2. **Agent safety rules** (`/.agents/rules/`) — domain-specific guardrails for data persistence, validation, component structure, and TypeScript safety.

---

## Phase 0: Scaffolding & Tool Setup

### What happened

Bootstrapped the project using `npm create vite@latest` with the React + TypeScript template — following the convention in `memory-bank/conventions.md` that says *"Use command line tools to bootstrap project"* rather than generating files manually.

### Rules applied

- **Conventions** (`conventions.md`): *"Use command line tools to bootstrap project"* — we ran the Vite CLI instead of hand-writing config files.
- **TypeScript Safety** (`typescript-safety.md`): Enabled `strict: true` in `tsconfig.app.json` immediately after scaffolding.

### Decisions

- Installed `tailwindcss` + `@tailwindcss/vite` for styling (per `product-context.md`).
- Cleaned out all Vite boilerplate (`App.css`, hero images, SVG logos) to start from zero.

---

## Phase P1: Minimal Working App

### What happened

With the project scaffolded, we built a working CRUD app as fast as possible — **before** adding the safety infrastructure. This was a deliberate architectural choice recorded in [ADR 001](memory-bank/decisions/001-prototype-first-approach.md).

### Files created

| File | Purpose |
|------|---------|
| `src/types/notes.ts` | Quick `Note` interface and `NoteId` brand type |
| `src/lib/storage.ts` | Raw `localStorage` read/write with basic try/catch |
| `src/features/notes/hooks/useNotesStore.ts` | Simple custom hook for CRUD + debounced persists |
| `src/features/notes/components/NoteCard.tsx` | Single note card with title, body preview, tags, delete |
| `src/features/notes/components/NoteEditor.tsx` | Create/edit form |
| `src/features/notes/components/NoteList.tsx` | Grid layout + empty state |
| `src/components/ThemeToggle.tsx` | Dark mode toggle with persisted preference |
| `src/components/ErrorBoundary.tsx` | Class-based error boundary |

### Rules applied

- **Component Safety** (`component-safety.md`):
  - Rule 1 — Every component has explicit typed props (e.g. `NoteCardProps`, `NoteEditorProps`).
  - Rule 5 — `localStorage` reads are isolated to one boot sequence in `useNotesStore`.
  - Rule 6 — Error boundary wraps the main content area.
  - Rule 7 — Fallbacks for null/missing data (`note?.title ?? "Untitled"`, `note?.body ?? "No content"`).

---

## Phase P2: Tags & Markdown

### What happened

Installed `marked` + `DOMPurify` and created a `MarkdownRenderer` component. Updated `NoteCard` to render note bodies as sanitized markdown instead of raw text.

### Rules applied

- **Data Validation** (`data-validation.md`):
  - Rule 6 — *"Prevent XSS by treating content as text"* — we use `DOMPurify.sanitize()` before setting innerHTML, never raw user input.

### Files created

| File | Purpose |
|------|---------|
| `src/components/MarkdownRenderer.tsx` | Memoized markdown renderer with DOMPurify sanitization |

---

## Phase P3: Backfill Infrastructure

### What happened

This was the retrofitting phase. We replaced the prototype's thin types and ad-hoc storage with a proper safety layer — without changing the UI.

### Changes

| File | Change |
|------|--------|
| `src/features/notes/schemas/noteSchema.ts` | **Created** — canonical Zod schemas (`NoteSchema`, `StoreSchema`), branded `NoteId`, `STORAGE_KEY` |
| `src/lib/storage.ts` | **Rewritten** — versioned store (`pt-notes:v1`), Zod validation on every read, quota check helper |
| `src/features/notes/hooks/useNotesStore.tsx` | **Rewritten** — converted to context provider with discriminated union `NotesState` type |
| `src/types/notes.ts` | **Deleted** — replaced by schema-based types |
| `src/components/StorageWarning.tsx` | **Created** — quota-warning banner |

### Rules applied

- **Data Persistence** (`data-persistence.md`):
  - Rule 1 — `localStorage` access wrapped in `try/catch` in both `loadNotes` and `saveNotes`.
  - Rule 2 — `getRemainingStorage()` checks `navigator.storage.estimate()` and warns when < 5 KB remains.
  - Rule 3 — Versioned key `pt-notes:v1` with a `version` field for future migrations.
  - Rule 4 — Deserialized data validated through Zod's `safeParse` before use; malformed entries are discarded.
  - Rule 5 — Writes are debounced at 500ms.
  - Rule 7 — Single source of truth in React context state; `localStorage` is only for boot load and persist.

- **Data Validation** (`data-validation.md`):
  - Rule 1 — *"Validate all external input with Zod schemas"* — `localStorage` reads, `JSON.parse` output, and form submissions all pass through Zod.
  - Rule 2 — `NoteSchema` enforces required fields, length limits (`title.max(200)`, `body.max(50_000)`, `tags.max(20)`).
  - Rule 3 — Uses `safeParse` instead of `parse` so failures are handled gracefully (logged, discarded) instead of throwing.
  - Rule 4 — Zod's default `strip` mode discards unknown/legacy fields on read.
  - Rule 5 — Form submissions validated via the shared `NoteSchema` before committing to state.
  - Rule 7 — Branded `NoteId` type (`string & { __brand: "NoteId" }`) prevents ID confusion.

- **Component Safety** (`component-safety.md`):
  - Rule 2 — Immutable updates via `setState` callbacks, never direct mutation.
  - Rule 4 — No `eslint-disable` for hooks deps — dependencies are explicit.

- **TypeScript Safety** (`typescript-safety.md`):
  - Rule 1 — `strict: true` enabled in `tsconfig.app.json`.
  - Rule 2 — No `any` — `JSON.parse` output typed as `unknown`, narrowed via Zod.
  - Rule 5 — Exported functions (`loadNotes`, `saveNotes`, `addNote`, etc.) have explicit return types.
  - Rule 6 — No non-null assertions (`!`) — optional chaining and fallbacks used throughout.
  - Rule 7 — Discriminated union `NotesState` ensures every UI state (loading, empty, error, loaded) is handled.

---

## Phase P4: Polish & Edge Cases

### What happened

Added search, tag filtering, and JSON export. Also recorded [ADR 001](memory-bank/decisions/001-prototype-first-approach.md).

### Rules applied

- **Component Safety** (`component-safety.md`):
  - Rule 7 — Search results handle the "no matching notes" edge case with a user-friendly message.
  - Rule 3 — Export creates a Blob URL in an event handler, not during render.

---

## How the Memory Bank Was Used

The memory bank (`/memory-bank/`) served as the project's source of truth throughout development:

| File | Role |
|------|------|
| `product-context.md` | Defined the tech stack (React + Vite + TS + TailwindCSS 4 + localStorage) |
| `conventions.md` | Set workflow rules (CLI bootstrap, feature-organized folders, utility-first CSS) |
| `decisions/` | Captured ADR 001 (prototype-first approach) |

Every architectural decision was checked against these documents. For example:
- The decision to use TailwindCSS 4 came from `product-context.md`.
- The folder structure (`features/notes/components/`, `features/notes/hooks/`) came from the *"Organize components in folders by feature"* convention.
- The choice to NOT disable the linter on `useEffect` deps came from `component-safety.md` rule 4.

## How the Agent Rules Were Used

The agent rules (`/.agents/rules/`) acted as real-time guardrails during coding. Each rule file covered a specific concern:

| Rule file | Impact on development |
|-----------|----------------------|
| `planning-priority.md` | Kept the agent in discussion mode during planning; prevented premature coding until the user gave a clear "go" signal |
| `component-safety.md` | Guided every component's props interface, side-effect placement, and error boundary usage |
| `data-persistence.md` | Dictated the storage key format, the debounce strategy, the try/catch pattern, and the quota check |
| `data-validation.md` | Mandated Zod schemas at every boundary, the branded NoteId type, and the XSS prevention via DOMPurify |
| `typescript-safety.md` | Enforced `strict: true`, banned `any`, required explicit return types, and standardized on discriminated unions |

The rules were followed even when they required rewriting prototype code. For example, the initial `storage.ts` used an unversioned key and a manual type guard for validation. When Phase P3 backfilled the infrastructure, it was rewritten to use **versioned keys** (rule 3), **Zod validation** (rule 4), **quota checks** (rule 2), and **try/catch** (rule 1) — all from `data-persistence.md`.

---

## Key Takeaways

1. **Prototype-first worked well** — Getting a visible UI quickly let us iterate on the feature set before locking in the safety infrastructure. The component APIs remained stable during the backfill, so no UI code needed changes.

2. **Memory bank + rules = faster decisions** — Having the product context and safety rules pre-written eliminated debate. When a question came up ("should we validate localStorage data?"), the answer was already documented.

3. **Backfilling safety is viable** — As long as the component boundaries are clean (typed props, separated concerns), you can swap out the underlying infrastructure (raw types → Zod schemas, simple hook → context provider) without touching UI code.