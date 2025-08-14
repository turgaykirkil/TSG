"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import CompaniesTable from './tables/CompaniesTable';
import PeopleTable from './tables/PeopleTable';
import CompanyHistoryTable from './tables/CompanyHistoryTable';
import type { Company } from '@/types/company.types';
import type { PersonLite, HistoryEntryLite } from '@/hooks/useUnifiedSearch';

interface EntityTabsProps {
  companies: Company[];
  persons: PersonLite[];
  history: HistoryEntryLite[];
}

export function EntityTabs({ companies, persons, history }: EntityTabsProps) {
  return (
    <div className="mt-2">
      <Tabs defaultValue="companies" className="w-full" aria-label="Varlık sekmeleri">
        <TabsList className="bg-[#0A192F] text-white">
          <TabsTrigger value="companies">Şirketler</TabsTrigger>
          <TabsTrigger value="people">Kişiler</TabsTrigger>
          <TabsTrigger value="history">Şirket Geçmişi</TabsTrigger>
        </TabsList>
        <TabsContent value="companies">
          <CompaniesTable companies={companies} />
        </TabsContent>
        <TabsContent value="people">
          <PeopleTable people={persons} />
        </TabsContent>
        <TabsContent value="history">
          <CompanyHistoryTable entries={history} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
