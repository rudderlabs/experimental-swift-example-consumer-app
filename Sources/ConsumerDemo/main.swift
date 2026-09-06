import Foundation
import DemoSDK
import DemoSprig
import DemoFirebase

let sprig = DemoSprig.track("  Demo   Event ")
let firebase = DemoFirebase.track([" Demo Event ", "demo event"])
precondition(sprig.name == "demo event")
precondition(firebase.count == 1 && firebase[0].name == "demo event")
precondition(DemoSDK.hasPrivacyManifest())
let resource = try DemoSDK.resourceMessage()
precondition(resource == "standalone resource loaded")
let result: [String: Any] = [
    "sdk": DemoSDKVersion.current,
    "sprig": DemoSprigVersion.current,
    "firebase": DemoFirebaseVersion.current,
    "event": sprig.name,
    "vendorDeduplicatedCount": firebase.count,
    "resource": resource,
    "privacyManifest": true
]
print(String(data: try JSONSerialization.data(withJSONObject: result, options: [.sortedKeys]), encoding: .utf8)!)
