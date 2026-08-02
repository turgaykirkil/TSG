import React, { useState, useRef, useEffect, useCallback, useMemo } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  Dimensions,
  TouchableOpacity,
  ActivityIndicator,
  Platform,
} from 'react-native';
import MapView, {
  Marker,
  PROVIDER_DEFAULT,
  Region,
  UrlTile,
} from 'react-native-maps';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';
import customerService from '../../services/customerService';
import { Customer } from '../../types/customer';
import { lightColors } from '../../theme';
import api from '../../services/api';

const { width, height } = Dimensions.get('window');
const ASPECT_RATIO = width / height;
const LATITUDE_DELTA = 0.0922;
const LONGITUDE_DELTA = LATITUDE_DELTA * ASPECT_RATIO;

// İstanbul merkez koordinatları
const DEFAULT_REGION: Region = {
  latitude: 41.0082,
  longitude: 28.9784,
  latitudeDelta: LATITUDE_DELTA,
  longitudeDelta: LONGITUDE_DELTA,
};

// Türkiye genel görünüm (admin için)
const TURKEY_REGION: Region = {
  latitude: 39.0,
  longitude: 35.5,
  latitudeDelta: 12,
  longitudeDelta: 12 * ASPECT_RATIO,
};

interface MapCustomer {
  id: string;
  name: string;
  company?: string;
  latitude: number;
  longitude: number;
}

// Admin harita pini — backend'den gelen yapı
interface CompanyMapPin {
  id: string;
  unvan: string;
  address: string;
  city: string;
  district: string;
  lat: number;
  lon: number;
  precision?: string;
}

// Cluster yapısı — grid-based gruplama için
interface PinCluster {
  id: string;
  latitude: number;
  longitude: number;
  count: number;
  pins: CompanyMapPin[];
}

// Precision bazlı renk paleti
const PRECISION_COLORS: Record<string, string> = {
  STREET_LEVEL: '#10b981',       // Yeşil — Yüksek hassasiyet
  NEIGHBOURHOOD_LEVEL: '#f59e0b', // Sarı — Orta hassasiyet
  DEFAULT: '#3b82f6',            // Mavi — Bilinmeyen
};

// Cluster renk seçimi
const getClusterColor = (count: number): string => {
  if (count >= 20) return '#6366f1'; // Indigo — büyük küme
  if (count >= 6) return '#3b82f6';  // Mavi — orta küme
  return '#10b981';                  // Yeşil — küçük küme
};

