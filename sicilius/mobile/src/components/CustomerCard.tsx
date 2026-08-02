import React, { memo } from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { MaterialCommunityIcons as IconMC } from '@expo/vector-icons';
import { Customer } from '../types/customer';

type CustomerCardProps = {
  customer: Customer;
  onPress: (customer: Customer) => void;
};

const CustomerCard = memo<CustomerCardProps>(({ customer, onPress }) => {
  return (
    <TouchableOpacity style={styles.card} activeOpacity={0.7} onPress={() => onPress(customer)}>
      <View style={styles.cardHeader}>
        <Text style={styles.nameText}>{customer.name}</Text>
        {customer.distance !== undefined && (
          <View style={styles.distanceContainer}>
            <IconMC name="map-marker-distance" size={14} color="#00A0E9" />
            <Text style={styles.distanceText}>
              {customer.distance.toFixed(1)} km
            </Text>
          </View>
        )}
      </View>
      <Text style={styles.companyText}>{customer.company}</Text>
      <Text style={styles.emailText}>{customer.email}</Text>
    </TouchableOpacity>
  );
});

const styles = StyleSheet.create({
  card: {
    marginHorizontal: 16,
    marginVertical: 6,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.08,
    shadowRadius: 3,
    elevation: 2,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  nameText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1F2937',
    flex: 1,
  },
  companyText: {
    fontSize: 14,
    color: '#4B5563',
    marginBottom: 2,
  },
  emailText: {
    fontSize: 12,
    color: '#9CA3AF',
  },
  distanceContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#E0F2FE',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 12,
    marginLeft: 8,
  },
  distanceText: {
    marginLeft: 4,
    fontSize: 12,
    fontWeight: '600',
    color: '#0284C7',
  },
});

CustomerCard.displayName = 'CustomerCard';

export default CustomerCard;
