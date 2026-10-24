# SPDX-License-Identifier: GPL-3.0-or-later
"""RG2-D2 offline stages; run from the repository with installed CPython.

Inventory reads pinned Save52, installed PNDT definitions and existing protection
manifests. Resource groups are skipped structurally, never resolved in stage one.
Names remain local and are excluded from prediction requests. Outputs are new
ignored files only. No target, network, source-save or analysis-project effects.
Prediction and comparator are separate processes; the latter requires a freeze.
"""
import argparse
import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'save-analysis/scripts'), str(ROOT/'research/resource-geometry'),
                str(ROOT/'research/resource-pattern-selection'), str(Path(__file__).parent),
                str(ROOT/'research/resource-carinae-source-context')]
import builder
from inventory_historical_saves import guard
from stream_save import decoded_save
from validate_mature_outposts import directory, pool, envelopes
from outpost_planetary_location import extract
from outpost_record_framing import iter_records
from research_durable_center import initial_transform
from research_workshop_origin import workshop_prefix
from planet_world_key import find_unit3_context, unit3_world_descriptors, qualified_grid
from saved_world_components import find_world_components
from durable_position_model import center
from inspect_outpost_definitions import esm_records

OUT = ROOT/'.local-work/resource-save52'


def select_root(path):
    """Select only an ignored local receipt root, without touching old runs."""
    global OUT
    selected = Path(path).resolve()
    if not selected.is_relative_to(ROOT/'.local-work'):
        raise ValueError('OUTPUT_MUST_BE_LOCAL')
    OUT = selected


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f:
        f.write(json.dumps(value, indent=2, allow_nan=False).encode('utf8')+b'\n')


def skip_resources(c, refs, count):
    """Consume framing without retaining resource tokens, labels or row bytes."""
    if count > (c.end-c.p)//4:
        raise ValueError('RESOURCE_GROUP_BOUNDS')
    for _ in range(count):
        refs(1)
        n = int.from_bytes(c.take(4), 'little')
        if n > (c.end-c.p)//17:
            raise ValueError('RESOURCE_ROW_BOUNDS')
        refs(n*2)
        c.take(n*17)
    return []


def source():
    # Historical inventory is consulted solely for this record's primary pin.
    path = ROOT/'.local-work/historical-inventory/scan-04/inventory.json'
    row = next(r for r in json.loads(path.read_text()) if r['inventory_id']=='HIST-0267')
    p = Path(row['source']['path'])
    expected = '6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8'
    if row['source']['sha256'] != expected or builder.pin(p) != expected:
        raise ValueError('SAVE52_IDENTITY')
    return p


