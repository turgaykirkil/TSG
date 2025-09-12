import Foundation

// NOT: 2025-09 itibarıyla ayrıştırma işlemi backend'e taşınmıştır.
// Bu dosya yalnızca geriye dönük tipler için tutulmaktadır.
// Lütfen yerel parser'ı KULLANMAYIN; backend NLP servislerini kullanın.

// Represents a single announcement parsed from the gazette.
@available(*, deprecated, message: "Yerel ayrıştırıcı kullanım dışı. Backend NLP JSON'u kullanılmalıdır.")
struct Announcement: Identifiable, Hashable {
    let id = UUID()
    var rawText: String
    var title: String
    var registrationNumber: String
    var mersisNumber: String
}

@available(*, deprecated, message: "Yerel ayrıştırıcı kullanım dışı. Backend NLP JSON'u kullanılmalıdır.")
struct GazetteParser {

    // Main parsing function
    func parse(fullText: String) -> [Announcement] {
        let announcementTexts = splitAnnouncements(from: fullText)
        
        let announcements = announcementTexts.compactMap { textBlock -> Announcement? in
            let title = extractTitle(from: textBlock) ?? "Unvan Bulunamadı"
            let regNo = extractRegistrationNumber(from: textBlock) ?? "Sicil No Bulunamadı"
            let mersis = extractMersisNumber(from: textBlock) ?? "MERSIS Bulunamadı"
            
            // Only return announcements that seem to have content
            if title == "Unvan Bulunamadı" && regNo == "Sicil No Bulunamadı" {
                return nil
            }
            
            return Announcement(
                rawText: textBlock,
                title: title,
                registrationNumber: regNo,
                mersisNumber: mersis
            )
        }
        
        return announcements
    }

    // Splits the entire OCR text into individual announcement blocks.
    private func splitAnnouncements(from fullText: String) -> [String] {
        // Correctly escaped regex for Swift strings.
        // Daha toleranslı ayırıcı: OCR kaynaklı "SÌCILI" gibi varyasyonları da yakalamak için [İIÌ] kullanıldı.
        // Ayrıca MÜDÜRLÜĞÜ/MÜDÜRLÜGÜ ve MEMURLUĞU varyasyonları desteklenir.
        let separatorPattern = "(?mi)^\\s*(?!Eski\\b)(?:T\\.?C\\.?\\s*)?.{0,80}?T[İIÌ]CARET(?:\\s+|\\R){0,3}S[İIÌ]C[İIÌ]L[İIÌ](?:\\s+|\\R){0,3}(?:M[ÜU]D[ÜU]RL[ÜU][ĞG][ÜU]['’]?N[DT][EA]N|MEMURLU[ĞG][UÜ]['’]?N[DT][EA]N)\\s*$"
        
        guard let regex = try? NSRegularExpression(pattern: separatorPattern, options: [.caseInsensitive, .anchorsMatchLines]) else {
            return [fullText]
        }
        
        let nsRange = NSRange(fullText.startIndex..<fullText.endIndex, in: fullText)
        let matches = regex.matches(in: fullText, options: [], range: nsRange)
        
        if matches.isEmpty {
            return [fullText] // Return as one block if no separators are found
        }

        var announcements: [String] = []
        var lastEndIndex = fullText.startIndex

        for match in matches {
            guard let matchRange = Range(match.range, in: fullText) else { continue }
            let announcementBlock = fullText[lastEndIndex..<matchRange.lowerBound]
            if !announcementBlock.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
                 announcements.append(String(announcementBlock))
            }
            lastEndIndex = matchRange.lowerBound
        }
        
        // Append the final announcement (the one that starts with the last separator found)
        let finalBlock = fullText[lastEndIndex..<fullText.endIndex]
        announcements.append(String(finalBlock))
        
        // The first element is often page header/footer garbage before the first real announcement header.
        if let first = announcements.first, !first.contains("T.C.") {
            return Array(announcements.dropFirst())
        }

        return announcements
    }
    
    // Extracts the company title (Ticaret Unvanı).
    private func extractTitle(from text: String) -> String? {
        let pattern = "(?:Ticaret|Tiearet|Tlearet)\\s+Unvanı\\s*[:>]?\\s*([\\s\\S]+?)(?:Adres\\s*:|Tescil\\s+Edilen|Yukarıda\\s+bilgileri|Müdürler|Yönetim|İşletme\\s+Konusu|$)"
        return extractFirstMatch(with: pattern, from: text)
    }

    // Extracts the Trade Registry Number (Ticaret Sicil No).
    private func extractRegistrationNumber(from text: String) -> String? {
        let pattern = "Ticaret\\s+Sicil(?:/Dosya)?\\s+No\\s*:\\s*([\\w-]+)"
        return extractFirstMatch(with: pattern, from: text)
    }
    
    // Extracts the MERSIS Number.
    private func extractMersisNumber(from text: String) -> String? {
        let pattern = "MERSIS\\s+No\\s*:\\s*(\\d+)"
        return extractFirstMatch(with: pattern, from: text)
    }

    // A helper function to execute a regex and return the first capture group.
    private func extractFirstMatch(with pattern: String, from text: String) -> String? {
        do {
            let regex = try NSRegularExpression(pattern: pattern, options: [.caseInsensitive, .dotMatchesLineSeparators])
            let nsRange = NSRange(text.startIndex..<text.endIndex, in: text)
            
            if let match = regex.firstMatch(in: text, options: [], range: nsRange) {
                if let range = Range(match.range(at: 1), in: text) {
                    // Clean up the result: remove HTML tags, extra spaces, and newlines.
                    var extractedText = String(text[range])
                    extractedText = extractedText.replacingOccurrences(of: "<[^>]+>", with: "", options: .regularExpression)
                    extractedText = extractedText.replacingOccurrences(of: "\n", with: " ").trimmingCharacters(in: .whitespacesAndNewlines)
                    // Condense multiple spaces into one.
                    extractedText = extractedText.replacingOccurrences(of: "\\\\s{2,}", with: " ", options: .regularExpression)
                    return extractedText
                }
            }
        } catch {
            print("Regex error: \(error.localizedDescription)")
        }
        return nil
    }
}
