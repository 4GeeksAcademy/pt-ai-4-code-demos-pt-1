# TypeScript Safety Rules

> Scope: TypeScript configuration, strictness, type boundaries, and linting.

## Rules

1. **`strict: true` is mandatory in `tsconfig`** — The project config must have
   `strict: true` enabled at all times. Never disable `strictNullChecks`,
   `noImplicitAny`, or `strictFunctionTypes` on a per-file basis.

2. **No `any` — use `unknown` instead** — When you don't know the type of a
   value (e.g. `JSON.parse` output), type it as `unknown` and narrow with a
   type guard or Zod schema. `any` disables the type checker and is banned.

   ```typescript
   // Good
   const raw: unknown = JSON.parse(data);
   const notes = NoteSchema.array().parse(raw);

   // Bad
   const notes: any = JSON.parse(data);
   ```

3. **Prefer `const` assertions for constants** — Use `as const` for enum-like
   objects, action types, and configuration tuples so the literal types flow
   through.

4. **Lint with `@typescript-eslint/strict`** — Enable the strict-type-checked
   plugin. Key rules:
   - `@typescript-eslint/no-unsafe-*` — catches unsafe any usage
   - `@typescript-eslint/no-floating-promises` — no unhandled promises
   - `@typescript-eslint/no-unused-vars` with `"error"` — no dead code

5. **Exported functions must have explicit return types** — Relying on
   inferred return types for public APIs makes it easy to accidentally
   change a contract. Private helpers may stay inferred.

6. **Ban `!` (non-null assertion operator)** — Use a type guard or optional
   chaining instead. `!` hides real null-safety bugs.

   ```typescript
   // Good
   if (note === null) { /* handle */ }
   note.title

   // Bad
   note!.title
   ```

7. **Use discriminated unions for component state** — Model multi-state
   UI (loading, empty, error, data) as a discriminated union so the
   compiler ensures every case is handled.

   ```typescript
   type NotesState =
     | { status: "loading" }
     | { status: "empty" }
     | { status: "error"; error: string }
     | { status: "loaded"; notes: Note[] };
   ```