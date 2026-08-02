import React, { memo } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';
import { Customer } from '../../types/customer';
import { lightColors } from '../../theme';

interface CustomerContactProps {
  customer: Customer | null;
}

const CustomerContact = memo<CustomerContactProps>(({ customer }) => {
  const addressText = typeof customer?.address === 'string'
    ? customer.address
    : (customer?.address?.street ? `${customer.address.street}, ${customer.address.city || ''}` : 'Adres belirtilmedi');

  return (
    <View style={styles.container}>
      <Text style={styles.sectionTitle}>İletişim Bilgileri</Text>
      <View style={styles.detailItem}>
        <Icon name="phone" size={20} color={lightColors.primary} />
        <Text style={styles.detailText}>{customer?.phone || 'Belirtilmedi'}</Text>
      </View>
      <View style={styles.detailItem}>
        <Icon name="email" size={20} color={lightColors.primary} />
        <Text style={styles.detailText}>{customer?.email || 'Belirtilmedi'}</Text>
      </View>
      <View style={styles.detailItem}>
        <Icon name="map-marker" size={20} color={lightColors.primary} />
        <Text style={styles.detailText}>{addressText}</Text>
      </View>
    </View>
  );
});

const styles = StyleSheet.create({
  container: {
    paddingVertical: 4,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: lightColors.text,
    marginBottom: 12,
  },
  detailItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 6,
  },
  detailText: {
    flex: 1,
    fontSize: 14,
    color: lightColors.text,
    marginLeft: 12,
  },
});

CustomerContact.displayName = 'CustomerContact';

export default CustomerContact;
