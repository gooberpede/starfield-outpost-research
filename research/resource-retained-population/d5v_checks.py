# SPDX-License-Identifier: GPL-3.0-or-later
"""Check D5V native receipts, independent coordinate controls and SVG replay.

Reads existing authored geometry/CSV and D5V local evidence. Runs only the owned
SVG renderer; writes a fresh ignored check directory and authored source/consumer
tables. No native execution, game, saves, database edits, downloads or Git writes.
"""
from pathlib import Path
from collections import Counter,defaultdict
import csv
import hashlib
import json
import shutil
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT/'.local-work/d5v'
DOC=ROOT/'docs/experiments/resource-retained-population'


def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def read(path):return json.loads(Path(path).read_text(encoding='utf8'))


def rows(path):
    with Path(path).open(encoding='utf8',newline='') as stream:return list(csv.DictReader(stream))


def table(path,items,fields):
    with Path(path).open('w',encoding='utf8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerows(items)


def main():
    output=LOCAL/sys.argv[1];assert output.parent==LOCAL and not output.exists();output.mkdir()
    assert min(shutil.disk_usage(d).free for d in ('C:/','D:/'))>=40_000_000_000
    native=read(LOCAL/'native05.json')
    assert native['code_sha256']==sha(ROOT/'research/resource-retained-population/d5v_native.py')
    assert native['passed']==len(native['rows'])==606
    assert len(native['point_rows'])==606
    for p,h in native['inputs'].items():assert sha(ROOT/p)==h,p
    branch_counts=Counter(v['expected']['branch'] for v in native['rows'])
    assert {'edge_3d_radius','all_strips_rejected','vertex_xy_radius_height',
            'quad_xy_containment','single_point_broadphase','zero_points','broadphase_rejected'}<=branch_counts.keys()
    assert all(v['native_accepted']==v['expected']['accepted'] for v in native['rows'])
    for v in native['rows']:
        payload=struct.pack('<4f',*v['bound'])+b''.join(struct.pack('<4f',*p) for p in v['points'])
        assert hashlib.sha256(payload).hexdigest()==v['geometry_sha256']
    points={v['label']:v for v in native['point_rows']}
    assert points['area-versus-point']['native_area'] and not points['area-versus-point']['native_point']
    assert points['one-point-height-independent']['native_point']
    frame={r['token']:r for r in rows(ROOT/'docs/experiments/static-exhaustion/saved-center-frame.csv') if r['sample']=='HIST-0267'}
    projection={r['token']:r for r in rows(ROOT/'docs/experiments/durable-center/projection.csv') if r['sample']=='HIST-0267'}
    consumers=[];coordinates=[];max_error=0
    for case in ('D2-83388f','D2-84e101'):
        data=read(DOC/'d5u/outposts'/f'{case}.json');ref=data['reference']
        f,p=frame[ref['beacon_token']],projection[ref['beacon_token']]
        local=[float(p['local_'+a]) for a in 'xyz']
        assert struct.pack('<3f',*local).hex()==f['center_hex']
        assert p['compensation']=='00'*12
        center=[struct.unpack('<f',struct.pack('<f',local[k]+100*(int(f['site_'+a])-int(f['origin_'+a]))))[0] for k,a in enumerate('xy')]+[local[2]]
        assert center==ref['center']==ref['beacon']
        for layer in data['layers']:
            area,point=Counter(),Counter()
            for n,r in enumerate(layer['regions']):
                label=f'{case}/{layer["id"]}/{n}'
                witness=next(v for v in native['rows'] if v['label']==label)
                expected_bytes=bytes.fromhex(r['native_bound_le']+r['ordered_xyzw_le'])
                assert hashlib.sha256(expected_bytes).hexdigest()==witness['geometry_sha256']
                assert witness['native_accepted']==r['ordinary_callback']['accepted']
                if witness['native_accepted']:area[r['resource']]+=1
                if points[label]['native_point']:point[r['resource']]+=1
            for resource in sorted({r['resource'] for r in layer['regions']}):
                consumers.append(dict(case=case,layer=layer['id'],mask=layer['mask'],resource=resource,
                                      name=data['palette'][resource]['name'],area_accepted_regions=area[resource],
                                      point_accepted_regions=point[resource],query_frame='qualified historical descriptor frame',
                                      classification='ESTABLISHED (executed), supplied model geometry; not gameplay'))
            for k in (0,1):
                assert layer['origin'][k]==layer['anchor'][k]-200
            coordinates.append(dict(case=case,layer=layer['id'],center_x=center[0],center_y=center[1],
                                    anchor_x=layer['anchor'][0],anchor_y=layer['anchor'][1],
                                    origin_x=layer['origin'][0],origin_y=layer['origin'][1],radius=150))
        for x,y in [center[:2],[-2716.5,-132.1],[81.25,90.5],[-240,240]]:
            px,py=80+(x-center[0]+240),225+(240-(y-center[1]))
            back=[center[0]+px-80-240,center[1]+240-py+225]
            max_error=max(max_error,abs(back[0]-x),abs(back[1]-y))
    assert max_error<1e-10
    table(DOC/'d5v/consumer-results.csv',consumers,list(consumers[0]))
    table(DOC/'d5v/coordinates.csv',coordinates,list(coordinates[0]))
    subprocess.run([sys.executable,'-B',str(ROOT/'research/resource-retained-population/d5v_maps.py'),str(output/'maps')],check=True)
    for p in (output/'maps').iterdir():assert p.read_bytes()==(DOC/'d5v'/p.name).read_bytes(),p.name
    svg_checks=[]
    manifest=read(DOC/'d5v/spatial.json')
    ns='{http://www.w3.org/2000/svg}'
    for name,expected in manifest['diagrams'].items():
        p=DOC/'d5v'/name;assert sha(p)==expected
        tree=ET.fromstring(p.read_text(encoding='utf8'))
        for circle in tree.iter(ns+'circle'):
            if circle.attrib.get('data-role')=='outpost-disk':
                panels=manifest['cases'][name.removesuffix('.svg')]['panels']
                assert any(abs(float(circle.attrib['cx'])-p['center_pixels'][0])<1e-8
                           and abs(float(circle.attrib['cy'])-p['center_pixels'][1])<1e-8
                           and abs(float(circle.attrib['r'])/p['scale']-150)<1e-8 for p in panels)
        svg_checks.append(name)
    initial=read(LOCAL/'initial.json')
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==initial['head']
    assert sha(ROOT/'.git/index')==initial['index']
    result=dict(native_comparisons=606,point_executions=606,branches=dict(branch_counts),
                native_receipt_sha256=sha(LOCAL/'native05.json'),coordinate_roundtrip_max_error=max_error,
                frame_tables_verified=2,svg_replay='byte identical',svg_files=svg_checks,head_index_unchanged=True,
                limits='Per-resource/per-region tests; no multi-entry native scan, live history or allocator failure qualification')
    (output/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
