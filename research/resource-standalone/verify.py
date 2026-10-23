# SPDX-License-Identifier: GPL-3.0-or-later
"""D1 held-out verification, ablation, isolation and bounded benchmarks.

Reads completed local corpus, seven protected native receipts and owned code.
Writes a fresh ignored results directory; isolated subprocesses execute only
the completed bundle in an empty cwd. Native controls are opened after output
is closed and hashed. No target operations, source updates or external access.
"""
import argparse
import copy
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics
import struct
import subprocess
import sys
import time
import zlib

ROOT=Path(__file__).resolve().parents[2]


def pin(path):
    with Path(path).open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()


def save(path,value):
    with path.open('x',encoding='utf8',newline='\n') as f:
        json.dump(value,f,indent=2,allow_nan=False);f.write('\n')


def native(path):
    """Adapt C2B independent framed parser; verify sequence, digest and ACK."""
    raw=path.read_bytes();at=0;rows=[]
    while at<len(raw):
        magic,seq,n,digest=struct.unpack_from('<4sQI32s',raw,at);at+=48
        if magic!=b'SRO1' or seq!=len(rows)+1 or n>1048576:raise ValueError('capture header')
        body=raw[at:at+n];at+=n
        if len(body)!=n or hashlib.sha256(body).digest()!=digest:raise ValueError('capture digest')
        rows.append(json.loads(body))
    ack=json.loads(path.with_suffix('.ack.json').read_text())
    if at!=len(raw) or ack['sha256']!=pin(path) or ack['bytes']!=len(raw):raise ValueError('capture closure')
    if [r['kind'] for r in rows]!=['SESSION','SAMPLE','END']:raise ValueError('capture kinds')
    return rows[1]


def request(body):
    feynman=body=='0005e0de'
    return dict(schema='sor-d1-request/1',definition='1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7',
        body=body,chart=0,descriptor=[25152,32448] if feynman else [21408,15648],
        query=[-2716.539306640625,-132.11228942871094,-0.10489535331726074] if feynman else
              [-813.3619384765625,-729.5208740234375,68.7126693725586],radius=150.0,
        upper=99.89510345458984 if feynman else 168.71267700195312)


