# -*- coding: utf-8 -*-
import os
import gc
import torch
import random
import json
import numpy as np
from pathlib import Path
from PIL import Image
from pdf2image import convert_from_bytes
import pytesseract
from supabase import create_client, Client
from dotenv import load_dotenv

from functools import wraps
import time
import traceback

# --- DECORATORS ---
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"✅ {func.__name__} fonksiyonu {end_time - start_time:.2f} saniyede tamamlandı.")
        return result
    return wrapper

# --- SUPABASE İstemci Başlatma ---
def init_supabase_client():
    try:
        env_path = Path(__file__).parent.parent / '.env'
        print(f"INFO: .env dosyası şu yolda aranıyor: {env_path}")
        load_dotenv(dotenv_path=env_path)
        url = os.environ.get("TSG_SUPABASE_URL")
        key = os.environ.get("TSG_SUPABASE_KEY")
        if not url or not key:
            print("HATA: TSG_SUPABASE_URL ve TSG_SUPABASE_KEY .env dosyasında bulunamadı.")
            return None
        return create_client(url, key)
    except Exception as e:
        print(f"Supabase istemcisi başlatılırken hata oluştu: {e}")
        return None

# --- PDF ve Görüntü İşleme Fonksiyonları ---
@timer
def download_pdf_from_supabase(supabase: Client, bucket_name: str, pdf_name: str) -> bytes:
    print(f"📥 '{pdf_name}' dosyası '{bucket_name}' bucket'ından indiriliyor...")
    try:
        response = supabase.storage.from_(bucket_name).download(pdf_name)
        return response
    except Exception as e:
        print(f"'{pdf_name}' indirilirken hata: {e}")
        return None

@timer
def pdf_bytes_to_images(pdf_bytes: bytes) -> list:
    try:
        return convert_from_bytes(pdf_bytes)
    except Exception as e:
        print(f"PDF byte'ları resimlere dönüştürülürken hata: {e}")
        return []



# --- METİN YAPILANDIRMA VE ANALİZ ---
def parse_structured_text(text: str) -> list:
    # Bu fonksiyon, yapılandırılmış metinden ilanları ayrıştırmak için placeholder'dır.
    # Gerçek implementasyon, metin formatına göre değişiklik gösterecektir.
    return [{'ilan_metni': text[:500]}] # Örnek olarak metnin ilk 500 karakterini al

def reorder_text_by_columns(text_lines) -> str:
    if not text_lines:
        return ""
    def find_peaks_simple(data, height=1):
        peaks = []
        if len(data) <= 1: return peaks
        if data[0] > data[1] and data[0] >= height: peaks.append(0)
        for i in range(1, len(data) - 1):
            if data[i] > data[i-1] and data[i] > data[i+1] and data[i] >= height: peaks.append(i)
        if data[-1] > data[-2] and data[-1] >= height: peaks.append(len(data)-1)
        return peaks

    x_centers = [(line.bbox[0] + line.bbox[2]) / 2 for line in text_lines]
    num_bins = max(10, int(len(x_centers) / 4))
    counts, bin_edges = np.histogram(x_centers, bins=num_bins)
    peaks = find_peaks_simple(counts, height=1)

    if not peaks:
        sorted_lines = sorted(text_lines, key=lambda line: line.bbox[1])
        return "\n".join([line.text for line in sorted_lines])

    column_centers = [(bin_edges[p] + bin_edges[p+1]) / 2 for p in peaks]
    columns = {center: [] for center in column_centers}
    for line in text_lines:
        center_x = (line.bbox[0] + line.bbox[2]) / 2
        closest_column = min(column_centers, key=lambda c: abs(c - center_x))
        columns[closest_column].append(line)

    sorted_column_centers = sorted(columns.keys())
    full_text = []
    for center in sorted_column_centers:
        sorted_lines = sorted(columns[center], key=lambda line: line.bbox[1])
        column_text = "\n".join([line.text for line in sorted_lines])
        full_text.append(column_text)
    return "\n\n========== SÜTUN SONU ==========\n\n".join(full_text)

