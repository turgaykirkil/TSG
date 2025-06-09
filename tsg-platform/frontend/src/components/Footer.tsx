import { Link } from 'react-router-dom';
import { Icons } from '@/components/icons';
import { cn } from '@/lib/utils';

const footerLinks = [
  { name: 'Gizlilik Politikası', href: '/privacy' },
  { name: 'Kullanım Koşulları', href: '/terms' },
  { name: 'Çerez Politikası', href: '/cookies' },
  { name: 'SSS', href: '/faq' },
];

const socialLinks = [
  {
    name: 'GitHub',
    href: 'https://github.com',
    icon: Icons.github,
  },
  {
    name: 'Twitter',
    href: 'https://twitter.com',
    icon: Icons.twitter,
  },
  {
    name: 'LinkedIn',
    href: 'https://linkedin.com',
    icon: Icons.linkedin,
  },
];

type FooterProps = {
  className?: string;
};

export function Footer({ className }: FooterProps) {
  const currentYear = new Date().getFullYear();

  return (
    <footer className={cn('border-t bg-background', className)}>
      <div className="container py-12">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-4">
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <Icons.logo className="h-8 w-8" />
              <span className="text-xl font-bold">TSG Platform</span>
            </div>
            <p className="text-muted-foreground text-sm">
              Şirketlerin ihtiyaç duyduğu çözümleri sunan kapsamlı bir platform.
            </p>
            <div className="flex space-x-4">
              {socialLinks.map((social) => {
                const Icon = social.icon;
                return (
                  <a
                    key={social.name}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-muted-foreground hover:text-foreground transition-colors"
                    aria-label={social.name}
                  >
                    <span className="sr-only">{social.name}</span>
                    <Icon className="h-5 w-5" />
                  </a>
                );
              })}
            </div>
          </div>

          <div>
            <h4 className="text-sm font-medium mb-4">Hızlı Bağlantılar</h4>
            <ul className="space-y-3">
              {footerLinks.map((link) => (
                <li key={link.name}>
                  <Link
                    to={link.href}
                    className="text-sm text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-medium mb-4">İletişim</h4>
            <address className="not-italic text-sm space-y-3">
              <div className="flex items-start space-x-2">
                <Icons.mapPin className="h-4 w-4 mt-0.5 text-muted-foreground flex-shrink-0" />
                <span className="text-muted-foreground">1234 Şirket Adresi, İstanbul, Türkiye</span>
              </div>
              <div className="flex items-center space-x-2">
                <Icons.mail className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                <a href="mailto:info@tsgplatform.com" className="text-muted-foreground hover:text-foreground transition-colors">
                  info@tsgplatform.com
                </a>
              </div>
              <div className="flex items-center space-x-2">
                <Icons.phone className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                <a href="tel:+905551234567" className="text-muted-foreground hover:text-foreground transition-colors">
                  +90 555 123 45 67
                </a>
              </div>
            </address>
          </div>

          <div>
            <h4 className="text-sm font-medium mb-4">Bizi Takip Edin</h4>
            <div className="flex space-x-4">
              {socialLinks.map((social) => {
                const Icon = social.icon;
                return (
                  <a
                    key={social.name}
                    href={social.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-muted-foreground hover:text-foreground transition-colors"
                    aria-label={social.name}
                  >
                    <span className="sr-only">{social.name}</span>
                    <Icon className="h-5 w-5" />
                  </a>
                );
              })}
            </div>
            
            <div className="mt-6">
              <h5 className="text-sm font-medium mb-2">Bültenimize Kaydolun</h5>
              <div className="flex space-x-2">
                <input
                  type="email"
                  placeholder="E-posta adresiniz"
                  className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
                />
                <button className="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-9 px-4 py-2">
                  Gönder
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t text-center text-sm text-muted-foreground">
          <p>&copy; {currentYear} TSG Platform. Tüm hakları saklıdır.</p>
          <div className="mt-2 flex justify-center space-x-4 text-xs">
            <Link to="/privacy" className="hover:underline">Gizlilik Politikası</Link>
            <span>•</span>
            <Link to="/terms" className="hover:underline">Kullanım Koşulları</Link>
            <span>•</span>
            <Link to="/cookies" className="hover:underline">Çerez Politikası</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
