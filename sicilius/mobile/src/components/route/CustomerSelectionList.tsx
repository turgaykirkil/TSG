import React, { useMemo } from 'react';
import { 
  View, 
  FlatList, 
  StyleSheet, 
  TouchableOpacity,
  Text,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { Customer } from '../../types/customer';
import { useCustomers } from '../../hooks/useCustomers';
import { lightColors } from '../../theme';

interface CustomerSelectionListProps {
  selectedPoints: Array<{customer: Customer, order: number}>;
  onCustomerPress: (customer: Customer) => void;
}

const CustomerSelectionList: React.FC<CustomerSelectionListProps> = ({ 
  selectedPoints, 
  onCustomerPress 
}) => {
  const { customers } = useCustomers();

  const filteredCustomers = useMemo(() => {
    if (!customers) return [];
    return customers.filter(customer => {
      const lat = customer.latitude || customer.address?.coordinates?.lat;
      const lng = customer.longitude || customer.address?.coordinates?.lng;
      return typeof lat === 'number' && typeof lng === 'number' && lat !== 0 && lng !== 0;
    });
  }, [customers]);

  const renderCustomerItem = ({ item }: { item: Customer }) => {
    const isSelected = selectedPoints.some(point => point.customer.id === item.id);
    const selectedOrder = selectedPoints.find(point => point.customer.id === item.id)?.order;

    return (
      <TouchableOpacity 
        style={styles.customerItem} 
        onPress={() => onCustomerPress(item)}
      >
        <MaterialCommunityIcons 
          name={isSelected ? 'checkbox-marked' : 'checkbox-blank-outline'} 
          size={24} 
          color={isSelected ? lightColors.primary : lightColors.placeholder} 
        />
        <Text style={styles.customerName}>{item.name}</Text>
        {isSelected && (
          <View 
            style={[
              styles.selectedIndicator, 
              { backgroundColor: lightColors.primary }
            ]}
          >
            <Text style={styles.selectedText}>{selectedOrder}</Text>
          </View>
        )}
      </TouchableOpacity>
    );
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={filteredCustomers}
        renderItem={renderCustomerItem}
        keyExtractor={(item) => item.id.toString()}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>Müşteri veya firma bulunamadı (koordinatlar yüklenemedi)</Text>
          </View>
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    maxHeight: 250,
    backgroundColor: lightColors.background,
  },
  customerItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: lightColors.border,
  },
  customerName: {
    flex: 1,
    marginLeft: 12,
    fontSize: 15,
    color: lightColors.text,
    fontWeight: '500',
  },
  selectedIndicator: {
    width: 24,
    height: 24,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  selectedText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: 'bold',
  },
  emptyContainer: {
    padding: 16,
    alignItems: 'center',
  },
  emptyText: {
    color: lightColors.subtext,
    fontSize: 13,
  },
});

export default React.memo(CustomerSelectionList);
