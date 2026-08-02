import React, { useRef, useState, useEffect, useCallback, useMemo } from 'react';
import { 
  View, 
  StyleSheet, 
  Dimensions,
  Text,
  TouchableOpacity
} from 'react-native';
import MapView, { Marker, Polyline, Callout, UrlTile, PROVIDER_DEFAULT } from 'react-native-maps';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useLocation } from '../../hooks/useLocation';
import { useCustomers } from '../../hooks/useCustomers';
import { Customer } from '../../types/customer';
import { lightColors } from '../../theme';
import RouteActionButtons from './RouteActionButtons';

interface RouteMapViewProps {
  selectedPoints: Array<{customer: Customer, order: number}>;
  optimizedRoute?: any;
  onCustomerPress: (customer: Customer | null) => void;
  onCalculateRoute: () => Promise<any>;
  isLoading: boolean;
}

// Güvenli metin dönüşümü (React Native object as child çökmesini önler)
const safeString = (val: any, fallback: string = ''): string => {
  if (val === null || val === undefined) return fallback;
  if (typeof val === 'string') return val;
  if (typeof val === 'number') return String(val);
  if (typeof val === 'object') {
    if (typeof val.street === 'string') return val.street;
    if (typeof val.name === 'string') return val.name;
    if (typeof val.title === 'string') return val.title;
  }
  return fallback;
};

