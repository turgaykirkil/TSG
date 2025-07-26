"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { ZoomIn, ZoomOut, Expand, Search } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { OcrPagePreview, OcrPreviewResponse, OcrTextLine } from "@/lib/types";

interface OcrTechnicalPreviewProps {
  preview: OcrPreviewResponse | null;
}

const OcrTechnicalPreview: React.FC<OcrTechnicalPreviewProps> = ({ preview }) => {

  if (!preview) {
    return null; // Or a placeholder/message when no preview data is available
  }

  return (
    <div className="space-y-8">
      {preview.pages.map((page: OcrPagePreview) => (
        <Card key={page.page_number} className="overflow-hidden shadow-lg rounded-lg">
          <CardHeader>
            <CardTitle>Sayfa {page.page_number}</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <TooltipProvider delayDuration={100}>
              <div className="flex h-[calc(100vh-300px)] bg-gray-50 dark:bg-gray-900">
                {/* Left Panel: Image Viewer */}
                <div className="flex-1 flex flex-col overflow-hidden">
                  <div className="flex items-center justify-between p-2 border-b bg-white dark:bg-gray-800">
                    <h5 className="font-semibold text-sm">Sayfa {page.page_number} / {preview.pages.length}</h5>
                    <div className="flex items-center gap-1">
                      <Button variant="ghost" size="icon" className="h-8 w-8"><ZoomIn className="h-4 w-4" /></Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8"><ZoomOut className="h-4 w-4" /></Button>
                      <Button variant="ghost" size="icon" className="h-8 w-8"><Expand className="h-4 w-4" /></Button>
                    </div>
                  </div>
                  <div className="flex-1 overflow-auto p-4 bg-gray-200 dark:bg-gray-700">
                    <div
                      className="relative mx-auto shadow-2xl"
                      style={{ width: 'fit-content' }}
                    >
                      <img
                        src={page.image_base64}
                        alt={`Sayfa ${page.page_number}`}
                        className="select-none border border-gray-300 dark:border-gray-600"
                      />
                      {page.lines.map((line: OcrTextLine, index: number) => {
                        const [x1, y1, x2, y2] = line.bbox;
                        return (
                          <Tooltip key={`box-tooltip-${index}`}>
                            <TooltipTrigger asChild>
                              <div
                                className="absolute border-2 border-primary/70 bg-primary/20 hover:bg-primary/40 hover:border-primary cursor-pointer transition-colors duration-150 rounded-sm"
                                style={{
                                  left: `${x1}px`,
                                  top: `${y1}px`,
                                  width: `${x2 - x1}px`,
                                  height: `${y2 - y1}px`,
                                }}
                              />
                            </TooltipTrigger>
                            <TooltipContent side="top" align="center" className="max-w-xs text-center bg-gray-900 text-white rounded-md p-2 text-xs shadow-lg">
                              <p>{line.text}</p>
                            </TooltipContent>
                          </Tooltip>
                        );
                      })}
                    </div>
                  </div>
                </div>

                {/* Right Panel: Recognized Text */}
                <div className="w-1/3 max-w-md border-l flex flex-col bg-white dark:bg-gray-800">
                  <div className="p-3 border-b flex items-center gap-2 sticky top-0 bg-white dark:bg-gray-800 z-10">
                    <Search className="h-4 w-4 text-muted-foreground" />
                    <h4 className="font-semibold tracking-tight">Tanınan Metin</h4>
                  </div>
                  <div className="flex-grow overflow-y-auto p-1">
                     <ul className="space-y-1 p-2">
                      {page.lines.map((line: OcrTextLine, index: number) => (
                        <li 
                          key={`text-${index}`}
                          className="p-2 rounded-md font-mono text-xs hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer transition-colors duration-150"
                        >
                          {line.text}
                        </li>
                      ))}
                    </ul> 
                  </div>
                </div>
              </div>
            </TooltipProvider>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default OcrTechnicalPreview;
