import { z } from 'zod';

// Schema for PostGIS point object that Supabase returns
const pointSchema = z.object({
  x: z.number(),
  y: z.number(),
});

// Bu şema, hem istemci hem de sunucu tarafında veri bütünlüğünü sağlamak için kullanılır.
export const companySchema = z.object({
  id: z.string().uuid().optional(), // Veritabanından gelince UUID olur
  sicil_no: z.string().min(1, 'Sicil numarası boş olamaz.'),
  firma_unvani: z.string().nullable(),
  adres: z.string().nullable().optional(),
  sicil_mudurluk: z.string().min(1, 'Sicil müdürlüğü boş olamaz.').optional(),
  created_at: z.string().datetime().optional(),
  last_scraped_at: z.string().datetime().nullable().optional(),
  koordinat: pointSchema.nullable().optional(), // Koordinat alanı eklendi
});

// Zod şemasından TypeScript tipini oluşturur.
export type Company = z.infer<typeof companySchema>;

// Type specifically for the map display component
export interface CompanyWithLocation {
  id: string;
  firma_unvani: string | null;
  koordinat: { x: number; y: number };
}
