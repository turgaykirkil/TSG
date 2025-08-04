import Foundation

// MARK: - Data Models

/// Bir ilanın dinamik analizinin sonucunu temsil eder.
struct AnalysisResult {
    let type: String
    let data: [String: Any]
}

/// Bir ilandan çıkarılan temel, standart verileri temsil eder.
struct CoreMetadata {
    let ilanSiraNo: String?
    let mersisNo: String?
    let sicilNo: String?
    let unvan: String?
}

/// Tamamen işlenmiş tek bir ilanı temsil eder.
struct Announcement: Identifiable {
    let id = UUID()
    let rawText: String
    let metadata: CoreMetadata
    let analysisResult: AnalysisResult
}

// MARK: - Gazette Parser

// MARK: - Dynamic Parser Engine

/// Tüm dinamik ayrıştırıcı fonksiyonlar için standart tip.
/// - Parameter textBlock: Analiz edilecek ilan metni.
/// - Returns: Çıkarılan özel verileri içeren bir sözlük.
typealias ParserFunction = (String) -> [String: Any]

/// Bir ayrıştırıcı kuralını tanımlar: anahtar kelimeler ve ilgili ayrıştırıcı fonksiyon.
struct ParserRule {
    let keywords: [String]
    let parser: ParserFunction
}

class GazetteParser {
    
    private var parserRegistry: [ParserRule] = []

    init() {
        setupParserRegistry()
    }

    private func setupParserRegistry() {
        parserRegistry = [
            ParserRule(keywords: ["hisse devri", "pay devri"], parser: self.parseShareTransfer)
            // Gelecekteki diğer kurallar buraya eklenecek
        ]
    }
    
    /// Ham gazete sayfası metnini alır ve içindeki tüm ilanları işleyerek bir `Announcement` dizisi döndürür.
    /// - Parameter pageText: OCR'dan gelen tam sayfa metni.
    /// - Returns: İşlenmiş ilanların bir dizisi.
    func parse(pageText: String) -> [Announcement] {
        let announcementTexts = splitIntoAnnouncements(fullText: pageText)
        
        return announcementTexts.map { textBlock -> Announcement in
            let metadata = extractCoreMetadata(from: textBlock)
            let analysisResult = analyzeAnnouncementType(from: textBlock)
            return Announcement(rawText: textBlock, metadata: metadata, analysisResult: analysisResult)
        }
    }

    /// Verilen metin için uygun ayrıştırıcıyı bulur ve çalıştırır.
    private func analyzeAnnouncementType(from textBlock: String) -> AnalysisResult {
        for rule in parserRegistry {
            for keyword in rule.keywords {
                if textBlock.localizedCaseInsensitiveContains(keyword) {
                    // Eşleşme bulundu, ilgili ayrıştırıcıyı çalıştır ve sonucu döndür.
                    let data = rule.parser(textBlock)
                    // 'analysis_type' anahtarını veriden çıkarıp, AnalysisResult'ın type'ı olarak kullanıyoruz.
                    let type = data["analysis_type"] as? String ?? "unknown"
                    return AnalysisResult(type: type, data: data)
                }
            }
        }
        // Uygun bir ayrıştırıcı bulunamazsa 'unknown' tipinde boş veri döndür.
        return AnalysisResult(type: "unknown", data: [:])
    }
    
    // MARK: - Dynamic Parsers

    /// Hisse devri ilanlarını ayrıştıran fonksiyon.
    private func parseShareTransfer(textBlock: String) -> [String: Any] {
        // TODO: Hisse devri mantığı burada detaylı olarak implemente edilecek.
        // Örnek: Devreden, devralan, hisse adedi gibi bilgiler regex ile çıkarılabilir.
        var data: [String: Any] = ["analysis_type": "share_transfer"]
        
        // Örnek bir veri çıkarma denemesi:
        if let devreden = extractValue(for: "devreden\\s*[:;]\\s*([A-ZÇĞİÖŞÜa-zçğıöşü\\s]+)", in: textBlock) {
            data["transferor"] = devreden.trimmingCharacters(in: .whitespacesAndNewlines)
        }
        
        return data
    }
    
