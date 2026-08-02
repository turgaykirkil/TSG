import React, { memo } from 'react';
import { FlatList, RefreshControl, View, StyleSheet, Text } from 'react-native';
import { Customer } from '../types/customer';
import CustomerCard from './CustomerCard';

type CustomerListProps = {
  customers: Customer[];
  onCustomerPress: (customer: Customer) => void;
  refreshing: boolean;
  onRefresh: () => void;
};

const CustomerList = memo<CustomerListProps>(({
  customers,
  onCustomerPress,
  refreshing,
  onRefresh,
}) => {
  const renderItem = ({ item }: { item: Customer }) => (
    <CustomerCard customer={item} onPress={onCustomerPress} />
  );

  if (customers.length === 0) {
    return (
      <View style={styles.emptyContainer}>
        <Text>Müşteri bulunamadı.</Text>
      </View>
    );
  }

  return (
    <FlatList
      data={customers}
      renderItem={renderItem}
      keyExtractor={item => item.id.toString()}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
      contentContainerStyle={styles.listContent}
    />
  );
});

const styles = StyleSheet.create({
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 32,
  },
  listContent: {
    paddingBottom: 16,
  },
});

CustomerList.displayName = 'CustomerList';

export default CustomerList;
