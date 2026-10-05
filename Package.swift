// swift-tools-version: 5.9
import PackageDescription
let package = Package(
    name: "PublicationConsumer",
    platforms: [.iOS(.v15), .macOS(.v12)],
    dependencies: [.package(url: "https://github.com/rudderlabs/experimental-rudder-sdk-swift.git", exact: "0.1.0"), .package(url: "https://github.com/rudderlabs/experimental-integration-swift-sprig.git", exact: "0.1.0"), .package(url: "https://github.com/rudderlabs/experimental-integration-swift-firebase.git", exact: "0.1.0")],
    targets: [.executableTarget(name: "ConsumerDemo", dependencies: [.product(name: "DemoSDK", package: "experimental-rudder-sdk-swift"), .product(name: "DemoSprig", package: "experimental-integration-swift-sprig"), .product(name: "DemoFirebase", package: "experimental-integration-swift-firebase")])]
)
