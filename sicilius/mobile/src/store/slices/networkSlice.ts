import { createSlice } from '@reduxjs/toolkit';
import { networkActions } from '../middleware/networkMiddleware';

interface NetworkState {
  isOnline: boolean;
  lastOnline: string | null;
}

const initialState: NetworkState = {
  isOnline: true,
  lastOnline: null,
};

const networkSlice = createSlice({
  name: 'network',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(networkActions.SET_ONLINE, (state) => {
        state.isOnline = true;
        state.lastOnline = new Date().toISOString();
      })
      .addCase(networkActions.SET_OFFLINE, (state) => {
        state.isOnline = false;
      });
  },
});

export default networkSlice.reducer;
