'use client';

import Link from 'next/link';
import { Mail, Phone, MapPin, Twitter, Linkedin, Github } from 'lucide-react';

type FooterLink = {
  name: string;
  href: string;
  icon?: React.ReactNode;
};

type FooterSection = {
  title: string;
  links: FooterLink[];
};

export function PublicFooter() {
  const currentYear = new Date().getFullYear();
  
  const footerLinks: FooterSection[] = [
    {
      title: 'Bağlantılar',
      links: [
        { name: 'Anasayfa', href: '/' },
        { name: 'Hakkında', href: '/about' },
        { name: 'İletişim', href: '/contact' },
      ],
    },
    {
      title: 'Yasal',
      links: [
        { name: 'Gizlilik Politikası', href: '/privacy' },
        { name: 'Kullanım Şartları', href: '/terms' },
        { name: 'Çerez Politikası', href: '/cookies' },
      ],
    },
    {
      title: 'İletişim',
      links: [
        { 
          name: 'info@tsgplatform.com', 
          href: 'mailto:info@tsgplatform.com',
          icon: <Mail className="w-4 h-4 mr-2" />
        },
        { 
          name: '+90 555 123 45 67', 
          href: 'tel:+905551234567',
          icon: <Phone className="w-4 h-4 mr-2" />
        },
        { 
          name: 'İstanbul, Türkiye', 
          href: 'https://maps.google.com',
          icon: <MapPin className="w-4 h-4 mr-2" />
        },
      ],
    },
  ];

  const socialLinks = [
    {
      name: 'Twitter',
      href: 'https://twitter.com',
      icon: <Twitter className="w-5 h-5" />,
    },
    {
      name: 'LinkedIn',
      href: 'https://linkedin.com',
      icon: <Linkedin className="w-5 h-5" />,
    },
    {
      name: 'GitHub',
      href: 'https://github.com',
      icon: <Github className="w-5 h-5" />,
    },
  ];

  return (
    <footer className="relative overflow-hidden bg-background border-t border-border/50">
      {/* Gradient background */}
      <div className="absolute inset-0 overflow-hidden opacity-10">
        <div className="absolute -top-1/2 left-1/2 w-[800px] h-[800px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-gradient-to-r from-primary/20 to-secondary/20 blur-3xl"></div>
      </div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
          {/* Logo and description */}
          <div className="space-y-5">
            <div className="flex items-center space-x-2">
              <span className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                TSG Platform
              </span>
            </div>
            <p className="text-foreground/70 text-sm leading-relaxed">
              Şirket bilgilerine kolay erişim için güçlü ve kullanıcı dostu bir platform.
            </p>
            
            {/* Social links */}
            <div className="flex space-x-4 pt-2">
              {socialLinks.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-foreground/60 hover:text-primary transition-colors"
                  aria-label={item.name}
                >
                  {item.icon}
                </Link>
              ))}
            </div>
          </div>
          
          {/* Footer links */}
          {footerLinks.map((section) => (
            <div key={section.title}>
              <h3 className="text-sm font-semibold text-foreground/90 mb-4">
                {section.title}
              </h3>
              <ul className="space-y-3">
                {section.links.map((item) => (
                  <li key={item.name}>
                    <Link
                      href={item.href}
                      className="flex items-center text-sm text-foreground/60 hover:text-primary transition-colors group"
                    >
                      {item.icon && (
                        <span className="mr-2 group-hover:translate-x-0.5 transition-transform">
                          {item.icon}
                        </span>
                      )}
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        
        {/* Divider */}
        <div className="border-t border-border/30 my-12"></div>
        
        {/* Bottom bar */}
        <div className="flex flex-col md:flex-row justify-between items-center pt-4">
          <p className="text-sm text-foreground/60 text-center md:text-left">
            &copy; {currentYear} TSG Platform. Tüm hakları saklıdır.
          </p>
          
          <div className="flex items-center space-x-6 mt-4 md:mt-0">
            <Link href="/privacy" className="text-sm text-foreground/60 hover:text-primary transition-colors">
              Gizlilik Politikası
            </Link>
            <Link href="/terms" className="text-sm text-foreground/60 hover:text-primary transition-colors">
              Kullanım Şartları
            </Link>
          </div>
        </div>
      </div>
      
      {/* Decorative elements */}
      <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-primary via-secondary to-primary opacity-30"></div>
    </footer>
  );
}
