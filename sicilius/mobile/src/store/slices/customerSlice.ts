import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Customer, CustomerState, CustomerFilters } from '../../types/customer';
import customerService from '../../services/customerService';

const initialState: CustomerState = {
  customers: [],
  selectedCustomer: null,
  loading: false,
  error: null,
  filters: {
    search: '',
    sortBy: 'name',
    sortOrder: 'asc',
  },
};

// Offline-aware thunks
export const fetchCustomers = createAsyncThunk(
  'customers/fetchCustomers',
  async (_, { dispatch }) => {
    dispatch({
      type: 'customers/fetchCustomers/pending',
      meta: { requiresNetwork: true }
    });
    const response = await customerService.getCustomers();
    return response;
  }
);

export const fetchCustomerById = createAsyncThunk(
  'customers/fetchCustomerById',
  async (customerId: string) => {
    const response = await customerService.getCustomerById(customerId);
    return response;
  }
);

export const createCustomer = createAsyncThunk(
  'customers/createCustomer',
  async (customerData: Partial<Customer>, { dispatch }) => {
    dispatch({
      type: 'customers/createCustomer/pending',
      meta: { requiresNetwork: true }
    });
    const response = await customerService.createCustomer(customerData as any);
    return response;
  }
);

export const updateCustomer = createAsyncThunk(
  'customers/updateCustomer',
  async ({ id, ...customerData }: Partial<Customer> & { id: string }, { dispatch }) => {
    dispatch({
      type: 'customers/updateCustomer/pending',
      meta: { requiresNetwork: true }
    });
    const response = await customerService.updateCustomer(id, customerData);
    return response;
  }
);

export const deleteCustomer = createAsyncThunk(
  'customers/deleteCustomer',
  async (customerId: string, { dispatch }) => {
    dispatch({
      type: 'customers/deleteCustomer/pending',
      meta: { requiresNetwork: true }
    });
    await customerService.deleteCustomer(customerId);
    return customerId;
  }
);

export const updateCustomerLocation = createAsyncThunk(
  'customers/updateLocation',
  async ({ id, location }: { id: string; location: { latitude: number; longitude: number } }, { dispatch }) => {
    dispatch({
      type: 'customers/updateLocation/pending',
      meta: { requiresNetwork: true }
    });
    const response = await customerService.updateCustomerLocation(id, location);
    return response;
  }
);

const customerSlice = createSlice({
  name: 'customers',
  initialState,
  reducers: {
    setFilters: (state, action: PayloadAction<Partial<CustomerFilters>>) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    clearFilters: (state) => {
      state.filters = initialState.filters;
    },
    clearSelectedCustomer: (state) => {
      state.selectedCustomer = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch Customers
    builder
      .addCase(fetchCustomers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCustomers.fulfilled, (state, action) => {
        state.loading = false;
        state.customers = action.payload;
      })
      .addCase(fetchCustomers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch customers';
      });

    // Fetch Customer by ID
    builder
      .addCase(fetchCustomerById.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchCustomerById.fulfilled, (state, action) => {
        state.loading = false;
        state.selectedCustomer = action.payload;
      })
      .addCase(fetchCustomerById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch customer';
      });

    // Create Customer
    builder
      .addCase(createCustomer.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createCustomer.fulfilled, (state, action) => {
        state.loading = false;
        state.customers.push(action.payload);
      })
      .addCase(createCustomer.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to create customer';
      });

    // Update Customer
    builder
      .addCase(updateCustomer.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateCustomer.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.customers.findIndex((c) => c.id === action.payload.id);
        if (index !== -1) {
          state.customers[index] = action.payload;
        }
        if (state.selectedCustomer?.id === action.payload.id) {
          state.selectedCustomer = action.payload;
        }
      })
      .addCase(updateCustomer.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to update customer';
      });

    // Delete Customer
    builder
      .addCase(deleteCustomer.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteCustomer.fulfilled, (state, action) => {
        state.loading = false;
        state.customers = state.customers.filter((c) => String(c.id) !== String(action.payload));
        if (state.selectedCustomer && String(state.selectedCustomer.id) === String(action.payload)) {
          state.selectedCustomer = null;
        }
      })
      .addCase(deleteCustomer.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to delete customer';
      });

    // Update Customer Location
    builder
      .addCase(updateCustomerLocation.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateCustomerLocation.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.customers.findIndex((c) => c.id === action.payload.id);
        if (index !== -1) {
          state.customers[index] = action.payload;
        }
        if (state.selectedCustomer?.id === action.payload.id) {
          state.selectedCustomer = action.payload;
        }
      })
      .addCase(updateCustomerLocation.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to update customer location';
      });
  },
});

export const { setFilters, clearFilters, clearSelectedCustomer } = customerSlice.actions;

export const selectCustomers = (state: any) => state.customers.customers;
export const selectLoading = (state: any) => state.customers.loading;

export default customerSlice.reducer;
