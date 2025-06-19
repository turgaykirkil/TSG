# TSG Platform Değişiklik Kaydı

## [0.1.4] - 2025-06-15

### Eklendi
- `zod` bağımlılığı `package.json` dependencies listesine eklendi.
- `src/lib/types/company.types.ts` oluşturuldu. `CompanyData` şeması buraya taşındı. Gelecek refaktörlerde tüm type importları buradan yapılacak.

### Değiştirildi
- ---

## [0.1.3] - 2025-06-15

### Eklendi
- `/dashboard`, `/profile`, `/upload` kullanıcı sayfaları oluşturuldu.
- `src/middleware.ts` korumalı rotalara `/upload`, `/history`, `/admin/**` eklendi.

### Değiştirildi
- Kullanıcı arayüzü için gradyen temalı butonlar ve Container yapısı.  
- Yeni sayfalar auth koruması ile yönlendirme içeriyor.

## [0.1.2] - 2025-06-15

### Eklendi
- `.env.local.example` dosyası oluşturuldu, gerekli Supabase ve site URL değişkenleri belgelendi.

### Değiştirildi
- `src/lib/auth.ts` dosyası tek `supabaseClient` kullanacak şekilde güncellendi ve TypeScript lint hataları giderildi.
- `src/app/api/auth/register/route.ts` artık ortak `supabase-admin` istemcisini kullanıyor.

## [0.1.1] - 2025-06-15

### Eklendi
- `src/lib/supabaseClient.ts` dosyası eklendi. Uygulamanın tek Supabase istemcisi olarak kullanılacak.

### Değiştirildi
- `src/lib/supabase.ts` dosyasından hard-coded Supabase URL ve anon key kaldırıldı, yeni istemciyi kullanacak şekilde refaktör edildi.



## [0.1.0] - 2025-06-05

### Eklendi
- Dosya yükleme API entegrasyonu (PDF/Excel)
- Admin panel dosya yükleme bileşeni
- Backend log canlı izleme desteği
