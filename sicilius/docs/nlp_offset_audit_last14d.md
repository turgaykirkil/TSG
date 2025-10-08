# NLP Offset Denetimi (Son 14 Gün)

Bu rapor, `public.ocr_results` tablosunda son 14 güne ait ilan parçalarının offset (start_offset/end_offset) tutarlılığını inceler. Kod değişikliği yapılmamıştır; yalnızca MCP ile veritabanı okuması yapılmıştır.

## Özet
- **[zaman aralığı]** Son 14 gün
- **[toplam kayıt]** 18,323
- **[out_of_bounds]** 18,138 kayıt (`end_offset > length(original_text)`) — çok yüksek oran
- **[missing_offsets]** 182 kayıt (`start_offset IS NULL OR end_offset IS NULL`)
- **[invalid_order]** 0 kayıt (`start_offset >= end_offset`)
- **[within_bounds]** 3 kayıt (offset aralığı `original_text` uzunluğu içinde)

Veri sorgusu örneği:
```
SELECT
  count(*) as total,
  count(*) FILTER (WHERE start_offset IS NULL OR end_offset IS NULL) as missing_offsets,
  count(*) FILTER (WHERE start_offset IS NOT NULL AND end_offset IS NOT NULL AND start_offset >= end_offset) as invalid_order,
  count(*) FILTER (WHERE start_offset < 0 OR end_offset < 0) as negative_offsets,
  count(*) FILTER (WHERE original_text IS NOT NULL AND end_offset > length(original_text)) as out_of_bounds,
  count(*) FILTER (WHERE start_offset IS NOT NULL AND end_offset IS NOT NULL AND (end_offset - start_offset) < 30) as too_short
FROM public.ocr_results
WHERE created_at >= now() - interval '14 days';
```

## Günlük Özet (son 12 gün)
```
2025-10-05: total=4883, out_of_bounds=4829, missing=54, invalid_order=0
2025-10-04: total=6430, out_of_bounds=6379, missing=50, invalid_order=0
2025-10-03: total=26,   out_of_bounds=25,   missing=1,  invalid_order=0
2025-10-02: total=1189, out_of_bounds=1178, missing=10, invalid_order=0
2025-10-01: total=152,  out_of_bounds=152,  missing=0,  invalid_order=0
2025-09-30: total=8,    out_of_bounds=8,    missing=0,  invalid_order=0
2025-09-29: total=2,    out_of_bounds=2,    missing=0,  invalid_order=0
2025-09-28: total=2,    out_of_bounds=2,    missing=0,  invalid_order=0
2025-09-27: total=11,   out_of_bounds=11,   missing=0,  invalid_order=0
2025-09-25: total=2338, out_of_bounds=2306, missing=32, invalid_order=0
2025-09-24: total=2245, out_of_bounds=2220, missing=25, invalid_order=0
2025-09-23: total=1037, out_of_bounds=1026, missing=10, invalid_order=0
```

## Örnek Hatalı Kayıtlar — out_of_bounds (end_offset > len(original_text))
Aşağıda son 14 günden 5 örnek:
```
{
  "id": 45444,
  "item_index": 1,
  "created_at": "2025-10-05 15:09:14+00",
  "len": 989,
  "start_offset": 10538,
  "end_offset": 11527,
  "text_head": "T.C. İSTANBUL TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN\nİlan Sıra No: 158273\nMersis No: 0613..."
}
{
  "id": 45440,
  "item_index": 1,
  "created_at": "2025-10-05 15:08:47+00",
  "len": 16826,
  "start_offset": 4874,
  "end_offset": 21700,
  "text_head": "T.C. İSTANBUL TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN\nIlan Sıra No: 3936\nMersis No: 0073..."
}
{
  "id": 45437,
  "item_index": 2,
  "created_at": "2025-10-05 15:08:20+00",
  "len": 8753,
  "start_offset": 12912,
  "end_offset": 21665,
  "text_head": "T.C. İSTANBUL TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN\nİlan Sıra No: 5564\nMersis No: 0844..."
}
{
  "id": 45436,
  "item_index": 1,
  "created_at": "2025-10-05 15:08:20+00",
  "len": 8256,
  "start_offset": 4644,
  "end_offset": 12900,
  "text_head": "T.C. İSTANBUL TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN\nIlan Sıra No: 5863\nMersis No: 0121..."
}
{
  "id": 45425,
  "item_index": 6,
  "created_at": "2025-10-05 15:07:54+00",
  "len": 2623,
  "start_offset": 10546,
  "end_offset": 13169,
  "text_head": "T.C. İSTANBUL TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN\nilan Sıra No: 5432\nMERSIS No: 0758..."
}
```

