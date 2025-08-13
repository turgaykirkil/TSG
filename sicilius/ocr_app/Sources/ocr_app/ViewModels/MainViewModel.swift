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
    // İşlem modu ve toplu/otomatik akış durumları
    enum ProcessingMode: String, CaseIterable, Identifiable {
        case manual = "Manuel"
        case automatic = "Otomatik"
        var id: String { rawValue }
    }
    @Published var processingMode: ProcessingMode = .manual
    @Published var manualCount: Int = 1
    @Published var isAutoRunning: Bool = false
    private var processingTask: Task<Void, Never>?
    private let ocrService: OCRService
    private let supabase: SupabaseClient
    private let pdfBucket = "gazette-pdfs"
    private let parser = GazetteParser()
    // Supabase Storage'dan indirilen aktif PDF'nin yolunu (bucket içi path) takip ederiz
    private var currentStoragePath: String?

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
                self.currentStoragePath = randomFile.name
                
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
    
    // Async varyant: akış içi ardışık kullanım için
    func performOCRAsync(data: Data) async {
        isLoading = true
        errorMessage = nil
        ocrResult = "OCR işlemi başlatıldı, lütfen bekleyin..."
        do {
            let ocr = try await ocrService.performOCR(on: data)
            self.ocrResult = ocr.text
            self.ocrOutputFolder = ocr.outputFolderURL
            self.ocrBaseFilename = ocr.baseFilename
            await self.parseTextWithNLP(text: ocr.text)
        } catch {
            self.errorMessage = "OCR işlemi sırasında bir hata oluştu: \(error.localizedDescription)"
            self.ocrResult = "İşlem başarısız oldu."
        }
        self.isLoading = false
    }

    // Tek adımlık indirme + OCR + NLP + JSON kaydetme
    func fetchAndProcessOnce() async {
        do {
            // Dosyaları listele ve rastgele PDF indir
            let files = try await supabase.storage.from(pdfBucket).list()
            let pdfFiles = files.filter { !$0.name.hasSuffix("/") && $0.name.lowercased().hasSuffix(".pdf") }
            guard let randomFile = pdfFiles.randomElement() else {
                throw URLError(.fileDoesNotExist, userInfo: [NSLocalizedDescriptionKey: "Bucket'ta PDF bulunamadı."])
            }
            self.ocrResult = "'\(randomFile.name)' dosyası indiriliyor..."
            let fileData = try await supabase.storage.from(pdfBucket).download(path: randomFile.name)
            // Seçimi güncelle ve OCR'ı çalıştır
            self.selectedPDF = fileData
            self.currentStoragePath = randomFile.name
            await self.performOCRAsync(data: fileData)
            // NLP JSON kaydet
            self.saveNlpJsonToDisk()
        } catch {
            self.errorMessage = "İşlem başarısız: \(error.localizedDescription)"
        }
    }

    // Manuel mod: belirlenen adet kadar sırayla çalıştır
    func startManualBatch() {
        guard !isAutoRunning, processingTask == nil else { return }
        let count = max(1, manualCount)
        processingTask = Task { [weak self] in
            guard let self else { return }
            for _ in 0..<count {
                if Task.isCancelled { break }
                await self.fetchAndProcessOnce()
            }
            await MainActor.run {
                self.processingTask = nil
            }
        }
    }

    // Otomatik mod: durdurulana kadar döngü
    func startAutomaticProcessing() {
        guard !isAutoRunning else { return }
        isAutoRunning = true
        processingTask = Task { [weak self] in
            guard let self else { return }
            while !Task.isCancelled {
                await self.fetchAndProcessOnce()
            }
            await MainActor.run {
                self.isAutoRunning = false
                self.processingTask = nil
            }
        }
    }

    func stopAutomaticProcessing() {
        processingTask?.cancel()
        processingTask = nil
        isAutoRunning = false
    }

    // Tek buton davranışı: PDF Getir / Durdur
    func handleFetchButtonTapped() {
        switch processingMode {
        case .manual:
            startManualBatch()
        case .automatic:
            if isAutoRunning { stopAutomaticProcessing() } else { startAutomaticProcessing() }
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
        // Disk yazımı kaldırıldı: Artık JSON/TXT dosyaları kaydedilmiyor.
        // Sadece backend'e ingest yapılır.
        do {
            guard let raw = self.nlpRawJson, !raw.isEmpty else {
                print("Ingest atlandı: raw_backend_json boş.")
                return
            }
            let itemsData = Data(raw.utf8)
            let itemsAny = try JSONSerialization.jsonObject(with: itemsData, options: [])
            guard let itemsArray = itemsAny as? [Any], !itemsArray.isEmpty else {
                print("Ingest atlandı: items boş veya dizi değil.")
                return
            }

            var payloadObj: [String: Any] = [
                "raw_text": self.ocrResult,
                "items": itemsArray
            ]
            if let path = self.currentStoragePath, !path.isEmpty {
                payloadObj["source_file"] = [
                    "bucket": self.pdfBucket,
                    "path": path
                ]
                payloadObj["delete_after_ingest"] = true
            }
            let postData = try JSONSerialization.data(withJSONObject: payloadObj, options: [])

            guard let url = URL(string: "http://127.0.0.1:5001/api/v1/nlp/ingest-structured") else {
                print("Ingest hata: URL oluşturulamadı.")
                return
            }
            var req = URLRequest(url: url)
            req.httpMethod = "POST"
            req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
            req.httpBody = postData

            print("Ingest-structured POST gönderiliyor... items=\(itemsArray.count)")
            URLSession.shared.dataTask(with: req) { data, resp, err in
                if let err = err {
                    print("Ingest-structured hata: \(err.localizedDescription)")
                    return
                }
                if let http = resp as? HTTPURLResponse {
                    print("Ingest-structured yanıt: status=\(http.statusCode)")
                }
                if let data = data, let body = String(data: data, encoding: .utf8) {
                    print("Ingest-structured gövde: \n\(body)")
                }
            }.resume()
        } catch {
            print("Ingest hazırlık hatası: \(error.localizedDescription)")
        }
    }
}
