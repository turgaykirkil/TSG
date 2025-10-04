import SwiftUI
import AppKit
import Combine
import Supabase
import Vision

// MARK: - NLP Data Models

struct NlpParseRequest: Codable {
    let text: String
}

// Backend'in döndürdüğü entities_full içindeki minimal alanlar
struct NlpEntitiesFull: Codable {
    let hususlar: [String]?
    let belgeler: String?
}

struct NlpEntity: Codable, Hashable, Identifiable {
    var id: String { text + label }
    let text: String
    let label: String
    // Kişiler için kişi satırına gömülü maskeli kimlik (opsiyonel)
    let masked_ids: String?
}
// Backend aksiyonları için model
struct NlpAction: Codable, Hashable, Identifiable {
    var id: String {
        let t = (type ?? "UNKNOWN")
        let d = (details ?? "")
        let p = (parties ?? []).joined(separator: "|")
        return t + "-" + d + "-" + p
    }
    let type: String?
    let details: String?
    let parties: [String]?
    let amounts: [String]?
    let effective_date: String?
    let devralan: String?
}

struct NlpParseResponse: Codable {
    let organizations: [NlpEntity]?
    let locations: [NlpEntity]?
    let persons: [NlpEntity]?
    let dates: [NlpEntity]?
    let money: [NlpEntity]?
    let misc: [NlpEntity]?
    let registration_number: String?
    let sicil_dosya_no: String?
    let mersis_no: String?
    let trade_name: String?
    let old_trade_name: String?
    let addresses: [String]?
    let old_addresses: [String]?
    let masked_ids: [String]?
    let ilan_sira_no: [String]?
    let hususlar: [String]?
    let belgeler: String?
    let entities_full: NlpEntitiesFull?
}

// Çoklu ilân öğesi (backend'in parse_multiple_announcements çıktısı)
struct NlpParsedAnnouncement: Codable, Identifiable {
    // Use a stable id if possible, else synthesize from index + header
    var id: String { "\(index ?? -1)-\(sicil_office_header ?? "")" }
    let index: Int?
    let sicil_office_header: String?
    let original_text: String?
    let start_offset: Int?
    let end_offset: Int?
    let organizations: [NlpEntity]?
    let locations: [NlpEntity]?
    let persons: [NlpEntity]?
    let dates: [NlpEntity]?
    let money: [NlpEntity]?
    let misc: [NlpEntity]?
    // Yeni: backend aksiyonları
    let actions: [NlpAction]?
    let registration_number: String?
    let sicil_dosya_no: String?
    let mersis_no: String?
    let trade_name: String?
    let old_trade_name: String?
    let addresses: [String]?
    let old_addresses: [String]?
    let phones: [String]?
    let ilan_sira_no: [String]?
    let hususlar: [String]?
    let belgeler: String?
    let entities_full: NlpEntitiesFull?
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
    // Minimal çoklu liste JSON (yedek/karşılaştırma amaçlı)
    @Published var nlpMinimalJson: String?
    // İntegration/ingest için: structured çoklu liste (daha önce nlpRawJson olarak kullanılıyordu)
    @Published var nlpStructuredJson: String?
    // Ingest sonrası PDF silme tercihi (UI üzerinden ayarlanır)
    @Published var deleteAfterIngest: Bool = true
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
    private let nlpBaseURL: URL
    private let pdfBucket = "gazette-pdfs"
    // Yerel GazetteParser kaldırıldı: Ayrıştırma tamamen backend tarafında yapılır.
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

