import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow, TableCaption } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
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
const formatDateTime = (value?: string | null): string => {
  if (!value || value === '-') return '-';
  let d = new Date(value);
  if (isNaN(d.getTime())) {
    // Mikro saniyeleri veya saat dilimi eksiklerini normalize etmeyi dene
    const base = value.slice(0, 19); // YYYY-MM-DDTHH:mm:ss
    const tryDate = new Date(base);
    if (!isNaN(tryDate.getTime())) d = tryDate;
  }
  if (isNaN(d.getTime())) return value; // son çare: ham metni göster
  return new Intl.DateTimeFormat('tr-TR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(d);
};

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
    <div className="rounded-md border bg-white">
      <Table aria-label="Şirketler tablosu">
        <TableHeader>
          <TableRow>
            <TableHead>Unvan</TableHead>
            <TableHead>Eşleşme</TableHead>
            <TableHead>Şehir</TableHead>
            <TableHead className="text-right">Son Güncelleme</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {rows.map((c, idx) => {
            const title = (c as any).firma_unvani ?? (c as any).unvan ?? '-';
            const registryNo = (c as any).sicil_no ?? '-';
            const registryOffice = (c as any).sicil_mudurluk ?? '-';
            const updatedAt = (c as any).updated_at ?? (c as any).last_scraped_at ?? (c as any).created_at ?? '-';
            const matchStrength = (c as any).match_strength as number | undefined;
            const rowKey = `${(c as any).id ?? registryNo ?? title}-${idx}`;
            const id = (c as any).id ?? '';
            const city = extractCityFromRegistryOffice(registryOffice);
            return (
              <TableRow
                key={rowKey}
                className={`cursor-pointer hover:bg-muted/50 ${idx % 2 === 1 ? 'bg-muted/30' : ''} focus:outline-none focus-visible:ring-2 focus-visible:ring-[#0A192F] focus-visible:ring-offset-2 focus-visible:ring-offset-background`}
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
                  {typeof matchStrength === 'number' ? (
                    <Badge variant="outline" title="Eşleşme kuvveti">
                      {matchStrength}
                    </Badge>
                  ) : (
                    '-'
                  )}
                </TableCell>
                <TableCell>{city}</TableCell>
                <TableCell className="text-right">{formatDateTime(updatedAt)}</TableCell>
              </TableRow>
            );
          })}
        </TableBody>
        <TableCaption>
          {companies.length === 0 ? 'Sonuç bulunamadı' : 'Son güncellenen şirket kayıtları'}
        </TableCaption>
      </Table>
    </div>
  );
}


