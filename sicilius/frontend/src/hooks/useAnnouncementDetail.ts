import { useQuery } from '@tanstack/react-query';

export interface AnnouncementDetailPayload {
  announcement: any | null;
  original_text: string | null;
}

const isUuid = (s?: string) => {
  const v = (s || '').trim();
  if (!v) return false;
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(v);
};

export const useAnnouncementDetail = (announcementId?: string, ocrId?: number, enabled: boolean = false) => {
  return useQuery<AnnouncementDetailPayload, Error>({
    queryKey: ['announcement-detail', announcementId, ocrId],
    queryFn: async () => {
      const id = (announcementId || '').trim();
      if (!id) throw new Error('Geçersiz ilan kimliği');
      if (!isUuid(id)) throw new Error('Bu ilan için detay metni yok (UUID değil)');

      // Build URL with optional ocr_id parameter
      let url = `/api/v1/search/announcement-detail?announcement_id=${encodeURIComponent(id)}`;
      if (ocrId != null) {
        url += `&ocr_id=${ocrId}`;
      }

      const res = await fetch(url, { credentials: 'include' });
      if (!res.ok) {
        let message = 'İlan detayı getirilemedi';
        try {
          const data = await res.json();
          message = data?.detail || message;
        } catch { }
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
