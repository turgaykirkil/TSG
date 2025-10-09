'use client';

import Link from 'next/link';
import { Twitter, Linkedin, Github } from 'lucide-react';
import { SiciliusLogo as Logo } from '@/components/icons/SiciliusLogo';

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
        { name: 'SSS', href: '/sss' },
        { name: 'İletişim', href: '/contact' },
      ],
    },
    {
      title: 'Yasal',
      links: [
        { name: 'Gizlilik Politikası', href: '/gizlilik-politikasi' },
        { name: 'Kullanıcı Sözleşmesi', href: '/kullanici-sozlesmesi' },
        { name: 'Çerez Politikası', href: '/cerez-politikasi' },
        { name: 'KVKK Aydınlatma', href: '/kvkk-aydinlatma' },
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
    <footer data-testid="public-footer" className="relative overflow-hidden bg-background border-t border-border/50">
      {/* Gradient background */}
      <div className="absolute inset-0 overflow-hidden opacity-10">
        <div className="absolute -top-1/2 left-1/2 w-[800px] h-[800px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-gradient-to-r from-primary/20 to-secondary/20 blur-3xl"></div>
      </div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
          {/* Logo and description */}
          <div className="space-y-5">
            <div className="flex items-center space-x-2">
              <Logo className="h-7 w-auto text-primary" />
              <span className="text-2xl font-bold gradient-text">Sicilius</span>
            </div>
            <p className="text-foreground/70 text-sm leading-relaxed">
              Şirket bilgilerine kolay erişim için güçlü ve kullanıcı dostu bir platform.
            </p>
            
            {/* Social links 
            <div className="flex space-x-4 pt-2">
              {socialLinks.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-foreground/60 hover:text-foreground transition-colors rounded p-1 -m-1 hover:bg-gray-100 dark:hover:bg-slate-800"
                  aria-label={item.name}
                >
                  {item.icon}
                </Link>
              ))}
            </div>*/}
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
                      className="flex items-center text-sm text-foreground/80 hover:text-foreground transition-colors group rounded px-1 -mx-1 hover:bg-gray-100 dark:hover:bg-slate-800"
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
            &copy; {currentYear} Sicilius. Tüm hakları saklıdır.
          </p>
          
          <div className="flex flex-wrap items-center gap-4 mt-4 md:mt-0">
            <Link href="/gizlilik-politikasi" className="text-sm text-foreground/80 hover:text-foreground transition-colors rounded px-1 -mx-1 hover:bg-gray-100 dark:hover:bg-slate-800">Gizlilik Politikası</Link>
            <span className="text-foreground/40">•</span>
            <Link href="/kullanici-sozlesmesi" className="text-sm text-foreground/80 hover:text-foreground transition-colors rounded px-1 -mx-1 hover:bg-gray-100 dark:hover:bg-slate-800">Kullanıcı Sözleşmesi</Link>
            <span className="text-foreground/40">•</span>
            <Link href="/cerez-politikasi" className="text-sm text-foreground/80 hover:text-foreground transition-colors rounded px-1 -mx-1 hover:bg-gray-100 dark:hover:bg-slate-800">Çerez Politikası</Link>
            <span className="text-foreground/40">•</span>
            <Link href="/kvkk-aydinlatma" className="text-sm text-foreground/80 hover:text-foreground transition-colors rounded px-1 -mx-1 hover:bg-gray-100 dark:hover:bg-slate-800">KVKK Aydınlatma</Link>
          </div>
        </div>
      </div>
      
      {/* Decorative elements */}
      <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-primary via-secondary to-primary opacity-30"></div>
    </footer>
  );
}
