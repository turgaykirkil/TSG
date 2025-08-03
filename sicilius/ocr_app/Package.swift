// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "ocr_app",
    platforms: [
        .macOS(.v12)
    ],
    products: [
        .executable(name: "ocr_app", targets: ["ocr_app"])
    ],
    dependencies: [
        .package(url: "https://github.com/supabase/supabase-swift.git", from: "2.0.0")
    ],
    targets: [
        .executableTarget(
            name: "ocr_app",
            dependencies: [
                .product(name: "Supabase", package: "supabase-swift")
            ],
            resources: [
                .process("Resources")
            ]
        )
    ]
)

