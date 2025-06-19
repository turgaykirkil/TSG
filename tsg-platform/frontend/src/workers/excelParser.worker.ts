/* eslint-disable no-restricted-globals */
import { processExcelFile } from '@/lib/file-utils';

// Worker mesaj türü
interface WorkerRequest {
  fileId: string;
  file: File;
}

interface WorkerResponse {
  fileId: string;
  result: ReturnType<typeof processExcelFile> extends Promise<infer R> ? R : never;
}

self.onmessage = async (event: MessageEvent<WorkerRequest>) => {
  const { fileId, file } = event.data;
  try {
    const result = await processExcelFile(file);
    const response: WorkerResponse = { fileId, result } as any;
    // @ts-ignore
    self.postMessage(response);
  } catch (error) {
    const response: WorkerResponse = { fileId, result: { success: false, fileName: file.name, sheets: [], error: (error as Error).message } } as any;
    // @ts-ignore
    self.postMessage(response);
  }
};
