'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import Reveal from '@/components/ui/reveal';

const faqs = [
    {
        q: 'Günlük sorgu limiti nedir? Neden uygulanıyor?',
        a: (
            <>
                Sicilius, herkes için adil ve kesintisiz erişimi korumak amacıyla günlük bir sorgu sınırı uygular.
                Bu sınır sistemlerimizin kararlı ve hızlı çalışmasına yardımcı olur. Limitler her gece otomatik olarak sıfırlanır.
            </>
        ),
    },
    {
        q: 'Hangi işlemler limiti tüketir?',
        a: <>Arama yapmak limitinizi tüketmez. Bir şirketin detay sayfasını açtığınızda limitiniz 1 azalır.</>,
    },
    {
        q: 'Üyelik davetle mi çalışıyor?',
        a: <>Evet. Sicilius, davetle üyelik sistemine sahiptir. Davet bağlantınızı kullanarak e-posta doğrulaması ve şifre belirleme adımlarıyla hesabınızı oluşturabilirsiniz.</>,
    },
    {
        q: 'Sicilius ücretli mi?',
        a: <>Hayır. Sicilius bağımsız ve ücretsiz bir platformdur. Bilgiye erişiminizi adil ve kesintisiz biçimde sürdürebilmek için günlük bir sınır uygularız.</>,
    },
    {
        q: 'Verilerim güvende mi?',
        a: (
            <>
                Güvenlik ve gizlilik önceliğimizdir. Hesap ve oturum bilgileriniz güvenli çerezlerle korunur. Ayrıntılar için
                <Link href="/gizlilik-politikasi" className="ml-1 rounded px-1 -mx-1 hover:bg-muted">Gizlilik Politikası</Link> ve
                <Link href="/kullanici-sozlesmesi" className="ml-1 rounded px-1 -mx-1 hover:bg-muted">Kullanıcı Sözleşmesi</Link> sayfalarına göz atabilirsiniz.
            </>
        ),
    },
    {
        q: 'Size nasıl geri bildirim verebilirim?',
        a: <>Görüş ve önerileriniz bizim için değerli. Lütfen <Link href="/contact" className="rounded px-1 -mx-1 hover:bg-muted">İletişim</Link> sayfasından bize yazın.</>,
    },
];

type ItemProps = {
    index: number;
    openIndex: number | null;
    setOpenIndex: (i: number | null) => void;
    q: string;
    a: React.ReactNode;
};

function AccordionItem({ index, openIndex, setOpenIndex, q, a }: ItemProps) {
    const open = openIndex === index;

    return (
        <div
            className={
                'rounded-lg border transition-colors duration-500 ease-out ' +
                (open
                    ? 'bg-gradient-to-br from-primary/10 to-secondary/10 dark:from-primary/15 dark:to-secondary/15 border-primary/30 shadow-md ring-1 ring-inset ring-primary/20'
                    : 'bg-card border-border')
            }
        >
            <button
                className="w-full px-4 py-3 flex items-center justify-between text-left text-sm font-medium text-foreground"
                aria-expanded={open}
                aria-controls={`faq-panel-${index}`}
                onClick={() => setOpenIndex(open ? null : index)}
            >
                {q}
                <span className={'ml-2 transition-transform duration-500 text-muted-foreground ' + (open ? 'rotate-180' : '')}>▾</span>
            </button>

            <div
                id={`faq-panel-${index}`}
                className={
                    'px-4 grid transition-[grid-template-rows,opacity] duration-500 ease-out ' +
                    (open ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0')
                }
                style={{ willChange: 'opacity' }}
            >
                <div className="overflow-hidden">
                    <div className="py-3 text-sm leading-6 text-foreground/80">
                        {a}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default function SSSClient() {
    const [openIndex, setOpenIndex] = useState<number | null>(null);

    return (
        <section className="snap-start bg-background py-16 md:py-20">
            <div className="container max-w-3xl px-6 text-foreground">
                <Reveal>
                    <h1 className="text-3xl font-bold tracking-tight">Sıkça Sorulan Sorular</h1>
                </Reveal>
                <Reveal delayMs={120}>
                    <p className="mt-2 text-foreground/80">Kurumsal veri analizleri, üyelik süreçleri ve platform kullanımı hakkında en çok merak edilenlere buradan ulaşın.</p>
                </Reveal>

                <div className="mt-8 space-y-3">
                    {faqs.map((item, i) => (
                        <Reveal key={item.q} delayMs={i * 80}>
                            <AccordionItem
                                index={i}
                                openIndex={openIndex}
                                setOpenIndex={setOpenIndex}
                                q={item.q}
                                a={item.a}
                            />
                        </Reveal>
                    ))}
                </div>
            </div>
        </section>
    );
}
