import XCTest
@testable import ocr_app

final class MinimalDecodeTests: XCTestCase {

    func testDecodeMinimalAnnouncements() throws {
        // Minimal backend çıktısına benzer örnek JSON (bazı alanlar özellikle eksik bırakıldı)
        let json = """
        [
          {
            "index": 0,
            "sicil_office_header": "T.C. ANKARA TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN",
            "original_text": "Orijinal metin A",
            "sicil_dosya_no": "100-A",
            "trade_name": "TEST ANONİM ŞİRKETİ",
            "old_trade_name": null,
            "addresses": ["TEST MAH. NO:1 ANKARA"],
            "hususlar": ["Kuruluş"],
            "belgeler": "Dilekçe"
          },
          {
            "index": 1,
            "sicil_office_header": "İSTANBUL TİCARET SİCİLİ MÜDÜRLÜĞÜ'NDEN",
            "original_text": "Orijinal metin B",
            "sicil_dosya_no": null,
            "trade_name": "GELİŞTİRME LİMİTED ŞİRKETİ",
            "addresses": [],
            "belgeler": ""
          }
        ]
        """.data(using: .utf8)!

        let decoded = try JSONDecoder().decode([NlpParsedAnnouncement].self, from: json)
        XCTAssertEqual(decoded.count, 2)
        // İlk kayıt
        let first = decoded[0]
        XCTAssertEqual(first.index, 0)
        XCTAssertEqual(first.sicil_dosya_no, "100-A")
        XCTAssertEqual(first.trade_name, "TEST ANONİM ŞİRKETİ")
        XCTAssertEqual(first.addresses ?? [], ["TEST MAH. NO:1 ANKARA"])
        XCTAssertEqual(first.hususlar ?? [], ["Kuruluş"])
        XCTAssertEqual(first.belgeler, "Dilekçe")
        // İkinci kayıt (birçok alan eksik gelebilir)
        let second = decoded[1]
        XCTAssertEqual(second.index, 1)
        XCTAssertNil(second.sicil_dosya_no)
        XCTAssertEqual(second.trade_name, "GELİŞTİRME LİMİTED ŞİRKETİ")
        XCTAssertTrue((second.addresses ?? []).isEmpty)
        XCTAssertEqual(second.belgeler, "")
        // Opsiyonel diziler nil olduğunda çökmemeli
        XCTAssertNil(second.persons)
        XCTAssertNil(second.organizations)
    }
}
