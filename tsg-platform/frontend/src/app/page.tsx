'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Icons } from '@/components/icons';

export default function HomePage() {
  return (
    <div className="flex flex-col min-h-screen bg-gray-50">
      {/* Header */}
      <header className="px-4 lg:px-6 h-16 flex items-center shadow-sm bg-white z-10">
        <Link href="#" className="flex items-center justify-center" prefetch={false}>
          <Icons.logo className="h-6 w-6 text-primary" />
          <span className="ml-2 text-xl font-bold text-gray-900">Sicilius</span>
        </Link>
        <nav className="ml-auto flex gap-4 sm:gap-6">
          <Link href="/login" className="text-sm font-medium hover:underline underline-offset-4" prefetch={false}>
            Giriş Yap
          </Link>
          <Link href="/register" passHref>
             <Button variant="default" size="sm" className="bg-primary text-white hover:bg-primary/90">
                Kayıt Ol
             </Button>
          </Link>
        </nav>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32 xl:py-48 bg-white">
          <div className="container px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-[1fr_400px] lg:gap-12 xl:grid-cols-[1fr_600px]">
              <div className="flex flex-col justify-center space-y-4">
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none text-gray-900">
                    Veri Analiz Gücünüzü Ortaya Çıkarın
                  </h1>
                  <p className="max-w-[600px] text-gray-500 md:text-xl">
                    Sicilius, karmaşık verileri anlaşılır içgörülere dönüştürür. Akıllı otomasyon ve güçlü analiz araçlarıyla iş süreçlerinizi optimize edin.
                  </p>
                </div>
                <div className="flex flex-col gap-2 min-[400px]:flex-row">
                  <Link
                    href="/login"
                    className="inline-flex h-10 items-center justify-center rounded-md bg-primary px-8 text-sm font-medium text-gray-50 shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
                    prefetch={false}
                  >
                    Başlayın
                  </Link>
                  <Link
                    href="#features"
                    className="inline-flex h-10 items-center justify-center rounded-md border border-primary bg-transparent px-8 text-sm font-medium text-primary shadow-sm transition-colors hover:bg-primary/5 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50"
                    prefetch={false}
                  >
                    Özellikleri Keşfet
                  </Link>
                </div>
              </div>
                <div>
                </div>
            </div>
          </div>
        </section>

        <section id="features" className="w-full py-12 md:py-24 lg:py-32 bg-gray-100">
           <div className="container px-4 md:px-6">
            <div className="flex flex-col items-center justify-center space-y-4 text-center">
                <div className="space-y-2">
                    <div className="inline-block rounded-lg bg-gray-200 px-3 py-1 text-sm">Temel Özellikler</div>
                    <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">İş Akışınızı Hızlandırın</h2>
                    <p className="max-w-[900px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                        Platformumuz, veri toplama, analiz ve raporlama süreçlerinizi otomatikleştirmek için tasarlanmıştır.
                    </p>
                </div>
            </div>
            <div className="mx-auto grid max-w-5xl items-center gap-6 py-12 lg:grid-cols-3 lg:gap-12">
                <div className="grid gap-1">
                    <h3 className="text-xl font-bold">Akıllı Veri Çıkarımı</h3>
                    <p className="text-sm text-gray-500">PDF ve Excel dosyalarından otomatik olarak veri çekin ve yapılandırın.</p>
                </div>
                <div className="grid gap-1">
                    <h3 className="text-xl font-bold">Coğrafi Veri Zenginleştirme</h3>
                    <p className="text-sm text-gray-500">Adres verilerinizi otomatik olarak coğrafi koordinatlarla zenginleştirin.</p>
                </div>
                <div className="grid gap-1">
                    <h3 className="text-xl font-bold">Güvenli Veri Yönetimi</h3>
                    <p className="text-sm text-gray-500">Tüm verileriniz, Supabase'in güçlü güvenlik altyapısıyla korunur.</p>
                </div>
            </div>
        </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="flex flex-col gap-2 sm:flex-row py-6 w-full shrink-0 items-center px-4 md:px-6 border-t bg-white">
        <p className="text-xs text-gray-500">&copy; 2024 Sicilius. Tüm hakları saklıdır.</p>
        <nav className="sm:ml-auto flex gap-4 sm:gap-6">
          <Link href="#" className="text-xs hover:underline underline-offset-4" prefetch={false}>
            Kullanım Koşulları
          </Link>
          <Link href="#" className="text-xs hover:underline underline-offset-4" prefetch={false}>
            Gizlilik Politikası
          </Link>
        </nav>
      </footer>
    </div>
  );
}