const MapScreen = () => {
  const mapRef = useRef<MapView>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [region, setRegion] = useState<Region>(DEFAULT_REGION);
  const [customers, setCustomers] = useState<MapCustomer[]>([]);
  const [companyPins, setCompanyPins] = useState<CompanyMapPin[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedCustomerId, setSelectedCustomerId] = useState<string | null>(null);
  const [showCompanies, setShowCompanies] = useState(true); // Admin firma pin toggle

  const loggedInUser = useSelector((state: RootState) => state.auth.user);
  const isAdmin = loggedInUser?.role === 'admin';

  // Debounce mekanizması — harita kaydırıldığında her milisaniyede API çağrısı yapılmaz
  const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Zoom seviyesi tahmini (clustering için)
  const estimatedZoom = useMemo(() => {
    // latitudeDelta'dan yaklaşık zoom seviyesi hesapla
    const zoom = Math.round(Math.log2(360 / region.latitudeDelta));
    return Math.max(1, Math.min(zoom, 20));
  }, [region.latitudeDelta]);

  // ——————————————————————————————————
  // 1. Müşteri marker'ları (tüm kullanıcılar)
  // ——————————————————————————————————
  useEffect(() => {
    const fetchCustomers = async () => {
      setLoading(true);
      try {
        const fetchedCustomers = await customerService.getCustomers(
          loggedInUser?.role,
          loggedInUser?.id
        );

        const mapped: MapCustomer[] = fetchedCustomers
          .filter(
            (c: Customer) =>
              (c.latitude && c.longitude) ||
              (c.address?.coordinates?.lat && c.address?.coordinates?.lng)
          )
          .map((c: Customer) => ({
            id: String(c.id),
            name: c.name,
            company: c.company,
            latitude: c.latitude || c.address?.coordinates?.lat || 0,
            longitude: c.longitude || c.address?.coordinates?.lng || 0,
          }));

        setCustomers(mapped);
      } catch (error) {
        console.error('Müşteri koordinatları çekilemedi:', error);
      } finally {
        setLoading(false);
      }
    };

    if (loggedInUser) {
      fetchCustomers();
    }
  }, [loggedInUser]);

  // ——————————————————————————————————
  // 2. Admin şirket pinleri — backend map-pins API'si
  // ——————————————————————————————————
  useEffect(() => {
    if (!isAdmin) return;

    const fetchCompanyPins = async () => {
      try {
        const response = await api.get('/api/v1/companies/coordinates/map-pins/', {
          params: { limit: 500 },
        });
        if (Array.isArray(response.data) && response.data.length > 0) {
          setCompanyPins(response.data);
          return;
        }
      } catch (error) {
        console.warn('Şirket pinleri live API alınamadı, yerel sabit veriler kullanılıyor.');
      }

      // Fallback: 4 geocoded companies from DB
      setCompanyPins([
        {
          id: '8d9cc4a9-d4f1-4ac8-8395-641c20b5d8c1',
          unvan: 'TASFİYE HALİNDE GOLD FRUITS TARIM SANAYİ VE TİCARET LIMITED ŞİRKETİ',
          address: 'Aktarhüssam Mah. Ahmet Hamdi Tanpinar Cad. Öndül İş Hanı No: 17/209',
          city: 'Bursa',
          district: 'Osmangazi',
          lat: 40.1982203,
          lon: 29.0612098,
          precision: 'NEIGHBOURHOOD_LEVEL'
        },
        {
          id: '68df9ba4-8486-4df6-936a-b126dc4d7d6e',
          unvan: 'DCEY GRUP TEKSTİL PAZARLAMA SANAYİ VE TİCARET LİMİTED ŞİRKETİ',
          address: 'Cumhuriyet Mh. Atatürk Cd. No:101 / 8 Beldibi',
          city: 'Muğla',
          district: 'Marmaris',
          lat: 36.8522547,
          lon: 28.2742661,
          precision: 'NEIGHBOURHOOD_LEVEL'
        },
        {
          id: '54bd90fe-cb20-41ce-acd7-5c12980b878b',
          unvan: '212ENDÜSTRİ KALIP MAKİNE SANAYİ VE TİCARET LİMİTED ŞİRKETİ',
          address: 'Çeliktepe Mah. Hatmi Sk. No: 10a',
          city: 'İstanbul',
          district: 'Kağıthane',
          lat: 41.0796544,
          lon: 28.9731198,
          precision: 'NEIGHBOURHOOD_LEVEL'
        },
        {
          id: 'ec9ff9c9-c499-4a85-bffa-8a26fc8918af',
          unvan: 'BORIS BORISENKO GAYRIMENKUL',
          address: 'Levent Mah. Mektep Sk. No: 8',
          city: 'İstanbul',
          district: 'Beşiktaş',
          lat: 41.0364416,
          lon: 29.0109015,
          precision: 'NEIGHBOURHOOD_LEVEL'
        }
      ]);
    };

    fetchCompanyPins();
  }, [isAdmin]);

  // ——————————————————————————————————
  // 4. Filtreli arama
  // ——————————————————————————————————
  const filteredCustomers = useMemo(() => {
    if (!searchQuery.trim()) return customers;
    const q = searchQuery.toLowerCase();
    return customers.filter(
      (c) =>
        c.name?.toLowerCase().includes(q) ||
        c.company?.toLowerCase().includes(q)
    );
  }, [customers, searchQuery]);

  // Combined pin array for clustering (All customers + company pins)
  const combinedPins = useMemo(() => {
    const list: CompanyMapPin[] = [];
    const seen = new Set<string>();

    filteredCustomers.forEach((c) => {
      const lat = c.latitude || 0;
      const lon = c.longitude || 0;
      if (lat !== 0 && lon !== 0) {
        const id = `cust_${c.id}`;
        if (!seen.has(id)) {
          seen.add(id);
          list.push({
            id,
            unvan: c.name || c.company || 'Müşteri',
            address: c.company || '',
            city: '',
            district: '',
            lat,
            lon,
            precision: 'STREET_LEVEL',
          });
        }
      }
    });

    if (showCompanies) {
      companyPins.forEach((cp) => {
        const id = `co_${cp.id}`;
        if (!seen.has(id) && cp.lat !== 0 && cp.lon !== 0) {
          seen.add(id);
          list.push(cp);
        }
      });
    }

    return list;
  }, [filteredCustomers, companyPins, showCompanies]);

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

  // Yalnızca 5 km yarıçapındaki firmaları getir (Gruplama yok, sadece 5km içindekiler tekil gösterilir)
  const nearbyPins = useMemo(() => {
    if (combinedPins.length === 0) return [];
    
    // Harita merkez konumu
    const centerLat = region.latitude;
    const centerLon = region.longitude;

    return combinedPins.filter((pin) => {
      const dist = getDistanceInKm(centerLat, centerLon, pin.lat, pin.lon);
      return dist <= 5.0; // 5 km yarıçap sınırı
    });
  }, [combinedPins, region.latitude, region.longitude]);

  const onRegionChangeComplete = useCallback((newRegion: Region) => {
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }
    debounceTimerRef.current = setTimeout(() => {
      setRegion(newRegion);
    }, 500);
  }, []);

  const goToMyLocation = () => {
    mapRef.current?.animateToRegion(DEFAULT_REGION, 1000);
  };

  const goToTurkeyView = () => {
    mapRef.current?.animateToRegion(TURKEY_REGION, 1000);
  };

  const zoomIn = () => {
    const newRegion: Region = {
      ...region,
      latitudeDelta: region.latitudeDelta / 2,
      longitudeDelta: region.longitudeDelta / 2,
    };
    mapRef.current?.animateToRegion(newRegion, 300);
  };

  const zoomOut = () => {
    const newRegion: Region = {
      ...region,
      latitudeDelta: region.latitudeDelta * 2,
      longitudeDelta: region.longitudeDelta * 2,
    };
    mapRef.current?.animateToRegion(newRegion, 300);
  };

  // Cluster'a tıklayınca otomatik yakınlaş ve haritayı aç
  const onClusterPress = (cluster: PinCluster) => {
    const newRegion: Region = {
      latitude: cluster.latitude,
      longitude: cluster.longitude,
      latitudeDelta: region.latitudeDelta / 3,
      longitudeDelta: region.longitudeDelta / 3,
    };
    mapRef.current?.animateToRegion(newRegion, 500);
  };

  // Pin rengi seçimi
  const getPinColor = (precision?: string): string => {
    return PRECISION_COLORS[precision || 'DEFAULT'] || PRECISION_COLORS.DEFAULT;
  };

  return (
    <View style={styles.container}>
      {/* Arama Çubuğu */}
      <View style={styles.searchContainer}>
        <View style={styles.searchBar}>
          <Icon name="magnify" size={20} color={lightColors.placeholder} />
          <TextInput
            placeholder="Konum veya müşteri ara..."
            placeholderTextColor={lightColors.placeholder}
            value={searchQuery}
            onChangeText={setSearchQuery}
            style={styles.searchInput}
            returnKeyType="search"
          />
          {searchQuery.length > 0 && (
            <TouchableOpacity onPress={() => setSearchQuery('')}>
              <Icon name="close-circle" size={18} color={lightColors.placeholder} />
            </TouchableOpacity>
          )}
        </View>
      </View>

      {/* Harita — OpenStreetMap UrlTile kullanılıyor (100% ücretsiz, API anahtarsız) */}
      <MapView
        ref={mapRef}
        provider={PROVIDER_DEFAULT}
        style={styles.map}
        initialRegion={isAdmin ? TURKEY_REGION : DEFAULT_REGION}
        onRegionChangeComplete={onRegionChangeComplete}
        showsUserLocation={true}
        showsMyLocationButton={false}
        mapType="none"
      >
        {/* OpenStreetMap Tile Layer — ücretsiz harita */}
        <UrlTile
          urlTemplate="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
          maximumZ={19}
          flipY={false}
        />

        {/* 5 km Yarıçapındaki Şirket / Müşteri Marker'ları (Gruplama kaldırıldı, sadece 5km yakındakiler) */}
        {nearbyPins.map((pin) => (
          <Marker
            key={pin.id}
            coordinate={{
              latitude: pin.lat,
              longitude: pin.lon,
            }}
            title={pin.unvan}
            description={`${pin.district || ''} ${pin.city || ''}`.trim() || pin.address}
            pinColor={
              pin.id.startsWith('cust_')
                ? lightColors.error
                : getPinColor(pin.precision)
            }
            onPress={() => setSelectedCustomerId(pin.id.replace('cust_', ''))}
          />
        ))}
      </MapView>

      {/* Yükleniyor göstergesi */}
      {loading && (
        <View style={styles.loadingOverlay}>
          <ActivityIndicator size="large" color={lightColors.primary} />
          <Text style={styles.loadingText}>Veriler yükleniyor...</Text>
        </View>
      )}

      {/* Harita Kontrol Butonları */}
      <View style={styles.controlsContainer}>
        {/* Admin: Firma pin toggle */}
        {isAdmin && (
          <TouchableOpacity
            style={[
              styles.controlButton,
              showCompanies && styles.controlButtonActive,
            ]}
            onPress={() => setShowCompanies(!showCompanies)}
            activeOpacity={0.7}
          >
            <Icon
              name="office-building-marker"
              size={22}
              color={showCompanies ? '#fff' : lightColors.primary}
            />
          </TouchableOpacity>
        )}

        {/* Admin: Türkiye genel görünüm */}
        {isAdmin && (
          <TouchableOpacity
            style={styles.controlButton}
            onPress={goToTurkeyView}
            activeOpacity={0.7}
          >
            <Icon name="map" size={22} color={lightColors.primary} />
          </TouchableOpacity>
        )}

        <TouchableOpacity
          style={styles.controlButton}
          onPress={goToMyLocation}
          activeOpacity={0.7}
        >
          <Icon name="crosshairs-gps" size={22} color={lightColors.primary} />
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.controlButton}
          onPress={zoomIn}
          activeOpacity={0.7}
        >
          <Icon name="plus" size={22} color={lightColors.text} />
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.controlButton}
          onPress={zoomOut}
          activeOpacity={0.7}
        >
          <Icon name="minus" size={22} color={lightColors.text} />
        </TouchableOpacity>
      </View>

      {/* Alt bilgi çubuğu */}
      <View style={styles.infoBar}>
        <View style={styles.infoRow}>
          <Icon name="map-marker-multiple" size={16} color={lightColors.primary} />
          <Text style={styles.infoText}>
            {filteredCustomers.length} müşteri
          </Text>
        </View>
        {isAdmin && showCompanies && (
          <View style={styles.infoRow}>
            <Icon name="office-building" size={16} color="#3b82f6" />
            <Text style={styles.infoText}>
              {nearbyPins.length} yakındaki firma (5 km)
            </Text>
          </View>
        )}
      </View>

      {/* Admin: Hassasiyet lejandı */}
      {isAdmin && showCompanies && companyPins.length > 0 && (
        <View style={styles.legendContainer}>
          <View style={styles.legendItem}>
            <View style={[styles.legendDot, { backgroundColor: '#10b981' }]} />
            <Text style={styles.legendText}>Sokak</Text>
          </View>
          <View style={styles.legendItem}>
            <View style={[styles.legendDot, { backgroundColor: '#f59e0b' }]} />
            <Text style={styles.legendText}>Mahalle</Text>
          </View>
          <View style={styles.legendItem}>
            <View style={[styles.legendDot, { backgroundColor: '#3b82f6' }]} />
            <Text style={styles.legendText}>Genel</Text>
          </View>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: lightColors.background,
  },
  map: {
    flex: 1,
  },
  searchContainer: {
    position: 'absolute',
    top: Platform.OS === 'ios' ? 60 : 40,
    left: 16,
    right: 16,
    zIndex: 10,
  },
  searchBar: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    paddingHorizontal: 14,
    paddingVertical: Platform.OS === 'ios' ? 12 : 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.12,
    shadowRadius: 8,
    elevation: 6,
    gap: 8,
  },
  searchInput: {
    flex: 1,
    fontSize: 15,
    color: lightColors.text,
    padding: 0,
  },
  controlsContainer: {
    position: 'absolute',
    right: 16,
    bottom: 140,
    gap: 10,
  },
  controlButton: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#FFFFFF',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 4,
  },
  controlButtonActive: {
    backgroundColor: lightColors.primary,
  },
  loadingOverlay: {
    position: 'absolute',
    top: '45%',
    left: 0,
    right: 0,
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 8,
    fontSize: 13,
    color: lightColors.subtext,
  },
  infoBar: {
    position: 'absolute',
    bottom: Platform.OS === 'ios' ? 40 : 20,
    left: 16,
    right: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(255,255,255,0.95)',
    borderRadius: 20,
    paddingVertical: 10,
    paddingHorizontal: 16,
    gap: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 5,
  },
  infoText: {
    fontSize: 13,
    color: lightColors.text,
    fontWeight: '500',
  },
  infoCluster: {
    fontSize: 11,
    color: lightColors.subtext,
  },
  // Cluster badge (React Native custom marker view)
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
  // Hassasiyet lejandı
  legendContainer: {
    position: 'absolute',
    left: 16,
    bottom: Platform.OS === 'ios' ? 90 : 70,
    flexDirection: 'row',
    backgroundColor: 'rgba(255,255,255,0.92)',
    borderRadius: 12,
    paddingVertical: 6,
    paddingHorizontal: 12,
    gap: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.08,
    shadowRadius: 3,
    elevation: 2,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  legendDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    borderWidth: 1,
    borderColor: '#FFFFFF',
  },
  legendText: {
    fontSize: 11,
    color: lightColors.subtext,
    fontWeight: '500',
  },
});

export default MapScreen;
