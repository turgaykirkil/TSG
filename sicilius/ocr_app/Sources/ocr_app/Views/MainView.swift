import SwiftUI

struct MainView: View {
    @EnvironmentObject var authViewModel: AuthViewModel
    @StateObject private var viewModel = MainViewModel()
    
    @State private var selectedSidebarItem: SidebarItem? = .ocr

    enum SidebarItem {
        case ocr
        case settings
    }

    var body: some View {
        HSplitView {
            // Yan Menü
            VStack(alignment: .leading) {
                Text("Sicilius OCR")
                    .font(.title)
                    .bold()
                    .padding([.horizontal, .top])
                List(selection: $selectedSidebarItem) {
                    Label("OCR İşlemi", systemImage: "doc.text.viewfinder")
                        .tag(SidebarItem.ocr as SidebarItem?)
                    Label("Ayarlar", systemImage: "gear")
                        .tag(SidebarItem.settings as SidebarItem?)
                }
                .listStyle(.sidebar)
            }
            .frame(minWidth: 180, idealWidth: 220, maxWidth: 280)

            // Ana İçerik
            switch selectedSidebarItem {
            case .ocr:
                ocrContentView
            case .settings:
                Text("Ayarlar sayfası burada olacak.")
                    .font(.largeTitle)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            case .none:
                Text("Lütfen bir seçim yapın.")
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
        }
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button(action: authViewModel.signOut) {
                    Label("Çıkış Yap", systemImage: "person.crop.circle.badge.xmark")
                }
                .help("Oturumu Kapat")
            }
        }
    }
    
    private var ocrContentView: some View {
        VStack(spacing: 0) {
            // Üst Kontrol Paneli
            VStack(alignment: .leading, spacing: 8) {
                Text("OCR Kontrol Paneli")
                    .font(.title2)
                    .fontWeight(.bold)

                HStack(spacing: 12) {
                    Button(action: viewModel.fetchRandomPDF) {
                        Label("PDF Getir", systemImage: "arrow.down.doc.fill")
                    }
                    .buttonStyle(.borderedProminent)
                    .disabled(viewModel.isLoading)
                    .controlSize(.large)

                    Button(action: viewModel.performOCR) {
                        Label("Tara", systemImage: "play.circle.fill")
                    }
                    .buttonStyle(.borderedProminent)
                    .tint(.green)
                    .disabled(viewModel.selectedPDF == nil || viewModel.isLoading)
                    .controlSize(.large)
                    
                    Spacer()
                    
                    if viewModel.isLoading {
                        ProgressView()
                            .scaleEffect(1.5)
                            .padding(.horizontal)
                    }
                }

                // Durum Mesajları
                if let errorMessage = viewModel.errorMessage {
                    Text(errorMessage)
                        .foregroundColor(.red)
                        .padding(8)
                        .frame(maxWidth: .infinity)
                        .background(Color.red.opacity(0.15))
                        .cornerRadius(8)
                } else {
                    Text(viewModel.ocrResult)
                        .foregroundColor(.secondary)
                        .padding(8)
                        .frame(maxWidth: .infinity, minHeight: 30)
                        .background(Color.primary.opacity(0.05))
                        .cornerRadius(8)
                }
            }
            .padding()
            .background(Material.ultraThin)

            Divider()

            // Sonuçlar ve PDF Önizleme Alanı
            HSplitView {
                // Sol Taraf: Ayrıştırılmış İlan Listesi
                if !viewModel.announcements.isEmpty {
                    List(viewModel.announcements) { announcement in
                        VStack(alignment: .leading, spacing: 8) {
                            Text(announcement.title)
                                .font(.headline)
                                .fontWeight(.bold)
                            
                            HStack {
                                Text("Sicil No:")
                                    .fontWeight(.semibold)
                                Text(announcement.registrationNumber)
                            }
                            
                            HStack {
                                Text("MERSIS No:")
                                    .fontWeight(.semibold)
                                Text(announcement.mersisNumber)
                            }
                        }
                        .padding(.vertical, 8)
                    }
                } else {
                     ZStack {
                        Color(NSColor.controlBackgroundColor)
                        Text("Ayrıştırılmış veri burada görünecek.")
                            .font(.title2)
                            .foregroundColor(.secondary)
                    }
                }

                // Sağ Taraf: PDF Önizleme
                VStack {
                    if let pdfData = viewModel.selectedPDF {
                        PDFKitView(data: pdfData)
                    } else {
                        ZStack {
                            Color(NSColor.controlBackgroundColor)
                            Text("Başlamak için bir PDF getirin.")
                                .font(.title)
                                .foregroundColor(.secondary)
                        }
                    }
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
        }
    }
}
