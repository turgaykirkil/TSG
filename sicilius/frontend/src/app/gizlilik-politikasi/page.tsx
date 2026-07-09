import { PublicHeader } from '@/components/layout/PublicHeader';
import { PublicFooter } from '@/components/layout/PublicFooter';

export const metadata = {
  title: 'Gizlilik Politikası | Sicilius',
  description: 'Sicilius platformu için gizlilik politikası ve veri güvenliği standartları.',
};

export default function GizlilikPolitikasiPage() {
  return (
    <>
      <PublicHeader />
      <main className="container max-w-4xl mx-auto pt-24 pb-12">
        <h1 className="text-3xl font-bold mb-2">Gizlilik Politikası</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400 mb-8">Son güncelleme: {new Date().toLocaleDateString('tr-TR')}</p>

        <section className="space-y-4">
          <p>
            Bu Gizlilik Politikası, Sicilius Platformu'nu ("Platform") kullanırken kişisel verilerinizin işlenmesine ilişkin
            esasları açıklar. Platformu kullanmakla bu politikayı okuduğunuzu ve kabul ettiğinizi beyan edersiniz.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">1. Toplanan Veriler</h2>
          <p>
            Hesap oluşturma ve oturum açma verileri, kullanım ve erişim kayıtları, cihaz/istemci bilgileri, iletişim içerikleri ve
            tercihleriniz işlenebilir. Çerezler ve benzeri teknolojilerle toplanan veriler için Çerez Politikası'na bakınız.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">2. İşleme Amaçları</h2>
          <ul className="list-disc pl-5 space-y-2">
            <li>Hizmetlerin sunulması, bakımı ve iyileştirilmesi</li>
            <li>Hesap güvenliği ve kimlik doğrulama</li>
            <li>Hukuki yükümlülüklerin yerine getirilmesi</li>
            <li>Hataların tespiti, performans ve analitik ölçümleri</li>
            <li>Kullanıcı destek ve iletişim süreçleri</li>
          </ul>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">3. Hukuki Sebepler</h2>
          <p>
            Kişisel verileriniz, sözleşmenin ifası, meşru menfaat, hukuki yükümlülüğün yerine getirilmesi ve açık rıza gibi KVKK'da
            öngörülen hukuki sebeplere dayanılarak işlenebilir.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">4. Aktarım ve Alıcı Grupları</h2>
          <p>
            Hizmet sağlayıcıları ve iş ortaklarıyla, mevzuatın öngördüğü hallerde yetkili mercilerle paylaşım yapılabilir. Üçüncü ülkelere
            aktarım olması halinde ilgili koruma mekanizmaları uygulanır.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">5. Saklama Süreleri</h2>
          <p>
            Veriler mevzuatta öngörülen veya işleme amacı için gerekli süre boyunca saklanır; süre sonunda güvenli şekilde silinir,
            anonim hale getirilir veya imha edilir.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">6. Haklarınız</h2>
          <p>
            KVKK uyarınca kişisel verilerinize erişme, düzeltme, silme, işlenmesini kısıtlama, itiraz etme ve veri taşınabilirliği haklarına sahipsiniz.
            Başvurularınızı aşağıdaki iletişim adresine iletebilirsiniz.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">7. İletişim</h2>
          <p>
            Sorularınız için: <a className="underline" href="mailto:privacy@sicilius.com.tr">privacy@sicilius.com.tr</a>
          </p>
        </section>
      </main>
      <PublicFooter />
    </>
  );
}
