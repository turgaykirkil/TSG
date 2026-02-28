import Link from 'next/link';
import { PublicHeader } from '@/components/layout/PublicHeader';
import { PublicFooter } from '@/components/layout/PublicFooter';
import { Button } from '@/components/ui/button';
import Reveal from '@/components/ui/reveal';
import WhySiciliusAnimated from '@/components/illustrations/WhySiciliusAnimated';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Sicilius | Kurumsal Veri Analizi ve Sorgulama',
  description: 'Türkiye kurumsal verileri üzerinde hızlı arama, ilişki analizi ve görselleştirme yapın. Dağınık kayıtları tek noktada keşfedin.',
};

// Üst header artık PublicHeader bileşeninden geliyor

const HeroSection = () => (
  <section className="relative h-[calc(100svh+4rem)] md:h-[calc(100svh+5rem)] snap-start flex items-center bg-background overflow-hidden">
    {/* Arka planda yumuşak animasyon */}
    <div className="hero-animated-bg" aria-hidden="true" />
    <div className="container mx-auto px-6 w-full text-center relative">
      <Reveal>
        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-slate-100 leading-tight mb-4">
          Kurumsal Veri Analiz Gücünüzü Ortaya Çıkarın
        </h1>
      </Reveal>
      <Reveal delayMs={120}>
        <p className="max-w-2xl mx-auto text-lg text-foreground/80 dark:text-slate-200 mb-8">
          Türkiye'deki halka açık kayıtları tek bir akıllı platformda birleştirin. Şirket sorgulama, ortaklık yapısı analizi ve kurumsal ilişki haritası ile karmaşık verileri saniyeler içinde çözün.
        </p>
      </Reveal>
      <Reveal delayMs={220}>
        <div className="flex justify-center gap-4">
          <Button asChild variant="gradient" className="px-8 py-3 font-semibold rounded-full">
            <Link href="/login">Giriş Yap</Link>
          </Button>
          <Button asChild variant="gradientText" className="px-8 py-3 font-semibold rounded-full">
            <Link href="#policies">Kullanım İlkeleri</Link>
          </Button>
        </div>
      </Reveal>
    </div>
  </section>
);

const FeaturesSection = () => (
  <section id="features" className="min-h-[calc(100svh-4rem)] md:min-h-[calc(100svh-5rem)] snap-start flex items-center py-20 bg-white dark:bg-slate-950">
    <div className="container mx-auto px-6 text-center">
      <div className="inline-block px-4 py-1 text-sm font-semibold text-blue-600 bg-blue-100 rounded-full mb-4">
        Temel Özellikler
      </div>
      <Reveal>
        <h2 className="text-4xl font-bold text-gray-900 dark:text-slate-100 mb-4">Kolay Şirket ve Sicil Kaydı Keşfi için Tasarlandı</h2>
      </Reveal>
      <Reveal delayMs={120}>
        <p className="max-w-3xl mx-auto text-foreground/80 dark:text-slate-200 mb-12">
          Kayıtları tek yerde sunar; hızlı arama, filtreler ve ilişki görünümüyle aradığınızı çabucak bulun.
        </p>
      </Reveal>
      <div className="grid md:grid-cols-3 gap-8 text-left">
        <Reveal className="p-8 bg-gray-50 dark:bg-slate-900 rounded-xl shadow-sm">
          <h3 className="text-xl font-bold mb-2 text-foreground">Gelişmiş Şirket Sorgulama</h3>
          <p className="text-gray-700 dark:text-slate-200">Resmi gazete duyuruları, unvan değişiklikleri ve tescil bilgilerine anında ulaşın.</p>
        </Reveal>
        <Reveal delayMs={100} className="p-8 bg-gray-50 dark:bg-slate-900 rounded-xl shadow-sm">
          <h3 className="text-xl font-bold mb-2 text-foreground">Kurumsal İlişki Ağı Analizi</h3>
          <p className="text-gray-700 dark:text-slate-200">Şirketler ve ortaklar arasındaki bağlantıları görselleştirerek stratejik içgörüler edinin.</p>
        </Reveal>
        <Reveal delayMs={200} className="p-8 bg-gray-50 dark:bg-slate-900 rounded-xl shadow-sm">
          <h3 className="text-xl font-bold mb-2 text-foreground">Akıllı Konum Haritası</h3>
          <p className="text-gray-700 dark:text-slate-200">Şirket adreslerini ve şube bilgilerini interaktif harita üzerinde doğrusal olarak keşfedin.</p>
        </Reveal>
      </div>
    </div>
  </section>
);