# --- ANA İŞ AKIŞI ---
def main():
    print("--- Hibrit OCR İşlem Hattı Başlatıldı (Tek Süreç Modu) ---")
    try:
        if torch.cuda.is_available(): device = torch.device("cuda")
        elif torch.backends.mps.is_available(): device = torch.device("mps")
        else: device = torch.device("cpu")
        print(f"Kullanılacak cihaz: {device}")

        # Modelleri ve işlemcileri ana süreçte bir kez yükle
        from surya.ocr import run_ocr
        from surya.model.detection.segformer import load_model as load_det_model, load_processor as load_det_processor
        from surya.model.recognition.model import load_model as load_rec_model
        from surya.model.recognition.processor import load_processor as load_rec_processor
        
        print("OCR modelleri ve işlemcileri yükleniyor...")
        det_processor = load_det_processor()
        det_model = load_det_model().to(device)
        rec_processor = load_rec_processor()
        rec_model = load_rec_model().to(device)
        print("✅ Modeller ve işlemciler başarıyla yüklendi.")

        supabase = init_supabase_client()
        if not supabase: return

        bucket_name = 'gazette-pdfs'
        print(f"'{bucket_name}' bucket'ındaki dosyalar listeleniyor...")
        all_files = supabase.storage.from_(bucket_name).list()
        pdf_files_info = [f for f in all_files if f['name'].lower().endswith('.pdf')]
        print(f"Toplam {len(pdf_files_info)} PDF dosyası bulundu.")

        num_to_sample = min(2, len(pdf_files_info))
        if num_to_sample == 0: print("İşlenecek PDF bulunamadı."); return
        selected_files = random.sample(pdf_files_info, num_to_sample)
        print(f"{num_to_sample} adet rastgele PDF test için seçildi.")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_folder = os.path.join(script_dir, "ocr_output")
        os.makedirs(output_folder, exist_ok=True)

        for file_info in selected_files:
            pdf_name = file_info['name']
            print(f"\n--- İşleniyor: {pdf_name} ---")
            pdf_stem = Path(pdf_name).stem
            pdf_output_dir = Path(output_folder) / pdf_stem
            os.makedirs(pdf_output_dir, exist_ok=True)

            pdf_bytes = download_pdf_from_supabase(supabase, bucket_name, pdf_name)
            if not pdf_bytes: continue

            images = pdf_bytes_to_images(pdf_bytes)
            if not images: continue

            processed_announcements = []
            full_raw_text_for_pdf = []

            for i, image in enumerate(images):
                page_num = i + 1
                print(f"  📖 Sayfa {page_num}/{len(images)} işleniyor...")
                page_image_path = pdf_output_dir / f"page_{page_num}.png"
                image.save(page_image_path, "PNG")

                prediction = None
                try:
                    image_pil = Image.open(page_image_path).convert("RGB")
                    predictions = run_ocr([image_pil], [["tr"]], det_model, det_processor, rec_model, rec_processor)
                    prediction = predictions[0]
                    del image_pil
                except Exception as e:
                    print(f"    ❌ HATA: Sayfa {page_num} işlenirken hata oluştu: {e}")
                    traceback.print_exc()

                if prediction and hasattr(prediction, 'text_lines'):
                    page_text = reorder_text_by_columns(prediction.text_lines)
                    full_raw_text_for_pdf.append(page_text)
                    announcements_on_page = parse_structured_text(page_text)
                    for announcement in announcements_on_page:
                        announcement['sayfa_numarasi'] = page_num
                    processed_announcements.extend(announcements_on_page)
                else:
                    print(f"    ⚠️ Sayfa {page_num} işlenemedi, atlanıyor.")

                del image, prediction
                gc.collect()
            
            print(f"🖼️  Görüntüler şuraya kaydedildi: {pdf_output_dir}")
            raw_text_filepath = pdf_output_dir / "raw_text.txt"
            with open(raw_text_filepath, 'w', encoding='utf-8') as f:
                f.write("\n\n--- SAYFA SONU ---\n\n".join(full_raw_text_for_pdf))
            print(f"📄 Ham metin şuraya kaydedildi: {raw_text_filepath}")

            json_output_filepath = pdf_output_dir / "structured_output.json"
            with open(json_output_filepath, 'w', encoding='utf-8') as f:
                json.dump(processed_announcements, f, ensure_ascii=False, indent=4)
            print(f"📄 Yapılandırılmış JSON şuraya kaydedildi: {json_output_filepath}")

            print(f"✅ {pdf_name} başarıyla işlendi ve {len(processed_announcements)} ilan ayrıştırıldı.")

            del pdf_bytes, images, processed_announcements, full_raw_text_for_pdf
            gc.collect()
            if torch.cuda.is_available(): torch.cuda.empty_cache()
            print(f"🧹 Bellek bir sonraki PDF için temizlendi.")

        print(f"\nİşlem tamamlandı. Tüm çıktılar '{output_folder}' klasörüne kaydedildi.")

    except Exception as e:
        print(f"Ana işlem sırasında bir hata oluştu: {e}")
        traceback.print_exc()
    finally:
        print("\n--- Hibrit OCR İşlem Hattı Tamamlandı ---")

if __name__ == "__main__":
    main()
