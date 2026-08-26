import { z } from "zod";

export type NoteId = string & { __brand: "NoteId" };

export const NoteIdSchema = z.string().uuid() as z.ZodType<NoteId>;

export const NoteSchema = z.object({
  id: NoteIdSchema,
  title: z.string().min(1).max(200),
  body: z.string().max(50_000),
  tags: z.array(z.string().max(50)).max(20).default([]),
  createdAt: z.number().positive(),
  updatedAt: z.number().positive(),
});

export type Note = z.infer<typeof NoteSchema>;

export function createNoteId(): NoteId {
  return crypto.randomUUID() as NoteId;
}

export const StoreSchema = z.object({
  version: z.literal(1),
  notes: z.array(NoteSchema),
  updatedAt: z.number().positive(),
});

export type StoreV1 = z.infer<typeof StoreSchema>;

export const STORAGE_KEY = "pt-notes:v1";