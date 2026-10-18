# SPDX-License-Identifier: GPL-3.0-or-later
"""Finite offline CR1 rework checks; run from repo with CPython -B.

Reads ignored primary receipts and hash-pinned originals, authored current.py,
native exports, HEAD/index. Writes one exclusive ignored JSON (--run). Uses
stdlib and owned save-analysis helpers only; no game/database/network/Git writes.
Real field joins and independent E2/type inputs are separate from adverse parser
tests; neither proves post-load authority, unassignment or effective contribution.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import struct

R = Path.cwd()
W = R / '.local-work/cr1-current'
sys.path[:0] = [str(R/'save-analysis/scripts'), str(Path(__file__).parent)]
from current import explicit_actor_links, registry_entries
from stream_save import decoded_save
from validate_mature_outposts import directory
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from workshop_population import typed_records


def pin(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


ap = argparse.ArgumentParser()
ap.add_argument('--run', required=True)
args = ap.parse_args()
assert re.fullmatch('[a-zA-Z0-9-]+', args.run)
for drive in ('C:/', 'D:/'):
    assert shutil.disk_usage(drive).free >= 40000000000
checks = []


def check(label, condition):
    assert condition, label
    checks.append(dict(check=label, result='PASS'))


for label in ('HIST-0021', 'HIST-0022', 'HIST-0024', 'HIST-0255'):
    revision = '06' if label=='HIST-0255' else '05'
    v = json.loads((W/(label+'-witness'+revision+'.json')).read_text(encoding='utf8'))
    check(label+' original hash', pin(Path(v['source']['path'])) == v['source']['sha256'])
    by = {x['identity']: x for x in v['rows']}
    for r in v['rows']:
        if 'actor_links' not in r:
            continue
        record = r['record']
        data = bytearray(record['end'])
        data[record['body']:record['end']] = bytes.fromhex(r['body_hex'])
        lookup = dict(zip(record['refs'], r['queue']))
        got = explicit_actor_links(data, record, lookup.__getitem__)
        check(label+' '+r['identity']+' actual wire reread', got == r['actor_links'])
        assignment = next((e for e in got['entries'] if e['keyword']=='starfield.esm:26beac'), None)
        e = assignment or got['entries'][0]
        if assignment:
            check(label+' '+r['identity']+' explicit handle mode', e['mode']==0)
        dest = by.get(e['target'], {})
        if assignment and dest.get('base') == 'starfield.esm:2c60e9':
            member = next(x for x in dest['extras']['extras'] if x['type']=='e2')
            check(label+' '+r['identity']+' independent destination membership',
                  r['identity'] in member['members'] and record['form_type']==0x4b
                  and dest['record']['form_type']==0x4a)
        def reject(name, b, rec):
            try:
                explicit_actor_links(b, rec, lookup.__getitem__)
            except (ValueError, KeyError):
                checks.append(dict(check=label+' '+r['identity']+' '+name, result='PASS'))
            else:
                raise AssertionError(name)
        reject('wrong version rejected', data, dict(record, buffer_version=152))
        reject('wrong type rejected', data, dict(record, form_type=0x4a))
        reject('truncated before target mode rejected', data,
               dict(record, end=e['mode_offset']))
        reject('short reference queue rejected', data, dict(record, refs=record['refs'][:3]))
        if got['trace'][0]['type']=='2b':
            altered = bytearray(data)
            altered[got['trace'][0]['npc_flags_offset']] = 1
            reject('nonzero nested NPC changes rejected', altered, record)
    boundary = json.loads((W/(label+'-registry-boundary01.json')).read_text(encoding='utf8'))
    with decoded_save(Path(v['source']['path']), W/'scratch-verify-current') as (data, decoded):
        d = directory(data)
        forms = struct.unpack_from('<'+'I'*d['reference_count'],data,d['regions']['reference_u32'][0]+4)
        plugins = plugin_tables(data)
        def resolve(n):
            return saved_form(token_value(f'{n:06x}',forms),plugins)
        start, end = boundary['registry_start'], boundary['registry_end']
        world = boundary['world_component_run']
        check(label+' independent world terminator adjacent to registry',
              bytes(data[world['terminator']:start])==bytes(4)
              and world['end']==start and world['terminator']-world['start']==37*len(world['worlds']))
        check(label+' all beacon parents independently in world run',
              set(boundary['independent_beacon_parent_tokens']) <= {x['world_token'] for x in world['worlds']})
        rows = registry_entries(data,start,end,resolve)
        check(label+' registry Player owner/index',len(rows)==1 and rows[0]['owner']=='starfield.esm:000014' and rows[0]['index']==0)
        check(label+' actual available array reread',rows[0]['available']==boundary['entries'][0]['available'])
        if label=='HIST-0255':
            check('HIST0255 positive roster count3',len(rows[0]['available'])==3)
            ids = {r['identity'] for r in rows[0]['available']}
            types = {saved_form(token_value(r['token'],forms),plugins):r['form_type'] for r in typed_records(data)}
            check('HIST0255 all three roster identities are actual ACHR',all(types[x]==0x4b for x in ids))
            check('HIST0255 Sarah explicit target in owned ship array',
                  next(e['target'] for e in by['starfield.esm:005986']['actor_links']['entries'] if e['keyword']=='starfield.esm:26beac')
                  in {r['identity'] for r in rows[0]['ships']})
        else:
            check(label+' explicit zero available count',rows[0]['available']==[])
        try:
            registry_entries(data,start,end-1,resolve)
        except ValueError:
            checks.append(dict(check=label+' truncated registry rejected',result='PASS'))
        else:
            raise AssertionError('truncated registry')
native = (W/'native/005.request.tsv').read_text(encoding='utf8')
part = native.split('case 0xe2:', 1)[1].split('case 0xe3:', 1)[0]
check('actual E2 writer prunes then writes count and saved identities',
      part.index('FUN_14040a0d0') < part.index('FUN_141868770') < part.index('FUN_140306db0'))
chain = (W/'native/004.request.tsv').read_text(encoding='utf8')
check('world serializer immediately before ship registry serializer',
      chain.index('FUN_140ad5f20((longlong)local_128)') < chain.index('FUN_14130fba0(local_128'))
base = json.loads((W/'baseline.json').read_text(encoding='utf8'))
check('HEAD unchanged', subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==base['head'])
check('index unchanged', pin(R/'.git/index')==base['index']['sha256'])
output = W/(args.run+'.json')
with output.open('x',encoding='utf8',newline='\n') as f:
    json.dump(dict(checks=checks, passed=len(checks),
                   limits='Offline bytes/native only; no complete or post-load unassignment/coherence oracle'),f,indent=2)
    f.write('\n')
print('PASS',len(checks))
