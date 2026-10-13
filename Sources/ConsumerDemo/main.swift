import Foundation
import RudderStackAnalytics
import RudderIntegrationFirebase

// Sprig is iOS only, so this macOS CLI links the SDK and Firebase; the iOS app links all three.
// Dummy write key and unroutable URLs: no credentials are needed and no events leave this process.
// FirebaseApp.configure() is not called because it needs a GoogleService-Info.plist.
let configuration = Configuration(writeKey: "consumer-demo-write-key",
                                  dataPlaneUrl: "https://data-plane.invalid",
                                  controlPlaneUrl: "https://control-plane.invalid",
                                  trackApplicationLifecycleEvents: false)
let analytics = Analytics(configuration: configuration)
let firebase = FirebaseIntegration()
analytics.add(plugin: firebase)
analytics.shutdown()

// Versions are checked from Package.resolved pins (the SDKs keep version constants internal).
let result: [String: Any] = [
    "analytics": "configured",
    "integrations": [firebase.key]
]
print(String(data: try JSONSerialization.data(withJSONObject: result, options: [.sortedKeys]), encoding: .utf8)!)
