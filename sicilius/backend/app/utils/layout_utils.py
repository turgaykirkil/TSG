def sort_text_blocks_by_columns(prediction, page_num=1):
    """
    OCR tarafından tespit edilen metin bloklarını, genellikle gazete sayfalarında olduğu gibi,
    yatay konumlarına göre iki sütuna ayırır ve her sütunu dikey olarak sıralar.

    Args:
        prediction: Surya OCR'dan gelen ve 'text_lines' içeren tek bir sayfa sonuç nesnesi.
                      Her text_line'ın bir 'bbox' (koordinatlar) ve 'text' alanı olmalıdır.
        page_num: Bilgilendirme amaçlı sayfa numarası (şu an için kullanılmıyor).

    Returns:
        Sütunlara ayrılmış ve sıralanmış metni içeren bir string.
    """
    if not prediction or not hasattr(prediction, 'text_lines') or not prediction.text_lines:
        return ""

    text_lines = prediction.text_lines

    # Sayfanın genişliğini en sağdaki metin bloğundan tahmin et
    try:
        page_width = max(line.bbox[2] for line in text_lines)
        column_threshold = page_width / 2
    except (ValueError, IndexError):
        # Eğer bbox bilgisi yoksa veya liste boşsa, basit sıralama yap
        return "\n".join([line.text for line in text_lines])

    left_col = []
    right_col = []

    for line in text_lines:
        # Metin bloğunun yatay merkezini bul
        horizontal_center = (line.bbox[0] + line.bbox[2]) / 2
        if horizontal_center < column_threshold:
            left_col.append(line)
        else:
            right_col.append(line)

    # Her sütunu dikey konumlarına göre sırala (y0 koordinatı)
    left_col.sort(key=lambda b: b.bbox[1])
    right_col.sort(key=lambda b: b.bbox[1])

    # Sıralanmış metinleri birleştir
    sorted_text = ""
    for line in left_col:
        sorted_text += line.text + "\n"
    
    sorted_text += "\n\n"

    for line in right_col:
        sorted_text += line.text + "\n"

    return sorted_text