const RouteMapView: React.FC<RouteMapViewProps> = ({ 
  selectedPoints, 
  optimizedRoute, 
  onCustomerPress,
  onCalculateRoute,
  isLoading
}) => {
  const { location } = useLocation();
  const { customers } = useCustomers();
  const mapRef = useRef<MapView>(null);

  const [mapRegion, setMapRegion] = useState({
    latitude: 41.0082,
    longitude: 28.9784,
    latitudeDelta: 0.0922,
    longitudeDelta: 0.0421,
  });

  useEffect(() => {
    if (location && typeof location.lat === 'number' && typeof location.lon === 'number') {
      setMapRegion({
        latitude: location.lat,
        longitude: location.lon,
        latitudeDelta: 0.0922,
        longitudeDelta: 0.0421,
      });
    }
  }, [location]);

  const clearSelection = useCallback(() => {
    onCustomerPress(null);
  }, [onCustomerPress]);

  const handleMarkerPress = useCallback((customer: Customer) => {
    if (customer && customer.id) {
      onCustomerPress(customer);
    }
  }, [onCustomerPress]);

  // Haversine mesafe hesabı (km)
  const getDistanceInKm = (lat1: number, lon1: number, lat2: number, lon2: number): number => {
    const R = 6371;
    const dLat = (lat2 - lat1) * (Math.PI / 180);
    const dLon = (lon2 - lon1) * (Math.PI / 180);
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos(lat1 * (Math.PI / 180)) *
        Math.cos(lat2 * (Math.PI / 180)) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  };

  // 5 km yarıçapındaki müşterileri getir (Gruplama yok)
  const nearbyCustomers = useMemo(() => {
    if (!customers || customers.length === 0) return [];

    const selectedIds = new Set(selectedPoints.map(p => String(p.customer.id)));
    const centerLat = mapRegion.latitude;
    const centerLon = mapRegion.longitude;

    return customers.filter((c: any) => {
      if (!c) return false;
      const cId = String(c.id);
      // Seçilen rota noktaları her zaman haritada görünür
      if (selectedIds.has(cId)) return true;

      const lat = typeof c.latitude === 'number' ? c.latitude : c.address?.coordinates?.lat;
      const lng = typeof c.longitude === 'number' ? c.longitude : c.address?.coordinates?.lng;

      if (!lat || !lng || lat === 0 || lng === 0 || isNaN(lat) || isNaN(lng)) return false;

      const dist = getDistanceInKm(centerLat, centerLon, Number(lat), Number(lng));
      return dist <= 5.0; // 5 km yarıçap sınırı
    });
  }, [customers, selectedPoints, mapRegion.latitude, mapRegion.longitude]);

  return (
    <View style={{ flex: 1 }}>
      <MapView
        ref={mapRef}
        provider={PROVIDER_DEFAULT}
        style={styles.map}
        initialRegion={mapRegion}
        onRegionChangeComplete={(r) => setMapRegion(r)}
        mapType="none"
        showsUserLocation
        showsMyLocationButton={false}
      >
        {/* OpenStreetMap Tile Layer — 100% Ücretsiz, API Anahtarsız */}
        <UrlTile
          urlTemplate="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
          maximumZ={19}
          flipY={false}
        />

        {/* 5 km Yarıçapındaki müşteri marker'ları (Gruplama yok) */}
        {nearbyCustomers.map(customer => {
          if (!customer) return null;
          const lat = typeof customer.latitude === 'number' ? customer.latitude : customer.address?.coordinates?.lat;
          const lng = typeof customer.longitude === 'number' ? customer.longitude : customer.address?.coordinates?.lng;

          if (!lat || !lng || lat === 0 || lng === 0 || isNaN(lat) || isNaN(lng)) return null;

          const customerIdStr = String(customer.id);
          const isSelected = selectedPoints.some(p => String(p.customer.id) === customerIdStr);
          const selectedOrder = selectedPoints.find(p => String(p.customer.id) === customerIdStr)?.order;

          const displayName = safeString(customer.name, safeString(customer.company, 'Müşteri'));
          const displayAddress = safeString(customer.address?.street, safeString(customer.address, 'Adres belirtilmedi'));

          return (
            <Marker
              key={customerIdStr}
              coordinate={{
                latitude: Number(lat),
                longitude: Number(lng),
              }}
              title={displayName}
              description={displayAddress}
              onPress={() => handleMarkerPress(customer)}
              tracksViewChanges={false}
            >
              <View style={styles.markerContainer}>
                <View style={[styles.orderBadge, !isSelected && styles.hiddenBadge]}>
                  <Text style={styles.orderBadgeText}>{String(selectedOrder || '')}</Text>
                </View>
                <MaterialCommunityIcons
                  name="map-marker"
                  size={42}
                  color={isSelected ? lightColors.primary : '#E11D48'}
                />
              </View>
            </Marker>
          );
        })}

        {optimizedRoute && optimizedRoute.coordinates && optimizedRoute.coordinates.length > 0 && (
          <Polyline
            coordinates={optimizedRoute.coordinates.map((coord: any) => ({
              latitude: Number(coord.latitude || coord.lat || 0),
              longitude: Number(coord.longitude || coord.lng || 0),
            })).filter((c: any) => c.latitude !== 0 && c.longitude !== 0)}
            strokeColor={lightColors.primary}
            strokeWidth={4}
          />
        )}
      </MapView>

      <View style={styles.actionButtonsContainer}>
        <RouteActionButtons 
          selectedPointsCount={selectedPoints.length}
          isLoading={isLoading}
          onCalculateRoute={onCalculateRoute}
          onClearSelection={clearSelection}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  map: {
    width: Dimensions.get('window').width,
    height: Dimensions.get('window').height,
  },
  markerContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  orderBadge: {
    position: 'absolute',
    top: -6,
    zIndex: 10,
    backgroundColor: lightColors.primary,
    width: 22,
    height: 22,
    borderRadius: 11,
    borderWidth: 2,
    borderColor: '#FFFFFF',
    justifyContent: 'center',
    alignItems: 'center',
  },
  hiddenBadge: {
    opacity: 0,
  },
  orderBadgeText: {
    color: '#FFFFFF',
    fontSize: 11,
    fontWeight: 'bold',
  },
  calloutContainer: {
    width: Dimensions.get('window').width * 0.7,
    padding: 10,
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  calloutTitle: {
    fontSize: 15,
    fontWeight: 'bold',
    color: lightColors.text,
    marginBottom: 4,
  },
  calloutDetails: {
    fontSize: 13,
    color: lightColors.subtext,
  },
  actionButtonsContainer: {
    position: 'absolute',
    bottom: 20,
    left: 0,
    right: 0,
    alignItems: 'center',
    zIndex: 10,
    backgroundColor: 'transparent',
  },
  clusterBadge: {
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 3,
    borderColor: '#FFFFFF',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.35,
    shadowRadius: 6,
    elevation: 6,
  },
  clusterText: {
    color: '#FFFFFF',
    fontSize: 13,
    fontWeight: '800',
    letterSpacing: -0.5,
  },
});

export default React.memo(RouteMapView);
