'use client';
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Hash, Building2, MapPin, Library, X } from 'lucide-react';
import type { ColumnType } from '@/hooks/useColumnMapper';

interface ColumnTypeModalProps {
  isOpen: boolean;
  onClose: () => void;
  columnName: string;
  onSelectType: (type: ColumnType) => void;
}

const typeOptions: { value: ColumnType; label: string; icon: React.ElementType }[] = [
  { value: 'sicil_no', label: 'Sicil No', icon: Hash },
  { value: 'firma_unvani', label: 'Firma Ünvanı', icon: Building2 },
  { value: 'adres', label: 'Adres', icon: MapPin },
  { value: 'sicil_mudurluk', label: 'Sicil Müdürlüğü', icon: Library },
];

export function ColumnTypeModal({ isOpen, onClose, columnName, onSelectType }: ColumnTypeModalProps) {
  const handleSelect = (type: ColumnType) => {
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
            <span className="font-medium">{`"${columnName}"`}</span> sütununu aşağıdaki veri tiplerinden biriyle eşleştirin:
          </DialogDescription>
          <div className="space-y-2">
            {typeOptions.map(({ value, label, icon: Icon }) => (
              <Button
                key={value}
                variant="outline"
                className="w-full justify-start gap-2"
                onClick={() => handleSelect(value)}
              >
                <Icon className="h-4 w-4" />
                <span>{label}</span>
              </Button>
            ))}
            <Button
              variant="ghost"
              className="w-full justify-start gap-2 text-gray-500 hover:text-red-500"
              onClick={() => handleSelect('none')}
            >
              <X className="h-4 w-4" />
              <span>Eşleştirmeyi Kaldır</span>
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
