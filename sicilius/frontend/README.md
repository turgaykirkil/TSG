# ⚛️ Frontend — Next.js 14 Web Application

Sicilius platformunun kullanıcı arayüzü, modern Next.js 14 App Router mimarisiyle geliştirilmiş, veri görselleştirme odaklı bir web uygulamasıdır.

## 🛠️ Teknoloji Yığını (Tech Stack)

- **Next.js 14:** React tabanlı modern framework (App Router & Standalone build).
- **TypeScript:** Güçlü tip koruması ve yüksek refaktör güvenliği.
- **Tailwind CSS:** Responsive ve hızlı arayüz geliştirme.
- **Shadcn/UI & Radix UI:** Premium, erişilebilir ve özelleştirilebilir arayüz bileşenleri.
- **React Force Graph:** NEXUS 2D/3D interaktif ağ ilişkileri grafiği.
- **Leaflet & OpenStreetMap:** Şirketlerin coğrafi konum analizi ve kümeleme haritaları.
- **Chart.js & Plotly:** Risk skorları, contagion simülasyonları ve Sankey sermaye akışları.

## 📂 Proje Yapısı

```
frontend/
├── src/
│   ├── app/            # Next.js App Router (Sayfalar ve Routelar)
│   │   ├── (app)/      # Auth korumalı uygulama sayfaları (Dashboard, Admin, Profile)
│   │   ├── (public)/   # Herkese açık sayfalar (Login, Register, SSS, Hakkında)
│   │   ├── api/        # Next.js iç API ve routing proxy'leri
│   │   └── presentation/# Standalone sunum sayfası
│   ├── components/     # Yeniden kullanılabilir UI ve grafik bileşenleri
│   ├── contexts/       # Global state ve Context API'leri
│   ├── hooks/          # Özel React hook'ları (API sorguları, harita işlemleri)
│   └── lib/            # Supabase istemcisi, API istekleri ve yardımcı fonksiyonlar
├── public/             # Statik assetler, SVG'ler ve NEXUS harici dosyaları
└── package.json        # Bağımlılıklar ve scriptler
```

## 🚀 Hızlı Başlangıç (Yerel Çalıştırma)

Uygulamayı yerelinizde geliştirmek için:

```bash
# 1. Bağımlılıkları yükleyin
npm install # veya yarn install

# 2. Çevre değişkenlerini oluşturun
cp .env.local.example .env.local

# 3. Geliştirici sunucusunu başlatın
npm run dev # veya yarn dev
```
Tarayıcınızda `http://localhost:3000` adresinden uygulamaya erişebilirsiniz.

## ⚙️ Çevre Değişkenleri (.env.local)

```env
NEXT_PUBLIC_API_URL=https://sicilius.com.tr
# Supabase veya Auth bağlantıları gerekirse:
NEXT_PUBLIC_SUPABASE_URL=...
NEXT_PUBLIC_SUPABASE_ANON_KEY=...
```

## 📦 Production Derleme (Build)

Next.js, hybrid Docker mimarisi için `standalone` modunda derlenecek şekilde yapılandırılmıştır.

```bash
# Production derlemesi al
npm run build

# Production sunucusunu başlat
npm run start
```

## 🎨 Tasarım Standartları

Uygulama, kurumsal istihbarat hissini yansıtan modern bir koyu tema (dark theme), glassmorphism efektleri ve dinamik mikro-animasyonlar barındırır. CSS Grid yapısı tamamen mobil cihazlara duyarlı (responsive) olacak şekilde tasarlanmıştır.
