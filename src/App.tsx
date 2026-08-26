import { useState } from "react";
import { ThemeToggle } from "./components/ThemeToggle";
import { ErrorBoundary } from "./components/ErrorBoundary";
import { StorageWarning } from "./components/StorageWarning";
import { NoteEditor } from "./features/notes/components/NoteEditor";
import { NoteList } from "./features/notes/components/NoteList";
import { NotesProvider, useNotesStore } from "./features/notes/hooks/useNotesStore";
import type { Note } from "./features/notes/schemas/noteSchema";

function AppContent() {
  const { state, storageLow, addNote, updateNote, deleteNote } = useNotesStore();
  const [editingNote, setEditingNote] = useState<Note | null>(null);
  const [isCreating, setIsCreating] = useState(false);

  const handleSave = (title: string, body: string, tags: string[]) => {
    if (editingNote) {
      updateNote(editingNote.id, { title, body, tags });
      setEditingNote(null);
    } else {
      addNote(title, body, tags);
      setIsCreating(false);
    }
  };

  const handleCancel = () => {
    setEditingNote(null);
    setIsCreating(false);
  };

  const notes = state.status === "loaded" ? state.notes : [];

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-gray-100">
      <header className="sticky top-0 z-10 border-b border-gray-200 bg-white/80 backdrop-blur dark:border-gray-800 dark:bg-gray-900/80">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
          <h1 className="text-xl font-bold">Notes</h1>
          <div className="flex items-center gap-2">
            {!isCreating && !editingNote && state.status !== "loading" && (
              <button
                onClick={() => setIsCreating(true)}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600"
              >
                + New Note
              </button>
            )}
            <ThemeToggle />
          </div>
        </div>
      </header>

      <StorageWarning visible={storageLow} />

      <main className="mx-auto max-w-5xl px-4 py-8">
        <ErrorBoundary>
          {state.status === "loading" && (
            <div className="flex items-center justify-center py-12">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent" />
            </div>
          )}

          {state.status === "error" && (
            <div className="rounded-lg border border-red-300 bg-red-50 p-4 text-red-800 dark:border-red-700 dark:bg-red-900/30 dark:text-red-300">
              <p className="font-semibold">Failed to load notes</p>
              <p className="mt-1 text-sm">{state.error}</p>
            </div>
          )}

          {(isCreating || editingNote) && (
            <div className="mb-8 rounded-lg border border-gray-200 bg-white p-6 shadow-sm dark:border-gray-700 dark:bg-gray-800">
              <NoteEditor
                note={editingNote}
                onSave={handleSave}
                onCancel={handleCancel}
              />
            </div>
          )}

          {state.status === "loaded" && (
            <NoteList
              notes={state.notes}
              onDelete={deleteNote}
              onEdit={setEditingNote}
            />
          )}
        </ErrorBoundary>
      </main>
    </div>
  );
}

function App() {
  return (
    <NotesProvider>
      <AppContent />
    </NotesProvider>
  );
}

export default App;
