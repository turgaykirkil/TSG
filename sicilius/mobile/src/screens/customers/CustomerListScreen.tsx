import React, { useState, useMemo, useLayoutEffect } from 'react';
import { View, StyleSheet, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { MaterialCommunityIcons as Icon } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { CustomerStackNavigationProp } from '../../navigation/types';
import { useCustomers } from '../../hooks/useCustomers';
import { lightColors } from '../../theme';

import CustomerListSearchBar from '../../components/customers/CustomerListSearchBar';
import CustomerListContent from '../../components/customers/CustomerListContent';
import CustomerListFAB from '../../components/customers/CustomerListFAB';

const CustomerListScreen: React.FC = () => {
  const navigation = useNavigation<CustomerStackNavigationProp>();
  const { customers, loading } = useCustomers();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCustomer, setSelectedCustomer] = useState<any>(null);
  const [isCallModalVisible, setIsCallModalVisible] = useState(false);

  useLayoutEffect(() => {
    navigation.setOptions({
      headerRight: () => (
        <View style={{ flexDirection: 'row', alignItems: 'center' }}>
          <TouchableOpacity
            style={{ padding: 8, marginRight: 6 }}
            onPress={() => navigation.navigate('CustomerMap')}
          >
            <Icon name="map-marker-radius" size={24} color="#FFFFFF" />
          </TouchableOpacity>
          <TouchableOpacity
            style={{ padding: 8, marginRight: 4 }}
            onPress={() => navigation.navigate('CustomerAnalytics')}
          >
            <Icon name="chart-box-outline" size={24} color="#FFFFFF" />
          </TouchableOpacity>
        </View>
      ),
    });
  }, [navigation]);

  const styles = useMemo(
    () =>
      StyleSheet.create({
        safeArea: {
          flex: 1,
          backgroundColor: lightColors.background,
        },
        container: {
          flex: 1,
          backgroundColor: lightColors.background,
        },
      }),
    []
  );

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <CustomerListSearchBar
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
        />
        <CustomerListContent
          customers={customers}
          loading={loading}
          searchQuery={searchQuery}
          onCustomerSelect={setSelectedCustomer}
          onCallModalToggle={setIsCallModalVisible}
        />
        <CustomerListFAB />
      </View>
    </SafeAreaView>
  );
};

export default CustomerListScreen;