## Örnek Hatalı Kayıtlar — missing_offsets (start veya end NULL)
```
{
  "id": 45391,
  "item_index": 6,
  "created_at": "2025-10-05 15:07:06+00",
  "len": 1139,
  "start_offset": null,
  "end_offset": null,
  "text_head": "T.C. İSTANBUL TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN\nIlan Sıra No: 135263\nMersis No: 0813..."
}
{
  "id": 45393,
  "item_index": 8,
  "created_at": "2025-10-05 15:07:06+00",
  "len": 1146,
  "start_offset": null,
  "end_offset": null,
  "text_head": "T.C. İSTANBUL TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN\nİlan Sıra No: 135262\nMersis No: 0008..."
}
{
  "id": 45387,
  "item_index": 2,
  "created_at": "2025-10-05 15:07:06+00",
  "len": 1044,
  "start_offset": null,
  "end_offset": null,
  "text_head": "T.C. İSTANBUL TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN\nIlan Sıra No: 135732\nMersis No: 0839..."
}
{
  "id": 45389,
  "item_index": 4,
  "created_at": "2025-10-05 15:07:06+00",
  "len": 1188,
  "start_offset": null,
  "end_offset": null,
  "text_head": "T.C. İSTANBUL TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN\nİlan Sıra No: 135737\nMersis No: 0529..."
}
{
  "id": 45269,
  "item_index": 4,
  "created_at": "2025-10-05 15:00:55+00",
  "len": 1180,
  "start_offset": null,
  "end_offset": null,
  "text_head": "T.C. BODRUM TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN\nİlan Sıra No: 3226\nMERSİS No: 0323..."
}
```

## Örnek Doğru Kayıtlar — within_bounds
```
{
  "id": 27116,
  "item_index": 1,
  "created_at": "2025-10-04 14:59:25+00",
  "len": 9831,
  "start_offset": 0,
  "end_offset": 9831,
  "text_head": "Sicilius OCR Sonucu - 2025-10-04 14:59:13 +0000\n--- Sayfa 1 ---\n..."
}
{
  "id": 21006,
  "item_index": 1,
  "created_at": "2025-10-02 17:41:46+00",
  "len": 115,
  "start_offset": 0,
  "end_offset": 115,
  "text_head": "'announcement_42e86c07-44b2-4abf-915d-6d1e24d9a14e_...pdf' dosyası indiriliyor..."
}
{
  "id": 7275,
  "item_index": 1,
  "created_at": "2025-09-23 08:56:39+00",
  "len": 10243,
  "start_offset": 0,
  "end_offset": 10243,
  "text_head": "Sicilius OCR Sonucu - 2025-09-23 08:56:36 +0000\n--- Sayfa 1 ---\n..."
}
```

## Tahmini Kök Neden
- **[offset referansı uyuşmazlığı]** `parse_multiple_announcements()` muhtemelen offset’leri **tam OCR metnine göre** üretiyor; fakat `_fallback_sidewrite_task()` içinde `original_text` **segment metni** olarak yazılıyor. Bu durumda `end_offset > length(original_text)` bozukluğu oluşuyor.
- **[iş akışı]** Son 14 günde çok sayıda kayıt `announcement_id` olmadan “fallback side-write” yoluyla yazılmış görünüyor; bu yolda segment metin saklanıyor.

İlgili referanslar:
- `backend/app/api/api_v1/endpoints/nlp.py` → `_fallback_sidewrite_task()`
- `backend/app/services/nlp_service.py` → `parse_multiple_announcements()` (offset üretimi)

## Etki
- **[vurgulama/işaretleme]** Offset’e bağlı metin vurgulama/doğrulama bozulur.
- **[kalite ölçümü]** Offset temelli kalite metrikleri yanlış çıkar.

## Önerilen Doğrulama (Kod değişikliği olmadan)
- **[A] Tanımı netleştir**: Offset’ler **hangi metne** göre? (tam OCR vs. segment). Tek tanımı benimseyelim.
- **[B] Veri etiketi**: Segment kayıtlarında geçici olarak offset’i `0..len(original_text)` olarak yorumlayalım; “segment-only” etiketiyle işaretlenebilir.
- **[C] Girdi yolu**: `parse-announcements` çağrılarına mümkünse `announcement_id` vererek RPC yolunu tercih etmek; böylece meta ile uyum artar.
- **[D] İzleme**: Günlük `out_of_bounds/total` oranını izleyip eşik aşımlarında uyarı.

## Notlar
- Bu rapor kod düzenlemesi yapmadan, yalnızca MCP ile DB okumasına dayanır.
- İstenirse ilk bozulmanın başladığı günü daha detaylı bir trend grafiği/çıktı ile raporlayabilirim.
