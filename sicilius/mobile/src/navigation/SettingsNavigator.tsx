import React, { useMemo } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { lightColors } from '../theme';
import { NativeStackNavigationOptions } from '@react-navigation/native-stack';

import SettingsScreen from '../screens/settings/SettingsScreen';
import { SettingsStackParamList } from './types';

const Stack = createNativeStackNavigator<SettingsStackParamList>();

// Sabit ekran konfigürasyonları
const SETTINGS_SCREEN_CONFIG = Object.freeze({
  SettingsList: {
    title: 'Ayarlar',
    component: SettingsScreen
  }
});

const SettingsNavigator = React.memo(() => {
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
  const SettingsScreens = useMemo(() => (
    Object.entries(SETTINGS_SCREEN_CONFIG).map(([name, config]) => (
      <Stack.Screen
        key={name}
        name={name as keyof SettingsStackParamList}
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
      {SettingsScreens}
    </Stack.Navigator>
  );
});

export default SettingsNavigator;
