import Foundation
import Combine

// Token'ı güvenli bir şekilde saklamak için.
private let keychainService = "com.sicilius.ocr-app"
private let keychainAccount = "user_access_token"

// Backend'den gelen token yanıtını modellemek için.
struct TokenResponse: Codable {
    let accessToken: String
    let tokenType: String

    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case tokenType = "token_type"
    }
}

@MainActor
class AuthViewModel: ObservableObject {
    @Published var isAuthenticated: Bool = false
    @Published var errorMessage: String? = nil
    @Published var isLoading: Bool = false

    private var cancellables = Set<AnyCancellable>()

    init() {
        // Uygulama başlarken Keychain'de token var mı diye kontrol et.
        checkSession()
    }

    func checkSession() {
        if KeychainService.load(service: keychainService, account: keychainAccount) != nil {
            self.isAuthenticated = true
        } else {
            self.isAuthenticated = false
        }
    }

    func signIn(email: String, password: String) {
        isLoading = true
        errorMessage = nil

        // 1. URL'yi oluştur
        guard let url = URL(string: "http://127.0.0.1:5002/api/v1/auth/login/access-token") else {
            errorMessage = "Geçersiz API URL'si"
            isLoading = false
            return
        }

        // 2. İstek (Request) oluştur
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        // 3. Header'ı backend'in beklediği gibi ayarla
        request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")

        // 4. Gövdeyi (Body) backend'in beklediği formatta ve alan adlarıyla oluştur
        var components = URLComponents()
        components.queryItems = [
            URLQueryItem(name: "username", value: email), // Backend 'username' bekliyor
            URLQueryItem(name: "password", value: password)
        ]
        request.httpBody = components.query?.data(using: .utf8)
        
        // 5. Ağ isteğini gönder
        URLSession.shared.dataTask(with: request) { data, response, error in
            DispatchQueue.main.async {
                self.isLoading = false

                // Hata kontrolü
                if let error = error {
                    self.errorMessage = "Ağ hatası: \(error.localizedDescription)"
                    self.isAuthenticated = false
                    return
                }

                // HTTP Status kontrolü
                guard let httpResponse = response as? HTTPURLResponse else {
                    self.errorMessage = "Geçersiz sunucu yanıtı"
                    self.isAuthenticated = false
                    return
                }
                
                guard let data = data else {
                    self.errorMessage = "Sunucudan veri alınamadı."
                    self.isAuthenticated = false
                    return
                }

                // Başarılı (2xx) ve Başarısız (4xx, 5xx) durumları yönet
                if (200...299).contains(httpResponse.statusCode) {
                    do {
                        let tokenResponse = try JSONDecoder().decode(TokenResponse.self, from: data)
                        // Token'ı Keychain'e kaydet
                        // Token'ı Keychain'e kaydet (dönüş değerini bilinçli olarak yoksay)
                        _ = KeychainService.save(token: tokenResponse.accessToken.data(using: .utf8)!, service: keychainService, account: keychainAccount)
                        self.isAuthenticated = true
                    } catch {
                        self.errorMessage = "Token verisi işlenemedi: \(error.localizedDescription)"
                        self.isAuthenticated = false
                    }
                } else {
                    // Backend'den gelen hata mesajını göstermeye çalış
                    if let errorDetail = try? JSONDecoder().decode([String: String].self, from: data) {
                        self.errorMessage = errorDetail["detail"] ?? "Bilinmeyen bir hata oluştu."
                    } else {
                         self.errorMessage = "Giriş bilgileri yanlış veya sunucu hatası. (Status: \(httpResponse.statusCode))"
                    }
                    self.isAuthenticated = false
                }
            }
        }.resume()
    }

    func signOut() {
        // Keychain'den token'ı sil
        if KeychainService.delete(service: keychainService, account: keychainAccount) {
            self.isAuthenticated = false
        } else {
            // Genellikle bu hata oluşmaz, ama olursa diye...
            self.errorMessage = "Çıkış yapılırken bir sorun oluştu."
        }
    }
}
