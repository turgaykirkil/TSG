import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow, TableCaption } from '@/components/ui/table';
import type { Company } from '@/types/company.types';

interface CompaniesTableProps {
  companies?: Company[];
}

export default function CompaniesTable({ companies = [] }: CompaniesTableProps) {
  return (
    <div className="rounded-md border bg-white">
      <Table aria-label="Şirketler tablosu">
        <TableHeader>
          <TableRow>
            <TableHead>Unvan</TableHead>
            <TableHead>Sicil No</TableHead>
            <TableHead>Müdürlük</TableHead>
            <TableHead className="text-right">Güncelleme</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {companies.map((c, idx) => {
            const title = (c as any).firma_unvani ?? (c as any).unvan ?? '-';
            const registryNo = (c as any).sicil_no ?? '-';
            const registryOffice = (c as any).sicil_mudurluk ?? '-';
            const updatedAt = (c as any).updated_at ?? (c as any).last_scraped_at ?? (c as any).created_at ?? '-';
            const rowKey = `${(c as any).id ?? registryNo ?? title}-${idx}`;
            return (
              <TableRow
                key={rowKey}
                className={`cursor-pointer hover:bg-muted/50 ${idx % 2 === 1 ? 'bg-muted/30' : ''} focus:outline-none focus-visible:ring-2 focus-visible:ring-[#0A192F] focus-visible:ring-offset-2 focus-visible:ring-offset-background`}
                onClick={() => console.log('Şirket detayına git:', (c as any).id || registryNo)}
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    console.log('Şirket detayına git:', (c as any).id || registryNo);
                  }
                }}
                aria-label={`Şirket: ${title}, Sicil No: ${registryNo}`}
              >
                <TableCell className="font-medium">{title}</TableCell>
                <TableCell>{registryNo}</TableCell>
                <TableCell>{registryOffice}</TableCell>
                <TableCell className="text-right">{updatedAt}</TableCell>
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