def run(build,out):
    build=build.resolve();out=out.resolve()
    if not out.is_relative_to(ROOT/'.local-work') or out.exists():raise ValueError('fresh local output')
    out.mkdir(parents=True);empty=out/'empty';empty.mkdir()
    sourcepins={str(p):pin(p) for p in [*build.rglob('*'),Path(__file__),Path(__file__).with_name('isolate.py')] if p.is_file()}
    outputs={};isolation=[]
    for variant in ('normalized','expanded'):
        for body in ('0005e0de','0005e4da'):
            qpath=out/f'{body}-request.json'
            if not qpath.exists():save(qpath,request(body))
            command=[sys.executable,'-I','-S','-B',str(Path(__file__).with_name('isolate.py')),
                '--code',str(build/'code'),'--corpus',str(build/f'{variant}.json'),'--request',str(qpath)]
            start=time.perf_counter();p=subprocess.run(command,cwd=empty,capture_output=True)
            (out/f'{variant}-{body}-stdout.json').write_bytes(p.stdout)
            (out/f'{variant}-{body}-audit.txt').write_bytes(p.stderr)
            if p.returncode:raise RuntimeError(p.stderr.decode())
            r=json.loads(p.stdout);audit=json.loads(p.stderr)
            if audit['inference_forbidden'] or audit['denied_probes']!=8:raise ValueError('isolation failure')
            if r['status']!='CONDITIONAL_GEOMETRY':raise ValueError(('prediction',r))
            outputs[variant,body]=r
            isolation.append(dict(variant=variant,body=body,seconds=time.perf_counter()-start,
                denied_probes=audit['denied_probes'],forbidden_inference_attempts=len(audit['inference_forbidden']),
                output_sha256=pin(out/f'{variant}-{body}-stdout.json'),command=command))
    startup=[]
    for variant in ('normalized','expanded'):
        command=[sys.executable,'-I','-S','-B',str(Path(__file__).with_name('isolate.py')),
            '--code',str(build/'code'),'--corpus',str(build/f'{variant}.json'),
            '--request',str(out/'0005e0de-request.json'),'--load-only']
        start=time.perf_counter();p=subprocess.run(command,cwd=empty,capture_output=True)
        if p.returncode or json.loads(p.stdout)['status']!='LOADED_AND_VALIDATED':raise ValueError('cold startup')
        startup.append(dict(variant=variant,cold_process_load_seconds=time.perf_counter()-start))
        (out/f'{variant}-startup-audit.txt').write_bytes(p.stderr)
    save(out/'startup.json',startup)
    # Only now open native controls. They are absent from builder/inference inputs.
    comparisons=[]
    controls={'0005e0de':('resource-region-ancestry',(299,325,696,716)),
              '0005e4da':('resource-carinae',(1270,1280,1301))}
    expected_pins={row['path'].replace('\\','/'):row['sha256'] for row in csv.DictReader(
        (ROOT/'docs/experiments/resource-pattern-selection/sources.csv').open(encoding='utf8'))}
    for body,(folder,ids) in controls.items():
        for n in ids:
            path=ROOT/f'.local-work/{folder}/retail-attempt0{1 if body=="0005e0de" else 2}/capture-{n:05d}.bin'
            if pin(path)!=expected_pins[path.relative_to(ROOT).as_posix()]:raise ValueError('native pin mismatch')
            sourcepins[str(path)]=pin(path);sourcepins[str(path.with_suffix('.ack.json'))]=pin(path.with_suffix('.ack.json'))
            row=native(path)
            fid=f'{struct.unpack_from("<I",bytes.fromhex(row["selected"]["raw_resource"]),40)[0]:08x}'
            geometry=row['geometry']['ordered_xyzw'];bound=row['geometry']['raw_region'][:32]
            for variant in ('normalized','expanded'):
                matches=[r for r in outputs[variant,body]['regions'] if r['resource']==fid and
                    r['ordered_xyzw_le']==geometry and r['native_bound_le']==bound]
                comparisons.append(dict(body=body,capture=n,variant=variant,resource='0x'+fid,
                    exact_matches=len(matches),native_decision=row['decision'],
                    callback_matches=all(r['callback']['accepted'] == (row['decision']=='ACCEPT') for r in matches)))
                if len(matches)!=1 or not comparisons[-1]['callback_matches']:
                    raise ValueError('held-out geometry or callback mismatch')
    save(out/'comparisons.json',comparisons)
    sys.path[:0]=[str(build/'code')]
    import predictor
    import geometry
    from predictor import predict,seal
    corpora={v:json.loads((build/f'{v}.json').read_text()) for v in ('normalized','expanded')}
    for body in controls:
        a,b=[outputs[v,body] for v in ('normalized','expanded')]
        if a['regions']!=b['regions'] or a['availability']!=b['availability']:raise ValueError('variant divergence')
    benchmarks=[]
    for variant,env in corpora.items():
        # Planet means a bounded request batch on one represented body, never a
        # whole-planet region census or an extrapolated full raster generation.
        for name,qs in (('one-outpost',[request('0005e0de')]),
            ('one-planet',[dict(request('0005e0de'),query=[-2716.539306640625+dx,-132.11228942871094+dy,0])
                for dx,dy in ((0,0),(100,0),(0,100))]),
            ('multiple-planets',[request('0005e0de'),request('0005e4da')])):
            times=[]
            for _ in range(2):
                start=time.perf_counter();rs=[predict(env,q) for q in qs];times.append(time.perf_counter()-start)
                if any(r['status']!='CONDITIONAL_GEOMETRY' for r in rs):raise ValueError('benchmark coverage')
            load=[]
            for _ in range(20):
                start=time.perf_counter();predictor.validate(json.loads((build/f'{variant}.json').read_text()));load.append(time.perf_counter()-start)
            benchmarks.append(dict(variant=variant,case=name,requests=len(qs),bodies=len({q['body'] for q in qs}),
                prediction_seconds=times,median_seconds=statistics.median(times),load_validate_median_seconds=statistics.median(load),
                regions=[len(r['regions']) for r in rs],coverage='Only supplied interior coarse tiles'))
    save(out/'benchmarks.json',benchmarks)
    base=corpora['normalized']['payload'];q=request('0005e0de')
    base_result=outputs['normalized','0005e0de'];ablations=[]
    for group in ('constants','settings','patterns','source_blocks','generation_blocks','bodies'):
        c=copy.deepcopy(base);del c[group];r=predict(seal(c),q)
        ablations.append(dict(group=group,operation='remove',status=r['status'],reason=r.get('reason')))
        if r['status']!='UNKNOWN':raise ValueError('missing group accepted')
    for name,edit in (
        ('inactive-settings',lambda c:c['settings'].__setitem__(3,0.01)),
        ('source-dimensions',lambda c:c['source_blocks'][base_result['regions'][0]['source'].split(':')[-1]].__setitem__(0,
            c['source_blocks'][base_result['regions'][0]['source'].split(':')[-1]][0]+12)),
        ('competition-order',lambda c:[v['resources'].reverse() for b in c['bodies'].values() for v in b['biomes'].values()]),
        ('system-key',lambda c:c['bodies']['0005e0de'].__setitem__('system',86470))):
        c=copy.deepcopy(base);edit(c);r=predict(seal(c),q)
        changed=r.get('regions')!=base_result['regions']
        ablations.append(dict(group=name,operation='perturb',status=r['status'],geometry_changed=changed))
        if not changed:raise ValueError('uninformative ablation '+name)
    save(out/'ablations.json',ablations)
    sizes=[]
    for variant,env in corpora.items():
        c=env['payload']
        for bodies in ([],['0005e0de'],['0005e4da'],list(c['bodies'])):
            sub=copy.deepcopy(c);sub['bodies']={b:sub['bodies'][b] for b in bodies}
            raw=predictor.canonical(predictor.seal(sub))+b'\n'
            sizes.append(dict(variant=variant,bodies=bodies,bytes=len(raw),zlib9_bytes=len(zlib.compress(raw,9)),
                note='Fixed shared tables retained to expose per-body marginal cost; empty-body size is accounting only'))
    save(out/'sizes.json',sizes)
    if any(pin(p)!=h for p,h in sourcepins.items()):raise ValueError('input changed')
    summary=dict(schema='sor-d1-validation/1',comparisons=comparisons,isolation=isolation,startup=startup,benchmarks=benchmarks,
        sizes=sizes,ablations=ablations,inputs=sourcepins,
        sites=[dict(body=b,regions=len(outputs['normalized',b]['regions']),sources=outputs['normalized',b]['source_count'],
            matched_native_controls=len(controls[b][1]),missing_native_controls=0,
            additional_generated_paths_without_seven_control_witness=len(outputs['normalized',b]['regions'])-len(controls[b][1]),
            additional_paths_classification='UNVERIFIED; not established native extras or errors',
            spatial_membership={resource:{key:sum(geometry.region_membership(r['points'],request(b)['query'][:2])==key
                for r in outputs['normalized',b]['regions'] if r['resource']==resource)
                for key in ('INTERIOR','BOUNDARY','OUTSIDE','UNKNOWN')}
                for resource in outputs['normalized',b]['availability']},
            availability=outputs['normalized',b]['availability'],native_census='UNKNOWN') for b in controls])
    save(out/'summary.json',summary)
    print(json.dumps({k:summary[k] for k in ('sites','comparisons')}))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--build',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();run(args.build,args.output)
