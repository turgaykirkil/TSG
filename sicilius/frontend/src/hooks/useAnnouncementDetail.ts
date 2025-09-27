import { useQuery } from '@tanstack/react-query';
import { API_BASE_URL } from '@/config/constants';

export interface AnnouncementDetailPayload {
  announcement: any | null;
  original_text: string | null;
}

export const useAnnouncementDetail = (announcementId?: string, enabled: boolean = false) => {
  return useQuery<AnnouncementDetailPayload, Error>({
    queryKey: ['announcement-detail', announcementId],
    queryFn: async () => {
      const id = (announcementId || '').trim();
      if (!id) throw new Error('Geçersiz ilan kimliği');
      const url = `${API_BASE_URL}/api/v1/search/announcement-detail?announcement_id=${encodeURIComponent(id)}`;
      const res = await fetch(url, { credentials: 'include' });
      if (!res.ok) {
        let message = 'İlan detayı getirilemedi';
        try {
          const data = await res.json();
          message = data?.detail || message;
        } catch {}
        const err: any = new Error(message);
        (err as any).status = res.status;
        throw err;
      }
      return res.json();
    },
    enabled: enabled && !!announcementId,
    staleTime: 60_000,
  });
};
