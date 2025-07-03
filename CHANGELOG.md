# Sicilius Platform Changelog

## [1.0.0] - 2023-10-15
### Added
- Initial release of Sicilius Platform

## [Unreleased]

## [0.1.8] - 2025-06-29

### Added
- **Scraping Page**: Created the initial page for the data scraping functionality at `/dashboard/scraping`.

### Fixed
- **Application Crash**: Resolved two critical issues causing the application to crash during compilation and runtime.
  - Fixed a syntax error (extra closing brace) in `src/app/page.tsx`.
  - Added the required `'use client';` directive to `src/layouts/DashboardLayout.tsx` to enable the use of client-side React hooks.

## [0.1.7] - 2025-06-29

### Added
- **UI/UX Overhaul**: Implemented a complete visual rebranding to "Sicilius" with a new "Minimalist Power" design philosophy.
  - Created a reusable `AuthLayout` component to ensure a consistent look and feel across authentication pages.
  - Redesigned the **Login Page** with a modern, two-column layout featuring the brand identity.
  - Redesigned the **Register Page** to match the new login page design for a seamless user experience.
  - Revamped the **Homepage** into a professional landing page that clearly communicates the platform's value proposition and aligns with the new brand identity.

### Changed
- **Branding**: Updated the color palette and typography across the application to reflect the new "Sicilius" brand. The primary color is now Night Blue (`#1e3a8a`).

### Fixed
- Fixed a minor syntax error on the new homepage component.

### Added
- **Dashboard UI:** Renamed statistics cards and updated their colors to match the Sicilius brand palette (blue, green, purple, red) for a more vibrant and consistent user interface.
- Integrated an interactive map view into the dashboard search page using a tabbed interface.
- Dynamically load the map component (`react-leaflet`) for better performance.

### Changed
- Centralized company-related TypeScript types into `src/types/company.types.ts`.
- Updated `useCompanySearch` hook to fetch company coordinates from the database.

### Fixed
- Resolved TypeScript errors related to missing `koordinat` property on company data by updating Zod schemas and type definitions.
- Corrected type imports on the search page to use the new centralized types.
- **[Arama Sayfası]** Harita sekmesindeki hatalı görünüm düzeltildi. Harita bileşeninin kapsayıcısına sabit bir yükseklik ve stil verilerek haritanın doğru şekilde render edilmesi sağlandı.
- **[Admin Paneli]** `CoordinatesDashboard` bileşeni, tüm lint ve tür hatalarını gidermek ve kararlılığı artırmak için tamamen yeniden düzenlendi.
  - `handleFetchCoordinates` ve `handleResolveConflicts` fonksiyonlarındaki `any` tipleri kaldırılarak tam tür güvenliği sağlandı.
  - `for...of` döngüsü, projenin `es5` hedefiyle uyumluluk için standart bir `for` döngüsüyle değiştirilerek `downlevelIteration` hatası giderildi.
  - Supabase RPC çağrılarındaki hatalı tip kullanımı düzeltildi.
- **[Performans]** `handleFetchCoordinates` fonksiyonu, aynı adrese sahip şirketleri gruplayarak her benzersiz adres için yalnızca bir coğrafi kodlama API'si çağrısı yapacak şekilde optimize edildi. Bu, API çağrı sayısını önemli ölçüde azaltır ve toplu güncelleme performansını artırır.
- **[Arama ve Harita Performansı]** Arama sayfasındaki `MapDisplay` bileşeni, `React.memo` kullanılarak optimize edildi ve gereksiz yeniden render işlemleri önlendi. `useCompanySearch` hook'u, daha iyi tip güvenliği için yeniden düzenlendi.

### Removed
- Deleted the obsolete `/map` route and its associated components and pages.

## [0.1.6] - 2024-07-29

### Fixed
- **CRITICAL**: Completely overhauled the backend PDF parsing service (`/api/v1/parse-pdf`). The new, simplified logic robustly handles multi-page tables by:
  1.  **Isolating the header**: The header is now identified exclusively on the first page, preventing data rows from being mistaken for headers.
  2.  **Ensuring data integrity**: All non-header and non-empty rows from all pages are now reliably extracted, permanently fixing the critical data loss issue where the row count was incorrect.
  3.  **Stabilizing output**: The parser now consistently returns a single, merged JSON object with all table data, eliminating previous errors of missing headers or incomplete data.
- **Login Redirection**: Fixed a race condition in the login form where the user was not automatically redirected after a successful login. Replaced client-side routing with a full page reload (`window.location.href`) to ensure the session is correctly updated and recognized by the middleware before the redirect occurs.

### Added
- **Multi-Sheet Excel Upload:** The file upload component now fully supports multi-sheet Excel files.
  - Each sheet is displayed in a separate tab, allowing for independent column mapping and data preview.
  - Implemented a modular `SheetMappingInterface` component to manage the state of each sheet independently, preserving user selections when switching tabs.
- **Horizontal Scrolling for Data Preview:** Added horizontal scrolling to the data preview table to ensure all columns are visible, even in wide datasets.

### Changed
- **Refactored `FileUploadSection`:** The main file upload component was significantly refactored for better state management, modularity, and maintainability.

