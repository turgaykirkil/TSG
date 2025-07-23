'use client';

import BatchProcessor from './components/batch-processor';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import api from '@/lib/axios';

// Define the type for an announcement
interface Announcement {
  id: string;
  title: string;
  publication_date: string;
  announcement_type: string;
  // Add other relevant fields from your model
  ocr_result?: { status: string }; // Optional ocr_result
}

const OcrManagementPage = () => {
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { session } = useAuth();

  useEffect(() => {
    const fetchAnnouncements = async () => {
      if (!session) return;
      try {
        setLoading(true);
        // Assuming an endpoint /api/v1/announcements exists
        // We might need to create this endpoint if it doesn't exist
                const response = await api.get('/api/v1/announcements');
        // Filter announcements that need OCR (e.g., no ocr_result or status is 'pending')
        const pendingAnnouncements = response.data.filter(
          (ann: Announcement) => !ann.ocr_result || ann.ocr_result.status === 'pending'
        );
        setAnnouncements(pendingAnnouncements);
      } catch (err) {
        setError('İlanlar yüklenirken bir hata oluştu.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnnouncements();
  }, [session]);

  if (loading) {
    return <div>Yükleniyor...</div>;
  }

  if (error) {
    return <div className="text-red-500">{error}</div>;
  }

  return (
    <div className="container mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">OCR Yönetim Paneli</h1>
      <div className="mb-8">
        <BatchProcessor />
      </div>
      
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">İşlem Bekleyen İlanlar</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Unvan</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Yayın Tarihi</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">İlan Türü</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Durum</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {announcements.length > 0 ? (
                announcements.map((ann) => (
                  <tr key={ann.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{ann.title}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{new Date(ann.publication_date).toLocaleDateString()}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{ann.announcement_type}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                        Bekliyor
                      </span>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={4} className="px-6 py-4 text-center text-sm text-gray-500">İşlem bekleyen ilan bulunamadı.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        <div className="mt-4">
          <button 
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400"
            disabled={announcements.length === 0}
          >
            Tüm Bekleyenler İçin OCR Başlat
          </button>
        </div>
      </div>
    </div>
  );
};

export default OcrManagementPage;
