import { StoreSchema, STORAGE_KEY } from "../features/notes/schemas/noteSchema";
import type { Note } from "../features/notes/schemas/noteSchema";

export async function getRemainingStorage(): Promise<number> {
  if (!navigator.storage?.estimate) return Infinity;
  const { quota, usage } = await navigator.storage.estimate();
  if (quota === undefined || usage === undefined) return Infinity;
  return quota - usage;
}

export function loadNotes(): Note[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];

    const parsed: unknown = JSON.parse(raw);
    const result = StoreSchema.safeParse(parsed);

    if (!result.success) {
      console.warn("Malformed store data, resetting:", result.error.issues);
      return [];
    }

    return result.data.notes;
  } catch (err) {
    console.error("Failed to load notes from localStorage:", err);
    return [];
  }
}

export function saveNotes(notes: Note[]): boolean {
  try {
    const payload = {
      version: 1 as const,
      notes,
      updatedAt: Date.now(),
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
    return true;
  } catch (err) {
    if (err instanceof DOMException && err.name === "QuotaExceededError") {
      console.error("Storage quota exceeded");
    } else {
      console.error("Failed to save notes:", err);
    }
    return false;
  }
}