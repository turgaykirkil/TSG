// PDF.js için tip tanımlamaları
declare module 'pdfjs-dist/build/pdf' {
  interface PDFPageProxy {
    getTextContent: () => Promise<{
      items: Array<{ str: string }>;
    }>;
  }

  interface PDFDocumentProxy {
    numPages: number;
    getPage: (pageNumber: number) => Promise<PDFPageProxy>;
  }

  interface PDFLoadingTask {
    promise: Promise<PDFDocumentProxy>;
  }

  interface GlobalWorkerOptionsType {
    workerSrc: string;
  }

  interface PDFJSStatic {
    version: string;
    getDocument: (options: { data: ArrayBuffer }) => PDFLoadingTask;
    GlobalWorkerOptions: GlobalWorkerOptionsType;
  }

  const pdfjsLib: PDFJSStatic;
  export = pdfjsLib;
}

declare module 'pdfjs-dist/build/pdf.worker.entry' {
  const workerSrc: string;
  export = workerSrc;
}

declare module 'pdfjs-dist/build/pdf.worker.min' {
  const workerSrc: string;
  export = workerSrc;
}
