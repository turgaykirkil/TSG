'use client';

import React, { useState, useRef, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Button } from '@/components/ui/button';
import { Search, Trash2, Database, Table2, RefreshCcw, LayoutPanelLeft, Check, X } from 'lucide-react';

export default function DatabaseGrid() {
  const queryClient = useQueryClient();
  const [selectedTable, setSelectedTable] = useState<string>('companies');
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  
  // Cell inline editing state
  const [editingCell, setEditingCell] = useState<{ id: string, col: string } | null>(null);
  const [cellValue, setCellValue] = useState<string>('');
  const inputRef = useRef<HTMLTextAreaElement | HTMLInputElement>(null);

  // 1. Fetch available tables
  const { data: tablesData } = useQuery({
    queryKey: ['admin-tables'],
    queryFn: async () => {
      const res = await fetch('/api/v1/admin/tables', { credentials: 'include' });
      if (!res.ok) throw new Error('Failed to fetch tables');
      return res.json();
    }
  });

  // 2. Fetch table rows
  const { data: rowsData, isLoading, refetch, isFetching } = useQuery({
    queryKey: ['admin-table-rows', selectedTable, page, search],
    queryFn: async () => {
      const params = new URLSearchParams({ page: String(page), size: '25' });
      if (search) params.append('search', search);
      const res = await fetch(`/api/v1/admin/tables/${selectedTable}?${params}`, { credentials: 'include' });
      if (!res.ok) throw new Error('Failed to fetch rows');
      return res.json();
    },
    enabled: !!selectedTable,
    staleTime: 30000,
  });

  // 3. Update Mutation
  const updateMutation = useMutation({
    mutationFn: async ({ id, payload }: { id: string, payload: any }) => {
      const res = await fetch(`/api/v1/admin/tables/${selectedTable}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error('Failed to update');
      return res.json();
    },
    onSuccess: () => {
      setEditingCell(null);
      queryClient.invalidateQueries({ queryKey: ['admin-table-rows'] });
    }
  });

  // 4. Delete Mutation
  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      const res = await fetch(`/api/v1/admin/tables/${selectedTable}/${id}`, {
        method: 'DELETE',
        credentials: 'include'
      });
      if (!res.ok) throw new Error('Failed to delete');
      return res.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['admin-table-rows'] });
    }
  });

  // Focus input automatically when editing starts
  useEffect(() => {
    if (editingCell && inputRef.current) {
      inputRef.current.focus();
      // Move cursor to the end
      const length = inputRef.current.value.length;
      if (inputRef.current.setSelectionRange) {
        inputRef.current.setSelectionRange(length, length);
      }
    }
  }, [editingCell]);

  const handleCellSave = () => {
    if (!editingCell) return;
    updateMutation.mutate({ id: editingCell.id, payload: { [editingCell.col]: cellValue } });
  };

  const handleCellKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      setEditingCell(null);
    } else if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleCellSave();
    }
  };

  const items = rowsData?.items || [];
  const columns = items.length > 0 ? Object.keys(items[0]).filter(k => k !== 'id') : [];

  return (
    <div className="flex flex-col h-full bg-background border border-slate-200 dark:border-slate-800 rounded-md overflow-hidden shadow-sm font-sans">
      
      {/* Top Bar - Supabase Style */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#18181B]">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-2 py-1 bg-white dark:bg-[#27272A] border border-slate-200 dark:border-slate-700 rounded-md shadow-sm">
            <Table2 className="w-4 h-4 text-slate-500" />
            <select 
              className="bg-transparent border-none text-[13px] font-medium text-slate-700 dark:text-slate-300 focus:ring-0 cursor-pointer outline-none w-40"
              value={selectedTable}
              onChange={(e) => { setSelectedTable(e.target.value); setPage(1); }}
            >
              {tablesData?.tables?.map((t: any) => (
                <option key={t.id} value={t.id} className="bg-background">{t.name}</option>
              ))}
            </select>
          </div>

          <div className="flex items-center h-8 bg-white dark:bg-[#27272A] border border-slate-200 dark:border-slate-700 rounded-md px-2 shadow-sm focus-within:ring-1 focus-within:ring-primary/50 transition-shadow w-64">
            <Search className="w-3.5 h-3.5 text-slate-400 mr-2" />
            <input 
              placeholder="Filter by value..." 
              className="bg-transparent border-none text-[13px] w-full outline-none placeholder:text-slate-400 text-slate-700 dark:text-slate-300"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') { setPage(1); refetch(); } }}
            />
          </div>
          
          <Button variant="ghost" size="icon" className="h-8 w-8 text-slate-500 hover:text-slate-700 dark:hover:text-slate-300" onClick={() => refetch()}>
            <RefreshCcw className={`w-3.5 h-3.5 ${isFetching ? 'animate-spin' : ''}`} />
          </Button>
        </div>
      </div>

      {/* Spreadsheet Grid */}
      <div className="flex-1 overflow-auto bg-white dark:bg-[#121212] relative">
        {isLoading ? (
          <div className="flex items-center justify-center h-full text-[13px] text-slate-500 font-mono">Loading data...</div>
        ) : items.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-slate-500">
            <Database className="w-8 h-8 mb-2 opacity-20" />
            <span className="text-[13px] font-mono">No records found</span>
          </div>
        ) : (
          <table className="w-max min-w-full text-left border-collapse">
            <thead className="sticky top-0 z-20 bg-slate-50 dark:bg-[#18181B] shadow-[0_1px_0_0_rgba(203,213,225,1)] dark:shadow-[0_1px_0_0_rgba(39,39,42,1)]">
              <tr>
                <th className="w-12 h-8 px-2 border-r border-slate-200 dark:border-slate-800 sticky left-0 z-30 bg-slate-50 dark:bg-[#18181B] text-center font-mono text-[11px] font-medium text-slate-500 select-none shadow-[1px_0_0_0_rgba(203,213,225,1)] dark:shadow-[1px_0_0_0_rgba(39,39,42,1)]">
                  <LayoutPanelLeft className="w-3.5 h-3.5 inline-block opacity-50" />
                </th>
                <th className="w-64 h-8 px-3 border-r border-slate-200 dark:border-slate-800 font-mono text-[11px] font-medium text-slate-500 tracking-wider select-none shrink-0">
                  id
                </th>
                {columns.map(col => (
                  <th key={col} className="min-w-[200px] max-w-[400px] h-8 px-3 border-r border-slate-200 dark:border-slate-800 font-mono text-[11px] font-medium text-slate-500 tracking-wider select-none">
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800/50">
              {items.map((row: any, idx: number) => (
                <tr key={row.id} className="group hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors">
                  <td className="w-12 h-8 border-r border-slate-200 dark:border-slate-800 text-center bg-slate-50 dark:bg-[#18181B] sticky left-0 z-10 shadow-[1px_0_0_0_rgba(203,213,225,1)] dark:shadow-[1px_0_0_0_rgba(39,39,42,1)] group-hover:bg-slate-100 dark:group-hover:bg-[#27272A] transition-colors relative">
                    <span className="text-[10px] text-slate-400 font-mono opacity-50 group-hover:opacity-0 absolute inset-0 flex items-center justify-center">
                      {idx + 1 + (page - 1) * 25}
                    </span>
                    <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100">
                      <button onClick={() => { if (confirm('Kayıt silinecek. Emin misiniz?')) deleteMutation.mutate(row.id); }} className="text-slate-400 hover:text-red-500 transition-colors">
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </td>
                  <td className="w-64 h-8 px-3 border-r border-slate-200 dark:border-slate-800 font-mono text-[12px] text-slate-400 truncate shrink-0" title={row.id}>
                    {row.id}
                  </td>
                  {columns.map(col => {
                    const isEditing = editingCell?.id === row.id && editingCell?.col === col;
                    const valueStr = String(row[col] ?? '');
                    // Render boolean, nulls clearly
                    const isNull = row[col] === null;
                    const isBoolOrNum = typeof row[col] === 'boolean' || typeof row[col] === 'number';

                    return (
                      <td 
                        key={col} 
                        className={`min-w-[200px] max-w-[400px] h-8 px-3 border-r border-slate-200 dark:border-slate-800 text-[13px] text-slate-700 dark:text-slate-300 truncate transition-colors relative cursor-default hover:bg-slate-100/50 dark:hover:bg-slate-700/30 ${isEditing ? 'bg-blue-50/50 dark:bg-blue-900/20 ring-1 ring-inset ring-primary z-10 overflow-visible' : ''}`}
                        onDoubleClick={() => {
                          setEditingCell({ id: row.id, col });
                          setCellValue(valueStr);
                        }}
                      >
                        {isEditing ? (
                          <div className="absolute inset-0 -m-[1px] bg-white dark:bg-[#18181B] shadow-lg ring-1 ring-primary flex rounded-sm z-50 min-w-[300px]">
                            <textarea 
                              ref={inputRef as any}
                              value={cellValue} 
                              onChange={(e) => setCellValue(e.target.value)}
                              onKeyDown={handleCellKeyDown}
                              className="w-full h-full min-h-[100px] bg-transparent outline-none p-2 text-[13px] font-mono text-slate-800 dark:text-slate-200 resize-none"
                            />
                            <div className="absolute right-2 bottom-2 flex gap-1 bg-white dark:bg-[#18181B] shadow-sm rounded-md border p-1">
                              <button onClick={() => setEditingCell(null)} className="p-1 text-slate-500 hover:text-red-500 rounded bg-slate-100 dark:bg-slate-800">
                                <X className="w-3.5 h-3.5" />
                              </button>
                              <button onClick={handleCellSave} className="p-1 text-slate-500 hover:text-green-500 rounded bg-slate-100 dark:bg-slate-800">
                                <Check className="w-3.5 h-3.5" />
                              </button>
                            </div>
                          </div>
                        ) : (
                          <div className={`truncate w-full ${isBoolOrNum ? 'font-mono text-blue-600 dark:text-blue-400' : ''}`} title={valueStr}>
                            {isNull ? <span className="text-slate-400 italic">NULL</span> : valueStr}
                          </div>
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Footer / Pagination */}
      <div className="flex items-center justify-between px-4 py-2 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#18181B]">
        <div className="text-[12px] text-slate-500 font-mono">
          {rowsData ? `${rowsData.total === 1000000 ? '100000+' : rowsData.total} records` : '0 records'}
        </div>
        
        {rowsData && rowsData.pages > 1 && (
          <div className="flex gap-1 items-center font-mono text-[12px]">
            <Button variant="ghost" size="sm" className="h-7 px-2 text-[12px] text-slate-500 hover:text-slate-700" disabled={page === 1} onClick={() => setPage(p => p - 1)}>Prev</Button>
            <span className="px-2 text-slate-500 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-md h-7 flex items-center justify-center min-w-[32px]">
              {page}
            </span>
            <Button variant="ghost" size="sm" className="h-7 px-2 text-[12px] text-slate-500 hover:text-slate-700" onClick={() => setPage(p => p + 1)}>Next</Button>
          </div>
        )}
      </div>
    </div>
  );
}
