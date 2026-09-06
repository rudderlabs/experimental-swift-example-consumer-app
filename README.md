# SwiftPM publication consumer

Temporary, unsupported SDK-5388 experiment. This consumer has no dependency on the private source repository.
The demo uses representative libraries, not the actual RudderStack, Sprig, or Firebase SDKs.
Apple Swift Collections supplies the real public vendor dependency.
No credentials, write key, or data plane is needed. Events remain in memory.

1. Run `python3 scripts/dependencies.py` to generate the SwiftPM manifest and Xcode project.
2. Run `swift run ConsumerDemo` to resolve the public package tags and check all three products.
3. Open `PublicationDemo.xcodeproj` to run the iOS app.
4. Run `python3 scripts/dependencies.py --set sprig=0.1.1` to select a newly published version.
5. Run `swift run ConsumerDemo` again.
6. Review `Package.resolved` and the printed runtime versions.

Public URLs will resolve only after the experimental repositories are approved and published.
For the local rehearsal, use `scripts/verify.py --local-remotes <absolute-path>`.
Local mirrors change transport only. The manifests retain the planned public URLs.
Keep local mirror configuration and locally generated lockfiles out of remote commits.
After remote publication, commit the clean public `Package.resolved` with an application upgrade.
