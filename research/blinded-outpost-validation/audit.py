# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline archive-backed preservation and installed-identity receipt.

Adapted from owned D5H audit.py at the starting HEAD. Reads protected sources,
active archive/index, save policy, installed inputs and Git identity. Writes an
exclusive task-local receipt. No restored payloads, target or Git mutations.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT/'.local-work/blinded-outpost-validation'


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path, value):
    with Path(path).open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def main():
    output = Path(sys.argv[1]).resolve()
    if not output.is_relative_to(LOCAL) or output.exists():
        raise ValueError('FRESH_LOCAL_RECEIPT_REQUIRED')
    free = {d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}
    if min(free.values()) < 40000000000:
        raise ValueError('DISK_FLOOR')
    start = json.loads((LOCAL/'start.json').read_bytes())
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    if head != start['head'] or pin(ROOT/'.git/index') != start['index_sha256']:
        raise ValueError('GIT_IDENTITY_CHANGED')
    brief = ROOT/'docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5K_stage_a_blinded_validation_toolchain.md'
    if pin(brief) != start['brief_sha256'] or pin(ROOT/'docs/experiments/blinded-outpost-validation/contract.md') != start['contract_sha256']:
        raise ValueError('FROZEN_CONTRACT_CHANGED')
    sys.path.insert(0, str(ROOT/'research/resources-evidence-consolidation'))
    from resources_preservation import verify_historical
    protection = verify_historical()
    from bridge import EXE, ESM, PLANET
    base = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
    installed = {}
    for name, expected in (('Starfield.exe', EXE), ('Data/Starfield.esm', ESM), ('Data/Starfield - PlanetData.ba2', PLANET)):
        actual = pin(base/name)
        if actual != expected:
            raise ValueError('UNKNOWN_INSTALLED_INPUT: ' + name)
        installed[name] = actual
    if subprocess.check_output(['git', 'diff', '--cached', '--name-only']):
        raise ValueError('STAGED_WORK')
    write(output, dict(head=head, index_sha256=start['index_sha256'],
        brief_sha256=start['brief_sha256'], installed=installed, protection=protection,
        free=free, staged_changes=False))
    print('Archive-backed protected inputs, installed identities, brief and HEAD/index: PASS')


if __name__ == '__main__':
    main()
