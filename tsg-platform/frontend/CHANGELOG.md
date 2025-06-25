# Sicilius Platform Changelog

## [0.6.0] - 2025-06-25

### Changed
- **Rebranding:** The entire frontend application has been rebranded from "TSG Platform" to "Sicilius". This includes all user-facing text, contact information, metadata, and internal identifiers to align with the new brand identity.
- Updated `README.md`, `package.json`, and other configuration files to reflect the "Sicilius" name.

## 0.5.1 - 2024-07-28

### Eklendi (Added)

- **[Coğrafi Kodlama Servisi]** Adresleri koordinata çevirmek için yedekli bir mekanizmaya sahip yeni bir coğrafi kodlama servisi (`src/lib/geocode.ts`) eklendi. Sistem, önce ücretsiz Nominatim servisini dener, başarısız olursa veya sonuç güvenirliği düşükse otomatik olarak LocationIQ servisine geçer. Bu, adres bulma isabet oranını ve sistemin genel güvenilirliğini artırır.

### Değiştirildi (Changed)

- **[Yönetici Paneli]** Koordinat paneli (`coordinates-dashboard.tsx`), artık yeni ve merkezi coğrafi kodlama servisini kullanacak şekilde tamamen yeniden düzenlendi.
- **[Kullanıcı Arayüzü]** Uygulama genelindeki yükleme ekranı (`loader.tsx`), daha büyük bir logo içerecek ve gereksiz metinleri kaldıracak şekilde yeniden tasarlandı. Bu, daha temiz ve markaya odaklı bir kullanıcı deneyimi sunar.


## 0.5.0 - 2024-07-28

### Eklendi (Added)

- **[Dosya Yükleme]** Platform artık `.pdf` uzantılı dosyaları kabul ediyor. Kullanıcılar, PDF dosyalarındaki tabloları ayrıştırabilir, istedikleri tabloyu seçebilir ve verileri sisteme yükleyebilir.
- **[Backend Entegrasyonu]** PDF dosyalarını işlemek için Python (FastAPI) tabanlı yeni bir backend servisiyle entegrasyon sağlandı.
- **[Kullanıcı Arayüzü]** PDF'ten birden fazla tablo ayrıştırıldığında, kullanıcıya hangi tabloyla devam edeceğini soran bir seçim arayüzü (`PdfTableSelector`) eklendi.

### Yeniden Yapılandırıldı (Refactored)

- **[Dosya İşleme Mimarisi]** `useFileProcessor` hook'u, hem Excel hem de PDF dosyalarını yönetebilen merkezi bir "orkestratör" olarak yeniden tasarlandı. Dosya türüne göre doğru işleme mantığını (Excel veya PDF) dinamik olarak çalıştırır.
- **[Veri Tipleri]** `lib/file-utils.ts` içindeki `ExcelSheetResult` tipi, hem Excel hem de PDF'ten gelen verilerle tutarlı olacak şekilde `headers` (başlıklar) alanını içerecek şekilde güncellendi. Bu, kod genelinde veri tutarlılığını artırdı.
- **[Bileşen Mimarisi]** `file-upload-section.tsx` bileşeni, yeni dosya işleme akışını (yükleme, PDF tablo seçimi, veri eşleştirme) destekleyecek şekilde baştan sona yeniden düzenlendi.

### Düzeltildi (Fixed)

