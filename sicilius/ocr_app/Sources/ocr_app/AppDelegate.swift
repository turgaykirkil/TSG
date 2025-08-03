import SwiftUI

// Uygulamanın yaşam döngüsü olaylarını yönetmek için özel bir AppDelegate sınıfı.
class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ aNotification: Notification) {
        // Bu, uygulamanın bir menü çubuğu ve Dock simgesi olan standart bir ön plan uygulaması
        // olarak davranmasını sağlar. Bu, klavye girdisi sorununu çözmek için kritiktir.
        NSApp.setActivationPolicy(.regular)
        NSApp.activate(ignoringOtherApps: true)
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool {
        // Son pencere kapatıldığında uygulamanın sonlanmasını sağlar.
        return true
    }
}
