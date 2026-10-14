"""SPDX-License-Identifier: GPL-3.0-or-later
Original offline Phase1 capture extent check. Reads 16 existing 0.1.1 journals and
selected manager/ProcGen raw files, checks original journal-record raw SHA hashes,
pins all used files before/after, exclusively writes local numeric coverage.
No process/live/target/database/save/config/Git/network effects. 40GB guard.
No earlier independent journal-file hash is invented: current journal pins and
prior postflight provenance are recorded separately from raw hash checks.
"""
from pathlib import Path
import argparse
import json
import sys
import struct

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'save-analysis/scripts'))
from inventory_historical_saves import identity, guard

ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);a=ap.parse_args()
if not a.run.replace('-','').isalnum():raise ValueError('RUN_NAME')
guard()
session=ROOT/'.local-work/beacon-observer-live/session-9236-127079640'
prior=ROOT/'.local-work/engine-oracle-live/phase1-01/postflight.json'
pins={str(prior):identity(prior)}
post=json.loads(prior.read_text(encoding='utf8'))
rows=[]
def covered(start,end,ranges):
    cursor=start
    for lo,hi in sorted(ranges):
        if lo>cursor:break
        if hi>cursor:cursor=hi
        if cursor>=end:return True
    return False
for capture in post['captures']:
    label=capture['label'];journal=session/label/'records.jsonl'
    pins[str(journal)]=identity(journal)
    records=[json.loads(v) for v in journal.read_text(encoding='utf8').splitlines()]
    begin=records[0]
    if begin['version']!='0.1.1' or begin['game_sha256']!='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28':raise ValueError('CAPTURE_BASELINE')
    module=int(begin['module_base'],16)
    raw_rows=[r for r in records if r['kind']=='raw']
    raw={r['root']:r for r in raw_rows}
    ranges=[(int(r['address'],16),int(r['address'],16)+r['bytes']) for r in raw_rows]
    values=[]
    for name in ('terrain','terrain.workshop_output.before','terrain.workshop_output.after'):
        r=raw.get(name)
        if r is None:
            values.append(dict(root=name,status='NOT_CAPTURED'));continue
        p=session/label/r['file'];pins[str(p)]=identity(p)
        if pins[str(p)]['sha256']!=r['sha256'] or pins[str(p)]['size']!=r['bytes']:raise ValueError('RAW_RECORD_PIN')
        b=p.read_bytes();v=dict(root=name,path=str(p),bytes=len(b),vtable_rva=hex(struct.unpack_from('<Q',b)[0]-module),snapshot_atomic=False)
        if name=='terrain':v['manager80_u32']=struct.unpack_from('<I',b,0x80)[0]
        else:
            pointer,count=struct.unpack_from('<QQ',b,0x20)
            end=pointer+24*count
            v.update(hash_slots_pointer=hex(pointer),hash_declared_slots=count,
                     hash_slots_fully_covered=bool(pointer and count and covered(pointer,end,ranges)))
        values.append(v)
    rows.append(dict(label=label,roots=values,ui_epoch_observed=False,
                     generation_cell_key_observed=False,query_vector_membership_observed=False))
if {p:identity(Path(p)) for p in pins}!=pins:raise ValueError('INPUT_CHANGED')
out=ROOT/'.local-work/resource-availability'/(a.run+'.json')
with out.open('x',encoding='utf8',newline='\n') as f:
    json.dump(dict(rows=rows,inputs=pins,journal_provenance='current hashes plus prior postflight; no prior independent journal hash claimed',script=identity(Path(__file__))),f,indent=2);f.write('\n')
guard();print('checkpoints',len(rows),'used file pins',len(pins),'covered hash slot arrays',sum(v.get('hash_slots_fully_covered',False) for r in rows for v in r['roots']))
