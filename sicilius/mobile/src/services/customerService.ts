import axios from 'axios';
import { Customer } from '../types/customer';
import api, { customerAPI } from './api';

// Web veritabanında yer alan 4 adet jeokodlanmış sabit firma verisi (Fallback / Tampon)
const FALLBACK_GEOLOCATION_COMPANIES: Customer[] = [
  {
    id: 'company_8d9cc4a9-d4f1-4ac8-8395-641c20b5d8c1',
    name: 'TASFİYE HALİNDE GOLD FRUITS TARIM SANAYİ VE TİCARET LIMITED ŞİRKETİ',
    company: 'TASFİYE HALİNDE GOLD FRUITS TARIM SANAYİ VE TİCARET LIMITED ŞİRKETİ',
    email: 'info@goldfruits.com.tr',
    phone: '0224 123 45 67',
    status: 'active',
    salesRepId: '1',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    address: {
      street: 'Aktarhüssam Mah. Ahmet Hamdi Tanpinar Cad. Öndül İş Hanı No: 17/209',
      city: 'Bursa',
      state: 'Osmangazi',
      zipCode: '16000',
      country: 'Türkiye',
      coordinates: {
        lat: 40.1982203,
        lng: 29.0612098,
      }
    },
    latitude: 40.1982203,
    longitude: 29.0612098,
  },
  {
    id: 'company_68df9ba4-8486-4df6-936a-b126dc4d7d6e',
    name: 'DCEY GRUP TEKSTİL PAZARLAMA SANAYİ VE TİCARET LİMİTED ŞİRKETİ',
    company: 'DCEY GRUP TEKSTİL PAZARLAMA SANAYİ VE TİCARET LİMİTED ŞİRKETİ',
    email: 'contact@dcey.com.tr',
    phone: '0252 890 12 34',
    status: 'active',
    salesRepId: '1',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    address: {
      street: 'Cumhuriyet Mh. Atatürk Cd. No:101 / 8 Beldibi',
      city: 'Muğla',
      state: 'Marmaris',
      zipCode: '48704',
      country: 'Türkiye',
      coordinates: {
        lat: 36.8522547,
        lng: 28.2742661,
      }
    },
    latitude: 36.8522547,
    longitude: 28.2742661,
  },
  {
    id: 'company_54bd90fe-cb20-41ce-acd7-5c12980b878b',
    name: '212ENDÜSTRİ KALIP MAKİNE SANAYİ VE TİCARET LİMİTED ŞİRKETİ',
    company: '212ENDÜSTRİ KALIP MAKİNE SANAYİ VE TİCARET LİMİTED ŞİRKETİ',
    email: 'info@212endustri.com',
    phone: '0212 345 67 89',
    status: 'active',
    salesRepId: '1',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    address: {
      street: 'Çeliktepe Mah. Hatmi Sk. No: 10a',
      city: 'İstanbul',
      state: 'Kağıthane',
      zipCode: '34413',
      country: 'Türkiye',
      coordinates: {
        lat: 41.0796544,
        lng: 28.9731198,
      }
    },
    latitude: 41.0796544,
    longitude: 28.9731198,
  },
  {
    id: 'company_ec9ff9c9-c499-4a85-bffa-8a26fc8918af',
    name: 'BORIS BORISENKO GAYRIMENKUL',
    company: 'BORIS BORISENKO GAYRIMENKUL',
    email: 'boris@borisenko.com',
    phone: '0212 987 65 43',
    status: 'active',
    salesRepId: '1',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    address: {
      street: 'Levent Mah. Mektep Sk. No: 8',
      city: 'İstanbul',
      state: 'Beşiktaş',
      zipCode: '34330',
      country: 'Türkiye',
      coordinates: {
        lat: 41.0364416,
        lng: 29.0109015,
      }
    },
    latitude: 41.0364416,
    longitude: 29.0109015,
  },
];

