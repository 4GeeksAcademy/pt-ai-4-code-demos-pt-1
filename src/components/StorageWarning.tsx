export interface StorageWarningProps {
  visible: boolean;
}

export function StorageWarning({ visible }: StorageWarningProps) {
  if (!visible) return null;

  return (
    <div className="mx-auto mt-4 max-w-5xl px-4">
      <div className="rounded-lg border border-amber-300 bg-amber-50 p-3 text-sm text-amber-800 dark:border-amber-700 dark:bg-amber-900/30 dark:text-amber-300">
        <span className="font-semibold">⚠️ Storage almost full</span> — Consider exporting or deleting old notes.
      </div>
    </div>
  );
}