def inventory():
    guard()
    OUT.mkdir(exist_ok=False)
    import protection
    audit = protection.audit()
    write(OUT/'protected-before.json', audit)
    if audit['changes']:
        raise ValueError('PROTECTION_FAILURE')
    frozen = json.loads((ROOT/'.local-work/resource-standalone/frozen-before.json').read_text())
    write(OUT/'frozen-format.json', dict(type=type(frozen).__name__,
                                        keys=list(frozen)[:3] if isinstance(frozen,dict) else []))
    p = source()
    if builder.pin(builder.ESM) != builder.DEFINITION or builder.pin(builder.EXE) != builder.EXE_HASH:
        raise ValueError('INSTALLED_IDENTITY')
    records = []
    bodies = {}
    for h, fs in esm_records(builder.ESM, {b'PNDT'}):
        records.append(dict(type='PNDT',formid=h['formid'],edid=fs.get(b'EDID',b'').rstrip(b'\0').decode(),
                            fields={k.decode():v.hex() for k,v in fs.items()}))
        if len(fs.get(b'GNAM',b''))==12:
            system, parent, index = struct.unpack('<III',fs[b'GNAM'])
            bodies[(system,index)] = f'{h["formid"]:08X}'
    with decoded_save(p, OUT/'scratch', seconds=float('inf')) as (b, metrics):
        d = directory(b)
        ex = extract(b, records)
        _, strings = pool(b,d)
        context = find_unit3_context(b,d['regions']['region_R1'][0],ex['global_units'][4][0]-8)
        descs, _ = unit3_world_descriptors(b,context)
        parents = {int(r['parent_token'],16) for r in ex['beacons']}
        components = find_world_components(b,*ex['global_units'][6],parents,bodies,descs)
        registrations = [e for e in envelopes(b,d) if e['qualifies'] and 'parsed' in e]
        if len(registrations)!=1:
            raise ValueError('REGISTRATION_ENVELOPE')
        registered = set(registrations[0]['parsed']['beacons'])
        wanted = {r['token']:r for r in ex['beacons']}
        cases = []
        for r in iter_records(b,*d['regions']['region_R3'],d['words'][9]):
            if r['token'] not in wanted:
                continue
            a = wanted[r['token']]
            t = initial_transform(b,r)
            prefix = t['prefix']
            row = dict(case='D2-'+r['token'],token=r['token'],record_offset=r['offset'],
                       offset_domain='DECODED_LOGICAL_STREAM',name=[strings[i]['text'] for i in r['strings']],
                       disabled=prefix['disabled'],deleted=prefix['deleted'],registered=r['token'] in registered,
                       body=f'{a["proposed_body_formid"]:08x}' if a['proposed_body_formid'] else None,
                       body_concordant=a['independent_direct_agreement'],frame=t['initial_frame_flag'],
                       parent=a['parent_token'],request=None)
            row['eligibility'] = ('DISABLED' if prefix['disabled'] or prefix['deleted'] else
                'ACTIVE' if prefix['disabled'] is False and r['token'] in registered and a['independent_direct_agreement'] else 'INDETERMINATE')
            try:
                w = workshop_prefix(b,r,prefix,skip_resources)
                row['workshop_id'] = w['identifier98_hex']
                co = next(v for v in components['rows'] if v['world']==a['parent_token'])
                de = next(v for v in descs if v['world_token']==co['secondary'])
                if de['body']!=co['body'] or de['body'].lower()!=row['body']:
                    raise ValueError('BODY_JOIN_MISMATCH')
                row['descriptor_key'] = de['key']
                origin = qualified_grid(int(de['key'],16))
                query, _ = center(prefix['xyz'],struct.unpack('<3f',bytes.fromhex(w['delta_hex'])))
                row['center'] = query
                if row['frame']!=0x0b or origin['tag'] not in (0,1):
                    raise ValueError('UNSUPPORTED_FRAME_OR_SEAM')
                if origin['x']%96 or origin['y']%96:
                    raise ValueError('UNALIGNED_DESCRIPTOR')
                row['request'] = dict(schema='sor-d1-request/1',definition=builder.DEFINITION,body=row['body'],
                    chart=origin['tag'],descriptor=[origin['x'],origin['y']],query=query,
                    radius=150.0,upper=struct.unpack('<f',struct.pack('<f',query[2]+100))[0])
                row['footprint'] = 'Fixed 150-unit ordinary query disk, upper=center Z+100; no hardware-derived fit'
            except (ValueError, StopIteration) as error:
                row['unsupported'] = str(error) or 'MISSING_WORLD_JOIN'
            cases.append(row)
        write(OUT/'inventory-v1.json',dict(time=now(),source=str(p),sha256=builder.pin(p),metrics=metrics,
              cases=cases,registered=sorted(registered),components=components,descriptors=descs,
              scope='Case-5 ordinary inline bases; registration envelope and direct/cache body joins',
              source_code={str(q.relative_to(ROOT)):builder.pin(q) for q in Path(__file__).parent.glob('*.py')}))
    print(json.dumps([{k:r.get(k) for k in ('case','eligibility','registered','body','frame','unsupported')} for r in cases]))


def qualify():
    """Qualify site-centre projection independently of resource answers."""
    from audit_beacon_projection import audit as project
    from ordinary_outpost_beacons import summarize
    from test_outpost_record_framing import independent
    old = json.loads((OUT/'inventory-v1.json').read_text())
    records = []
    for h, fs in esm_records(builder.ESM,{b'PNDT'}):
        records.append(dict(type='PNDT',formid=h['formid'],edid=fs.get(b'EDID',b'').rstrip(b'\0').decode(),
                            fields={k.decode():v.hex() for k,v in fs.items()}))
    with decoded_save(source(),OUT/'scratch',seconds=float('inf')) as (b,metrics):
        d = directory(b)
        ex = extract(b,records)
        census = summarize(b,dict(direct_bases={0x2c60e9:'OutpostBeaconActivator'},templates={}))
        ordinary = {r['saved_reference_token'] for r in census['candidates'] if r['category']=='ordinary'}
        if ordinary != {r['token'] for r in old['cases']}:
            raise ValueError('CENSUS_DISAGREEMENT')
        arithmetic = independent(b,*d['regions']['region_R3'],d['words'][9])
        framing = [(r['offset'],r['end'],r['token'],r['flags']) for r in
                   iter_records(b,*d['regions']['region_R3'],d['words'][9])]
        if framing != [r[:4] for r in arithmetic]:
            raise ValueError('INDEPENDENT_FRAMING')
        for row in old['cases']:
            row['control'] = row['token'] in ('83388f','82be17')
            a = next(v for v in ex['beacons'] if v['token']==row['token'])
            sites = []
            for p in a['points']:
                pair = struct.unpack_from('<2d',b,p['offset']+6)
                sites.append(project(pair))
            row['site_projection'] = sites
            row['request'] = None
            if row['eligibility']!='ACTIVE':
                continue
            try:
                cells = {(v['tag'],v['i'],v['j']) for v in sites}
                if len(cells)!=1 or any(max(abs(v['square_residual_x']),abs(v['square_residual_y']))>0.001 for v in sites):
                    raise ValueError('SITE_GRID_CENTRE_NOT_QUALIFIED')
                tag,x,y = next(iter(cells))
                origin = qualified_grid(int(row['descriptor_key'],16))
                if tag not in (0,1) or tag!=origin['tag']:
                    raise ValueError('SITE_DESCRIPTOR_CHART_OR_SEAM')
                if row['frame']!=0x2b:
                    raise ValueError('UNQUALIFIED_FRAME')
                query = [struct.unpack('<f',struct.pack('<f',row['center'][k]+100*(v-origin[a])))[0]
                         for k,v,a in ((0,x,'x'),(1,y,'y'))]+[row['center'][2]]
                row['site_cell'] = [tag,x,y]
                row['request'] = dict(schema='sor-d1-request/1',definition=builder.DEFINITION,body=row['body'],
                    chart=tag,descriptor=[origin['x'],origin['y']],query=query,radius=150.0,
                    upper=struct.unpack('<f',struct.pack('<f',query[2]+100))[0])
                row['coordinate_qualification'] = 'STATIC ordinary initialization; grid-centre residual <0.001 fine cells; historical rebase/epoch unknown'
                row.pop('unsupported',None)
            except ValueError as error:
                row['unsupported'] = str(error)
        write(OUT/'inventory-v2.json',dict(old,time=now(),cases=old['cases'],census=census,
              independent_records=len(framing),coordinate_rule='Existing saved-frame 0x2b site base; float32 center plus 100*(site-descriptor)'))
    print(json.dumps([{k:r.get(k) for k in ('case','control','eligibility','site_cell','unsupported')} for r in old['cases']]))


