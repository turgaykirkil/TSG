import SwiftUI
import Combine
import Supabase
import Vision

@MainActor
class MainViewModel: ObservableObject {
    @Published var selectedPDF: Data?
    @Published var ocrResult: String = "Henüz OCR işlemi yapılmadı."
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

        do {
            self.ocrService = try OCRService()
        } catch {
            fatalError("OCRService başlatılamadı: \(error.localizedDescription)")
        }
        } catch {
            fatalError("Yapılandırma hatası: \(error.localizedDescription). Lütfen Config.plist dosyasını ve içeriğini kontrol edin.")
        }
    }

    func fetchRandomPDF() {
        isLoading = true
        errorMessage = nil
        selectedPDF = nil
        ocrResult = ""

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
                let text = try await ocrService.performOCR(on: pdfData)
                // OCR metnini parser ile işle
                let parsedAnnouncements = parser.parse(fullText: text)
        
        // --- HATA AYIKLAMA BAŞLANGICI ---
        print("\n--- PARSER AYIKLAMA SONUÇLARI ---")
        print("Toplam \(parsedAnnouncements.count) adet ilan bloğu bulundu.")
        for (index, announcement) in parsedAnnouncements.enumerated() {
            print("\n------------------------------------")
            print("--- BLOK \(index + 1) ---")
            print(announcement.rawText)
            print("------------------------------------\n")
        }
        print("--- PARSER AYIKLAMA SONUÇLARI BİTTİ ---\n")
        // --- HATA AYIKLAMA SONU ---
        
                self.announcements = parsedAnnouncements
                self.ocrResult = "\(parsedAnnouncements.count) adet ilan bulundu ve başarıyla işlendi."
            } catch {
                self.errorMessage = "OCR işlemi sırasında bir hata oluştu: \(error.localizedDescription)"
                self.ocrResult = "İşlem başarısız oldu."
            }
            self.isLoading = false
        }
    }
}
