import SwiftUI

@main
struct OcrApp: App {
    // Uygulamanın yaşam döngüsünü yönetmek için AppDelegate'i bağla.
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate
    // AuthViewModel, uygulamanın genelinde kimlik doğrulama durumunu yönetecek.
    @StateObject private var authViewModel = AuthViewModel()

    var body: some Scene {
        WindowGroup("Sicilius OCR App") {
            // Eğer kullanıcı giriş yapmışsa Ana Ekran'ı, yapmamışsa Giriş Ekranı'nı göster.
            if authViewModel.isAuthenticated {
                MainView()
                    .environmentObject(authViewModel) // AuthViewModel'i alt görünümlere aktar.
            } else {
                LoginView()
                    .environmentObject(authViewModel)
            }
        }
        // .windowStyle(HiddenTitleBarWindowStyle()) // HATA AYIKLAMA: Bu stil klavye girdisini engelliyor, geçici olarak devre dışı bırakıldı.
    }
}
