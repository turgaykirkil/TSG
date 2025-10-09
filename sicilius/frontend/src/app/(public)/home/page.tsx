import Image from 'next/image';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import Reveal from '@/components/ui/reveal';
import { Search, BarChart, Shield, Zap, Users, FileText, CheckCircle2 } from 'lucide-react';

const features = [
  {
    name: 'Hızlı Arama',
    description: 'Şirket adı, vergi no veya sicil no ile anında arama yapın.',
    icon: Search,
  },
  {
    name: 'Detaylı Analiz',
    description: 'Şirket verilerini detaylı bir şekilde analiz edin ve karşılaştırın.',
    icon: BarChart,
  },
  {
    name: 'Güvenli Veri',
    description: 'Verileriniz 256-bit şifreleme ile güvende.',
    icon: Shield,
  },
  {
    name: 'Anlık Güncellemeler',
    description: 'Şirket bilgileri anlık olarak güncellenir.',
    icon: Zap,
  },
  {
    name: 'İlişki Haritası',
    description: 'Şirketler arasındaki ilişkileri görselleştirin.',
    icon: Users,
  },
  {
    name: 'Detaylı Raporlar',
    description: 'Özelleştirilebilir raporlar oluşturun ve dışa aktarın.',
    icon: FileText,
  },
];

