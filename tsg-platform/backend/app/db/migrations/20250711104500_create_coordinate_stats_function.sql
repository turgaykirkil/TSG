CREATE OR REPLACE FUNCTION get_coordinate_statistics()
RETURNS json
LANGUAGE plpgsql
AS $$
DECLARE
    total_companies_count BIGINT;
    coordinated_companies_count BIGINT;
    conflicting_companies_count BIGINT;
    result JSON;
BEGIN
    -- 1. Toplam şirket sayısını al
    SELECT count(*) INTO total_companies_count FROM public.companies;

    -- 2. Adresi ve koordinatı null olmayan şirketlerin sayısını al
    SELECT count(*)
    INTO coordinated_companies_count
    FROM public.companies
    WHERE address IS NOT NULL AND koordinat IS NOT NULL;

    -- 3. Çakışan şirketleri bul
    WITH address_conflicts AS (
        -- Birden fazla benzersiz koordinatla ilişkili adresleri bul
        SELECT address
        FROM public.companies
        WHERE address IS NOT NULL AND koordinat IS NOT NULL
        GROUP BY address
        HAVING count(DISTINCT koordinat::text) > 1
    ),
    coordinate_conflicts AS (
        -- Birden fazla benzersiz adresle ilişkili koordinatları bul
        SELECT koordinat
        FROM public.companies
        WHERE address IS NOT NULL AND koordinat IS NOT NULL
        GROUP BY koordinat
        HAVING count(DISTINCT address) > 1
    ),
    conflicting_sicils AS (
        -- Çakışan bir adrese sahip şirketlerin tüm sicil_no'larını al
        SELECT sicil_no
        FROM public.companies c
        WHERE c.address IN (SELECT address FROM address_conflicts)
        UNION
        -- Çakışan bir koordinata sahip şirketlerin tüm sicil_no'larını al
        SELECT sicil_no
        FROM public.companies c
        WHERE c.koordinat::text IN (SELECT koordinat::text FROM coordinate_conflicts)
    )
    -- Benzersiz çakışan şirketlerin sayısını say
    SELECT count(*) INTO conflicting_companies_count FROM conflicting_sicils;

    -- 4. JSON sonucunu oluştur
    result := json_build_object(
        'total', total_companies_count,
        'coordinated', coordinated_companies_count,
        'uncoordinated', total_companies_count - coordinated_companies_count,
        'conflicts', conflicting_companies_count
    );

    RETURN result;
END;
$$;
