import argparse
import os
from pathlib import Path
import time
import gc
import torch
import sys
from tqdm import tqdm
from pdf2image import convert_from_bytes
from app.services.ocr_service import OcrService

# FAZ 1: MPS için ortam değişkenlerini ayarla
# Olası çökme durumlarında işlemlerin CPU'ya düşmesini sağlar.
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# Proje kök dizinini sys.path'e ekleyerek app modülünün bulunmasını sağla
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

def process_batch(input_dir: Path, output_dir: Path, delay: int):
    """
    Belirtilen bir klasördeki tüm PDF dosyalarını işler ve sonuçları
    başka bir klasöre metin dosyaları olarak kaydeder.
    """
    print(f"Giriş Klasörü: {input_dir}")
    print(f"Çıkış Klasörü: {output_dir}")
    print("-" * 50)

    # Çıkış klasörünün var olduğundan emin ol
    output_dir.mkdir(exist_ok=True)

    # Giriş klasöründeki PDF dosyalarını bul
    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"'{input_dir}' klasöründe işlenecek PDF dosyası bulunamadı.")
        return

    print(f"Toplam {len(pdf_files)} adet PDF dosyası bulundu. İşlem başlıyor...")

    start_time_total = time.time()

    print(f"Döngüye girmeden önce {len(pdf_files)} dosya işlenmek üzere hazır.")
    # Dosyaları tqdm ile bir ilerleme çubuğu göstererek işle
    for pdf_path in tqdm(pdf_files, desc="PDF'ler işleniyor"):
        ocr_service = None
        try:
            pdf_file_name = pdf_path.name
            tqdm.write(f"\n{pdf_file_name} için OCR servisi başlatılıyor...")
            # FAZ 1: Stabilite ayarlarıyla MPS'i tekrar etkinleştir
            ocr_service = OcrService(device="mps")

            with open(pdf_path, "rb") as f:
                pdf_content = f.read()
            
            images = convert_from_bytes(pdf_content)
            tqdm.write(f"{len(images)} sayfa bulundu ve görüntülere dönüştürüldü.")

            ocr_predictions = ocr_service.run_ocr(images=images)

            if not ocr_predictions:
                tqdm.write(f"UYARI: {pdf_path.name} için OCR sonucu bulunamadı.")
                continue

            full_text = ""
            for page_result in ocr_predictions:
                if page_result and hasattr(page_result, 'text_lines') and page_result.text_lines:
                    for line in page_result.text_lines:
                        full_text += line.text + "\n"
                full_text += "\n--- Sayfa Sonu ---\n\n"

            output_txt_path = output_dir / f"{pdf_path.stem}.txt"
            with open(output_txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            
            tqdm.write(f"{pdf_path.name} başarıyla işlendi ve kaydedildi.")

        except Exception as e:
            tqdm.write(f"HATA: '{pdf_path.name}' dosyası işlenemedi. Sebep: {e}")
        finally:
            tqdm.write("Kaynaklar temizleniyor...")
            if 'ocr_service' in locals() and ocr_service is not None:
                del ocr_service
            if 'images' in locals() and images is not None:
                del images
            if 'ocr_predictions' in locals() and ocr_predictions is not None:
                del ocr_predictions

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            # FAZ 1: MPS belleğini temizle
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()
            gc.collect()
            tqdm.write("Temizlik tamamlandı.")
            if delay > 0:
                tqdm.write(f"{delay} saniye bekleniyor...")
                time.sleep(delay)

    end_time_total = time.time()
    print("\n" + "-" * 50)
    print(f"\u2705 Toplu işlem tamamlandı!")
    print(f"Toplam süre: {end_time_total - start_time_total:.2f} saniye.")
    print(f"Sonuçlar '{output_dir}' klasörüne kaydedildi.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Bir klasördeki PDF dosyalarını toplu olarak işleyen OCR betiği."
    )
    parser.add_argument(
        "input_dir",
        type=str,
        help="İşlenecek PDF dosyalarını içeren klasörün yolu."
    )
    parser.add_argument(
        "output_dir",
        type=str,
        nargs='?', 
        default="test_output",
        help="OCR sonuçlarının metin dosyaları olarak kaydedileceği klasörün yolu. (Varsayılan: test_output)"
    )
    parser.add_argument(
        "--delay",
        type=int,
        default=0,
        help="Dosyalar arasında beklenecek saniye cinsinden süre. (Varsayılan: 0)"
    )

    args = parser.parse_args()

    input_path = Path(args.input_dir)
    output_path = Path(args.output_dir)

    if not input_path.is_dir():
        print(f"Hata: Giriş yolu '{input_path}' ({input_path.resolve()}) geçerli bir klasör değil.")
    else:
        process_batch(input_path, output_path, args.delay)