const WhySiciliusSection = () => (
  <section id="why-sicilius" className="min-h-[calc(100svh-4rem)] md:min-h-[calc(100svh-5rem)] snap-start flex items-center bg-gray-50 dark:bg-slate-900 py-20">
    <div className="container mx-auto px-6">
      <div className="text-center mb-12">
        <Reveal>
          <h2 className="text-4xl font-bold text-gray-900 dark:text-slate-100">Neden Sicilius?</h2>
        </Reveal>
        <Reveal delayMs={120}>
          <p className="max-w-2xl mx-auto mt-4 text-lg text-gray-700 dark:text-slate-200">Dağınık kamu kayıtlarının tek bakışta anlam kazanması için kurgulandı.</p>
        </Reveal>
      </div>
      <div className="grid md:grid-cols-2 gap-16 items-center">
        <div className="space-y-8">
          <Reveal>
            <h3 className="text-2xl font-bold mb-2 text-foreground">Tek Bakışta Bütünlük</h3>
            <p className="text-gray-700 dark:text-slate-200">Farklı kaynaklardan gelen kayıtlar tutarlı bir görünümde buluşur.</p>
          </Reveal>
          <Reveal delayMs={120}>
            <h3 className="text-2xl font-bold mb-2 text-foreground">Aradığını Hemen Bul</h3>
            <p className="text-gray-700 dark:text-slate-200">Kayıtları ada, numaraya veya bağlama göre hızla daraltın.</p>
          </Reveal>
          <Reveal delayMs={220}>
            <h3 className="text-2xl font-bold mb-2 text-foreground">Güven Veren Temel</h3>
            <p className="text-gray-700 dark:text-slate-200">Altyapımız şeffaflık ve sürdürülebilirlik ilkeleriyle kurgulandı.</p>
          </Reveal>
        </div>
        <Reveal delayMs={200}>
          <WhySiciliusAnimated />
        </Reveal>
      </div>
    </div>
  </section>
);

const PoliciesSection = () => (
  <section id="policies" className="min-h-[calc(100svh-4rem)] md:min-h-[calc(100svh-5rem)] snap-start flex items-center bg-white dark:bg-slate-950 py-20">
    <div className="container mx-auto px-6">
      <div className="text-center mb-10">
        <Reveal>
          <h2 className="text-4xl font-bold text-gray-900 dark:text-slate-100 mb-3">Kullanım İlkeleri</h2>
        </Reveal>
        <Reveal delayMs={120}>
          <p className="max-w-2xl mx-auto text-lg text-gray-700 dark:text-slate-200">Sicilius, ticari şeffaflık için her zaman ücretsizdir. Günlük 20 profesyonel sorgu hakkı ile veri analizine hemen başlayın.</p>
        </Reveal>
      </div>
      <div className="grid md:grid-cols-3 gap-8">
        <Reveal className="p-6 border rounded-xl bg-gray-50 dark:bg-slate-900">
          <h3 className="text-xl font-semibold mb-2 text-foreground">Sınırsız ve Ücretsiz Erişim</h3>
          <p className="text-foreground/90 dark:text-slate-200">Platformumuz topluluk yararına her zaman ücretsiz kalacaktır. Gizli ücretler veya abonelikler yoktur.</p>
        </Reveal>
        <Reveal delayMs={100} className="p-6 border rounded-xl bg-gray-50 dark:bg-slate-900">
          <h3 className="text-xl font-semibold mb-2 text-foreground">Günlük Sorgu Kapasitesi</h3>
          <p className="text-foreground/90 dark:text-slate-200">Adil kullanım kotası dahilinde her gün 20 yeni şirket veya ilan detayını derinlemesine inceleyebilirsiniz.</p>
        </Reveal>
        <Reveal delayMs={200} className="p-6 border rounded-xl bg-gray-50 dark:bg-slate-900">
          <h3 className="text-xl font-semibold mb-2 text-foreground">Özel Davet Sistemi</h3>
          <p className="text-foreground/90 dark:text-slate-200">Veri kalitesini korumak için sistemimiz davetiye ile çalışmaktadır. Mevcut üyeler aracılığıyla platforma katılabilirsiniz.</p>
        </Reveal>
      </div>
      <div className="mt-10 text-center text-sm text-foreground/80">
        <p>
          Detaylı hükümler ve koşullar için <Link href="/kullanici-sozlesmesi" className="rounded px-1 -mx-1 hover:bg-gray-100 dark:hover:bg-slate-800">Kullanıcı Sözleşmesi</Link>,
          {' '}<Link href="/gizlilik-politikasi" className="rounded px-1 -mx-1 hover:bg-gray-100 dark:hover:bg-slate-800">Gizlilik Politikası</Link>,
          {' '}<Link href="/cerez-politikasi" className="rounded px-1 -mx-1 hover:bg-gray-100 dark:hover:bg-slate-800">Çerez Politikası</Link> ve
          {' '}<Link href="/kvkk-aydinlatma" className="rounded px-1 -mx-1 hover:bg-gray-100 dark:hover:bg-slate-800">KVKK Aydınlatma</Link> sayfalarını inceleyiniz.
        </p>
      </div>
    </div>
  </section>
);

// Alt footer artık PublicFooter bileşeninden geliyor

export default function HomePage() {
  return (
    <div className="bg-background min-h-screen flex flex-col">
      <PublicHeader />
      <main className="flex-1 h-[calc(100svh-4rem)] md:h-[calc(100svh-5rem)] overflow-y-auto snap-y snap-mandatory scroll-pt-24 md:scroll-pt-28">
        <HeroSection />
        <FeaturesSection />
        <WhySiciliusSection />
        <PoliciesSection />
      </main>
      <PublicFooter />
    </div>
  );
}
