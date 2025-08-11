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
                        HStack(spacing: 12) {
                            Picker("Görünüm", selection: $resultTab) {
                                ForEach(ResultTab.allCases) { tab in
                                    Text(tab.rawValue).tag(tab)
                                }
                            }
                            .pickerStyle(.segmented)
                            Spacer()
                            if resultTab == .nlp {
                                Button(action: { viewModel.copyNlpJsonToClipboard() }) {
                                    Label("Kopyala JSON", systemImage: "doc.on.doc")
                                }
                                .buttonStyle(.bordered)
                                .controlSize(.small)
                                .disabled(viewModel.nlpRawJson == nil)
                                Button(action: { viewModel.saveNlpJsonToDisk() }) {
                                    Label("JSON'u Kaydet", systemImage: "square.and.arrow.down")
                                }
                                .buttonStyle(.bordered)
                                .controlSize(.small)
                                .disabled(viewModel.nlpRawJson == nil)
                            }
                        }
                        .frame(height: 32)
                        
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
                                // Önce çoklu ilânları göster, yoksa tekil akışa düş
                                if let list = viewModel.parsedAnnouncements, !list.isEmpty {
                                    ForEach(list) { ann in
                                        GroupBox {
                                            VStack(alignment: .leading, spacing: 8) {
                                                // Başlık ve temel alanlar
                                                if let header = ann.sicil_office_header, !header.isEmpty {
                                                    HStack(spacing: 6) {
                                                        Image(systemName: "building.columns")
                                                        Text(header)
                                                            .font(.subheadline)
                                                            .fontWeight(.semibold)
                                                    }
                                                }
                                                HStack(spacing: 12) {
                                                    if let mersis = ann.mersis_no, !mersis.isEmpty {
                                                        HStack(spacing: 6) {
                                                            Image(systemName: "number")
                                                            Text("MERSIS No:")
                                                                .fontWeight(.semibold)
                                                            Text(mersis)
                                                        }
                                                    }
                                                    if let sicil = ann.sicil_dosya_no ?? ann.registration_number, !sicil.isEmpty {
                                                        HStack(spacing: 6) {
                                                            Image(systemName: "number")
                                                            Text("Ticaret Sicil No:")
                                                                .fontWeight(.semibold)
                                                            Text(sicil)
                                                        }
                                                    }
                                                }
                                                if let unvan = ann.trade_name, !unvan.isEmpty {
                                                    HStack(alignment: .top, spacing: 6) {
                                                        Image(systemName: "doc.text")
                                                        Text("Ticaret Unvanı:")
                                                            .fontWeight(.semibold)
                                                        Text(unvan)
                                                    }
                                                }

                                                // Adresler
                                                if let addrs = ann.addresses, !addrs.isEmpty {
                                                    DisclosureGroup(content: {
                                                        VStack(alignment: .leading, spacing: 6) {
                                                            ForEach(addrs.indices, id: \.self) { idx in
                                                                Text("• " + addrs[idx])
                                                                    .textSelection(.enabled)
                                                            }
                                                        }
                                                    }, label: {
                                                        HStack {
                                                            Image(systemName: "mail.and.text.magnifyingglass")
                                                            Text("Adresler")
                                                            Spacer()
                                                            Text("\(addrs.count)")
                                                                .font(.subheadline)
                                                                .foregroundColor(.secondary)
                                                        }
                                                    })
                                                }

                                                // Varlık grupları
                                                // (Kuruluşlar bölümü kaldırıldı)

                                                DisclosureGroup(content: {
                                                    EntitySectionView(title: "Kişiler", systemImage: "person.2", items: ann.persons, showHeader: false)
                                                }, label: {
                                                    HStack {
                                                        Image(systemName: "person.2")
                                                        Text("Kişiler")
                                                        Spacer()
                                                        Text("\(ann.persons.count)")
                                                            .font(.subheadline)
                                                            .foregroundColor(.secondary)
                                                    }
                                                })

                                                // (Konumlar bölümü kaldırıldı)

                                                // (Tarihler bölümü kaldırıldı)

                                                let monies = ann.money ?? []
                                                if !monies.isEmpty {
                                                    DisclosureGroup(content: {
                                                        EntitySectionView(title: "Para", systemImage: "turkishlirasign", items: monies, showHeader: false)
                                                    }, label: {
                                                        HStack {
                                                            Image(systemName: "turkishlirasign")
                                                            Text("Para")
                                                            Spacer()
                                                            Text("\(monies.count)")
                                                                .font(.subheadline)
                                                                .foregroundColor(.secondary)
                                                        }
                                                    })
                                                }

                                                let others = ann.misc ?? []
                                                if !others.isEmpty {
                                                    DisclosureGroup(content: {
                                                        EntitySectionView(title: "Diğer", systemImage: "tag", items: others, showHeader: false)
                                                    }, label: {
                                                        HStack {
                                                            Image(systemName: "tag")
                                                            Text("Diğer")
                                                            Spacer()
                                                            Text("\(others.count)")
                                                                .font(.subheadline)
                                                                .foregroundColor(.secondary)
                                                        }
                                                    })
                                                }

                                                // Ham segmenti göster
                                                if let seg = ann.original_text, !seg.isEmpty {
                                                    DisclosureGroup("Orijinal Segment") {
                                                        Text(seg)
                                                            .font(.system(.footnote, design: .monospaced))
                                                            .textSelection(.enabled)
                                                    }
                                                }
                                            }
                                        } label: {
                                            HStack {
                                                Image(systemName: "doc.text.magnifyingglass")
                                                Text("İlan #\(ann.index ?? 0)")
                                                if let name = ann.trade_name, !name.isEmpty { Text("• ") + Text(name).fontWeight(.semibold) }
                                                Spacer()
                                            }
                                        }
                                    }
                                } else if let pe = viewModel.parsedEntities {
                                    VStack(alignment: .leading, spacing: 6) {
                                        if let mersis = pe.mersis_no, !mersis.isEmpty {
                                            HStack(spacing: 6) {
                                                Image(systemName: "number")
                                                Text("MERSIS No:")
                                                    .fontWeight(.semibold)
                                                Text(mersis)
                                            }
                                        }
                                        if let sicil = pe.sicil_dosya_no ?? pe.registration_number, !sicil.isEmpty {
                                            HStack(spacing: 6) {
                                                Image(systemName: "number")
                                                Text("Ticaret Sicil No:")
                                                    .fontWeight(.semibold)
                                                Text(sicil)
                                            }
                                        }
                                        if let unvan = pe.trade_name, !unvan.isEmpty {
                                            HStack(alignment: .top, spacing: 6) {
                                                Image(systemName: "doc.text")
                                                Text("Ticaret Unvanı:")
                                                    .fontWeight(.semibold)
                                                Text(unvan)
                                            }
                                        }
                                    }
                                    // (Kuruluşlar bölümü kaldırıldı)
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
                                    // (Konumlar bölümü kaldırıldı)
                                    // (Tarihler bölümü kaldırıldı)
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
                                    if let addrs = pe.addresses, !addrs.isEmpty {
                                        DisclosureGroup(content: {
                                            VStack(alignment: .leading, spacing: 6) {
                                                ForEach(addrs.indices, id: \.self) { idx in
                                                    Text("• " + addrs[idx])
                                                        .textSelection(.enabled)
                                                }
                                            }
                                        }, label: {
                                            HStack {
                                                Image(systemName: "mail.and.text.magnifyingglass")
                                                Text("Adresler")
                                                Spacer()
                                                Text("\(addrs.count)")
                                                    .font(.subheadline)
                                                    .foregroundColor(.secondary)
                                            }
                                        })
                                    }
                                } else {
                                    Text("Henüz NLP çıktısı yok. Önce OCR yapın.")
                                        .foregroundColor(.secondary)
                                }
                            }
                            .frame(maxWidth: .infinity, alignment: .topLeading)
                        }
                        .textSelection(.enabled)
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
