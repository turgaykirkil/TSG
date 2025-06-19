'use client';

import Link from 'next/link';
import { ArrowRight, BarChart3, ShieldCheck, Zap, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function HomePage() {
  const features = [
    {
      icon: <BarChart3 className="w-6 h-6" />,
      title: 'Detaylı Analiz',
      description: 'Şirket verilerini detaylı bir şekilde analiz edin ve anlamlı içgörüler elde edin.'
    },
    {
      icon: <ShieldCheck className="w-6 h-6" />,
      title: 'Güvenli Veri',
      description: 'Verileriniz en yüksek güvenlik standartlarıyla korunmaktadır.'
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: 'Hızlı Erişim',
      description: 'İhtiyacınız olan bilgilere hızlı ve kolay bir şekilde ulaşın.'
    },
    {
      icon: <Users className="w-6 h-6" />,
      title: 'Kullanıcı Dostu',
      description: 'Kolay kullanımlı arayüzü ile işlerinizi hızla halledin.'
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-32 pb-20 md:pt-40">
        {/* Gradient background */}
        <div className="absolute inset-0 overflow-hidden -z-10">
          <div className="absolute -top-1/2 left-1/2 w-[1200px] h-[1200px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-gradient-to-r from-primary/10 via-secondary/10 to-primary/10 blur-3xl"></div>
        </div>
        
        <div className="container px-4 mx-auto relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-6">
              <span className="relative flex h-2 w-2 mr-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
              </span>
              Yeni güncellemeler yayınlandı
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6 leading-tight">
              Şirket Bilgileriniz <span className="bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">Tek Platformda</span>
            </h1>
            
            <p className="text-xl text-foreground/70 mb-10 max-w-2xl mx-auto">
              TSG Platform ile şirket bilgilerinizi kolayca yönetin, analiz edin ve raporlayın. 
              İş süreçlerinizi hızlandırmak için güçlü araçlarla donatıldık.
            </p>
            
            <div className="flex flex-col sm:flex-row justify-center gap-4 mb-16">
              <Link href="/register">
                <Button className="gradient-primary px-8 py-6 text-lg font-medium hover:shadow-primary/40 transition-all">
                  Ücretsiz Başla
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/about">
                <Button variant="outline" className="px-8 py-6 text-lg font-medium">
                  Daha Fazla Bilgi
                </Button>
              </Link>
            </div>
            
            <div className="flex justify-center">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-primary/30 to-secondary/30 rounded-2xl blur-2xl -z-10"></div>
                <div className="relative bg-background/80 backdrop-blur-sm p-1 rounded-2xl border border-border/50 shadow-lg">
                  <div className="h-64 w-full bg-muted rounded-xl overflow-hidden">
                    <div className="h-full w-full bg-gradient-to-br from-primary/10 to-secondary/10 flex items-center justify-center">
                      <p className="text-foreground/50">Dashboard Önizlemesi</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-muted/30">
        <div className="container px-4 mx-auto">
          <div className="max-w-2xl mx-auto text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">Neden Bizi Tercih Etmelisiniz?</h2>
            <p className="text-foreground/70">İşletmenizi bir sonraki seviyeye taşımak için ihtiyacınız olan tüm araçlar tek bir platformda</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div 
                key={index}
                className="bg-background rounded-xl p-6 border border-border/30 hover:border-primary/30 transition-all hover:shadow-lg hover:-translate-y-1"
              >
                <div className="w-12 h-12 rounded-lg bg-primary/10 text-primary flex items-center justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-lg font-semibold text-foreground mb-2">{feature.title}</h3>
                <p className="text-foreground/60">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container px-4 mx-auto">
          <div className="bg-gradient-to-r from-primary/5 via-background to-secondary/5 rounded-2xl p-8 md:p-12 border border-border/30">
            <div className="max-w-3xl mx-auto text-center">
              <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-6">Hemen Ücretsiz Başlayın</h2>
              <p className="text-foreground/70 text-lg mb-8">
                TSG Platform'un sunduğu tüm özellikleri keşfedin ve iş süreçlerinizi optimize etmeye bugün başlayın.
              </p>
              <div className="flex flex-col sm:flex-row justify-center gap-4">
                <Link href="/register">
                  <Button className="gradient-primary px-8 py-6 text-lg font-medium hover:shadow-primary/40 transition-all">
                    Ücretsiz Kayıt Ol
                  </Button>
                </Link>
                <Link href="/contact">
                  <Button variant="outline" className="px-8 py-6 text-lg font-medium">
                    İletişime Geçin
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
