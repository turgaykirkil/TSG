import SwiftUI
import AppKit
import Combine
import Supabase
import Vision

// MARK: - NLP Data Models

struct NlpParseRequest: Codable {
    let text: String
}

struct NlpEntity: Codable, Hashable, Identifiable {
    var id: String { text + label }
    let text: String
    let label: String
}

struct NlpParseResponse: Codable {
    let organizations: [NlpEntity]
    let locations: [NlpEntity]
    let persons: [NlpEntity]
    let dates: [NlpEntity]
    let money: [NlpEntity]
    let misc: [NlpEntity]
    let registration_number: String?
    let sicil_dosya_no: String?
    let mersis_no: String?
    let trade_name: String?
    let addresses: [String]?
    let masked_ids: [String]?
}

// Çoklu ilân öğesi (backend'in parse_multiple_announcements çıktısı)
struct NlpParsedAnnouncement: Codable, Identifiable {
    // Use a stable id if possible, else synthesize from index + header
    var id: String { "\(index ?? -1)-\(sicil_office_header ?? "")" }
    let index: Int?
    let sicil_office_header: String?
    let original_text: String?
    let organizations: [NlpEntity]
    let locations: [NlpEntity]
    let persons: [NlpEntity]
    let dates: [NlpEntity]
    let money: [NlpEntity]?
    let misc: [NlpEntity]?
    let registration_number: String?
    let sicil_dosya_no: String?
    let mersis_no: String?
    let trade_name: String?
    let addresses: [String]?
    let masked_ids: [String]?
    let phones: [String]?
}

@MainActor
class MainViewModel: ObservableObject {
    @Published var selectedPDF: Data?
    @Published var ocrResult: String = "Henüz OCR işlemi yapılmadı."
    @Published var parsedEntities: NlpParseResponse? // Tekil kullanım için geriye dönük
    @Published var parsedAnnouncements: [NlpParsedAnnouncement]? // Çoklu ilân çıktısı
    @Published var announcements: [Announcement] = []
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    @Published var ocrOutputFolder: URL?
    @Published var ocrBaseFilename: String?
    @Published var nlpRawJson: String?
    private let ocrService: OCRService
    private let supabase: SupabaseClient
    private let pdfBucket = "gazette-pdfs"
    private let parser = GazetteParser()

    init() {
        // AuthViewModel'deki gibi, güvenli yapılandırmadan Supabase istemcisini oluşturuyoruz.
        do {
            let supabaseURLString = try ConfigService.get(key: "SUPABASE_URL")
            let supabaseKey = try ConfigService.get(key: "SUPABASE_KEY")
            
            guard let supabaseURL = URL(string: supabaseURLString) else {
                fatalError("Geçersiz Supabase URL'si. Config.plist dosyasını kontrol edin.")
            }
            
            self.supabase = SupabaseClient(supabaseURL: supabaseURL, supabaseKey: supabaseKey)

        } catch {
            fatalError("Yapılandırma hatası: \(error.localizedDescription). Lütfen Config.plist dosyasını ve içeriğini kontrol edin.")
        }
        
        do {
            self.ocrService = try OCRService()
        } catch {
            fatalError("OCRService başlatılamadı: \(error.localizedDescription)")
        }
    }

    func fetchRandomPDF() {
        isLoading = true
        errorMessage = nil
        selectedPDF = nil
        ocrResult = ""
        parsedEntities = nil
        parsedAnnouncements = nil

        Task {
            do {
                // 1. Bucket'taki tüm dosyaları listele
                let files = try await supabase.storage.from(pdfBucket).list()
                
                // 2. PDF olmayanları veya klasörleri filtrele (varsa)
                let pdfFiles = files.filter { !$0.name.hasSuffix("/") && $0.name.lowercased().hasSuffix(".pdf") }
                
                guard !pdfFiles.isEmpty else {
                    throw URLError(.fileDoesNotExist, userInfo: [NSLocalizedDescriptionKey: "'\(pdfBucket)' bucket'ında hiç PDF dosyası bulunamadı."])
                }
                
                // 3. Rastgele bir dosya seç
                guard let randomFile = pdfFiles.randomElement() else {
                    throw URLError(.cannotCreateFile, userInfo: [NSLocalizedDescriptionKey: "Dosya listesinden rastgele bir seçim yapılamadı."])
                }
                
                // 4. Seçilen dosyayı indir
                ocrResult = "'\(randomFile.name)' dosyası indiriliyor..."
                let fileData = try await supabase.storage.from(pdfBucket).download(path: randomFile.name)
                
                // 5. UI'ı güncelle
                self.selectedPDF = fileData
                self.ocrResult = "'\(randomFile.name)' başarıyla indirildi. OCR için hazır."
                
            } catch {
                self.errorMessage = "PDF alınamadı: \(error.localizedDescription)"
            }
            self.isLoading = false
        }
    }

