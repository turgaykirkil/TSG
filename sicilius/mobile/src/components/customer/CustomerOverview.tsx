import React, { memo } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Customer } from '../../types/customer';
import { lightColors } from '../../theme';

interface CustomerOverviewProps {
  customer: Customer | null;
}

const CustomerOverview = memo<CustomerOverviewProps>(({ customer }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.sectionTitle}>Ticari Özet</Text>
      <View style={styles.statsContainer}>
        <View style={styles.statItem}>
          <Text style={styles.statNumber}>
            {(customer as any)?.totalOrders !== undefined ? (customer as any).totalOrders : '0'}
          </Text>
          <Text style={styles.statLabel}>Toplam Sipariş</Text>
        </View>
        <View style={styles.verticalDivider} />
        <View style={styles.statItem}>
          <Text style={styles.statNumber}>
            {(customer as any)?.totalRevenue !== undefined ? `₺${(customer as any).totalRevenue.toLocaleString('tr-TR')}` : '₺0'}
          </Text>
          <Text style={styles.statLabel}>Toplam Hacim</Text>
        </View>
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
    marginBottom: 16,
  },
  statsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statItem: {
    flex: 1,
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 20,
    fontWeight: 'bold',
    color: lightColors.primary,
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 13,
    color: lightColors.subtext,
  },
  verticalDivider: {
    width: 1,
    height: '80%',
    backgroundColor: lightColors.border,
  },
});

CustomerOverview.displayName = 'CustomerOverview';

export default CustomerOverview;
