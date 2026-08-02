import { configureStore, combineReducers } from '@reduxjs/toolkit';
import { 
  persistStore, 
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER 
} from 'redux-persist';
import AsyncStorage from '@react-native-async-storage/async-storage';

import authReducer from './slices/authSlice';
import taskReducer from './slices/taskSlice';
import customerReducer from './slices/customerSlice';
import networkReducer from './slices/networkSlice';
import syncReducer from './slices/syncSlice';
import themeReducer from './slices/themeSlice';
import { networkMiddleware } from './middleware/networkMiddleware';
import { syncMiddleware } from './middleware/syncMiddleware';

const persistConfig = {
  key: 'root',
  version: 1,
  storage: AsyncStorage,
  whitelist: ['auth', 'theme'] // Add theme to whitelist
};

const rootReducer = combineReducers({
  auth: authReducer,
  tasks: taskReducer,
  customers: customerReducer,
  network: networkReducer,
  sync: syncReducer,
  theme: themeReducer, // Add theme reducer
});

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }).concat(networkMiddleware, syncMiddleware),
});

export const persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
