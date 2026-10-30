# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify absolute native axes and preserved D5V science without native execution.

Reads correction baseline, supplied geometry, saved-centre controls and SVGs.
Replays the owned renderer into fresh ignored scratch; writes only a new check
receipt. No game, raw save, database, network, installed write or Git mutation.
"""
from pathlib import Path
import csv
import hashlib
import json
import math
import shutil
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT/'.local-work/d5v-c1'
DOC=ROOT/'docs/experiments/resource-retained-population'
NS='{http://www.w3.org/2000/svg}'


def sha(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def read(path):return json.loads(Path(path).read_text(encoding='utf8'))


def rows(path):
    with Path(path).open(encoding='utf8') as stream:return list(csv.DictReader(stream))


def main():
    output=LOCAL/sys.argv[1];assert output.parent==LOCAL and not output.exists();output.mkdir()
    assert min(shutil.disk_usage(d).free for d in ('C:/','D:/'))>=40_000_000_000
    initial=read(LOCAL/'initial.json');baseline=LOCAL/'baseline'
    for p,h in initial['geometry'].items():assert sha(ROOT/p)==h
    for name in ('d5v/consumer-results.csv','d5v/coordinates.csv','d5v/lifecycle.svg',
                 'd5v-lifecycle-consumer-map.md','d5v-sources.csv'):
        p=DOC/name;assert p.read_bytes()==(baseline/p.relative_to(ROOT)).read_bytes(),name
    for name in ('d5v_native.py',):
        p=ROOT/'research/resource-retained-population'/name
        assert p.read_bytes()==(baseline/p.relative_to(ROOT)).read_bytes()
    old=read(baseline/'docs/experiments/resource-retained-population/d5v/spatial.json')
    current=read(DOC/'d5v/spatial.json');assert current['schema']=='sor-d5v-spatial/2'
    assert old['inputs']==current['inputs']
    frames={r['token']:r for r in rows(ROOT/'docs/experiments/static-exhaustion/saved-center-frame.csv') if r['sample']=='HIST-0267'}
    projections={r['token']:r for r in rows(ROOT/'docs/experiments/durable-center/projection.csv') if r['sample']=='HIST-0267'}
    results=[];largest=0;rounded_largest=0
    for case,case_data in current['cases'].items():
        assert case_data['reference']==old['cases'][case]['reference']
        assert case_data['consumer']==old['cases'][case]['consumer']
        assert case_data['source_geometry_sha256']==old['cases'][case]['source_geometry_sha256']
        geometry=read(ROOT/case_data['source_geometry']);ref=geometry['reference'];center=ref['center'][:2]
        f,p=frames[ref['beacon_token']],projections[ref['beacon_token']]
        local=[float(p['local_'+a]) for a in 'xyz'];assert struct.pack('<3f',*local).hex()==f['center_hex']
        expected=[struct.unpack('<f',struct.pack('<f',local[k]+100*(int(f['site_'+a])-int(f['origin_'+a]))))[0] for k,a in enumerate('xy')]
        assert center==expected==ref['beacon'][:2] and p['compensation']=='00'*12
        root=ET.fromstring((DOC/'d5v'/f'{case}.svg').read_text(encoding='utf8'))
        ticks={axis:[e for e in root.iter(NS+'text') if e.attrib.get('data-role')==f'native-{axis}-tick'] for axis in 'xy'}
        center_labels=[e.text for e in root.iter(NS+'text') if e.attrib.get('data-role')=='native-center-label']
        assert len(center_labels)==4 and all(f'{center[0]:.3f}' in t and f'{center[1]:.3f}' in t for t in center_labels)
        panels=case_data['panels'];assert len(panels)==4
        assert panels[0]['bounds_native']==panels[1]['bounds_native']
        assert panels[2]['bounds_native']==panels[3]['bounds_native']
        for panel in panels:
            xmin,xmax,ymin,ymax=panel['bounds_native'];scale=panel['scale'];left,top,size=[panel[k] for k in ('left','top','size')]
            assert panel['center']==panel['beacon']==center and center!=[0,0]
            assert panel['coordinate_domain']=='historical native descriptor-frame XY'
            def forward(q):return [left+(q[0]-xmin)*scale,top+(ymax-q[1])*scale]
            def inverse(q):return [xmin+(q[0]-left)/scale,ymax-(q[1]-top)/scale]
            assert forward(center)==panel['center_pixels']
            assert math.isclose(panel['radius_pixels']/scale,150,abs_tol=1e-12)
            cases=[('centre',center),('beacon',ref['beacon'][:2])]
            cases += [('cardinal',[center[0]+dx,center[1]+dy]) for dx,dy in ((150,0),(-150,0),(0,150),(0,-150))]
            cases += [('corner',[x,y]) for x in (xmin,xmax) for y in (ymin,ymax)]
            for layer in geometry['layers']:
                if layer['id'] not in panel['layer_ids']:continue
                for region in layer['regions']:
                    cases.append(('bound',region['native_bound'][:2]))
                    cases += [('deposit',q[:2]) for q in region['points']]
                    if '-full-' in panel['id']:
                        x,y,_,r=region['native_bound'];r=max(r,.5)
                        assert xmin<x-r and x+r<xmax and ymin<y-r and y+r<ymax
            for kind,q in cases:
                pixels=forward(q);back=inverse(pixels)
                err=max(abs(back[k]-q[k]) for k in (0,1));largest=max(largest,err)
                rounded=[round(v,9) for v in pixels];err2=max(abs(inverse(rounded)[k]-q[k]) for k in (0,1))
                rounded_largest=max(rounded_largest,err2)
                assert err<1e-9 and err2 <= 0.5001e-9/scale+1e-9,(case,kind,err,err2)
            for axis in 'xy':
                values=panel['ticks_'+axis];assert len(values)>=3
                for value in values:
                    target=([forward([value,ymin])[0],top+size+22] if axis=='x'
                            else [left-8,forward([xmin,value])[1]+4])
                    assert any(e.text==f'{value:g}' and float(e.attrib['data-native'])==value
                               and abs(float(e.attrib['x'])-target[0])<1e-8
                               and abs(float(e.attrib['y'])-target[1])<1e-8 for e in ticks[axis])
            circles=[e for e in root.iter(NS+'circle') if e.attrib.get('data-role')=='outpost-disk'
                     and abs(float(e.attrib['cx'])-panel['center_pixels'][0])<1e-8
                     and abs(float(e.attrib['cy'])-panel['center_pixels'][1])<1e-8]
            assert len(circles)==2
            for e in circles:
                assert float(e.attrib['data-native-x'])==center[0] and float(e.attrib['data-native-y'])==center[1]
                assert abs(float(e.attrib['r'])/scale-150)<1e-8
            group=next(e for e in root.iter(NS+'g') if e.attrib.get('id')==panel['id'])
            for role in ('native-center','saved-beacon'):
                marker=next(e for e in group.iter(NS+'path') if e.attrib.get('data-role')==role)
                assert float(marker.attrib['data-native-x'])==center[0] and float(marker.attrib['data-native-y'])==center[1]
            # Independently join original region bounds to actual SVG clip circles.
            selected=[v for v in geometry['layers'] if v['id'] in panel['layer_ids']]
            for li,layer in enumerate(selected):
                regions=layer['regions']
                if case=='D2-83388f' and panel['id'].endswith('-1'):
                    regions=[r for r in regions if r['ordinary_callback']['accepted']]
                for ri,r in enumerate(regions):
                    clip=next(e for e in group.iter(NS+'clipPath') if e.attrib['id']==f'{panel["id"]}-l{li}-r{ri}')
                    e=next(clip.iter(NS+'circle'));bound=r['native_bound'];expected_pixel=forward(bound[:2])
                    assert abs(float(e.attrib['cx'])-expected_pixel[0])<1e-8
                    assert abs(float(e.attrib['cy'])-expected_pixel[1])<1e-8
                    assert abs(float(e.attrib['r'])-max(bound[3],.5)*scale)<1e-8
            results.append(dict(case=case,panel=panel['id'],native_center=center,bounds_native=panel['bounds_native'],
                                ticks_x=panel['ticks_x'],ticks_y=panel['ticks_y'],points_checked=len(cases),scale=scale))
    subprocess.run([sys.executable,'-B',str(ROOT/'research/resource-retained-population/d5v_maps.py'),str(output/'replay')],check=True)
    for p in (output/'replay').iterdir():assert p.read_bytes()==(DOC/'d5v'/p.name).read_bytes(),p.name
    for name,h in current['diagrams'].items():assert sha(DOC/'d5v'/name)==h
    assert sha(ROOT/'.git/index')==initial['index']
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()==initial['head']
    result=dict(schema='sor-d5v-c1-checks/1',panels=results,max_roundtrip_native_error=largest,
                max_serialized_pixel_roundtrip_native_error=rounded_largest,
                numerical_tolerance_native=1e-9,pixel_serialization_places=9,
                serialized_tolerance='0.5001e-9 / pixels_per_native_unit + 1e-9 native units',
                scientific_inputs_and_consumer_outputs='byte/field unchanged',
                saved_center_joins=2,svg_replay='byte identical',lifecycle='byte unchanged',
                checks_script_sha256=sha(__file__),renderer_sha256=sha(ROOT/'research/resource-retained-population/d5v_maps.py'))
    (output/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k!='panels'},indent=2))


if __name__=='__main__':main()
