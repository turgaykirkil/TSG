import React, { 
  useState, 
  useCallback 
} from 'react';
import { 
  View, 
  StyleSheet, 
  Alert
} from 'react-native';
import * as Location from 'expo-location';
import { Customer } from '../../types/customer';
import { routeService } from '../../services/routeService';
import { lightColors } from '../../theme';

import RouteMapView from '../../components/route/RouteMapView';
import RouteDetailsModal from '../../components/route/RouteDetailsModal';

const RouteOptimizationScreen = () => {
  const [selectedPoints, setSelectedPoints] = useState<Array<{customer: Customer, order: number}>>([]);
  const [optimizedRoute, setOptimizedRoute] = useState<any | null>(null);
  const [userLocation, setUserLocation] = useState<{ latitude: number; longitude: number } | undefined>(undefined);
  const [routeDetailsModalVisible, setRouteDetailsModalVisible] = useState(false);
  const [routeDetails, setRouteDetails] = useState<{
    customers: Customer[];
    distance: number;
    duration: number;
  } | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleCustomerPress = useCallback((customer: Customer | null) => {
    if (!customer) {
      setSelectedPoints([]);
      setOptimizedRoute(null);
      return;
    }

    const isAlreadySelected = selectedPoints.some(point => point.customer.id === customer.id);
    
    if (isAlreadySelected) {
      const updatedPoints = selectedPoints.filter(point => point.customer.id !== customer.id);
      setSelectedPoints(updatedPoints.map((point, index) => ({
        ...point,
        order: index + 1
      })));
    } else {
      const newSelectedPoint = {
        customer,
        order: selectedPoints.length + 1
      };
      
      setSelectedPoints([...selectedPoints, newSelectedPoint]);
    }
  }, [selectedPoints]);

  const calculateRoute = useCallback(async () => {
    try {
      setIsLoading(true);
      if (!selectedPoints || selectedPoints.length < 1) {
        Alert.alert('Uyarı', 'Rota hesaplaması için en az 1 müşteri veya firma seçmelisiniz.');
        return null;
      }

      const validCustomers = selectedPoints.map(point => point.customer)
        .filter(customer => {
          const lat = customer.latitude || customer.address?.coordinates?.lat;
          const lng = customer.longitude || customer.address?.coordinates?.lng;
          return typeof lat === 'number' && typeof lng === 'number' && lat !== 0 && lng !== 0;
        });
      
      if (validCustomers.length < 1) {
        Alert.alert('Uyarı', 'Seçilen noktaların koordinatları geçersiz. Lütfen başka noktalar seçin.');
        return null;
      }

      // Kullanıcının anlık konumunu al (İş Yeri / Mevcut Konum)
      let currentGpsLoc: { latitude: number; longitude: number } | undefined = undefined;
      try {
        const { status } = await Location.requestForegroundPermissionsAsync();
        if (status === 'granted') {
          let pos = await Location.getLastKnownPositionAsync({});
          if (!pos) {
            pos = await Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.Balanced });
          }
          if (pos && pos.coords) {
            currentGpsLoc = {
              latitude: pos.coords.latitude,
              longitude: pos.coords.longitude,
            };
            setUserLocation(currentGpsLoc);
          }
        }
      } catch (locErr) {
        console.log('GPS konumu alınamadı, Harita uygulaması varsayılan konum ile başlatılacak.');
      }

      const optRoute = await routeService.calculateOptimizedRoute(validCustomers, currentGpsLoc);
      
      if (!optRoute) {
        throw new Error('Rota hesaplanamadı');
      }

      const details = {
        customers: optRoute.customerDetails || validCustomers,
        distance: optRoute.totalDistance || 0,
        duration: optRoute.estimatedTime || 0
      };

      setRouteDetails(details);
      setOptimizedRoute(optRoute);
      setRouteDetailsModalVisible(true);

      return optRoute;
    } catch (error) {
      Alert.alert('Hata', 'Rota hesaplanırken bir hata oluştu. Lütfen tekrar deneyin.');
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [selectedPoints]);

  const closeRouteDetailsModal = useCallback(() => {
    setRouteDetailsModalVisible(false);
  }, []);

  const showRouteOnMap = useCallback(() => {
    setRouteDetailsModalVisible(false);
  }, []);

  const startNavigation = useCallback(() => {
    if (routeDetails && routeDetails.customers && routeDetails.customers.length > 0) {
      routeService.openExternalNavigation(routeDetails.customers, userLocation);
    } else {
      Alert.alert('Uyarı', 'Navigasyon için geçerli rota bulunamadı.');
    }
  }, [routeDetails, userLocation]);

  const cancelRoute = useCallback(() => {
    // Rotayı tamamen iptal et
    setSelectedPoints([]);
    setOptimizedRoute(null);
    setRouteDetails(null);
    setRouteDetailsModalVisible(false);
  }, []);

  return (
    <View style={styles.container}>
      <RouteMapView 
        selectedPoints={selectedPoints}
        optimizedRoute={optimizedRoute}
        onCustomerPress={handleCustomerPress}
        onCalculateRoute={calculateRoute}
        isLoading={isLoading}
      />
      
      <RouteDetailsModal 
        visible={routeDetailsModalVisible}
        routeDetails={routeDetails}
        onClose={closeRouteDetailsModal}
        onShowOnMap={showRouteOnMap}
        onStartNavigation={startNavigation}
        onCancelRoute={cancelRoute}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: lightColors.background,
  },
});

export default React.memo(RouteOptimizationScreen);
