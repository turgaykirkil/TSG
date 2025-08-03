import os
import re
import json
from pathlib import Path

def parse_share_transfer(text_block):
    """
    'Pay Devri' ilanlarından detayları çıkarır.
    Örnek: Kimin kime, ne kadar pay devrettiği ve yeni ortaklık yapısı.
    """
    details = {
        "devir_islemleri": [],
        "yeni_ortaklik_yapisi": []
    }
    
    # Devir işlemlerini bulma
    # Örnek: "Sirket Ortaklarından ... KİMLİK NUMARALI ... ... TL sermaye karşılığı ... adet payını ... KİMLİK NUMARALI ...'e devretmiştir."
    devir_pattern = r"Şirket Ortaklarından .*? (?:Kimlik Numaralı|Mersis Numaralı) (.*?) (.*?) (?:[\d\.,]+) TL sermaye karşılığı .*? payını .*? (?:Kimlik Numaralı|Mersis Numaralı) (.*?) (.*?)'e devretmiştir"
    devir_matches = re.finditer(devir_pattern, text_block, re.IGNORECASE)
    for match in devir_matches:
        details["devir_islemleri"].append({
            "devreden_id": match.group(1).strip(),
            "devreden_isim": ' '.join(match.group(2).split()),
            "devralan_id": match.group(3).strip(),
            "devralan_isim": ' '.join(match.group(4).split()),
        })

    # Yeni ortaklık yapısını bulma (Basit bir başlangıç)
    if "son ortaklık yapısı aşağıdaki gibidir" in text_block.lower():
        yeni_yapi_text = text_block.split("son ortaklık yapısı aşağıdaki gibidir:")[-1]
        ortak_matches = re.finditer(r"(.*?): Beheri .*? (\d+[\.,\d]*) Türk Lirası,", yeni_yapi_text)
        for ortak_match in ortak_matches:
            details["yeni_ortaklik_yapisi"].append({
                "ortak_adi": ' '.join(ortak_match.group(1).split()),
                "sermaye_tl": ortak_match.group(2).strip()
            })

    return details

def parse_officers(text_block):
    """
    'Yönetim/Temsil' (Yetkililer) ilanlarından detayları çıkarır.
    Örnek: Atanan/ayrılan yöneticiler, unvanları, yetki kapsamları.
    """
    details = {
        "atanan_yetkililer": [],
        "ayrilan_yetkililer": []
    }
    # Örnek: "Türkiye Uyruklu ... Kimlik No'lu, ... ikamet eden, AD SOYAD, ... olarak seçilmiştir. Yetki Şekli: ..."
    yeni_atanan_pattern = r"YENİ ATANAN TEMSİLCİLER[\s\S]*?Kimlik No'lu, .*? ikamet eden, (.*?), .*? (Temsile Yetkili.*?) olarak seçilmiştir\."
    matches = re.finditer(yeni_atanan_pattern, text_block, re.IGNORECASE)
    for match in matches:
        details["atanan_yetkililer"].append({
            "isim": ' '.join(match.group(1).split()),
            "unvan_ve_yetki": ' '.join(match.group(2).split())
        })
    return details

def parse_address_change(text_block):
    """
    'Adres Değişikliği' ilanlarından detayları çıkarır.
    """
    details = {}
    match = re.search(r"(.*?) adresinden, (.*?) adresine taşınmıştır", text_block, re.IGNORECASE)
    if match:
        details['eski_adres'] = ' '.join(match.group(1).split()).strip()
        details['yeni_adres'] = ' '.join(match.group(2).split()).strip()
    return details

def parse_capital_change(text_block):
    """
    'Sermaye Artırımı/Azaltımı' ilanlarından detayları çıkarır.
    """
    details = {}
    eski_sermaye = re.search(r"Önceki sermayeyi teşkil eden ([\d\.,]+) TL", text_block, re.IGNORECASE)
    yeni_sermaye = re.search(r"Şirketin sermayesi[\s,]*([\d\.,]+) .*-TL'dir", text_block, re.IGNORECASE)
    if eski_sermaye:
        details['eski_sermaye_tl'] = eski_sermaye.group(1).strip()
    if yeni_sermaye:
        details['yeni_sermaye_tl'] = yeni_sermaye.group(1).strip()
    return details


