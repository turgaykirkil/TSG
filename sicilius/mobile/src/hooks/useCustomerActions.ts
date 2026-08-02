import { useCallback } from 'react';
import { Linking, Platform } from 'react-native';
import { Customer } from '../types/customer';

interface UseCustomerActionsReturn {
  handleCall: () => void;
  handleEmail: () => void;
  handleOpenMaps: () => void;
}

export const useCustomerActions = (customer: Customer | null): UseCustomerActionsReturn => {
  const handleCall = useCallback(() => {
    if (customer?.phone) {
      Linking.openURL(`tel:${customer.phone}`);
    }
  }, [customer?.phone]);

  const handleEmail = useCallback(() => {
    if (customer?.email) {
      Linking.openURL(`mailto:${customer.email}`);
    }
  }, [customer?.email]);

  const handleOpenMaps = useCallback(() => {
    if (customer?.address) {
      const coordinates = customer.address.coordinates;
      const lat = coordinates?.lat || coordinates?.[0];
      const lng = coordinates?.lng || coordinates?.[1];

      if (lat && lng) {
        const url = Platform.select({
          ios: `maps://maps.apple.com/?q=${customer.name}&ll=${lat},${lng}&z=16`,
          android: `geo:${lat},${lng}?q=${lat},${lng}(${encodeURIComponent(customer.name)})`,
          default: `https://www.google.com/maps/search/?api=1&query=${lat},${lng}&query_place_id=${encodeURIComponent(customer.name)}`
        });
        
        Linking.openURL(url).catch(() => {
          // Fallback olarak Google Maps web linki
          Linking.openURL(`https://www.google.com/maps/search/?api=1&query=${lat},${lng}&query_place_id=${encodeURIComponent(customer.name)}`);
        });
      } else {
        // Adres bilgisi ile arama
        const addressString = `${customer.address.street}, ${customer.address.city}, ${customer.address.country}`;
        Linking.openURL(`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(addressString)}`);
      }
    }
  }, [customer?.address, customer?.name]);

  return {
    handleCall,
    handleEmail,
    handleOpenMaps
  };
};