def predict():
    """Close all first-pass outputs before any comparator process is allowed."""
    build = OUT/'build-v1'
    out = OUT/'first-pass-v1'
    out.mkdir(exist_ok=False)
    empty = out/'empty'
    empty.mkdir()
    inputs = {str(p):builder.pin(p) for p in [OUT/'requests-v1.json',build/'normalized.json',
              build/'manifest.json',*list((build/'code').glob('*.py'))]}
    write(out/'input-freeze.json',dict(time=now(),inputs=inputs))
    results = []
    for item in json.loads((OUT/'requests-v1.json').read_text()):
        guard()
        case = item['case']
        qpath = out/(case+'-request.json')
        write(qpath,item['request'])
        command = [sys.executable,'-I','-S','-B',str(Path(__file__).with_name('isolate.py')),
            '--code',str(build/'code'),'--corpus',str(build/'normalized.json'),'--request',str(qpath)]
        start = now()
        p = subprocess.run(command,cwd=empty,capture_output=True)
        (out/(case+'-stdout.json')).write_bytes(p.stdout)
        (out/(case+'-audit.json')).write_bytes(p.stderr)
        if p.returncode:
            raise RuntimeError(p.stderr.decode())
        r = json.loads(p.stdout)
        audit = json.loads(p.stderr)
        if audit['inference_forbidden'] or audit['denied_probes']!=8:
            raise ValueError('ISOLATION_FAILURE')
        results.append(dict(case=case,control=item['control'],start=start,end=now(),status=r['status'],
            reason=r.get('reason'),resources=r.get('availability',{}),source_count=r.get('source_count'),
            regions=len(r.get('regions',[])),failures=r.get('failures',[]),command=command,
            output_sha256=builder.pin(out/(case+'-stdout.json')),audit_sha256=builder.pin(out/(case+'-audit.json'))))
        print(json.dumps({k:v for k,v in results[-1].items() if k not in ('command','failures')}),flush=True)
    if any(builder.pin(p)!=h for p,h in inputs.items()):
        raise ValueError('FROZEN_INPUT_CHANGED')
    write(out/'summary.json',results)
    files = {str(p):builder.pin(p) for p in out.glob('*') if p.is_file()}
    write(out/'prediction-freeze.json',dict(time=now(),inputs=inputs,files=files,
        contract='All outputs closed and hashed before comparator launch; no comparator resource evidence read by this process'))


def requests():
    """Project every eligible case into the exact D1 request schema."""
    path = OUT/'inventory-v2.json'
    inv = json.loads(path.read_text())
    write(OUT/'requests-v1.json',[dict(case=r['case'],control=r['control'],request=r['request'])
          for r in inv['cases'] if r['eligibility']=='ACTIVE'])
    write(OUT/'roster-freeze.json',dict(time=now(),inventory_sha256=builder.pin(path),
          requests_sha256=builder.pin(OUT/'requests-v1.json')))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('stage',choices=['inventory','qualify','requests','predict'])
    ap.add_argument('--root',type=Path,default=OUT)
    args=ap.parse_args()
    select_root(args.root)
    globals()[args.stage]()