export const customerService = {
  getCustomers: async (userRole?: string, userId?: string): Promise<Customer[]> => {
    let mappedCustomers: Customer[] = [];

    // 1. Fetch B2B customers from API
    try {
      const data = await customerAPI.getAll();
      if (Array.isArray(data)) {
        mappedCustomers = data.map((c: any) => ({
          id: String(c.id),
          name: c.company_name || c.title || c.name || 'Müşteri',
          company: c.company_name || c.title || 'B2B Müşteri',
          email: c.contact_email || c.email || '',
          phone: c.phone || '',
          status: c.status || 'active',
          salesRepId: c.sales_rep_id || c.salesRepId || '1',
          createdAt: c.created_at || new Date().toISOString(),
          updatedAt: c.updated_at || new Date().toISOString(),
          address: {
            street: typeof c.address === 'string' ? c.address : String(c.address?.street || c.address?.title || 'Adres belirtilmedi'),
            city: typeof c.address?.city === 'string' ? c.address.city : 'İstanbul',
            state: '',
            zipCode: '',
            country: 'Türkiye',
            coordinates: {
              lat: typeof c.latitude === 'number' ? c.latitude : (c.address?.coordinates?.lat || 0),
              lng: typeof c.longitude === 'number' ? c.longitude : (c.address?.coordinates?.lng || 0),
            }
          },
          latitude: typeof c.latitude === 'number' ? c.latitude : (c.address?.coordinates?.lat || 0),
          longitude: typeof c.longitude === 'number' ? c.longitude : (c.address?.coordinates?.lng || 0),
        }));
      }
    } catch (error) {
      console.warn('b2b-customers API error, proceeding with company pins:', error);
    }

    // 2. Fetch geocoded company map pins from API (with fallback URLs for local dev)
    let companyFetched = false;
    let pinData: any[] = [];

    const endpointsToTry = [
      '/api/v1/companies/coordinates/map-pins/',
      '/api/v1/companies/coordinates/map-pins',
      '/api/v1/companies/admin-list'
    ];

    for (const ep of endpointsToTry) {
      try {
        const pinRes = await api.get(ep, { params: { limit: 1000 } });
        if (Array.isArray(pinRes.data) && pinRes.data.length > 0) {
          pinData = pinRes.data;
          break;
        }
      } catch (err) {
        // Continue trying next endpoint or local backend fallback
      }
    }

    // Fallback: If primary API failed (e.g. 404 on prod URL), try local backend server
    if (pinData.length === 0) {
      const localBackends = [
        'http://127.0.0.1:5001',
        'http://localhost:5001',
        'http://10.0.2.2:5001',
        'http://172.20.10.6:5001'
      ];
      for (const lb of localBackends) {
        try {
          const res = await axios.get(`${lb}/api/v1/companies/coordinates/map-pins/?limit=1000`, { timeout: 3000 });
          if (Array.isArray(res.data) && res.data.length > 0) {
            pinData = res.data;
            break;
          }
        } catch {
          // ignore local fallback error
        }
      }
    }

    if (pinData.length > 0) {
      companyFetched = true;
      const companyCustomers: Customer[] = pinData
        .filter((cp: any) => {
          const lat = parseFloat(cp.lat);
          const lng = parseFloat(cp.lon || cp.lng);
          return !isNaN(lat) && !isNaN(lng) && lat !== 0 && lng !== 0;
        })
        .map((cp: any) => {
          const lat = parseFloat(cp.lat);
          const lng = parseFloat(cp.lon || cp.lng);
          return {
            id: `company_${cp.id}`,
            name: cp.unvan || cp.company_name || 'Firma',
            company: cp.unvan || cp.company_name || 'Firma',
            email: '',
            phone: '',
            status: 'active',
            salesRepId: '1',
            createdAt: cp.updated_at || new Date().toISOString(),
            updatedAt: cp.updated_at || new Date().toISOString(),
            address: {
              street: cp.address || `${cp.district || ''} ${cp.city || ''}`.trim() || 'Adres',
              city: cp.city || 'İstanbul',
              state: cp.district || '',
              zipCode: '',
              country: 'Türkiye',
              coordinates: { lat, lng }
            },
            latitude: lat,
            longitude: lng,
          };
        });

      const existingIds = new Set(mappedCustomers.map(c => c.id));
      for (const cc of companyCustomers) {
        if (!existingIds.has(cc.id)) {
          mappedCustomers.push(cc);
        }
      }
    }

    // 3. If no company pins were returned from live API or local fallback, merge fallback sample companies
    if (!companyFetched) {
      const existingIds = new Set(mappedCustomers.map(c => c.id));
      for (const fc of FALLBACK_GEOLOCATION_COMPANIES) {
        if (!existingIds.has(fc.id)) {
          mappedCustomers.push(fc);
        }
      }
    }

    return mappedCustomers;
  },

  getCustomerById: async (id: string): Promise<Customer | null> => {
    try {
      const c = await customerAPI.getById(id);
      if (c) {
        return {
          id: String(c.id),
          name: c.company_name || c.title || c.name || 'Müşteri',
          company: c.company_name || c.title || 'B2B Müşteri',
          email: c.contact_email || c.email || '',
          phone: c.phone || '',
          status: c.status || 'active',
          salesRepId: c.sales_rep_id || c.salesRepId || '1',
          createdAt: c.created_at || new Date().toISOString(),
          updatedAt: c.updated_at || new Date().toISOString(),
          address: typeof c.address === 'string' ? {
            street: c.address,
            city: 'İstanbul',
            state: '',
            zipCode: '',
            country: 'Türkiye',
            coordinates: {
              lat: c.latitude || 41.0082,
              lng: c.longitude || 28.9784,
            }
          } : c.address || {
            street: 'Adres belirtilmedi',
            city: 'İstanbul',
            state: '',
            zipCode: '',
            country: 'Türkiye',
            coordinates: { lat: c.latitude || 41.0082, lng: c.longitude || 28.9784 }
          },
          latitude: c.latitude || 41.0082,
          longitude: c.longitude || 28.9784,
        };
      }
    } catch (error) {
      console.warn('getCustomerById API error:', error);
    }

    // Check in fallback list if not found
    const fallbackMatch = FALLBACK_GEOLOCATION_COMPANIES.find(fc => fc.id === id);
    return fallbackMatch || null;
  },

  createCustomer: async (customerData: Omit<Customer, 'id'>) => {
    try {
      const payload = {
        title: customerData.name || customerData.company,
        company_name: customerData.company,
        contact_email: customerData.email,
        phone: customerData.phone,
        address: customerData.address?.street || '',
        tax_number: String(Math.floor(1000000000 + Math.random() * 9000000000)),
        status: customerData.status || 'active',
        latitude: customerData.address?.coordinates?.lat || 41.0082,
        longitude: customerData.address?.coordinates?.lng || 28.9784,
      };
      const created = await customerAPI.create(payload);
      return created;
    } catch (error) {
      console.error('Error in customerService.createCustomer:', error);
      throw error;
    }
  },

  updateCustomer: async (id: string, customerData: Partial<Customer>) => {
    try {
      const updated = await customerAPI.update(id, customerData);
      return updated;
    } catch (error) {
      console.error('Error in customerService.updateCustomer:', error);
      throw error;
    }
  },

  deleteCustomer: async (id: string) => {
    try {
      await customerAPI.delete(id);
    } catch (error) {
      console.error('Error in customerService.deleteCustomer:', error);
      throw error;
    }
  },

  updateCustomerLocation: async (id: string, location: { latitude: number; longitude: number }) => {
    try {
      const updated = await customerAPI.update(id, {
        latitude: location.latitude,
        longitude: location.longitude,
      });
      return updated;
    } catch (error) {
      console.error('Error in customerService.updateCustomerLocation:', error);
      throw error;
    }
  },
};

export default customerService;
