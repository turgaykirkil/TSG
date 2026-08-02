import { TypedUseSelectorHook, useDispatch, useSelector } from 'react-redux';
import type { RootState, AppDispatch } from './index';

// Redux için type-safe hooks
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// Network durumu için hook
export const useNetworkStatus = () => {
  return useAppSelector((state) => ({
    isOnline: state.network.isOnline,
    lastOnline: state.network.lastOnline,
  }));
};

// Senkronizasyon durumu için hook
export const useSyncStatus = () => {
  return useAppSelector((state) => ({
    isSyncing: state.sync.isSyncing,
    lastSync: state.sync.lastSync,
    error: state.sync.error,
    queueLength: state.sync.queueLength,
  }));
};