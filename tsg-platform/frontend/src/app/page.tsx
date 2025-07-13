import Link from 'next/link';
import { SiciliusLogo as Logo } from '@/components/icons/SiciliusLogo'; // Logoyu isimlendirilmiş export olarak import et ve 'Logo' olarak yeniden adlandır

// Bileşenleri daha modüler hale getirelim
const Header = () => (
  <header className="fixed top-0 left-0 w-full bg-white/80 backdrop-blur-sm z-50 border-b border-gray-200">
    <div className="container mx-auto px-6 h-16 flex justify-between items-center">
      <Link href="#" className="flex items-center">
        <Logo className="h-8 w-auto text-primary" />
      </Link>
      <nav className="hidden md:flex items-center space-x-8">
        <Link href="#features" className="text-sm text-gray-600 hover:text-blue-600">Özellikler</Link>
        <Link href="#why-sicilius" className="text-sm text-gray-600 hover:text-blue-600">Neden Sicilius?</Link>
        <Link href="#pricing" className="text-sm text-gray-600 hover:text-blue-600">Fiyatlandırma</Link>
      </nav>
      <div className="flex items-center space-x-4">
        <Link href="/login" className="text-sm font-medium text-gray-600 hover:text-blue-600">Giriş Yap</Link>
        <Link href="/register" className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-full hover:bg-blue-700 transition-colors">
          Kayıt Ol
        </Link>
      </div>
    </div>
  </header>
);

const HeroSection = () => (
  <section className="pt-40 pb-24 text-center bg-gray-50">
    <div className="container mx-auto px-6">
      <h1 className="text-5xl md:text-6xl font-bold text-gray-900 leading-tight mb-4">
        Veri Analiz Gücünüzü Ortaya Çıkarın
      </h1>
      <p className="max-w-2xl mx-auto text-lg text-gray-600 mb-8">
        Sicilius, karmaşık verileri anlaşılır içgörülere dönüştürür. Akıllı otomasyon ve güçlü analiz araçlarıyla iş süreçlerinizi optimize edin.
      </p>
      <div className="flex justify-center space-x-4">
        <Link href="/register" className="px-8 py-3 font-semibold text-white bg-blue-600 rounded-full hover:bg-blue-700 transition-transform transform hover:scale-105">
          Hemen Başlayın
        </Link>
        <Link href="#features" className="px-8 py-3 font-semibold text-blue-600 bg-white border border-gray-300 rounded-full hover:bg-gray-100 transition-transform transform hover:scale-105">
          Daha Fazla Bilgi
        </Link>
      </div>
    </div>
  </section>
);

const FeaturesSection = () => (
  <section id="features" className="py-20 bg-white">
    <div className="container mx-auto px-6 text-center">
      <div className="inline-block px-4 py-1 text-sm font-semibold text-blue-600 bg-blue-100 rounded-full mb-4">
        Temel Özellikler
      </div>
      <h2 className="text-4xl font-bold text-gray-900 mb-4">İş Akışınızı Hızlandırın</h2>
      <p className="max-w-3xl mx-auto text-gray-600 mb-12">
        Platformumuz, veri toplama, analiz ve raporlama süreçlerinizi otomatikleştirmek için tasarlanmıştır.
      </p>
      <div className="grid md:grid-cols-3 gap-8 text-left">
        <div className="p-8 bg-gray-50 rounded-xl shadow-sm">
          <h3 className="text-xl font-bold mb-2">Akıllı Veri Çıkarımı</h3>
          <p className="text-gray-600">PDF ve Excel dosyalarından otomatik olarak veri çekin ve yapılandırın.</p>
        </div>
        <div className="p-8 bg-gray-50 rounded-xl shadow-sm">
          <h3 className="text-xl font-bold mb-2">Coğrafi Veri Zenginleştirme</h3>
          <p className="text-gray-600">Adres verilerinizi otomatik olarak coğrafi koordinatlarla zenginleştirin.</p>
        </div>
        <div className="p-8 bg-gray-50 rounded-xl shadow-sm">
          <h3 className="text-xl font-bold mb-2">Güvenli Veri Yönetimi</h3>
          <p className="text-gray-600">Tüm verileriniz, Supabase'in güçlü güvenlik altyapısıyla korunur.</p>
        </div>
      </div>
    </div>
  </section>
);

const WhySiciliusSection = () => (
    <section id="why-sicilius" className="py-20 bg-gray-50">
        <div className="container mx-auto px-6">
            <div className="text-center mb-12">
                <h2 className="text-4xl font-bold text-gray-900">Neden Sicilius?</h2>
                <p className="max-w-2xl mx-auto mt-4 text-lg text-gray-600">Verilerinizi rekabet avantajına dönüştürmek için tasarlandık.</p>
            </div>
            <div className="grid md:grid-cols-2 gap-16 items-center">
                <div className="space-y-8">
                    <div>
                        <h3 className="text-2xl font-bold mb-2">Tek Platform, Tüm İhtiyaçlar</h3>
                        <p className="text-gray-600">Farklı araçlar arasında geçiş yapmaya son. Veri toplama, analiz, görselleştirme ve raporlama işlemlerinin tamamını tek bir yerden yönetin.</p>
                    </div>
                    <div>
                        <h3 className="text-2xl font-bold mb-2">Zamandan ve Maliyetten Tasarruf</h3>
                        <p className="text-gray-600">Manuel veri işleme süreçlerini otomatikleştirerek ekibinizin daha stratejik görevlere odaklanmasını sağlayın, operasyonel verimliliği artırın.</p>
                    </div>
                    <div>
                        <h3 className="text-2xl font-bold mb-2">Ölçeklenebilir ve Güvenli Altyapı</h3>
                        <p className="text-gray-600">İşletmeniz büyüdükçe artan veri hacminizi kolayca yönetin. Supabase altyapısı ile verileriniz her zaman güvende ve erişilebilir.</p>
                    </div>
                </div>
                <div className="bg-white p-8 rounded-xl shadow-lg h-96 flex items-center justify-center">
                    <p className="text-2xl text-gray-300">[Etkileyici bir görsel veya animasyon alanı]</p>
                </div>
            </div>
        </div>
    </section>
);

