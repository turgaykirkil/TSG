import Link from 'next/link';
import { PublicHeader } from '@/components/layout/PublicHeader';
import { PublicFooter } from '@/components/layout/PublicFooter';
import { Button } from '@/components/ui/button';

// Üst header artık PublicHeader bileşeninden geliyor

const HeroSection = () => (
  <section className="pt-40 pb-24 text-center bg-gray-50 dark:bg-slate-900">
    <div className="container mx-auto px-6">
      <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-slate-100 leading-tight mb-4">
        Veri Analiz Gücünüzü Ortaya Çıkarın
      </h1>
      <p className="max-w-2xl mx-auto text-lg text-gray-600 dark:text-slate-300 mb-8">
        Sicilius, halka açık kaynaklardan derlenen şirket verilerini anlaşılır içgörülere dönüştürür. Güçlü arama ve harita yetenekleriyle kayıt ve ilişkileri hızla görüntüleyin.
      </p>
      <div className="flex justify-center space-x-4">
        <Button asChild variant="gradient" className="px-8 py-3 font-semibold rounded-full">
          <Link href="/login">Giriş Yap</Link>
        </Button>
        <Button
          asChild
          variant="gradientText"
          className="px-8 py-3 font-semibold rounded-full"
        >
          <Link href="#policies">Kullanım İlkeleri</Link>
        </Button>
      </div>
    </div>
  </section>
);

const FeaturesSection = () => (
  <section id="features" className="py-20 bg-white dark:bg-slate-950">
    <div className="container mx-auto px-6 text-center">
      <div className="inline-block px-4 py-1 text-sm font-semibold text-blue-600 bg-blue-100 rounded-full mb-4">
        Temel Özellikler
      </div>
      <h2 className="text-4xl font-bold text-gray-900 dark:text-slate-100 mb-4">İş Akışınızı Hızlandırın</h2>
      <p className="max-w-3xl mx-auto text-gray-600 dark:text-slate-300 mb-12">
        Platformumuz, veri toplama, analiz ve raporlama süreçlerinizi otomatikleştirmek için tasarlanmıştır.
      </p>
      <div className="grid md:grid-cols-3 gap-8 text-left">
        <div className="p-8 bg-gray-50 dark:bg-slate-900 rounded-xl shadow-sm">
          <h3 className="text-xl font-bold mb-2 text-foreground">Akıllı Veri Çıkarımı</h3>
          <p className="text-gray-600 dark:text-slate-300">PDF ve Excel dosyalarından otomatik olarak veri çekin ve yapılandırın.</p>
        </div>
        <div className="p-8 bg-gray-50 dark:bg-slate-900 rounded-xl shadow-sm">
          <h3 className="text-xl font-bold mb-2 text-foreground">Coğrafi Veri Zenginleştirme</h3>
          <p className="text-gray-600 dark:text-slate-300">Adres verilerinizi otomatik olarak coğrafi koordinatlarla zenginleştirin.</p>
        </div>
        <div className="p-8 bg-gray-50 dark:bg-slate-900 rounded-xl shadow-sm">
          <h3 className="text-xl font-bold mb-2 text-foreground">Güvenli Veri Yönetimi</h3>
          <p className="text-gray-600 dark:text-slate-300">Tüm verileriniz, Supabase'in güçlü güvenlik altyapısıyla korunur.</p>
        </div>
      </div>
    </div>
  </section>
);

const WhySiciliusSection = () => (
    <section id="why-sicilius" className="py-20 bg-gray-50 dark:bg-slate-900">
        <div className="container mx-auto px-6">
            <div className="text-center mb-12">
                <h2 className="text-4xl font-bold text-gray-900 dark:text-slate-100">Neden Sicilius?</h2>
                <p className="max-w-2xl mx-auto mt-4 text-lg text-gray-600 dark:text-slate-300">Verilerinizi rekabet avantajına dönüştürmek için tasarlandık.</p>
            </div>
            <div className="grid md:grid-cols-2 gap-16 items-center">
                <div className="space-y-8">
                    <div>
                        <h3 className="text-2xl font-bold mb-2 text-foreground">Tek Platform, Tüm İhtiyaçlar</h3>
                        <p className="text-gray-600 dark:text-slate-300">Farklı araçlar arasında geçiş yapmaya son. Veri toplama, analiz, görselleştirme ve raporlama işlemlerinin tamamını tek bir yerden yönetin.</p>
                    </div>
                    <div>
                        <h3 className="text-2xl font-bold mb-2 text-foreground">Zamandan ve Maliyetten Tasarruf</h3>
                        <p className="text-gray-600 dark:text-slate-300">Manuel veri işleme süreçlerini otomatikleştirerek ekibinizin daha stratejik görevlere odaklanmasını sağlayın, operasyonel verimliliği artırın.</p>
                    </div>
                    <div>
                        <h3 className="text-2xl font-bold mb-2 text-foreground">Ölçeklenebilir ve Güvenli Altyapı</h3>
                        <p className="text-gray-600 dark:text-slate-300">İşletmeniz büyüdükçe artan veri hacminizi kolayca yönetin. Supabase altyapısı ile verileriniz her zaman güvende ve erişilebilir.</p>
                    </div>
                </div>
                <div className="bg-white dark:bg-slate-950 p-8 rounded-xl shadow-lg h-96 flex items-center justify-center">
                    <p className="text-2xl text-gray-300 dark:text-slate-600">[Etkileyici bir görsel veya animasyon alanı]</p>
                </div>
            </div>
        </div>
    </section>
);

const PoliciesSection = () => (
  <section id="policies" className="py-20 bg-white dark:bg-slate-950">
    <div className="container mx-auto px-6">
      <div className="text-center mb-10">
        <h2 className="text-4xl font-bold text-gray-900 dark:text-slate-100 mb-3">Kullanım İlkeleri</h2>
        <p className="max-w-2xl mx-auto text-lg text-gray-600 dark:text-slate-300">Sicilius her zaman ücretsizdir; adil kullanım ilkesiyle günlük 20 sorgu hakkı sunar.</p>
      </div>
      <div className="grid md:grid-cols-3 gap-8">
        <div className="p-6 border rounded-xl bg-gray-50 dark:bg-slate-900">
          <h3 className="text-xl font-semibold mb-2">Her Zaman Ücretsiz</h3>
          <p className="text-gray-600 dark:text-slate-300">Uygulama kalıcı olarak ücretsizdir. Ücretli plan, satış teklifi veya taahhüt bulunmaz.</p>
        </div>
        <div className="p-6 border rounded-xl bg-gray-50 dark:bg-slate-900">
          <h3 className="text-xl font-semibold mb-2">Günlük 20 Sorgu</h3>
          <p className="text-gray-600 dark:text-slate-300">Her kullanıcı için günlük 20 sorgu sınırı uygulanır. Limit yenilemesi her gün yapılır.</p>
        </div>
        <div className="p-6 border rounded-xl bg-gray-50 dark:bg-slate-900">
          <h3 className="text-xl font-semibold mb-2">Davetle Üyelik</h3>
          <p className="text-gray-600 dark:text-slate-300">Kayıt açık değildir. Mevcut kullanıcı, ayda yalnızca 1 e-posta adresi davet edebilir.</p>
        </div>
      </div>
      <div className="mt-10 text-center text-sm text-gray-600">
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
    <div className="bg-white min-h-screen flex flex-col">
      <PublicHeader />
      <main className="pt-20 md:pt-24">
        <HeroSection />
        <FeaturesSection />
        <WhySiciliusSection />
        <PoliciesSection />
      </main>
      <PublicFooter />
    </div>
  );
}
