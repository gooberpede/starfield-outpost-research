# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify D5AE preservation, source identity and task-text inventory offline.

Reads start/input/source receipts, original/copy core files and task artifacts.
Writes an exclusive local receipt including exclusions and Git status. Stdlib
and Git reads only; no stage, ref, game, save, Ghidra or network mutation.
SOR-P-0002: D5AD selected-input preservation and project review-package methods.
Stop on drift, missing required artifact or caller-available disk-floor failure.
This is byte/inventory validation, not a semantic or independent review oracle.
"""
import csv
import json
from pathlib import Path
import subprocess
import sys

from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    out = Path(sys.argv[1]).resolve()
    if out.exists() or not out.is_relative_to(ROOT / '.local-work/d5ae'):
        raise ValueError('Fresh task-local receipt required')
    start = json.loads((ROOT / '.local-work/d5ae/baseline.json').read_bytes())
    git = lambda *a: subprocess.check_output(['git', *a], cwd=ROOT).decode()
    if git('rev-parse','HEAD').strip() != start['head'] or sha(ROOT/'.git/index') != start['index_sha256']:
        raise ValueError('HEAD/index drift')
    inputs = json.loads((ROOT / '.local-work/d5ae/inputs01.json').read_bytes())
    checked = {}
    for path, row in inputs['inputs'].items():
        actual = sha(path)
        if actual != row['sha256']:
            raise ValueError('Original input drift: ' + path)
        checked[path] = actual
    for p in sorted((ROOT / '.local-work/d5ae').glob('export*/command.json')):
        receipt = json.loads(p.read_bytes())
        if 'command' not in receipt:
            raise ValueError('Unknown exporter receipt')
        command = receipt['command']
        if any('ReverseEngineering' in c for c in command):
            raise ValueError('Original project launch in command')
        for path, expected in receipt['project_pins'].items():
            actual = checked[path] if path in checked else sha(path)
            if actual != expected:
                raise ValueError('Project core drift: '+path)
            checked[path] = expected
    with (ROOT/'docs/experiments/resource-retained-population/d5ae-sources.csv').open(encoding='utf8') as f:
        sources=list(csv.DictReader(f))
    for row in sources:
        p=Path(row['path'])
        if not p.is_absolute():
            p=ROOT/p
        if sha(p) != row['sha256']:
            raise ValueError('Source drift: '+str(p))
        checked[str(p)] = row['sha256']
    paths=set(git('diff','HEAD','--name-only').splitlines())
    paths.update(git('ls-files','--others','--exclude-standard').splitlines())
    authored=[]
    brief='docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AE_GC10_construction_winner_scheduling.md'
    for name in sorted(paths):
        p=ROOT/name
        data=p.read_bytes()
        text=data.decode('utf8')
        if name != brief and ('\r' in text or text.startswith('\ufeff')):
            raise ValueError('Authored encoding: '+name)
        authored.append(dict(path=name,sha256=sha(p),bytes=len(data),
                             kind='supplied brief' if name==brief else 'task authored'))
    excluded=[]
    for directory in (ROOT/'.local-work/d5ae',ROOT/'.local-work/d5ac/d5ae-reconstruction01',
                      ROOT/'.local-work/d5ad/d5ae-chronology01'):
        for p in sorted(directory.rglob('*')):
            if p.is_file():
                excluded.append(dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,
                                     sha256=sha(p),classification='LOCAL-ONLY; excluded from Git patches'))
    result=dict(head=start['head'],index_sha256=start['index_sha256'],
                free=guard(),checked=checked,authored=authored,exclusions=excluded,
                status=git('status','--short','--untracked-files=all'),
                scope='Selected input/core/source preservation and text inventory; not full active-save or semantic validation',
                no_staging_commit_push=True,script_sha256=sha(__file__))
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(checked=len(checked),authored=len(authored),excluded=len(excluded))))


if __name__ == '__main__':
    main()
