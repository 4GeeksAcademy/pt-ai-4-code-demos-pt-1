# Data Integrity & Validation Safety Rules

> Scope: Input validation, data schemas, type safety at runtime boundaries.

## Rules

1. **Validate all external input with Zod schemas** — Every piece of data
   entering the app from `localStorage`, URL params, or user input must pass
   through a Zod schema at the boundary. Never trust raw `JSON.parse` output.

2. **Define note shape as a strict schema** — The `Note` type must have a
   canonical Zod schema that enforces required fields, length limits, and
   formats.

   ```typescript
   export const NoteSchema = z.object({
     id: z.string().uuid(),
     title: z.string().min(1).max(200),
     body: z.string().max(50_000),
     tags: z.array(z.string().max(50)).max(20).default([]),
     createdAt: z.number().positive(),
     updatedAt: z.number().positive(),
   });
   export type Note = z.infer<typeof NoteSchema>;
   ```

3. **Reject, don't coerce silently** — When validation fails, reject the data
   and log a clear message. Prefer `safeParse` over `parse` so the caller can
   choose how to handle failure (e.g. show a toast, skip the bad record).

4. **Strip unknown fields on read** — Zod's `strip` method (the default) is
   fine for localStorage reads — you want to discard unknown/legacy fields
   rather than keep them around.

5. **Never trust `event.target.value` raw** — Always validate form submissions
   client-side before committing to state or persistence. Use Zod schemas
   shared between the form component and the validation boundary.

6. **Prevent XSS by treating content as text** — Notes contain user-authored
   text. Never dangerously set innerHTML with note content. Render all note
   bodies as plain text or through a safe markdown renderer (e.g.
   `marked` with sanitization enabled).

7. **Use branded types for identifiers** — Avoid passing raw strings/numbers
   where typed IDs are expected. Use branded types to catch ID confusion at
   the type level:

   ```typescript
   export type NoteId = string & { __brand: "NoteId" };
   ```