    /// Bir metin bloğunu 'Sicil Müdürlüğü' başlıklarına göre bireysel ilan metinlerine böler.
    private func splitIntoAnnouncements(fullText: String) -> [String] {
        // Ayraç deseni: (S/A)(...) veya (10/A)(...) gibi görünen kod blokları.
        // Bu desen bir ilanın bittiğini ve yenisinin başladığını gösterir.
        // Regex'i Swift String'i içinde doğru yazmak için backslash'lar escape edilmelidir.
        let separatorPattern = "\\(\\S+\\)\\(\\S+\\)"

        guard let regex = try? NSRegularExpression(pattern: separatorPattern, options: []) else {
            return [fullText] // Regex oluşturulamazsa, tüm metni tek parça döndür.
        }

        let range = NSRange(fullText.startIndex..., in: fullText)
        let matches = regex.matches(in: fullText, options: [], range: range)

        if matches.isEmpty {
            // Eğer ayraç bulunamazsa, tüm metni tek bir ilan olarak kabul et.
            // Bu, tek ilanlı sayfalar için bir geri dönüş (fallback) sağlar.
            return [fullText.trimmingCharacters(in: .whitespacesAndNewlines)]
        }

        var announcements: [String] = []
        var lastEnd: String.Index = fullText.startIndex

        for match in matches {
            guard let matchRange = Range(match.range, in: fullText) else { continue }
            
            // Bir önceki ayraçtan bu ayraca kadar olan metni al.
            let announcementText = String(fullText[lastEnd..<matchRange.lowerBound])
            if !announcementText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
                announcements.append(announcementText)
            }
            lastEnd = matchRange.lowerBound
        }

        // Son ayraçtan metnin sonuna kadar olan kısmı da ekle.
        let lastAnnouncementText = String(fullText[lastEnd...])
        if !lastAnnouncementText.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
            announcements.append(lastAnnouncementText)
        }

        // İlk eleman genellikle sayfa başlığı gibi istenmeyen metinler içerir.
        // Bunu temizleyelim.
        if let first = announcements.first, first.contains("ilan Sira No") == false {
             announcements.removeFirst()
        }

        return announcements.map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }.filter { !$0.isEmpty }
    }
    
    /// Tek bir ilan metninden temel meta verileri (MERSİS vb.) çıkarır.
    private func extractCoreMetadata(from textBlock: String) -> CoreMetadata {
        // OCR hatalarına karşı daha toleranslı regex'ler
        let ilanSiraNo = extractValue(for: "[İI]lan S[ıi]ra No\\s*:\\s*([\\w-]+)", in: textBlock)
        let mersisNo = extractValue(for: "Mersis No\\s*:\\s*([\\w-]+)", in: textBlock)
        let sicilNo = extractValue(for: "Ticaret Sicil(?:/Dosya)? No\\s*:\\s*([\\w\\s-]+)", in: textBlock)
        let unvan = extractValue(for: "Ticaret Unvan[ıi]\\s*:\\s*(.*?)(?=\\nAdres:|$)", in: textBlock, options: .dotMatchesLineSeparators)

        return CoreMetadata(
            ilanSiraNo: ilanSiraNo,
            mersisNo: mersisNo,
            sicilNo: sicilNo,
            unvan: unvan?.trimmingCharacters(in: .whitespacesAndNewlines)
        )
    }

    /// Belirli bir regex kalıbı için bir metinden ilk eşleşen grubu çıkaran yardımcı fonksiyon.
    private func extractValue(for pattern: String, in text: String, options: NSRegularExpression.Options = []) -> String? {
        let baseOptions: NSRegularExpression.Options = .caseInsensitive
        let finalOptions = baseOptions.union(options)
        guard let regex = try? NSRegularExpression(pattern: pattern, options: finalOptions) else {
            return nil
        }
        let range = NSRange(text.startIndex..., in: text)
        if let match = regex.firstMatch(in: text, options: [], range: range) {
            if let swiftRange = Range(match.range(at: 1), in: text) {
                return String(text[swiftRange])
            }
        }
        return nil
    }
}
