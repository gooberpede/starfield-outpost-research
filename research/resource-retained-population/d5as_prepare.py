# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare a local D5AS package and compare protected content offline.

Reads the retained Pilot04 package/build/receipts, host files and protected
inputs using owned D5AR/D5AL helpers (SOR-P-0002). Writes only new ignored
artifacts, a dedicated empty series directory and restoration rehearsal copies.
Requires pinned Windows CPython with -E -B and Starfield closed for full audits.
Does not inspect effective deployment, execute native code or alter the target.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import zipfile

import d5ab_p4_operations as protection
from d5al_content import archive_hashes, compare_protection
from d5ar_direct_package import (
    ARCHIVE as PILOT_ZIP, CONFIG, DLL, HOSTS, LOCAL as D5AR, NOTICES, PREFIX, ROOT,
    digest, disk_floor, host_check, plain, qualified, require, sha,
)

LOCAL = ROOT / '.local-work/d5as'
CAPTURE = LOCAL / 'capture'
BEFORE = LOCAL / 'protection-before02/protection.json'
BEFORE_SHA = '49b19aa5bd9043ad5486da1216b3475c1490a3787c05cd9ea21a31c94d2ae6d2'
PACKAGE = LOCAL / 'SorOutpostGeometrySnapshot-0.2.0-D5AS-NOT-AUTHORIZED.zip'
PILOT = PILOT_ZIP.parent
PILOT_PREFLIGHT = PILOT / 'operator-preflight01/preflight.json'
PILOT_PACKAGE_SHA = '47c7ec6e59bd2f5b8ccda3bd92df77d0aa8720765fd6ed52f32bf14a4f71535c'
PILOT_PREFLIGHT_SHA = 'baa081ab974f6c9d33b28533e4f5d183f0e5b7287cf309a19e53c74f3297da44'
DLL_SHA = '207ff49ee06ab52b6cc5978247c4f45b09a41a676ab55b491fa8d7ace1acd401'
SOURCE_LOCK_SHA = '063117f8149060b0347ef475145c9306b49b924cf7d29fcef05216cdadb8eb24'


