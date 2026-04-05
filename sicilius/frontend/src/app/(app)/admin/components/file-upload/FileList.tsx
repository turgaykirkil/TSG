import { Icons } from "@/components/icons";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import type { CustomFile } from "@/lib/types/file.types";
import { formatFileSize } from "@/lib/utils/file-utils";

interface FileListProps {
  files: CustomFile[];
  onRemove: (fileId: string) => void;
}

export function FileList({ files, onRemove }: FileListProps) {
  if (files.length === 0) return null;

  return (
    <div className="space-y-2">
      {files.map((file) => (
        <div
          key={file.id}
          className="border rounded-lg p-4 flex items-center justify-between"
        >
          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-2">
              <Icons.file className="h-5 w-5 text-muted-foreground" />
              <div className="truncate">
                <p className="text-sm font-medium truncate">{file.name}</p>
                <p className="text-xs text-muted-foreground">
                  {formatFileSize(file.size)}
                  {file.status === 'processing' && ' • İşleniyor...'}
                  {file.status === 'success' && ' • Başarılı'}
                  {file.error && ` • Hata: ${file.error}`}
                </p>
              </div>
            </div>
            {file.status === 'processing' && (
              <Progress value={file.progress} className="h-2 mt-2" />
            )}
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={(e) => {
              e.stopPropagation();
              onRemove(file.id);
            }}
            disabled={file.status === 'processing'}
          >
            <Icons.trash className="h-4 w-4 text-destructive" />
          </Button>
        </div>
      ))}
    </div>
  );
}
