import SwiftUI
import AppKit

// JSON -> Ağaç veri modeli
enum JSONNodeType: String {
    case object = "Object"
    case array = "Array"
    case string = "String"
    case number = "Number"
    case bool = "Bool"
    case null = "Null"
}

struct JSONNode: Identifiable, Hashable {
    let id = UUID()
    let key: String?
    let type: JSONNodeType
    let value: String?
    var children: [JSONNode] = []

    static func == (lhs: JSONNode, rhs: JSONNode) -> Bool { lhs.id == rhs.id }
    func hash(into hasher: inout Hasher) { hasher.combine(id) }
}

// MARK: - Builder
extension JSONNode {
    static func build(key: String? = nil, from any: Any) -> JSONNode {
        if let dict = any as? [String: Any] {
            let kids = dict.keys.sorted().map { k -> JSONNode in
                return JSONNode.build(key: k, from: dict[k] as Any)
            }
            return JSONNode(key: key, type: .object, value: nil, children: kids)
        } else if let arr = any as? [Any] {
            let kids: [JSONNode] = arr.enumerated().map { (idx, val) in
                JSONNode.build(key: "[\(idx)]", from: val)
            }
            return JSONNode(key: key, type: .array, value: nil, children: kids)
        } else if let s = any as? String {
            return JSONNode(key: key, type: .string, value: s)
        } else if let n = any as? NSNumber {
            // NSNumber bool ayırımı
            if CFGetTypeID(n) == CFBooleanGetTypeID() {
                return JSONNode(key: key, type: .bool, value: (n.boolValue ? "true" : "false"))
            } else {
                return JSONNode(key: key, type: .number, value: n.stringValue)
            }
        } else if any is NSNull {
            return JSONNode(key: key, type: .null, value: "null")
        } else {
            // Tanınmayan tür: String'e dök
            return JSONNode(key: key, type: .string, value: String(describing: any))
        }
    }

    static func buildRoot(from jsonString: String) -> [JSONNode]? {
        guard let data = jsonString.data(using: .utf8) else { return nil }
        do {
            let obj = try JSONSerialization.jsonObject(with: data, options: [])
            if let arr = obj as? [Any] {
                return [JSONNode.build(key: nil, from: arr)]
            } else {
                return [JSONNode.build(key: nil, from: obj)]
            }
        } catch {
            return nil
        }
    }
}

// MARK: - Görünüm
struct JsonTreeView: View {
    let jsonString: String

    @State private var query: String = ""

    var body: some View {
        VStack(spacing: 8) {
            HStack(spacing: 8) {
                Image(systemName: "line.3.horizontal.decrease.circle")
                    .foregroundColor(.secondary)
                TextField("Ara (anahtar/değer)", text: $query)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
            }
            .padding(.horizontal, 4)

            if let roots = JSONNode.buildRoot(from: jsonString) {
                ScrollView {
                    LazyVStack(alignment: .leading, spacing: 4) {
                        ForEach(roots) { node in
                            JSONNodeRow(node: node, filter: query)
                                .padding(.vertical, 2)
                        }
                    }
                    .padding(6)
                }
                .background(Color.black.opacity(0.03))
                .border(Color.gray.opacity(0.2), width: 1)
            } else {
                Text("JSON parse edilemedi.")
                    .foregroundColor(.red)
            }
        }
    }
}

// Tek tek düğümleri DisclosureGroup ile göster
struct JSONNodeRow: View {
    let node: JSONNode
    let filter: String

    @State private var expanded: Bool = true

    var body: some View {
        switch node.type {
        case .object, .array:
            DisclosureGroup(isExpanded: $expanded) {
                VStack(alignment: .leading, spacing: 2) {
                    ForEach(filtered(children: node.children)) { child in
                        JSONNodeRow(node: child, filter: filter)
                            .padding(.leading, 14)
                    }
                }
            } label: {
                HStack(alignment: .firstTextBaseline, spacing: 6) {
                    keyTag
                    typeTag
                    if let countText = countBadgeText() {
                        Text(countText)
                            .font(.caption2)
                            .foregroundColor(.secondary)
                    }
                    Spacer()
                    copyButton(copyText: jsonFragment(from: node))
                }
            }
        case .string, .number, .bool, .null:
            HStack(alignment: .firstTextBaseline, spacing: 6) {
                keyTag
                valueText
                    .lineLimit(nil)
                    .fixedSize(horizontal: false, vertical: true)
                Spacer(minLength: 8)
                copyButton(copyText: jsonFragment(from: node))
            }
        }
    }

