import { Middleware } from '@reduxjs/toolkit';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Senkronizasyon durumlarını tutan sabitler
export const syncActions = {
  QUEUE_ACTION: 'sync/queueAction',
  SYNC_START: 'sync/start',
  SYNC_SUCCESS: 'sync/success',
  SYNC_FAILURE: 'sync/failure',
};

// Senkronizasyon kuyruğunu yöneten middleware
export const syncMiddleware: Middleware = store => {
  let syncInProgress = false;
  const SYNC_QUEUE_KEY = '@sync_queue';

  // Kuyruktaki eylemleri yükle
  const loadQueue = async () => {
    try {
      const queue = await AsyncStorage.getItem(SYNC_QUEUE_KEY);
      return queue ? JSON.parse(queue) : [];
    } catch (error) {
      console.error('Error loading sync queue:', error);
      return [];
    }
  };

  // Kuyruğu kaydet
  const saveQueue = async (queue: any[]) => {
    try {
      await AsyncStorage.setItem(SYNC_QUEUE_KEY, JSON.stringify(queue));
    } catch (error) {
      console.error('Error saving sync queue:', error);
    }
  };

  // Senkronizasyonu başlat
  const startSync = async () => {
    if (syncInProgress) return;
    
    syncInProgress = true;
    store.dispatch({ type: syncActions.SYNC_START });

    try {
      const queue = await loadQueue();
      
      // Kuyruktaki her eylemi sırayla işle
      for (const action of queue) {
        try {
          // Eylemi tekrar gönder
          await store.dispatch({ ...action, meta: { ...action.meta, isRetry: true } });
        } catch (error) {
          console.error('Error processing queued action:', error);
          // Hatalı eylemi işaretleyebilir veya kaldırabilirsiniz
        }
      }

      // Başarılı senkronizasyon
      await AsyncStorage.setItem(SYNC_QUEUE_KEY, '[]');
      store.dispatch({ type: syncActions.SYNC_SUCCESS });
    } catch (error) {
      // Senkronizasyon hatası
      store.dispatch({ 
        type: syncActions.SYNC_FAILURE,
        error: error.message 
      });
    } finally {
      syncInProgress = false;
    }
  };

  return next => (action: any) => {
    // Eylem kuyruğa ekleniyorsa
    if (action?.type === syncActions.QUEUE_ACTION) {
      loadQueue().then(queue => {
        queue.push(action.payload);
        saveQueue(queue);
      });
      return;
    }

    // Çevrimiçi olduğumuzda senkronizasyonu başlat
    if (action.type === 'network/setOnline' && !syncInProgress) {
      startSync();
    }

    return next(action);
  };
};