# SPDX-License-Identifier: GPL-3.0-or-later
"""Render D5V conditional native-frame comparisons from preserved C1 data.

Reads authored C1 geometry; writes SVGs and numerical
backing data to the supplied fresh directory. Uses owned C1 plotting primitives.
No regeneration, proprietary extraction, target, save, database or network use.
"""
from pathlib import Path
from collections import Counter
import hashlib
import html
import json
import math
import sys
import xml.etree.ElementTree as ET
from d5u_c1_maps import text, finish
from d5t_maps import primitives

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'docs/experiments/resource-retained-population/d5u/outposts'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def start(title,height=1030):
    return ['<svg xmlns="http://www.w3.org/2000/svg" width="1280" '
            f'height="{height}" viewBox="0 0 1280 {height}">',
            f'<title>{html.escape(title)}</title>',
            '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8Z" fill="#466a82"/></marker></defs>',
            '<rect width="1280" height="100%" fill="#f8fafc"/>',
            '<g font-family="Segoe UI,Arial,sans-serif" fill="#182d3a">',
            text(32,42,title,26,'font-weight="600"')]


def schematic(title,boxes,edges,footer):
    lines=start(title,810)
    for identity,x,y,w,h,label in boxes:
        lines.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="white" stroke="#708da0"/>')
        for n,s in enumerate(label):
            lines.append(text(x+15,y+27+n*24,s,16))
    for x1,y1,x2,y2,label in edges:
        lines.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="#466a82" stroke-width="2" marker-end="url(#arrow)"/>')
        if label:
            label_y = y1-65 if y1==y2 else (y1+y2)/2-8
            label_x = x1+12 if x1==x2 else (x1+x2)/2
            anchor = 'start' if x1==x2 else 'middle'
            lines.append(text(label_x,label_y,label,12,
                              f'text-anchor="{anchor}" paint-order="stroke" stroke="#f8fafc" stroke-width="4"'))
    for n,s in enumerate(footer):lines.append(text(32,710+n*25,s,15))
    return finish(lines)


