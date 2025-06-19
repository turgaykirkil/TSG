import { Button } from '@/components/ui/button';

export default function ContactPage() {
  return (
    <div className="bg-white py-16 sm:py-24">
      <div className="mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl space-y-16 sm:space-y-20 lg:mx-0 lg:max-w-none">
          <div>
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">İletişim</h2>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              Sorularınız, önerileriniz veya geri bildirimleriniz için bizimle iletişime geçebilirsiniz.
            </p>
          </div>
          
          <div className="grid grid-cols-1 gap-x-8 gap-y-12 sm:grid-cols-2 lg:grid-cols-4">
            <div className="sm:col-span-2">
              <h3 className="text-base font-semibold text-gray-900">Bize Ulaşın</h3>
              <dl className="mt-6 space-y-3 text-sm leading-6 text-gray-600">
                <div>
                  <dt className="sr-only">Email</dt>
                  <dd>
                    <a className="font-semibold text-indigo-600" href="mailto:info@tsgplatform.com">info@tsgplatform.com</a>
                  </dd>
                </div>
                <div className="mt-1">
                  <dt className="sr-only">Telefon</dt>
                  <dd>+90 212 123 45 67</dd>
                </div>
                <div className="mt-1">
                  <dt className="sr-only">Adres</dt>
                  <dd>
                    <address className="not-italic">
                      Levent Mahallesi, Büyükdere Caddesi<br />
                      No:123 Kat:5<br />
                      Şişli/İstanbul, 34330
                    </address>
                  </dd>
                </div>
              </dl>
            </div>
            
            <div className="sm:col-span-2">
              <h3 className="text-base font-semibold text-gray-900">Çalışma Saatlerimiz</h3>
              <dl className="mt-6 space-y-3 text-sm leading-6 text-gray-600">
                <div className="flex justify-between">
                  <dt>Pazartesi—Cuma</dt>
                  <dd className="text-gray-900">09:00 - 18:00</dd>
                </div>
                <div className="flex justify-between">
                  <dt>Cumartesi</dt>
                  <dd className="text-gray-900">10:00 - 15:00</dd>
                </div>
                <div className="flex justify-between">
                  <dt>Pazar</dt>
                  <dd className="text-gray-900">Kapalı</dd>
                </div>
              </dl>
            </div>
          </div>
          
          <div className="border-t border-gray-200 pt-8">
            <h3 className="text-base font-semibold text-gray-900">Bize Yazın</h3>
            <form action="#" method="POST" className="mt-6 grid grid-cols-1 gap-x-8 gap-y-6 sm:grid-cols-2">
              <div>
                <label htmlFor="first-name" className="block text-sm font-semibold leading-6 text-gray-900">
                  Adınız
                </label>
                <div className="mt-2.5">
                  <input
                    type="text"
                    name="first-name"
                    id="first-name"
                    autoComplete="given-name"
                    className="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  />
                </div>
              </div>
              <div>
                <label htmlFor="last-name" className="block text-sm font-semibold leading-6 text-gray-900">
                  Soyadınız
                </label>
                <div className="mt-2.5">
                  <input
                    type="text"
                    name="last-name"
                    id="last-name"
                    autoComplete="family-name"
                    className="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  />
                </div>
              </div>
              <div className="sm:col-span-2">
                <label htmlFor="email" className="block text-sm font-semibold leading-6 text-gray-900">
                  E-posta Adresiniz
                </label>
                <div className="mt-2.5">
                  <input
                    type="email"
                    name="email"
                    id="email"
                    autoComplete="email"
                    className="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  />
                </div>
              </div>
              <div className="sm:col-span-2">
                <label htmlFor="subject" className="block text-sm font-semibold leading-6 text-gray-900">
                  Konu
                </label>
                <div className="mt-2.5">
                  <input
                    type="text"
                    name="subject"
                    id="subject"
                    className="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  />
                </div>
              </div>
              <div className="sm:col-span-2">
                <label htmlFor="message" className="block text-sm font-semibold leading-6 text-gray-900">
                  Mesajınız
                </label>
                <div className="mt-2.5">
                  <textarea
                    name="message"
                    id="message"
                    rows={4}
                    className="block w-full rounded-md border-0 px-3.5 py-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    defaultValue={''}
                  />
                </div>
              </div>
              <div className="sm:col-span-2">
                <Button type="submit" className="w-full sm:w-auto">
                  Gönder
                </Button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
