import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Temporarily import db.json content for testing
const db = {
  "users": [
    {
      "id": "1",
      "email": "admin@sicilius.com.tr",
      "password": "123456",
      "name": "Admin User",
      "role": "admin",
      "canViewAll": true
    },
    {
      "id": "2",
      "email": "supervisor@sicilius.com.tr",
      "password": "123456",
      "name": "Supervisor User",
      "role": "supervisor",
      "canViewAll": true
    },
    {
      "id": "3",
      "email": "marmara@sicilius.com.tr",
      "password": "123456",
      "name": "Ahmet Yılmaz",
      "role": "sales_rep",
      "region": "Marmara",
      "canViewAll": false
    },
    {
      "id": "4",
      "email": "ege@sicilius.com.tr",
      "password": "123456",
      "name": "Mehmet Demir",
      "role": "sales_rep",
      "region": "Ege",
      "canViewAll": false
    },
    {
      "id": "5",
      "email": "anadolu@sicilius.com.tr",
      "password": "123456",
      "name": "Ayşe Kaya",
      "role": "sales_rep",
      "region": "İç Anadolu",
      "canViewAll": false
    }
  ]
};

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
};

export const loginAsync = createAsyncThunk(
  'auth/loginAsync',
  async (credentials: { email: string; password: string; rememberMe?: boolean }) => {
    try {
      // Simulate fetching user data from db.json
      const user = db.users.find(
        (u) => u.email === credentials.email && u.password === credentials.password
      );

      if (!user) throw new Error('Giriş başarısız oldu');

      if (credentials.rememberMe) {
        await AsyncStorage.setItem('userToken', 'dummy-token');
      }

      return user;
    } catch (error) {
      throw new Error('Giriş başarısız oldu');
    }
  }
);

export const logoutAsync = createAsyncThunk(
  'auth/logoutAsync',
  async (_, { dispatch }) => {
    await AsyncStorage.removeItem('userToken');
    dispatch(logout()); // Logout reducer'ını çağırarak state güncellemesi
    return true;
  }
);

export const checkAuthAsync = createAsyncThunk(
  'auth/checkAuthAsync',
  async () => {
    try {
      const token = await AsyncStorage.getItem('userToken');
      if (!token) {
        throw new Error('Token bulunamadı');
      }
      
      // TODO: Validate token with API
      return {
        user: {
          id: '1',
          email: 'test@example.com',
          name: 'Test User',
          role: 'test',
        },
      };
    } catch (error) {
      throw error;
    }
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    login: (state, action: PayloadAction<User>) => {
      state.user = action.payload;
      state.isAuthenticated = true;
    },
    logout: (state) => {
      state.user = null;
      state.isAuthenticated = false;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginAsync.fulfilled, (state, action) => {
        state.user = action.payload;
        state.isAuthenticated = true;
      })
      .addCase(logoutAsync.fulfilled, (state) => {
        state.user = null;
        state.isAuthenticated = false;
      })
      .addCase(checkAuthAsync.fulfilled, (state, action) => {
        state.user = action.payload.user;
        state.isAuthenticated = true;
      });
  },
});

export const { login, logout } = authSlice.actions;
export default authSlice.reducer;
