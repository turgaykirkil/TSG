'use client';

import React, { createContext, useContext, useState, ReactNode, useCallback } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

export type AlertVariant = 'info' | 'success' | 'warning' | 'destructive';

export type AlertPayload = {
  title: string;
  description?: string;
  variant?: AlertVariant;
  onClose?: () => void;
};

type AlertContextType = {
  showAlert: (payload: AlertPayload) => void;
  hideAlert: () => void;
};

const AlertContext = createContext<AlertContextType | undefined>(undefined);

export function AlertProvider({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(false);
  const [payload, setPayload] = useState<AlertPayload | null>(null);

  const hideAlert = useCallback(() => {
    setOpen(false);
    if (payload?.onClose) payload.onClose();
    // küçük bir gecikme ile payload'ı temizle
    setTimeout(() => setPayload(null), 150);
  }, [payload]);

  const showAlert = useCallback((p: AlertPayload) => {
    setPayload(p);
    setOpen(true);
  }, []);

  return (
    <AlertContext.Provider value={{ showAlert, hideAlert }}>
      {children}
      <Dialog open={open} onOpenChange={(o) => { if (!o) hideAlert(); }}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{payload?.title || 'Bilgi'}</DialogTitle>
            {payload?.description && (
              <DialogDescription>{payload.description}</DialogDescription>
            )}
          </DialogHeader>
          <div className="pt-2 flex justify-end">
            <Button onClick={hideAlert}>Tamam</Button>
          </div>
        </DialogContent>
      </Dialog>
    </AlertContext.Provider>
  );
}

export function useAlert() {
  const ctx = useContext(AlertContext);
  if (!ctx) throw new Error('useAlert must be used within an AlertProvider');
  return ctx;
}
