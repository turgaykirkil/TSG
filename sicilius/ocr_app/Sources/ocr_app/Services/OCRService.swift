import Foundation
import Vision
import PDFKit


enum OCRError: Error {
    case resourceLoadingError(file: String)
    case pdfConversionError
    case imageConversionError
    case recognitionError(Error)
    case noTextFound
}

struct OCRService {
    init() throws {
        // Initialization logic can be added here if needed in the future.
    }

    func performOCR(on pdfData: Data) async throws -> String {
        guard let pdfDocument = PDFDocument(data: pdfData) else {
            throw OCRError.pdfConversionError
        }

        let fileManager = FileManager.default

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
        try fileManager.createDirectory(at: outputFolderURL, withIntermediateDirectories: true, attributes: nil)

        var fullRecognizedText = "Sicilius OCR Sonucu - \(Date())\n"
        var imageSaveCount = 0

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

            // Resmi PNG olarak kaydet
            let imageURL = outputFolderURL.appendingPathComponent("\(baseFilename)_sayfa_\(i + 1).png")
            let imageRepresentation = NSBitmapImageRep(cgImage: cgImage)
            if let pngData = imageRepresentation.representation(using: .png, properties: [:]) {
                try pngData.write(to: imageURL)
                imageSaveCount += 1
            }

            // Vision ile metin tanıma
            let requestHandler = VNImageRequestHandler(cgImage: cgImage, options: [:])
            let request = VNRecognizeTextRequest()
            request.recognitionLevel = .accurate
            request.usesLanguageCorrection = true
            request.recognitionLanguages = ["tr-TR", "en-US"]

            try requestHandler.perform([request])

            guard let observations = request.results else {
                continue
            }
            
            let pageText = observations.compactMap { $0.topCandidates(1).first?.string }.joined(separator: "\n")
            
            fullRecognizedText.append("\n\n--- Sayfa \(i + 1) ---\n\n")
            fullRecognizedText.append(pageText)
        }

        // Toplu metin sonucunu dosyaya yaz
        let txtURL = outputFolderURL.appendingPathComponent("\(baseFilename)_tum_sayfalar.txt")
        try fullRecognizedText.write(to: txtURL, atomically: true, encoding: .utf8)

        if fullRecognizedText.isEmpty && imageSaveCount == 0 {
            throw OCRError.noTextFound
        }

        return "\(imageSaveCount) sayfa resmi ve 1 metin dosyası başarıyla '\(outputFolderURL.path)' klasörüne kaydedildi."
    }
}

