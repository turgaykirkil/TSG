import React, { useEffect, useState } from 'react';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { Provider as ReduxProvider, useSelector } from 'react-redux';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { StyleSheet, StatusBar, View, ActivityIndicator } from 'react-native';
import * as SplashScreen from 'expo-splash-screen';

import store from './src/store/store';
import AppNavigator from './src/navigation/AppNavigator';
import { lightColors, darkColors } from './src/theme';
import { login } from './src/store/authSlice';
import SiciliusLogo from './src/components/common/SiciliusLogo';

SplashScreen.hideAsync().catch(() => {});

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  splashContainer: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    alignItems: 'center',
    justifyContent: 'center',
  },
});

const MainAppContent: React.FC = () => {
  const isDarkMode = useSelector((state: any) => state.theme?.isDarkMode ?? false);
  const colors = isDarkMode ? darkColors : lightColors;

  return (
    <SafeAreaProvider>
      <StatusBar
        barStyle={isDarkMode ? 'light-content' : 'dark-content'}
        backgroundColor={colors.background}
      />
      <AppNavigator />
    </SafeAreaProvider>
  );
};

const App: React.FC = () => {
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    const initializeApp = async () => {
      try {
        const userData = await AsyncStorage.getItem('userData');
        if (userData) {
          store.dispatch(login(JSON.parse(userData)));
        }
        await new Promise((resolve) => setTimeout(resolve, 2000));
      } catch (error) {
        console.error('Error initializing app:', error);
      } finally {
        setIsInitialized(true);
      }
    };

    initializeApp();
  }, []);

  if (!isInitialized) {
    return (
      <View style={styles.splashContainer}>
        <StatusBar barStyle="dark-content" backgroundColor="#FFFFFF" />
        <SiciliusLogo size={80} showText={true} textColor="#0EA5E9" />
        <ActivityIndicator color="#0EA5E9" style={{ marginTop: 28 }} />
      </View>
    );
  }

  return (
    <GestureHandlerRootView style={styles.container}>
      <ReduxProvider store={store}>
        <MainAppContent />
      </ReduxProvider>
    </GestureHandlerRootView>
  );
};

export default App;
