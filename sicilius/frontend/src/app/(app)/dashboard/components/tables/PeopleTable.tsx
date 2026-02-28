import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow, TableCaption } from '@/components/ui/table';
import type { PersonLite } from '@/hooks/useUnifiedSearch';

interface PeopleTableProps {
  people?: PersonLite[];
}

export function PeopleTable({ people = [] }: PeopleTableProps) {
  return (
    <div className="rounded-md border bg-white dark:bg-slate-900 dark:border-slate-700">
      <Table aria-label="Kişiler tablosu">
        <TableHeader>
          <TableRow>
            <TableHead>Ad Soyad</TableHead>
            <TableHead>E-posta</TableHead>
            <TableHead>TCKN/UID</TableHead>
            <TableHead className="text-right">Güncelleme</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {people.map((row, idx) => (
            <TableRow
              key={row.id || idx}
              className={`cursor-pointer hover:bg-muted/50 dark:hover:bg-slate-800 ${idx % 2 === 1 ? 'bg-muted/30 dark:bg-slate-900/40' : ''} focus:outline-none focus-visible:ring-2 focus-visible:ring-[#0A192F] focus-visible:ring-offset-2 focus-visible:ring-offset-background`}
              onClick={() => { /* Kişi detayına git */ }}
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  // console.log('Kişi detayına git:', row.id);
                }
              }}
              aria-label={`Kişi: ${row.full_name || '-'}${row.nationality_id ? ', Kimlik: ' + row.nationality_id : ''}`}
            >
              <TableCell className="font-medium">{row.full_name || '-'}</TableCell>
              <TableCell>{row.email || '-'}</TableCell>
              <TableCell>{row.nationality_id || '-'}</TableCell>
              <TableCell className="text-right">{row.updated_at || '-'}</TableCell>
            </TableRow>
          ))}
        </TableBody>
        <TableCaption>Kişiler</TableCaption>
      </Table>
    </div>
  );
}

export default PeopleTable;
