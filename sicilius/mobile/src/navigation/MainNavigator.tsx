import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { Platform } from 'react-native';

import HomeScreen from '../screens/main/HomeScreen';
import TaskNavigator from './TaskNavigator';
import CustomerNavigator from './CustomerNavigator';
import RouteOptimizationScreen from '../screens/route/RouteOptimizationScreen';
import SettingsNavigator from './SettingsNavigator';

import { MainTabParamList } from './types';
import { BottomTabNavigationOptions } from '@react-navigation/bottom-tabs';
import { lightColors } from '../theme';

const Tab = createBottomTabNavigator<MainTabParamList>();

// Performans için sabit icon mapping
const TAB_ICONS: Record<keyof MainTabParamList, string> = Object.freeze({
  'Home': 'home-variant',
  'Tasks': 'clipboard-check-outline',
  'Map': 'map-marker-radius-outline',
  'Route': 'map-marker-path',
  'Customers': 'account-group-outline',
  'Settings': 'cog-outline'
});

// Performans için memoize edilmiş icon fonksiyonu
const createTabBarIcon = (route: { name: keyof MainTabParamList }) => {
  const iconName = TAB_ICONS[route.name] || 'circle';
  
  return ({ color, size }: { color: string; size: number }) => (
    <MaterialCommunityIcons 
      name={iconName as any} 
      size={size} 
      color={color} 
      key={iconName}
    />
  );
};

const MainNavigator = () => {
  // Performans için optimize edilmiş screenOptions
  const screenOptions = ({ route }: { route: { name: keyof MainTabParamList } }): BottomTabNavigationOptions => ({
    headerShown: false,
    tabBarActiveTintColor: lightColors.primary,
    tabBarInactiveTintColor: lightColors.disabled,
    tabBarStyle: {
      backgroundColor: lightColors.surface,
      borderTopColor: lightColors.border,
      borderTopWidth: 0.5,
      elevation: 0,
      shadowOpacity: 0,
      height: Platform.OS === 'ios' ? 88 : 64,
      paddingBottom: Platform.OS === 'ios' ? 28 : 8,
      paddingTop: 8,
    },
    tabBarLabelStyle: {
      fontSize: 11,
      fontWeight: '600',
    },
    tabBarIcon: createTabBarIcon(route)
  });

  return (
    <Tab.Navigator
      screenOptions={screenOptions}
      detachInactiveScreens={true}
      sceneContainerStyle={{ backgroundColor: 'transparent' }}
    >
      <Tab.Screen 
        name="Home" 
        component={HomeScreen} 
        options={{ 
          title: 'Ana Sayfa',
          lazy: true 
        }} 
      />
      <Tab.Screen 
        name="Tasks" 
        component={TaskNavigator} 
        options={{ 
          title: 'Görevler',
          lazy: true 
        }} 
      />
      <Tab.Screen 
        name="Route" 
        component={RouteOptimizationScreen} 
        options={{ 
          title: 'Rota',
          lazy: true 
        }} 
      />
      <Tab.Screen 
        name="Customers" 
        component={CustomerNavigator} 
        options={{ 
          title: 'Müşteriler',
          lazy: true 
        }} 
      />
      <Tab.Screen 
        name="Settings" 
        component={SettingsNavigator}
        options={{ 
          title: 'Ayarlar',
          lazy: true 
        }} 
      />
    </Tab.Navigator>
  );
};

export default MainNavigator;
