# SPDX-License-Identifier: GPL-3.0-or-later
"""Original offline E1 receipt checker, not a production simulator.
Reads pinned local inventories/native exports/protected files and five archived
saves through the owned save-menu reader. Writes an exclusive ignored JSON
receipt. Requires repository cwd, CPython stdlib and existing task inventories.
No game/process/save/project/index/network effects. Arithmetic examples test
binary32 illustration only; textual instruction checks are not semantic proof.
"""
from pathlib import Path
import argparse
import hashlib
import json
import struct
import sys
import datetime

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT/'.local-work/e1-production'
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from save_menu import inspect
from inventory_historical_saves import guard

def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def f32(x):
    return struct.unpack('<f', struct.pack('<f', x))[0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    assert args.run.isalnum()
    guard()
    checks = []
    def check(ok, label):
        assert ok, label
        checks.append(label)
    protected = json.loads((BASE/'protected-before.json').read_text())
    for p in protected:
        check(sha(Path(p['path'])) == p['sha256'], 'protected '+p['path'])
    inventory = json.loads((BASE/'perks01.json').read_text())
    check(sha(Path(inventory['source']['path'])) == inventory['source']['sha256'], 'ESM pin')
    perks = inventory['records']
    entries = []
    d8 = []
    for r in perks:
        entry_type = None
        for tag, value in r['fields']:
            if tag == 'PRKE':
                entry_type = bytes.fromhex(value)[0]
            if tag == 'PRKF':
                entry_type = None
            if tag == 'DATA' and entry_type == 2 and len(value) == 6 and value.startswith('a103'):
                entries.append(r['formid'])
            if tag == 'DATA' and entry_type == 2 and len(value) == 6 and value.startswith('d8'):
                d8.append(r['formid'])
    check(len(perks) == 502, 'main ESM PERK census 502')
    check(len(entries) == 20 and len(set(entries)) == 9, '20 A1/op3 entries in nine definitions')
    check(not d8, 'no DATA D8 in inspected 502 PERK definitions')
    check(sum(r['edid'].startswith('MagPerk_') for r in perks) == 51, '51 MagPerk definitions')
    examples = [f32(f32(x)*f32(3600)) for x in (.01,.015,.02,.025,.03)]
    check(examples == [36.,54.,72.,90.,108.], 'nominal binary32 examples')
    # An explicit synthetic fold, with each native-style multiplication rounded.
    fold = f32(f32(f32(36)*f32(.95))*f32(.5))
    check(fold == 17.100000381469727, 'synthetic sequential timer fold')
    for file, needles in {
        'e1-production-04.tsv':['FUNCTION\t140c94430', 'VMULSS'],
        'e1-production-08.tsv':['FUNCTION\t140c94060', 'FUNCTION\t140f51350'],
        'e1-production-10.tsv':['FUNCTION\t140ca13b0','FUNCTION\t1409e8570','FUNCTION\t140b64fc0'],
        'e1-production-12.tsv':['FUNCTION\t140c954b0','LEA RDX,[RCX + 0x18]'],
        'e1-native-04.tsv':['FUNCTION\t140f7f1e0','VCVTTSS2SI'],
    }.items():
        s = (ROOT/'.local-work/recon'/file).read_text()
        for needle in needles:
            check(needle in s, file+' '+needle)
    manifest = json.loads((ROOT/'.local-work/manual-S0-S7C/manifest.json').read_text())
    saves = []
    for sample in manifest['samples']:
        if sample['label'] not in {'S0','S3','S3C','S4','S4C'}:
            continue
        source = sample['source_before']
        copy = Path(sample['copy']['path'])
        spec = dict(label=sample['label'], path=str(copy), sha256=source['sha256'], source=source)
        row = inspect(spec, datetime.timezone(datetime.timedelta(hours=11)), '+11:00')
        check(row['status'] != 'ERROR', 'header '+sample['label'])
        check(sha(copy) == source['sha256'], 'archive unchanged '+sample['label'])
        row['destination_present'] = Path(source['path']).exists()
        saves.append(row)
    check(len(saves) == 5, 'five candidate saves inspected')
    s4 = next(r for r in saves if r['research_id'] == 'S4')
    check('Save12_' in s4['read_path'] and not s4['destination_present'], 'S4 is absent Save12')
    check(s4['fields']['character']['value'] == 'Attila Kiraly', 'S4 character')
    check(s4['fields']['location']['value'] == 'Kreet - Outpost', 'S4 location')
    receipt = dict(checks=checks, count=len(checks), saves=saves,
                   examples=dict(nominal_seconds=examples, synthetic_fold=fold),
                   limits='Integrity and scoped fixtures; no actual runtime arithmetic or production measured')
    with (BASE/('verification-'+args.run+'.json')).open('x',encoding='utf8',newline='\n') as f:
        json.dump(receipt, f, indent=2)
        f.write('\n')
    guard()
    print('PASS',len(checks),'checks; five save headers; no runtime result')

if __name__ == '__main__':
    main()
