'use client';

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

interface ColumnTypeModalProps {
  isOpen: boolean;
  onClose: () => void;
  columnName: string;
  onSelectType: (type: 'sicil_no' | 'firma_unvani' | 'none') => void;
}

export function ColumnTypeModal({ 
  isOpen, 
  onClose, 
  columnName, 
  onSelectType 
}: ColumnTypeModalProps) {
  const handleSelect = (type: 'sicil_no' | 'firma_unvani' | 'none') => {
    onSelectType(type);
    onClose();
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Sütun Türünü Seçin</DialogTitle>
        </DialogHeader>
        <div className="space-y-4 py-4">
          <p className="text-sm text-gray-600">
            <span className="font-medium">{columnName}</span> sütununu seçin:
          </p>
          <div className="space-y-2">
            <Button 
              variant="outline" 
              className="w-full justify-start"
              onClick={() => handleSelect('sicil_no')}
            >
              Sicil No
            </Button>
            <Button 
              variant="outline" 
              className="w-full justify-start"
              onClick={() => handleSelect('firma_unvani')}
            >
              Firma Ünvanı
            </Button>
            <Button 
              variant="ghost" 
              className="w-full justify-start text-gray-500"
              onClick={() => handleSelect('none')}
            >
              Seçimi Kaldır
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
