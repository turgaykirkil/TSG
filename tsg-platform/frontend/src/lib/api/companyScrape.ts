import axios from 'axios';
import type { CompanyScrape, CompanyScrapeCreate, CompanyScrapeStatus } from '@/types/companyScrape';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001/api/v1';

if (!process.env.NEXT_PUBLIC_API_URL) {
  console.warn('NEXT_PUBLIC_API_URL environment variable is not set. Using default: http://localhost:5001/api/v1');
}

// Axios instance oluştur
const api = axios.create({
  baseURL: API_URL.endsWith('/') ? API_URL.slice(0, -1) : API_URL,
  withCredentials: false, // CORS için gerekirse true yapılabilir
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// Hata yönetimi
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Yeni şirket ekle veya güncelle
export const createOrUpdateCompany = async (data: CompanyScrapeCreate): Promise<CompanyScrape> => {
  try {
    const response = await api.post('/company-scrapes', data);
    return response.data;
  } catch (error) {
    console.error('Şirket kaydı oluşturulurken hata oluştu:', error);
    throw error;
  }
};

// Toplu şirket ekle
export const batchCreateCompanies = async (companies: CompanyScrapeCreate[]): Promise<CompanyScrape[]> => {
  try {
    const response = await api.post('/company-scrapes/batch', companies);
    return response.data;
  } catch (error) {
    console.error('Toplu şirket eklenirken hata oluştu:', error);
    throw error;
  }
};

// Scraping yapılması gereken şirketleri getir
export const getCompaniesNeedingScraping = async (): Promise<CompanyScrape[]> => {
  try {
    const response = await api.get('/company-scrapes/needs-scraping');
    return response.data;
  } catch (error) {
    console.error('Scraping yapılacak şirketler getirilirken hata oluştu:', error);
    throw error;
  }
};

// Tüm şirketleri getir
export const getAllCompanies = async (): Promise<CompanyScrape[]> => {
  try {
    const response = await api.get('/company-scrapes');
    return response.data;
  } catch (error) {
    console.error('Şirketler getirilirken hata oluştu:', error);
    throw error;
  }
};

// Scraping durumuna göre filtreleme
export const getCompaniesByStatus = async (status: CompanyScrapeStatus): Promise<CompanyScrape[]> => {
  try {
    const response = await api.get(`/company-scrapes?status=${status}`);
    return response.data;
  } catch (error) {
    console.error('Şirketler filtrelenirken hata oluştu:', error);
    throw error;
  }
};

// Toplu scraping başlat
export const startBatchScraping = async (companyIds: number[]): Promise<void> => {
  try {
    await api.post('/company-scrapes/start-batch', { companyIds });
  } catch (error) {
    console.error('Toplu scraping başlatılırken hata oluştu:', error);
    throw error;
  }
};

// Şirketi "scraped" olarak işaretle
export const markCompanyAsScraped = async (companyId: number): Promise<CompanyScrape> => {
  try {
    const response = await api.patch(`/company-scrapes/${companyId}/mark-scraped`);
    return response.data;
  } catch (error) {
    console.error('Şirket işaretlenirken hata oluştu:', error);
    throw error;
  }
};
