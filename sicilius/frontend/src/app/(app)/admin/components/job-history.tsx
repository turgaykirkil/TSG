import { useState } from 'react';
import { Icons } from '@/components/icons';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

export default function JobHistory() {
  const [filter, setFilter] = useState({ type: '', status: '', search: '' });

  const jobHistory = [
    { id: 1, type: 'Dosya Yükleme', fileName: 'firma-listesi.xlsx', date: '2025-06-05 14:30', status: 'Tamamlandı', duration: '45s' },
    { id: 2, type: 'Web Scraping', fileName: 'İstanbul Müdürlüğü', date: '2025-06-05 10:15', status: 'Tamamlandı', duration: '12m 34s' },
    { id: 3, type: 'OCR İşlemi', fileName: 'resmi-gazete.pdf', date: '2025-06-04 16:45', status: 'Başarısız', duration: '2m 15s', error: 'Dosya formatı desteklenmiyor' },
    { id: 4, type: 'Veri Yayınlama', fileName: 'ilan-verileri', date: '2025-06-04 09:20', status: 'Tamamlandı', duration: '1m 10s' },
    { id: 5, type: 'Dosya Yükleme', fileName: 'personel-listesi.xlsx', date: '2025-06-03 11:30', status: 'Tamamlandı', duration: '30s' },
  ];

  const filteredJobs = jobHistory.filter(job => {
    return (
      (filter.type === '' || job.type === filter.type) &&
      (filter.status === '' || job.status === filter.status) &&
      (filter.search === '' || 
        job.fileName.toLowerCase().includes(filter.search.toLowerCase()) ||
        job.type.toLowerCase().includes(filter.search.toLowerCase()))
    );
  });

  return (
    <div className="space-y-6">
      <Card>
        <CardContent className="pt-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="text-sm font-medium mb-1 block">İşlem Türü</label>
              <Select onValueChange={value => setFilter({...filter, type: value})}>
                <SelectTrigger>
                  <SelectValue placeholder="Tüm Türler" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Tüm Türler</SelectItem>
                  <SelectItem value="Dosya Yükleme">Dosya Yükleme</SelectItem>
                  <SelectItem value="Web Scraping">Web Scraping</SelectItem>
                  <SelectItem value="OCR İşlemi">OCR İşlemi</SelectItem>
                  <SelectItem value="Veri Yayınlama">Veri Yayınlama</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-sm font-medium mb-1 block">Durum</label>
              <Select onValueChange={value => setFilter({...filter, status: value})}>
                <SelectTrigger>
                  <SelectValue placeholder="Tüm Durumlar" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Tüm Durumlar</SelectItem>
                  <SelectItem value="Tamamlandı">Tamamlandı</SelectItem>
                  <SelectItem value="Bekliyor">Bekliyor</SelectItem>
                  <SelectItem value="Başarısız">Başarısız</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="md:col-span-2">
              <label className="text-sm font-medium mb-1 block">Arama</label>
              <Input 
                placeholder="Dosya adı veya işlem türü ara..." 
                value={filter.search}
                onChange={e => setFilter({...filter, search: e.target.value})}
              />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>İş Geçmişi</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Tarih</TableHead>
                <TableHead>İşlem Türü</TableHead>
                <TableHead>Dosya/İşlem</TableHead>
                <TableHead>Durum</TableHead>
                <TableHead>Süre</TableHead>
                <TableHead>Detay</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredJobs.map((job) => (
                <TableRow key={job.id}>
                  <TableCell>{job.date}</TableCell>
                  <TableCell>{job.type}</TableCell>
                  <TableCell className="font-medium">{job.fileName}</TableCell>
                  <TableCell>
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      job.status === 'Tamamlandı' ? 'bg-green-100 text-green-800' :
                      job.status === 'Başarısız' ? 'bg-red-100 text-red-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {job.status}
                    </span>
                  </TableCell>
                  <TableCell>{job.duration}</TableCell>
                  <TableCell>
                    <Button variant="outline" size="sm">
                      <Icons.fileText className="mr-1 h-4 w-4" />
                      Detay
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
