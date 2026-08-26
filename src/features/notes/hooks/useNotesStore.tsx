import { createContext, useContext, useCallback, useEffect, useRef, useState, type ReactNode } from "react";
import { loadNotes, saveNotes, getRemainingStorage } from "../../../lib/storage";
import { createNoteId, NoteSchema } from "../schemas/noteSchema";
import type { Note, NoteId } from "../schemas/noteSchema";

export type NotesState =
  | { status: "loading" }
  | { status: "empty" }
  | { status: "error"; error: string }
  | { status: "loaded"; notes: Note[] };

interface NotesStoreContextValue {
  state: NotesState;
  storageLow: boolean;
  addNote: (title: string, body: string, tags?: string[]) => void;
  updateNote: (id: NoteId, updates: Partial<Pick<Note, "title" | "body" | "tags">>) => void;
  deleteNote: (id: NoteId) => void;
}

const NotesStoreContext = createContext<NotesStoreContextValue | null>(null);

export function NotesProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<NotesState>({ status: "loading" });
  const [storageLow, setStorageLow] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);

  // Boot: load notes from storage
  useEffect(() => {
    try {
      const notes = loadNotes();
      setState(
        notes.length === 0
          ? { status: "empty" }
          : { status: "loaded", notes }
      );
    } catch (err) {
      setState({ status: "error", error: String(err) });
    }

    // Check storage quota
    getRemainingStorage().then((remaining) => {
      if (remaining < 5_000) setStorageLow(true);
    });
  }, []);

  const persist = useCallback((updated: Note[]) => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => {
      const ok = saveNotes(updated);
      if (!ok) setStorageLow(true);
    }, 500);
  }, []);

  useEffect(() => {
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, []);

  const addNote = useCallback(
    (title: string, body: string, tags: string[] = []) => {
      const now = Date.now();
      const parsed = NoteSchema.safeParse({
        id: createNoteId(),
        title,
        body,
        tags,
        createdAt: now,
        updatedAt: now,
      });
      if (!parsed.success) return;
      const note = parsed.data;
      setState((prev) => {
        const currentNotes = prev.status === "loaded" ? prev.notes : [];
        const updated = [note, ...currentNotes];
        persist(updated);
        return { status: "loaded", notes: updated };
      });
    },
    [persist]
  );

  const updateNote = useCallback(
    (id: NoteId, updates: Partial<Pick<Note, "title" | "body" | "tags">>) => {
      setState((prev) => {
        if (prev.status !== "loaded") return prev;
        const updated = prev.notes.map((n) =>
          n.id === id ? { ...n, ...updates, updatedAt: Date.now() } : n
        );
        persist(updated);
        return { status: "loaded", notes: updated };
      });
    },
    [persist]
  );

  const deleteNote = useCallback(
    (id: NoteId) => {
      setState((prev) => {
        if (prev.status !== "loaded") return prev;
        const updated = prev.notes.filter((n) => n.id !== id);
        persist(updated);
        return updated.length === 0
          ? { status: "empty" }
          : { status: "loaded", notes: updated };
      });
    },
    [persist]
  );

  return (
    <NotesStoreContext.Provider value={{ state, storageLow, addNote, updateNote, deleteNote }}>
      {children}
    </NotesStoreContext.Provider>
  );
}

export function useNotesStore(): NotesStoreContextValue {
  const ctx = useContext(NotesStoreContext);
  if (!ctx) throw new Error("useNotesStore must be used within NotesProvider");
  return ctx;
}