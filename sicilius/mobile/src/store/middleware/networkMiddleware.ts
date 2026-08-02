import { Middleware } from '@reduxjs/toolkit';
import NetInfo from '@react-native-community/netinfo';

// Ağ durumunu kontrol eden eylemler
export const networkActions = {
  SET_ONLINE: 'network/setOnline',
  SET_OFFLINE: 'network/setOffline',
};

// Ağ durumunu takip eden middleware
export const networkMiddleware: Middleware = store => {
  // Ağ durumunu dinle
  NetInfo.addEventListener(state => {
    if (state.isConnected) {
      store.dispatch({ type: networkActions.SET_ONLINE });
    } else {
      store.dispatch({ type: networkActions.SET_OFFLINE });
    }
  });

  return (next: (action: unknown) => unknown) => (action: unknown) => {
    // Eğer çevrimdışıysa ve API çağrısı yapılıyorsa, eylemi kuyrukla
    if (
      typeof action === 'object' &&
      action !== null &&
      'meta' in action &&
      typeof action.meta === 'object' &&
      action.meta !== null &&
      'requiresNetwork' in action.meta &&
      action.meta.requiresNetwork &&
      !store.getState().network.isOnline
    ) {
      store.dispatch({
        type: 'sync/queueAction',
        payload: action,
      });
      return;
    }

    return next(action);
  };
};
