import argparse
import os
import sys
import time
from pathlib import Path
import gc
import multiprocessing

import psutil
from tqdm import tqdm
from pdf2image import convert_from_bytes

# FAZ 1: MPS için ortam değişkenlerini ayarla
# Olası çökme durumlarında işlemlerin CPU'ya düşmesini sağlar.
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

# FAZ 2: MPS bellek yönetimi ve kararlılık ayarları
# Bellek taşmasını ve hataları önlemek için hem düşük hem de yüksek bellek eşiklerini manuel olarak ayarla.
os.environ['PYTORCH_MPS_LOW_WATERMARK_RATIO'] = '0.5'  # Düşük eşik
os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.8' # Yüksek eşik

# FAZ 3: Surya OCR için batch boyutunu ayarla
# Daha küçük batch boyutu, MPS üzerinde daha kararlı çalışmaya yardımcı olur.
os.environ['RECOGNITION_BATCH_SIZE'] = '32' # Varsayılan daha yüksek olabilir, 32 güvenli bir başlangıç.

# Proje kök dizinini sys.path'e ekleyin
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

sys.path.append(str(project_root.parent))

from app.services.ocr_service import OcrService
from app.utils.layout_utils import sort_text_blocks_by_columns

def get_memory_usage(process):
    """Process nesnesinden bellek kullanımını MB cinsinden alır."""
    return process.memory_info().rss / (1024 * 1024)

def get_cpu_temperature():
    """İşlemci sıcaklığını Santigrat derece cinsinden alır."""
    if not hasattr(psutil, "sensors_temperatures"):
        return None
    
    temps = psutil.sensors_temperatures()
    if not temps:
        return None

    # Farklı sistemlerdeki (Linux/macOS/Windows) anahtar isimlerini dene
    # Öncelik: 'coretemp' (Linux), 'k10temp' (AMD), genel CPU etiketleri
    for name in temps:
        if name in ['coretemp', 'k10temp']:
            return temps[name][0].current

    # Etiketlere göre ara (daha genel bir yaklaşım)
    for name, entries in temps.items():
        for entry in entries:
            label = entry.label.lower()
            if 'cpu' in label or 'core' in label or 'package' in label:
                return entry.current

    # Hiçbiri bulunamazsa, bulunan ilk sıcaklık değerini döndür
    for name in temps:
        if temps[name]:
            return temps[name][0].current
            
    return None


def process_single_pdf(pdf_path_str, output_dir_str, device):
    """Tek bir PDF dosyasını işleyen işçi fonksiyonu."""
    pdf_path = Path(pdf_path_str)
    output_dir = Path(output_dir_str)
    output_txt_path = output_dir / f"{pdf_path.stem}.txt"

    # Modelin bu süreçte yüklenmesi
    ocr_service = OcrService(device=device)

    try:
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        
        images = convert_from_bytes(pdf_bytes, dpi=300)
        print(f"'{pdf_path.name}' için {len(images)} sayfa bulundu.")

        ocr_predictions = ocr_service.run_ocr(images=images)
        
        full_text = ""
        for i, prediction in enumerate(ocr_predictions):
            page_text = sort_text_blocks_by_columns(prediction, page_num=i + 1)
            full_text += page_text
            full_text += "\n\n--- SAYFA SONU ---\n\n"

        output_txt_path.write_text(full_text, encoding='utf-8')
        print(f"'{pdf_path.name}' başarıyla işlendi ve '{output_txt_path}' dosyasına kaydedildi.")

    except Exception as e:
        print(f"HATA: '{pdf_path.name}' dosyası işlenemedi. Sebep: {e}")


