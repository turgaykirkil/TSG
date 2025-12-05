import SwiftUI
import AppKit
import Combine
import Vision
import Foundation

// MARK: - NLP Data Models

struct NlpParseRequest: Codable {
    let text: String
}

// MARK: - Backend Helpers

extension MainViewModel {
    private func loadAccessToken() -> String? {
        guard let data = KeychainService.load(service: keychainServiceIdentifier, account: keychainAccountIdentifier),
              let token = String(data: data, encoding: .utf8),
              !token.isEmpty else {
            return nil
        }
        return token
    }

    private func makeError(_ message: String, code: Int = -1) -> NSError {
        NSError(domain: "com.sicilius.ocr-app", code: code, userInfo: [NSLocalizedDescriptionKey: message])
    }

    private func makeApiURL(_ pathComponents: [String], queryItems: [URLQueryItem]? = nil) -> URL? {
        var url = apiBaseURL
        for component in pathComponents {
            url.appendPathComponent(component)
        }
        var components = URLComponents(url: url, resolvingAgainstBaseURL: false)
        if let queryItems, !queryItems.isEmpty {
            components?.queryItems = queryItems
        }
        return components?.url
    }

    private func makeAuthorizedRequest(
        url: URL,
        method: String = "GET",
        body: Data? = nil,
        contentType: String? = nil
    ) throws -> URLRequest {
        guard let token = loadAccessToken() else {
            throw makeError("Yetkilendirme token'ı bulunamadı. Lütfen yeniden giriş yapın.")
        }

        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        if let body {
            request.httpBody = body
            request.setValue(contentType ?? "application/json", forHTTPHeaderField: "Content-Type")
        }
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        request.timeoutInterval = 120
        return request
    }

    private func listStorageObjects(limit: Int, prefix: String? = nil) async throws -> [StorageObjectResponse] {
        var queryItems: [URLQueryItem] = [URLQueryItem(name: "limit", value: "\(limit)")]
        if let prefix, !prefix.isEmpty {
            queryItems.append(URLQueryItem(name: "prefix", value: prefix))
        }
        guard let url = makeApiURL(["api", "v1", "storage", "announcements"], queryItems: queryItems) else {
            throw makeError("Geçersiz storage API URL")
        }
        let request = try makeAuthorizedRequest(url: url)
        let (data, response) = try await urlSession.data(for: request)
        guard let http = response as? HTTPURLResponse else {
            throw makeError("Geçersiz storage yanıtı")
        }
        guard (200..<300).contains(http.statusCode) else {
            let body = String(data: data, encoding: .utf8) ?? ""
            throw makeError("Storage listeleme başarısız. status=\(http.statusCode) body=\(body)", code: http.statusCode)
        }
        return try jsonDecoder.decode([StorageObjectResponse].self, from: data)
    }

    private func downloadPDF(at storagePath: String) async throws -> Data {
        let segments = storagePath.split(separator: "/").map(String.init)
        guard !segments.isEmpty else {
            throw makeError("Geçersiz dosya yolu")
        }
        guard let metaURL = makeApiURL(["api", "v1", "storage", "announcements"] + segments + ["download"]) else {
            throw makeError("Geçersiz download URL")
        }
        let request = try makeAuthorizedRequest(url: metaURL)
        let (data, response) = try await urlSession.data(for: request)
        guard let http = response as? HTTPURLResponse else {
            throw makeError("Geçersiz download yanıtı")
        }
        guard (200..<300).contains(http.statusCode) else {
            let body = String(data: data, encoding: .utf8) ?? ""
            throw makeError("İndirme URL'i alınamadı. status=\(http.statusCode) body=\(body)", code: http.statusCode)
        }
        let presigned = try jsonDecoder.decode(PresignedUrlResponse.self, from: data)
        guard let presignedURL = URL(string: presigned.url) else {
            throw makeError("Geçersiz presigned URL")
        }
        let (fileData, fileResponse) = try await urlSession.data(from: presignedURL)
        if let httpFile = fileResponse as? HTTPURLResponse, !(200..<300).contains(httpFile.statusCode) {
            throw makeError("PDF indirme başarısız. status=\(httpFile.statusCode)", code: httpFile.statusCode)
        }
        return fileData
    }
}

extension MainViewModel {
    private struct AnnouncementRow: Decodable {
        let id: String
        let publication_date: String?
        let issue_number: Int?
        let page_number: Int?
        let pdf_url: String?
    }

