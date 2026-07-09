import { PublicHeader } from '@/components/layout/PublicHeader';
import { PublicFooter } from '@/components/layout/PublicFooter';

export const metadata = {
  title: 'Kullanıcı Sözleşmesi | Sicilius',
  description: 'Sicilius platformu kullanım şartları, sorumluluk reddi ve hukuki beyanlar.',
};

export default function KullaniciSozlesmesiPage() {
  return (
    <>
      <PublicHeader />
      <main className="container max-w-4xl mx-auto pt-24 pb-12">
        <h1 className="text-3xl font-bold mb-2">Kullanıcı Sözleşmesi</h1>
        <p className="text-sm text-slate-500 dark:text-slate-400 mb-8">Son güncelleme: {new Date().toLocaleDateString('tr-TR')}</p>

        <section className="space-y-4">
          <p>
            Bu Kullanıcı Sözleşmesi ("Sözleşme"), Sicilius Platformu'na ("Platform") erişiminiz ve kullanımınız
            ile ilgili şart ve koşulları düzenler. Platforma erişmekle ya da kullanmakla, bu Sözleşme'yi okuduğunuzu,
            anladığınızı ve hükümlerini kabul ettiğinizi beyan etmiş olursunuz.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">1. Tanımlar</h2>
          <p>
            "Kullanıcı": Platform'a erişen veya Platform'u kullanan gerçek veya tüzel kişiyi ifade eder. "İçerik":
            Platform üzerinden sunulan tüm bilgi, veri, metin, görsel ve diğer materyallerdir.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">2. Kapsam ve Amaç</h2>
          <p>
            Platform; araştırma ve bilgilendirme amacıyla, ağırlıklı olarak halka açık kaynaklar ve ücretsiz platformlardan
            temin edilen verileri derleyerek kullanıcıya sunar. Platform, herhangi bir sektörel, hukuki, mali veya yatırım
            danışmanlığı hizmeti sağlamaz.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">3. Veri Kaynakları ve Doğruluk</h2>
          <p>
            Platformda yer alan bilgiler üçüncü taraf, kamuya açık kaynaklardan derlenmekte olup bilgilendirme amaçlıdır.
            Verilerin doğruluğu, güncelliği ve eksiksizliği konusunda herhangi bir taahhüt verilmez. Kullanıcı, Platformdaki
            bilgileri esas alarak işlem yapmadan önce bilgileri bağımsız olarak doğrulamakla yükümlüdür.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">4. Sorumluluk Reddi</h2>
          <p>
            Kullanıcının Platform üzerindeki bilgilere güvenerek gerçekleştirdiği işlem, karar veya eylemler sonucu doğabilecek
            doğrudan ya da dolaylı zararlar, kâr kaybı veya her türlü kayıptan Platform ve ilişkili kişi/kuruluşlar sorumlu
            tutulamaz.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">5. Fikri Mülkiyet</h2>
          <p>
            Platform ve üzerinde yer alan tüm özgün içerik, tasarım ve yazılımlar ilgili mevzuat kapsamında korunmaktadır.
            Kullanıcı, Platform içeriğini mevzuata uygun biçimde ve yalnızca kişisel kullanım amacıyla görüntüleyebilir;
            izinsiz kopyalama, çoğaltma, dağıtma veya ticari amaçla kullanma haklarına sahip değildir.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">6. Kullanım Koşulları</h2>
          <ul className="list-disc pl-5 space-y-2">
            <li>Platform hukuka, ahlaka ve genel adaba aykırı, yanıltıcı veya üçüncü kişilerin haklarını ihlal eden biçimde kullanılamaz.</li>
            <li>Hesap güvenliği kullanıcı sorumluluğundadır; yetkisiz erişim şüphesinde derhal bildirim yapılmalıdır.</li>
            <li>Platformun çalışmasını engelleyen, aşırı yük bindiren veya sistem güvenliğini ihlal eden faaliyetler yasaktır.</li>
          </ul>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">7. Hesap ve Üyelik</h2>
          <p>
            Üyelik gerektiren hizmetlerde doğru ve güncel bilgi verilmesi zorunludur. Platform, kullanım şartlarını ihlal eden veya
            güvenlik riski oluşturan hesapları kısıtlama veya sonlandırma hakkını saklı tutar.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">8. Gizlilik ve Kişisel Veriler</h2>
          <p>
            Platform, kişisel verileri yürürlükteki mevzuata uygun şekilde işler. Gizlilik ve veri işleme esasları ayrıca ilan edilen
            politika ve aydınlatma metinlerinde açıklanır.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">9. Değişiklik ve Yürürlük</h2>
          <p>
            Platform, bu Sözleşme hükümlerini tek taraflı olarak güncelleyebilir. Güncellenen hükümler yayınlandığı tarihte yürürlüğe
            girer. Kullanıcı, güncellemeleri düzenli olarak takip etmekle yükümlüdür.
          </p>
        </section>

        <section className="mt-8 space-y-3">
          <h2 className="text-xl font-semibold">10. İletişim</h2>
          <p>
            Bu Sözleşme ve Platform kullanımıyla ilgili sorularınız için lütfen iletişime geçin: <a className="underline" href="mailto:legal@sicilius.com.tr">legal@sicilius.com.tr</a>
          </p>
        </section>
      </main>
      <PublicFooter />
    </>
  );
}
