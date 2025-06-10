// Ticaret Sicil Müdürlükleri listesi
export const MUDURLUKLER = [
  { value: 'İstanbul', label: 'İstanbul Ticaret Sicil Müdürlüğü' },
  { value: 'Ankara', label: 'Ankara Ticaret Sicil Müdürlüğü' },
  { value: 'İzmir', label: 'İzmir Ticaret Sicil Müdürlüğü' }
] as const;

// Eski kullanım için geriye dönük uyumluluk
export const MÜDÜRLÜKLER = MUDURLUKLER.map(m => m.label);

export const FILE_TYPES = {
  EXCEL: [
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel'
  ],
  PDF: ['application/pdf']
} as const;

// Müdürlük tipi
export type Mudurluk = typeof MUDURLUKLER[number];
