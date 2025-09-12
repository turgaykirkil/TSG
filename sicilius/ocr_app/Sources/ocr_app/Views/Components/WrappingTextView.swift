import SwiftUI
import AppKit

// macOS: Yalnız dikey kaydırmalı, yatayda sarmalı metin görünümü
struct WrappingTextView: NSViewRepresentable {
    let text: String
    var isEditable: Bool = false
    // SwiftUI tarafındaki mevcut genişliği ilet, böylece satır sarması dinamik kalır
    var availableWidth: CGFloat? = nil

    func makeNSView(context: Context) -> NSScrollView {
        let scrollView = NSScrollView()
        scrollView.hasVerticalScroller = true
        scrollView.hasHorizontalScroller = false
        scrollView.autohidesScrollers = true
        scrollView.borderType = .noBorder
        scrollView.drawsBackground = false

        let textView = NSTextView()
        textView.isEditable = isEditable
        textView.isSelectable = true
        textView.isRichText = false
        textView.minSize = NSSize(width: 0, height: 0)
        textView.maxSize = NSSize(width: CGFloat.greatestFiniteMagnitude, height: CGFloat.greatestFiniteMagnitude)
        textView.isVerticallyResizable = true
        textView.isHorizontallyResizable = false
        textView.autoresizingMask = [.width]
        textView.textContainerInset = NSSize(width: 10, height: 6)
        textView.textContainer?.lineFragmentPadding = 0
        textView.textContainer?.widthTracksTextView = true
        let initialWidth = availableWidth ?? scrollView.contentSize.width
        textView.textContainer?.containerSize = NSSize(width: initialWidth, height: CGFloat.greatestFiniteMagnitude)
        textView.font = NSFont.monospacedSystemFont(ofSize: 13, weight: .regular)
        textView.textColor = NSColor.labelColor
        textView.backgroundColor = NSColor.windowBackgroundColor.withAlphaComponent(0.03)
        textView.string = text
        // Başlangıçta görünür olması için çerçeveyi içerik boyutuna ayarla
        textView.frame = NSRect(origin: .zero, size: NSSize(width: initialWidth, height: scrollView.contentSize.height))

        scrollView.documentView = textView
        return scrollView
    }

    func updateNSView(_ nsView: NSScrollView, context: Context) {
        guard let textView = nsView.documentView as? NSTextView else { return }
        if textView.string != text {
            textView.string = text
        }
        textView.isEditable = isEditable
        textView.isHorizontallyResizable = false
        textView.textContainer?.widthTracksTextView = true
        // Genişliği scrollView/GeometryReader'dan gelen değere sabitleyip sadece dikeyde büyüt
        let width = availableWidth ?? nsView.contentSize.width
        textView.textContainer?.containerSize = NSSize(width: width, height: CGFloat.greatestFiniteMagnitude)
        // Çerçeve genişliğini de eşitle (satır satıra kaymayı tetikler)
        var frame = textView.frame
        if frame.size.width != width {
            frame.size.width = width
            textView.frame = frame
        }
        textView.enclosingScrollView?.hasHorizontalScroller = false
    }
}
