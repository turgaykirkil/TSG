import { Metadata } from 'next';
import SSSClient from './SSSClient';

export const metadata: Metadata = {
  title: 'Sıkça Sorulan Sorular | Sicilius',
  description: 'Sicilius hakkında en çok merak edilen soruların yanıtlarını bulun. Sorgu limitleri, üyelik sistemi ve veri güvenliği hakkında bilgiler.',
};

export default function SSSPage() {
  return <SSSClient />;
}