'use client';

import { Button } from '@/components/ui/button';
import Reveal from '@/components/ui/reveal';
import { useState, useRef } from 'react';
import { useToast } from '@/components/ui/use-toast';

export default function ContactPage() {
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();
  const formRef = useRef<HTMLFormElement>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData(e.currentTarget);
    const data = {
      first_name: formData.get('first-name') as string,
      last_name: formData.get('last-name') as string,
      email: formData.get('email') as string,
      subject: formData.get('subject') as string,
      message: formData.get('message') as string,
    };

    try {
      const res = await fetch('http://localhost:5001/api/v1/contact/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(data),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData?.detail || 'Mesaj gönderilemedi');
      }

      toast({
        title: 'Başarılı!',
        description: 'Mesajınız başarıyla gönderildi. En kısa sürede size dönüş yapacağız.',
      });

      // Reset form
      formRef.current?.reset();
    } catch (error: any) {
      toast({
        title: 'Hata',
        description: error?.message || 'Mesaj gönderilirken bir hata oluştu. Lütfen tekrar deneyin.',
        variant: 'destructive',
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="min-h-[calc(100svh-4rem)] md:min-h-[calc(100svh-5rem)] snap-start flex items-center bg-background py-16 sm:py-24">
      <div className="mx-auto max-w-5xl px-6 lg:px-8 w-full text-foreground">
        <div className="mx-auto max-w-2xl space-y-16 sm:space-y-20 lg:mx-0 lg:max-w-none">
          <div>
            <Reveal>
              <h2 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">İletişim</h2>
            </Reveal>
            <Reveal delayMs={120}>
              <p className="mt-6 text-lg leading-8 text-foreground/70">
                Sorularınız, önerileriniz veya geri bildirimleriniz için bizimle iletişime geçebilirsiniz.
              </p>
            </Reveal>
          </div>

          <div className="flex justify-center">

            <div className="w-full max-w-2xl">
              <Reveal>
                <h3 className="text-base font-semibold text-foreground">Bize Yazın</h3>
              </Reveal>
              <Reveal delayMs={120}>
                <form ref={formRef} onSubmit={handleSubmit} className="mt-6 grid grid-cols-1 gap-x-8 gap-y-6 sm:grid-cols-2">
                  <div>
                    <label htmlFor="first-name" className="block text-sm font-semibold leading-6 text-foreground">
                      Adınız
                    </label>
                    <div className="mt-2.5">
                      <input
                        type="text"
                        name="first-name"
                        id="first-name"
                        required
                        autoComplete="given-name"
                        className="block w-full rounded-md border-0 px-3.5 py-2 text-foreground shadow-sm ring-1 ring-inset ring-border placeholder:text-muted-foreground focus:ring-2 focus:ring-inset focus:ring-ring sm:text-sm sm:leading-6 bg-background"
                      />
                    </div>
                  </div>
                  <div>
                    <label htmlFor="last-name" className="block text-sm font-semibold leading-6 text-foreground">
                      Soyadınız
                    </label>
                    <div className="mt-2.5">
                      <input
                        type="text"
                        name="last-name"
                        id="last-name"
                        required
                        autoComplete="family-name"
                        className="block w-full rounded-md border-0 px-3.5 py-2 text-foreground shadow-sm ring-1 ring-inset ring-border placeholder:text-muted-foreground focus:ring-2 focus:ring-inset focus:ring-ring sm:text-sm sm:leading-6 bg-background"
                      />
                    </div>
                  </div>
                  <div className="sm:col-span-2">
                    <label htmlFor="email" className="block text-sm font-semibold leading-6 text-foreground">
                      E-posta Adresiniz
                    </label>
                    <div className="mt-2.5">
                      <input
                        type="email"
                        name="email"
                        id="email"
                        required
                        autoComplete="email"
                        className="block w-full rounded-md border-0 px-3.5 py-2 text-foreground shadow-sm ring-1 ring-inset ring-border placeholder:text-muted-foreground focus:ring-2 focus:ring-inset focus:ring-ring sm:text-sm sm:leading-6 bg-background"
                      />
                    </div>
                  </div>
                  <div className="sm:col-span-2">
                    <label htmlFor="subject" className="block text-sm font-semibold leading-6 text-foreground">
                      Konu
                    </label>
                    <div className="mt-2.5">
                      <input
                        type="text"
                        name="subject"
                        id="subject"
                        required
                        className="block w-full rounded-md border-0 px-3.5 py-2 text-foreground shadow-sm ring-1 ring-inset ring-border placeholder:text-muted-foreground focus:ring-2 focus:ring-inset focus:ring-ring sm:text-sm sm:leading-6 bg-background"
                      />
                    </div>
                  </div>
                  <div className="sm:col-span-2">
                    <label htmlFor="message" className="block text-sm font-semibold leading-6 text-foreground">
                      Mesajınız
                    </label>
                    <div className="mt-2.5">
                      <textarea
                        name="message"
                        id="message"
                        rows={4}
                        required
                        className="block w-full rounded-md border-0 px-3.5 py-2 text-foreground shadow-sm ring-1 ring-inset ring-border placeholder:text-muted-foreground focus:ring-2 focus:ring-inset focus:ring-ring sm:text-sm sm:leading-6 bg-background"
                      />
                    </div>
                  </div>
                  <div className="sm:col-span-2">
                    <Button type="submit" variant="gradient" className="w-full sm:w-auto" disabled={loading}>
                      {loading ? 'Gönderiliyor...' : 'Gönder'}
                    </Button>
                  </div>
                </form>
              </Reveal>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
