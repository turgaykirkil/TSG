import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow, TableCaption } from '@/components/ui/table';
import type { HistoryEntryLite } from '@/hooks/useUnifiedSearch';

interface CompanyHistoryTableProps {
  entries?: HistoryEntryLite[];
}

export function CompanyHistoryTable({ entries = [] }: CompanyHistoryTableProps) {
  return (
    <div className="rounded-md border bg-white">
      <Table aria-label="Şirket geçmişi tablosu">
        <TableHeader>
          <TableRow>
            <TableHead>Şirket ID</TableHead>
            <TableHead>Değişiklik</TableHead>
            <TableHead className="text-right">Tarih</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {entries.map((row, idx) => (
            <TableRow
              key={row.id || idx}
              className={`cursor-pointer hover:bg-muted/50 ${idx % 2 === 1 ? 'bg-muted/30' : ''} focus:outline-none focus-visible:ring-2 focus-visible:ring-[#0A192F] focus-visible:ring-offset-2 focus-visible:ring-offset-background`}
              onClick={() => console.log('Geçmiş detayı:', row.id)}
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  console.log('Geçmiş detayı:', row.id);
                }
              }}
              aria-label={`Şirket ID: ${row.company_id || '-'}, Değişiklik: ${row.entry_type || '-'}`}
            >
              <TableCell className="font-medium">{row.company_id || '-'}</TableCell>
              <TableCell>{row.entry_type || '-'}</TableCell>
              <TableCell className="text-right">{row.entry_date || '-'}</TableCell>
            </TableRow>
          ))}
        </TableBody>
        <TableCaption>Şirketler için son değişiklik kayıtları</TableCaption>
      </Table>
    </div>
  );
}

export default CompanyHistoryTable;
