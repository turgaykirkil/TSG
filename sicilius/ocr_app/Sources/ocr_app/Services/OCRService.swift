import Foundation
import Vision
import PDFKit
import AppKit


enum OCRError: Error {
    case resourceLoadingError(file: String)
    case pdfConversionError
    case imageConversionError
    case recognitionError(Error)
    case noTextFound
}

struct OCRResult {
    let text: String
    let outputFolderURL: URL
    let baseFilename: String
}

struct OCRService {
    init() throws {
        // Initialization logic can be added here if needed in the future.
    }

    func performOCR(on pdfData: Data) async throws -> OCRResult {
        guard let pdfDocument = PDFDocument(data: pdfData) else {
            throw OCRError.pdfConversionError
        }

        // Disk yazımı kaldırıldı: FileManager kullanımı gereksiz

        // Proje kök dizinini bulmak için mevcut dosyanın konumunu kullan
        let currentFileURL = URL(fileURLWithPath: #file)
        // 5 seviye yukarı çıkarak 'sicilius' ana dizinine ulaş
        // .../sicilius/ocr_app/Sources/ocr_app/Services/ -> .../sicilius/
        let projectRootURL = currentFileURL
            .deletingLastPathComponent()
            .deletingLastPathComponent()
            .deletingLastPathComponent()
            .deletingLastPathComponent()
            .deletingLastPathComponent()

        let outputFolderURL = projectRootURL.appendingPathComponent("ocr_ciktilari")
        let timestamp = Int(Date().timeIntervalSince1970)
        let baseFilename = "ocr_sonuc_\(timestamp)"
        // Diskte klasör oluşturma devre dışı: çıktı dosyası yazılmayacak

        var fullRecognizedText = "Sicilius OCR Sonucu - \(Date())\n"

        for i in 0..<pdfDocument.pageCount {
            guard let page = pdfDocument.page(at: i) else { continue }
            
            let pageRect = page.bounds(for: .mediaBox)
            let nsImage = NSImage(size: pageRect.size)
            nsImage.lockFocus()
            guard let context = NSGraphicsContext.current?.cgContext else {
                nsImage.unlockFocus()
                throw OCRError.imageConversionError
            }
            page.draw(with: .mediaBox, to: context)
            nsImage.unlockFocus()
            
            guard let cgImage = nsImage.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
                throw OCRError.imageConversionError
            }

            // PNG kaydetme kaldırıldı (istek üzerine). Sadece OCR yapılacak.

            // Sütun-temelli OCR (ColumnOCRService) ile sayfayı işle
            let languages = ["tr-TR", "en-US"]
            let columnOCR = ColumnOCRService()
            let pageText: String
            do {
                pageText = try columnOCR.recognizePageWithColumns(cgImage: cgImage, languages: languages)
            } catch {
                // Hata olursa mevcut tek-parça OCR'e geri dön
                let requestHandler = VNImageRequestHandler(cgImage: cgImage, options: [:])
                let request = VNRecognizeTextRequest()
                request.recognitionLevel = .accurate
                request.usesLanguageCorrection = true
                request.recognitionLanguages = languages
                try requestHandler.perform([request])
                let observations = request.results ?? []
                pageText = observations.compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
            }
            
            fullRecognizedText.append("\n\n--- Sayfa \(i + 1) ---\n\n")
            fullRecognizedText.append(pageText)
        }

        // Disk yazımı kaldırıldı: toplu metin dosyaya yazılmıyor

        // PNG kaydetme kaldırıldığı için imageSaveCount kontrolü de kaldırıldı.

        return OCRResult(text: fullRecognizedText, outputFolderURL: outputFolderURL, baseFilename: baseFilename)
    }
}

