import { processExcelFile, type ExcelProcessResult } from '@/lib/file-utils';

interface WorkerRequest {
  fileId: string;
  file: File;
}

interface WorkerSuccessResponse {
  type: 'SUCCESS';
  fileId: string;
  result: ExcelProcessResult;
}

interface WorkerErrorResponse {
  type: 'ERROR';
  fileId: string;
  error: string;
}



self.onmessage = async (event: MessageEvent<WorkerRequest>) => {
  const { fileId, file } = event.data;

  try {
    const result = await processExcelFile(file);
    const response: WorkerSuccessResponse = { type: 'SUCCESS', fileId, result };
    postMessage(response);
  } catch (e) {
    const errorMessage = e instanceof Error ? e.message : 'Bilinmeyen bir worker hatası oluştu';
    const response: WorkerErrorResponse = { type: 'ERROR', fileId, error: errorMessage };
    postMessage(response);
  }
};
