import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow, TableCaption } from '@/components/ui/table';
import ScoreBadge from '../ScoreBadge';
import type { Company } from '@/types/company.types';

interface CompaniesTableProps {
  companies?: Company[];
  onSelectCompany?: (id: string) => void;
}

// Şehir bilgisi, çoğunlukla "<ŞEHİR> TİCARET SİCİLİ MÜDÜRLÜĞÜ" biçimindeki
// `sicil_mudurluk` alanından türetilir. Bu yardımcı, şehir adını ayıklar.
const extractCityFromRegistryOffice = (office?: string | null): string => {
  if (!office) return '-';
  const upper = office.toUpperCase();
  const marker = 'TİCARET SİCİL';
  const idx = upper.indexOf(marker);
  if (idx > 0) return office.slice(0, idx).trim();
  // Yedek: ilk kelimeyi dön.
  const first = office.split(/\s+/)[0]?.trim();
  return first || '-';
};

// Tarih/saat metnini kullanıcı dostu biçimde göster.
// Not: Liste görünümünden "Son Güncelleme" kaldırıldığı için tarih formatlayıcı kullanılmıyor.

export default function CompaniesTable({ companies = [], onSelectCompany }: CompaniesTableProps) {
  // Eşleşme kuvveti varsa skoruna göre azalan sırada göster
  const rows = Array.isArray(companies)
    ? [...companies].sort((a: any, b: any) => {
        const sa = typeof a?.match_strength === 'number' ? a.match_strength : -1;
        const sb = typeof b?.match_strength === 'number' ? b.match_strength : -1;
        return sb - sa;
      })
    : [];

  return (
    <div className="rounded-md border bg-white dark:bg-slate-900 dark:border-slate-700 mb-8 md:mb-12">
      <Table aria-label="Şirketler tablosu">
        <TableHeader>
          <TableRow>
            <TableHead>Unvan</TableHead>
            <TableHead>Eşleşme</TableHead>
            <TableHead>Şehir</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((c, idx) => {
            const title = (c as any).firma_unvani ?? (c as any).unvan ?? '-';
            const registryNo = (c as any).sicil_no ?? '-';
            const registryOffice = (c as any).sicil_mudurluk ?? '-';
            const matchStrength = (c as any).match_strength as number | undefined;
            const rowKey = `${(c as any).id ?? registryNo ?? title}-${idx}`;
            const id = (c as any).id ?? '';
            const city = extractCityFromRegistryOffice(registryOffice);
            return (
              <TableRow
                key={rowKey}
                className={`group cursor-pointer hover:bg-muted/50 dark:hover:bg-slate-800 ${idx % 2 === 1 ? 'bg-muted/30 dark:bg-slate-900/40' : ''} focus:outline-none focus-visible:ring-2 focus-visible:ring-[#0A192F] focus-visible:ring-offset-2 focus-visible:ring-offset-background transition-transform`}
                data-testid={`company-row-${idx}`}
                onClick={() => {
                  if (onSelectCompany && typeof id === 'string' && id) onSelectCompany(id);
                  else console.log('Şirket detayına git (id yok):', registryNo || title);
                }}
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    if (onSelectCompany && typeof id === 'string' && id) onSelectCompany(id);
                    else console.log('Şirket detayına git (id yok):', registryNo || title);
                  }
                }}
                aria-label={`Şirket: ${title}, Şehir: ${city}`}
              >
                <TableCell className="font-medium">{title}</TableCell>
                <TableCell>
                  <ScoreBadge score={matchStrength} />
                </TableCell>
                <TableCell>{city}</TableCell>
              </TableRow>
            );
          })}
        </TableBody>
        <TableCaption>
          {companies.length === 0 ? 'Sonuç bulunamadı' : 'Şirket kayıtları'}
        </TableCaption>
      </Table>
    </div>
  );
}


