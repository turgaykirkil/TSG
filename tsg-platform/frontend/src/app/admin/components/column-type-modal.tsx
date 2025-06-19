'use client';

import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Hash, Building2, MapPin, X } from 'lucide-react';

interface ColumnTypeModalProps {
  isOpen: boolean;
  onClose: () => void;
  columnName: string;
  onSelectType: (type: 'sicil_no' | 'firma_unvani' | 'adres' | 'none') => void;
}

export function ColumnTypeModal({ 
  isOpen, 
  onClose, 
  columnName, 
  onSelectType 
}: ColumnTypeModalProps) {
  const handleSelect = (type: 'sicil_no' | 'firma_unvani' | 'adres' | 'none') => {
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
          <DialogDescription className="text-sm text-gray-600">
            <span className="font-medium">{columnName}</span> sütununu seçin:
          </DialogDescription>
          <div className="space-y-2">
            <Button 
              variant="outline" 
              className="w-full justify-start gap-2"
              onClick={() => handleSelect('sicil_no')}
            >
              <Hash className="h-4 w-4 text-blue-500" />
              <span>Sicil No</span>
            </Button>
            <Button 
              variant="outline" 
              className="w-full justify-start gap-2"
              onClick={() => handleSelect('firma_unvani')}
            >
              <Building2 className="h-4 w-4 text-green-500" />
              <span>Firma Ünvanı</span>
            </Button>
            <Button 
              variant="outline" 
              className="w-full justify-start gap-2"
              onClick={() => handleSelect('adres')}
            >
              <MapPin className="h-4 w-4 text-purple-500" />
              <span>Adres</span>
            </Button>
            <Button 
              variant="ghost" 
              className="w-full justify-start gap-2 text-gray-500 hover:text-red-500"
              onClick={() => handleSelect('none')}
            >
              <X className="h-4 w-4" />
              <span>Seçimi Kaldır</span>
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
