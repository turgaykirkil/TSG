"use client";

interface ResultsHeaderProps {
  title: string;
  count?: number;
}

export default function ResultsHeader({ title, count }: ResultsHeaderProps) {
  return (
    <div className="flex items-center justify-between mb-2">
      <h2 className="text-lg font-semibold" style={{ color: '#0A192F' }}>{title}</h2>
      {typeof count === 'number' && (
        <span className="text-xs text-muted-foreground">{count} kayıt</span>
      )}
    </div>
  );
}
