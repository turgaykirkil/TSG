import Link from 'next/link';

export default function SSSPage() {
  return (
    <div className="container mx-auto max-w-3xl px-6 py-12">
      <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100">Sıkça Sorulan Sorular</h1>
      <p className="mt-2 text-gray-600 dark:text-gray-300">
        Sicilius hakkında en çok merak edilen soruları ve yanıtlarını burada bulabilirsiniz.
      </p>

      <div className="mt-8 space-y-3">
        <details className="group rounded-lg border border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-slate-900">
          <summary className="cursor-pointer select-none text-sm font-medium text-gray-900 dark:text-gray-100 flex items-center justify-between">
            Günlük sorgu limiti nedir? Neden uygulanıyor?
            <span className="ml-2 text-gray-500 group-open:rotate-180 transition-transform">▾</span>
          </summary>
          <div className="mt-2 text-sm leading-6 text-gray-700 dark:text-gray-300">
            Sicilius, herkes için adil ve kesintisiz erişimi korumak amacıyla günlük bir sorgu sınırı uygular. Bu sınır
            sistemlerimizin kararlı ve hızlı çalışmasına yardımcı olur. Limitler her gece otomatik olarak sıfırlanır.
          </div>
        </details>

        <details className="group rounded-lg border border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-slate-900">
          <summary className="cursor-pointer select-none text-sm font-medium text-gray-900 dark:text-gray-100 flex items-center justify-between">
            Hangi işlemler limiti tüketir?
            <span className="ml-2 text-gray-500 group-open:rotate-180 transition-transform">▾</span>
          </summary>
          <div className="mt-2 text-sm leading-6 text-gray-700 dark:text-gray-300">
            Arama yapmak limitinizi tüketmez. Bir şirketin detay sayfasını (modali) açtığınızda limitiniz 1 azalır.
          </div>
        </details>

        <details className="group rounded-lg border border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-slate-900">
          <summary className="cursor-pointer select-none text-sm font-medium text-gray-900 dark:text-gray-100 flex items-center justify-between">
            Üyelik davetle mi çalışıyor?
            <span className="ml-2 text-gray-500 group-open:rotate-180 transition-transform">▾</span>
          </summary>
          <div className="mt-2 text-sm leading-6 text-gray-700 dark:text-gray-300">
            Evet. Sicilius, davetle üyelik sistemine sahiptir. Davet bağlantınızı kullanarak e-posta doğrulaması ve şifre
            belirleme adımlarıyla hesabınızı oluşturabilirsiniz.
          </div>
        </details>

        <details className="group rounded-lg border border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-slate-900">
          <summary className="cursor-pointer select-none text-sm font-medium text-gray-900 dark:text-gray-100 flex items-center justify-between">
            Sicilius ücretli mi?
            <span className="ml-2 text-gray-500 group-open:rotate-180 transition-transform">▾</span>
          </summary>
          <div className="mt-2 text-sm leading-6 text-gray-700 dark:text-gray-300">
            Hayır. Sicilius bağımsız ve ücretsiz bir platformdur. Bilgiye erişiminizi adil ve kesintisiz biçimde
            sürdürebilmek için günlük bir sınır uygularız.
          </div>
        </details>

        <details className="group rounded-lg border border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-slate-900">
          <summary className="cursor-pointer select-none text-sm font-medium text-gray-900 dark:text-gray-100 flex items-center justify-between">
            Verilerim güvende mi?
            <span className="ml-2 text-gray-500 group-open:rotate-180 transition-transform">▾</span>
          </summary>
          <div className="mt-2 text-sm leading-6 text-gray-700 dark:text-gray-300">
            Güvenlik ve gizlilik önceliğimizdir. Hesap ve oturum bilgileriniz güvenli çerezlerle korunur. Ayrıntılar için
            <Link href="/gizlilik-politikasi" className="ml-1 rounded px-1 -mx-1 hover:bg-gray-100 dark:hover:bg-slate-800">Gizlilik Politikası</Link> ve
            <Link href="/kullanici-sozlesmesi" className="ml-1 rounded px-1 -mx-1 hover:bg-gray-100 dark:hover:bg-slate-800">Kullanıcı Sözleşmesi</Link> sayfalarına göz atabilirsiniz.
          </div>
        </details>

        <details className="group rounded-lg border border-gray-200 dark:border-gray-700 p-4 bg-white dark:bg-slate-900">
          <summary className="cursor-pointer select-none text-sm font-medium text-gray-900 dark:text-gray-100 flex items-center justify-between">
            Size nasıl geri bildirim verebilirim?
            <span className="ml-2 text-gray-500 group-open:rotate-180 transition-transform">▾</span>
          </summary>
          <div className="mt-2 text-sm leading-6 text-gray-700 dark:text-gray-300">
            Görüş ve önerileriniz bizim için değerli. Lütfen <Link href="/contact" className="rounded px-1 -mx-1 hover:bg-gray-100 dark:hover:bg-slate-800">İletişim</Link> sayfasından bize yazın.
          </div>
        </details>
      </div>
    </div>
  );
}