export default function HomePage() {
  return (
    <div className="bg-background text-foreground">
      {/* Hero Section */}
      <section className="relative min-h-[calc(100svh-4rem)] md:min-h-[calc(100svh-5rem)] snap-start flex items-center isolate overflow-hidden bg-gradient-to-b from-blue-50/50 dark:from-slate-900/20">
        <div className="mx-auto max-w-7xl px-6 pb-24 pt-10 sm:pb-32 lg:flex lg:px-8 lg:py-40 w-full">
          <div className="mx-auto max-w-2xl lg:mx-0 lg:max-w-xl lg:flex-shrink-0 lg:pt-8">
            <Reveal>
              <div className="mt-24 sm:mt-32 lg:mt-16">
                <span className="rounded-full bg-primary/10 px-3 py-1 text-sm font-semibold leading-6 text-primary ring-1 ring-inset ring-primary/10">
                  Yeni sürüm yayınlandı
                </span>
              </div>
            </Reveal>
            <Reveal delayMs={120}>
              <h1 className="mt-10 text-4xl font-bold tracking-tight sm:text-6xl">
                Şirket Bilgilerine Hızlı ve Güvenli Erişim
              </h1>
            </Reveal>
            <Reveal delayMs={220}>
              <p className="mt-6 text-lg leading-8 text-foreground/70">
                Sicilius ile şirket bilgilerini kolayca görüntüleyin, analiz edin ve raporlayın.
                Ticaret Sicil Gazetesi kayıtlarına tek bir yerden erişin.
              </p>
            </Reveal>
            <Reveal delayMs={320}>
              <div className="mt-10 flex items-center gap-x-6">
                <Button asChild size="lg" variant="gradient" className="rounded-lg">
                  <Link href="/davet">Davet ile Katıl</Link>
                </Button>
                <Link href="/about" className="text-sm font-semibold leading-6">
                  Daha fazla bilgi <span aria-hidden="true">→</span>
                </Link>
                <Link href="/sss" className="text-sm font-semibold leading-6">
                  SSS <span aria-hidden="true">→</span>
                </Link>
              </div>
            </Reveal>
          </div>
          <Reveal delayMs={300}>
            <div className="mx-auto mt-16 flex max-w-2xl sm:mt-24 lg:ml-10 lg:mr-0 lg:mt-0 lg:max-w-none lg:flex-none xl:ml-32">
              <div className="max-w-3xl flex-none sm:max-w-5xl lg:max-w-none">
                <div className="-m-2 rounded-xl bg-gray-900/5 dark:bg-white/5 p-2 ring-1 ring-inset ring-gray-900/10 dark:ring-white/10 lg:-m-4 lg:rounded-2xl lg:p-4">
                  <Image
                    src="/dashboard-preview.png"
                    alt="Sicilius Dashboard Önizleme"
                    className="w-[76rem] rounded-md shadow-2xl ring-1 ring-inset ring-gray-900/10 dark:ring-white/10"
                    width={1216}
                    height={720}
                    priority
                  />
                </div>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* Features Section */}
      <section className="min-h-[calc(100svh-4rem)] md:min-h-[calc(100svh-5rem)] snap-start flex items-center py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8 w-full">
          <div className="mx-auto max-w-2xl lg:text-center">
            <Reveal>
              <h2 className="text-base font-semibold leading-7 text-primary">Daha hızlı, daha iyi</h2>
            </Reveal>
            <Reveal delayMs={120}>
              <p className="mt-2 text-3xl font-bold tracking-tight sm:text-4xl">İşinizi kolaylaştıran tüm araçlar</p>
            </Reveal>
            <Reveal delayMs={220}>
              <p className="mt-6 text-lg leading-8 text-foreground/70">
                Sicilius, şirket bilgilerine erişim sürecinizi basitleştirir ve hızlandırır. İşte size sunduğumuz bazı özellikler:
              </p>
            </Reveal>
          </div>
          <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
            <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-2 lg:gap-y-16">
              {features.map((feature, idx) => (
                <Reveal key={feature.name} delayMs={idx * 120} className="relative pl-16">
                  <dt className="text-base font-semibold leading-7">
                    <div className="absolute left-0 top-0 flex h-10 w-10 items-center justify-center rounded-lg bg-primary text-primary-foreground">
                      <feature.icon className="h-6 w-6" aria-hidden="true" />
                    </div>
                    {feature.name}
                  </dt>
                  <dd className="mt-2 text-base leading-7 text-foreground/70">{feature.description}</dd>
                </Reveal>
              ))}
            </dl>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="snap-start py-16 sm:py-24">
        <div className="relative isolate">
          <div className="mx-auto max-w-7xl sm:px-6 lg:px-8">
            <div className="mx-auto flex max-w-2xl flex-col gap-16 bg-white/5 dark:bg-white/5 px-6 py-16 ring-1 ring-inset ring-gray-900/10 dark:ring-white/10 sm:rounded-3xl sm:p-8 lg:mx-0 lg:max-w-none lg:flex-row lg:items-center lg:py-20 xl:gap-x-20 xl:px-20">
              <div className="w-full flex-auto">
                <Reveal>
                  <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">Hemen başlayın, 14 gün ücretsiz deneyin</h2>
                </Reveal>
                <Reveal delayMs={120}>
                  <p className="mt-6 text-lg leading-8 text-foreground/70">
                    Sicilius'un tüm özelliklerini 14 gün boyunca ücretsiz deneyin. Kredi kartı bilgisi gerekmez.
                  </p>
                </Reveal>
                <Reveal delayMs={220}>
                  <div className="mt-10 flex items-center gap-x-6">
                    <Button asChild size="lg" variant="gradient" className="rounded-lg">
                      <Link href="/davet">Davet ile Katıl</Link>
                    </Button>
                    <Link href="/contact" className="text-sm font-semibold leading-6">
                      Bize ulaşın <span aria-hidden="true">→</span>
                    </Link>
                  </div>
                </Reveal>
              </div>
              <div className="flex-none">
                <ul role="list" className="grid gap-x-8 gap-y-10">
                  {[
                    '14 gün ücretsiz deneme',
                    'Kredi kartı gerekmez',
                    'İptal her zaman ücretsiz',
                    '7/24 destek',
                    'Veri güvenliği garantisi',
                  ].map((feature, idx) => (
                    <Reveal key={feature} delayMs={idx * 100}>
                      <li className="flex gap-x-3">
                        <CheckCircle2 className="h-6 w-5 flex-none text-primary" aria-hidden="true" />
                        <span className="text-sm leading-6 text-foreground/80">{feature}</span>
                      </li>
                    </Reveal>
                  ))}
                </ul>
              </div>
            </div>
          </div>
          <div className="absolute inset-x-0 -top-16 -z-10 flex transform-gpu justify-center overflow-hidden blur-3xl" aria-hidden="true">
            <div
              className="aspect-[1318/752] w-[82.375rem] flex-none bg-gradient-to-r from-[#80caff] to-[#4f46e5] opacity-25"
              style={{
                clipPath:
                  'polygon(73.6% 51.7%, 91.7% 11.8%, 100% 46.4%, 97.4% 82.2%, 92.5% 84.9%, 75.7% 64%, 55.3% 47.5%, 46.5% 49.4%, 45% 62.9%, 50.3% 87.2%, 21.3% 64.1%, 0.1% 100%, 5.4% 51.1%, 21.4% 63.9%, 58.9% 0.2%, 73.6% 51.7%)',
              }}
            />
          </div>
        </div>
      </section>
    </div>
  );
}