def write_json(path, data):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(data, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write('\n')


def safe_output(path):
    path = Path(path).absolute()
    require(path.is_relative_to(LOCAL) and '..' not in path.parts and path != LOCAL
            and not path.is_relative_to(CAPTURE), 'Use a fresh D5AS local output outside capture')
    plain(path.parent)
    require(not path.exists() and not path.is_symlink() and not path.is_junction(),
            'Output already exists')
    return path


def config_bytes(folder):
    plain(folder)
    return (str(folder) + '\n').encode('utf-8')


def package():
    free_before = disk_floor()
    host_check()
    require(sha(PILOT_ZIP) == PILOT_PACKAGE_SHA, 'Pilot04 archive identity changed')
    folders = [D5AR / f'direct-worker-rework0{i}' for i in (3, 4)]
    pins = qualified(folders[0])
    require(pins == qualified(folders[1]) and pins[DLL] == DLL_SHA
            and pins['source-lock.json'] == SOURCE_LOCK_SHA, 'Build identity disagreement')
    pilot = json.loads((PILOT / 'packaging.json').read_bytes())
    receipts = {str(p / 'build.json'): sha(p / 'build.json') for p in folders}
    require(receipts == pilot['build_receipts'], 'Historical build receipt identity changed')
    with zipfile.ZipFile(PILOT_ZIP) as archive:
        expected = [PREFIX + DLL, PREFIX + CONFIG, NOTICES + 'PROJECT-LICENSE.txt',
                    NOTICES + 'SFSE-PluginAPI-LICENSE.txt']
        require(sorted(archive.namelist()) == sorted(expected) and archive.testzip() is None,
                'Unexpected Pilot04 archive inventory')
        members = {name: archive.read(name) for name in expected}
    require(members[PREFIX + DLL] == (folders[0] / DLL).read_bytes() and
            members[NOTICES + 'PROJECT-LICENSE.txt'] == (ROOT / 'LICENSE').read_bytes() and
            members[NOTICES + 'SFSE-PluginAPI-LICENSE.txt'] ==
            (ROOT / 'runtime/exp0002/third_party/sfse/LICENSE.txt').read_bytes(),
            'DLL or notice bytes changed')
    before = json.loads(PILOT_PREFLIGHT.read_bytes())['protection']
    require(sha(PILOT_PREFLIGHT) == PILOT_PREFLIGHT_SHA, 'Pilot04 protection receipt changed')
    protected_roots = [Path(before['live_path']), Path(before['sync']['remote_path']),
                       *(Path(p).parent for p in before['archive_guard']),
                       *(Path(row['path']).parent for rows in before['backups'].values()
                         for row in rows)]
    plain(LOCAL.parent)
    require(all(not CAPTURE.is_relative_to(root) and not root.is_relative_to(CAPTURE)
                for root in protected_roots), 'Capture overlaps a protected namespace')
    LOCAL.mkdir(exist_ok=True)
    plain(LOCAL)
    safe_output(PACKAGE)
    safe_output(LOCAL / 'package.json')
    CAPTURE.mkdir()
    members[PREFIX + CONFIG] = config_bytes(CAPTURE)
    # The probe is deliberately separate from the empty statistical directory.
    import tempfile
    with tempfile.TemporaryDirectory(prefix='path-probe-', dir=LOCAL) as scratch:
        probe = Path(scratch) / 'nested'
        probe.mkdir()
        require(config_bytes(probe).decode().strip() == str(probe), 'Sidecar round trip')
        with (probe / 'probe').open('xb') as stream:
            stream.write(b'D5AS disposable output probe\n')
    require(not any(CAPTURE.iterdir()), 'Statistical directory must begin empty')
    with zipfile.ZipFile(PACKAGE, 'x') as archive:
        for name, data in sorted(members.items()):
            item = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            item.external_attr = 0o100644 << 16
            archive.writestr(item, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(PACKAGE) as archive:
        require(archive.namelist() == sorted(members) and archive.testzip() is None and
                all(archive.read(name) == data for name, data in members.items()),
                'Packaged bytes differ')
    result = dict(schema='sor-d5as-package/1', authority='OFFLINE_ONLY_NOT_AUTHORIZED',
                  archive_sha256=sha(PACKAGE), artifacts=pins, build_receipts=receipts,
                  members={name: digest(data) for name, data in members.items()},
                  host_files=HOSTS, capture_directory=str(CAPTURE), free_before=free_before,
                  free_after=disk_floor(), pilot_archive_sha256=PILOT_PACKAGE_SHA,
                  head=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                               text=True).strip(),
                  python=sys.version, interpreter_sha256=sha(Path(sys.executable)))
    write_json(LOCAL / 'package.json', result)
    return result['archive_sha256']


def protected_checkpoint(output, baseline=None):
    free_before = disk_floor()
    output = safe_output(output)
    protection.no_game()
    host_check()
    require(sha(PILOT_PREFLIGHT) == PILOT_PREFLIGHT_SHA, 'Pilot04 protection receipt changed')
    historical = json.loads(PILOT_PREFLIGHT.read_bytes())
    before = historical['protection']
    before_remote_sizes = historical['remote_protected_sizes']
    if baseline is not None:
        require(Path(baseline).absolute() == BEFORE, 'Use the integrated D5AS protected baseline')
        require(sha(BEFORE) == BEFORE_SHA, 'Integrated D5AS protected baseline changed')
        prior = json.loads(BEFORE.read_bytes())
        require(prior['schema'] == 'sor-d5as-protection/1' and prior['phase'] == 'before',
                'D5AS before receipt required')
        before = prior['protection']
        before_remote_sizes = prior['remote_protected_sizes']
    output.mkdir()
    now = protection.full(output)
    now['archive_content_sha256'] = archive_hashes(now)
    comparison = compare_protection(before, now)
    remote = protection.remote_sizes(now)
    require(remote == before_remote_sizes and now['sync']['scientific_inputs_match'],
            'Protected Steam remote contents or namespace changed')
    policy_module = protection.policy_module()
    remote_content = policy_module.partition(now['sync']['remote'], now['save_policy'])['protected']
    if baseline is not None:
        expected = policy_module.partition(before['sync']['remote'], before['save_policy'])['protected']
        require(remote_content == expected,
                'Protected Steam remote content changed')
    value = dict(schema='sor-d5as-protection/1', phase='before' if baseline is None else 'after',
                 checked_utc=datetime.now(timezone.utc).isoformat(), equal=True,
                 previous_sha256=PILOT_PREFLIGHT_SHA if baseline is None else sha(Path(baseline)),
                 comparison=comparison, protection=now, remote_protected_sizes=remote,
                 free_before=free_before, free_after=disk_floor())
    write_json(output / 'protection.json', value)
    return str(output / 'protection.json')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('package', 'protect'))
    parser.add_argument('--output', type=Path)
    parser.add_argument('--baseline', type=Path)
    args = parser.parse_args()
    if args.action == 'package':
        print(package())
    else:
        require(args.output is not None, 'Supply fresh local output directory')
        print(protected_checkpoint(args.output, args.baseline))


if __name__ == '__main__':
    main()
