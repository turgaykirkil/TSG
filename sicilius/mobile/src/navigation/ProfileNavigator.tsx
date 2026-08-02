import React, { useMemo } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { lightColors } from '../theme';
import { NativeStackNavigationOptions } from '@react-navigation/native-stack';

import ProfileScreen from '../screens/main/ProfileScreen';
import ProfileEditScreen from '../screens/main/ProfileEditScreen';
import ProfileSettingsScreen from '../screens/main/ProfileSettingsScreen';
import { ProfileStackParamList } from './types';

const Stack = createNativeStackNavigator<ProfileStackParamList>();

// Sabit ekran konfigürasyonları
const SCREEN_CONFIG = Object.freeze({
  ProfileMain: {
    title: 'Profil',
    component: ProfileScreen
  },
  ProfileEdit: {
    title: 'Profili Düzenle',
    component: ProfileEditScreen
  },
  ProfileSettings: {
    title: 'Profil Ayarları',
    component: ProfileSettingsScreen
  }
});

const ProfileNavigator = React.memo(() => {
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
  const ProfileScreens = useMemo(() => (
    Object.entries(SCREEN_CONFIG).map(([name, config]) => (
      <Stack.Screen
        key={name}
        name={name as keyof ProfileStackParamList}
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
      {ProfileScreens}
    </Stack.Navigator>
  );
});

export default ProfileNavigator;