- **[Tip Güvenliği]** `file-upload-section.tsx` içinde `useColumnMapper` hook'una geçirilen veri için açık tip tanımı eklenerek TypeScript'in yanlış tip (`unknown[][]`) çıkarma sorunu giderildi. Bu, veri eşleştirme mantığının kararlılığını artırır.
- **[Bileşen Uyumu]** `file-upload-section.tsx` içindeki `ColumnTypeModal` bileşenine yanlış aktarılan `props` (`header` yerine `columnName`) düzeltilerek bileşenler arası uyumluluk sağlandı.
- **[Veri Bütünlüğü]** PDF ayrıştırıcıdan gelen verilerin, `useColumnMapper` hook'u tarafından beklenen `(string | number | null)[][]` tipine uygun olması için güvenli bir tip dönüşümü eklendi.
- **[Genel Kararlılık]** `file-upload-section.tsx` bileşenindeki tüm sözdizimi ve lint hataları giderilerek bileşenin tamamen çalışır ve kararlı bir duruma getirilmesi sağlandı.
- **[Excel İşleme Hatası]** `useFileProcessor.ts` hook'undaki hatalı veri işleme mantığı düzeltildi. Excel dosyaları işlenirken var olmayan bir `data` alanı yerine doğru olan `sheets` alanı kullanılarak, "Cannot read properties of undefined (reading 'map')" hatası giderildi ve Excel yükleme işlevselliği yeniden kararlı hale getirildi.
- **[Kullanıcı Arayüzü]** Veri eşleştirme tablosunda yatay kaydırma (horizontal scroll) etkinleştirildi. Geniş tabloların tüm sütunlarının görüntülenebilmesi için `ScrollArea` bileşeni, `overflow-auto` özelliğine sahip standart bir `div` ile değiştirildi.
- **[Veri Yükleme Hatası]** "Firmaları Yükle" butonuna tıklandığında verilerin Supabase'e gönderilememesi sorunu çözüldü. Yüklenen verilerdeki alan adları (`unvan` -> `firma_unvani` vb.) Supabase şemasıyla doğru şekilde eşleştirildi.
- **[Kullanıcı Arayüzü]** Zorunlu `sicil_mudurluk` alanı için arayüze bir seçim kutusu (Select) eklendi. Bu sayede veriler yüklenmeden önce ilgili müdürlüğün seçilmesi sağlandı ve sabit kodlanmış değer kaldırılarak veri bütünlüğü artırıldı.

## 0.4.1 - 2024-07-27

### Düzeltildi (Fixed)

- **[Kimlik Doğrulama]** `DashboardLayout.tsx`: Kimlik doğrulama mantığı, `next-auth`'ın `useSession` hook'u kullanılarak tamamen yeniden yazıldı. Eski ve hataya açık bağımlılıklar kaldırılarak bileşen kararlı hale getirildi ve korumalı sayfalardaki yönlendirme sorunları çözüldü.

### Değiştirildi (Changed)

- **[Performans]** Proje genelindeki (`Header.tsx`, `about/page.tsx`, `home/page.tsx`) standart `<img>` etiketleri, Next.js'in optimize edilmiş `<Image>` bileşeni ile değiştirildi. Bu değişiklik, sayfa yükleme performansını (LCP) iyileştirir ve üretim derlemesindeki uyarıları ortadan kaldırır.


## 0.4.0 - 2024-07-27

### Eklendi (Added)

- **[Kullanıcı Arayüzü]** `(app)/layout.tsx` & `ui/loader.tsx`: Kullanıcı deneyimini iyileştirmek amacıyla, dashboard'daki sayfa geçişleri sırasında Sicilius logosuyla birlikte animasyonlu bir yüklenme göstergesi (loader) eklendi.
- **[Paketler]** Veri görselleştirmesi için `recharts` kütüphanesi projeye eklendi.

### Değiştirildi (Changed)

- **[Arama İşlevselliği]** `AppHeader.tsx` & `(app)/dashboard/search/page.tsx`: Header'daki arama çubuğu aktif hale getirildi. Artık kullanıcı tarafından girilen arama terimi, doğrudan `/dashboard/search` sayfasına yönlendiriliyor. Arama sayfası, URL'deki sorgu parametresini (`?q=`) ana veri kaynağı olarak kullanacak şekilde yeniden düzenlendi, böylece hem header'dan hem de sayfa içinden yapılan aramalar tamamen senkronize ve tutarlı çalışıyor.
- **[Kullanıcı Arayüzü]** `dashboard/page.tsx`: Genel bakış (dashboard) sayfası, Apple estetiğinden ilham alan, modern ve etkileşimli bir tasarımla tamamen yenilendi. Yeni arayüzde `recharts` ile oluşturulmuş bir büyüme grafiği, `framer-motion` ile akıcı animasyonlar ve `lucide-react` ikonları ile zenginleştirilmiş istatistik kartları bulunmaktadır.

### Değiştirildi (Changed)

- **[Kullanıcı Arayüzü]** `AppSidebar.tsx` & `AppHeader.tsx`: Uygulama başlığı ve kenar çubuğu, modern bir kullanıcı deneyimi sunmak üzere tamamen yeniden tasarlandı. Dağınık kullanıcı menüsü ve bildirim ikonları, tüm işlemleri birleştiren şık bir avatar menüsü ile değiştirildi. Kenar çubuğu sadeleştirildi ve marka kimliği 'Sicilius' olarak güncellendi.

### Düzeltildi (Fixed)

