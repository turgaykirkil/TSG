import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Dimensions, TouchableOpacity } from 'react-native';
import MapView, { Marker, Callout } from 'react-native-maps';
import * as LocationModule from 'expo-location';
import { useCustomers } from '../../hooks/useCustomers';
import { Customer } from '../../types/customer';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';

const { width, height } = Dimensions.get('window');
const ASPECT_RATIO = width / height;
const LATITUDE_DELTA = 0.0922;
const LONGITUDE_DELTA = LATITUDE_DELTA * ASPECT_RATIO;

const CustomerMapScreen = ({ navigation }: any) => {
  const { customers } = useCustomers();

  const [region, setRegion] = useState({
    latitude: 41.0082,
    longitude: 28.9784,
    latitudeDelta: LATITUDE_DELTA,
    longitudeDelta: LONGITUDE_DELTA,
  });

  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);

  useEffect(() => {
    getCurrentLocation();
  }, []);

  const getCurrentLocation = async () => {
    try {
      const { status } = await LocationModule.requestForegroundPermissionsAsync();
      if (status === 'granted') {
        const pos = await LocationModule.getCurrentPositionAsync({});
        const { latitude, longitude } = pos.coords;
        setRegion(prev => ({ ...prev, latitude, longitude }));
      }
    } catch (e) {
      console.log('Location error:', e);
    }
  };

  const getCoordinates = (customer: any) => {
    const lat = customer.latitude || customer.address?.coordinates?.lat || customer.lat || 41.0082;
    const lng = customer.longitude || customer.address?.coordinates?.lng || customer.lng || 28.9784;
    return { latitude: Number(lat), longitude: Number(lng) };
  };

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

  const nearbyCustomers = React.useMemo(() => {
    if (!customers) return [];
    return customers.filter((c: any) => {
      const lat = Number(c.latitude || c.address?.coordinates?.lat || c.lat || 0);
      const lng = Number(c.longitude || c.address?.coordinates?.lng || c.lng || 0);
      if (lat === 0 || lng === 0) return false;
      const dist = getDistanceInKm(region.latitude, region.longitude, lat, lng);
      return dist <= 5.0;
    });
  }, [customers, region.latitude, region.longitude]);

  return (
    <View style={styles.container}>
      <MapView
        style={styles.map}
        region={region}
        onRegionChangeComplete={setRegion}
        showsUserLocation
        showsMyLocationButton
      >
        {nearbyCustomers.map((customer: any) => {
          const coords = getCoordinates(customer);
          return (
            <Marker
              key={customer.id}
              coordinate={coords}
              onPress={() => setSelectedCustomer(customer)}
            >
              <Callout style={styles.calloutContainer}>
                <View style={styles.calloutBox}>
                  <Text style={styles.calloutTitle}>{customer.name || customer.title}</Text>
                  <Text style={styles.calloutSub}>
                    {customer.company_name || customer.company || 'B2B Müşteri'}
                  </Text>
                  <Text style={styles.calloutPhone}>{customer.phone || customer.email || ''}</Text>
                </View>
              </Callout>
            </Marker>
          );
        })}
      </MapView>

      {selectedCustomer && (
        <View style={styles.customerCard}>
          <View style={styles.cardHeader}>
            <View style={{ flex: 1 }}>
              <Text style={styles.cardTitle}>{selectedCustomer.name || (selectedCustomer as any).title}</Text>
              <Text style={styles.cardSub}>
                {(selectedCustomer as any).company_name || selectedCustomer.company || 'B2B Müşteri'}
              </Text>
            </View>
            <TouchableOpacity onPress={() => setSelectedCustomer(null)}>
              <Icon name="close" size={20} color="#9CA3AF" />
            </TouchableOpacity>
          </View>

          {(selectedCustomer as any).address ? (
            <Text style={styles.cardAddress} numberOfLines={2}>
              {typeof (selectedCustomer as any).address === 'string'
                ? (selectedCustomer as any).address
                : (selectedCustomer as any).address?.street || ''}
            </Text>
          ) : null}

          <View style={styles.cardFooter}>
            <Text style={styles.cardPhone}>{selectedCustomer.phone || selectedCustomer.email || ''}</Text>
            <TouchableOpacity
              style={styles.detailBtn}
              onPress={() => navigation.navigate('CustomerDetail', { customerId: selectedCustomer.id })}
            >
              <Text style={styles.detailBtnText}>Detaylar</Text>
              <Icon name="chevron-right" size={18} color="#FFFFFF" />
            </TouchableOpacity>
          </View>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F3F4F6',
  },
  map: {
    flex: 1,
  },
  calloutContainer: {
    width: 180,
  },
  calloutBox: {
    padding: 8,
  },
  calloutTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 2,
  },
  calloutSub: {
    fontSize: 12,
    color: '#4B5563',
    marginBottom: 2,
  },
  calloutPhone: {
    fontSize: 11,
    color: '#00A0E9',
  },
  customerCard: {
    position: 'absolute',
    bottom: 24,
    left: 16,
    right: 16,
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    elevation: 6,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 3 },
    shadowOpacity: 0.15,
    shadowRadius: 5,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 6,
  },
  cardTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1F2937',
  },
  cardSub: {
    fontSize: 13,
    color: '#6B7280',
    marginTop: 1,
  },
  cardAddress: {
    fontSize: 12,
    color: '#4B5563',
    marginBottom: 12,
  },
  cardFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 4,
  },
  cardPhone: {
    fontSize: 13,
    fontWeight: '600',
    color: '#00A0E9',
  },
  detailBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#00A0E9',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 8,
  },
  detailBtnText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 13,
    marginRight: 2,
  },
});

export default CustomerMapScreen;
