CREATE OR REPLACE FUNCTION tr_normalize(original_text text)
RETURNS text AS $$
DECLARE
    normalized_text text;
BEGIN
    IF original_text IS NULL THEN
        RETURN NULL;
    END IF;
    normalized_text := lower(original_text);
    normalized_text := replace(normalized_text, 'ı', 'i');
    normalized_text := replace(normalized_text, 'ğ', 'g');
    normalized_text := replace(normalized_text, 'ü', 'u');
    normalized_text := replace(normalized_text, 'ş', 's');
    normalized_text := replace(normalized_text, 'ö', 'o');
    normalized_text := replace(normalized_text, 'ç', 'c');
    normalized_text := replace(normalized_text, 'â', 'a');
    normalized_text := replace(normalized_text, 'î', 'i');
    RETURN normalized_text;
END;
$$ LANGUAGE plpgsql IMMUTABLE;
