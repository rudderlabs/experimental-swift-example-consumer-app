import SwiftUI
import DemoSDK
import DemoSprig
import DemoFirebase

@main
struct PublicationDemoApp: App {
    var body: some Scene { WindowGroup { DemoView() } }
}
struct DemoView: View {
    @State private var event = "  Demo   Event "
    @State private var result = "Ready to invoke all three published packages."
    var body: some View {
        NavigationStack {
            Form {
                Section("Installed packages") {
                    LabeledContent("SDK", value: DemoSDKVersion.current)
                    LabeledContent("Sprig", value: DemoSprigVersion.current)
                    LabeledContent("Firebase", value: DemoFirebaseVersion.current)
                }
                Section("Event") {
                    TextField("Event name", text: $event)
                    Button("Run package checks") { check() }
                    Text(result).accessibilityIdentifier("result")
                }
                Section("SDK resource") {
                    Text((try? DemoSDK.resourceMessage()) ?? "Resource failed")
                    Text(DemoSDK.hasPrivacyManifest() ? "Privacy manifest loaded" : "Privacy manifest missing")
                }
                Text("Temporary unsupported publication experiment. No events leave this app.")
            }.navigationTitle("Publication Lab").onAppear { check() }
        }
    }
    private func check() {
        let sprig = DemoSprig.track(event)
        let firebase = DemoFirebase.track([event, event])
        result = "Sprig: \(sprig.name)\nFirebase: \(firebase.count) unique event(s)"
    }
}
