import SwiftUI

/// Bu görünüm, içinde bulunduğu pencereyi bulur ve klavye girdilerini alması için onu aktif hale getirir.
/// SwiftUI'daki pencere aktivasyon hatalarını çözmek için kullanılır.
struct WindowActivationView: NSViewRepresentable {
    func makeNSView(context: Context) -> NSView {
        let view = NSView()
        DispatchQueue.main.async {
            // Pencereyi bul ve aktif yap
            if let window = view.window {
                window.makeKeyAndOrderFront(nil)
            }
        }
        return view
    }

    func updateNSView(_ nsView: NSView, context: Context) {}
}
