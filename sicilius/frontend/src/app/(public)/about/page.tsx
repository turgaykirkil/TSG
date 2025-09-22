import Image from 'next/image';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Building2, Users, BarChart, Shield, Zap, Lightbulb, Handshake, Award } from 'lucide-react';

// Hakkımızda sayfasını yalın ve doğru bilgi verecek şekilde sadeleştirdik.

const features = [
  {
    name: 'Kapsamlı Veri',
    description: 'Milyonlarca şirketin güncel bilgilerine tek platformdan erişin.',
    icon: Building2,
  },
  {
    name: 'Kullanıcı Dostu',
    description: 'Kolay anlaşılır arayüzü ile hızlı ve etkili kullanım.',
    icon: Users,
  },
  {
    name: 'Detaylı Analiz',
    description: 'Güçlü analiz araçları ile şirket verilerini derinlemesine inceleyin.',
    icon: BarChart,
  },
  {
    name: 'Güvenli',
    description: 'En son güvenlik standartları ile verileriniz güvende.',
    icon: Shield,
  },
  {
    name: 'Anlık Güncelleme',
    description: 'Şirket bilgileri sürekli güncel tutulur.',
    icon: Zap,
  },
  {
    name: 'Uzman Kadro',
    description: 'Deneyimli ekibimiz her zaman yanınızda.',
    icon: Users,
  },
];

const values = [
  {
    name: 'Yenilikçilik',
    description: 'Sürekli olarak yeni teknolojileri takip ediyor ve uyguluyoruz.',
    icon: Lightbulb,
  },
  {
    name: 'Güvenilirlik',
    description: 'Müşteri memnuniyetini her şeyin üzerinde tutuyoruz.',
    icon: Shield,
  },
  {
    name: 'İşbirliği',
    description: 'Müşterilerimizle güçlü ve sürdürülebilir ilişkiler kuruyoruz.',
    icon: Handshake,
  },
  {
    name: 'Mükemmellik',
    description: 'En yüksek standartlarda hizmet sunmayı hedefliyoruz.',
    icon: Award,
  },
];

export default function AboutPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <div className="relative isolate overflow-hidden bg-gradient-to-b from-blue-50/50">
        <div className="mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:flex lg:px-8 lg:py-40">
          <div className="mx-auto max-w-2xl lg:mx-0 lg:max-w-xl lg:flex-shrink-0 lg:pt-8">
            <h1 className="mt-10 text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              Hakkımızda
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              Sicilius bağımsız ve ücretsiz bir platformdur. Amacımız, kamuya açık kurumsal bilgilere
              herkes için adil ve kesintisiz erişim sağlamaktır. Hızlı arama, detaylı şirket kartları ve
              sade bir deneyim sunuyoruz; ticari satış, paket veya kurumsal plan sunmuyoruz.
            </p>
            <div className="mt-10 flex items-center gap-x-6">
              <Button asChild size="lg" variant="gradient" className="rounded-lg">
                <Link href="/davet">Davet ile Katıl</Link>
              </Button>
              <Link href="/contact" className="text-sm font-semibold leading-6 text-gray-900">
                Bizimle İletişime Geçin <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
          <div className="mx-auto mt-16 flex max-w-2xl sm:mt-24 lg:ml-10 lg:mr-0 lg:mt-0 lg:max-w-none lg:flex-none xl:ml-32">
            <div className="max-w-3xl flex-none sm:max-w-5xl lg:max-w-none">
              <div className="-m-2 rounded-xl bg-gray-900/5 p-2 ring-1 ring-inset ring-gray-900/10 lg:-m-4 lg:rounded-2xl lg:p-4">
                <Image
                  src="/about-hero.jpg"
                  alt="Sicilius Ekibi"
                  className="w-[76rem] rounded-md shadow-2xl ring-1 ring-inset ring-gray-900/10"
                  width={1216}
                  height={684}
                  priority
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:text-center">
            <h2 className="text-base font-semibold leading-7 text-blue-600">Neden Bizi Tercih Etmelisiniz?</h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              İşinizi büyütmenize yardımcı olacak araçlar
            </p>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              Sicilius olarak, şirket bilgilerine erişim sürecinizi basitleştiriyor ve hızlandırıyoruz.
            </p>
          </div>
          <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
            <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-3 lg:gap-y-16">
              {features.map((feature) => (
                <div key={feature.name} className="relative pl-16">
                  <dt className="text-base font-semibold leading-7 text-gray-900">
                    <div className="absolute left-0 top-0 flex h-12 w-12 items-center justify-center rounded-lg bg-blue-600">
                      <feature.icon className="h-6 w-6 text-white" aria-hidden="true" />
                    </div>
                    {feature.name}
                  </dt>
                  <dd className="mt-2 text-base leading-7 text-gray-600">{feature.description}</dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </div>

      {/* Team Section kaldırıldı: kurgu içerikler temizlendi */}

      {/* Values Section */}
      <div className="py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl lg:mx-0">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Değerlerimiz</h2>
            <p className="mt-6 text-lg leading-8 text-gray-600">
              İş yapış şeklimizi şekillendiren temel değerlerimiz:
            </p>
          </div>
          <dl className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 text-base leading-7 text-gray-600 sm:grid-cols-2 lg:mx-0 lg:max-w-none lg:gap-x-16">
            {values.map((value) => (
              <div key={value.name} className="relative pl-9">
                <dt className="inline font-semibold text-gray-900">
                  <value.icon className="absolute left-1 top-1 h-5 w-5 text-blue-600" aria-hidden="true" />
                  {value.name}
                </dt>{' '}
                <dd className="inline">{value.description}</dd>
              </div>
            ))}
          </dl>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-white py-24 sm:py-32">
        <div className="relative isolate overflow-hidden bg-blue-600 px-6 py-24 text-center shadow-2xl sm:rounded-3xl sm:px-16">
          <h2 className="mx-auto max-w-2xl text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Adil ve Kesintisiz Erişim İçin Birlikteyiz
          </h2>
          <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-blue-100">
            Davet bağlantınızla hemen katılın; ücretli paket veya kurumsal plan yok. Sade, hızlı ve ücretsiz.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <Button asChild variant="gradient" className="px-3.5 py-2.5 text-sm font-semibold">
              <Link href="/davet">Davet ile Katıl</Link>
            </Button>
            <Link href="/contact" className="text-sm font-semibold leading-6 text-white">
              İletişime Geçin <span aria-hidden="true">→</span>
            </Link>
          </div>
          <svg
            viewBox="0 0 1024 1024"
            className="absolute left-1/2 top-1/2 -z-10 h-[64rem] w-[64rem] -translate-x-1/2 [mask-image:radial-gradient(closest-side,white,transparent)]"
            aria-hidden="true"
          >
            <circle cx={512} cy={512} r={512} fill="url(#827591b1-ce8c-4110-b064-7cb85a0b1217)" fillOpacity="0.2" />
            <defs>
              <radialGradient id="827591b1-ce8c-4110-b064-7cb85a0b1217">
                <stop stopColor="#3B82F6" />
                <stop offset={1} stopColor="#1D4ED8" />
              </radialGradient>
            </defs>
          </svg>
        </div>
      </div>
    </div>
  );
}
