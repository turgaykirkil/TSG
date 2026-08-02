export interface CustomerAddress {
  street?: string;
  city?: string;
  state?: string;
  zipCode?: string;
  country?: string;
  coordinates: {
    lat: number;
    lng: number;
  };
}

export type Customer = {
  id: string | number;
  name: string;
  company: string;
  email: string;
  phone: string;
  distance?: number;
  status: string;
  salesRepId?: string;
  notes?: string;
  tags?: string[];
  priorityScore?: number;
  weatherPenalty?: number;
  trafficPenalty?: number;
  location?: {
    latitude: number;
    longitude: number;
  };
  statistics?: {
    totalOrders: number;
    totalRevenue: number;
    lastOrderDate: string;
  };
  createdAt?: string;
  updatedAt?: string;
  latitude?: number;
  longitude?: number;
  address: CustomerAddress;
};

export interface CustomerState {
  customers: Customer[];
  selectedCustomer: Customer | null;
  loading: boolean;
  error: string | null;
  filters: {
    search: string;
    sortBy: 'name' | 'company' | 'createdAt';
    sortOrder: 'asc' | 'desc';
  };
}

export type CustomerFilters = CustomerState['filters'];
export type CustomerSortField = CustomerFilters['sortBy'];
export type SortOrder = CustomerFilters['sortOrder'];
