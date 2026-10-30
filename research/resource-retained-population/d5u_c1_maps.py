# SPDX-License-Identifier: GPL-3.0-or-later
"""Render seven outpost composites and a frame diagnostic from delivered JSON.

Reads only authored C1 composite JSON and existing authored D5U geometry/palette.
Writes deterministic SVGs and their transform/hash manifest; --output requires a
fresh directory. Imports owned D5T primitive arithmetic. No asset/raw evidence,
native execution, target, save, database, dependency, network or Git operation.
Viewport clipping is deliberate and labelled; full retained geometry stays in JSON.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from d5t_maps import primitives

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT/'docs/experiments/resource-retained-population/d5u/outposts'
CASES = ['D2-'+v for v in ('83388f','82be17','81a75b','81bf2a','825f95','844cc6','84e101')]


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def text(x,y,value,size=14,extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" {extra}>{html.escape(str(value))}</text>'


def start(height,title):
    return ['<svg xmlns="http://www.w3.org/2000/svg" width="1280" '+f'height="{height}" viewBox="0 0 1280 {height}">',
            f'<title>{html.escape(title)}</title>',
            '<desc>Conditional ordinary generation-competition geometry in a saved historical descriptor frame. '
            'The black circle is the fixed 150-native-unit research boundary. No historical joint winner, terrain or final UI catalogue is asserted.</desc>',
            '<rect width="1280" height="100%" fill="#f8fafc"/>',
            '<g font-family="Segoe UI,Arial,sans-serif" fill="#182d3a">']


def finish(lines):
    result = '\n'.join(lines+['</g></svg>'])+'\n'
    ET.fromstring(result)
    return result


def panel(lines,identity,left,top,size,extent,center,radius,layers,palette,title,subtitle,
          anchors=False,geometry_on=True):
    lo,hi = extent
    scale = size/(hi-lo)
    def point(x,y):
        return left+(x-lo)*scale,top+(hi-y)*scale
    lines += [text(left,top-43,title,20,'font-weight="600"'),text(left,top-20,subtitle,12),
              f'<rect x="{left}" y="{top}" width="{size}" height="{size}" fill="white" stroke="#b7c6cd"/>',
              f'<defs><clipPath id="view-{identity}"><rect x="{left}" y="{top}" width="{size}" height="{size}"/></clipPath></defs>']
    ticks = [-200,-100,0,100,200] if extent==[-240,240] else [lo,(lo+hi)/2,hi]
    for value in ticks:
        x,y = point(value,value)
        lines += [f'<path d="M{x} {top}v{size} M{left} {y}h{size}" stroke="#e3eaee"/>',
                  text(x,top+size+22,f'{value:g}',11,'text-anchor="middle"'),
                  text(left-8,y+4,f'{value:g}',11,'text-anchor="end"')]
    lines.append(f'<g clip-path="url(#view-{identity})">')
    count = 0
    if geometry_on:
        for li,layer in enumerate(layers):
            lines.append(f'<g data-layer="{layer["id"]}">')
            for ri,region in enumerate(layer['regions']):
                color = palette[region['resource']]['rgb']
                bx,by,bz,br = region['native_bound']
                bx,by = point(bx,by)
                clip = f'{identity}-l{li}-r{ri}'
                lines += [f'<defs><clipPath id="{clip}"><circle cx="{bx:.9f}" cy="{by:.9f}" r="{max(br,.5)*scale:.9f}"/></clipPath></defs>',
                          f'<g clip-path="url(#{clip})" fill="{color}" stroke="{color}" stroke-width="0.35">']
                for shape in primitives(region['points']):
                    if shape['kind']=='disk':
                        x,y = point(*shape['center'])
                        lines.append(f'<circle cx="{x:.9f}" cy="{y:.9f}" r="{shape["radius"]*scale:.9f}"/>')
                    else:
                        coords = ' '.join(f'{x:.9f},{y:.9f}' for x,y in (point(*v) for v in shape['vertices']))
                        lines.append(f'<polygon points="{coords}"/>')
                    count += 1
                lines.append('</g>')
            lines.append('</g>')
    anchor_labels = []
    if anchors:
        for layer in {v['source_id']:v for v in layers}.values():
            ax,ay = point(*layer['anchor'])
            w,h = [100*v*scale for v in layer['nominal']]
            lines += [f'<rect x="{ax}" y="{ay-h}" width="{w}" height="{h}" fill="none" stroke="#873688" stroke-width="1.2" stroke-dasharray="5 3"/>',
                      f'<path d="M{ax-5} {ay}h10 M{ax} {ay-5}v10" stroke="#873688" stroke-width="2"/>']
            anchor_labels.append((ax,ay,layer['source_id']))
            ox,oy = point(*layer['origin'])
            lines.append(f'<path d="M{ox-3} {oy-3}l6 6 M{ox-3} {oy+3}l6 -6" stroke="#667c88"/>')
    cx,cy = point(*center)
    pixel_radius = radius*scale
    assert left<cx-pixel_radius and cx+pixel_radius<left+size
    assert top<cy-pixel_radius and cy+pixel_radius<top+size
    lines += [f'<circle data-role="outpost-disk" cx="{cx:.9f}" cy="{cy:.9f}" r="{pixel_radius:.9f}" fill="none" stroke="white" stroke-width="5"/>',
              f'<circle data-role="outpost-disk" cx="{cx:.9f}" cy="{cy:.9f}" r="{pixel_radius:.9f}" fill="none" stroke="#101e28" stroke-width="2.5"/>',
              f'<path data-role="native-center" d="M{cx-8} {cy}h16 M{cx} {cy-8}v16" stroke="white" stroke-width="5"/>',
              f'<path d="M{cx-8} {cy}h16 M{cx} {cy-8}v16" stroke="#101e28" stroke-width="2"/>',
              f'<path data-role="saved-beacon" d="M{cx} {cy-6}l6 6 -6 6 -6 -6 Z" fill="none" stroke="#101e28" stroke-width="1.5"/>']
    for ax,ay,label in anchor_labels:
        dx = pixel_radius+20 if (ax-cx)**2+(ay-cy)**2<(pixel_radius+25)**2 else 6
        lines.append(text(ax+dx,ay-8,label,11,'paint-order="stroke" stroke="white" stroke-width="3" stroke-linejoin="round"'))
    lines += ['</g>',text(left+size/2,top+size+43,'X → native units',12,'text-anchor="middle"'),
              text(left-57,top+size/2,'Y ↑',13)]
    return dict(id=identity,left=left,top=top,size=size,extent=extent,scale=scale,
                center=center,radius_native=radius,radius_pixels=pixel_radius,
                center_pixels=[cx,cy],source_ids=list(dict.fromkeys(v['source_id'] for v in layers)),
                layer_ids=[v['id'] for v in layers],primitives=count,
                deliberate_viewport_clip=geometry_on,geometry_drawn=geometry_on)


def shifted(layer,center):
    result = dict(layer)
    result['regions'] = [dict(r,points=[[p[0]-center[0],p[1]-center[1],p[2],p[3]] for p in r['points']],
                              native_bound=[r['native_bound'][0]-center[0],r['native_bound'][1]-center[1],*r['native_bound'][2:]])
                         for r in layer['regions']]
    return result


def composite(data):
    ref,layers,palette = data['reference'],data['layers'],data['palette']
    variables = list(dict.fromkeys(v['source_id'] for v in layers if v['variant_count']>1))
    height = 990+len(variables)*650
    lines = start(height,ref['name']+' — outpost composite')
    lines += [text(32,39,ref['name'],28,'font-weight="600"'),
              text(32,67,f"{ref['case']} · build 1.16.244.0 · chart {ref['chart']} · fixed main definitions",15),
              text(32,93,'Conditional historical-frame ordinary model · historical winner / loaded epoch UNKNOWN',16),
              text(32,118,'Saved native centre '+str(ref['center'])+' · radius 150 native units',13),
              text(32,142,'Saved beacon coincides by zero Workshop compensation. This is a research disk; terrain and final UI availability are not shown.',13)]
    fixed = [shifted(v,ref['center']) for v in layers if v['variant_count']==1]
    contributors = [v['source_id'] for v in fixed if any(r['disk_intersection'].get('intersection')=='POSITIVE_AREA' for r in v['regions'])]
    subtitle = 'Positive disk area: '+(', '.join(contributors) if contributors else 'none in invariant layers')+'.'
    panels = [panel(lines,'fixed',90,210,480,[-240,240],[0,0],150,fixed,palette,
                    'Invariant-source composite',subtitle)]
    bounds = [-200,200]
    for layer in layers:
        for k in (0,1):
            bounds += [layer['origin'][k]-ref['center'][k]-100,
                       layer['anchor'][k]+100*layer['nominal'][k]-ref['center'][k]+100]
    extent = [math_floor(min(bounds),200),math_ceil(max(bounds),200)]
    layout_layers = [dict(v,anchor=[v['anchor'][k]-ref['center'][k] for k in (0,1)],
                         origin=[v['origin'][k]-ref['center'][k] for k in (0,1)]) for v in layers]
    panels.append(panel(lines,'layout',760,210,400,extent,[0,0],150,layout_layers,palette,
                        'All source anchors and nominal boxes','Purple +: source anchor. Gray ×: generator origin (anchor −200).',True,False))
    lines += [text(760,675,'Source layout only; boxes are not deposits.',13),
              text(760,698,'No source anchor is assumed to be the outpost centre.',13),
              text(760,721,f"{data['coverage']['total_sources']} halo sources · {len(layers)} independent layers",13),
              text(32,765,'Black circle: fixed 150-unit disk. Cross: saved native centre. Diamond: saved beacon in the same representation.',14),
              text(32,789,'All zoom panels use X right / Y up, centre (0,0), ±240 native units, and 1 pixel per native unit.',13),
              text(32,813,'Viewport clipping outside the zoom is deliberate; the entire disk is visible. Full exact points/bounds remain in the case JSON.',13)]
    colors = list(dict.fromkeys(r['resource'] for v in layers for r in v['regions']))
    for i,res in enumerate(colors):
        x,y = 32+(i%5)*245,846+(i//5)*24
        lines += [f'<rect x="{x}" y="{y-13}" width="17" height="15" fill="{palette[res]["rgb"]}"/>',
                  text(x+25,y,palette[res]['name']+' · IRES',12)]
    notes = {
        'D2-83388f':'Observed historically: Copper, Cobalt, Nickel, Ionic Liquids. All four have positive modeled disk area from U01/U02.',
        'D2-82be17':'Disk area: Rothicite / Iron / Alkanes from U08. Historical equipment is independent presence evidence.',
        'D2-81a75b':'Disk area: Tungsten / Chlorine from U09; additional Chlorine from U11. Water uses a separate route.',
        'D2-81bf2a':'Disk area: Aluminum / Beryllium from U15. Special Helium-3 is excluded from this ordinary map.',
        'D2-825f95':'Disk area: Aluminum / Neodymium from C1-X06. U17/U18 have no positive-area disk contribution.',
        'D2-844cc6':'Invariant disk area: Antimony / Fluorine / Copper from C1-X08. Gold appears in U20-M3 below.',
        'D2-84e101':'No invariant disk overlap. U25-M0 and U25-M3 below each intersect for Ionic Liquids / Fluorine / Copper.'}
    lines += [text(32,888,notes[ref['case']],14),
              text(32,914,'Resource colors follow IRES TINC; draw order does not define resource dominance. Marginal native rounding is approximate.',13),
              text(32,938,'Special Helium-3, Water admission, atmosphere, terrain and other catalogue routes are outside this ordinary comparison.',13),
              text(32,962,'Historical availability is independent evidence; see the reconciliation report. No Cartesian combination of variants is asserted.',13)]
    for i,identity in enumerate(variables):
        pair = [v for v in layers if v['source_id']==identity]
        assert len(pair)==2
        top = 1050+i*650
        for j,layer in enumerate(pair):
            positives = sum(r['disk_intersection'].get('intersection')=='POSITIVE_AREA' for r in layer['regions'])
            panels.append(panel(lines,layer['id'],90+640*j,top,480,[-240,240],[0,0],150,
                                [shifted(layer,ref['center'])],palette,
                                f"{identity} alone · ordinary mask {layer['mask']}",
                                f"{layer['source_key']} · {len(layer['regions'])} paths · {positives} positive in disk"))
        lines += [text(32,top+556,'Conditional source contribution alternatives in the common outpost frame; other source geometries are omitted from these panels.',13),
                  text(32,top+580,'These panels do not establish a historical winner or a jointly achievable combination with another variable source.',13)]
    return finish(lines),panels,height


def math_floor(value,step):
    return int(value//step)*step


def math_ceil(value,step):
    return -int(-value//step)*step


def diagnostic(primary,prospective):
    old = next(v for v in primary['layers'] if v['source_id']=='U01')
    old_relative = shifted(old,old['anchor'])
    new = next(v for v in prospective['outcomes'] if v['source_id']=='U01' and v['mask']==8)
    new_layer = dict(id='U01-prospective-M8',source_id='U01',regions=[dict(r,points=r['points_xyz_width']) for r in new['regions']])
    center = [primary['reference']['center'][k]-old['anchor'][k] for k in (0,1)]
    lines = start(1060,'U01 coordinate join: historical frame versus normalized prospective generation')
    lines += [text(32,36,'U01 · a coordinate join does not preserve a procedural seed',27),
              text(32,66,'Feynman V Cu Co Ni IL · source 0:25116:32436:0029d20d · build 1.16.244.0',15),
              text(32,94,'Both panels use the source anchor as (0,0), generator origin (−200,−200), X right / Y up and the same scale.',14),
              text(32,119,'The 150-unit circle is the same historical reference disk. Only the left geometry uses the historical descriptor frame.',14)]
    panels = []
    for j,layer in enumerate((old_relative,new_layer)):
        panels.append(panel(lines,f'diagnostic-{j}',80+640*j,205,500,[-500,1450],center,150,[layer],primary['palette'],
                            ['Historical-frame conditional model','Normalized prospective native execution'][j],
                            ['Descriptor (25152,32448); original generator origin (−3800,−1400)',
                             'Descriptor (25116,32436); original generator origin (−200,−200)'][j]))
    lines += [text(32,785,'Left: 30 retained paths. Right: 28 retained paths. Equal display origins do not make these populations interchangeable.',15),
              text(32,815,'Historical native centre = (−2716.539306640625, −132.11228942871094). U01 anchor = (−3600, −1200).',14),
              text(32,845,'Historical source-relative centre = (883.460693359375, 1067.887710571289). Its circle is a reference on the prospective panel.',14),
              text(32,875,'Packed-key cell (1,1): historical seed XY (21353,31049); prospective seed XY (24917,32237). No /100 correction is applied.',14),
              text(32,905,'The map transform is reversible: native point = source-relative point + source anchor; outpost-relative point = native point − centre.',14),
              text(32,935,'Black circle / cross / diamond: historical research disk, saved native centre and saved beacon. Native points/bounds stay exact in JSON.',13),
              text(32,965,'Resource colors: IRES TINC. Competition footprint reconstruction approximates marginal native floating-point boundaries.',13),
              text(32,995,'The left model is not an observed full historical source population. Four independent primary callback paths match native evidence.',13)]
    for i,resource in enumerate(('000057ce','000057cb')):
        x = 32+i*270
        lines += [f'<rect x="{x}" y="1020" width="18" height="15" fill="{primary["palette"][resource]["rgb"]}"/>',
                  text(x+26,1033,primary['palette'][resource]['name']+' · IRES TINC',13)]
    return finish(lines),panels,1060


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    output = args.output or DATA
    if args.output:
        output.mkdir(parents=True,exist_ok=False)
    manifest = dict(schema='sor-d5u-c1-svg/1',files={})
    primary = None
    for case in CASES:
        data = read(DATA/f'{case}.json')
        svg,panels,height = composite(data)
        (output/f'{case}.svg').write_text(svg,encoding='utf8',newline='\n')
        manifest['files'][case+'.svg'] = dict(sha256=hashlib.sha256(svg.encode()).hexdigest(),
                                            width=1280,height=height,data=case+'.json',panels=panels)
        if case=='D2-83388f':
            primary = data
    svg,panels,height = diagnostic(primary,read(DATA.parent/'geometry.json'))
    (output/'coordinate-join.svg').write_text(svg,encoding='utf8',newline='\n')
    manifest['files']['coordinate-join.svg'] = dict(sha256=hashlib.sha256(svg.encode()).hexdigest(),
                                                  width=1280,height=height,data='D2-83388f.json + ../geometry.json',panels=panels)
    (output/'map-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8',newline='\n')
    print('Rendered eight deterministic SVGs from delivered data; full 150-unit circles are inside every viewport.')


if __name__=='__main__':
    main()
