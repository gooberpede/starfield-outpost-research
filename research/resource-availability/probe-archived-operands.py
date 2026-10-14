"""SPDX-License-Identifier: GPL-3.0-or-later
Original observation-only archived-capture probe. Reads exact initial-session
manifest/records and selected raw files; validates original hashes before/after.
Writes exclusive local scalar/header coverage receipt; no target or save writes.
Runtime snapshots are non-atomic and not UI/generation invocation observations.
"""
from pathlib import Path
import argparse
import json
import sys
import struct

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inventory_historical_saves import identity, guard
from research_workshop_origin import LABELS

ap = argparse.ArgumentParser()
ap.add_argument('--run', required=True)
a = ap.parse_args()
if not a.run.replace('-', '').isalnum(): raise ValueError('RUN_NAME')
guard()
session = ROOT/'.local-work/beacon-observer-live/session-17596-91165828'
manifest = ROOT/'.local-work/beacon-observer-live-review/initial-01/session-file-manifest.json'
frozen = {v['path'].replace('\\','/'):v for v in json.loads(manifest.read_text(encoding='utf8'))}
pins, rows = {str(manifest):identity(manifest)}, []
for label in LABELS:
    record_path = session/label/'records.jsonl'
    selected = [record_path]
    records = [json.loads(v) for v in record_path.read_text(encoding='utf8').splitlines()]
    module = int(records[0]['module_base'],16)
    raw = {r['root']:r for r in records if r['kind']=='raw'}
    values = []
    for name in ('terrain','terrain.workshop_output.before','terrain.workshop_output.after'):
        r = raw.get(name)
        if r is None:
            values.append(dict(root=name,status='NOT_CAPTURED')); continue
        path = session/label/r['file']; selected.append(path)
        b = path.read_bytes()
        if len(b)<0xa0: raise ValueError('CAPTURE_SIZE')
        row = dict(root=name, path=str(path), bytes=len(b),
                   vtable_rva=hex(struct.unpack_from('<Q',b)[0]-module),
                   snapshot_atomic=False)
        if name=='terrain':
            row['manager80_u32']=struct.unpack_from('<I',b,0x80)[0]
            row['procgen_pointer']=hex(struct.unpack_from('<Q',b,0x130)[0])
        else:
            row['hash_header20_hex']=b[0x20:0x48].hex()
            row['pointed_hash_members_captured']=False
        values.append(row)
    for path in selected:
        actual = identity(path); expected = frozen[path.relative_to(session).as_posix()]
        if actual['sha256'] != expected['sha256'] or actual['size'] != expected['bytes']:
            raise ValueError('ARCHIVED_CAPTURE_PIN')
        pins[str(path)] = actual
    rows.append(dict(label=label, roots=values,
                     coverage='manager scalars and ProcGen header only; no generation-call/cell-key/resource-geometry/UI epoch join'))
if {p:identity(Path(p)) for p in pins} != pins: raise ValueError('INPUT_CHANGED')
out = ROOT/'.local-work/resource-availability'/(a.run+'.json')
with out.open('x',encoding='utf8',newline='\n') as f:
    json.dump(dict(rows=rows, inputs=pins, script=identity(Path(__file__))),f,indent=2);f.write('\n')
guard()
print('checkpoints',len(rows),'pinned files',len(pins))
