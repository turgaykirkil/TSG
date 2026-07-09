import { PublicHeader } from '@/components/layout/PublicHeader';
import { PublicFooter } from '@/components/layout/PublicFooter';

export const metadata = {
  title: 'Çerez Politikası | Sicilius',
  description: 'Sicilius platformunda kullanılan çerezler ve kullanıcı tercihleri hakkında bilgi.',
};

export default function CerezPolitikasiPage() {
  return (
    <>
      <PublicHeader />
      <main className="container max-w-4xl mx-auto pt-24 pb-12">
        <h1 className="text-3xl font-bold mb-2">Çerez Politikası</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400 mb-8">Son güncelleme: {new Date().toLocaleDateString('tr-TR')}</p>

        <section className="space-y-4">
          <p>
            Bu Çerez Politikası, Sicilius Platformu'nda ("Platform") kullanılan çerez ve benzeri teknolojilere ilişkin bilgi vermek amacıyla hazırlanmıştır.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">1. Çerez Nedir?</h2>
          <p>
            Çerezler, ziyaret ettiğiniz internet siteleri tarafından tarayıcınıza veya cihazınıza yerleştirilen küçük metin dosyalarıdır.
            Oturumunuzu sürdürmek, tercihlerinizi hatırlamak ve site performansını ölçmek için kullanılır.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">2. Kullanılan Çerez Türleri</h2>
          <ul className="list-disc pl-5 space-y-2">
            <li>Zorunlu çerezler (oturum, güvenlik, kimlik doğrulama)</li>
            <li>Performans ve analitik çerezleri</li>
            <li>İşlevsellik çerezleri (tercihlerin hatırlanması)</li>
          </ul>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">3. Çerez Yönetimi</h2>
          <p>
            Tarayıcı ayarlarından çerezleri devre dışı bırakabilir, silebilir veya uyarı almayı tercih edebilirsiniz. Çerezleri kapatmanız
            bazı hizmetlerin düzgün çalışmamasına yol açabilir.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">4. Üçüncü Taraf Çerezleri</h2>
          <p>
            Üçüncü taraf sağlayıcıların çerezleri; performans ölçümü, hata ayıklama veya entegrasyon hizmetleri için kullanılabilir.
            Bu çerezler ilgili üçüncü tarafların politikalarına tabidir.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">5. İletişim</h2>
          <p>
            Çerezlere ilişkin sorularınız için: <a className="underline" href="mailto:privacy@sicilius.com.tr">privacy@sicilius.com.tr</a>
          </p>
        </section>
      </main>
      <PublicFooter />
    </>
  );
}
