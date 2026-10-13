import SwiftUI
import RudderStackAnalytics
import RudderIntegrationSprig
import RudderIntegrationFirebase

@main
struct PublicationDemoApp: App {
    var body: some Scene { WindowGroup { DemoView() } }
}

struct DemoView: View {
    // Dummy write key and unroutable URLs: no credentials are needed and no events leave this app.
    // FirebaseApp.configure() and Sprig's environment setup are not called; they need real project settings.
    @State private var analytics: Analytics?
    @State private var integrations: [String] = []

    var body: some View {
        NavigationStack {
            Form {
                Section("Installed packages") {
                    Text("RudderStackAnalytics")
                    Text("RudderIntegrationSprig")
                    Text("RudderIntegrationFirebase")
                    Text("Versions are pinned in Package.resolved.").font(.footnote)
                }
                Section("Integrations") {
                    Text(integrations.isEmpty ? "Not configured" : integrations.joined(separator: ", "))
                        .accessibilityIdentifier("result")
                }
                Text("Temporary unsupported publication experiment. No events leave this app.")
            }.navigationTitle("Publication Lab").onAppear { configure() }
        }
    }

    private func configure() {
        guard analytics == nil else { return }
        let configuration = Configuration(writeKey: "consumer-demo-write-key",
                                          dataPlaneUrl: "https://data-plane.invalid",
                                          controlPlaneUrl: "https://control-plane.invalid")
        let analytics = Analytics(configuration: configuration)
        let sprig = SprigIntegration()
        let firebase = FirebaseIntegration()
        analytics.add(plugin: sprig)
        analytics.add(plugin: firebase)
        self.analytics = analytics
        integrations = [sprig.key, firebase.key]
    }
}