- **[Kullanıcı Arayüzü]** `dashboard/page.tsx`: Dashboard sayfası, küçük ekranlarda daha iyi bir kullanıcı deneyimi sunmak için mobil uyumlu hale getirildi. Kartlar ve diğer bileşenler artık mobil cihazlarda dikey olarak düzgün bir şekilde sıralanıyor.
- **[Kullanıcı Arayüzü]** `dashboard/page.tsx`: İstatistik kartlarındaki sayıların mobil cihazlarda taşması ve metinlerin sıkışması sorunları, duyarlı font boyutları ve artırılmış satır yüksekliği ile giderildi.
- **[Kullanıcı Arayüzü]** `AppSidebar.tsx`: Kenar çubuğundaki kırık logo sorunu düzeltildi ve linkin üzerindeki gereksiz ipucu yazısı (tooltip) kaldırıldı.


## 0.3.1 - 2024-07-27

### Düzeltildi (Fixed)

- **[Kimlik Doğrulama]** `user-auth-form.tsx`: Başarılı giriş işleminden sonra kullanıcıların otomatik olarak dashboard'a yönlendirilmemesi sorunu giderildi. `useRouter` hook'u eklenerek `signIn` başarılı olduğunda manuel yönlendirme sağlandı.

## 0.3.0 - 2024-07-27

### Eklendi (Added)

- **[Kullanıcı Arayüzü]** `icons.tsx`: Sicilius markası için teknoloji ve bağlantıyı simgeleyen, iç içe geçmiş iki 'S' harfinden oluşan modern ve minimalist yeni bir SVG logo tasarlandı ve uygulamaya entegre edildi.

### Değiştirildi (Changed)

- **[Kullanıcı Arayüzü]** `login` ve `register` sayfaları, karanlık temadan tamamen arındırılarak açık tonlarda, ferah ve modern bir gradyan arka planla güncellendi. Metin, ikon ve kart renkleri yeni aydınlık temayla tam uyumlu hale getirildi.
- **[Kullanıcı Arayüzü]** `(public)/layout.tsx`: Kimlik doğrulama sayfalarındaki `PublicHeader` ve `PublicFooter` bileşenleri kaldırılarak kullanıcıların dikkatini dağıtacak unsurlar ortadan kaldırıldı ve tamamen forma odaklanmaları sağlandı.

### Kaldırıldı (Removed)

- **[Kullanıcı Arayüzü]** `user-auth-form.tsx`: Kullanıcı formundaki "Veya devam et" ayıracı ve metni kaldırılarak daha sade ve akıcı bir kullanıcı deneyimi sunuldu.


## [0.1.5] - 2024-07-27

### Yeniden Yapılandırıldı

- `file-upload-section.tsx` bileşeni, hataları gidermek ve kararlılığı artırmak için modern React hook'ları (`useExcelParser`, `useColumnMapper`, `useCompanyUploader`) kullanarak baştan sona yeniden yazıldı.
- Dosya yükleme süreci (sürükle-bırak, ayrıştırma, sütun eşleştirme, veri doğrulama ve yükleme) daha modüler ve yönetilebilir hale getirildi.
- Kullanıcı arayüzü ve kullanıcı deneyimi, işlem adımlarını daha net gösterecek şekilde iyileştirildi.
- Hata yönetimi, `sonner` bildirimleri ile daha anlaşılır hale getirildi.

### Düzeltildi (Fixed)

- **file-upload-section.tsx:** Bileşen, modern ve özel hook'lar (`useExcelParser`, `useColumnMapper`, `useCompanyUploader`) kullanılarak tamamen yeniden yazıldı. Bu değişiklik, bileşeni daha modüler, okunabilir ve bakımı kolay hale getirdi.
- **UX Geliştirmeleri:** Dosya sürükleme ve bırakma alanında, veri işlemede ve yükleme sırasında daha iyi kullanıcı geri bildirimi sağlandı.
- **Hata Yönetimi:** Dosya türü, boyutu ve içeriği için daha sağlam hata yönetimi eklendi.
- **Kod Kalitesi:** Tüm `lint` hataları giderildi ve TypeScript tür güvenliği artırıldı.

## [0.1.6] - 2024-07-26

### Düzeltildi (Fixed)
- **file-upload-section.tsx:** Hook entegrasyonu ve state yönetimi tamamen düzeltildi. Bileşen, `useExcelParser`, `useColumnMapper` ve `useCompanyUploader` hook'larının doğru arayüzlerine, `ColumnTypeModal` bileşeninin doğru proplarına ve `MUDURLUKLER` sabitinin doğru veri yapısına (`{value, label}`) ve import yoluna göre yeniden yapılandırıldı. Bu değişiklik, önceki sürümdeki tüm `lint` ve tür hatalarını gidererek dosya yükleme işlevini tamamen çalışır hale getirir.

