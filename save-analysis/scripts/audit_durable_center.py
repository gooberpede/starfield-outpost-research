"""SPDX-License-Identifier: GPL-3.0-or-later
SOR-EXP-0018 selected numerical audit. Reads research_durable_center receipts,
fresh research_workshop_origin capture receipt and fixed-city CSV. Writes a NEW
directory of authored numerical CSVs and summary JSON only. Stdlib/project math,
no raw save reads, target/database/network/Git effects. 40 GB guard enforced.
"""
import argparse
import collections
import csv
import json
from pathlib import Path
import struct

from inventory_historical_saves import identity, guard
from research_workshop_origin import write
from audit_beacon_projection import audit


def table(path, rows):
    if not rows: raise ValueError('EMPTY_TABLE')
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with path.open('x',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n')
        w.writeheader(); w.writerows(rows)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--receipts',type=Path,required=True)
    ap.add_argument('--captures',type=Path,required=True)
    ap.add_argument('--fixed',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--session',type=Path)
    a=ap.parse_args(); guard(a.output.parent)
    paths=[a.receipts,a.captures,a.fixed]
    before=[identity(p) for p in paths]
    samples=json.loads(a.receipts.read_text())
    captures=json.loads(a.captures.read_text())
    a.output.mkdir(parents=True,exist_ok=False)
    invariance=[]; objects=[]; projection=[]; manifests=[]; controls=[]
    for s in samples:
        manifests.append(dict(sample=s['label'],decoded_bytes=s['metrics']['declared_decoded_size'],
            decoded_sha256=s['metrics']['decoded_sha256'],selected_records=len(s['rows'])))
        if s['label']=='HIST-0245':
            for control in s['extraction'].get('player_location_control',[]):
                for pt in control['points']:
                    projection.append(dict(sample='Save2-player-site',token='400014',body=f"{pt['body_formid']:08X}",
                        **audit(pt['pair'])))
        for t in s['rows']:
            p=t['prefix']; r=t['record']; wp=t['workshop']
            if s['label'] in ('Save25','Save26'):
                pair=t['association']['points'][0]
                invariance.append(dict(sample=s['label'],token=r['token'],parent=p['parent_token'],
                    name=t['association']['name_for_comparison'][0]['text'],
                    identifier98=wp['identifier98_hex'],body=f"{pair['body_formid']:08X}",
                    longitude=pair['longitude_rad'],latitude=pair['latitude_rad'],
                    xyz=p['xyz'],xyz_hex=t['xyz_hex'],delta=t['delta'],center=t['center'],
                    center_hex=t['center_hex'],xyz_offset=r['body']+1,delta_offset=wp['delta_offset'],
                    candidate_origin=t['models'][0]['candidate_origin'],residual=t['models'][0]['residual'],
                    phase_a=t['models'][0]['centre_phase'],phase_b=t['models'][0]['corner_phase']))
            if s['label'] in ('S3','S6','S7','L2C') or (s['label']=='HIST-0267' and t['role']!='beacon' and len([v for v in objects if v['sample']=='HIST-0267'])<6):
                beacon=next((v for v in s['rows'] if v['role']=='beacon' and v['prefix']['parent_token']==p['parent_token']),None)
                fallback=next((v for v in s['rows'] if v['role']=='beacon'),None)
                anchor=beacon or fallback
                diff=[x-y for x,y in zip(p['xyz'],anchor['prefix']['xyz'])] if anchor else None
                objects.append(dict(sample=s['label'],role=t['role'],token=r['token'],parent=p['parent_token'],
                    base=p['base_token'],case=p['case'],shape=p['shape'],frame_flag=t['initial_frame_flag'],
                    xyz=p['xyz'],xyz_offset=r['body']+1,rotation_fields=t['rotations'],
                    subtraction_from_beacon=diff,same_parent_as_anchor=beacon is not None,
                    subtraction_status='same-parent reference difference' if beacon else 'frame-unqualified candidate'))
            if t.get('association'):
                for pt in t['association']['points']:
                    projection.append(dict(sample=s['label'],token=r['token'],body=f"{pt['body_formid']:08X}",
                        compensation=wp.get('delta_hex'),**audit(pt['pair'],t.get('center',p['xyz']))))
    for label in ('S1','S2','S3','S4','S5','S6','S7'):
        pair=[next(s for s in samples if s['label']==v) for v in (label,label+'C')]
        before_rows={t['role']:t for t in pair[0]['rows']}
        after_rows={t['role']:t for t in pair[1]['rows']}
        assert before_rows.keys()==after_rows.keys()
        for role,t in before_rows.items():
            z=after_rows[role]
            assert t['xyz_hex']==z['xyz_hex']
            assert [v['hex'] for v in t['rotations']]==[v['hex'] for v in z['rotations']]
        controls.append(dict(action=label,control=label+'C',roles=list(before_rows),xyz_bits_equal=True,rotation_bits_equal=True))
    for city in csv.DictReader(a.fixed.open(encoding='utf8')):
        projection.append(dict(sample=city['world_formid'],token='',body=city['body_formid'],
            **audit([float(city['longitude_rad']),float(city['latitude_rad'])])))
    player=[r for r in projection if r['sample']=='Save2-player-site']
    city=[r for r in projection if r['sample']=='0001251B']
    assert len(player)==len(city)==1
    assert (player[0]['longitude_rad'],player[0]['latitude_rad'])==(city[0]['longitude_rad'],city[0]['latitude_rad'])
    for row in invariance:
        matches=[z for z in invariance if z['identifier98']==row['identifier98']]
        assert len(matches)==2 and matches[0]['center_hex']==matches[1]['center_hex']
        assert (matches[0]['longitude'],matches[0]['latitude'])==(matches[1]['longitude'],matches[1]['latitude'])
    for c in captures:
        assert c['recovered_origin_hex'] in {r['center_hex'] for r in invariance}
    mature=next(s for s in samples if s['label']=='HIST-0267')
    mb=[r for r in mature['rows'] if r['role']=='beacon']
    assert len(mb)==19 and all(r['workshop']['delta_hex']=='00'*12 for r in mb)
    for filename,rows in [('invariance.csv',invariance),('object-transforms.csv',objects),
        ('projection.csv',projection),('decoded-inputs.csv',manifests),('controls.csv',controls)]:
        table(a.output/filename,rows)
    summary=dict(samples=len(samples),selected_records=sum(len(s['rows']) for s in samples),
        mature_roles=dict(collections.Counter(t['role'] for t in mature['rows'])),
        mature_compensations_decoded=len(mb),mature_zero_compensations=len(mb),
        captures=len(captures),control_pairs=len(controls),projection_rows=len(projection),
        max_lon_error=max(abs(r['longitude_error_rad']) for r in projection),
        max_lat_error=max(abs(r['latitude_error_rad']) for r in projection),
        before=before,after=[identity(p) for p in paths],
        conclusion='EXACT SAMPLED LOCAL INVARIANCE; CONTINUOUS GEOGRAPHIC MAPPING OPEN')
    assert summary['before']==summary['after']
    if a.session:
        terrains=[]
        for label in ('baseline-003','control-003','premove-003','moved-003','saved-003',
                      'reloaded-003','reload-control-003','visit-002','control-002'):
            folder=a.session/label
            rows=[json.loads(v) for v in (folder/'records.jsonl').read_text().splitlines()]
            raw={r['root']:r for r in rows if r['kind']=='raw' and r['root'] in ('terrain','terrain.grid','stitch.block','stitch.merge')}
            data={}
            for key,r in raw.items():
                import hashlib
                b=(folder/r['file']).read_bytes()
                if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']: raise ValueError('RAW_CAPTURE_HASH')
                data[key]=b
            b=data['terrain']; mode=int.from_bytes(b[0x20:0x24],'little')
            origin=0x1c0 if mode==3 else 0xc8
            coarse=struct.unpack_from('<2i',b,origin+4)
            sub=struct.unpack_from('<2i',b,origin+0x14)
            fine=struct.unpack_from('<2i',b,origin+0x24)
            block=struct.unpack('<i',data['stitch.block'])[0]+struct.unpack('<i',data['stitch.merge'])[0]
            resolution=struct.unpack_from('<i',data['terrain.grid'],0x50)[0]
            indices=[16*block*c+block*s+f for c,s,f in zip(coarse,sub,fine)]
            assert indices==[10464,21120] and block==12 and resolution==256
            terrains.append(dict(label=label,terrain_sha256=raw['terrain']['sha256'],mode=mode,
                origin_member_offset=hex(origin),tag=b[origin],coarse=coarse,sub=sub,fine=fine,
                block=block,resolution=resolution,indices=indices))
        table(a.output/'terrain-captures.csv',terrains)
        summary['terrain_snapshots']=len(terrains)
    write(a.output/'summary.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ('before','after')},indent=2))


if __name__=='__main__': main()
