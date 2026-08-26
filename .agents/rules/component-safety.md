# Component Safety Rules

> Scope: React component structure, props, rendering, and side effects.

## Rules

1. **Every component must have explicit, typed props** — Use an interface or
   type alias exported alongside the component. Never use `any` or implicit
   `children` without declaring it.

   ```typescript
   // Good
   export interface NoteCardProps {
     note: Note;
     onDelete: (id: NoteId) => void;
     className?: string;
   }
   export function NoteCard({ note, onDelete, className }: NoteCardProps) { ... }

   // Bad
   export function NoteCard(props: any) { ... }
   ```

2. **Never mutate props or state directly** — All state updates must go through
   `useState` setters, `useReducer` dispatches, or an immutable state library.
   No direct `state.items.push(...)`.

3. **Keep side effects in `useEffect` or event handlers** — Render logic
   (the function body / JSX) must be pure: no `localStorage.setItem`,
   no `fetch`, no `document.title` assignments.

4. **Always list explicit `useEffect` dependencies** — Never suppress the
   linter with `// eslint-disable-next-line react-hooks/exhaustive-deps`.
   If a dependency causes an infinite loop, restructure the logic, don't
   hide it.

5. **Isolate localStorage reads to one boot sequence** — Read from localStorage
   once in a provider or a custom hook (e.g. `useNotesStore`), not spread
   across individual components.

6. **Use React Error Boundaries** — Wrap the note editor and note list in
   separate error boundaries so a crash in one area doesn't take down the
   whole app. Log errors via `componentDidCatch` or the `onError` callback.

7. **Guard against render-time exceptions** — When rendering user content
   (note titles, bodies), always provide a fallback for null/undefined/malformed
   data. Leaning on optional chaining and default values is preferred.

   ```typescript
   // Good
   <h2>{note?.title ?? "Untitled"}</h2>

   // Bad — silently renders nothing
   <h2>{note?.title}</h2>
   ```