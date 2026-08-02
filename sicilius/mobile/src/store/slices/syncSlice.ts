import { createSlice } from '@reduxjs/toolkit';
import { syncActions } from '../middleware/syncMiddleware';

interface SyncState {
  isSyncing: boolean;
  lastSync: string | null;
  error: string | null;
  queueLength: number;
}

const initialState: SyncState = {
  isSyncing: false,
  lastSync: null,
  error: null,
  queueLength: 0,
};

const syncSlice = createSlice({
  name: 'sync',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(syncActions.SYNC_START, (state) => {
        state.isSyncing = true;
        state.error = null;
      })
      .addCase(syncActions.SYNC_SUCCESS, (state) => {
        state.isSyncing = false;
        state.lastSync = new Date().toISOString();
        state.error = null;
        state.queueLength = 0;
      })
      .addCase(syncActions.SYNC_FAILURE, (state, action) => {
        state.isSyncing = false;
        state.error = (action as any).error || 'Sync failed';
      })
      .addCase(syncActions.QUEUE_ACTION, (state) => {
        state.queueLength += 1;
      });
  },
});

export default syncSlice.reducer;
