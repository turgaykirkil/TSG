import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';

// --- Types ---

export interface ParsedTable {
  table_name: string;
  headers: string[];
  rows: Record<string, any>[];
}

interface ParsePdfResponse {
  data: ParsedTable[];
  error: string | null;
}

const parsePdfApi = async (file: File): Promise<ParsedTable[]> => {
  const formData = new FormData();
  formData.append('file', file);

  const apiUrl = process.env.NEXT_PUBLIC_PDF_PARSER_URL;
  if (!apiUrl) {
    throw new Error('PDF parser API URL is not configured. Please set NEXT_PUBLIC_PDF_PARSER_URL in your environment variables.');
  }

  const response = await fetch(apiUrl, {
    method: 'POST',
    body: formData,
    // Note: Don't set 'Content-Type' header, browser does it for multipart/form-data
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'An unknown error occurred.' }));
    throw new Error(errorData.detail || 'Failed to parse PDF');
  }

  return response.json();
};

export const usePDFParser = () => {
  const [parsedTables, setParsedTables] = useState<ParsedTable[]>([]);

  const mutation = useMutation<ParsedTable[], Error, File>({ 
    mutationFn: parsePdfApi,
    onSuccess: (data) => {
      setParsedTables(data);
    },
    // onError is handled by the component via mutation.isError and mutation.error
  });

  const parsePdf = (file: File) => {
    if (!file) return;
    // Reset state before a new upload
    setParsedTables([]);
    mutation.mutate(file);
  };

  return {
    parsePdf,
    parsedTables,
    isLoading: mutation.isPending,
    error: mutation.error,
    isSuccess: mutation.isSuccess,
    reset: () => {
        mutation.reset();
        setParsedTables([]);
    }
  };
};
