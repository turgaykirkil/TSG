import React, { useState, useMemo } from 'react';
import { View, StyleSheet, FlatList, TouchableOpacity, Linking, Alert, Text, ActivityIndicator } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { CustomerStackNavigationProp } from '../../navigation/types';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { Swipeable } from 'react-native-gesture-handler';

interface CustomerListContentProps {
  customers: any[];
  loading: boolean;
  searchQuery: string;
  onCustomerSelect?: (customer: any) => void;
  onCallModalToggle?: (visible: boolean) => void;
}

function formatDistance(distKm?: number): string {
  if (distKm === undefined || isNaN(distKm)) return 'Mesafe Hesaplanıyor';
  if (distKm < 1) {
    return `${Math.round(distKm * 1000)} m`;
  }
  return `${distKm.toFixed(1)} km`;
}

const BATCH_SIZE = 20;

const CustomerListContent: React.FC<CustomerListContentProps> = ({
  customers,
  loading,
  searchQuery,
  onCustomerSelect,
  onCallModalToggle,
}) => {
  const navigation = useNavigation<CustomerStackNavigationProp>();
  const [page, setPage] = useState(1);

  const filteredCustomers = useMemo(() => {
    return customers.filter((customer) =>
      (customer.name || customer.tradeName || '').toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [customers, searchQuery]);

  const visibleCustomers = useMemo(() => {
    return filteredCustomers.slice(0, page * BATCH_SIZE);
  }, [filteredCustomers, page]);

  const handleEndReached = () => {
    if (visibleCustomers.length < filteredCustomers.length) {
      setPage((prev) => prev + 1);
    }
  };

  const handleCall = (customer: any) => {
    if (onCustomerSelect) {
      onCustomerSelect(customer);
    }
    if (onCallModalToggle) {
      onCallModalToggle(true);
    }
    if (customer.phone) {
      Linking.openURL(`tel:${customer.phone}`).catch(() => {
        Alert.alert('Hata', 'Arama yapılamadı.');
      });
    }
  };

  const renderRightActions = (customer: any) => (
    <View style={styles.rightActions}>
      <TouchableOpacity
        style={[styles.actionButton, styles.actionButtonCall]}
        onPress={() => handleCall(customer)}
      >
        <MaterialCommunityIcons name="phone" color="white" size={24} />
      </TouchableOpacity>
      <TouchableOpacity
        style={[styles.actionButton, styles.actionButtonMap]}
        onPress={() => (navigation.navigate as any)('CustomerMap', { customerId: customer.id })}
      >
        <MaterialCommunityIcons name="map-marker" color="white" size={24} />
      </TouchableOpacity>
    </View>
  );

  const renderCustomerItem = (customer: any) => {
    const initial = (customer.name || customer.tradeName || 'M').charAt(0).toUpperCase();
    return (
      <Swipeable renderRightActions={() => renderRightActions(customer)} key={customer.id}>
        <TouchableOpacity
          style={styles.customerItem}
          onPress={() => navigation.navigate('CustomerDetail', { customerId: customer.id })}
        >
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>{initial}</Text>
          </View>
          <View style={styles.customerInfo}>
            <View style={styles.customerHeader}>
              <Text style={styles.customerName} numberOfLines={1}>
                {customer.name || customer.tradeName}
              </Text>
              {customer.type ? <Text style={styles.customerType}>{customer.type}</Text> : null}
            </View>
            <View style={styles.customerDetails}>
              <View style={styles.detailContainer}>
                <MaterialCommunityIcons name="phone" size={14} color="#6B7280" />
                <Text style={styles.detailText}>{customer.phone || 'Telefon Yok'}</Text>
              </View>
              <View style={[styles.detailContainer, styles.distanceContainer]}>
                <MaterialCommunityIcons name="map-marker-distance" size={14} color="#00A0E9" />
                <Text style={styles.detailText}>{formatDistance(customer.distance)}</Text>
              </View>
            </View>
          </View>
        </TouchableOpacity>
      </Swipeable>
    );
  };

  if (loading) {
    return (
      <View style={styles.emptyContainer}>
        <ActivityIndicator size="large" color="#00A0E9" />
      </View>
    );
  }

  if (filteredCustomers.length === 0) {
    return (
      <View style={styles.emptyContainer}>
        <MaterialCommunityIcons
          name="account-search"
          size={64}
          color="#9CA3AF"
          style={styles.emptyIcon}
        />
        <Text style={styles.emptyText}>
          Hiçbir müşteri bulunamadı. {searchQuery && `"${searchQuery}" ile eşleşen sonuç yok.`}
        </Text>
      </View>
    );
  }

  return (
    <FlatList
      data={visibleCustomers}
      renderItem={({ item }) => renderCustomerItem(item)}
      keyExtractor={(item) => item.id}
      contentContainerStyle={styles.customerListContainer}
      showsVerticalScrollIndicator={false}
      onEndReached={handleEndReached}
      onEndReachedThreshold={0.5}
      ListFooterComponent={
        visibleCustomers.length < filteredCustomers.length ? (
          <View style={{ paddingVertical: 16, alignItems: 'center' }}>
            <ActivityIndicator size="small" color="#00A0E9" />
            <Text style={{ fontSize: 11, color: '#9CA3AF', marginTop: 4 }}>Daha fazla firma yükleniyor...</Text>
          </View>
        ) : null
      }
    />
  );
};

const styles = StyleSheet.create({
  customerListContainer: {
    paddingVertical: 8,
  },
  customerItem: {
    backgroundColor: '#FFFFFF',
    marginHorizontal: 16,
    marginVertical: 6,
    padding: 14,
    borderRadius: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.08,
    shadowRadius: 2,
    flexDirection: 'row',
    alignItems: 'center',
  },
  avatar: {
    width: 46,
    height: 46,
    borderRadius: 23,
    backgroundColor: '#E0F2FE',
    justifyContent: 'center',
    alignItems: 'center',
  },
  avatarText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#0284C7',
  },
  customerInfo: {
    flex: 1,
    marginLeft: 12,
  },
  customerHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  customerName: {
    fontSize: 15,
    fontWeight: 'bold',
    color: '#1F2937',
    flex: 1,
    marginRight: 8,
  },
  customerType: {
    fontSize: 12,
    color: '#00A0E9',
    fontWeight: '600',
  },
  customerDetails: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 4,
  },
  detailText: {
    fontSize: 12,
    color: '#6B7280',
    marginLeft: 4,
  },
  detailContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 16,
  },
  distanceContainer: {
    marginRight: 0,
    marginLeft: 'auto',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
    minHeight: 200,
  },
  emptyText: {
    fontSize: 15,
    color: '#6B7280',
    textAlign: 'center',
    marginTop: 8,
  },
  emptyIcon: {
    marginBottom: 12,
  },
  rightActions: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: 6,
    marginLeft: -8,
  },
  actionButton: {
    justifyContent: 'center',
    alignItems: 'center',
    width: 60,
    height: '100%',
    borderRadius: 8,
    marginHorizontal: 2,
  },
  actionButtonCall: {
    backgroundColor: '#00A0E9',
  },
  actionButtonMap: {
    backgroundColor: '#10B981',
  },
});

export default CustomerListContent;
