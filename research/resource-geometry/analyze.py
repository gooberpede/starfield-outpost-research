# SPDX-License-Identifier: GPL-3.0-or-later
"""RG1 offline actual-definition/synthetic-context qualification.

Run at repository root with --output an unused ignored JSON path. Reads installed
Starfield.exe/Starfield.esm and selected owned method/receipt sources, hashes
originals before/after, writes only exclusive JSON. No live/game/save/DB mutation,
installs, networking or external implementation. Requires existing CPython stdlib
and project-owned inspect_outpost_definitions.py. Mathematical queries are NOT
measured native points. A definition block is NOT a qualified site context.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import struct
import sys
from geometry import unopposed_cell, sincos, nominal_strips

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / 'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records


def pin(p):
    p = Path(p)
    with p.open('rb') as f:
        return dict(path=str(p), bytes=p.stat().st_size,
                    sha256=hashlib.file_digest(f, 'sha256').hexdigest())


def analyze():
    ap = argparse.ArgumentParser(); ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert not args.output.exists()
    free = {d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}
    assert min(free.values()) >= 40_000_000_000
    game = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
    exe, esm = game/'Starfield.exe', game/'Data/Starfield.esm'
    before = [pin(exe), pin(esm)]
    assert before[0]['sha256'] == '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
    old = R/'.local-work/resource-milestone-b-spatial-constants.json'
    constants = json.loads(old.read_text())['constants']
    blob = exe.read_bytes()
    for c in constants:
        assert blob[c['file_offset']:c['file_offset']+4].hex() == c['bytes']
    c = {int(x['va'],16):x['float'] for x in constants}
    # Same PE section translation as owned constant study; retain exact offsets.
    pe = struct.unpack_from('<I',blob,0x3c)[0]
    n, opt = struct.unpack_from('<H',blob,pe+6)[0], struct.unpack_from('<H',blob,pe+20)[0]
    sections = [struct.unpack_from('<IIII',blob,pe+24+opt+i*40+8) for i in range(n)]
    scalars = []
    for va in (0x144f03f50,0x144f06670,0x144f04cb8):
        rva = va-0x140000000
        section = next(s for s in sections if s[1] <= rva < s[1]+s[2])
        offset = section[3]+rva-section[1]; raw = blob[offset:offset+4]
        scalars.append(dict(static_va=hex(va),file_offset=offset,hex=raw.hex()))
        if va != 0x144f06670: c[va] = struct.unpack('<f',raw)[0]
    assert scalars[1]['hex'] == '00000080'  # XOR sign mask at heading call.
    records = list(esm_records(esm,{b'RSGD',b'IRES'},repeated=True))
    rarity = {}
    for rec, fields in records:
        if rec['type'] == 'IRES':
            fields = dict(fields)
            if b'SNAM' in fields: rarity[rec['formid']] = int.from_bytes(fields[b'SNAM'],'little') & 255
    rows = []
    for rec, fields in records:
        if rec['type'] != 'RSGD': continue
        resource = None
        for tag, data in fields:
            if tag == b'RNAM': resource = int.from_bytes(data,'little')
            if tag != b'DNAM' or resource not in rarity: continue
            assert len(data) == 560
            r = rarity[resource]; off = 40*(r+7)
            if off+40 > len(data): continue
            block = struct.unpack_from('<10f',data,off)
            req = dict(packed_key=7,owner_key=259487,cell=[0,0],origin=[0,0],
                       clip_center=[50,50,0],clip_half=[100000,100000,0],
                       block=list(block),weight=1,source='SYNTHETIC/unopposed-source',
                       resource=f'Starfield.esm:{resource:08x}',
                       provenance='actual installed DNAM; synthetic key/frame/weight/selection',
                       context_qualified=True,prior_different_resources=[])
            generated = unopposed_cell(req,c)
            rows.append(dict(rsgd=f'{rec["formid"]:08x}',record_file_offset=rec['offset'],
                             resource=req['resource'],rarity=r,block_offset=off,
                             dnam_sha256=hashlib.sha256(data).hexdigest(),request=req,result=generated))
    generated = [r for r in rows if r['result'].get('points') and len(r['result']['points'])>1]
    checks = []
    for row in generated:
        pts = row['result']['points']; q = [(pts[0][i]+pts[1][i])/2 for i in (0,1)]
        positive = nominal_strips(pts,q,150)
        # Conservative far negative based on all vertices, not a presumed bound.
        vertices = [v for strip in positive.get('strips',[]) for v in strip['vertices']]
        if not vertices: continue
        far = [max(v[i] for v in vertices)+1000 for i in (0,1)]
        negative = nominal_strips(pts,far,150)
        checks.append(dict(rsgd=row['rsgd'],resource=row['resource'],
                           basis='actual-definition / synthetic-context mathematical control',
                           positive=positive['intersection'],negative=negative['intersection']))
    assert generated and checks
    assert all(x['positive']=='POSITIVE_AREA' and x['negative']=='DISJOINT_OR_ZERO_AREA' for x in checks)
    assert [pin(exe),pin(esm)] == before
    result = dict(inputs=before,constant_source=pin(old),scalars=scalars,
                  constants={hex(k):v for k,v in c.items()},
                  rows=rows,spatial_checks=checks,free_before=free,
                  counts=dict(blocks=len(rows),multi_point_contexts=len(generated),checks=len(checks),
                              unknown=sum(r['result']['status']=='UNKNOWN' for r in rows)),
                  native_spatial_oracle='UNAVAILABLE',actual_site_generation='NOT_TESTED',
                  fixed_rotation=sincos(c[0x144f052b0],c),script=pin(__file__))
    with args.output.open('x',encoding='utf8',newline='\n') as f: json.dump(result,f,indent=2); f.write('\n')
    print(result['counts'])


if __name__ == '__main__': analyze()
