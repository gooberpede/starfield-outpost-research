"""SPDX-License-Identifier: GPL-3.0-or-later
EXP0021 adapter for existing frozen EXP0020 extraction receipts, not a save parser.
Reads samples/component/descriptor/frame tables; writes NEW selected input and
prediction JSON files plus SHA receipts. Stdlib/project only, 40GB guard. Never
reads prior center/cell expected values as model inputs; site indices are the
qualified upstream saved-anchor quantization (explicit scope boundary).
"""
import argparse
import csv
import json
from pathlib import Path

from durable_position_model import EXE_SHA, reconstruct
from inventory_historical_saves import guard, identity


def prepare(samples, components, descriptors, frames, output):
    guard(output.parent)
    paths=[samples,components,descriptors,frames]
    before=[identity(p) for p in paths]
    def rows(p):
        with p.open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
    comps,descs,frs=map(rows,(components,descriptors,frames))
    inputs=[]
    for sample in json.loads(samples.read_text(encoding='utf8')):
        for b in sample['rows']:
            if b['role']!='beacon':continue
            matching=[r for r in frs if r['sample']==sample['label'] and r['token']==b['prefix']['self_token']]
            if not matching:continue
            if len(matching)!=1:raise ValueError('FRAME_NOT_UNIQUE')
            fr=matching[0]
            if fr['disabled']=='True':continue
            cs=[r for r in comps if r['sample']==sample['label'] and r['world']==b['prefix']['parent_token']]
            if len(cs)!=1:raise ValueError('COMPONENT_NOT_UNIQUE')
            co=cs[0]
            ds=[r for r in descs if r['sample']==sample['label'] and r['world_token']==co['secondary']]
            if len(ds)!=1 or ds[0]['body']!=co['body']:raise ValueError('DESCRIPTOR_NOT_UNIQUE')
            de=ds[0]
            if any(f"{p['body_formid']:08X}"!=co['body'] for p in b['association']['points']):
                raise ValueError('SITE_BODY_MISMATCH')
            site=None if not fr['site_tag'] else [int(fr[k]) for k in ('site_tag','site_x','site_y')]
            inputs.append(dict(schema='sor-position/1',exe_sha256=EXE_SHA,
                source=dict(sample=sample['label'],decoded_sha256=sample['metrics']['decoded_sha256'],
                            record_offset=b['record']['offset'],evidence='SOR-EV-0028; framed case5 / Workshop bc / typed world-component join'),
                identity=dict(body=co['body'],saved_reference=b['prefix']['self_token'],
                              parent=co['world'],secondary=co['secondary'],workshop_id=b['workshop']['identifier98_hex']),
                frame=b['initial_frame_flag'],position_hex=b['xyz_hex'],compensation_hex=b['workshop']['delta_hex'],
                descriptor=dict(key=de['key'],body=de['body'],world_token=de['world_token'],
                                system_id=int(co['system_id']),body_index=int(co['body_index'])),site_cell=site))
    predictions=[reconstruct(i) for i in inputs]
    if before != [identity(p) for p in paths]:raise ValueError('INPUT_CHANGED')
    output.mkdir(exist_ok=False)
    for name,value in [('inputs',inputs),('predictions',predictions),('receipt',dict(inputs=before,
            cases=len(inputs),validation='STATIC/REPRODUCER; zero new engine oracle observations'))]:
        (output/(name+'.json')).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n',encoding='utf8',newline='\n')
    return len(inputs)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('samples','components','descriptors','frames','output'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args()
    print('Selected cases:',prepare(a.samples,a.components,a.descriptors,a.frames,a.output))
