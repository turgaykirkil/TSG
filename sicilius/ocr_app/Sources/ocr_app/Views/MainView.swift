import SwiftUI

struct MainView: View {
    @EnvironmentObject var authViewModel: AuthViewModel
    @StateObject private var viewModel = MainViewModel()
    
    @State private var selectedSidebarItem: SidebarItem? = .ocr
    
    // Sağ panel görünüm modu
    @State private var resultTab: ResultTab = .raw

    enum ResultTab: String, CaseIterable, Identifiable {
        case raw = "Ham Metin"
        case nlp = "NLP Çıktısı"
        var id: String { rawValue }
    }

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
                if viewModel.isLoading {
                    Text("İşlem sürüyor...")
                        .foregroundColor(.secondary)
                        .padding(8)
                        .frame(maxWidth: .infinity, minHeight: 30)
                        .background(Color.primary.opacity(0.05))
                        .cornerRadius(8)
                } else if let errorMessage = viewModel.errorMessage {
                    Text(errorMessage)
                        .foregroundColor(.red)
                        .padding(8)
                        .frame(maxWidth: .infinity)
                        .background(Color.red.opacity(0.15))
                        .cornerRadius(8)
                } else if viewModel.selectedPDF != nil {
                    Text("PDF indirildi. Tara butonuna basın.")
                        .foregroundColor(.secondary)
                        .padding(8)
                        .frame(maxWidth: .infinity, minHeight: 30)
                        .background(Color.primary.opacity(0.05))
                        .cornerRadius(8)
                } else {
                    Text("Henüz OCR işlemi yapılmadı.")
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
                // Sol Taraf: PDF Önizleme
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

                // Sağ Taraf: Ham Metin / NLP Çıktısı
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Picker("Görünüm", selection: $resultTab) {
                            ForEach(ResultTab.allCases) { tab in
                                Text(tab.rawValue).tag(tab)
                            }
                        }
                        .pickerStyle(.segmented)
                        
                        Spacer()
                    }
                    
                    switch resultTab {
                    case .raw:
                        VStack(alignment: .leading, spacing: 6) {
                            Text("Ham Metin Çıktısı")
                                .font(.headline)
                            TextEditor(text: $viewModel.ocrResult)
                                .font(.system(.body, design: .monospaced))
                                .padding(4)
                                .border(Color.gray.opacity(0.2), width: 1)
                                .textSelection(.enabled)
                        }
                    case .nlp:
                        ScrollView {
                            VStack(alignment: .leading, spacing: 12) {
                                Text("NLP Çıktısı")
                                    .font(.headline)
                                if let pe = viewModel.parsedEntities {
                                    if let reg = pe.registration_number, !reg.isEmpty {
                                        HStack(spacing: 6) {
                                            Image(systemName: "number")
                                            Text("Ticaret Sicil No:")
                                                .fontWeight(.semibold)
                                            Text(reg)
                                        }
                                    }
                                    DisclosureGroup(content: {
                                        EntitySectionView(title: "Kuruluşlar", systemImage: "building.2", items: pe.organizations, showHeader: false)
                                    }, label: {
                                        HStack {
                                            Image(systemName: "building.2")
                                            Text("Kuruluşlar")
                                            Spacer()
                                            Text("\(pe.organizations.count)")
                                                .font(.subheadline)
                                                .foregroundColor(.secondary)
                                        }
                                    })
                                    DisclosureGroup(content: {
                                        EntitySectionView(title: "Kişiler", systemImage: "person.2", items: pe.persons, showHeader: false)
                                    }, label: {
                                        HStack {
                                            Image(systemName: "person.2")
                                            Text("Kişiler")
                                            Spacer()
                                            Text("\(pe.persons.count)")
                                                .font(.subheadline)
                                                .foregroundColor(.secondary)
                                        }
                                    })
                                    DisclosureGroup(content: {
                                        EntitySectionView(title: "Konumlar", systemImage: "mappin.and.ellipse", items: pe.locations, showHeader: false)
                                    }, label: {
                                        HStack {
                                            Image(systemName: "mappin.and.ellipse")
                                            Text("Konumlar")
                                            Spacer()
                                            Text("\(pe.locations.count)")
                                                .font(.subheadline)
                                                .foregroundColor(.secondary)
                                        }
                                    })
                                    DisclosureGroup(content: {
                                        EntitySectionView(title: "Tarihler", systemImage: "calendar", items: pe.dates, showHeader: false)
                                    }, label: {
                                        HStack {
                                            Image(systemName: "calendar")
                                            Text("Tarihler")
                                            Spacer()
                                            Text("\(pe.dates.count)")
                                                .font(.subheadline)
                                                .foregroundColor(.secondary)
                                        }
                                    })
                                    DisclosureGroup(content: {
                                        EntitySectionView(title: "Para", systemImage: "turkishlirasign", items: pe.money, showHeader: false)
                                    }, label: {
                                        HStack {
                                            Image(systemName: "turkishlirasign")
                                            Text("Para")
                                            Spacer()
                                            Text("\(pe.money.count)")
                                                .font(.subheadline)
                                                .foregroundColor(.secondary)
                                        }
                                    })
                                    DisclosureGroup(content: {
                                        EntitySectionView(title: "Diğer", systemImage: "tag", items: pe.misc, showHeader: false)
                                    }, label: {
                                        HStack {
                                            Image(systemName: "tag")
                                            Text("Diğer")
                                            Spacer()
                                            Text("\(pe.misc.count)")
                                                .font(.subheadline)
                                                .foregroundColor(.secondary)
                                        }
                                    })
                                } else {
                                    Text("Henüz NLP çıktısı yok. Önce OCR yapın.")
                                        .foregroundColor(.secondary)
                                }
                            }
                            .frame(maxWidth: .infinity, alignment: .topLeading)
                        }
                        .padding()
                }
            }
            .padding()
            .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
        }
    }
}
}

// Yardımcı görünüm: varlık listesi
private struct EntitySectionView: View {
    let title: String
    let systemImage: String
    let items: [NlpEntity]
    var showHeader: Bool = true

    var body: some View {
        if !items.isEmpty {
            VStack(alignment: .leading, spacing: 6) {
                if showHeader {
                    HStack(spacing: 6) {
                        Image(systemName: systemImage)
                        Text(title)
                            .font(.subheadline)
                            .fontWeight(.semibold)
                    }
                }

                ForEach(Array(items.enumerated()), id: \.offset) { pair in
                    let item = pair.element
                    HStack(alignment: .top, spacing: 6) {
                        Text("•").fontWeight(.bold)
                        VStack(alignment: .leading, spacing: 2) {
                            Text(item.text)
                                .lineLimit(2)
                                .truncationMode(.tail)
                            Text(item.label)
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                    }
                }
            }
        }
    }
}