const PricingSection = () => (
    <section id="pricing" className="py-20 bg-white">
        <div className="container mx-auto px-6 text-center">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Şeffaf Fiyatlandırma</h2>
            <p className="max-w-2xl mx-auto text-lg text-gray-600 mb-12">İhtiyaçlarınıza en uygun planı seçerek hemen başlayın. Gizli ücretler yok, taahhüt yok.</p>
            <div className="grid lg:grid-cols-3 gap-8 max-w-4xl mx-auto">
                {/* Plan 1 */}
                <div className="border rounded-xl p-8 flex flex-col">
                    <h3 className="text-2xl font-bold mb-2">Başlangıç</h3>
                    <p className="text-gray-600 mb-4">Bireysel kullanıcılar ve küçük ekipler için.</p>
                    <p className="text-4xl font-bold my-4">₺499<span className="text-lg font-normal text-gray-500">/ay</span></p>
                    <ul className="text-left space-y-2 mb-8">
                        <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> 1 Kullanıcı</li>
                        <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> 10.000 Veri Satırı</li>
                        <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Temel Raporlama</li>
                    </ul>
                    <Link href="/register" className="mt-auto w-full text-center px-6 py-3 font-semibold text-white bg-blue-600 rounded-full hover:bg-blue-700">
                        Planı Seç
                    </Link>
                </div>
                {/* Plan 2 - Öne Çıkan */}
                <div className="border-2 border-blue-600 rounded-xl p-8 flex flex-col relative shadow-xl">
                    <div className="absolute top-0 -translate-y-1/2 left-1/2 -translate-x-1/2">
                        <div className="bg-blue-600 text-white px-4 py-1 text-sm font-semibold rounded-full">En Popüler</div>
                    </div>
                    <h3 className="text-2xl font-bold mb-2">Profesyonel</h3>
                    <p className="text-gray-600 mb-4">Büyüyen işletmeler ve ajanslar için.</p>
                    <p className="text-4xl font-bold my-4">₺999<span className="text-lg font-normal text-gray-500">/ay</span></p>
                    <ul className="text-left space-y-2 mb-8">
                        <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> 5 Kullanıcı</li>
                        <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> 100.000 Veri Satırı</li>
                        <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Gelişmiş Raporlama</li>
                        <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> API Erişimi</li>
                    </ul>
                    <Link href="/register" className="mt-auto w-full text-center px-6 py-3 font-semibold text-white bg-blue-600 rounded-full hover:bg-blue-700">
                        Planı Seç
                    </Link>
                </div>
                {/* Plan 3 */}
                <div className="border rounded-xl p-8 flex flex-col">
                    <h3 className="text-2xl font-bold mb-2">Kurumsal</h3>
                    <p className="text-gray-600 mb-4">Geniş ölçekli operasyonlar için.</p>
                    <p className="text-4xl font-bold my-4">Bize Ulaşın</p>
                    <ul className="text-left space-y-2 mb-8">
                        <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Sınırsız Kullanıcı</li>
                        <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Özel Veri Limiti</li>
                        <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Öncelikli Destek</li>
                        <li className="flex items-center"><span className="text-green-500 mr-2">✓</span> Özel Entegrasyonlar</li>
                    </ul>
                    <Link href="/contact" className="mt-auto w-full text-center px-6 py-3 font-semibold text-blue-600 bg-white border border-gray-300 rounded-full hover:bg-gray-100">
                        İletişime Geç
                    </Link>
                </div>
            </div>
        </div>
    </section>
);

const Footer = () => (
  <footer className="py-12 bg-gray-50 border-t">
    <div className="container mx-auto px-6 text-center">
        <p className="text-sm text-gray-500 mb-4">&copy; 2024 Sicilius. Tüm hakları saklıdır.</p>
        <div className="flex justify-center space-x-6">
            <Link href="#" className="text-sm text-gray-500 hover:underline">Kullanım Koşulları</Link>
            <Link href="#" className="text-sm text-gray-500 hover:underline">Gizlilik Politikası</Link>
        </div>
    </div>
  </footer>
);

export default function HomePage() {
  return (
    <div className="bg-white">
      <Header />
      <main>
        <HeroSection />
        <FeaturesSection />
        <WhySiciliusSection />
        <PricingSection />
      </main>
      <Footer />
    </div>
  );
}
