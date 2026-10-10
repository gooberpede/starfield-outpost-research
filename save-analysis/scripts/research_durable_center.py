"""SPDX-License-Identifier: GPL-3.0-or-later
SOR-EXP-0018 offline research probe, stdlib and existing project readers only.
Reads hash-pinned archived Save25/26 and manual corpus, verified ESM catalog,
existing captures/receipts. Writes new ignored run JSON; decoder scratch is
temporary. No engine, database, network or Git writes. 40 GB guard enforced.
Conditional REFR cases are explicitly labelled; no universal identity schema.
"""
import argparse
import json
import math
from pathlib import Path
import struct

from inventory_historical_saves import identity, guard, metadata
from stream_save import decoded_save
from outpost_record_framing import iter_records
from outpost_membership import initial_prefix
from research_two_outpost_anchors import inspect
from research_workshop_origin import workshop_prefix, write
from validate_mature_outposts import directory
from beacon_terrain_projection import f32, to_square, from_square, split_local

ROOT = Path(__file__).resolve().parents[2]


def resource_rows(c, refs, count):
    """Modern resource-prefix grammar, static 140f50880/140f515a0/1402cef80.
    Outer resource ref + uint32 row count; each row pops two refs, takes 17
    body bytes. Values deliberately unclassified. Bounds checked before loops.
    """
    if count > (c.end-c.p)//4: raise ValueError('RESOURCE_GROUP_BOUNDS')
    groups=[]
    for _ in range(count):
        resource=refs(1)[0]
        n=int.from_bytes(c.take(4),'little')
        if n>(c.end-c.p)//17: raise ValueError('RESOURCE_ROW_BOUNDS')
        rows=[]
        for _ in range(n):
            start=c.p
            tokens=refs(2)
            c.take(17)
            rows.append(dict(offset=start,references=tokens))
        groups.append(dict(resource=resource,rows=rows))
    return groups


def initial_transform(b, r):
    """Read only present rotation floats after the bounded native initial prefix.
    Omitted axes are UNKNOWN here; caller separately proves the load default.
    """
    case = 5 if not r['flags'] & 0x8000 else 6 if r['flags'] & 0x02000008 else 4 if r['flags'] & 6 else 7
    p = initial_prefix(b, r, case)
    rot = []
    q = r['body'] + 13
    if case != 7:
        for axis in range(3):
            if p['shape'] & (1 << axis):
                rot.append(dict(axis=axis, offset=q, hex=bytes(b[q:q+4]).hex(),
                                value=struct.unpack_from('<f', b, q)[0]))
                q += 4
    frame_flag = None
    if case != 7:
        frame_flag = (0x20 if p['shape']&8 else 0 if p['shape']&0x10 else b[q])
    return dict(prefix=p, rotations=rot, record=r, initial_frame_flag=frame_flag,
                xyz_hex=bytes(b[r['body']+1:r['body']+13]).hex() if case != 7 else None)


def compensated(xyz, delta):
    if len(xyz) != 3 or len(delta) != 3 or not all(math.isfinite(v) for v in (*xyz, *delta)):
        raise ValueError('INVALID_VECTOR')
    return [f32(f32(a)+f32(d)) for a, d in zip(xyz, delta)]


