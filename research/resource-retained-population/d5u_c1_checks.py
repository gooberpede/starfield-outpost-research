# SPDX-License-Identifier: GPL-3.0-or-later
"""Check delivered coordinate joins, source coverage, geometry and SVG replay.

Reads authored data, C1 baseline and provenance receipts; hashes protected
installed/database inputs without modifying them. Runs only the authored SVG
renderer in a fresh ignored directory. Writes a new ignored check receipt.
No procedural/native generation, raw saves, game, network or Git mutations.
"""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT/'.local-work/d5u-c1'
DOC = ROOT/'docs/experiments/resource-retained-population/d5u/outposts'
NS = '{http://www.w3.org/2000/svg}'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    output = LOCAL/sys.argv[1]
    assert output.resolve().is_relative_to(LOCAL.resolve()) and not output.exists()
    output.mkdir()
    before = read(LOCAL/'initial.json')
    for category in ('installed','database'):
        assert {p:sha(p) for p in before[category]}==before[category]
    sources=list(csv.DictReader((DOC.parent.parent/'d5u-c1-sources.csv').open(encoding='utf8')))
    for source in sources:
        path=Path(source['path'])
        if source['category']=='AUTHENTICATED ARCHIVE MEMBER':
            path=ROOT/'.local-work/resources-evidence-consolidation/d5u-c1-input-lease01'/path
        elif not path.is_absolute():
            path=ROOT/path
        assert sha(path)==source['sha256'],source['path']
    preserved = [p for p in before['files'] if p.startswith('docs/experiments/resource-retained-population/d5u/')
                 and p!='docs/experiments/resource-retained-population/d5u/README.md']
    assert len(preserved)==41
    assert all(sha(ROOT/p)==before['files'][p]['sha256'] for p in preserved)
    manifest = read(DOC/'map-manifest.json')
    assert len(manifest['files'])==8
    identities,layer_count,region_count,largest_error = set(),0,0,0
    for file in manifest['files'].values():
        for panel in file['panels']:
            lo,hi = panel['extent']
            left,top,scale,size = [panel[k] for k in ('left','top','scale','size')]
            cx,cy = panel['center_pixels']
            radius = panel['radius_pixels']
            assert abs(radius/scale-150)<1e-12
            assert left<cx-radius and cx+radius<left+size and top<cy-radius and cy+radius<top+size
            def forward(p):
                return [left+(p[0]-lo)*scale,top+(hi-p[1])*scale]
            def inverse(p):
                return [(p[0]-left)/scale+lo,hi-(p[1]-top)/scale]
            assert forward([panel['center'][0],panel['center'][1]+1])[1]<cy
            for point in ([lo,lo],[hi,hi],panel['center'],[12.25,-34.5]):
                largest_error=max(largest_error,max(abs(a-b) for a,b in zip(point,inverse(forward(point)))))
        assert largest_error<1e-10
    for case in ('83388f','82be17','81a75b','81bf2a','825f95','844cc6','84e101'):
        data = read(DOC/f'D2-{case}.json')
        layers = data['layers'];reference = data['reference']
        assert reference['radius']==150 and reference['beacon']==reference['center']
        counts = Counter(v['source_id'] for v in layers)
        assert data['coverage']['total_sources']==len(counts)
        for layer in layers:
            assert layer['source_id']!='U26' and layer['variant_count']==counts[layer['source_id']]
            identities.add((data['reference']['case'],layer['source_id']))
            assert layer['origin']==[v-200 for v in layer['anchor']]
            assert [layer['anchor'][k]-reference['center'][k]+reference['center'][k] for k in (0,1)]==layer['anchor']
            for region in layer['regions']:
                region_count+=1
                assert b''.join(struct.pack('<4f',*p) for p in region['points']).hex()==region['ordered_xyzw_le']
                assert struct.pack('<4f',*region['native_bound']).hex()==region['native_bound_le']
                # Special and the zero-DNAM ordinary placeholder share an ID.
                # No Special path may leak into these ordinary-only maps.
                assert region['resource']!='000057f5'
        layer_count+=len(layers)
    assert len(identities)==34 and layer_count==40
    primary = read(DOC/'D2-83388f.json')
    assert primary['reference']['center'][:2]==[-2716.539306640625,-132.11228942871094]
    assert {v['source_id']:v['anchor'] for v in primary['layers']}=={
        'U01':[-3600,-1200],'U02':[-3600,0],'U03':[-2400,-1200],'U04':[-2400,0]}
    assert sum(len(v['regions']) for v in primary['layers'])==103
    positive = {r['resource']:v['source_id'] for v in primary['layers'] for r in v['regions']
                if r['disk_intersection'].get('intersection')=='POSITIVE_AREA'}
    assert positive=={'000057ce':'U01','000057cb':'U01','000057cf':'U02','000057d4':'U02'}
    for case,expected in [('825f95',{'000057d6','000057db'}),('81bf2a',{'000057d6','000057d8'})]:
        data=read(DOC/f'D2-{case}.json')
        assert {r['resource'] for v in data['layers'] for r in v['regions']
                if r['disk_intersection'].get('intersection')=='POSITIVE_AREA'}==expected
    replay = output/'replay'
    run = subprocess.run([sys.executable,'-B',str(Path(__file__).with_name('d5u_c1_maps.py')),
                          '--output',str(replay)],cwd=ROOT,capture_output=True)
    (output/'replay.log').write_bytes(run.stdout+run.stderr)
    assert run.returncode==0
    assert (replay/'map-manifest.json').read_bytes()==(DOC/'map-manifest.json').read_bytes()
    for name,file in manifest['files'].items():
        path=DOC/name
        assert sha(path)==file['sha256'] and path.read_bytes()==(replay/name).read_bytes()
        root=ET.parse(path).getroot()
        ids=[e.attrib['id'] for e in root.iter() if 'id' in e.attrib]
        assert len(ids)==len(set(ids)) and root.attrib['width']=='1280'
        assert root.find(NS+'title') is not None
        disks=[e for e in root.iter() if e.attrib.get('data-role')=='outpost-disk']
        assert len(disks)==2*len(file['panels'])
        for panel in file['panels']:
            matching=[e for e in disks if abs(float(e.attrib['cx'])-panel['center_pixels'][0])<1e-8
                      and abs(float(e.attrib['cy'])-panel['center_pixels'][1])<1e-8
                      and abs(float(e.attrib['r'])-panel['radius_pixels'])<1e-8]
            assert matching
    free={d:shutil.disk_usage(d).free for d in ('C:/','D:/')}
    assert min(free.values())>=40_000_000_000
    result=dict(sources=34,verified_provenance_rows=len(sources),layers=layer_count,regions=region_count,svgs=8,
                geometry_and_point_bytes='PASS',transforms_and_radius='PASS',
                max_transform_roundtrip_error=largest_error,byte_identical_svg_replay='PASS',
                preserved_D5U_science_files=len(preserved),installed_database='PASS',free=free,
                limits='Rendering success is separate from manual visual QA and independent scientific review.')
    (output/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    print(json.dumps(result))


if __name__=='__main__':
    main()
