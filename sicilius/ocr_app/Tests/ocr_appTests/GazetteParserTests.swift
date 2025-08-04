import XCTest
@testable import ocr_app

final class GazetteParserTests: XCTestCase {

    var parser: GazetteParser!

    override func setUp() {
        super.setUp()
        parser = GazetteParser()
    }

    override func tearDown() {
        parser = nil
        super.tearDown()
    }

    func testFullParsingScenario() {
        // Örnek bir gazete sayfası metni
        let sampleGazetteText = """
        T.C. ANKARA TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN
        İlan Sıra No: 12345
        MERSIS No: 0123456789012345
        Ticaret Sicil/Dosya No: 100-A
        Ticaret Unvanı: TEST ANONİM ŞİRKETİ
        Adres: TEST MAHALLESİ NO:1 ANKARA
        İşlem: Şirket normal bir şekilde çalışmaktadır.

        İSTANBUL TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN
        İlan Sıra No: 67890
        MERSIS No: 9876543210987654
        Ticaret Sicil/Dosya No: 200-B
        Ticaret Unvanı: GELİŞTİRME LİMİTED ŞİRKETİ
        Adres: GELİŞTİRME CADDESİ NO:2 İSTANBUL
        Konu: Hisse devri yapılmıştır. Ortaklardan Ahmet Yılmaz, hisselerini Mehmet Kaya'ya devreden olmuştur.
        """

        // 1. Parser'ı çalıştır
        let announcements = parser.parse(pageText: sampleGazetteText)

        // 2. Sonuçları doğrula
        XCTAssertEqual(announcements.count, 2, "İlan sayısı 2 olmalıydı.")

        // 3. İlk ilanın verilerini kontrol et
        if let firstAnn = announcements.first {
            XCTAssertEqual(firstAnn.coreMetadata.sicilNo, "100-A", "İlk ilanın sicil numarası yanlış.")
            XCTAssertEqual(firstAnn.coreMetadata.unvan, "TEST ANONİM ŞİRKETİ", "İlk ilanın unvanı yanlış.")
            XCTAssertEqual(firstAnn.dynamicData["analysis_type"] as? String, "unknown", "İlk ilanın tipi 'unknown' olmalıydı.")
        }

        // 4. İkinci (hisse devri) ilanın verilerini kontrol et
        if announcements.count > 1 {
            let secondAnn = announcements[1]
            XCTAssertEqual(secondAnn.coreMetadata.mersisNo, "9876543210987654", "İkinci ilanın MERSIS numarası yanlış.")
            XCTAssertEqual(secondAnn.dynamicData["analysis_type"] as? String, "share_transfer", "İkinci ilanın tipi 'share_transfer' olmalıydı.")
            XCTAssertNotNil(secondAnn.dynamicData["transferor"], "Devreden bilgisi çıkarılmalıydı.")
            XCTAssertEqual(secondAnn.dynamicData["transferor"] as? String, "Mehmet Kaya'ya", "Devreden bilgisi yanlış çıkarıldı.")
        }
    }
}
