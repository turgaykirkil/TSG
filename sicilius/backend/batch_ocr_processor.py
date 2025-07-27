import argparse
import os
import time
from pathlib import Path
from tqdm import tqdm

# Proje kök dizinini sys.path'e ekleyerek app modülünün bulunmasını sağla
import sys
# Bu betiğin bulunduğu dizinden iki üst dizine çıkarak proje kökünü bul
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from app.services.ocr_service import get_surya_ocr_preview


def process_batch(input_dir: Path, output_dir: Path):
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

    # OCR servisi bir kereliğine (singleton) başlatılacağı için ilk başlatma biraz sürebilir.
    # Bu yüzden ilk dosyadan önce bir uyarı verelim.
    print("OCR modelleri yükleniyor... Bu işlem ilk çalıştırmada biraz zaman alabilir.")
    start_time_total = time.time()

    # Dosyaları tqdm ile bir ilerleme çubuğu göstererek işle
    for pdf_path in tqdm(pdf_files, desc="PDF'ler işleniyor"):
        try:
            # PDF dosyasını byte olarak oku
            with open(pdf_path, "rb") as f:
                pdf_content = f.read()

            # OCR işlemini gerçekleştir
            preview_response = get_surya_ocr_preview(
                pdf_content=pdf_content, file_name=pdf_path.name
            )

            # Sonuçları birleştirerek metin içeriği oluştur
            full_text = ""
            for page in preview_response.pages:
                for line in page.lines:
                    full_text += line.text + "\n"
                full_text += "\n--- Sayfa Sonu ---\n\n"

            # Sonucu bir .txt dosyasına yaz
            output_txt_path = output_dir / f"{pdf_path.stem}.txt"
            with open(output_txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)

        except Exception as e:
            tqdm.write(f"HATA: '{pdf_path.name}' dosyası işlenemedi. Sebep: {e}")

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
        help="OCR sonuçlarının metin dosyaları olarak kaydedileceği klasörün yolu."
    )

    args = parser.parse_args()

    input_path = Path(args.input_dir)
    output_path = Path(args.output_dir)

    if not input_path.is_dir():
        print(f"Hata: Giriş yolu '{input_path}' geçerli bir klasör değil.")
    else:
        process_batch(input_path, output_path)
