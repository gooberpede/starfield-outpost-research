# SPDX-License-Identifier: GPL-3.0-or-later
"""RG2-A1-F1 bounded offline challenge, stdlib and owned readers/math only.

Reads pinned frozen geometries, Save52 extractor/root receipts, installed main
ESM and source derivatives. Writes one exclusive --output JSON under .local-work;
raw reflected definition fields in that receipt stay LOCAL-ONLY. Pins every input
pre/post. No decoding, target/process/DB/configuration effects or new predictions.
Saved point queries apply the PREEXISTING v2 translation, never a fitted offset.
"""
from pathlib import Path
import argparse, collections, hashlib, json, math, struct, sys

R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records
from resource_availability import harvester_resource_gate
from resource_spatial import evaluate_region
from fractions import Fraction as F
from geometry import bounded_region_circle, nominal_strips, region_membership, point_membership

def pin(p):
    p=Path(p)
    with p.open('rb') as f: h=hashlib.file_digest(f,'sha256').hexdigest()
    return dict(path=str(p),bytes=p.stat().st_size,sha256=h)

def analyze():
    M=R/'.local-work/resource-geometry-mature-context'
    paths=[M/f'site-{n}-initial02.json' for n in ('feynman','carinae')]
    paths += [R/'.local-work/extractor-resource/run05/mature-Save52.json',
              R/'.local-work/workshop-population-rework/roots03/inventory.json',
              R/'.local-work/resource-availability/resource-definitions01.json',
              R/'.local-work/resource-geometry/source-definitions01.json',
              Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm')]
    before=[pin(p) for p in paths]
    assert before[-1]['sha256']=='1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
    loaded=[json.loads(p.read_text(encoding='utf8')) for p in paths[:-1]]
    sites=loaded[:2]; instances=loaded[2]['instances']; roots=loaded[3]['combined_roots']
    rootby={r['instance_identity']:r for r in roots}
    records=[]
    wanted={0x27ab66,0x6ac92,0x6ac8f,0x6ac95,0x6ac9c,0x6ac8e,0x5ef19,0x83fc,
            0x202f4f,0x5ef1e,0x83ec,0x271128,0x31986f,0x83ff,
            0x20a06c,0x20a073,0x20a08f,0x20a090}
    for r,fs in esm_records(paths[-1],{b'CONT',b'IRES',b'AVIF',b'DFOB'},repeated=True):
        if r['formid'] in wanted:
            f=dict(fs);props=[]
            if b'PRPS' in f:
                b=f[b'PRPS'];assert len(b)%12==0
                props=[dict(actor_value=f'{a:08x}',value=v,trailing_word=z)
                       for a,v,z in struct.iter_unpack('<IfI',b)]
            records.append(dict(**r,edid=f.get(b'EDID',b'').rstrip(b'\0').decode(),
                props=props,fields=[(t.decode(),b.hex()) for t,b in fs]))
    by={r['formid']:r for r in loaded[4]['records'] if r['plugin'].lower()=='starfield.esm'}
    water_rnam=[]
    for fid in (0xfc61c,0x145440,0x1160d9):
        rsgds=[int.from_bytes(bytes.fromhex(b),'little') for t,b in by[fid]['fields'] if t=='RNAM']
        declared=[int.from_bytes(bytes.fromhex(b),'little') for rid in rsgds for t,b in by[rid]['fields'] if t=='RNAM']
        water_rnam.append(dict(biome=f'{fid:08x}',rsgds=[f'{v:08x}' for v in rsgds],water_declared=0x83ec in declared))
    rows=[]; witnesses=[]
    resources={'Feynman':{'000057cb':'Nickel','000057ce':'Cobalt','000057cf':'Copper',
                         '000057d4':'Ionic Liquids','000057d0':'Fluorine','000083ec':'Water'},
               'Carinae':{'000057c9':'Alkanes','000057c7':'Iron','00005df1':'Rothicite'}}
    for site,owner,parent in zip(sites,['DYNAMIC:ff03388f','DYNAMIC:ff02be17'],['84ec80','84655c']):
        regions=[r for s in site['sources'] for r in s['regions']]
        for fid,label in resources[site['sample']].items():
            rs=[r for r in regions if r['resource']==fid]
            singles=[dict(source=r['source'],cell=r['cell'],point=r['points'][0],
                          native_bound=r['native_bound'],nominal=r['nominal'],
                          bounded=r['bounded_region_circle']) for r in rs if len(r['points'])==1]
            positive=[r for r in rs if r['bounded_region_circle']['intersection']=='POSITIVE_AREA']
            # Bound-overlap graph gives only possible connections. Different
            # graph components certify separated bounded-union groups; an edge
            # never certifies that the actual footprints touch.
            pending=set(range(len(positive)));groups=[]
            while pending:
                group={pending.pop()};queue=list(group)
                while queue:
                    i=queue.pop();a=positive[i]['native_bound']
                    for j in list(pending):
                        b=positive[j]['native_bound']
                        if sum((F(a[k])-F(b[k]))**2 for k in (0,1)) <= (F(a[3])+F(b[3]))**2:
                            pending.remove(j);group.add(j);queue.append(j)
                groups.append([dict(source=positive[i]['source'],cell=positive[i]['cell']) for i in sorted(group)])
            callbacks=[dict(source=r['source'],cell=r['cell'],result=evaluate_region(
                [*site['center'],0],150,0,r['native_bound'][:3],r['native_bound'][3],r['points'])) for r in rs]
            rows.append(dict(site=site['sample'],resource=fid,label=label,paths=len(rs),
                lengths=dict(collections.Counter(len(r['points']) for r in rs)),singletons=singles,
                width_min=min((p[3] for r in rs for p in r['points']),default=None),
                width_max=max((p[3] for r in rs for p in r['points']),default=None),
                sources=sorted({r['source'] for r in rs}),
                nominal_possible_connection_groups=groups,
                modeled_planar_native_callback=[v for v in callbacks if v['result']['accepted'] is not False],
                bounded=[dict(source=r['source'],cell=r['cell'],result=r['bounded_region_circle']) for r in rs if r['bounded_region_circle']['intersection']!='DISJOINT_OR_ZERO_AREA'],
                strips=[dict(source=r['source'],cell=r['cell'],result=r['nominal'].get('intersection','UNKNOWN')) for r in rs if r['nominal'].get('intersection','UNKNOWN')!='DISJOINT_OR_ZERO_AREA']))
        for a in instances:
            root=rootby.get(a['saved_reference'])
            if not root or root['owner_identity']!=owner:continue
            assert root['base_identity']==a['base_identity'] and root['record_offset']==a['offset']
            assert root['raw_position']==a['prefix']['xyz'] and a['prefix']['parent_token']==parent
            xy=[a['prefix']['xyz'][i]+site['translation'][i] for i in range(2)]
            fid=a['definition']['associations'][0]['resource_identity'].split(':')[1].zfill(8)
            selected=[r for r in regions if r['resource']==fid]
            gap=min((math.dist(xy,r['native_bound'][:2])-r['native_bound'][3] for r in selected),default=None)
            hits=lambda fn: [dict(source=r['source'],cell=r['cell'],state=fn(r['points'],xy)) for r in selected if fn(r['points'],xy)!='OUTSIDE']
            witnesses.append(dict(site=site['sample'],token=a['token'],identity=a['saved_reference'],
                base=a['base_identity'],resource=fid,owner=owner,parent=parent,
                offset=a['offset'],end=a['end'],saved_xyz=a['prefix']['xyz'],model_xy=xy,
                saved_disabled=root['saved_disabled'],saved_deleted=root['saved_deleted_bit'],
                beacon_distance_xy=math.dist(xy,site['center']),bounded_point=hits(region_membership),
                nearest_native_bound_point_gap=gap,
                tapered_point=hits(point_membership),production='NOT_ESTABLISHED',
                offset_domain='DECODED_LOGICAL_SAVE_STREAM'))
    # Synthetic POINTER identity distinguishes availability channels, never a
    # fabricated runtime pointer/snapshot. Source identities are separately read.
    controls=[]
    for branch,props in [('ordinary',(False,False,False)),('terrestrial_skip',(False,False,True)),
                         ('atmosphere',(False,True,False)),('bypass',(True,False,False))]:
        for has_water in (False,True):
            controls.append(dict(branch=branch,biome_water=has_water,
                result=harvester_resource_gate((1,),(),(),(1,) if has_water else (),
                    place_anywhere_present=props[0],atmosphere_present=props[1],skip_vein_present=props[2])))
    assert before==[pin(p) for p in paths]
    return dict(schema='sor-rg2a1-f1-reconciliation/1',inputs=before,definitions=records,
        geometry=rows,witnesses=witnesses,synthetic_gate_controls=controls,water_rnam=water_rnam,
        target_operations=False,model_changed=False)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    out=args.output.absolute();assert out.is_relative_to(R/'.local-work') and not out.exists()
    result=analyze()
    with out.open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
    print('witnesses',len(result['witnesses']),'resource summaries',len(result['geometry']),'inputs unchanged')