def model_candidates(pair, xyz):
    """Two deliberately competing continuous extensions; neither is qualified.
    Establishes identifiability limits, never a production geographical API.
    """
    tag, u, v = to_square(*pair)
    indices = [round((t+.5)*49152-.5) for t in (u, v)]
    q, residual = zip(*(split_local(t) for t in xyz[:2]))
    origin = [i-t for i, t in zip(indices, q)]
    # Two phases of a continuous extension of the same discrete chart.
    # Existing observations exercise the discrete projection only, so they
    # cannot select either extension as an authoritative continuous consumer.
    a = from_square(tag, (origin[0]+xyz[0]/100+.5)/49152-.5,
                    (origin[1]+xyz[1]/100+.5)/49152-.5)
    b = from_square(tag, (origin[0]+xyz[0]/100)/49152-.5,
                    (origin[1]+xyz[1]/100)/49152-.5)
    return dict(tag=tag, indices=indices, local_floor=q, residual=residual,
                candidate_origin=origin, centre_phase=a, corner_phase=b,
                phase_difference=[x-y for x, y in zip(a, b)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    if not args.run.replace('-', '').isalnum(): raise ValueError('RUN_NAME')
    out = ROOT/'.local-work/durable-center'/args.run
    out.mkdir(parents=True, exist_ok=False)
    guard(out)
    catpath = ROOT/'.local-work/save-capacity-location/esm-index-verified.json'
    cat = json.loads(catpath.read_text())
    old = json.loads((ROOT/'.local-work/workshop-origin/final-03/before.json').read_text())
    manual = json.loads((ROOT/'.local-work/manual-S0-S7C/manifest.json').read_text())
    candidates = json.loads((ROOT/'.local-work/manual-S0-S7C/analysis-01/candidates.json').read_text())
    cases = [(label, Path(p), v['sha256']) for label in ('Save25','Save26')
             for p,v in old.items() if Path(p).name.startswith(label+'_')]
    if len(cases) != 2: raise ValueError('PRIMARY_INPUTS')
    cases += [(r['label'], Path(r['copy']['path']), r['copy']['sha256']) for r in manual['samples']]
    frozen = json.loads((ROOT/'.local-work/save-capacity-location/body-final-03/save-derived.json').read_text())
    cases += [(r['label'], Path(r['source']['copy']['path']), r['source']['copy']['sha256'])
              for r in frozen if r['label'] in ('Save3','L2C','HIST-0245','HIST-0267')]
    protected = [catpath, Path(cat['source']['path'])]+[p for _, p, _ in cases]
    before = {str(p):identity(p) for p in protected}
    write(out/'before.json', before)
    if before[str(Path(cat['source']['path']))]['sha256'] != cat['source']['sha256']: raise ValueError('ESM_HASH')
    results = []
    for label, path, expected in cases:
        if before[str(path)]['sha256'] != expected: raise ValueError('SAVE_HASH')
        with decoded_save(path, out/'scratch') as (b, metrics):
            d = directory(b)
            is_manual = label in {r['label'] for r in manual['samples']}
            wanted = set(candidates['tokens'].values()) if is_manual else set()
            ex = inspect(b, cat['records'])
            if ex:
                wanted.update(r['token'] for r in ex['beacons'])
            rows=[]
            for r in iter_records(b, *d['regions']['region_R3'], d['words'][9]):
                known_base = len(r['refs'])>2 and r['refs'][1] in ('63aed9','45ef19','6031e1') and r['refs'][2]==r['token'] and not r['flags']&0x8000
                if r['token'] not in wanted and not (not is_manual and known_base): continue
                t = initial_transform(b, r)
                t['role'] = next((k for k,v in candidates['tokens'].items() if v==r['token']),
                    {'63aed9':'storage','45ef19':'extractor','6031e1':'solar'}.get(t['prefix']['base_token'],'beacon'))
                try: t['workshop']=workshop_prefix(b,r,t['prefix'],resource_rows)
                except ValueError as e: t['workshop']=dict(unsupported=str(e))
                rows.append(t)
            if is_manual:
                prior = next(r for r in candidates['samples'] if r['label']==label)
                if metrics['decoded_sha256'] != prior['decoded_sha256']: raise ValueError('DECODE_HASH')
                # Original lifecycle candidates must now be framed starts.
                for t in rows:
                    offsets = prior['candidates'][t['role']]['main_offsets']
                    if offsets != [t['record']['offset']]: raise ValueError('FRAMING_CORRESPONDENCE')
            if ex:
                for t in rows:
                    matches=[v for v in ex['beacons'] if v['token']==t['record']['token']]
                    if not matches: continue
                    beacon=matches[0]
                    t['association']=beacon
                    if 'delta_hex' in t['workshop']:
                        delta=struct.unpack('<3f',bytes.fromhex(t['workshop']['delta_hex']))
                        t['delta']=delta
                        t['center']=compensated(t['prefix']['xyz'],delta)
                        t['center_hex']=struct.pack('<3f',*t['center']).hex()
                        t['models']=[model_candidates((pt['longitude_rad'],pt['latitude_rad']),t['center']) for pt in beacon['points']]
            results.append(dict(label=label,metrics=metrics,metadata=metadata(b),rows=rows,
                                extraction=ex))
        guard(out)
        print(label, [(r['role'],r['prefix'].get('case'),r['prefix'].get('xyz')) for r in rows],flush=True)
    write(out/'results.json',results)
    transitions=[]
    for first in results[0]['rows']:
        key=first['workshop'].get('identifier98_hex')
        if key is None: raise ValueError('PRIMARY_WORKSHOP_UNSUPPORTED')
        matches=[r for r in results[1]['rows'] if r['workshop'].get('identifier98_hex')==key]
        if len(matches)!=1: raise ValueError('PRIMARY_ID_AMBIGUOUS')
        last=matches[0]
        if first['center_hex']!=last['center_hex']: raise ValueError('CENTER_INVARIANCE')
        if [p['pair_hex'] for p in first['association']['points']] != [p['pair_hex'] for p in last['association']['points']]:
            raise ValueError('SITE_CHANGED')
        transitions.append(dict(workshop_identifier_hex=key,
            center_hex=first['center_hex'],center_error=[b-a for a,b in zip(first['center'],last['center'])],
            beacon_displacement=[b-a for a,b in zip(first['prefix']['xyz'],last['prefix']['xyz'])],
            beacon_distance=math.dist(first['prefix']['xyz'],last['prefix']['xyz'])))
    write(out/'transitions.json',transitions)
    after={str(p):identity(p) for p in protected}
    if before != after: raise ValueError('INPUT_CHANGED')
    write(out/'preservation.json',dict(before=before,after=after))
    import sys
    write(out/'tools.json',dict(python=sys.version,argv=sys.argv,
        scripts=[identity(p) for p in Path(__file__).parent.glob('*.py')]))


if __name__ == '__main__': main()
