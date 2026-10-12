# SPDX-License-Identifier: GPL-3.0-or-later
"""Original offline conditional geometry probe. Reads retained authored ledger,
writes a new JSON derivative only; stdlib/existing authored diagnostic dependencies.
No target/database/save/network/Git effects. Angular output is MODEL-PREDICTED,
not a native execution observation; all unrecorded landscape/handle gates remain open.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

from position_quantizer_diagnostic import diagnose_mode


def snap(tag, cx, cy, sx, sy, resolution=256):
    """96EFB0 geometry after96ECB0; fine values are set zero."""
    crossed_x = False
    if sx >= 12:
        if cx >= resolution-1:
            tag = int(tag == 0)
            cx -= resolution
            crossed_x = True
        cx += 1
        sx = 0
    else:
        sx = 8 if sx >= 4 else 0
    if sy >= 12:
        if not crossed_x:
            if cy >= resolution-1:
                tag = int(tag == 0)
                cx = resolution-cx-1
            else:
                cy += 1
        sy = 0
    else:
        sy = 8 if sy >= 4 else 0
    return [tag,cx,cy,sx,sy,0,0]


def unpack(key, block=12, resolution=256):
    if block != 12 or resolution != 256 or not 0 <= key < 2**64:
        raise ValueError('UNQUALIFIED_GEOMETRY_PARAMETERS')
    x,y,tag = key&65535,(key>>16)&65535,(key>>32)&7
    system,body = (key>>41)&0x3ffff,(key>>35)&63
    if tag not in (0,1,2,3) or max(x,y) >= 16*block*resolution:
        raise ValueError('UNQUALIFIED_PACKED_GEOMETRY_DOMAIN')
    if tag in (2,3):
        n=16*block*resolution
        x,y=n-x-1,n-y-1
    cx,rx=divmod(x,16*block)
    cy,ry=divmod(y,16*block)
    sx,fx=divmod(rx,block)
    sy,fy=divmod(ry,block)
    return dict(system_id=system,body_index=body,geometry=[tag,cx,cy,sx,sy,fx,fy])


def probe(rows):
    result=[]
    for row in rows:
        begin=row['snapshots']['begin']
        lon,lat=struct.unpack_from('<2d',bytes.fromhex(begin['candidate']['hex']))
        key=struct.unpack_from('<Q',bytes.fromhex(begin['world']['hex']),0x310)[0]
        source=unpack(key)
        modes={}
        for mode in ('avx','fma'):
            d=diagnose_mode(lon,lat,mode)
            ax,ay=d['hierarchy']
            candidate=snap(d['cell'][0],ax['coarse'],ay['coarse'],ax['sub'],ay['sub'])
            modes[mode]=dict(candidate_geometry=candidate,
                source_geometry=source['geometry'],
                compared_geometric_fields_equal=candidate==source['geometry'],
                first_geometric_mismatch=next((i for i,(a,b) in enumerate(zip(candidate,source['geometry'])) if a!=b),None),
                unsnapped_candidate=d['cell'])
        result.append(dict(invocation=row['invocation'],packed_source_hex=f'{key:016x}',
            source=source,modes=modes))
    return dict(classification='CONDITIONAL MODEL-PREDICTED DIAGNOSTIC',
        assumptions=['landscape+50 resolution256','global block+merge sum12',
            'packed source system/body matches landscape+54',
            'native scalar cos agrees with Python surrogate','AVX/FMA native trig modeled small-input paths',
            'round-nearest environment; source table/pattern handles deliberately excluded'],
        cannot_establish=['resolver/overlay/landscape presence','actual native hierarchy result',
            'source component match','Q branch execution','handle fields equality','oracle equivalence'],
        invocations=result)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('ledger',type=Path)
    p.add_argument('output',type=Path)
    a=p.parse_args()
    raw=a.ledger.read_bytes()
    out=probe(json.loads(raw))
    out['input_sha256']=hashlib.sha256(raw).hexdigest()
    with a.output.open('x',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(invocations=len(out['invocations']),
        geometry_equal_by_mode={m:sum(x['modes'][m]['compared_geometric_fields_equal'] for x in out['invocations']) for m in ('avx','fma')})))


if __name__=='__main__':
    main()
