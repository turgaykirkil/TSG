import React, { useEffect, useMemo, useCallback } from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { lightColors } from '../theme';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { ActivityIndicator, View } from 'react-native';

import AuthNavigator from './AuthNavigator';
import MainNavigator from './MainNavigator';
import ProfileNavigator from './ProfileNavigator';
import { RootStackParamList } from './types';

const Stack = createNativeStackNavigator<RootStackParamList>();

// Loading Component'i optimize et ve memoize et
const LoadingComponent = React.memo(() => (
  <View 
    style={{ 
      flex: 1, 
      justifyContent: 'center', 
      alignItems: 'center',
      backgroundColor: lightColors.background 
    }}
    testID="loading-container"
  >
    <ActivityIndicator 
      size="large" 
      color={lightColors.primary} 
      testID="root-loading-indicator"
      accessibilityLabel="Yükleniyor"
    />
  </View>
));

const RootNavigator = React.memo(() => {
  const authState = useSelector((state: RootState) => state.auth as any);
  const isAuthenticated = authState?.isAuthenticated ?? false;
  const loading = authState?.loading ?? false;

  if (loading) {
    return <LoadingComponent />;
  }

  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {!isAuthenticated ? (
        <Stack.Group screenOptions={{ gestureEnabled: false }}>
          <Stack.Screen name="Auth" component={AuthNavigator} />
        </Stack.Group>
      ) : (
        <Stack.Group screenOptions={{ gestureEnabled: false }}>
          <Stack.Screen name="Main" component={MainNavigator} />
          <Stack.Screen 
            name="Profile" 
            component={ProfileNavigator} 
            options={{ presentation: 'modal' }}
          />
        </Stack.Group>
      )}
    </Stack.Navigator>
  );
});

export default RootNavigator;