    // Filtreleme
    private func filtered(children: [JSONNode]) -> [JSONNode] {
        let q = filter.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !q.isEmpty else { return children }
        return children.filter { containsQuery(node: $0, q) }
    }
    private func containsQuery(node: JSONNode, _ q: String) -> Bool {
        if (node.key ?? "").localizedCaseInsensitiveContains(q) { return true }
        if (node.value ?? "").localizedCaseInsensitiveContains(q) { return true }
        return node.children.contains { containsQuery(node: $0, q) }
    }

    // Etiketler
    private var keyTag: some View {
        HStack(spacing: 4) {
            if let k = node.key {
                Text(k)
                    .font(.system(.body, design: .monospaced))
                    .foregroundColor(.primary)
                    .bold()
            } else {
                Text("(root)")
                    .font(.system(.body, design: .monospaced))
                    .foregroundColor(.secondary)
            }
        }
    }

    private var typeTag: some View {
        Text(typeLabel(node.type))
            .font(.caption2)
            .padding(.horizontal, 6)
            .padding(.vertical, 2)
            .background(typeColor(node.type).opacity(0.12))
            .foregroundColor(typeColor(node.type).opacity(0.9))
            .clipShape(Capsule())
    }

    private var valueText: some View {
        Group {
            switch node.type {
            case .string:
                Text("\"\(node.value ?? "")\"")
                    .foregroundColor(.green)
                    .font(.system(.body, design: .monospaced))
            case .number:
                Text(node.value ?? "")
                    .foregroundColor(.blue)
                    .font(.system(.body, design: .monospaced))
            case .bool:
                Text(node.value ?? "")
                    .foregroundColor(.purple)
                    .font(.system(.body, design: .monospaced))
            case .null:
                Text("null")
                    .foregroundColor(.gray)
                    .font(.system(.body, design: .monospaced))
            default:
                EmptyView()
            }
        }
    }

    // Araçlar
    private func typeColor(_ t: JSONNodeType) -> Color {
        switch t {
        case .object: return .orange
        case .array: return .teal
        case .string: return .green
        case .number: return .blue
        case .bool: return .purple
        case .null: return .gray
        }
    }
    private func typeLabel(_ t: JSONNodeType) -> String { t.rawValue }

    private func countBadgeText() -> String? {
        switch node.type {
        case .object: return "\(node.children.count) alan"
        case .array: return "\(node.children.count) öğe"
        default: return nil
        }
    }

    // Kopyalama
    private func copyButton(copyText: String) -> some View {
        Button {
            copyToPasteboard(copyText)
        } label: {
            Image(systemName: "doc.on.doc")
                .font(.caption)
        }
        .buttonStyle(.plain)
        .help("Kopyala")
    }

    private func copyToPasteboard(_ s: String) {
        let pb = NSPasteboard.general
        pb.clearContents()
        pb.setString(s, forType: .string)
    }

    // Düğümden JSON fragmanı üret (güzelleştirilmiş)
    private func jsonFragment(from node: JSONNode) -> String {
        func toAny(_ node: JSONNode) -> Any {
            switch node.type {
            case .object:
                var dict: [String: Any] = [:]
                for c in node.children {
                    dict[c.key ?? ""] = toAny(c)
                }
                return dict
            case .array:
                return node.children.map { toAny($0) }
            case .string: return node.value ?? ""
            case .number:
                // Sayı dönüştürme
                if let v = node.value, let d = Double(v) { return d }
                return node.value ?? "0"
            case .bool:
                return (node.value == "true")
            case .null:
                return NSNull()
            }
        }
        let any = toAny(node)
        if JSONSerialization.isValidJSONObject(any),
           let data = try? JSONSerialization.data(withJSONObject: any, options: [.prettyPrinted]),
           let str = String(data: data, encoding: .utf8) {
            return str
        }
        return String(describing: any)
    }
}

#Preview {
    JsonTreeView(jsonString: "{\"a\":1}")
        .frame(width: 500, height: 400)
}