def native_panel(lines,identity,left,top,size,bounds,center,radius,layers,palette,title,subtitle):
    """Plot unchanged descriptor-frame values; only the viewport maps to pixels."""
    xmin,xmax,ymin,ymax=bounds
    scale=size/(xmax-xmin)
    assert abs((ymax-ymin)-(xmax-xmin))<1e-9
    def point(x,y):return left+(x-xmin)*scale,top+(ymax-y)*scale
    lines += [text(left,top-43,title,19,'font-weight="600"'),text(left,top-20,subtitle,12),
              f'<rect x="{left}" y="{top}" width="{size}" height="{size}" fill="white" stroke="#b7c6cd"/>',
              f'<defs><clipPath id="view-{identity}"><rect x="{left}" y="{top}" width="{size}" height="{size}"/></clipPath></defs>']
    span=xmax-xmin
    step=100 if span<=600 else 10**math.floor(math.log10(span/4))
    while span/step>7:step*=2
    ticks=[]
    for axis,lo,hi in [('x',xmin,xmax),('y',ymin,ymax)]:
        values=[k*step for k in range(math.ceil(lo/step),math.floor(hi/step)+1)]
        ticks.append(values)
        for value in values:
            if axis=='x':
                x,_=point(value,ymin)
                lines += [f'<path d="M{x:.9f} {top}v{size}" stroke="#e3eaee"/>',
                          f'<text data-role="native-x-tick" data-native="{value}" x="{x:.9f}" y="{top+size+22}" font-size="11" text-anchor="middle">{value:g}</text>']
            else:
                _,y=point(xmin,value)
                lines += [f'<path d="M{left} {y:.9f}h{size}" stroke="#e3eaee"/>',
                          f'<text data-role="native-y-tick" data-native="{value}" x="{left-8}" y="{y+4:.9f}" font-size="11" text-anchor="end">{value:g}</text>']
    lines.append(f'<g data-role="native-panel" data-frame="historical-native-descriptor-xy" id="{identity}" clip-path="url(#view-{identity})">')
    count=0
    for li,layer in enumerate(layers):
        lines.append(f'<g data-layer="{layer["id"]}">')
        for ri,region in enumerate(layer['regions']):
            color=palette[region['resource']]['rgb']
            bx,by,_,br=region['native_bound'];px,py=point(bx,by);clip=f'{identity}-l{li}-r{ri}'
            lines += [f'<defs><clipPath id="{clip}"><circle cx="{px:.9f}" cy="{py:.9f}" r="{max(br,.5)*scale:.9f}"/></clipPath></defs>',
                      f'<g clip-path="url(#{clip})" fill="{color}" stroke="{color}" stroke-width="0.35">']
            for shape in primitives(region['points']):
                if shape['kind']=='disk':
                    x,y=point(*shape['center'])
                    lines.append(f'<circle cx="{x:.9f}" cy="{y:.9f}" r="{shape["radius"]*scale:.9f}"/>')
                else:
                    coords=' '.join(f'{x:.9f},{y:.9f}' for x,y in (point(*v) for v in shape['vertices']))
                    lines.append(f'<polygon points="{coords}"/>')
                count+=1
            lines.append('</g>')
        lines.append('</g>')
    cx,cy=point(*center);pr=radius*scale
    assert left<cx-pr and cx+pr<left+size and top<cy-pr and cy+pr<top+size
    attrs=f'data-native-x="{center[0]}" data-native-y="{center[1]}"'
    lines += [f'<circle data-role="outpost-disk" {attrs} cx="{cx:.9f}" cy="{cy:.9f}" r="{pr:.9f}" fill="none" stroke="white" stroke-width="5"/>',
              f'<circle data-role="outpost-disk" {attrs} cx="{cx:.9f}" cy="{cy:.9f}" r="{pr:.9f}" fill="none" stroke="#101e28" stroke-width="2.5"/>',
              f'<path data-role="native-center" {attrs} d="M{cx-8:.9f} {cy:.9f}h16 M{cx:.9f} {cy-8:.9f}v16" stroke="white" stroke-width="5"/>',
              f'<path d="M{cx-8:.9f} {cy:.9f}h16 M{cx:.9f} {cy-8:.9f}v16" stroke="#101e28" stroke-width="2"/>',
              f'<path data-role="saved-beacon" {attrs} d="M{cx:.9f} {cy-6:.9f}l6 6 -6 6 -6 -6 Z" fill="none" stroke="#101e28" stroke-width="1.5"/>','</g>',
              text(cx+10,cy-12,f'C ({center[0]:.3f}, {center[1]:.3f})',11,
                   'data-role="native-center-label" paint-order="stroke" stroke="white" stroke-width="4"'),
              text(left+size/2,top+size+43,'Native descriptor-frame X (native units)',12,'text-anchor="middle"'),
              f'<text x="{left-64}" y="{top+size/2}" font-size="12" text-anchor="middle" transform="rotate(-90 {left-64} {top+size/2})">Native descriptor-frame Y (native units)</text>',
              text(left,top+size+65,f'Centre / saved beacon: ({center[0]:.3f}, {center[1]:.3f})',12)]
    return dict(id=identity,left=left,top=top,size=size,bounds_native=bounds,scale=scale,
                coordinate_domain='historical native descriptor-frame XY',center=center,beacon=center,
                center_pixels=[cx,cy],radius_native=radius,radius_pixels=pr,ticks_x=ticks[0],ticks_y=ticks[1],
                layer_ids=[v['id'] for v in layers],primitives=count,
                deliberate_viewport_clip=True,geometry_drawn=True)


