# SPDX-License-Identifier: GPL-3.0-or-later
"""Reverify local identities and exact hook bytes without executing the target.

Reads installed game/data/SFSE and existing owned source/static exports. Writes
one exclusive ignored receipt and raw site bytes under .local-work/d5x. CPython
stdlib only; no database, save, configuration, Git or network writes.
"""
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    out = ROOT / '.local-work/d5x' / sys.argv[1]
    out.mkdir(exist_ok=False)
    spec = importlib.util.spec_from_file_location('owned_build', ROOT / 'runtime/retained-population/build.py')
    build = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build)
    prior = json.loads((ROOT / '.local-work/d5w/initial.json').read_text())
    installed = {name: sha(name) for name in prior['installed']}
    assert installed == prior['installed']
    sfse = Path(json.loads((ROOT / '.local-work/native-oracle-050/builds/qualification-03/build.json').read_text())['sfse_path'])
    assert sha(sfse) == build.SFSE_HASH
    installed[str(sfse)] = sha(sfse)
    loader = build.GAME / 'sfse_loader.exe'
    assert loader.is_file()
    installed[str(loader)] = sha(loader)
    database = {name: sha(name) for name in prior['database']}
    assert database == prior['database']
    data = (build.GAME / 'Starfield.exe').read_bytes()
    ranges = {}
    for rva, size in ((0x79de77,0x52),(0x79fc37,0x71),(0x79fcb3,0x27),(0x23393f0,0x3b)):
        raw = build.pe_read(data,rva,size)
        (out / f'cfg-{rva:x}.bin').write_bytes(raw)
        ranges[f'0x{rva:x}'] = dict(bytes=size,sha256=hashlib.sha256(raw).hexdigest())
    sites = {}
    for rva, count in [(0x79f860, 7), (0x79fa90, 8), (0x79fca3, 9),
                       (0x79fccb, 5), (0x79feaf, 5), (0x79ff18, 5), (0x79b8e8, 5),
                       (0x79ddf0, 5), (0x79d910, 5), (0x975030, 8),
                       (0x9829b0, 5), (0x982b70, 5), (0x79dec4, 5), (0x78d6f4,5)]:
        raw = build.pe_read(data, rva, 32)
        (out / f'{rva:x}.bin').write_bytes(raw)
        sites[f'0x{rva:x}'] = dict(length=count, raw_sha256=hashlib.sha256(raw).hexdigest(), displaced_hex=raw[:count].hex())
    paths = [ROOT / 'runtime/retained-population' / n for n in
             ('plugin.cpp', 'observer.h', 'patch.h', 'build.py', 'read_capture.py')]
    for va in (0x14079f860, 0x14079b520, 0x14079ddf0, 0x14079d910, 0x1409829b0, 0x140982b70):
        paths.append(next(p for p in (ROOT / f'.local-work/{task}/functions/{va:x}.txt'
                                     for task in ('d5w', 'd5v')) if p.is_file()))
    paths.append(ROOT / '.local-work/d5p-r3/investigation03/native.tsv')
    git = lambda *args: subprocess.check_output(['git', '--no-optional-locks', *args], cwd=ROOT).decode().strip()
    result = dict(schema='sor-d5x-identity/1', utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  installed=installed, database=database, sites=sites, cfg_ranges=ranges,sources={str(p): sha(p) for p in paths},
                  head=git('rev-parse', 'HEAD'), index_sha256=sha(ROOT / '.git/index'),
                  status=git('status', '--short'), free=build.guard(), python_sha256=sha(sys.executable),
                  brief_sha256=sha(ROOT / 'docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5X_construction_winner_observer_feasibility_qualification.md'))
    (out / 'identity.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(out=str(out), installed=installed, sites=sites), indent=2))


if __name__ == '__main__':
    main()