## [0.1.4] - 2024-07-26

### Yeniden Yapılandırıldı (Refactored)

- **[Kimlik Doğrulama]** `login` ve `register` sayfaları, `src/components/auth/user-auth-form.tsx` altında merkezi bir kimlik doğrulama bileşeni kullanacak şekilde tamamen yeniden yazıldı. Bu değişiklik, kod tekrarını azaltır ve her iki sayfada da tutarlı bir kullanıcı deneyimi sağlar.
- **[Kimlik Doğrulama]** Form yönetimi için `react-hook-form` ve şema tabanlı doğrulama için `zod` entegre edildi.

## 0.2.0 - 2024-07-26

### Yeniden Yapılandırıldı (Refactored)

- **[Kimlik Doğrulama]** `login` ve `register` sayfaları, `src/components/auth/user-auth-form.tsx` altında merkezi bir kimlik doğrulama bileşeni kullanacak şekilde tamamen yeniden yazıldı. Bu değişiklik, kod tekrarını azaltır ve her iki sayfada da tutarlı bir kullanıcı deneyimi sağlar.
- **[Kimlik Doğrulama]** Form yönetimi için `react-hook-form` ve şema tabanlı doğrulama için `zod` entegre edildi.

### Eklendi (Added)

- **[Kullanıcı Arayüzü]** Uygulama genelinde tutarlı bildirimler sağlamak için Shadcn UI tabanlı yeni bir `toast` bildirim sistemi (`src/components/ui/toast.tsx`, `toaster.tsx`, `use-toast.ts`) eklendi. Ana layout'a (`src/app/layout.tsx`) `Toaster` bileşeni entegre edildi.
- **[Paketler]** Projeye `react-hook-form`, `@hookform/resolvers` ve `@radix-ui/react-toast` bağımlılıkları eklendi.

### Düzeltildi (Fixed)

- **[Hata Giderme]** `login` ve `register` sayfalarındaki `framer-motion` animasyonlarında TypeScript tip uyumsuzluğuna neden olan `ease` özelliğiyle ilgili hatalar giderildi.
- **[Hata Giderme]** Kimlik doğrulama formunda eksik olan veya yanlış yollara sahip olan `import` hataları düzeltildi.

## 0.1.6 - 2025-06-22

### Eklendi

- **[Kullanıcı Arayüzü]** `src/app/page.tsx`: Ana sayfaya, Apple'ın web sitesinden ilham alan modern ve akıcı `framer-motion` animasyonları eklendi. Başlıklar, metinler ve kartlar artık sayfa yüklendiğinde ve kaydırıldığında estetik bir şekilde beliriyor.
- **[Kullanıcı Arayüzü]** `src/app/page.tsx`: Ana karşılama ekranına kullanıcıların platforma kolayca erişebilmesi için bir "Giriş Yap" butonu eklendi.


## 0.1.5 - 2025-06-21

### Added
- Modern gradient theme with Sicilius branding
- Updated all UI components with Sicilius logo and colors
- New color palette for modern look

### Changed
- Removed settings and profile buttons from admin page
- Updated CSS configuration to fix Tailwind warnings
- Updated all page titles to "Sicilius"
- Updated metadata for SEO with Sicilius brand
- Replaced TSG Platform branding with Sicilius across all dashboard pages
- Updated dashboard page titles and descriptions
- Updated admin page header and card titles
- Updated search page error messages and loading states
- Removed navigation from login and register pages
- Updated login/register page text to Sicilius branding
- Updated homepage text content to Sicilius branding

### Fixed
- Tailwind CSS configuration warnings
- CSS reset and base styles
- UI consistency across all pages

## 0.1.4 - 2025-06-20

### Added
- Zod validation for Excel parsing
- Excel preview table component
- Worker-based Excel processing
- Batch add companies mutation

### Changed
- Updated file upload section architecture
- Improved error handling
- Enhanced type safety

### Fixed
- React query mutation issues
- File size validation
- Worker initialization

## 0.1.3 - 2025-06-19

### Added
- Supabase client unification
- Environment-based session management
- Role-based auth middleware
- Modern UI components

### Changed
- Updated auth flow
- Improved error handling
- Enhanced session management

### Fixed
- Auth redirection issues
- Session persistence
- Role claim handling
