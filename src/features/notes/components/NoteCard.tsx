import type { Note, NoteId } from "../../../features/notes/schemas/noteSchema";
import { MarkdownRenderer } from "../../../components/MarkdownRenderer";

export interface NoteCardProps {
  note: Note;
  onDelete: (id: NoteId) => void;
  onEdit: (note: Note) => void;
}

export function NoteCard({ note, onDelete, onEdit }: NoteCardProps) {
  return (
    <article className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition hover:shadow-md dark:border-gray-700 dark:bg-gray-800">
      <div className="mb-2 flex items-start justify-between">
        <h2
          className="cursor-pointer text-lg font-semibold text-gray-900 dark:text-gray-100"
          onClick={() => onEdit(note)}
        >
          {note.title || "Untitled"}
        </h2>
        <button
          onClick={() => onDelete(note.id)}
          className="ml-2 rounded p-1 text-gray-400 hover:text-red-500 dark:hover:text-red-400"
          aria-label="Delete note"
        >
          <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>

      <div className="mb-3 line-clamp-6 text-sm text-gray-600 dark:text-gray-400">
        {note.body ? (
          <MarkdownRenderer content={note.body} />
        ) : (
          "No content"
        )}
      </div>

      {note.tags.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {note.tags.map((tag) => (
            <span
              key={tag}
              className="rounded-full bg-blue-100 px-2 py-0.5 text-xs text-blue-700 dark:bg-blue-900 dark:text-blue-300"
            >
              {tag}
            </span>
          ))}
        </div>
      )}

      <time className="mt-2 block text-xs text-gray-400 dark:text-gray-500">
        {new Date(note.updatedAt).toLocaleDateString()}
      </time>
    </article>
  );
}