        // NLP Base URL (Config.plist: NLP_BASE_URL). Yoksa localhost'a düş.
        let nlpBase: String = (try? ConfigService.get(key: "NLP_BASE_URL")) ?? "http://127.0.0.1:5001"
        guard let nlpURL = URL(string: nlpBase) else {
            fatalError("Geçersiz NLP_BASE_URL: \(nlpBase)")
        }
        self.nlpBaseURL = nlpURL
        
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
                let ocr = try await Task.detached(priority: .userInitiated) { [pdfData, ocrService] in
                    return try await ocrService.performOCR(on: pdfData)
                }.value
                await MainActor.run {
                    // UI güncelle
                    self.ocrResult = ocr.text
                    self.ocrOutputFolder = ocr.outputFolderURL
                    self.ocrBaseFilename = ocr.baseFilename
                }
                // NLP çağrısını ana aktörden ayır
                Task.detached { [weak self] in
                    await self?.parseTextWithNLP(text: ocr.text)
                }
                
            } catch {
                await MainActor.run {
                    self.errorMessage = "OCR işlemi sırasında bir hata oluştu: \(error.localizedDescription)"
                    self.ocrResult = "İşlem başarısız oldu."
                }
            }
            // Final state update on the main thread
            await MainActor.run { self.isLoading = false }
        }
    }
    
    // Async varyant: akış içi ardışık kullanım için
    func performOCRAsync(data: Data) async {
        isLoading = true
        errorMessage = nil
        ocrResult = "OCR işlemi başlatıldı, lütfen bekleyin..."
        do {
            if Task.isCancelled { self.isLoading = false; return }
            let ocr = try await Task.detached(priority: .userInitiated) { [data, ocrService] in
                return try await ocrService.performOCR(on: data)
            }.value
            await MainActor.run {
                self.ocrResult = ocr.text
                self.ocrOutputFolder = ocr.outputFolderURL
                self.ocrBaseFilename = ocr.baseFilename
            }
            // Otomatik akış için NLP'yi tamamlamayı bekle
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
            if Task.isCancelled { return }
            let fileData = try await supabase.storage.from(pdfBucket).download(path: randomFile.name)
            // Seçimi güncelle ve OCR'ı çalıştır
            self.selectedPDF = fileData
            self.currentStoragePath = randomFile.name
            if Task.isCancelled { return }
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
                await Task.yield()
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
                await Task.yield()
                // Döngüler arası küçük gecikme ile CPU/Ağ yükünü yumuşat
                try? await Task.sleep(nanoseconds: 200_000_000) // 200ms
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
        // Gerekli sabitleri ana aktörden kopyala
        let baseURL = self.nlpBaseURL
        let requestBody = NlpParseRequest(text: text)
        // Ağ ve decode işlemlerini arka planda çalıştır
        let result = await Task.detached(priority: .userInitiated) { () -> (structured: String?, decoded: [NlpParsedAnnouncement]?, minimal: String?, netMs: Int, decMs: Int, err: String?) in
            // 1) Structured çoklu
            let listURL = baseURL
                .appendingPathComponent("api")
                .appendingPathComponent("v1")
                .appendingPathComponent("nlp")
                .appendingPathComponent("parse-announcements")
            var listReq = URLRequest(url: listURL)
            listReq.httpMethod = "POST"
            listReq.addValue("application/json", forHTTPHeaderField: "Content-Type")
            listReq.timeoutInterval = 120
            do { listReq.httpBody = try JSONEncoder().encode(requestBody) } catch {
                return (nil, nil, nil, 0, 0, "encode error: \(error.localizedDescription)")
            }
            do {
                let t0 = CFAbsoluteTimeGetCurrent()
                let (data, response) = try await URLSession.shared.data(for: listReq)
                let tNet = Int((CFAbsoluteTimeGetCurrent() - t0) * 1000)
                guard let http = response as? HTTPURLResponse, http.statusCode == 200 else {
                    let statusCode = (response as? HTTPURLResponse)?.statusCode ?? -1
                    let body = String(data: data, encoding: .utf8) ?? ""
                    return (nil, nil, nil, tNet, 0, "list http \(statusCode): \(body)")
                }
                let structured = String(data: data, encoding: .utf8)
                let tDec0 = CFAbsoluteTimeGetCurrent()
                let decoded = try JSONDecoder().decode([NlpParsedAnnouncement].self, from: data)
                let tDec = Int((CFAbsoluteTimeGetCurrent() - tDec0) * 1000)

                // 2) Minimal
                let minimalURL = baseURL
                    .appendingPathComponent("api")
                    .appendingPathComponent("v1")
                    .appendingPathComponent("nlp")
                    .appendingPathComponent("parse-announcements-minimal")
                var minimalReq = URLRequest(url: minimalURL)
                minimalReq.httpMethod = "POST"
                minimalReq.addValue("application/json", forHTTPHeaderField: "Content-Type")
                minimalReq.timeoutInterval = 120
                do { minimalReq.httpBody = try JSONEncoder().encode(requestBody) } catch {
                    return (structured, decoded, nil, tNet, tDec, "minimal encode error: \(error.localizedDescription)")
                }
                do {
                    let (mdata, mresp) = try await URLSession.shared.data(for: minimalReq)
                    guard let mhttp = mresp as? HTTPURLResponse, mhttp.statusCode == 200 else {
                        let statusCode = (mresp as? HTTPURLResponse)?.statusCode ?? -1
                        let body = String(data: mdata, encoding: .utf8) ?? ""
                        return (structured, decoded, nil, tNet, tDec, "minimal http \(statusCode): \(body)")
                    }
                    let minimal = String(data: mdata, encoding: .utf8)
                    return (structured, decoded, minimal, tNet, tDec, nil)
                } catch {
                    return (structured, decoded, nil, tNet, tDec, "minimal error: \(error.localizedDescription)")
                }
            } catch {
                return (nil, nil, nil, 0, 0, "list error: \(error.localizedDescription)")
            }
        }.value

        // UI güncellemeleri
        await MainActor.run {
            if let err = result.err {
                self.errorMessage = err
            } else {
                self.errorMessage = nil
            }
            if let s = result.structured { self.nlpStructuredJson = s }
            if let d = result.decoded { self.parsedAnnouncements = d; self.parsedEntities = nil }
            if let m = result.minimal { self.nlpMinimalJson = m }
            if result.decoded != nil {
                print("[NLP:list] İstek=\(result.netMs) ms, Decode=\(result.decMs) ms, Count=\(result.decoded?.count ?? 0)")
            }
        }
    }

    // NLP'yi mevcut OCR metni ile manuel olarak yeniden çalıştır
    func reRunNLP() async {
        if isLoading { return }
        let txt = self.ocrResult.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !txt.isEmpty else {
            self.errorMessage = "Yeniden NLP için OCR metni boş. Önce OCR çalıştırın veya ham metni girin."
            return
        }
        self.errorMessage = nil
        self.isLoading = true
        defer { self.isLoading = false }
        await self.parseTextWithNLP(text: txt)
    }

    // MARK: - Utilities: Copy & Save NLP JSON
    func copyNlpJsonToClipboard() {
        // Öncelik: structured çoklu; yoksa minimal gösterim
        let json = self.nlpStructuredJson?.isEmpty == false ? self.nlpStructuredJson! : (self.nlpMinimalJson ?? "")
        guard !json.isEmpty else {
            self.errorMessage = "Kopyalanacak JSON bulunamadı. Önce OCR ve NLP işlemini çalıştırın."
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
            // Ingest için structured çoklu liste gereklidir
            guard let raw = self.nlpStructuredJson, !raw.isEmpty else {
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
            }
            // Kullanıcı tercihi: ingest sonrasında PDF'nin silinip silinmeyeceği
            payloadObj["delete_after_ingest"] = self.deleteAfterIngest
            let postData = try JSONSerialization.data(withJSONObject: payloadObj, options: [])

            let url = nlpBaseURL
                .appendingPathComponent("api")
                .appendingPathComponent("v1")
                .appendingPathComponent("nlp")
                .appendingPathComponent("ingest-structured")
            var req = URLRequest(url: url)
            req.httpMethod = "POST"
            req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
            req.httpBody = postData
            req.timeoutInterval = 120

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
