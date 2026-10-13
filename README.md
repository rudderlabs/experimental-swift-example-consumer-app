# SwiftPM publication consumer

Temporary, unsupported SDK-5388 experiment. This consumer has no dependency on the private source repository.
It installs the experimental public packages: `RudderStackAnalytics` (SDK), `RudderIntegrationSprig` (iOS only), and `RudderIntegrationFirebase`.
No credentials or real write key are needed. The demos use a dummy write key and unroutable URLs, so no events leave the app,
and they do not call `FirebaseApp.configure()` or set up Sprig.

1. Run `python3 scripts/dependencies.py` to generate the SwiftPM manifest and Xcode project.
2. Run `swift run ConsumerDemo` (macOS): it configures Analytics with the Firebase integration. Sprig is linked only on iOS.
3. Open `PublicationDemo.xcodeproj` to run the iOS app, which links all three products.
4. Run `python3 scripts/dependencies.py --set sprig=1.0.1 --set sdk=1.2.1` to select versions (one `--set` per package).
5. Run `python3 scripts/verify.py --ios` to resolve anonymously and build the CLI and the iOS Simulator app.
6. Review `Package.resolved`. The SDKs keep their version constants internal, so the verifier checks versions through its pins.

For the local rehearsal, use `scripts/verify.py --local-remotes <absolute-path>`.
Local mirrors change transport only. The manifests retain the planned public URLs.
Keep local mirror configuration and locally generated lockfiles out of remote commits.
After remote publication, commit the clean public `Package.resolved` with an application upgrade.

## Branch

Use default `main` for consumer changes and CI. Subsequent updates require reviewed PRs.
Package versions still come from semantic version tags; the app does not depend on a package branch.

## Branch compatibility checks

Normal consumer configuration uses exact package versions. Branch requirements are an opt-in migration test in disposable copies, not the recommended installation mode.

```sh
python3 scripts/dependencies.py --set sprig=1.0.1 --branch sprig=main
python3 scripts/verify.py
```

The branch field selects the Git branch to resolve, and the verifier checks the branch recorded in Package.resolved. Both SwiftPM and Xcode manifests use the same selected requirement.

The source rehearsal exercises these selections locally. Hosted public branch checks remain separate acceptance evidence.
