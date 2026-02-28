import { Metadata } from 'next';
import ContactClient from './ContactClient';

export const metadata: Metadata = {
  title: 'İletişim | Sicilius',
  description: 'Sicilius ile iletişime geçin. Sorularınız, önerileriniz veya teknik destek talepleriniz için bize mesaj gönderin.',
};

export default function ContactPage() {
  return <ContactClient />;
}
