import SwiftUI
import Foundation

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

    

    enum SidebarItem: Hashable {
        case ocr
        case settings
    }

    var body: some View {
        HSplitView {
            // Yan Menü
            VStack(alignment: .leading) {
                Text("Sicilius OCR App")
                    .font(.title)
                    .bold()
                    .padding([.horizontal, .top])
                List {
                    Label("OCR İşlemi", systemImage: "doc.text.viewfinder")
                        .contentShape(Rectangle())
                        .onTapGesture { selectedSidebarItem = .ocr }
                    Label("Ayarlar", systemImage: "gear")
                        .contentShape(Rectangle())
                        .onTapGesture { selectedSidebarItem = .settings }
                }
                .listStyle(.sidebar)
            }
            .frame(minWidth: 180, idealWidth: 220, maxWidth: 280)

            // Ana İçerik
            switch selectedSidebarItem {
            case .ocr:
                ocrContentView
            case .settings:
                settingsView
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
    
    private var settingsView: some View {
        Form {
            Section(header: Text("İşlem Modu")) {
                Picker("Mod", selection: $viewModel.processingMode) {
                    Text(MainViewModel.ProcessingMode.manual.rawValue).tag(MainViewModel.ProcessingMode.manual)
                    Text(MainViewModel.ProcessingMode.automatic.rawValue).tag(MainViewModel.ProcessingMode.automatic)
                }
                .pickerStyle(.segmented)
                .frame(maxWidth: 360)
                
                if viewModel.processingMode == .manual {
                    HStack(spacing: 12) {
                        Text("Adet")
                        Stepper(value: $viewModel.manualCount, in: 1...100) {
                            Text("\(viewModel.manualCount)")
                        }
                        .frame(maxWidth: 200)
                    }
                    Text("Manuel modda 'PDF Getir' butonuna basınca belirtilen adet kadar PDF sırasıyla indirilir, OCR ve NLP yapılır, sonuçlar backend'e ingest edilir (JSON yerel diske yazılmaz).")
                        .font(.footnote)
                        .foregroundColor(.secondary)
                        .fixedSize(horizontal: false, vertical: true)
                } else {
                    Text("Otomatik modda 'PDF Getir' butonu 'Durdur' olarak değişir. Durdurulana kadar yeni PDF'ler indirilir, OCR ve NLP çalışır ve sonuçlar backend'e ingest edilir.")
                        .font(.footnote)
                        .foregroundColor(.secondary)
                        .fixedSize(horizontal: false, vertical: true)
                }
            }
            Section(header: Text("İngest / Silme")) {
                Toggle(isOn: $viewModel.deleteAfterIngest) {
                    Text("İngest sonrası PDF'yi Supabase Storage'dan sil")
                }
                .toggleStyle(.switch)
                Text("Bu seçenek açıkken ingest başarılı olduğunda, indirilen PDF dosyası storage'dan silinir ve ilgili DB kayıtları işaretlenir.")
                    .font(.footnote)
                    .foregroundColor(.secondary)
            }
            
            Section(header: Text("İpuçları")) {
                Text("OCR geçici çıktıları 'ocr_ciktilari' klasörüne kaydedilir. Sağ paneldeki 'JSON'u Kaydet' butonu backend'e ingest çağrısı gönderir (JSON yerelde saklanmaz).")
                    .font(.footnote)
                    .foregroundColor(.secondary)
            }
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
    }
    
    private var ocrContentView: some View {
        VStack(spacing: 0) {
            topControlPanel
            Divider()
            resultsSplitView
        }
    }
    
    // Üst Kontrol Paneli ayrı bir görünüme bölündü
    @ViewBuilder private var topControlPanel: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("OCR Kontrol Paneli")
                .font(.title2)
                .fontWeight(.bold)

            HStack(spacing: 12) {
                Button(action: viewModel.handleFetchButtonTapped) {
                    if viewModel.processingMode == .automatic {
                        if viewModel.isAutoRunning {
                            Label("Durdur", systemImage: "stop.circle.fill")
                        } else {
                            Label("PDF Getir", systemImage: "arrow.down.doc.fill")
                        }
                    } else {
                        Label("PDF Getir", systemImage: "arrow.down.doc.fill")
                    }
                }
                .buttonStyle(.borderedProminent)
                .disabled(viewModel.processingMode == .manual && viewModel.isLoading)
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
            } else if viewModel.isAutoRunning {
                Text("Otomatik mod aktif: Yeni PDF'ler indiriliyor, OCR ve NLP sonuçları kaydediliyor...")
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
                Text("PDF indirildi veya OCR tamamlandı.")
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
    }

    // Sol/sağ paneli içeren görünüm
    private var resultsSplitView: some View {
        HSplitView {
            pdfPreviewView()
            rightPanelView()
        }
        .padding()
        .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
    }

    // Sol panel: PDF önizleme
    private func pdfPreviewView() -> some View {
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

    // Sağ panel: üst kontroller + sonuç görünümü
    @ViewBuilder private func rightPanelView() -> some View {
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
                        Button(action: {
                            Task { await viewModel.reRunNLP() }
                        }) {
                            Label("NLP'yi Yeniden Çalıştır", systemImage: "arrow.clockwise")
                        }
                        .buttonStyle(.borderedProminent)
                        .controlSize(.small)
                        .disabled(viewModel.isLoading || viewModel.ocrResult.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                        Button(action: { viewModel.copyNlpJsonToClipboard() }) {
                            Label("Kopyala JSON", systemImage: "doc.on.doc")
                        }
                        .buttonStyle(.bordered)
                        .controlSize(.small)
                        .disabled(viewModel.nlpMinimalJson == nil && viewModel.nlpStructuredJson == nil)
                        Button(action: { viewModel.saveNlpJsonToDisk() }) {
                            Label("JSON'u Kaydet", systemImage: "square.and.arrow.down")
                        }
                        .buttonStyle(.bordered)
                        .controlSize(.small)
                        .disabled(viewModel.nlpStructuredJson == nil)
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
                nlpResultsView()
            }
        }
    }

    // NLP sonuçlarının detaylı görünümü
    @ViewBuilder private func nlpResultsView() -> some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 12) {
                Text("NLP Çıktısı")
                    .font(.headline)
                if let list = viewModel.parsedAnnouncements, !list.isEmpty {
                    ForEach(Array(list.enumerated()), id: \.offset) { (_, ann) in
                        AnnouncementCardView(ann: ann)
                    }
                } else if let pe = viewModel.parsedEntities {
                    VStack(alignment: .leading, spacing: 6) {
                        if let ilanlar = pe.ilan_sira_no, !ilanlar.isEmpty {
                            HStack(spacing: 6) {
                                Image(systemName: "list.number")
                                Text("İlan Sıra No:")
                                    .fontWeight(.semibold)
                                Text(ilanlar.joined(separator: ", "))
                            }
                        }
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
                                Text("Ticaret Sicil/Dosya No:")
                                    .fontWeight(.semibold)
                                Text(sicil)
                            }
                        }
                        if let unvan = pe.trade_name, !unvan.isEmpty {
                            HStack(alignment: .top, spacing: 6) {
                                Image(systemName: "doc.text")
                                Text("Ticaret Ünvanı:")
                                    .fontWeight(.semibold)
                                Text(unvan)
                            }
                        }
                        if let eski = pe.old_trade_name, !eski.isEmpty {
                            HStack(alignment: .top, spacing: 6) {
                                Image(systemName: "doc.text.fill")
                                Text("Eski Ticaret Ünvanı:")
                                    .fontWeight(.semibold)
                                Text(eski)
                            }
                        }
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
                                    Text("Adres")
                                    Spacer()
                                    Text("\(addrs.count)")
                                        .font(.subheadline)
                                        .foregroundColor(.secondary)
                                }
                            })
                        }
                        if let oldAddrs = pe.old_addresses, !oldAddrs.isEmpty {
                            DisclosureGroup(content: {
                                VStack(alignment: .leading, spacing: 6) {
                                    ForEach(oldAddrs.indices, id: \.self) { idx in
                                        Text("• " + oldAddrs[idx])
                                            .textSelection(.enabled)
                                    }
                                }
                            }, label: {
                                HStack {
                                    Image(systemName: "clock.arrow.circlepath")
                                    Text("Eski Adres")
                                    Spacer()
                                    Text("\(oldAddrs.count)")
                                        .font(.subheadline)
                                        .foregroundColor(.secondary)
                                }
                            })
                        }
                        let peHusList = (!(pe.hususlar ?? []).isEmpty ? (pe.hususlar ?? []) : (pe.entities_full?.hususlar ?? []))
                        if !peHusList.isEmpty {
                            DisclosureGroup(content: {
                                VStack(alignment: .leading, spacing: 6) {
                                    ForEach(peHusList.indices, id: \.self) { idx in
                                        Text("• " + peHusList[idx])
                                            .textSelection(.enabled)
                                    }
                                }
                            }, label: {
                                HStack {
                                    Image(systemName: "checklist")
                                    Text("Tescil Edilen Hususlar")
                                    Spacer()
                                    Text("\(peHusList.count)")
                                        .font(.subheadline)
                                        .foregroundColor(.secondary)
                                }
                            })
                        }
                        let peBelPrimary = pe.belgeler?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
                        let peBelFallback = pe.entities_full?.belgeler?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
                        let peBelMerge = !peBelPrimary.isEmpty ? peBelPrimary : peBelFallback
                        if !peBelMerge.isEmpty {
                            DisclosureGroup("Tescile Delil Olan Belgeler") {
                                Text(peBelMerge)
                                    .font(.system(.footnote, design: .monospaced))
                                    .textSelection(.enabled)
                            }
                        }
                    }
                    let pePersons = pe.persons ?? []
                    if !pePersons.isEmpty {
                        DisclosureGroup(content: {
                            EntitySectionView(title: "Kişiler", systemImage: "person", items: pePersons, showHeader: false)
                        }, label: {
                            HStack {
                                Image(systemName: "person")
                                Text("Kişiler")
                                Spacer()
                                Text("\(pePersons.count)")
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }
                        })
                    }
                    DisclosureGroup(content: {
                        EntitySectionView(title: "Para", systemImage: "turkishlirasign", items: pe.money ?? [], showHeader: false)
                    }, label: {
                        HStack {
                            Image(systemName: "turkishlirasign")
                            Text("Para")
                            Spacer()
                            Text("\(pe.money?.count ?? 0)")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    })
                    DisclosureGroup(content: {
                        EntitySectionView(title: "Diğer", systemImage: "tag", items: pe.misc ?? [], showHeader: false)
                    }, label: {
                        HStack {
                            Image(systemName: "tag")
                            Text("Diğer")
                            Spacer()
                            Text("\(pe.misc?.count ?? 0)")
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
        .textSelection(.enabled)
        .padding()
    }
}

// Alt görünüm: Çoklu ilân kartı
private struct AnnouncementCardView: View {
    let ann: NlpParsedAnnouncement

    var body: some View {
        GroupBox {
            VStack(alignment: .leading, spacing: 8) {
                if let header = ann.sicil_office_header, !header.isEmpty {
                    HStack(spacing: 6) {
                        Image(systemName: "building.columns")
                        Text(header)
                            .font(.subheadline)
                            .fontWeight(.semibold)
                    }
                }

                if let ilanlar = ann.ilan_sira_no, !ilanlar.isEmpty {
                    HStack(spacing: 6) {
                        Image(systemName: "list.number")
                        Text("İlan Sıra No:")
                            .fontWeight(.semibold)
                        Text(ilanlar.joined(separator: ", "))
                    }
                }
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
                        Text("Ticaret Sicil/Dosya No:")
                            .fontWeight(.semibold)
                        Text(sicil)
                    }
                }
                if let unvan = ann.trade_name, !unvan.isEmpty {
                    HStack(alignment: .top, spacing: 6) {
                        Image(systemName: "doc.text")
                        Text("Ticaret Ünvanı:")
                            .fontWeight(.semibold)
                        Text(unvan)
                    }
                }
                if let eski = ann.old_trade_name, !eski.isEmpty {
                    HStack(alignment: .top, spacing: 6) {
                        Image(systemName: "doc.text.fill")
                        Text("Eski Ticaret Ünvanı:")
                            .fontWeight(.semibold)
                        Text(eski)
                    }
                }

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
                            Text("Adres")
                            Spacer()
                            Text("\(addrs.count)")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    })
                }
                if let oldAddrs = ann.old_addresses, !oldAddrs.isEmpty {
                    DisclosureGroup(content: {
                        VStack(alignment: .leading, spacing: 6) {
                            ForEach(oldAddrs.indices, id: \.self) { idx in
                                Text("• " + oldAddrs[idx])
                                    .textSelection(.enabled)
                            }
                        }
                    }, label: {
                        HStack {
                            Image(systemName: "clock.arrow.circlepath")
                            Text("Eski Adres")
                            Spacer()
                            Text("\(oldAddrs.count)")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    })
                }

                let husList = (!(ann.hususlar ?? []).isEmpty ? (ann.hususlar ?? []) : (ann.entities_full?.hususlar ?? []))
                if !husList.isEmpty {
                    DisclosureGroup(content: {
                        VStack(alignment: .leading, spacing: 6) {
                            ForEach(husList.indices, id: \.self) { idx in
                                Text("• " + husList[idx])
                                    .textSelection(.enabled)
                            }
                        }
                    }, label: {
                        HStack {
                            Image(systemName: "checklist")
                            Text("Tescil Edilen Hususlar")
                            Spacer()
                            Text("\(husList.count)")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    })
                }

                let belPrimary = ann.belgeler?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
                let belFallback = ann.entities_full?.belgeler?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
                let belMerge = !belPrimary.isEmpty ? belPrimary : belFallback
                if !belMerge.isEmpty {
                    DisclosureGroup("Tescile Delil Olan Belgeler") {
                        Text(belMerge)
                            .font(.system(.footnote, design: .monospaced))
                            .textSelection(.enabled)
                    }
                }

                if let s = ann.start_offset, let e = ann.end_offset {
                    let length = max(0, e - s)
                    HStack(spacing: 6) {
                        Image(systemName: "text.cursor")
                        Text("Konum:")
                            .fontWeight(.semibold)
                        Text("\(s) – \(e) (")
                        + Text("\(length)").font(.system(.footnote)).foregroundColor(.secondary)
                        + Text(" karakter)")
                    }
                }

                if let acts = ann.actions, !acts.isEmpty {
                    DisclosureGroup(content: {
                        VStack(alignment: .leading, spacing: 6) {
                            ForEach(Array(acts.enumerated()), id: \.offset) { pair in
                                let a = pair.element
                                VStack(alignment: .leading, spacing: 2) {
                                    HStack(spacing: 6) {
                                        Image(systemName: "bolt.fill")
                                        Text(a.type ?? "(tip yok)")
                                            .fontWeight(.semibold)
                                    }
                                    if let d = a.details, !d.isEmpty {
                                        Text(d)
                                    }
                                    if let dev = a.devralan, !dev.isEmpty {
                                        Text("Devralan: \(dev)")
                                            .font(.caption)
                                            .foregroundColor(.secondary)
                                    }
                                    if let eff = a.effective_date, !eff.isEmpty {
                                        Text("Yürürlük: \(eff)")
                                            .font(.caption)
                                            .foregroundColor(.secondary)
                                    }
                                    if let ps = a.parties, !ps.isEmpty {
                                        Text("Taraflar: \(ps.joined(separator: ", "))")
                                            .font(.caption)
                                            .foregroundColor(.secondary)
                                    }
                                    if let amts = a.amounts, !amts.isEmpty {
                                        Text("Tutarlar: \(amts.joined(separator: ", "))")
                                            .font(.caption)
                                            .foregroundColor(.secondary)
                                    }
                                }
                                .padding(.vertical, 2)
                            }
                        }
                    }, label: {
                        HStack {
                            Image(systemName: "bolt")
                            Text("Aksiyonlar")
                            Spacer()
                            Text("\(acts.count)")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    })
                }

                let persons = ann.persons ?? []
                if !persons.isEmpty {
                    DisclosureGroup(content: {
                        EntitySectionView(title: "Kişiler", systemImage: "person", items: persons, showHeader: false)
                    }, label: {
                        HStack {
                            Image(systemName: "person")
                            Text("Kişiler")
                            Spacer()
                            Text("\(persons.count)")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    })
                }

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
                if let name = ann.trade_name, !name.isEmpty {
                    Text("• ")
                    + Text(name).fontWeight(.semibold)
                }
            }
        }
    }
}

// ... (buradaki kod, önceki kodun aynısıdır)

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
                            // Kişilerde maskeli kimlik varsa göster
                            if item.label.uppercased().hasPrefix("PER"), let mid = item.masked_ids, !mid.isEmpty {
                                HStack(spacing: 6) {
                                    Image(systemName: "number")
                                    Text(mid)
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
