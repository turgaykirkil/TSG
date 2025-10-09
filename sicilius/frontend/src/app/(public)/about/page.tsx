import Image from 'next/image';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import Reveal from '@/components/ui/reveal';
import { Building2, Users, BarChart, Shield, Zap, Lightbulb, Handshake, Award } from 'lucide-react';
// Görseller public klasöründe: /LightTema.png ve /DarkTema.png

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
    <div className="bg-background text-foreground">
      {/* Hero Section */}
      <section className="relative min-h-[calc(100svh-4rem)] md:min-h-[calc(100svh-5rem)] snap-start flex items-center isolate overflow-hidden bg-gradient-to-b from-blue-50/50 dark:from-slate-900/20">
        <div className="mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:flex lg:px-8 lg:py-40">
          <div className="mx-auto max-w-2xl lg:mx-0 lg:max-w-xl lg:flex-shrink-0 lg:pt-8">
            <Reveal>
              <h1 className="mt-10 text-4xl font-bold tracking-tight text-foreground sm:text-6xl">Hakkımızda</h1>
            </Reveal>
            <Reveal delayMs={120}>
              <p className="mt-6 text-lg leading-8 text-foreground/70">
                Sicilius bağımsız ve ücretsiz bir platformdur. Amacımız, kamuya açık kurumsal bilgilere herkes için adil ve kesintisiz erişim sağlamaktır. Hızlı arama, detaylı şirket kartları ve sade bir deneyim sunuyoruz; ticari satış, paket veya kurumsal plan sunmuyoruz.
              </p>
            </Reveal>
            <Reveal delayMs={220}>
              <div className="mt-10 flex items-center gap-x-6">
                <Button asChild size="lg" variant="gradient" className="rounded-lg">
                  <Link href="/davet">Davet ile Katıl</Link>
                </Button>
                <Link href="/contact" className="text-sm font-semibold leading-6">
                  Bizimle İletişime Geçin <span aria-hidden="true">→</span>
                </Link>
              </div>
            </Reveal>
          </div>
          <div>
            <div className="mx-auto mt-16 flex max-w-2xl sm:mt-24 lg:ml-10 lg:mr-0 lg:mt-0 lg:max-w-none lg:flex-none xl:ml-32">
              <div className="max-w-3xl flex-none sm:max-w-5xl lg:max-w-none">
                <div className="-m-2 rounded-xl bg-gray-900/5 dark:bg-white/5 p-2 ring-1 ring-inset ring-gray-900/10 dark:ring-white/10 lg:-m-4 lg:rounded-2xl lg:p-4">
                  <div className="relative w-full max-w-2xl mx-auto overflow-hidden rounded-md">
                    {/* Light tema görseli */}
                    <Image
                      src="/LightTema.png"
                      alt="Sicilius Ekibi — Light Tema"
                      className="block w-full h-auto rounded-md shadow-2xl ring-1 ring-inset ring-gray-900/10 transition-opacity dark:opacity-0"
                      width={832}
                      height={468}
                      sizes="(min-width: 1280px) 832px, (min-width: 1024px) 672px, (min-width: 768px) 640px, 100vw"
                      priority
                    />
                    {/* Dark tema görseli */}
                    <Image
                      src="/DarkTema.png"
                      alt="Sicilius Ekibi — Dark Tema"
                      className="absolute inset-0 w-full h-full object-cover rounded-md shadow-2xl ring-1 ring-inset ring-white/10 opacity-0 dark:opacity-100 transition-opacity"
                      width={832}
                      height={468}
                      sizes="(min-width: 1280px) 832px, (min-width: 1024px) 672px, (min-width: 768px) 640px, 100vw"
                      aria-hidden
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="min-h-[calc(100svh-4rem)] md:min-h-[calc(100svh-5rem)] snap-start flex items-center py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8 w-full">
          <div className="mx-auto max-w-2xl lg:text-center">
            <Reveal>
              <h2 className="text-base font-semibold leading-7 text-primary">Neden Bizi Tercih Etmelisiniz?</h2>
            </Reveal>
            <Reveal delayMs={120}>
              <p className="mt-2 text-3xl font-bold tracking-tight text-foreground sm:text-4xl">İşinizi büyütmenize yardımcı olacak araçlar</p>
            </Reveal>
            <Reveal delayMs={220}>
              <p className="mt-6 text-lg leading-8 text-foreground/70">Sicilius olarak, şirket bilgilerine erişim sürecinizi basitleştiriyor ve hızlandırıyoruz.</p>
            </Reveal>
          </div>
          <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-4xl">
            <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-10 lg:max-w-none lg:grid-cols-3 lg:gap-y-16">
              {features.map((feature, idx) => (
                <Reveal key={feature.name} delayMs={idx * 120} className="relative pl-16">
                  <dt className="text-base font-semibold leading-7 text-foreground">
                    <div className="absolute left-0 top-0 flex h-12 w-12 items-center justify-center rounded-lg bg-primary text-primary-foreground">
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

      {/* Values Section */}
      <section className="min-h-[calc(100svh-4rem)] md:min-h-[calc(100svh-5rem)] snap-start flex items-center py-24 sm:py-32">
        <div className="mx-auto max-w-7xl px-6 lg:px-8 w-full">
          <div className="mx-auto max-w-2xl lg:mx-0">
            <Reveal>
              <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">Değerlerimiz</h2>
            </Reveal>
            <Reveal delayMs={120}>
              <p className="mt-6 text-lg leading-8 text-foreground/70">İş yapış şeklimizi şekillendiren temel değerlerimiz:</p>
            </Reveal>
          </div>
          <dl className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-8 text-base leading-7 text-foreground/70 sm:grid-cols-2 lg:mx-0 lg:max-w-none lg:gap-x-16">
            {values.map((value, idx) => (
              <Reveal key={value.name} delayMs={idx * 120} className="relative pl-9">
                <dt className="inline font-semibold text-foreground">
                  <value.icon className="absolute left-1 top-1 h-5 w-5 text-primary" aria-hidden="true" />
                  {value.name}
                </dt>{' '}
                <dd className="inline">{value.description}</dd>
              </Reveal>
            ))}
          </dl>
        </div>
      </section>

      {/* CTA Section */}
      <section className="snap-start py-24 sm:py-32">
        <div className="container mx-auto px-6">
          <div className="relative isolate overflow-hidden text-center shadow-2xl rounded-3xl ring-1 ring-inset ring-border/50 mx-auto max-w-5xl bg-gradient-to-br from-primary/10 via-background to-secondary/10 dark:from-primary/15 dark:via-slate-900 dark:to-secondary/15 px-8 sm:px-12 md:px-16 py-16 md:py-20">
            <Reveal>
              <h2 className="mx-auto max-w-2xl text-3xl font-bold tracking-tight text-foreground sm:text-4xl">Adil ve Kesintisiz Erişim İçin Birlikteyiz</h2>
            </Reveal>
            <Reveal delayMs={120}>
              <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-foreground/80">Davet bağlantınızla hemen katılın; ücretli paket veya kurumsal plan yok. Sade, hızlı ve ücretsiz.</p>
            </Reveal>
            <Reveal delayMs={220}>
              <div className="mt-10 flex items-center justify-center gap-x-6">
                <Button asChild variant="gradient" className="px-3.5 py-2.5 text-sm font-semibold">
                  <Link href="/davet">Davet ile Katıl</Link>
                </Button>
                <Link href="/contact" className="text-sm font-semibold leading-6 text-primary">
                  İletişime Geçin <span aria-hidden="true">→</span>
                </Link>
              </div>
            </Reveal>
          </div>
        </div>
      </section>
    </div>
  );
}
