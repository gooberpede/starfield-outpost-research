"""SPDX-License-Identifier: GPL-3.0-or-later
SOR-EXP-0014 selected evidence writer. Reads an explicit ignored extraction;
writes exclusive authored CSV/JSON to a caller directory. Stdlib only. No raw
save I/O, target/database/network/Git effects. Never infers scale or north.
"""
import argparse
import csv
import json
import math
from pathlib import Path
from research_surface_anchors import write


def compare(a, b):
    pa, pb = a['points'][0], b['points'][0]
    ua = [pa['direction_'+k] for k in 'xyz']
    ub = [pb['direction_'+k] for k in 'xyz']
    cross = [ua[1]*ub[2]-ua[2]*ub[1], ua[2]*ub[0]-ua[0]*ub[2], ua[0]*ub[1]-ua[1]*ub[0]]
    delta = [y-x for x,y in zip(a['local_xyz'], b['local_xyz'])]
    return dict(parent_tokens_equal=a['parent_token']==b['parent_token'],
                pair_bits_equal=pa['pair_hex']==pb['pair_hex'],
                body_equal=pa['body_formid']==pb['body_formid'],
                delta_xyz=delta, local_distance_unassigned_units=math.hypot(*delta),
                angular_separation_rad=math.atan2(math.hypot(*cross), sum(x*y for x,y in zip(ua,ub))),
                longitude_delta_rad=pb['longitude_rad']-pa['longitude_rad'],
                latitude_delta_rad=pb['latitude_rad']-pa['latitude_rad'])


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args()
    cases=json.loads(a.results.read_text())
    a.output.mkdir(parents=True,exist_ok=True)
    rows=[]
    for s in cases:
        if s['label'] not in ('Save25','S1','S1C','L2C'):
            continue
        for r in s['extraction']['beacons']:
            for p in r['points']:
                name=r['name_for_comparison'][0]
                rows.append(dict(sample=s['label'], label=name['text'], token=r['token'],
                    parent=r['parent_token'], record_start=r['record_start'], record_end=r['record_end'],
                    record_body=r['record']['body'], explicit_type=r['record']['explicit_type'],
                    reference_queue=r['parent_queue_offset'], name_index=name['index'], name_text_offset=name['text_offset'],
                    base_token=r['prefix']['base_token'], disabled=r['saved_disabled'],
                    flags_offset=r['prefix']['saved_flags_offset'], saved_form_flags=r['prefix']['saved_form_flags'],
                    xyz_offset=r['xyz_offset'], xyz_hex=r['xyz_hex'], x=r['local_xyz'][0],y=r['local_xyz'][1],z=r['local_xyz'][2],
                    shape=r['prefix']['shape'], rotation_present_fields=json.dumps(r['rotation_present_fields']),
                    body_formid=f"{p['body_formid']:08X}", parent_offset=p['offset'],
                    pair_offset=p['pair_offset'], repeated_parent_offset=p['repeated_parent_offset'],
                    kind=p['raw_kind'], pair_hex=p['pair_hex'], longitude_rad=p['longitude_rad'], latitude_rad=p['latitude_rad'],
                    longitude_deg=p['longitude_deg'], latitude_deg=p['latitude_deg'],
                    all_cache_offsets=';'.join(str(c['offset']) for c in r['cache']),
                    all_cache_system_body_world=';'.join(f"{c['system_id']}/{c['body_index']}/{c['source_world_token']}" for c in r['cache'])))
    with (a.output/'beacons.csv').open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    primary=next(s for s in cases if s['label']=='Save25')['extraction']['beacons']
    # Select labels only for comparison after all identities were extracted.
    first=next(r for r in primary if r['name_for_comparison'][0]['text']=='SOR-002')
    second=next(r for r in primary if r['name_for_comparison'][0]['text']=='SOR-003')
    s1=next(s for s in cases if s['label']=='S1')['extraction']['beacons'][0]
    write(a.output/'comparisons.json',dict(within_save25=compare(first,second),
        s1_to_sor002=compare(s1,first), s1_to_sor003=compare(s1,second)))
    print(json.dumps(compare(first,second),indent=2))


if __name__=='__main__':main()
