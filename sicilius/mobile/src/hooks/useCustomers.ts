import { useState, useEffect } from 'react';
import * as Location from 'expo-location';
import { Customer } from '../types/customer';
import { customerService } from '../services/customerService';

function calculateDistanceKm(lat1: number, lon1: number, lat2: number, lon2: number): number {
  if (!lat1 || !lon1 || !lat2 || !lon2) return 999999;
  const R = 6371;
  const dLat = (lat2 - lat1) * (Math.PI / 180);
  const dLon = (lon2 - lon1) * (Math.PI / 180);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * (Math.PI / 180)) * Math.cos(lat2 * (Math.PI / 180)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

export const useCustomers = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        let userLat = 41.0422; // Default Istanbul center fallback
        let userLng = 29.0083;

        try {
          const { status } = await Location.requestForegroundPermissionsAsync();
          if (status === 'granted') {
            const loc = await Location.getLastKnownPositionAsync() || await Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.Balanced });
            if (loc?.coords) {
              userLat = loc.coords.latitude;
              userLng = loc.coords.longitude;
            }
          }
        } catch {
          // Fallback to Istanbul center
        }

        const data = await customerService.getCustomers();
        
        // Compute distance for each customer and sort closest first (yakından uzağa)
        const updated = data.map((c: any) => {
          const lat = c.latitude || c.address?.coordinates?.lat || 0;
          const lng = c.longitude || c.address?.coordinates?.lng || 0;
          const dist = calculateDistanceKm(userLat, userLng, lat, lng);
          return {
            ...c,
            distance: dist < 999999 ? dist : undefined
          };
        });

        // Sort by distance ascending (Yakından Uzağa)
        updated.sort((a, b) => (a.distance ?? 999999) - (b.distance ?? 999999));

        setCustomers(updated);
      } catch (error) {
        setCustomers([]);
      } finally {
        setLoading(false);
      }
    };

    fetchCustomers();
  }, []);

  return { customers, loading };
};
