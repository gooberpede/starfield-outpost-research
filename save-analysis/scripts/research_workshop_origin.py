"""SPDX-License-Identifier: GPL-3.0-or-later
Offline SOR-EXP-0017 reader. Reads exact hash-pinned archived Save25/26 and
session manifest/raw captures, existing ESM catalog and Ghidra database files.
Writes only a fresh ignored run directory, temporary decoder scratch and JSON
receipts. Stdlib plus existing project readers; no engine/database/Git/network
effects. 40-billion-byte C:/D: floor enforced by the mapped decoder/guard.
Whole records and private paths remain local. No save bytes are modified.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

from inventory_historical_saves import identity, guard
from stream_save import decoded_save
from research_two_outpost_anchors import inspect
from validate_mature_outposts import directory
from outpost_record_framing import iter_records
from outpost_record_framing import Reader

ROOT = Path(__file__).resolve().parents[2]
LABELS = ['baseline-003', 'control-003', 'premove-003', 'moved-003',
          'saved-003', 'reloaded-003', 'reload-control-003', 'visit-002', 'control-002']


def write(p, obj):
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')


def hits(b, needle):
    found, p = [], 0
    while (p := b.find(needle, p)) >= 0:
        found.append(p)
        p += 1
    return found


def f32(values):
    return struct.pack('<3f', *values)


def workshop_prefix(b, record, prefix):
    """Modern 1.16.244 sample branch only; stop on unsupported leading extra.

    Source-informed by 140521620/140a23de0/140562ef0/140f50880. Reads the
    reference and string queues separately from the body. Supports zero resource
    entries only; no guessing/skipping their variable grammar. Does not decode
    extras following Workshop or assert closure of the entire REFR body.
    """
    if record['flags'] & (0x80 | 0x10):
        raise ValueError('unsupported pre-extra fields')
    c=Reader(b,prefix['form_prefix_end'],record['end'])
    ri=prefix['next_reference_index']
    def refs(n):
        nonlocal ri
        if not 0<=n<=len(record['refs'])-ri: raise ValueError('reference queue bounds')
        values=record['refs'][ri:ri+n]; ri+=n
        return values
    count=c.count(); leading=[]
    for _ in range(count):
        start=c.p; typ=c.take(1)[0]; leading.append(typ)
        if typ==0x9c: c.take(4) # modern ExtraFlags branch
        elif typ==0xda:
            # two PackIn refs, LevPackIn ref, handle ref, modern ref; +68 byte/+64 uint32
            refs(5); c.take(5)
        elif typ==0x4c:
            n=c.count()
            for _ in range(n): refs(2); c.take(1)
        elif typ==0x84:
            n=c.count()
            for _ in range(n): refs(1); c.take(1)
        elif typ==0xbc:
            resources=int.from_bytes(c.take(4),'little')
            if resources: raise ValueError('nonempty Workshop resources unsupported')
            handles=refs(c.count())
            flag=c.take(1).hex()
            if not record['strings']: raise ValueError('workshop string queue empty')
            value78=c.take(4).hex()
            offset=c.p; delta=c.take(12).hex(); identifier=c.take(8).hex()
            return dict(extra_start=start,leading_types=leading,declared_extras=count,
                resource_count=resources,handles=handles,flag94_hex=flag,
                name_string_index=record['strings'][0],field78_hex=value78,
                delta_offset=offset,delta_record_offset=offset-record['offset'],
                delta_body_offset=offset-record['body'],delta_hex=delta,
                identifier98_hex=identifier,end=c.p,next_reference_index=ri,
                coverage='modern zero-resource Workshop prefix; following extras not decoded')
        else: raise ValueError(f'unsupported leading extra {typ:02x}')
    raise ValueError('no Workshop extra')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    if not args.run.replace('-', '').isalnum():
        raise ValueError('run name')
    out = ROOT/'.local-work/workshop-origin'/args.run
    out.mkdir(parents=True, exist_ok=False)
    guard(out)
    prior = ROOT/'.local-work/beacon-observer-live-review/initial-01'
    manifest = json.loads((prior/'final-summary.json').read_text())
    save26 = Path(manifest['save']['archive'])
    save25row = next(r for r in manifest['preservation']
                     if 'savegames' in r['path'] and Path(r['path']).name.startswith('Save25_'))
    saves = [('Save25', Path(save25row['path']), save25row['sha256']),
             ('Save26', save26, manifest['save']['sha256'])]
    session = ROOT/'.local-work/beacon-observer-live/session-17596-91165828'
    catalog_path = ROOT/'.local-work/save-capacity-location/esm-index-verified.json'
    catalog = json.loads(catalog_path.read_text())
    protected = [p for _, p, _ in saves] + [catalog_path, Path(catalog['source']['path']),
        Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')]
    db = Path('D:/ReverseEngineering/Starfield/GhidraProject')
    protected += sorted(p for p in db.rglob('*') if p.is_file() and '.lock' not in p.name)
    before = {str(p): identity(p) for p in protected}
    write(out/'before.json', before)
    for _, p, expected in saves:
        if before[str(p)]['sha256'] != expected:
            raise ValueError('source hash mismatch')
    if before[str(Path(catalog['source']['path']))]['sha256'] != catalog['source']['sha256']:
        raise ValueError('ESM hash mismatch')
    # Verify the original session-file manifest, not a previous decoded summary.
    oldfiles = json.loads((prior/'session-file-manifest.json').read_text())
    for row in oldfiles:
        p = session/row['path']
        if p.stat().st_size != row['bytes'] or identity(p)['sha256'] != row['sha256']:
            raise ValueError('capture manifest mismatch: '+row['path'])
    captures = []
    original = {}
    for label in LABELS:
        folder = session/label
        rows = [json.loads(s) for s in (folder/'records.jsonl').read_text().splitlines()]
        raw = {r['root']: r for r in rows if r['kind']=='raw' and not r['root'].endswith('.node')}
        for ref in (r for r in rows if r['kind']=='reference' and r['formid'] in ('0xff01ab8f','0xff01ab50')):
            root, fid = ref['root'], ref['formid']
            rr, wr = raw[root], raw[root+'.extra.workshop']
            rb, wb = (folder/rr['file']).read_bytes(), (folder/wr['file']).read_bytes()
            xyz, delta = rb[0x8c:0x98], wb[0x60:0x6c]
            assert wb[0x12]==0xbc
            assert struct.unpack_from('<Q',wb)[0]-int(rows[0]['module_base'],16)==0x4c24e60
            if label == LABELS[0]: original[fid] = xyz
            ov, cv, dv = [struct.unpack('<3f', v) for v in (original[fid],xyz,delta)]
            assert delta == f32([a-b for a,b in zip(ov,cv)])
            assert original[fid] == f32([a+b for a,b in zip(cv,dv)])
            captures.append(dict(label=label, formid=fid, reference=rr, workshop=wr,
                xyz_hex=xyz.hex(), delta_hex=delta.hex(), xyz=cv, delta=dv,
                workshop_vtable_rva=hex(struct.unpack_from('<Q',wb)[0]-int(rows[0]['module_base'],16)),
                workshop_type=wb[0x12], recovered_origin_hex=original[fid].hex()))
            captures[-1].update(field78_hex=wb[0x78:0x7c].hex(),
                flag94_hex=wb[0x94:0x95].hex(),identifier98_hex=wb[0x98:0xa0].hex())
    write(out/'captures.json', captures)
    needle = bytes.fromhex(next(r['delta_hex'] for r in captures if r['label']=='moved-003' and r['formid']=='0xff01ab8f'))
    results = []
    for label,p,_ in saves:
        with decoded_save(p,out/'scratch') as (b,m):
            extracted = inspect(b,catalog['records'])
            for beacon in extracted['beacons']:
                try: beacon['workshop_prefix']=workshop_prefix(b,beacon['record'],beacon['prefix'])
                except ValueError as e: beacon['workshop_prefix']=dict(unsupported=str(e))
            d = directory(b)
            literal = hits(b,needle)
            selected = []
            for r in iter_records(b,*d['regions']['region_R3'],d['words'][9]):
                if any(r['offset']<=q<r['end'] for q in literal) or r['token'] in {v['token'] for v in extracted['beacons']}:
                    selected.append(dict(record=r, body_hex=bytes(b[r['body']:r['end']]).hex(),
                                         literal_record_offsets=[q-r['offset'] for q in literal if r['offset']<=q<r['end']]))
            results.append(dict(label=label,metrics=m,extraction=extracted,
                                literal_delta_offsets=literal,selected_records=selected))
    write(out/'saves.json', results)
    transition=[]
    for a in results[0]['extraction']['beacons']:
        wa=a['workshop_prefix']
        if 'unsupported' in wa: continue
        matches=[v for v in results[1]['extraction']['beacons']
                 if v['workshop_prefix'].get('identifier98_hex')==wa['identifier98_hex']]
        if len(matches)!=1: raise ValueError('workshop identifier correspondence ambiguous')
        z=matches[0]; wz=z['workshop_prefix']
        for label,wp in [('baseline-003',wa),('saved-003',wz),('reloaded-003',wz)]:
            live=[v for v in captures if v['label']==label and v['identifier98_hex']==wp['identifier98_hex']]
            if len(live)!=1: raise ValueError('runtime workshop identifier correspondence ambiguous')
            for key in ('delta_hex','field78_hex','flag94_hex','identifier98_hex'):
                assert live[0][key]==wp[key], key
            assert live[0]['xyz_hex']==(a if label=='baseline-003' else z)['xyz_hex']
        av=struct.unpack('<3f',bytes.fromhex(a['xyz_hex']))
        zv=struct.unpack('<3f',bytes.fromhex(z['xyz_hex']))
        delta=struct.unpack('<3f',bytes.fromhex(wz['delta_hex']))
        assert f32([x+y for x,y in zip(zv,delta)])==bytes.fromhex(a['xyz_hex'])
        transition.append(dict(name=a['name_for_comparison'][0]['text'],
            before_token=a['token'],after_token=z['token'],before_parent=a['parent_token'],after_parent=z['parent_token'],
            before_xyz_hex=a['xyz_hex'],after_xyz_hex=z['xyz_hex'],
            before_workshop=wa,after_workshop=wz,
            direct_pairs_unchanged=[v['pair_hex'] for v in a['points']]==[v['pair_hex'] for v in z['points']],
            direct_body_ids_unchanged=[v['body_formid'] for v in a['points']]==[v['body_formid'] for v in z['points']],
            runtime_field_matches=True,recovered_origin_bits=True))
    write(out/'transition.json',transition)
    after = {str(p):identity(p) for p in protected}
    if before != after: raise ValueError('protected input changed')
    write(out/'preservation.json',dict(before=before,after=after,session_files_verified=len(oldfiles)))
    write(out/'tools.json',dict(python=sys.version,argv=sys.argv,
        scripts=[identity(p) for p in Path(__file__).parent.glob('*.py')]))
    print(json.dumps(dict(captures=len(captures),session_files_verified=len(oldfiles),
        saves=[dict(label=r['label'],decoded=r['metrics'],literal=r['literal_delta_offsets'],
            beacons=[dict(token=v['token'],parent=v['parent_token'],xyz=v['local_xyz']) for v in r['extraction']['beacons']]) for r in results])))


if __name__ == '__main__': main()
