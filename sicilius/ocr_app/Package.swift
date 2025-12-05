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
    dependencies: [],
    targets: [
        .executableTarget(
            name: "ocr_app",
            dependencies: [],
            resources: [
                .process("Resources")
            ]
        ),
        .testTarget(
            name: "ocr_appTests",
            dependencies: ["ocr_app"]
        )
    ]
)

