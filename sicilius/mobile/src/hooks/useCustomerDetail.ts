import { useState, useEffect } from 'react';
import customerService from '../services/customerService';
import { Customer } from '../types/customer';

interface UseCustomerDetailProps {
  customerId?: string;
  customerData?: Customer;
}

interface UseCustomerDetailReturn {
  customer: Customer | null;
  loading: boolean;
  error: string | null;
  refreshCustomer: () => Promise<void>;
}

export const useCustomerDetail = ({ customerId, customerData }: UseCustomerDetailProps): UseCustomerDetailReturn => {
  const [customer, setCustomer] = useState<Customer | null>(customerData || null);
  const [loading, setLoading] = useState(!customerData);
  const [error, setError] = useState<string | null>(null);

  const loadCustomer = async () => {
    if (!customerId) {
      if (!customerData) {
        setError('Müşteri bilgisi bulunamadı');
      }
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await customerService.getCustomerById(customerId);
      if (response) {
        setCustomer(response);
      } else {
        setError('Müşteri bulunamadı');
      }
    } catch (err: any) {
      setError(err?.message || 'Müşteri yüklenirken bir hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCustomer();
  }, [customerId, customerData]);

  const refreshCustomer = async () => {
    await loadCustomer();
  };

  return {
    customer,
    loading,
    error,
    refreshCustomer
  };
};