# Olay türlerini anahtar kelimeler ve ilgili ayrıştırıcı fonksiyonlarla eşleştir
EVENT_MAP = {
    'PAY DEVRİ': parse_share_transfer,
    'YÖNETİM (MÜDÜR) - TEMSİL': parse_officers,
    'YÖNETİM - TEMSİL': parse_officers,
    'ADRES DEĞİŞİKLİĞİ': parse_address_change,
    'SERMAYE ARTIRIMI': parse_capital_change,
    'SERMAYE AZALTIMI': parse_capital_change,
}

def get_event_parser(text_block):
    """
    İlan metninden olay türünü tespit eder ve ilgili ayrıştırıcı fonksiyonu döndürür.
    """
    # 'Tescil Edilen Hususlar' en güvenilir belirteç
    tescil_match = re.search(r"Tescil Edilen Hususlar:\s*(.*?)(?=\n|Tescile Delil Olan Belgeler:)", text_block, re.IGNORECASE)
    if tescil_match:
        event_type_str = tescil_match.group(1).strip().upper()
        for key, parser_func in EVENT_MAP.items():
            if key in event_type_str:
                return event_type_str, parser_func
    return None, None

def parse_announcement_block(block):
    """
    Tek bir ilan bloğunu işler, temel bilgileri ve olay detaylarını çıkarır.
    """
    data = {}
    # Temel bilgileri çıkar
    ticaret_unvani_match = re.search(r'Ticaret Unvanı:\s*([\s\S]*?)(?=Adres:|Mersis No:|$)', block, re.IGNORECASE)
    data['ticaret_unvani'] = ' '.join(ticaret_unvani_match.group(1).split()).strip() if ticaret_unvani_match else None

    mersis_no_match = re.search(r'Mersis No:\s*(\S+)', block, re.IGNORECASE)
    data['mersis_no'] = mersis_no_match.group(1).strip() if mersis_no_match else None

    sicil_no_match = re.search(r'Ticaret Sicil/Dosya No:\s*(\S+)', block, re.IGNORECASE)
    data['sicil_no'] = sicil_no_match.group(1).strip() if sicil_no_match else None

    # Sadece temel bilgileri olan blokları işlemeye devam et
    if not data['ticaret_unvani']:
        return None

    # Olay türünü ve ilgili ayrıştırıcıyı al
    event_type, parser_function = get_event_parser(block)
    data['ilan_turu'] = event_type
    data['ilan_detaylari'] = {}

    # Eğer bir uzman ayrıştırıcı varsa, onu çalıştır
    if parser_function:
        data['ilan_detaylari'] = parser_function(block)
    
    data['raw_text'] = block
    return data

def main():
    """
    Ana betik fonksiyonu.
    """
    script_dir = Path(__file__).parent
    input_dir = script_dir / 'ocr_output'
    output_file = script_dir / 'detailed_announcements.json'

    if not input_dir.exists():
        print(f"Hata: Girdi klasörü bulunamadı: {input_dir}")
        print("Lütfen önce 'surya_tesseract_pipeline.py' betiğini çalıştırdığınızdan emin olun.")
        return

    all_insights = []
    print(f"'{input_dir}' klasöründeki OCR sonuçları okunuyor...")

    # Her bir PDF'in alt klasörünü işle
    for pdf_dir in input_dir.iterdir():
        if not pdf_dir.is_dir():
            continue

        json_file = pdf_dir / 'structured_output.json'
        if not json_file.exists():
            continue

        print(f"- İşleniyor: {pdf_dir.name}")
        with open(json_file, 'r', encoding='utf-8') as f:
            announcements = json.load(f)
        
        for announcement in announcements:
            raw_text = announcement.get('raw_block_text')
            if not raw_text:
                continue
            
            parsed_data = parse_announcement_block(raw_text)
            if parsed_data:
                parsed_data['source_pdf'] = pdf_dir.name
                all_insights.append(parsed_data)

    print(f"\nToplam {len(all_insights)} adet ilan derinlemesine analiz edildi.")

    # Sonuçları JSON dosyasına yaz
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_insights, f, ensure_ascii=False, indent=4)

    print(f"Detaylı analiz sonuçları başarıyla '{output_file}' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