### Fixed
- **Linting and Compilation Errors:** Resolved numerous compilation errors related to incorrect hook usage, missing imports, and state management conflicts during the refactoring process.
- **Data Misalignment:** Fixed issues where blank header cells in Excel files could cause data misalignment and React key errors.
- **Harita Bileşenindeki Çökme Sorunu:** Harita bileşenindeki çökme sorununu çözmek için yapılan tüm adımları içeren detaylı bir bölüm eklenmiştir.
  - Adres dizeleri LocationIQ API'sine gönderilmeden önce normalleştirilerek 404 hataları azaltıldı.
  - Harita bileşenindeki "render is not a function" ve context çökme hataları giderildi. Bu kapsamda:
    - Bileşenin sunucu tarafında render edilmesi (SSR) `ssr: false` seçeneği ile engellendi.
    - Hatalı `CompanyWithLocation` tip importu düzeltildi.
    - Leaflet ikonlarının `require()` yerine modern `import` ile yüklenmesi sağlandı.
    - `MapContainer` alt bileşenleri, context hatalarını önlemek için bir Fragment içine alındı.
    - Haritanın sadece istemci tarafında yüklendikten sonra render edilmesi için `isMounted` kontrolü eklendi.
- **Koordinat Ayrıştırma Düzeltmesi (WKB Desteği):** Veritabanından WKB (Well-Known Binary) formatında gelen coğrafi verilerin `wkx` kütüphanesi kullanılarak doğru bir şekilde ayrıştırılması sağlandı. Bu, koordinat sorununu kesin olarak çözerek tüm firmaların haritada görüntülenmesini sağladı.
- **Feature:** Harita üzerindeki ikonlara tıklandığında açılan balona (Popup) firma adresi eklendi ve aynı koordinattaki firmalar tek bir ikon altında gruplanarak gösterilmeye başlandı.
- **Fix:** Koordinat verisinin doğrudan nesne (GeoJSON) olarak geldiği durumlar için destek eklendi. Kod artık üç farklı formatı (doğrudan nesne, WKB metni, JSON metni) işleyerek harita gösterimini daha esnek ve hatasız hale getiriyor.
- **Harita Stili Güncellemesi:** Harita görünümü, daha modern ve minimalist bir tasarım sunan CartoDB Positron teması ile güncellendi.

### Eklendi
- Arka plan görev yönetimi için kapsamlı bir sistem eklendi
  - `Scheduler` sınıfı ile periyodik görev yönetimi
  - Takılan işleri tespit etme ve yönetme özelliği
  - Eski iş kayıtlarını otomatik temizleme
- Yeni görev türleri eklendi:
  - `check_stuck_jobs`: Uzun süren işleri kontrol eder
  - `cleanup_jobs`: Eski iş kayıtlarını temizler
- Yapılandırılabilir görev ayarları eklendi
- Görev durumunu izlemek için API endpoint'leri eklendi
- Kapsamlı dokümantasyon eklendi

### Değiştirildi
- Ana uygulama başlatma ve kapatma işlemleri güncellendi
- Yapılandırma ayarları genişletildi
- Loglama iyileştirmeleri yapıldı

### Düzeltmeler
- CORS yapılandırması düzeltildi
- Görev yönetimi ile ilgili hatalar giderildi

## [0.1.5] - 2024-06-26

### Fixed
- **UI Color Rendering**: Resolved an issue where custom brand colors (e.g., secondary, accent) were not rendering correctly. Added specific color classes to the `safelist` in `tailwind.config.js` to ensure the JIT compiler always generates the required styles, guaranteeing consistent UI theming.

### Yeniden Yapılandırma
- **FileUploadSection:** Admin panelindeki dosya yükleme bileşeni (`file-upload-section.tsx`), mevcut hook'larla (`useExcelParser`, `useColumnMapper`, `useCompanyUploader`) tam uyumlu çalışacak şekilde baştan sona yeniden yazıldı.

### Düzeltmeler
- **FileUploadSection:** Bileşendeki tüm lint, tür ve çalışma zamanı hataları giderildi.
- **UI:** Eksik olan `Alert` ve `ScrollArea` shadcn/ui bileşenleri projeye eklendi.
- **FileUploadSection:** Veri önizleme tablosu, daha fazla satır gösterecek şekilde kaydırılabilir hale getirildi.
- **ColumnTypeModal:** Sütun eşleştirme pop-up'ı, `useColumnMapper` hook'undan gelen tüm veri türlerini destekleyecek şekilde dinamik hale getirildi.
- **UserAuthForm:** Kimlik doğrulama formundaki `name` alanı tür hatası giderildi ve kullanıcı arayüzü, önceki isteklere uygun olarak temizlendi.
- **Excel Parser (Kritik Düzeltme):** Excel işleme motoru, boş hücrelerin neden olduğu sütun kayması hatalarını gidermek için yeniden yapılandırıldı. Kod artık `sheet_to_json` yerine dosyayı hücre hücre manuel olarak okuyor, bu da veri bütünlüğünü ve yapısal doğruluğu her koşulda garanti altına alıyor.
- **Company Uploader:** Veri yükleme sırasında `CompanyData` tipine uymayan fazladan alanların eklenmesine neden olan bir tip hatası giderildi.

## [0.1.0] - 2023-01-01

### Eklendi
- İlk sürüm oluşturuldu
- Temel CRUD işlemleri eklendi
- Kullanıcı kimlik doğrulama sistemi eklendi

- **Fixed**: Corrected the LocationIQ API endpoint in  to resolve 404 errors and restore the geocoding fallback functionality.
