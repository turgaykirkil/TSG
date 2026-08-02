import React, { useMemo } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { lightColors } from '../theme';
import { NativeStackNavigationOptions } from '@react-navigation/native-stack';

import CustomerListScreen from '../screens/customers/CustomerListScreen';
import CustomerDetailScreen from '../screens/customers/CustomerDetailScreen';
import NewCustomerScreen from '../screens/customers/NewCustomerScreen';
import EditCustomerScreen from '../screens/customers/EditCustomerScreen';
import CustomerMapScreen from '../screens/customers/CustomerMapScreen';
import CustomerAnalyticsScreen from '../screens/analytics/CustomerAnalyticsScreen';
import { CustomerStackParamList } from './types';

const Stack = createNativeStackNavigator<CustomerStackParamList>();

// Sabit ekran konfigürasyonları
const CUSTOMER_SCREEN_CONFIG = Object.freeze({
  CustomerList: {
    title: 'Müşteriler',
    component: CustomerListScreen
  },
  CustomerDetail: {
    title: 'Müşteri Detayı',
    component: CustomerDetailScreen
  },
  NewCustomer: {
    title: 'Yeni Müşteri',
    component: NewCustomerScreen
  },
  EditCustomer: {
    title: 'Müşteri Düzenle',
    component: EditCustomerScreen
  },
  CustomerMap: {
    title: 'Müşteri Haritası',
    component: CustomerMapScreen
  },
  CustomerAnalytics: {
    title: 'Müşteri Analizi',
    component: CustomerAnalyticsScreen
  }
});

const CustomerNavigator = React.memo(() => {
  // Navigator seçeneklerini memoize et
  const navigatorScreenOptions = useMemo<NativeStackNavigationOptions>(() => ({
    headerStyle: {
      backgroundColor: lightColors.primary,
    },
    headerTintColor: '#fff',
    headerTitleStyle: {
      fontWeight: 'bold',
    },
    // Performans için ek ayarlar
    animation: 'slide_from_right',
    gestureEnabled: true,
    detachInactiveScreens: true
  }), []);

  // Ekran tanımlamalarını memoize et
  const CustomerScreens = useMemo(() => (
    Object.entries(CUSTOMER_SCREEN_CONFIG).map(([name, config]) => (
      <Stack.Screen
        key={name}
        name={name as keyof CustomerStackParamList}
        component={config.component}
        options={{
          title: config.title,
        }}
      />
    ))
  ), []);

  return (
    <Stack.Navigator
      screenOptions={navigatorScreenOptions}
    >
      {CustomerScreens}
    </Stack.Navigator>
  );
});

export default CustomerNavigator;
