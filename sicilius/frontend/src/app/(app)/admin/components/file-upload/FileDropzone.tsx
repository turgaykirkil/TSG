import { useDropzone } from "react-dropzone";
import { Icons } from "@/components/icons";
import { FILE_TYPES } from "@/lib/constants/mudurlukler";

interface FileDropzoneProps {
  onDrop: (files: File[]) => void;
  isDragActive: boolean;
  disabled?: boolean;
}

export function FileDropzone({ onDrop, isDragActive, disabled }: FileDropzoneProps) {
  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
      ...FILE_TYPES.EXCEL.reduce((acc, type) => ({ ...acc, [type]: ['.xlsx', '.xls'] }), {}),
      ...FILE_TYPES.PDF.reduce((acc, type) => ({ ...acc, [type]: ['.pdf'] }), {}),
    },
    multiple: true,
    disabled,
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
        isDragActive ? 'border-primary bg-primary/10' : 'border-muted-foreground/25 hover:border-primary/50'
      } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center justify-center space-y-2">
        <Icons.upload className="h-10 w-10 text-muted-foreground" />
        <p className="text-sm text-muted-foreground">
          {isDragActive
            ? 'Dosyaları buraya bırakın'
            : 'Sürükleyip bırakın veya tıklayarak seçin'}
        </p>
        <p className="text-xs text-muted-foreground">
          Excel veya PDF dosyaları (Max: 10MB)
        </p>
      </div>
    </div>
  );
}
