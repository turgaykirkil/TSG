import SwiftUI
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
}

@MainActor
class MainViewModel: ObservableObject {
    @Published var selectedPDF: Data?
    @Published var ocrResult: String = "Henüz OCR işlemi yapılmadı."
    @Published var parsedEntities: NlpParseResponse?
    @Published var announcements: [Announcement] = []
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
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
                let rawText = try await ocrService.performOCR(on: pdfData)
                
                // Update UI with raw text first
                self.ocrResult = rawText
                
                // After getting raw text, call the NLP service
                await self.parseTextWithNLP(text: rawText)
                
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
        guard let url = URL(string: "http://localhost:5001/api/v1/nlp/parse-announcement") else {
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
            
            let decodedResponse = try JSONDecoder().decode(NlpParseResponse.self, from: data)
            self.parsedEntities = decodedResponse
            print("Successfully parsed entities: \(decodedResponse.organizations.count) organizations found.")

        } catch {
            self.errorMessage = "NLP service request failed: \(error.localizedDescription)"
            print("NLP service error: \(error)")
        }
    }
}
