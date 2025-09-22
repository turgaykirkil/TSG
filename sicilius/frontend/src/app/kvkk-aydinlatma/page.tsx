import { PublicHeader } from '@/components/layout/PublicHeader';
import { PublicFooter } from '@/components/layout/PublicFooter';

export const metadata = {
  title: 'KVKK Aydınlatma Metni • Sicilius',
  description: 'Sicilius Platformu için KVKK Aydınlatma Metni.'
};

export default function KvkkAydinlatmaPage() {
  return (
    <>
      <PublicHeader />
      <main className="container max-w-4xl mx-auto pt-24 pb-12">
      <h1 className="text-3xl font-bold mb-2">KVKK Aydınlatma Metni</h1>
      <p className="text-sm text-slate-500 dark:text-slate-400 mb-8">Son güncelleme: {new Date().toLocaleDateString('tr-TR')}</p>

      <section className="space-y-4">
        <p>
          6698 sayılı Kişisel Verilerin Korunması Kanunu (KVKK) uyarınca veri sorumlusu sıfatıyla, kişisel verilerinizi bu metinde
          açıklanan amaçlarla ve hukuki sebeplerle işlemekteyiz.
        </p>
      </section>

      <section className="mt-8 space-y-3">
        <h2 className="text-xl font-semibold">1. Veri Sorumlusu</h2>
        <p>
          Sicilius Platformu – İletişim: <a className="underline" href="mailto:kvkk@sicilius.local">kvkk@sicilius.local</a>
        </p>
      </section>

      <section className="mt-8 space-y-3">
        <h2 className="text-xl font-semibold">2. İşleme Amaçları</h2>
        <ul className="list-disc pl-5 space-y-2">
          <li>Hizmet sunumu ve geliştirilmesi</li>
          <li>Kimlik doğrulama ve hesap güvenliği</li>
          <li>Yasal yükümlülüklerin yerine getirilmesi</li>
          <li>Talep ve şikâyetlerin yönetimi</li>
        </ul>
      </section>

      <section className="mt-8 space-y-3">
        <h2 className="text-xl font-semibold">3. Hukuki Sebepler</h2>
        <p>
          KVKK m.5/2 ve m.6 hükümleri kapsamında; sözleşmenin kurulması/ifası, hukuki yükümlülük, meşru menfaat ve açık rıza
          hukuki sebeplerine dayanılabilir.
        </p>
      </section>

      <section className="mt-8 space-y-3">
        <h2 className="text-xl font-semibold">4. Alıcı Grupları ve Aktarım</h2>
        <p>
          Hizmet sağlayıcıları, iş ortakları, denetim ve danışmanlık firmaları ile yasal zorunluluk halinde yetkili kurumlara veri aktarımı yapılabilir.
          Yurt dışına aktarım gerekli olduğunda KVKK’ya uygun güvenlik önlemleri sağlanır.
        </p>
      </section>

      <section className="mt-8 space-y-3">
        <h2 className="text-xl font-semibold">5. Toplama Yöntemi</h2>
        <p>
          Veriler; çevrimiçi formlar, çerezler, log kayıtları, destek kanalları ve üçüncü taraf servisler aracılığıyla elektronik ortamda otomatik yollarla toplanır.
        </p>
      </section>

      <section className="mt-8 space-y-3">
        <h2 className="text-xl font-semibold">6. İlgili Kişinin Hakları</h2>
        <p>
          KVKK m.11 uyarınca; verilerinize erişme, düzeltme, silme/anonimleştirme, aktarmayı talep etme, işlemeyi kısıtlama, itiraz etme haklarına sahipsiniz.
          Başvurularınızı yazılı olarak veya kayıtlı elektronik posta ile iletebilirsiniz.
        </p>
      </section>

      <section className="mt-8 space-y-3">
        <h2 className="text-xl font-semibold">7. Başvuru</h2>
        <p>
          Başvurular için: <a className="underline" href="mailto:kvkk@sicilius.local">kvkk@sicilius.local</a>
        </p>
      </section>
      </main>
      <PublicFooter />
    </>
  );
}
