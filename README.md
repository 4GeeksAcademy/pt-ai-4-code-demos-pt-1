# Notes App

A single-page note-taking app built with **React 19**, **Vite**, **TypeScript (strict)**, **TailwindCSS 4**, and **Zod**.

## Features

- **Full CRUD** — Create, read, update, and delete notes
- **Markdown support** — Write notes in markdown, rendered via `marked` + sanitized with `DOMPurify`
- **Tags** — Categorize notes with tags; filter by tag
- **Search** — Full-text search across titles and bodies
- **Dark mode** — Toggle with persisted preference
- **Export** — Download all notes as a JSON file
- **Safe storage** — Versioned `localStorage` (`pt-notes:v1`) with Zod runtime validation, debounced writes, and quota monitoring

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | React 19 |
| Bundler | Vite 8 |
| Language | TypeScript (strict mode) |
| Styling | TailwindCSS 4 (utility-first) |
| Validation | Zod 4 |
| Markdown | marked + DOMPurify |
| Persistence | localStorage (versioned, validated) |

## Getting Started

```bash
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server with HMR |
| `npm run build` | Type-check and build for production |
| `npm run preview` | Preview the production build |
| `npm run lint` | Run ESLint |

## Project Structure

```
src/
├── App.tsx                                 # Root shell with NotesProvider
├── main.tsx                                # Entry point
├── index.css                               # Tailwind entry (@import "tailwindcss")
├── components/
│   ├── ErrorBoundary.tsx                   # React error boundary for crash isolation
│   ├── MarkdownRenderer.tsx                # Safe markdown → HTML via marked + DOMPurify
│   ├── StorageWarning.tsx                  # Low-storage quota warning banner
│   └── ThemeToggle.tsx                     # Dark mode toggle (persisted to localStorage)
├── features/notes/
│   ├── schemas/
│   │   └── noteSchema.ts                  # Canonical Zod schemas (Note, StoreV1), branded NoteId
│   ├── hooks/
│   │   └── useNotesStore.tsx              # Context provider with discriminated union state
│   └── components/
│       ├── NoteCard.tsx                   # Note card: markdown body, tags, delete
│       ├── NoteEditor.tsx                 # Create/edit form with Zod-backed validation
│       └── NoteList.tsx                   # Search bar, tag filter, export button, grid layout
└── lib/
    └── storage.ts                         # localStorage abstraction: try/catch, quota, Zod validation
```

## Architecture

### Data Flow

```
User Input → Form Component → useNotesStore (React Context) → React State
                                                                   ↓
                                                              storage.ts (debounced 500ms)
                                                                   ↓
                                                              localStorage (pt-notes:v1)
```

### State Model

Notes are managed through a discriminated union:

```typescript
type NotesState =
  | { status: "loading" }
  | { status: "empty" }
  | { status: "error"; error: string }
  | { status: "loaded"; notes: Note[] };
```

Every component handles all states — loading, empty, error, and data.

### Storage Schema

Data is stored under the key `pt-notes:v1` in a versioned JSON blob:

```typescript
interface StoreV1 {
  version: 1;
  notes: Note[];
  updatedAt: number;
}
```

On every read, the blob is validated against a Zod schema. Malformed data is silently discarded with a warning, rather than crashing the app.

## Safety & Edge Cases

| Concern | Mitigation |
|---------|-----------|
| Corrupted localStorage | Zod `safeParse` — discards malformed records with console warning |
| Storage quota exceeded | `try/catch` on write; `navigator.storage.estimate()` quota check |
| Private browsing | `try/catch` around all `localStorage` access (Safari throws) |
| XSS | Markdown rendered via `DOMPurify.sanitize()` — never `dangerouslySetInnerHTML` with raw user content |
| Component crash | `ErrorBoundary` wraps note editor and note list independently |
| Rapid writes | 500ms debounce before persisting to `localStorage` |
| Type confusion | Branded `NoteId` type prevents ID mix-ups |
| Missing/null data | Optional chaining + `??` fallbacks in all render paths |
