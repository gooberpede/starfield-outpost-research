# SPDX-License-Identifier: GPL-3.0-or-later
"""Rehash the frozen B1 audit inputs without loading native code or saves.

Reads installed files, original D5X manifests/package/source and designated
Save52 bytes. Uses the owned R1 PE reader for disk RVA mapping. Writes only a
fresh ignored audit receipt; no deployment, process, network, save/configuration,
analysis-project or Git mutation. Save bytes are hashed, never parsed/copied.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/d5x-b1-audit'
FROZEN = ROOT / '.local-work/d5x'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    label = sys.argv[1]
    assert re.fullmatch('[a-z0-9-]+', label)
    out = LOCAL / label
    out.mkdir(parents=True, exist_ok=False)
    compatibility = json.loads((FROZEN / 'compatibility01.json').read_text())
    installed = {name: sha(name) for name in compatibility['installed']}
    assert installed == compatibility['installed']
    spec = importlib.util.spec_from_file_location('owned_pe', ROOT / 'runtime/retained-population/build.py')
    pe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pe)
    image = Path(next(n for n in installed if n.endswith('Starfield.exe'))).read_bytes()
    guards = []
    for index, (rva, value) in enumerate(compatibility['sites'].items()):
        data = pe.pe_read(image, int(rva, 16), 32)
        assert hashlib.sha256(data).hexdigest() == value['raw_sha256']
        assert data[:value['length']].hex() == value['displaced_hex']
        guards.append(dict(index=index, rva=int(rva, 16), **value))
    generated = FROZEN / 'build24/identity.generated.h'
    targets = re.findall(r'\{(\d+),"([a-f0-9]{64})"\}', generated.read_text())
    assert len(targets) == 6
    for rva, digest in targets:
        assert hashlib.sha256(pe.pe_read(image, int(rva), 32)).hexdigest() == digest
    card = 'docs/experiments/resource-retained-population/run-card-d5x-b1.md'
    frozen_pins = {}
    for name in compatibility['pins']:
        if name == card:
            original = subprocess.check_output(['git', '--no-optional-locks', 'show', 'HEAD:'+card], cwd=ROOT)
            frozen_pins[name] = hashlib.sha256(original).hexdigest()
        else:
            frozen_pins[name] = sha(ROOT / name)
    assert frozen_pins == compatibility['pins']
    package = FROZEN / 'build24/SorConstructionWinner-D5X-review.zip'
    with zipfile.ZipFile(package) as archive:
        members = archive.namelist()
        assert sorted(members) == ['COPYING', 'Data/SFSE/Plugins/SorConstructionWinner.dll', 'SFSE-PluginAPI-MIT.txt']
        assert hashlib.sha256(archive.read(members[0])).hexdigest() == sha(FROZEN / 'build24/SorConstructionWinner.dll')
    policy = ROOT / 'research/resource-carinae-source-context/save_policy.json'
    protected = json.loads(policy.read_text())['designated']
    name = next(n for n in protected if n.startswith('Save52_'))
    save = Path('C:/Users/User/Documents/My Games/Starfield/Saves') / name
    observed_save = dict(path=str(save), bytes=save.stat().st_size, sha256=sha(save))
    assert observed_save['bytes'] == protected[name]['bytes'] and observed_save['sha256'] == protected[name]['sha256']
    build = json.loads((FROZEN / 'build24/build.json').read_text())
    assert all(sha(name) == digest for name, digest in build['inputs'].items())
    assert all(sha(FROZEN / 'build24' / name) == digest for name, digest in build['outputs'].items())
    git = lambda *args: subprocess.check_output(['git', '--no-optional-locks', *args], cwd=ROOT).decode().strip()
    receipt = dict(schema='sor-d5x-b1-audit-identity/1', authority='OFFLINE_ONLY; B1/B2 NOT AUTHORIZED',
                   installed=installed, sites=guards, targets=targets, frozen_pins=frozen_pins,
                   package_members=members, save52=observed_save, save_policy_sha256=sha(policy),
                   head=git('rev-parse', 'HEAD'), index_sha256=sha(ROOT / '.git/index'), status=git('status', '--short'),
                   disk_free={d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')},
                   script_sha256=sha(__file__), python_sha256=sha(sys.executable),
                   compatibility_sha256=sha(FROZEN / 'compatibility01.json'),
                   proposed_card_sha256=sha(ROOT/card), original_card_basis='HEAD bytes, separately from proposed amendment',
                   note='Save52 hash only; not a fresh full live protection/backup/Cloud preflight')
    assert min(receipt['disk_free'].values()) >= 40_000_000_000
    (out / 'identity.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(receipt=str(out/'identity.json'), sites=len(guards), targets=len(targets), save52=observed_save, passed=True), indent=2))


if __name__ == '__main__':
    main()
