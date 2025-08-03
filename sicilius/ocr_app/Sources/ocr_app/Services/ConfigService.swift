import Foundation

enum ConfigError: Error {
    case fileNotFound(String)
    case invalidFormat(String)
    case keyNotFound(String)
}

struct ConfigService {
    static func get(key: String) throws -> String {
                                                guard let path = Bundle.module.path(forResource: "Config", ofType: "plist") else {
            throw ConfigError.fileNotFound("Config.plist bulunamadı. Proje kaynaklarına eklendiğinden emin olun.")
        }

        guard let xml = FileManager.default.contents(atPath: path) else {
            throw ConfigError.fileNotFound("Config.plist okunamadı.")
        }

        guard let config = try? PropertyListSerialization.propertyList(from: xml, options: .mutableContainers, format: nil) as? [String: String] else {
            throw ConfigError.invalidFormat("Config.plist formatı geçersiz.")
        }

        guard let value = config[key] else {
            throw ConfigError.keyNotFound("\(key) anahtarı Config.plist içinde bulunamadı.")
        }
        
        return value
    }
}
