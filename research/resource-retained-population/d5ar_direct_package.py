# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare Pilot04 from two qualified local builds or check deployed files.

Reads build/host identities and notices. Build writes a fresh ignored archive,
receipt and empty capture directory. The deployed check is read-only. Neither
action starts Starfield, deploys files, changes saves or contacts a network.
"""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import zipfile

if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '0') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

from d5ar_native_inventory import disk_floor

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/d5ar'
PACKAGE = LOCAL / 'pilot-vortex04-rework01'
CAPTURE = PACKAGE / 'capture'
ARCHIVE = PACKAGE / 'SorOutpostGeometrySnapshot-0.2.0-D5AR-Vortex-Pilot04-REWORK01-NOT-AUTHORIZED.zip'
REVIEW = 'SorOutpostGeometrySnapshot-0.2.0-NOT-AUTHORIZED.zip'
RECEIPT = PACKAGE / 'packaging.json'
CARD = ROOT / 'docs/experiments/resource-retained-population/run-card-d5ar-pilot04-proposal.md'
PRIOR_CARD = CARD.with_name('run-card-d5ar-pilot-proposal.md')
GAME = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
DLL = 'SorOutpostGeometrySnapshot.dll'
CONFIG = 'SorOutpostGeometrySnapshot.output-path'
PREFIX = 'Data/SFSE/Plugins/'
NOTICES = PREFIX + 'SorOutpostGeometrySnapshot-notices/'
MIT = 'runtime/exp0002/third_party/sfse/LICENSE.txt'
HOSTS = {
    'Starfield.exe': '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28',
    'sfse_1_16_244.dll': '28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b',
    'sfse_loader.exe': '16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def plain(path):
    for directory in (path, *path.parents):
        require(directory.is_dir() and not directory.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT,
                f'Expected a plain directory at {directory}')


def host_check():
    for name, expected in HOSTS.items():
        require(sha(GAME / name) == expected, f'Installed host identity mismatch for {name}')


def qualified(folder):
    plain(folder)
    receipt = json.loads((folder / 'build.json').read_bytes())
    require(receipt['exit'] == receipt['bridge_fixture_exit'] == 0 and receipt['source_preserved'],
            'Build, source preservation or bridge control failed')
    require(receipt['exact_dll_modes'] == [dict(mode=i, exit=0) for i in range(81)] and
            set(receipt['direct_worker_controls']) == {str(i) for i in range(62, 81)} and
            all(receipt['direct_worker_controls'][str(mode)]['copy_status'] == status
                for mode, status in ((76, 'COPIED_UNQUALIFIED'), (77, 'COPIED_UNQUALIFIED'),
                                     (78, 'OPERATOR_STOP_DURING_PUBLICATION'), (79, 'DIRECT_OBSERVER_EXCEPTION'),
                                     (80, 'COPIED_UNQUALIFIED'))) and
            {row['kind']: row['exit'] for row in receipt['negative_host_guards']} == {'renamed': 6, 'modified': 6},
            'Exact DLL controls did not all qualify')
    pins = {
        DLL: receipt['dll_sha256'],
        'source-lock.json': receipt['source_lock_sha256'],
        'd5ar-plugin-fixture.exe': receipt['fixture_host_sha256'],
        'd5ar-bridge-fixture.exe': sha(folder / 'd5ar-bridge-fixture.exe'),
        REVIEW: receipt['package_sha256'],
    }
    require(all(sha(folder / name) == value for name, value in pins.items()), 'Build artifact identity mismatch')
    lock = json.loads((folder / 'source-lock.json').read_bytes())
    require(all(sha(ROOT / name) == value for name, value in lock['files'].items()), 'Current source differs from build')
    return pins


def build():
    free = disk_floor()
    host_check()
    plain(LOCAL)
    first, second = (LOCAL / name for name in ('direct-worker-rework03', 'direct-worker-rework04'))
    pins = qualified(first)
    require(pins == qualified(second), 'Independent clean build artifacts differ')
    dll = (first / DLL).read_bytes()
    gpl, mit = (ROOT / 'LICENSE').read_bytes(), (ROOT / MIT).read_bytes()
    with zipfile.ZipFile(first / REVIEW) as review:
        require(review.testzip() is None and review.read(DLL) == dll and
                review.read('LICENSE') == gpl and review.read(MIT) == mit,
                'Review ZIP payload or notice mismatch')
    PACKAGE.mkdir()
    CAPTURE.mkdir()
    plain(CAPTURE)
    members = {PREFIX + DLL: dll, PREFIX + CONFIG: (str(CAPTURE) + '\n').encode('utf-8'),
               NOTICES + 'PROJECT-LICENSE.txt': gpl, NOTICES + 'SFSE-PluginAPI-LICENSE.txt': mit}
    with zipfile.ZipFile(ARCHIVE, 'x') as archive:
        for name, data in sorted(members.items()):
            item = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            item.external_attr = 0o100644 << 16
            archive.writestr(item, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(ARCHIVE) as archive:
        require(archive.namelist() == sorted(members) and archive.testzip() is None and
                all(archive.read(name) == data for name, data in members.items()), 'Vortex archive mismatch')
    require(not any(CAPTURE.iterdir()), 'Capture directory is not empty')
    receipt = dict(status='PASS_OFFLINE_PACKAGING_PILOT_APPROVAL_SEPARATE',
                   archive_sha256=sha(ARCHIVE), artifacts=pins,
                   build_receipts={str(folder / 'build.json'): sha(folder / 'build.json') for folder in (first, second)},
                   operator_card_sha256=sha(CARD), inherited_card_sha256=sha(PRIOR_CARD),
                   method_sha256=sha(Path(__file__)), host_files=HOSTS, capture_directory=str(CAPTURE),
                   members={name: digest(data) for name, data in members.items()},
                   free_before=free, free_after=disk_floor())
    with RECEIPT.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')
    print(receipt['status'], receipt['archive_sha256'])


def check_deployed():
    free = disk_floor()
    host_check()
    plain(CAPTURE)
    receipt = json.loads(RECEIPT.read_bytes())
    require(receipt['status'] == 'PASS_OFFLINE_PACKAGING_PILOT_APPROVAL_SEPARATE' and
            receipt['archive_sha256'] == sha(ARCHIVE) and receipt['operator_card_sha256'] == sha(CARD) and
            receipt['inherited_card_sha256'] == sha(PRIOR_CARD) and receipt['method_sha256'] == sha(Path(__file__)),
            'Package, card or method changed')
    with zipfile.ZipFile(ARCHIVE) as archive:
        require(archive.namelist() == sorted(receipt['members']) and archive.testzip() is None,
                'Archive layout or CRC mismatch')
        for name, expected in receipt['members'].items():
            require(digest(archive.read(name)) == expected, f'Archive member differs at {name}')
            path = GAME / name
            require(path.is_file() and sha(path) == expected, f'Deployed member missing or differs at {path}')
    for parent in (GAME, GAME / 'Data', GAME / 'Data/Data/SFSE/Plugins'):
        for name in (DLL, CONFIG):
            path = parent / name
            require(not path.exists() and not path.is_symlink(), f'Unexpected duplicate at {path}')
    require(not any(CAPTURE.iterdir()), 'Capture directory is not empty')
    print(json.dumps(dict(status='PASS_DEPLOYED_FILES_ONLY', free=free, capture_directory=str(CAPTURE))))


if __name__ == '__main__':
    require(len(sys.argv) == 2 and sys.argv[1] in ('build', 'check-deployed'), 'Use build or check-deployed')
    (build if sys.argv[1] == 'build' else check_deployed)()
