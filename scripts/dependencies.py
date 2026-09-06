"""Generate both consumer manifests from one explicit version selection."""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def render(root=ROOT, updates=()):
    path = root / "dependencies.json"
    dependencies = json.loads(path.read_text())
    for update in updates:
        key, version = update.split("=", 1)
        if key not in dependencies or not re.fullmatch(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", version):
            raise ValueError("Expected sdk=X.Y.Z, sprig=X.Y.Z, or firebase=X.Y.Z")
        dependencies[key]["version"] = version
    path.write_text(json.dumps(dependencies, indent=2) + "\n")
    specs, products = [], []
    for d in dependencies.values():
        identity = d['url'].rsplit('/', 1)[1].removesuffix('.git')
        specs.append(f'.package(url: "{d["url"]}", exact: "{d["version"]}")')
        products.append(f'.product(name: "{d["product"]}", package: "{identity}")')
    (root / "Package.swift").write_text(f'''// swift-tools-version: 5.9
import PackageDescription
let package = Package(
    name: "PublicationConsumer",
    platforms: [.iOS(.v15), .macOS(.v12)],
    dependencies: [{", ".join(specs)}],
    targets: [.executableTarget(name: "ConsumerDemo", dependencies: [{", ".join(products)}])]
)
''')
    def uid(number):
        return f"{number:024X}"
    rows = []
    def obj(number, body):
        rows.append(f"{uid(number)} = {{ {body} }};")
    refs, prods, builds = [], [], []
    for index, d in enumerate(dependencies.values()):
        ref, prod, build = 100 + index, 200 + index, 300 + index
        refs.append(uid(ref)); prods.append(uid(prod)); builds.append(uid(build))
        obj(ref, f'isa = XCRemoteSwiftPackageReference; repositoryURL = "{d["url"]}"; requirement = {{ kind = exactVersion; version = {d["version"]}; }};')
        obj(prod, f'isa = XCSwiftPackageProductDependency; package = {uid(ref)}; productName = {d["product"]};')
        obj(build, f'isa = PBXBuildFile; productRef = {uid(prod)};')
    obj(1, f'isa = PBXProject; attributes = {{ LastUpgradeCheck = 2600; }}; buildConfigurationList = {uid(10)}; compatibilityVersion = "Xcode 14.0"; developmentRegion = en; knownRegions = (en, Base); mainGroup = {uid(2)}; productRefGroup = {uid(3)}; projectDirPath = ""; projectRoot = ""; targets = ({uid(4)}); packageReferences = ({", ".join(refs)});')
    obj(2, f'isa = PBXGroup; children = ({uid(5)}, {uid(3)}); sourceTree = "<group>";')
    obj(3, f'isa = PBXGroup; children = ({uid(6)}); name = Products; sourceTree = "<group>";')
    obj(4, f'isa = PBXNativeTarget; buildConfigurationList = {uid(11)}; buildPhases = ({uid(7)}, {uid(8)}, {uid(9)}); buildRules = (); dependencies = (); name = PublicationDemo; productName = PublicationDemo; productReference = {uid(6)}; productType = "com.apple.product-type.application"; packageProductDependencies = ({", ".join(prods)});')
    obj(5, 'isa = PBXFileReference; lastKnownFileType = sourcecode.swift; path = iOS/PublicationDemoApp.swift; sourceTree = "<group>";')
    obj(6, 'isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; path = PublicationDemo.app; sourceTree = BUILT_PRODUCTS_DIR;')
    obj(7, f'isa = PBXSourcesBuildPhase; buildActionMask = 2147483647; files = ({uid(14)}); runOnlyForDeploymentPostprocessing = 0;')
    obj(8, f'isa = PBXFrameworksBuildPhase; buildActionMask = 2147483647; files = ({", ".join(builds)}); runOnlyForDeploymentPostprocessing = 0;')
    obj(9, 'isa = PBXResourcesBuildPhase; buildActionMask = 2147483647; files = (); runOnlyForDeploymentPostprocessing = 0;')
    obj(10, f'isa = XCConfigurationList; buildConfigurations = ({uid(15)}, {uid(16)}); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release;')
    obj(11, f'isa = XCConfigurationList; buildConfigurations = ({uid(17)}, {uid(18)}); defaultConfigurationIsVisible = 0; defaultConfigurationName = Release;')
    obj(14, f'isa = PBXBuildFile; fileRef = {uid(5)};')
    for index, mode in [(15, 'Debug'), (16, 'Release')]:
        obj(index, f'isa = XCBuildConfiguration; buildSettings = {{ SDKROOT = iphoneos; IPHONEOS_DEPLOYMENT_TARGET = 16.0; SWIFT_VERSION = 5.0; CLANG_ENABLE_MODULES = YES; }}; name = {mode};')
    for index, mode in [(17, 'Debug'), (18, 'Release')]:
        optimization = '-Onone' if mode == 'Debug' else '-O'
        obj(index, f'isa = XCBuildConfiguration; buildSettings = {{ GENERATE_INFOPLIST_FILE = YES; INFOPLIST_KEY_UILaunchScreen_Generation = YES; INFOPLIST_KEY_UIApplicationSceneManifest_Generation = YES; PRODUCT_BUNDLE_IDENTIFIER = com.rudderstack.experimental.spmpublish; PRODUCT_NAME = "$(TARGET_NAME)"; CURRENT_PROJECT_VERSION = 1; MARKETING_VERSION = 0.1.0; CODE_SIGN_STYLE = Automatic; TARGETED_DEVICE_FAMILY = "1,2"; SWIFT_OPTIMIZATION_LEVEL = "{optimization}"; }}; name = {mode};')
    project = root / "PublicationDemo.xcodeproj"
    project.mkdir(exist_ok=True)
    (project / "project.pbxproj").write_text('// !$*UTF8*$!\n{ archiveVersion = 1; classes = {}; objectVersion = 60; objects = {\n' + '\n'.join(rows) + f'\n}}; rootObject = {uid(1)}; }}\n')
    scheme = project / "xcshareddata/xcschemes/PublicationDemo.xcscheme"
    scheme.parent.mkdir(parents=True, exist_ok=True)
    reference = f'<BuildableReference BuildableIdentifier="primary" BlueprintIdentifier="{uid(4)}" BuildableName="PublicationDemo.app" BlueprintName="PublicationDemo" ReferencedContainer="container:PublicationDemo.xcodeproj"/>'
    scheme.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<Scheme LastUpgradeVersion="2600" version="1.3">
<BuildAction parallelizeBuildables="YES" buildImplicitDependencies="YES"><BuildActionEntries>
<BuildActionEntry buildForTesting="YES" buildForRunning="YES" buildForProfiling="YES" buildForArchiving="YES" buildForAnalyzing="YES">{reference}</BuildActionEntry>
</BuildActionEntries></BuildAction>
<LaunchAction buildConfiguration="Debug" selectedDebuggerIdentifier="Xcode.DebuggerFoundation.Debugger.LLDB" selectedLauncherIdentifier="Xcode.IDEFoundation.Launcher.LLDB" launchStyle="0" useCustomWorkingDirectory="NO" ignoresPersistentStateOnLaunch="NO" debugDocumentVersioning="YES" allowLocationSimulation="YES"><BuildableProductRunnable runnableDebuggingMode="0">{reference}</BuildableProductRunnable></LaunchAction>
<ProfileAction buildConfiguration="Release" shouldUseLaunchSchemeArgsEnv="YES" savedToolIdentifier="" useCustomWorkingDirectory="NO" debugDocumentVersioning="YES"><BuildableProductRunnable runnableDebuggingMode="0">{reference}</BuildableProductRunnable></ProfileAction>
<AnalyzeAction buildConfiguration="Debug"/>
<ArchiveAction buildConfiguration="Release" revealArchiveInOrganizer="YES"/>
</Scheme>
''')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", action="append", default=[])
    args = parser.parse_args()
    render(updates=args.set)