def main():
    out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=False)
    summary={'schema':'sor-d5v-spatial/2','classification':'Conditional historical-frame native model',
             'inputs':{},'cases':{},'diagrams':{},'native_vs_display':'Public data and axes are absolute native descriptor-frame XY. Viewport translation, scale and SVG Y inversion affect pixels only.'}
    for case in ('D2-83388f','D2-84e101'):
        source=DATA/f'{case}.json';data=json.loads(source.read_text(encoding='utf8'))
        summary['inputs'][str(source.relative_to(ROOT))]=sha(source)
        ref=data['reference'];layers=data['layers'];palette=data['palette']
        if case=='D2-83388f':
            selections=[layers,[dict(v,regions=[r for r in v['regions'] if r['ordinary_callback']['accepted']]) for v in layers]]
            headings=['Retained ordinary source geometry','Regions admitted by the 150-unit area query']
            subtitles=['Conditional construction / retained ownership','Same geometry; actual native callback tested per region']
        else:
            selections=[[v for v in layers if v['variant_count']==1 or (v['source_id']=='U25' and v['mask']==mask)] for mask in (0,3)]
            headings=['Conditional U25 construction: mask 0','Conditional U25 construction: mask 3']
            subtitles=['Separate alternative; historical winner unknown','Separate alternative; operator reports qualitative agreement']
        lines=start(ref['name'],1730)
        lines += [text(32,73,'Historical-frame reconstruction · fixed main definitions · no loaded epoch or gameplay transition asserted',15),
                  text(32,101,'Native centre '+str(ref['center'])+' · full 150-native-unit ordinary default radius',14),
                  text(32,127,'Saved beacon = centre only in this zero-compensation saved representation. Source anchors are separate.',14)]
        panels=[];records=[]
        cx,cy=ref['center'][:2];zoom=[cx-240,cx+240,cy-240,cy+240]
        for n,selection in enumerate(selections):
            panels.append(native_panel(lines,f'{case}-{n}',80+620*n,225,480,zoom,ref['center'][:2],150,
                                       selection,palette,headings[n],subtitles[n]))
            counts=Counter(r['resource'] for v in selection for r in v['regions'] if r['ordinary_callback']['accepted'])
            record={'panel':n,'layer_ids':[v['id'] for v in selection],
                    'accepted_region_counts':dict(sorted(counts.items())),
                    'area_resources':[palette[k]['name'] for k in sorted(counts)],
                    'query_native':ref['center'],'radius':150,'upper':ref['upper']}
            records.append(record)
            lines.append(text(80+620*n,785,'Area membership: '+', '.join(record['area_resources']),13))
        lines += [text(32,811,'U23 alternatives are omitted from this second-V comparison: both have zero disk intersection; no joint winner is asserted.' if case=='D2-84e101' else 'All four source contributions are included; the right panel selects regions, without changing their native point bytes.',12),
                  text(32,839,'Lifecycle: retained map hit does not regenerate; reset removes ownership and visited state before new successful demand.',14),
                  text(32,857,'Consumer: area membership can stay equal while generated shapes or accepted-path counts differ. No frequency is inferred.',14),
                  text(32,885,'Black cross / diamond / circle: saved centre / saved beacon / full default radius; axes are absolute native descriptor-frame XY.',13),
                  text(32,913,'Deposit silhouettes approximate marginal native segment rounding. Native callback decisions are a distinct tested predicate.',14),
                  text(32,941,'Excluded: terrain, POI-clipped borders, scanner overlay, Special/Water/atmosphere, hardware collision and actual loaded queries.',14)]
        colors=sorted({r['resource'] for v in layers for r in v['regions']})
        for n,resource in enumerate(colors):
            x=32+n*200
            lines += [f'<rect x="{x}" y="970" width="15" height="15" fill="{palette[resource]["rgb"]}"/>',
                      text(x+22,983,palette[resource]['name'],13)]
        # Full-extent companions preserve every displayed deposit outside the zoom.
        bounds=[r['native_bound'] for selection in selections for v in selection for r in v['regions']]
        xmin=min([cx-150]+[b[0]-max(b[3],.5) for b in bounds]);xmax=max([cx+150]+[b[0]+max(b[3],.5) for b in bounds])
        ymin=min([cy-150]+[b[1]-max(b[3],.5) for b in bounds]);ymax=max([cy+150]+[b[1]+max(b[3],.5) for b in bounds])
        span=max(xmax-xmin,ymax-ymin)+80;mx=(xmin+xmax)/2;my=(ymin+ymax)/2
        full=[mx-span/2,mx+span/2,my-span/2,my+span/2]
        for n,selection in enumerate(selections):
            panels.append(native_panel(lines,f'{case}-full-{n}',80+620*n,1110,480,full,ref['center'][:2],150,
                                       selection,palette,'Full extent · '+('left comparison' if n==0 else 'right comparison'),
                                       'Same native axes; every displayed region bound is inside this viewport'))
        lines += [text(32,1700,'Upper panels deliberately zoom; lower panels retain full displayed deposits. Native region-bound clipping is part of the supplied shape.',13)]
        (out/f'{case}.svg').write_text(finish(lines),encoding='utf8',newline='\n')
        summary['cases'][case]={'reference':ref,'source_geometry':str(source.relative_to(ROOT)),
                              'source_geometry_sha256':sha(source),'panels':panels,'consumer':records}
    coordinate_boxes=[
        ('a',32,95,360,115,['Body-face cells: signed Int2','Descriptor O, site S, source A','Fine-cell scale: 100 native units']),
        ('b',470,95,730,115,['Historical descriptor frame (binary32 XY / XYZ)','C = f32(L + 100(S − O)); anchor = 100(A − O)','Generator origin = anchor − (200,200), not centre']),
        ('c',32,320,520,115,['Area query: indexed XYZ, index, domain','Q = f32(XYZ + translation[index]) when in range','Native geometry comparison requires matching frame']),
        ('d',680,320,520,115,['Extractor candidate: reference +0x8c / +0x94','Plain XYZ copied into point query; no index here','No historical candidate position is asserted']),
        ('e',32,540,1168,100,['Absolute native X/Y data and axes. Pixels only: u = left + (x − xmin) s; v = top + (ymax − y) s',
                                 'Inverse: native x = xmin + (u − left)/s; native y = ymax − (v − top)/s',
                                 'X/Y are native axes; north/east/metres and 3D handedness are not inferred.'])]
    coordinate_edges=[(392,150,470,150,'saved-frame join'),(400,210,280,320,'conditional common frame'),
                      (950,210,950,320,'conditional common frame'),(290,435,290,540,'native → display'),(950,435,950,540,'native → display')]
    coordinates=schematic('Native coordinate domains and explicit display transform',coordinate_boxes,coordinate_edges,
                          ['Source geometry and query operands remain native values. Only the SVG viewport reverses Y.',
                           'A current indexed translation is not recovered from a historical save. Unjoined live frames are not overlaid.'])
    (out/'coordinates.svg').write_text(coordinates,encoding='utf8',newline='\n')
    lifecycle_boxes=[
        ('a',32,100,360,100,['Cold ProcGen / new context','Map empty; visited empty','Successful unvisited miss constructs']),
        ('b',470,100,360,100,['Retained source wrapper','Owned regions / copied points','Map hit or visited bypass: no generation']),
        ('c',900,100,310,100,['Broad manager reset','Module +0x18 clears stores','Later demand may reconstruct']),
        ('d',32,330,360,125,['Grid shift / source retirement','Retained overlaps can survive','Retirement removes map entry','Visited identity can remain']),
        ('e',470,330,360,125,['Area updater → catalogue / UI','Domain/displacement refresh','Area predicate + ATMO / BIOM','List filters; asynchronous UI reads']),
        ('f',900,330,310,125,['Candidate placement gate','Point predicate at raw XYZ','Intersect produced resources','Separate territory/collision gates'])]
    lifecycle_edges=[(392,150,470,150,'construct'),(830,150,900,150,'reset'),
                     (510,200,210,330,'ordinary shift'),(650,200,650,330,'area scan'),
                     (800,200,1055,330,'point scan')]
    life=schematic('Population lifecycle and consumer boundaries',lifecycle_boxes,lifecycle_edges,
                   ['Static branches and conditional model outputs; arrows do not claim an observed gameplay chronology.',
                    'Retirement alone does not require regeneration. A retained visited key can suppress a later miss.'])
    (out/'lifecycle.svg').write_text(life,encoding='utf8',newline='\n')
    for p in out.glob('*.svg'):
        ET.fromstring(p.read_text(encoding='utf8'))
        summary['diagrams'][p.name]=sha(p)
    (out/'spatial.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8',newline='\n')
    print('Rendered four D5V SVGs and explicit native/display backing data.')


if __name__=='__main__':main()
