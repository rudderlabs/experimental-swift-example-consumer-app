// swift-tools-version: 5.9
import PackageDescription
let package = Package(
    name: "PublicationConsumer",
    platforms: [.iOS(.v15), .macOS(.v12)],
    dependencies: [.package(url: "https://github.com/rudderlabs/experimental-rudder-sdk-swift.git", exact: "1.4.1"), .package(url: "https://github.com/rudderlabs/experimental-integration-swift-sprig.git", exact: "1.0.1"), .package(url: "https://github.com/rudderlabs/experimental-integration-swift-firebase.git", exact: "1.1.3")],
    targets: [.executableTarget(name: "ConsumerDemo", dependencies: [.product(name: "RudderStackAnalytics", package: "experimental-rudder-sdk-swift"), .product(name: "RudderIntegrationSprig", package: "experimental-integration-swift-sprig", condition: .when(platforms: [.iOS])), .product(name: "RudderIntegrationFirebase", package: "experimental-integration-swift-firebase")])]
)
