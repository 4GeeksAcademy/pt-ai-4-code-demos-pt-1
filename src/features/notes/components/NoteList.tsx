import { useState, useMemo } from "react";
import type { Note, NoteId } from "../../../features/notes/schemas/noteSchema";
import { NoteCard } from "./NoteCard";

export interface NoteListProps {
  notes: Note[];
  onDelete: (id: NoteId) => void;
  onEdit: (note: Note) => void;
}

export function NoteList({ notes, onDelete, onEdit }: NoteListProps) {
  const [search, setSearch] = useState("");
  const [tagFilter, setTagFilter] = useState("");

  const allTags = useMemo(() => {
    const tagSet = new Set<string>();
    notes.forEach((n) => n.tags.forEach((t) => tagSet.add(t)));
    return Array.from(tagSet).sort();
  }, [notes]);

  const filtered = useMemo(() => {
    let result = notes;

    if (search.trim()) {
      const q = search.toLowerCase();
      result = result.filter(
        (n) =>
          n.title.toLowerCase().includes(q) ||
          n.body.toLowerCase().includes(q)
      );
    }

    if (tagFilter) {
      result = result.filter((n) => n.tags.includes(tagFilter));
    }

    return result;
  }, [notes, search, tagFilter]);

  if (notes.length === 0) {
    return (
      <div className="py-12 text-center text-gray-500 dark:text-gray-400">
        <p className="text-lg">No notes yet</p>
        <p className="mt-1 text-sm">Create your first note to get started!</p>
      </div>
    );
  }

  return (
    <div>
      {/* Filters */}
      <div className="mb-6 flex flex-wrap gap-3">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search notes..."
          className="min-w-[200px] flex-1 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 dark:placeholder-gray-500"
        />

        {allTags.length > 0 && (
          <select
            value={tagFilter}
            onChange={(e) => setTagFilter(e.target.value)}
            className="rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100"
          >
            <option value="">All tags</option>
            {allTags.map((tag) => (
              <option key={tag} value={tag}>{tag}</option>
            ))}
          </select>
        )}
      </div>

      {/* Note count & export */}
      <div className="mb-4 flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
        <span>{filtered.length} of {notes.length} notes</span>
        <ExportButton notes={notes} />
      </div>

      {/* Notes grid */}
      {filtered.length === 0 ? (
        <div className="py-12 text-center text-gray-500 dark:text-gray-400">
          <p className="text-lg">No matching notes</p>
          <p className="mt-1 text-sm">Try a different search term or tag</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {filtered.map((note) => (
            <NoteCard
              key={note.id}
              note={note}
              onDelete={onDelete}
              onEdit={onEdit}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function ExportButton({ notes }: { notes: Note[] }) {
  const handleExport = () => {
    const blob = new Blob([JSON.stringify(notes, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `notes-export-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <button
      onClick={handleExport}
      className="rounded-lg border border-gray-300 px-3 py-1 text-xs hover:bg-gray-100 dark:border-gray-600 dark:hover:bg-gray-700"
    >
      Export JSON
    </button>
  );
}