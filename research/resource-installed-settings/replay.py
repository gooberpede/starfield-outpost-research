# SPDX-License-Identifier: GPL-3.0-or-later
"""C1H versioned offline replay with unchanged RG1 geometry arithmetic.

Reads frozen v2 requests, installed settings audit, local definitions, C1E/C1G
closed receipts and saved-witness CSV. Writes fresh local full geometry and a
reviewable numeric summary. No target, save, database, config or network effects.
Run from repository root. Unknown selection inputs fail instead of being fitted.
"""
import argparse
import collections
import copy
import csv
import hashlib
import json
import math
from pathlib import Path
import struct
import sys
from settings import ROOT, resolve, pin, bits

sys.path[:0] = [str(ROOT/'research/resource-geometry'),
               str(ROOT/'research/resource-region-ancestry')]
import geometry
from qualify import independent
from resource_spatial import evaluate_region
from resource_availability import generation_first_gate

def signature(r):
    return b''.join(struct.pack('<4f',*p) for p in r['points'])+struct.pack('<4f',*r['native_bound'])

def identity(r):
    return r['source'],r['resource'],tuple(r['cell']),signature(r)

def summarize(regions, center):
    return {fid:dict(paths=len(rs),
                    bounded=dict(collections.Counter(geometry.bounded_region_circle(r['points'],center)['intersection']
                                 if geometry.bounded_region_circle(r['points'],center)['status']!='UNKNOWN' else 'UNKNOWN' for r in rs)),
                    tapered=dict(collections.Counter(geometry.nominal_strips(r['points'],center).get('intersection','UNKNOWN') for r in rs)),
                    nominal_area=dict(collections.Counter(str(evaluate_region([*center,0],150,0,r['native_bound'][:3],r['native_bound'][3],r['points'])['accepted']) for r in rs)))
            for fid in sorted({r['resource'] for r in regions})
            for rs in [[r for r in regions if r['resource']==fid]]}

def run(a):
    settings = json.loads(a.settings.read_text(encoding='utf8'))
    # This version resolves main-file settings only when the installed audit
    # found no other named or same-ID candidate. No invented load-order merge.
    assert len(settings['candidates']) == 6 and all(c['file']=='Starfield.esm' for c in settings['candidates'])
    assert not settings['config_mentions']
    installed = {r['rarity']:r['installed_value'] for r in settings['settings']}
    defaults = {r['rarity']:r['default_value'] for r in settings['settings']}
    freeze_path = ROOT/'docs/experiments/resource-geometry-mature-context/freeze-mature-v2.json'
    freeze = json.loads(freeze_path.read_text())
    definitions = ROOT/'.local-work/resource-geometry/source-definitions01.json'
    defs = json.loads(definitions.read_text())['records']
    rarity = {f'{r["formid"]:08x}':int.from_bytes(bytes.fromhex(dict(r['fields'])['SNAM']),'little')&255 for r in defs if r['type']=='IRES'}
    operands_path = ROOT/'docs/experiments/resource-geometry-mature-context/operands-v2.json'
    operands = json.loads(operands_path.read_text())['rows']
    cs_path = ROOT/'.local-work/resource-milestone-b-spatial-constants.json'
    cs = json.loads(cs_path.read_text())['constants']
    constants = {int(c['va'],16):c['float'] for c in cs}
    witness_path = ROOT/'docs/experiments/resource-geometry-mature-context/f1-witnesses.csv'
    with witness_path.open(encoding='utf8') as f:
        witnesses = list(csv.DictReader(f))
    paths = [a.settings, freeze_path, definitions, operands_path, cs_path, witness_path,
             Path(__file__), ROOT/'research/resource-installed-settings/settings.py',
             ROOT/'research/resource-geometry/geometry.py', ROOT/'save-analysis/scripts/resource_spatial.py',
             *[Path(p['path']) for p in freeze['complete_geometry']]]
    before = {str(p):pin(p) for p in paths}
    result = dict(schema='sor-c1h-predictions/1', status='CONDITIONAL_INSTALLED_MAIN_SETTINGS_ORDINARY_INITIALIZATION',
                  publication='REVIEW-REQUIRED', scientific_promotion=False, inputs=before, sites=[])
    full = []
    for frozen_pin in freeze['complete_geometry']:
        assert pin(frozen_pin['path']) == frozen_pin['sha256']
        frozen = json.loads(Path(frozen_pin['path']).read_text())
        constants.update({int(c['va'],16):c['value'] for c in frozen['constants']})
        base, new, sources = [], [], []
        for s in frozen['sources']:
            req = copy.deepcopy(s['request'])
            provenance = []
            for r in req['ordered_resources']:
                cls = rarity[r['resource']]
                branch = 'everywhere' if cls==6 else 'ordinary'
                old = resolve(cls,s['mask'],defaults,branch)
                assert bits(old)==bits(r['weight']), (s['source'], r)
                provenance.append(dict(resource='0x'+r['resource'], rarity=cls, branch=branch,
                                       mask=s['mask'],cell_chance=r['block'][7],
                                       default_weight_bits=bits(old),installed_weight_bits=bits(resolve(cls,s['mask'],installed,branch))))
            regenerated = geometry.populate_source(req,constants)
            assert regenerated['status']=='CONDITIONAL_PLANAR_SOURCE'
            assert [identity(r) for r in regenerated['regions']]==[identity(r) for r in s['regions']]
            base.extend(regenerated['regions'])
            for r in req['ordered_resources']:
                cls = rarity[r['resource']]
                r['weight'] = resolve(cls,s['mask'],installed,'everywhere' if cls==6 else 'ordinary')
            generated = geometry.populate_source(req,constants)
            assert generated['status']=='CONDITIONAL_PLANAR_SOURCE'
            new.extend(generated['regions'])
            case = next(o for o in operands if o['name']==frozen['name'])
            family = next(f for f in case['candidate_families'] if int(f['biome'],16)==s['source']['resource_biome'])
            sources.append(dict(source=s['source'], selection=family, operands=provenance,
                                baseline_count=len(s['regions']),installed_count=len(generated['regions'])))
            full.append(dict(site=frozen['sample'],request=req,regions=generated['regions']))
        bs, ns = {identity(r) for r in base}, {identity(r) for r in new}
        def member(k):
            return dict(source=k[0],resource='0x'+k[1],cell=k[2],geometry_sha256=hashlib.sha256(k[3]).hexdigest())
        row = dict(site=frozen['sample'],frame=dict(center=frozen['center'],translation=frozen['translation'],
                   origin=frozen['origin'],basis=frozen['source_frame_basis']),sources=sources,
                   baseline_count=len(base),installed_count=len(new),unchanged_geometry=len(bs&ns),
                   removed=[member(k) for k in sorted(bs-ns)],added=[member(k) for k in sorted(ns-bs)],
                   baseline=summarize(base,frozen['center']), installed=summarize(new,frozen['center']),witnesses=[])
        for w in witnesses:
            if w['site']!=frozen['sample']:continue
            xy = [float(w['model_x']),float(w['model_y'])]
            def diagnostic(pop):
                rs=[r for r in pop if r['resource']==w['resource']]
                return dict(bounded_hits=sum(geometry.region_membership(r['points'],xy)=='INTERIOR' for r in rs),
                            tapered_hits=sum(geometry.point_membership(r['points'],xy)=='INTERIOR' for r in rs),
                            nearest_bound_gap=min(math.dist(xy,r['native_bound'][:2])-r['native_bound'][3] for r in rs))
            row['witnesses'].append(dict(token=w['token'],resource='0x'+w['resource'],model_xy=xy,
                                         baseline=diagnostic(base),installed=diagnostic(new)))
        if frozen['sample']=='Feynman':
            row.update(native_compare(new,base))
            row['chance_comparison'] = chance_compare(full)
        result['sites'].append(row)
    assert before=={str(p):pin(p) for p in paths}
    result['limits'] = 'No complete native census, historical source/epoch join, final catalogue admission, or Carinae live geometry. Retained C1E query replay remains conditional on per-use stability.'
    return result,full