def process_batch(
    input_dir: Path,
    output_dir: Path,
    delay: int,
    max_temp: int,
    resume_temp: int,
    check_interval: int
):
    """
    Belirtilen bir klasördeki tüm PDF dosyalarını işler ve sonuçları
    metin dosyaları olarak kaydeder.
    """
    process = psutil.Process(os.getpid())
    start_mem = get_memory_usage(process)
    tqdm.write(f"Başlangıç Bellek Kullanımı: {start_mem:.2f} MB")

    print(f"Giriş Klasörü: {input_dir}")
    print(f"Çıkış Klasörü: {output_dir}")
    print("-" * 50)

    # Çıkış klasörü yoksa oluştur
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_files = sorted(list(input_dir.glob("*.pdf")))
    tqdm.write(f"Toplam {len(pdf_files)} adet PDF dosyası bulundu. İşlem başlıyor...")
    
    # Sıcaklık kontrolü için sensörleri kontrol et
    has_sensors = True
    if max_temp and not get_cpu_temperature():
        tqdm.write("UYARI: Bu sistemde sıcaklık sensörleri okunamıyor. Sıcaklık kontrolü devre dışı bırakıldı.")
        has_sensors = False

    overall_start_time = time.time()
    total_pages_processed = 0
    processed_files = 0

    for pdf_path in tqdm(pdf_files, desc="PDF'ler işleniyor"):
        output_txt_path = output_dir / f"{pdf_path.stem}.txt"
        if output_txt_path.exists():
            tqdm.write(f"'{output_txt_path.name}' zaten var, geçiliyor.")
            continue

        # Sıcaklık kontrolü
        if max_temp and has_sensors:
            current_temp = get_cpu_temperature()
            if current_temp and current_temp >= max_temp:
                tqdm.write(f"\nUYARI: İşlemci sıcaklığı ({current_temp:.1f}°C) maksimum limiti ({max_temp}°C) aştı. Soğuması için duraklatılıyor...")
                while current_temp and current_temp >= resume_temp:
                    time.sleep(check_interval)
                    current_temp = get_cpu_temperature()
                    if current_temp:
                        tqdm.write(f"Mevcut sıcaklık: {current_temp:.1f}°C... (Devam etmek için < {resume_temp}°C olmalı)")
                if current_temp:
                    tqdm.write(f"BİLGİ: İşlemci sıcaklığı ({current_temp:.1f}°C) güvenli seviyeye düştü. İşleme devam ediliyor.")

        # Her PDF için yeni bir süreç başlat
        process = multiprocessing.Process(target=process_single_pdf, args=(str(pdf_path), str(output_dir), "mps"))
        process.start()
        process.join() # Sürecin bitmesini bekle

        processed_files += 1
        # Sayfa sayısını almak için artık PDF'i burada okumamız gerekiyor
        # Şimdilik bu kısmı basitleştirelim, raporlama daha sonra düzeltilebilir.

        if delay > 0:
            time.sleep(delay)

    overall_end_time = time.time()
    total_duration = overall_end_time - overall_start_time

    tqdm.write("\n--------------------------------------------------")
    tqdm.write("✅ Toplu İşlem Raporu")
    tqdm.write("--------------------------------------------------")
    tqdm.write(f"Toplam Süre: {total_duration:.2f} saniye")
    tqdm.write(f"İşlenen PDF Sayısı: {processed_files}")
    # Diğer raporlama metrikleri, süreç izolasyonu nedeniyle basitleştirildi.


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
    parser.add_argument(
        "--max-temp",
        type=int,
        default=None,
        help="İşlemi duraklatmak için maksimum CPU sıcaklığı (°C). Belirtilmezse kontrol yapılmaz."
    )
    parser.add_argument(
        "--resume-temp",
        type=int,
        default=None,
        help="İşleme devam etmek için CPU sıcaklığı (°C). max-temp'ten 5 derece düşük olarak ayarlanır."
    )
    parser.add_argument(
        "--check-interval",
        type=int,
        default=15,
        help="Yüksek sıcaklıkta bekleme sırasında kontrol aralığı (saniye)."
    )

    args = parser.parse_args()

    input_path = Path(args.input_dir)
    output_path = Path(args.output_dir)

    if not input_path.is_dir():
        print(f"Hata: Giriş yolu '{input_path}' ({input_path.resolve()}) geçerli bir klasör değil.")
    else:
        # Sıcaklık kontrolü için ön kontrol ve yapılandırma
        if args.max_temp and not get_cpu_temperature():
            print("UYARI: Bu sistemde sıcaklık sensörleri okunamıyor. Sıcaklık kontrolü devre dışı bırakıldı.")
            args.max_temp = None

        if args.max_temp and not args.resume_temp:
            args.resume_temp = args.max_temp - 5
            print(f"BİLGİ: --resume-temp belirtilmedi. Otomatik olarak {args.resume_temp}°C olarak ayarlandı.")

        process_batch(
            input_dir=input_path, 
            output_dir=output_path, 
            delay=args.delay, 
            max_temp=args.max_temp,
            resume_temp=args.resume_temp,
            check_interval=args.check_interval
        )