    func performOCR() {
        guard let pdfData = selectedPDF else {
            errorMessage = "Lütfen önce bir PDF dosyası seçin."
            return
        }
        
        isLoading = true
        errorMessage = nil
        ocrResult = "OCR işlemi başlatıldı, lütfen bekleyin..."
        
        Task {
            do {
                let ocr = try await ocrService.performOCR(on: pdfData)
                // Update UI with raw text and capture output folder/base filename
                self.ocrResult = ocr.text
                self.ocrOutputFolder = ocr.outputFolderURL
                self.ocrBaseFilename = ocr.baseFilename
                
                // After getting raw text, call the NLP service
                await self.parseTextWithNLP(text: ocr.text)
                
            } catch {
                self.errorMessage = "OCR işlemi sırasında bir hata oluştu: \(error.localizedDescription)"
                self.ocrResult = "İşlem başarısız oldu."
            }
            // Final state update on the main thread
            self.isLoading = false
        }
    }
    
    // MARK: - NLP Service Communication
    
    func parseTextWithNLP(text: String) async {
        // Çoklu ilân endpoint'i
        guard let url = URL(string: "http://localhost:5001/api/v1/nlp/parse-announcements") else {
            self.errorMessage = "Invalid NLP service URL"
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let requestBody = NlpParseRequest(text: text)
        do {
            request.httpBody = try JSONEncoder().encode(requestBody)
        } catch {
            self.errorMessage = "Failed to encode NLP request: \(error.localizedDescription)"
            return
        }
        
        do {
            let (data, response) = try await URLSession.shared.data(for: request)
            
            guard let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 else {
                let statusCode = (response as? HTTPURLResponse)?.statusCode ?? -1
                let responseBody = String(data: data, encoding: .utf8) ?? "No response body"
                print("NLP Service Error Response Body: \(responseBody)")
                throw URLError(.badServerResponse, userInfo: [NSLocalizedDescriptionKey: "NLP service returned status code \(statusCode)"])
            }
            
            // Keep raw JSON for copy/save features
            self.nlpRawJson = String(data: data, encoding: .utf8)
            let decodedList = try JSONDecoder().decode([NlpParsedAnnouncement].self, from: data)
            self.parsedAnnouncements = decodedList
            self.parsedEntities = nil // tekil akış artık kullanılmıyor
            print("Successfully parsed announcements: count=\(decodedList.count)")

        } catch {
            self.errorMessage = "NLP service request failed: \(error.localizedDescription)"
            print("NLP service error: \(error)")
        }
    }

    // MARK: - Utilities: Copy & Save NLP JSON
    func copyNlpJsonToClipboard() {
        guard let json = nlpRawJson, !json.isEmpty else {
            self.errorMessage = "Kopyalanacak NLP JSON bulunamadı. Önce OCR ve NLP işlemini çalıştırın."
            return
        }
        let pasteboard = NSPasteboard.general
        pasteboard.clearContents()
        pasteboard.setString(json, forType: .string)
    }

    func saveNlpJsonToDisk() {
        guard let folder = ocrOutputFolder, let base = ocrBaseFilename else {
            self.errorMessage = "OCR çıktı klasörü bulunamadı. Önce OCR çalıştırın."
            return
        }
        let parsedList = parsedAnnouncements ?? []
        let hasList = !parsedList.isEmpty
        let combinedURL = folder.appendingPathComponent("\(base)_nlp.json")
        let rawListURL = folder.appendingPathComponent("\(base)_nlp_list.json")

        struct CombinedNlpOutput: Codable {
            let original_text: String
            let parsed_announcements: [NlpParsedAnnouncement]
            let raw_backend_json: String?
            let output_folder: String
            let base_filename: String
            let created_at: String
        }

        let formatter = ISO8601DateFormatter()
        let payload = CombinedNlpOutput(
            original_text: self.ocrResult,
            parsed_announcements: parsedList,
            raw_backend_json: self.nlpRawJson,
            output_folder: folder.path,
            base_filename: base,
            created_at: formatter.string(from: Date())
        )

        do {
            // 1) Backend'in ham dizi çıktısı (tüm alanlar korunur) - her durumda kaydetmeyi dene
            if let raw = nlpRawJson, !raw.isEmpty, let rawData = raw.data(using: .utf8) {
                try rawData.write(to: rawListURL)
                print("NLP liste JSON kaydedildi: \(rawListURL.path)")
            } else {
                print("Uyarı: raw_backend_json boş, _nlp_list.json yazılamadı.")
            }
            // 2) Meta + struct'lı birleştirilmiş çıktı - yalnızca liste doluysa yaz
            if hasList {
                let data = try JSONEncoder().encode(payload)
                try data.write(to: combinedURL)
                print("NLP JSON kaydedildi: \(combinedURL.path)")
            } else {
                self.errorMessage = "Uyarı: parsedAnnouncements boş. Sadece ham backend listesi kaydedildi."
            }
            // Kaydedilen dosyayı Finder’da göster: liste boşsa ham listeyi göster
            let revealURL = hasList ? combinedURL : rawListURL
            NSWorkspace.shared.activateFileViewerSelecting([revealURL])
        } catch {
            self.errorMessage = "NLP JSON kaydedilemedi: \(error.localizedDescription)"
        }
    }
}