def native_compare(new,base):
    receipts=ROOT/'.local-work/resource-region-ancestry/retail-attempt01'
    rows=[independent(p)[1] for p in sorted(receipts.glob('capture-*.bin'))]
    events=[json.loads(line) for line in (receipts/'events.jsonl').read_text().splitlines()]
    assert rows==[r for r in events if r['kind']=='SAMPLE']
    analysis=json.loads((ROOT/'.local-work/resource-region-ancestry/analysis-attempt01.json').read_text())
    assert analysis['event_sha256']==pin(receipts/'events.jsonl')
    transfer=rows[-1]
    assert transfer['ancestry']=='BOUND_TRANSFER'
    assert len(rows)==967
    accepted=[]; visited=collections.Counter(); observed_sigs=set()
    for r in rows:
        if r.get('decision') not in ('ACCEPT','REJECT'):continue
        h=bytes.fromhex(r['geometry']['raw_region']);p=bytes.fromhex(r['geometry']['ordered_xyzw'])
        fid=f'{struct.unpack_from("<I",bytes.fromhex(r["selected"]["raw_resource"]),40)[0]:08x}'
        sig=p+h[:16]; observed_sigs.add((fid,sig))
        matches=[g for g in new if g['resource']==fid and signature(g)==sig]
        visited[r['decision']]+=1
        visited[r['decision']+'_exact_modeled_geometry']+=bool(matches)
        q=struct.unpack('<3f',bytes.fromhex(r['qb_retained_bits']))
        radius,upper=struct.unpack_from('<2f',bytes.fromhex(r['raw_closure']),16)
        d=evaluate_region(q,radius,upper,struct.unpack_from('<3f',h),struct.unpack_from('<f',h,12)[0],list(struct.iter_unpack('<4f',p)))
        visited['retained_query_'+str(d['accepted'])+'_native_'+r['decision']]+=1
        if r['decision']=='ACCEPT':
            assert r['ancestry']=='BOUND_CALLBACK' and r['file_provenance']['main_file_identity']
            assert all(r[k]==transfer[k] for k in ('pid','tid','thread_lifetime','updater_token','temporary_set'))
            assert any(m['pointer']==r['resource_pointer'] for m in transfer['refresh_payload']['members'])
            assert any(j['capture']==r['capture'] and j['accepted_region_to_transfer'] for j in analysis['joins'])
            accepted.append(dict(capture=r['capture'],resource='0x'+fid,native_source_ordinal=r['source_ordinal'],
                raw_sha256=pin(receipts/f'capture-{r["capture"]:05d}.bin'),
                geometry_sha256=hashlib.sha256(sig).hexdigest(),
                baseline_matches=sum(g['resource']==fid and signature(g)==sig for g in base),
                installed_matches=[dict(source=g['source'],cell=g['cell']) for g in matches],
                query_xyz=q,radius=radius,absolute_upper=upper,retained_query_replay=d,
                native_generation_source='UNKNOWN',historical_epoch='UNKNOWN'))
    assert len(accepted)==4
    # Use the actual retained query operands, not the nominal 150-unit circle.
    q,radius,upper=accepted[0]['query_xyz'],accepted[0]['radius'],accepted[0]['absolute_upper']
    assert all((x['query_xyz'],x['radius'],x['absolute_upper'])==(q,radius,upper) for x in accepted)
    positives=collections.Counter(); unknown=collections.Counter()
    for g in new:
        d=evaluate_region(q,radius,upper,g['native_bound'][:3],g['native_bound'][3],g['points'])
        if d['accepted']:positives['0x'+g['resource']]+=1
        if d['accepted'] is None:unknown['0x'+g['resource']]+=1
    return dict(accepted=accepted,visited=dict(visited),
                modeled_paths_without_exact_visited_geometry=sum((g['resource'],signature(g)) not in observed_sigs for g in new),
                actual_retained_query_positive_paths=dict(positives),actual_retained_query_unknown_paths=dict(unknown),
                events_sha256=pin(receipts/'events.jsonl'))