    private struct StorageObjectResponse: Decodable {
        let object_name: String
        let size: Int
        let last_modified: Date?

        private enum CodingKeys: String, CodingKey { case object_name, size, last_modified }

        init(from decoder: Decoder) throws {
            let container = try decoder.container(keyedBy: CodingKeys.self)
            object_name = try container.decode(String.self, forKey: .object_name)
            size = try container.decodeIfPresent(Int.self, forKey: .size) ?? 0
            if let dateString = try container.decodeIfPresent(String.self, forKey: .last_modified) {
                let formatter = ISO8601DateFormatter()
                formatter.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
                if let parsed = formatter.date(from: dateString) {
                    last_modified = parsed
                } else {
                    last_modified = ISO8601DateFormatter().date(from: dateString)
                }
            } else {
                last_modified = nil
            }
        }
    }

    private struct PresignedUrlResponse: Decodable {
        let url: String
        let expires_in: Int
    }

    private func resolveAnnouncementForCurrentFile() async {
        let baseURL = self.nlpBaseURL
        guard let path = self.currentStoragePath, !path.isEmpty else { return }
        // Sadece dosya adını yolla
        let fileName = (path as NSString).lastPathComponent
        let resolveBase = baseURL
            .appendingPathComponent("api")
            .appendingPathComponent("v1")
            .appendingPathComponent("nlp")
            .appendingPathComponent("resolve-announcement")
        var comps = URLComponents(url: resolveBase, resolvingAgainstBaseURL: false)!
        comps.queryItems = [URLQueryItem(name: "file_name", value: fileName)]
        guard let url = comps.url else { return }
        var req = URLRequest(url: url)
        req.httpMethod = "GET"
        req.timeoutInterval = 30
        do {
            let (data, resp) = try await URLSession.shared.data(for: req)
            guard let http = resp as? HTTPURLResponse else { return }
            if http.statusCode == 200 {
                if let obj = try? JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                    let ann = obj["id"] as? String
                    let pub = obj["publication_date"] as? String
                    let iss = obj["issue_number"] as? Int
                    let page = obj["page_number"] as? Int
                    let purl = obj["pdf_url"] as? String
                    self.resolvedAnnouncementId = ann
                    self.resolvedPublicationDate = pub
                    self.resolvedIssueNumber = iss
                    self.resolvedPageNumber = page
                    self.resolvedPdfUrl = purl
                    print("[PDF] resolve-announcement: id=\(ann ?? "-") issue=\(iss ?? -1) page=\(page ?? -1)")
                }
            } else {
                // 404 veya diğerleri: state temizle (fallback regex devrede kalır)
                self.resolvedAnnouncementId = nil
                self.resolvedPublicationDate = nil
                self.resolvedIssueNumber = nil
                self.resolvedPageNumber = nil
                self.resolvedPdfUrl = nil
            }
        } catch {
            // Sessiz düş: regex fallback çalışır
            self.resolvedAnnouncementId = nil
            self.resolvedPublicationDate = nil
            self.resolvedIssueNumber = nil
            self.resolvedPageNumber = nil
            self.resolvedPdfUrl = nil
        }
    }

    private func fetchAnnouncementRow() async throws -> AnnouncementRow {
        guard let url = makeApiURL(["api", "v1", "announcements"], queryItems: [URLQueryItem(name: "limit", value: "50")]) else {
            throw makeError("Geçersiz announcements API URL")
        }
        let request = try makeAuthorizedRequest(url: url)
        let (data, response) = try await urlSession.data(for: request)
        guard let http = response as? HTTPURLResponse else {
            throw makeError("Geçersiz sunucu yanıtı")
        }
        guard (200..<300).contains(http.statusCode) else {
            let body = String(data: data, encoding: .utf8) ?? ""
            throw makeError("Announcements isteği başarısız. status=\(http.statusCode) body=\(body)", code: http.statusCode)
        }
        let rows = try jsonDecoder.decode([AnnouncementRow].self, from: data)
        guard let pick = rows.randomElement() else {
            throw makeError("Announcement listesi boş")
        }
        return pick
    }

    private func deriveStoragePath(from pdfURL: String?) -> String? {
        guard let pdfURL, !pdfURL.isEmpty else { return nil }
        if let range = pdfURL.range(of: "/gazette-pdfs/") {
            let after = pdfURL[range.upperBound...]
            let s = String(after)
            if let q = s.firstIndex(of: "?") { return String(s[..<q]) }
            return s
        }
        return nil
    }

    private func fetchFromAnnouncementsAndDownload() async throws -> (fileName: String, data: Data) {
        let row = try await fetchAnnouncementRow()
        await MainActor.run {
            self.resolvedAnnouncementId = row.id
            self.resolvedPublicationDate = row.publication_date
            self.resolvedIssueNumber = row.issue_number
            self.resolvedPageNumber = row.page_number
            self.resolvedPdfUrl = row.pdf_url
        }
        guard let storagePath = deriveStoragePath(from: row.pdf_url) else {
            throw URLError(.fileDoesNotExist, userInfo: [NSLocalizedDescriptionKey: "pdf_url'den storage path çıkarılamadı."])
        }
        let fileData = try await downloadPDF(at: storagePath)
        return (storagePath, fileData)
    }

    private func downloadRandomFromStorage() async throws -> (fileName: String, data: Data) {
        let objects = try await listStorageObjects(limit: 500)
        let pdfFiles = objects.filter { !$0.object_name.hasSuffix("/") && $0.object_name.lowercased().hasSuffix(".pdf") }
        guard let randomFile = pdfFiles.randomElement() else {
            throw makeError("Storage içerisinde PDF bulunamadı.")
        }
        let data = try await downloadPDF(at: randomFile.object_name)
        // REST başarısızsa resolve meta olmadan devam; backend ingest dosya adına göre çözer
        return (randomFile.object_name, data)
    }
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
    private let apiBaseURL: URL
    private let nlpBaseURL: URL
    private let urlSession: URLSession
    private let jsonDecoder: JSONDecoder
    private let pdfBucket = "gazette-pdfs"
    private let keychainServiceIdentifier = "com.sicilius.ocr-app"
    private let keychainAccountIdentifier = "user_access_token"
    // Yerel GazetteParser kaldırıldı: Ayrıştırma tamamen backend tarafında yapılır.
    // Supabase Storage'dan indirilen aktif PDF'nin yolunu (bucket içi path) takip ederiz
    private var currentStoragePath: String?
    // Resolve endpoint’inden gelen id+meta (indirilen dosya adına göre)
    private var resolvedAnnouncementId: String?
    private var resolvedPublicationDate: String?
    private var resolvedIssueNumber: Int?
    private var resolvedPageNumber: Int?
    private var resolvedPdfUrl: String?

    init() {
        let apiBase: String = (try? ConfigService.get(key: "API_BASE_URL")) ?? "http://127.0.0.1:5002"
        guard let apiURL = URL(string: apiBase) else {
            fatalError("Geçersiz API_BASE_URL: \(apiBase)")
        }
        self.apiBaseURL = apiURL

        let nlpBase: String = (try? ConfigService.get(key: "NLP_BASE_URL")) ?? "http://127.0.0.1:5002"
        guard let nlpURL = URL(string: nlpBase) else {
            fatalError("Geçersiz NLP_BASE_URL: \(nlpBase)")
        }
        self.nlpBaseURL = nlpURL

        self.urlSession = URLSession(configuration: .default)
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        self.jsonDecoder = decoder

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
                // 1. Announcements'tan bir satır seç ve indirilecek dosyayı belirle
                let (path, fileData) = try await fetchFromAnnouncementsAndDownload()
                // 2. UI'ı güncelle
                self.selectedPDF = fileData
                self.ocrResult = "'\(path)' başarıyla indirildi. OCR için hazır."
                self.currentStoragePath = path
                print("[PDF] İndirildi: file_name=\(path) storage_path=\(self.currentStoragePath ?? "-")")
            } catch {
                // Fallback: Storage list + indir
                do {
                    let (path, fileData) = try await downloadRandomFromStorage()
                    self.selectedPDF = fileData
                    self.ocrResult = "'\(path)' başarıyla indirildi. OCR için hazır."
                    self.currentStoragePath = path
                    print("[PDF] İndirildi (fallback): file_name=\(path) storage_path=\(self.currentStoragePath ?? "-")")
                    // Fallback'te dosya adına göre ilân id+meta çöz
                    await self.resolveAnnouncementForCurrentFile()
                } catch {
                    self.errorMessage = "PDF alınamadı: \(error.localizedDescription)"
                }
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
        // İndirilmiş PDF adı/ yolu mevcutsa OCR başlangıcında logla
        print("[PDF] OCR başlıyor: file_name=\(self.currentStoragePath ?? "bilinmiyor")")
        
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
        // İndirilmiş PDF adı/ yolu mevcutsa OCR başlangıcında logla (async varyant)
        print("[PDF] OCR başlıyor (async): file_name=\(self.currentStoragePath ?? "bilinmiyor")")
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
            // Announcements'tan bir satır seç ve indirilecek dosyayı belirle
            let (path, fileData) = try await fetchFromAnnouncementsAndDownload()
            if Task.isCancelled { return }
            // Seçimi güncelle ve OCR'ı çalıştır
            self.selectedPDF = fileData
            self.currentStoragePath = path
            print("[PDF] İndirildi: file_name=\(path) storage_path=\(self.currentStoragePath ?? "-")")
            if Task.isCancelled { return }
            print("[PDF] OCR başlıyor (pipeline): file_name=\(self.currentStoragePath ?? "bilinmiyor")")
            await self.performOCRAsync(data: fileData)
            // NLP JSON kaydet
            self.saveNlpJsonToDisk()
        } catch {
            // Fallback: Storage list + indir
            do {
                let (path, fileData) = try await downloadRandomFromStorage()
                if Task.isCancelled { return }
                self.selectedPDF = fileData
                self.currentStoragePath = path
                print("[PDF] İndirildi (fallback): file_name=\(path) storage_path=\(self.currentStoragePath ?? "-")")
                // Fallback'te dosya adına göre ilân id+meta çöz
                await self.resolveAnnouncementForCurrentFile()
                if Task.isCancelled { return }
                print("[PDF] OCR başlıyor (pipeline): file_name=\(self.currentStoragePath ?? "bilinmiyor")")
                await self.performOCRAsync(data: fileData)
                self.saveNlpJsonToDisk()
            } catch {
                self.errorMessage = "İşlem başarısız: \(error.localizedDescription)"
            }
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
        guard let token = loadAccessToken() else {
            await MainActor.run {
                self.errorMessage = "Yetkilendirme token'ı bulunamadı. Lütfen yeniden giriş yapın."
            }
            return
        }
        let session = self.urlSession
        let encoder = JSONEncoder()
        // 1) Öncelik: resolve endpoint’inden gelen id
        let announcementId: String? = self.resolvedAnnouncementId
        // 2) Meta: announcement_id yoksa meta ile side-write yapılabilmesi için query param göndereceğiz
        let resolvedPub = self.resolvedPublicationDate
        let resolvedIssue = self.resolvedIssueNumber
        let resolvedPage = self.resolvedPageNumber
        let resolvedPdf = self.resolvedPdfUrl
        // 3) Dosya adı: resolve başarısızsa isimle eşleştirme için backend'e iletelim
        let storagePath = self.currentStoragePath
        let fileNameParam: String? = {
            guard let sp = storagePath, !sp.isEmpty else { return nil }
            return (sp as NSString).lastPathComponent
        }()
        // Fallback devre dışı: resolve başarısızsa announcementId boş kalır; backend ingest dosya adına göre çözer.
        // Ağ ve decode işlemlerini arka planda çalıştır
        let bearerToken = token
        let result = await Task.detached(priority: .userInitiated) { () -> (structured: String?, decoded: [NlpParsedAnnouncement]?, minimal: String?, netMs: Int, decMs: Int, err: String?) in
            // 1) Structured çoklu
            let listURLBase = baseURL
                .appendingPathComponent("api")
                .appendingPathComponent("v1")
                .appendingPathComponent("nlp")
                .appendingPathComponent("parse-announcements")
            var listComps = URLComponents(url: listURLBase, resolvingAgainstBaseURL: false)!
            var listQI: [URLQueryItem] = []
            if let ann = announcementId, !ann.isEmpty {
                listQI.append(URLQueryItem(name: "announcement_id", value: ann))
            } else {
                if let pub = resolvedPub { listQI.append(URLQueryItem(name: "publication_date", value: pub)) }
                if let iss = resolvedIssue { listQI.append(URLQueryItem(name: "issue_number", value: String(iss))) }
                if let pag = resolvedPage { listQI.append(URLQueryItem(name: "page_number", value: String(pag))) }
                if let purl = resolvedPdf, !purl.isEmpty { listQI.append(URLQueryItem(name: "pdf_url", value: purl)) }
                if let fn = fileNameParam, !fn.isEmpty { listQI.append(URLQueryItem(name: "pdf_file_name", value: fn)) }
            }
            if let fn = fileNameParam, !fn.isEmpty, listQI.isEmpty { listQI.append(URLQueryItem(name: "pdf_file_name", value: fn)) }
            if !listQI.isEmpty { listComps.queryItems = listQI }
            let listURL = listComps.url ?? listURLBase
            var listReq = URLRequest(url: listURL)
            listReq.httpMethod = "POST"
            listReq.addValue("application/json", forHTTPHeaderField: "Content-Type")
            listReq.addValue("application/json", forHTTPHeaderField: "Accept")
            listReq.addValue("Bearer \(bearerToken)", forHTTPHeaderField: "Authorization")
            listReq.timeoutInterval = 120
            do { listReq.httpBody = try encoder.encode(requestBody) } catch {
                return (nil, nil, nil, 0, 0, "encode error: \(error.localizedDescription)")
            }
            do {
                let t0 = CFAbsoluteTimeGetCurrent()
                let (data, response) = try await session.data(for: listReq)
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
                let minimalURLBase = baseURL
                    .appendingPathComponent("api")
                    .appendingPathComponent("v1")
                    .appendingPathComponent("nlp")
                    .appendingPathComponent("parse-announcements-minimal")
                var minimalComps = URLComponents(url: minimalURLBase, resolvingAgainstBaseURL: false)!
                var minQI: [URLQueryItem] = []
                if let ann = announcementId, !ann.isEmpty {
                    minQI.append(URLQueryItem(name: "announcement_id", value: ann))
                } else {
                    if let pub = resolvedPub { minQI.append(URLQueryItem(name: "publication_date", value: pub)) }
                    if let iss = resolvedIssue { minQI.append(URLQueryItem(name: "issue_number", value: String(iss))) }
                    if let pag = resolvedPage { minQI.append(URLQueryItem(name: "page_number", value: String(pag))) }
                    if let purl = resolvedPdf, !purl.isEmpty { minQI.append(URLQueryItem(name: "pdf_url", value: purl)) }
                    if let fn = fileNameParam, !fn.isEmpty { minQI.append(URLQueryItem(name: "pdf_file_name", value: fn)) }
                }
                if let fn = fileNameParam, !fn.isEmpty, minQI.isEmpty { minQI.append(URLQueryItem(name: "pdf_file_name", value: fn)) }
                if !minQI.isEmpty { minimalComps.queryItems = minQI }
                let minimalURL = minimalComps.url ?? minimalURLBase
                var minimalReq = URLRequest(url: minimalURL)
                minimalReq.httpMethod = "POST"
                minimalReq.addValue("application/json", forHTTPHeaderField: "Content-Type")
                minimalReq.addValue("application/json", forHTTPHeaderField: "Accept")
                minimalReq.addValue("Bearer \(bearerToken)", forHTTPHeaderField: "Authorization")
                minimalReq.timeoutInterval = 120
                do { minimalReq.httpBody = try encoder.encode(requestBody) } catch {
                    return (structured, decoded, nil, tNet, tDec, "minimal encode error: \(error.localizedDescription)")
                }
                do {
                    let (mdata, mresp) = try await session.data(for: minimalReq)
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
                "original_text": self.ocrResult,
                "items": itemsArray
            ]
            if let path = self.currentStoragePath, !path.isEmpty {
                payloadObj["source_file"] = [
                    "bucket": self.pdfBucket,
                    "path": path
                ]
                // Öncelik: resolve endpoint’i ile elde edilen id+meta
                if let ann = self.resolvedAnnouncementId, !ann.isEmpty {
                    payloadObj["announcement_id"] = ann
                    print("[PDF] ingest payload announcement_id=\(ann)")
                }
            }
            // Meta verileri ekle (varsa)
            if let pub = self.resolvedPublicationDate { payloadObj["publication_date"] = pub }
            if let iss = self.resolvedIssueNumber { payloadObj["issue_number"] = iss }
            if let page = self.resolvedPageNumber { payloadObj["page_number"] = page }
            if let purl = self.resolvedPdfUrl { payloadObj["pdf_url"] = purl }
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
