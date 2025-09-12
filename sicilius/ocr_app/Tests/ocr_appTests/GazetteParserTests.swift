import XCTest
@testable import ocr_app

final class GazetteParserTests: XCTestCase {

    // Ayrıştırma backend'e taşındı. Bu nedenle eski yerel parser testleri devre dışıdır.
    // Backend entegrasyon testleri ayrı bir hedefte ve ortamda çalıştırılacaktır.

    override func setUp() {
        super.setUp()
    }

    override func tearDown() {
        super.tearDown()
    }

    func testParsingMovedToBackend() throws {
        throw XCTSkip("Yerel GazetteParser kullanımı kaldırıldı; ayrıştırma backend servisi ile yapılmaktadır.")
    }
}
