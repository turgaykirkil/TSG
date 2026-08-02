import { useState, useEffect } from 'react';
import * as LocationModule from 'expo-location';

export type Location = {
  lat: number;
  lon: number;
};

export const useLocation = () => {
  const [location, setLocation] = useState<Location | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const getCurrentLocation = async () => {
    try {
      setLoading(true);
      const { status } = await LocationModule.requestForegroundPermissionsAsync();
      if (status !== 'granted') {
        setError('Konum izni reddedildi');
        setLoading(false);
        return;
      }
      const pos = await LocationModule.getCurrentPositionAsync({
        accuracy: LocationModule.Accuracy.Balanced,
      });
      setLocation({
        lat: pos.coords.latitude,
        lon: pos.coords.longitude,
      });
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Konum alınamadı');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getCurrentLocation();
  }, []);

  return {
    location,
    error,
    loading,
    refreshLocation: getCurrentLocation,
  };
};
