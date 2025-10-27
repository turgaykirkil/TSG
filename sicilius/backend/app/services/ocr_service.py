from PIL import Image
from typing import List, Dict, Tuple
from pdf2image import convert_from_bytes
from app.schemas.ocr_preview_response import OcrPreviewResponse, OcrPagePreview, OcrTextLine
from io import BytesIO
import base64
import logging
import os
from pathlib import Path
import pytesseract
from pytesseract import Output

logger = logging.getLogger(__name__)

def _merge_bbox(b1: Tuple[int, int, int, int], b2: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    x1 = min(b1[0], b2[0])
    y1 = min(b1[1], b2[1])
    x2 = max(b1[2], b2[2])
    y2 = max(b1[3], b2[3])
    return (x1, y1, x2, y2)



def get_surya_ocr_preview(pdf_content: bytes, file_name: str) -> OcrPreviewResponse:
    """
    Tesseract tabanlı hızlı OCR önizlemesi.
    Surya/torch bağımlılığı olmadan çalışır ve her satır için yaklaşık bbox döndürür.
    """
    logger.info(f"Processing PDF preview via Tesseract for file: {file_name}")
    try:
        # DEBUG çıktı klasörü
        output_dir = Path("test_output")
        os.makedirs(output_dir, exist_ok=True)
        base_filename = Path(file_name).stem

        images = convert_from_bytes(pdf_content)
        logger.info(f"Converted PDF to {len(images)} images.")

        preview_pages: List[OcrPagePreview] = []

        for i, pil_image in enumerate(images):
            page_num = i + 1
            # Debug imajı kaydet
            img_debug_path = output_dir / f"{base_filename}_page_{page_num}.png"
            pil_image.save(img_debug_path, "PNG")

            # Base64 görüntü üret
            buffered = BytesIO()
            pil_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # Tesseract ile satır çıkarımı (line seviyesinde bbox birleştirme)
            data = pytesseract.image_to_data(pil_image, lang='tur', output_type=Output.DICT)
            n = len(data.get('text', []))
            groups: Dict[Tuple[int, int, int], Dict[str, object]] = {}
            for idx in range(n):
                txt = (data['text'][idx] or '').strip()
                try:
                    conf = float(data['conf'][idx]) if data['conf'][idx] not in (None, '', '-1') else -1.0
                except Exception:
                    conf = -1.0
                if not txt or conf < 0:
                    continue
                key = (int(data.get('block_num', [0])[idx] or 0), int(data.get('par_num', [0])[idx] or 0), int(data.get('line_num', [0])[idx] or 0))
                l = int(data.get('left', [0])[idx] or 0)
                t = int(data.get('top', [0])[idx] or 0)
                w = int(data.get('width', [0])[idx] or 0)
                h = int(data.get('height', [0])[idx] or 0)
                bbox = (l, t, l + w, t + h)
                if key not in groups:
                    groups[key] = {'text': txt, 'bbox': bbox}
                else:
                    groups[key]['text'] = (groups[key]['text'] + ' ' + txt).strip()
                    groups[key]['bbox'] = _merge_bbox(groups[key]['bbox'], bbox)  # type: ignore

            # satırları yukarıdan aşağıya sırala
            lines: List[OcrTextLine] = []
            for (_k, v) in groups.items():
                bb = v['bbox']  # type: ignore
                x1, y1, x2, y2 = int(bb[0]), int(bb[1]), int(bb[2]), int(bb[3])
                lines.append(OcrTextLine(text=str(v['text']), bbox=(x1, y1, x2, y2)))
            lines.sort(key=lambda ln: ln.bbox[1])

            # debug metin
            text_debug_path = output_dir / f"{base_filename}_page_{page_num}.txt"
            with open(text_debug_path, 'w', encoding='utf-8') as f:
                for ln in lines:
                    f.write(ln.text + "\n")

            preview_pages.append(OcrPagePreview(
                page_number=page_num,
                image_base64=f"data:image/png;base64,{img_str}",
                lines=lines
            ))

        logger.info(f"Tesseract OCR preview generated for {len(preview_pages)} pages.")
        return OcrPreviewResponse(pages=preview_pages)
    except Exception as e:
        logger.error(f"Failed to process PDF preview for {file_name}: {e}", exc_info=True)
        raise
