"""Run the public consumer with fresh package state and no GitHub credentials."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def verify(root=ROOT, local_remotes=None, ios=False):
    env = {k: v for k, v in os.environ.items() if k not in
           ('GH_TOKEN', 'GITHUB_TOKEN', 'GIT_ASKPASS', 'SSH_ASKPASS') and not k.startswith('GIT_CONFIG')}
    env.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1', GIT_TERMINAL_PROMPT='0',
               GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='credential.helper', GIT_CONFIG_VALUE_0='')
    def run(args):
        result = subprocess.run([str(x) for x in args], cwd=root, env=env, text=True, capture_output=True)
        if result.returncode:
            raise RuntimeError(result.stdout + '\n' + result.stderr)
        return result.stdout
    deps = json.loads((root / 'dependencies.json').read_text())
    if local_remotes:
        for index, d in enumerate(deps.values(), 1):
            name = d['url'].rsplit('/', 1)[1]
            mirror = (local_remotes / name).resolve().as_uri()
            run(['swift', 'package', 'config', 'set-mirror', '--original', d['url'], '--mirror', mirror])
            # Xcode's system Git transport also needs the isolated local URL mapping.
            env[f'GIT_CONFIG_KEY_{index}'] = f'url.{mirror}.insteadOf'
            env[f'GIT_CONFIG_VALUE_{index}'] = d['url']
        env['GIT_CONFIG_COUNT'] = str(len(deps) + 1)
    elif (root / '.swiftpm/configuration/mirrors.json').exists():
        raise ValueError('Remove local mirrors before anonymous public validation')
    with tempfile.TemporaryDirectory(prefix='swift-consumer-state-') as temp:
        state = Path(temp)
        flags = ['--cache-path', state/'cache', '--config-path', state/'config',
                 '--security-path', state/'security', '--scratch-path', state/'build',
                 '--disable-dependency-cache', '--disable-keychain', '--disable-netrc']
        output = run(['swift', 'run', *flags, 'ConsumerDemo'])
        result = json.loads(output.strip().splitlines()[-1])
        for key, dep in deps.items():
            if result[key] != dep['version']:
                raise ValueError(f'Runtime version differs for {key}')
        pins = json.loads((root/'Package.resolved').read_text())
        for dep in deps.values():
            name = dep['url'].rsplit('/', 1)[1].removesuffix('.git')
            pin = next(p for p in pins['pins'] if p['identity'] == name)
            if pin['state']['version'] != dep['version']:
                raise ValueError(f'Resolver selected the wrong version for {name}')
        if ios:
            output = run(['xcodebuild', '-project', 'PublicationDemo.xcodeproj', '-scheme', 'PublicationDemo',
                          '-configuration', 'Debug', '-sdk', 'iphonesimulator',
                          '-destination', 'generic/platform=iOS Simulator',
                          '-derivedDataPath', root/'DerivedData', '-clonedSourcePackagesDirPath', state/'xcode-packages',
                          '-scmProvider', 'system', 'CODE_SIGNING_ALLOWED=NO', 'build'])
            if '** BUILD SUCCEEDED **' not in output:
                raise ValueError('Xcode did not report a successful build')
            result['iOSSimulatorBuild'] = 'passed'
    return {'runtime': result, 'resolved': pins,
            'transport': 'local-git-mirrors' if local_remotes else 'anonymous-public-git'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--local-remotes', type=Path)
    parser.add_argument('--ios', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(local_remotes=args.local_remotes, ios=args.ios), indent=2))