def chance_compare(full):
    receipts=ROOT/'.local-work/resource-selection-operands/retail-attempt01'
    comparisons=[]
    # The existing independent decoder also reads the C1G three-frame SRO1 envelope.
    for capture in (1129,1141,1431):
        path=receipts/f'capture-{capture:05d}.bin'
        r=independent(path)[1]
        assert r['site']=='chance_branch' and r['resource_call_join']
        fid=0x57d4 if capture in (1129,1141) else 0x57cf
        src=next(s for s in full if s['site']=='Feynman' and s['request']['source']=='0:25116:32448:00257f38')
        resource=next(x for x in src['request']['ordered_resources'] if int(x['resource'],16)==fid)
        xy=struct.unpack('<ii',bytes.fromhex(r['cell_xy_i32']['raw']))
        key=int.from_bytes(bytes.fromhex(r['packed_key_u64']['raw']),'little')
        assert src['request']['packed_keys'][f'{xy[0]},{xy[1]}']==key
        gate=generation_first_gate(key,src['request']['owner_key'],resource['block'][7],resource['weight'])
        call_capture=1020 if fid==0x57d4 else 1310
        call=independent(receipts/f'capture-{call_capture:05d}.bin')[1]
        assert call['site']=='resource_call'
        assert all(r[k]==call[k] for k in ('pid','tid','thread_lifetime','invocation_token','entry_rsp'))
        assert struct.unpack_from('<I',bytes.fromhex(call['ires']['raw']),0x28)[0]==fid
        assert int.from_bytes(bytes.fromhex(r['cell_dnam_pointer']['raw']),'little')==call['selected_dnam']['address']
        observed=dict(weight=f'0x{call["effective_weight_bits"]:08x}',draw=f'0x{r["draw_times_100_bits"]:08x}',threshold=f'0x{r["threshold_bits"]:08x}',edge=r['chance_edge'])
        predicted=dict(weight=bits(resource['weight']),draw=bits(gate['draw100']),threshold=bits(gate['threshold']),edge='ADMIT' if gate['first_gate_pass'] else 'REJECT')
        comparisons.append(dict(capture=capture,call_capture=call_capture,resource=f'0x{fid:08x}',cell=xy,observed=observed,predicted=predicted,equal=observed==predicted,receipt_sha256=pin(path),call_sha256=pin(receipts/f'capture-{call_capture:05d}.bin')))
    return comparisons

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--settings',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--geometry',type=Path,required=True)
    a=ap.parse_args()
    assert all(p.resolve().is_relative_to(ROOT/'.local-work/resource-installed-settings') for p in (a.output,a.geometry))
    assert not a.output.exists() and not a.geometry.exists()
    result,full=run(a)
    for path,value in ((a.output,result),(a.geometry,full)):
        with path.open('x',encoding='utf8',newline='\n') as f:
            json.dump(value,f,indent=2);f.write('\n')
    print([(r['site'],r['baseline_count'],r['installed_count'],len(r['removed']),len(r['added'])) for r in result['sites']])
