# SPDX-License-Identifier: GPL-3.0-or-later
"""Create D5U evidence-linked CSV, geometry JSON and deterministic SVGs.

Reads D5U census/native receipts and installed IRES color/name fields. Writes
only requested research derivatives and ignored QA metadata. Owned D5T planar
primitive reconstruction is reused with its explicit marginal-rounding limit.
Outpost labels use the existing authored case inventory, never raw save access.
No game, save, native execution, Ghidra, network, dependency install or Git write.
"""
from collections import Counter
import html
import json
import math
import re
from pathlib import Path
import struct
import sys

from d5u_census import ROOT, LOCAL, DOC, write, table
from d5t_maps import primitives
sys.path.insert(0,str(ROOT/'save-analysis/scripts'))
from inspect_outpost_definitions import esm_records

MASKS = {0:'#e8edf2',1:'#f8c471',2:'#c39bd3',3:'#5dade2',4:'#76d7c4',8:'#ec7063'}
CASE_NAMES = {'original-V':'Feynman V first site','Carinae':'Carinae III-a','Archimedes':'Archimedes III',
              'D2-81bf2a':'Feynman VI-b','D2-825f95':'Feynman VII-b','D2-844cc6':'Feynman VIII-b',
              'D2-84e101':'Feynman V second site','corner-V':'Feynman V corner'}
OUTPOST_CASES = {'original-V':'D2-83388f','Carinae':'D2-82be17','Archimedes':'D2-81a75b'}


def esc(value):
    return html.escape(str(value))


def text(x,y,value,size=14,extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" {extra}>{esc(value)}</text>'


def start(width,height,title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            f'<title>{esc(title)}</title>', '<rect width="100%" height="100%" fill="#f8fafc"/>',
            '<g font-family="Segoe UI,Arial,sans-serif" fill="#162b38">']


def finish(lines):
    return '\n'.join(lines+['</g></svg>'])+'\n'


def support_map(source):
    row,coords = source['catalogue'],source['coordinates']
    w,h = row['width'],row['height']
    s = min(32,640/(max(w,h)+6))
    left,top = 100,140
    lines = start(960,1100,f"{row['source_id']} source-query mask support")
    lines += [text(32,36,f"{row['source_id']} · {row['outpost_name']} · query variability",22),
              text(32,64,row['source_key'],17),text(32,89,'Source-relative integer query index bins · X right, Y up · 100 native units per cell'),
              text(32,113,'Bin [x,x+1) represents the integer query x; colors are ordinary numeric nibbles.')]
    def point(x,y):
        return left+(x+3)*s,top+(h+3-y)*s
    x0,y0 = point(-3,h+3)
    lines.append(f'<rect x="{x0}" y="{y0}" width="{(w+6)*s}" height="{(h+6)*s}" fill="#d9d9d9"/>')
    for q in coords:
        x,y = point(q['x'],q['y']+1)
        lines.append(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{MASKS[q["mask"]]}" stroke="white" stroke-width="0.5"/>')
        cx,cy = x+s/2,y+s/2
        if q['status'].startswith('PROVEN'):
            lines.append(f'<circle cx="{cx}" cy="{cy}" r="{s*.27}" fill="none" stroke="#111" stroke-width="2.4"/>')
            lines.append(f'<path d="M{cx-s*.16} {cy}h{s*.32} M{cx} {cy-s*.16}v{s*.32}" stroke="#111"/>')
    x,y = point(0,h)
    lines.append(f'<rect x="{x}" y="{y}" width="{w*s}" height="{h*s}" fill="none" stroke="#6d267a" stroke-width="2.6" stroke-dasharray="7 4"/>')
    ax,ay = point(.5,.5)
    lines.append(f'<path d="M{ax-6} {ay}h12 M{ax} {ay-6}v12" stroke="#6d267a" stroke-width="2"/>')
    for v in sorted(set([-2,0,w,w+2])):
        x,y = point(v,-2)
        lines += [text(x,y+24,v,12,'text-anchor="middle"')]
    for v in sorted(set([-2,0,h,h+2])):
        x,y = point(-2,v)
        lines += [text(x-12,y+4,v,12,'text-anchor="end"')]
    base = top+(h+6)*s+60
    lines += [text(55,base,'Dashed purple: nominal source footprint. Surrounding colored cells: two-cell padding.'),
              text(55,base+25,'Black circled cross: proven winner witness. Other colored bins: individually unqualified candidates.'),
              text(55,base+50,'Gray outside: proven excluded from this source support. No internal exclusions are asserted.')]
    hist = json.loads(row['histogram'])
    for i,(m,count) in enumerate(hist.items()):
        x = 55+i*190
        lines.append(f'<rect x="{x}" y="{base+70}" width="20" height="18" fill="{MASKS[int(m)]}" stroke="#555"/>')
        lines.append(text(x+28,base+85,f'Mask {m}: {count} cells'))
    lines += [text(55,base+120,'Counts describe support, never winner probabilities.'),
              text(55,base+145,'Source-only frame. Outpost centre / beacon alignment: UNKNOWN in this frame. No radius overlay.'),
              text(55,base+170,f"Reachable masks: {row['reachable_masks']} · effective weight classes: {row['weight_classes']} · geometry: {row['geometry_outcomes']}"),
              text(55,base+195,'Build 1.16.244.0 · fixed main definitions · cold successful qualified construction; see report.',12)]
    authority = ('D5S normal-arrival batch' if row['source_id']=='U25' else 'D5U QS1 direct-cell continuations'
                 if row['source_id']=='U26' else 'D5I QS1 direct-cell continuations' if row['raster_masks']>1
                 else 'None; singleton classification is conditional on successful construction')
    lines.append(text(55,base+217,'Plotted witness authority: '+authority+'.',12))
    assert base+217<1100,(row['source_id'],base)
    return finish(lines)


def geometry_map(outcomes,palette,title):
    # All panels in the entire D5U geometry collection share this canonical frame.
    lo,hi = -500,1200
    s = .32
    span = (hi-lo)*s
    width = max(1100,650*len(outcomes)+40)
    lines = start(width,850,title)
    lines += [text(28,34,title,23),text(28,61,'Native generation-competition footprints · source anchor (0,0) · X right, Y up · native units'),
              text(28,84,'Continuous planar reconstruction; native marginal floating-point boundaries are approximate.',13)]
    for panel,outcome in enumerate(outcomes):
        left,top = 65+650*panel,175
        def point(x,y):
            return left+(x-lo)*s,top+(hi-y)*s
        lines += [text(left,117,f"{outcome['source_id']} · mask {outcome['mask']} · {len(outcome['regions'])} regions",19),
                  text(left,141,outcome['outpost_name'],13),text(left,162,outcome['source_key'],11)]
        lines.append(f'<rect x="{left}" y="{top}" width="{span}" height="{span}" fill="white" stroke="#bccbd2"/>')
        for value in (-400,0,400,800,1200):
            x,y = point(value,value)
            lines.append(f'<path d="M{x} {top}v{span} M{left} {y}h{span}" stroke="#e1e6eb"/>')
            lines += [text(x,top+span+22,value,12,'text-anchor="middle"'),text(left-8,y+4,value,12,'text-anchor="end"')]
        order = list(dict.fromkeys(r['resource'] for r in outcome['regions']))
        for resource in reversed(order):
            color = palette[resource]['rgb']
            lines.append(f'<g fill="{color}" stroke="{color}" stroke-width="0.5">')
            for i,region in enumerate(outcome['regions']):
                if region['resource']!=resource:
                    continue
                bx,by,bz,radius = region['native_bound']
                bx,by = point(bx,by)
                identity = f'p{panel}r{i}'
                lines.append(f'<defs><clipPath id="{identity}"><circle cx="{bx}" cy="{by}" r="{max(radius,.5)*s}"/></clipPath></defs>')
                lines.append(f'<g clip-path="url(#{identity})">')
                for shape in region['primitives']:
                    if shape['kind']=='disk':
                        x,y = point(*shape['center'])
                        lines.append(f'<circle cx="{x}" cy="{y}" r="{shape["radius"]*s}"/>')
                        x0,y0 = shape['center'];rad = shape['radius']
                        assert lo<=x0-rad and x0+rad<=hi and lo<=y0-rad and y0+rad<=hi
                    else:
                        assert all(lo<=v<=hi for xy in shape['vertices'] for v in xy)
                        coords = ' '.join(f'{x},{y}' for x,y in [point(*v) for v in shape['vertices']])
                        lines.append(f'<polygon points="{coords}"/>')
                lines.append('</g>')
            lines.append('</g>')
        x,y = point(0,0)
        lines.append(f'<path d="M{x-6} {y}h12 M{x} {y-6}v12" stroke="#842e8b" stroke-width="2"/>')
        counts = Counter(r['resource'] for r in outcome['regions'])
        for i,resource in enumerate(order):
            x = left+(i%3)*175
            y = 753+(i//3)*22
            lines.append(f'<rect x="{x}" y="{y}" width="12" height="12" fill="{palette[resource]["rgb"]}"/>')
            lines.append(text(x+17,y+11,f"{palette[resource]['name']} {counts[resource]}",11))
    lines += [text(28,812,'Source-only prospective frame. Outpost native centre / beacon: UNKNOWN; translation to an actual outpost is unestablished.',13),
              text(28,834,'150-unit outpost boundary is omitted. Colors: installed IRES TINC. Shapes: exact native points and bounds, approximate segment vertices.',12)]
    return finish(lines)


def comparison_svg(sources):
    lines = start(1120,1080,'D5U cross-source comparison')
    lines += [text(30,34,'D5U · 25 historical sources and one corner discriminator',25),
              text(30,64,'Separate quantities; numbered circles encode counts, not spatial probabilities.'),
              text(30,90,'* Conditional on a successful fixed-input construction. Q = QS1 feasible witness classes. E = executed native geometry.')]
    for x,label in [(35,'Source / case'),(530,'Raster masks'),(680,'Reachable masks'),(830,'Weight classes'),(980,'Geometry')]:
        lines.append(text(x,130,label,15))
    for i,source in enumerate(sources):
        row = source['catalogue']
        y = 165+i*31
        lines += [text(35,y,f"{row['source_id']}  {row['outpost_name']}  {row['source_key']}",12)]
        for col,key in enumerate(('raster_masks','raster_masks','weight_classes','raster_masks')):
            value = row[key]
            x = 565+150*col
            lines.append(f'<circle cx="{x}" cy="{y-5}" r="11" fill="{["#cddce8","#dae9da","#f3dfb6","#ddcff0"][col]}"/>')
            lines.append(text(x,y,value,13,'text-anchor="middle"'))
            suffix = '' if col in (0,2) else (' Q' if col==1 else ' E') if row['raster_masks']>1 else ' *'
            lines.append(text(x+17,y,suffix,12))
    lines += [text(35,1010,'Singleton geometry follows complete fixed-input equivalence; individual winner membership remains UNKNOWN except marked witnesses.'),
              text(35,1035,'Unknown overlays, definitions, frame, failed allocations or nonordinary routes fall outside this conditional classification.',13),
              text(35,1060,'U26 is added, not part of the historical 25. Counterfactual Nickel mask controls are excluded from these counts.',13)]
    return finish(lines)


def main():
    import csv
    name_source = ROOT/'docs/experiments/resource-save52/cases.csv'
    names = {r['case']:r for r in csv.DictReader(name_source.open(encoding='utf8'))}
    census = json.loads((LOCAL/'census.json').read_text(encoding='utf8'))
    summary = json.loads((LOCAL/'native05/summary.json').read_text(encoding='utf8'))
    executed = {v['source_id']:v for v in summary}
    keys = json.loads((LOCAL/'keys04.json').read_text(encoding='utf8'))
    assert len(keys['queries']) == census['cells'] == 6536
    palette, outcomes = {},[]
    wanted = set()
    for source in census['sources']:
        wanted.update(r['id'] for r in source['resources'])
    esm = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm')
    for header,fields in esm_records(esm,{b'IRES'},repeated=True):
        identity = f"{header['formid']:08x}"
        if identity not in wanted:
            continue
        data = dict(fields)
        tint = data[b'TINC']
        editor_id = data[b'EDID'].rstrip(b'\0').decode()
        name = re.sub(r'^ResInorg(?:Uncommon|Common|Rare|Exotic|Unique)', '', editor_id)
        name = re.sub(r'_[GSL]$', '', name).replace('IonicLiquids','Ionic Liquids').replace('Helium3','Helium-3')
        palette[identity] = dict(rgb='#'+tint[:3].hex(),tinc=tint.hex(),record_file_offset=header['offset'],
                                 name=name,editor_id=editor_id)
    assert set(palette) == wanted
    for source in census['sources']:
        row = source['catalogue']
        case = OUTPOST_CASES.get(row['case'],row['case'])
        if case in names:
            assert row['body']==names[case]['body']
            row['outpost_name'],row['outpost_case'] = names[case]['name'],case
        else:
            assert row['source_id']=='U26'
            row['outpost_name'],row['outpost_case'] = 'No associated outpost (Feynman V discriminator)','NONE'
        row['outpost_name_provenance'] = 'resource-save52/cases.csv: '+case if case in names else 'Added static discriminator; no outpost identity assigned'
        variable = row['raster_masks']>1
        row['historical_d5i'] = ('VARIABLE' if variable else 'INVARIANT') if row['source_id']!='U26' else 'NOT IN HISTORICAL 25'
        row['current_classification'] = 'VARIABLE' if variable else 'INVARIANT CONDITIONAL ON SUCCESS'
        row['reachability_evidence'] = ('d5u-methods.md: U26 constructive first-miss proof' if row['source_id']=='U26'
            else 'd5s-query-winner-model.md; D5H/I QS1 also applicable' if row['source_id']=='U25'
            else '../resource-query-variability/proofs.md: source-specific traces' if variable
            else '../resource-query-reachability/native.md: singleton transformed support upper; conditional nonempty A')
        row['reachable_masks'] = str(row['raster_masks'])+(' QS1' if variable else ' conditional-success')
        row['geometry_outcomes'] = str(row['raster_masks'])+(' executed' if variable else ' fixed-input proof')
        for q in source['coordinates']:
            if variable and row['source_id']!='U26':
                witnesses = [(-2,-2),(10,11)] if row['source_id']=='U25' else [(4,-1),(4,1)]
                if (q['x'],q['y']) in witnesses:
                    q['status'] = 'PROVEN D5S' if row['source_id']=='U25' else 'PROVEN D5I QS1'
            elif row['source_id']=='U26' and [q['x'],q['y']] in [v['query'] for v in keys['corners']]:
                q['status'] = 'PROVEN D5U QS1'
        if row['source_id'] in executed:
            receipt = json.loads((LOCAL/'native05'/executed[row['source_id']]['native']).read_text(encoding='utf8'))
            source_outcomes = []
            for run in receipt['runs']:
                if 'repeat' in run['outcome'] or run['outcome'].startswith('CONTROL'):
                    continue
                # Nickel masks 1/3 are a separate counterfactual mechanism control.
                outcome = dict(source_id=row['source_id'],source_key=row['source_key'],mask=run['mask'],
                               outpost_name=row['outpost_name'],outpost_case=row['outpost_case'],
                               admissibility='QS1 conditional' if str(run['mask']) in source['weights'] else 'COUNTERFACTUAL CONTROL; not reachable at this source',
                               native_receipt=executed[row['source_id']]['native'],regions=[])
                for raw in run['regions']:
                    pts = [list(p) for p in struct.iter_unpack('<4f',bytes.fromhex(raw['points']))]
                    region = dict(resource=raw['resource'],points_xyz_width=pts,
                                  native_bound=list(struct.unpack('<4f',bytes.fromhex(raw['header'][:32]))),
                                  metadata_words=list(struct.unpack('<2I',bytes.fromhex(raw['header'][32:48]))),
                                  primitives=primitives(pts))
                    outcome['regions'].append(region)
                outcomes.append(outcome)
                if str(run['mask']) in source['weights']:
                    source_outcomes.append(outcome)
            (DOC/f"{row['source_id']}-geometry.svg").write_text(geometry_map(source_outcomes,palette,f"{row['source_id']} ordinary geometry variants"),encoding='utf8',newline='\n')
        (DOC/f"{row['source_id']}-support.svg").write_text(support_map(source),encoding='utf8',newline='\n')
    # Explicit common-frame comparison of the first/second V reference sources.
    reference = [o for o in outcomes if o['source_id'] in ('U02','U25')]
    (DOC/'feynman-reference.svg').write_text(geometry_map(reference,palette,'First and second Feynman V reference source contracts'),encoding='utf8',newline='\n')
    control = [o for o in outcomes if o['source_id']=='U01' and o['mask'] in (1,3)]
    assert control[0]['regions'] == control[1]['regions']
    (DOC/'weight-equivalence-control.svg').write_text(geometry_map(control,palette,'Counterfactual masks 1 and 3 · Nickel-family equivalence control'),encoding='utf8',newline='\n')
    write(DOC/'geometry.json',dict(schema='sor-d5u-geometry/1',palette=palette,outcomes=outcomes,
          frame='Source anchor zero; generator origin (-200,-200); native units; X right, Y up',
          rendering='D5T generation-competition footprint: positive-width disks and max-width segment rectangles intersect native bound disk max(r,0.5). Native marginal float/quaternion boundaries approximated.',
          extent=[-500,1200,-500,1200],scale=.32,per_panel_origin=[65,175],panel_stride=650,
          outpost_centre='UNKNOWN',beacon='UNKNOWN',publication='REVIEW-REQUIRED'))
    table(DOC/'catalogue.csv',[s['catalogue'] for s in census['sources']])
    table(DOC/'queries.csv',[q for s in census['sources'] for q in s['coordinates']])
    (DOC/'comparison.svg').write_text(comparison_svg(census['sources']),encoding='utf8',newline='\n')
    gallery = ['# D5U source-map index','', '[Report](../d5u-report.md) · [comparison graphic](comparison.svg) · [catalogue](catalogue.csv) · [all query bins](queries.csv) · [native geometry](geometry.json)', '',
               'Every support map shows all candidate bins, nominal footprint, padding, proven witness overlays and explicit uncertainty. These are source-only prospective frames; the outpost centre and beacon alignment are UNKNOWN. Counts are conditional outcomes, never frequencies.', '',
               'Outpost names are the exact recorded navigation labels, joined by stable saved beacon/case identity. Names do not select resources. U26 has no associated outpost. See the [name and centre explanation](../d5u-names-and-centre-followup.md) for provenance and why the 150-unit disk was omitted.', '',
               '| ID / case | Exact source | Support | Native geometry |','|---|---|---|---|']
    for s in census['sources']:
        row=s['catalogue'];identity=row['source_id']
        geom=f'[{identity} variants]({identity}-geometry.svg)' if identity in executed else 'One class by fixed-input proof; not separately executed'
        gallery.append(f"| {identity} / {row['outpost_name']} | `{row['source_key']}` | [{identity} support]({identity}-support.svg) | {geom} |")
    gallery += ['', '[First/second V reference comparison](feynman-reference.svg) uses one common source-relative frame. [Nickel mask-equivalence control](weight-equivalence-control.svg) is counterfactual at that source, not evidence of reachable masks 1/3.', '',
                'The six historical variable sources are U16, U19 through U21, U23 and U25. Their historical D5I/QS1 geometry inputs differed in frame in some cases; these new native totals do not revise those frozen results. U26 is the independently selected three-mask discriminator.']
    (DOC/'README.md').write_text('\n'.join(gallery)+'\n',encoding='utf8',newline='\n')
    write(LOCAL/'map-checks.json',dict(sources=len(census['sources']),cells=census['cells'],outcomes=len(outcomes),
                                     same_weight_native_equal=True,svg_count=len(list(DOC.glob('*.svg'))),code_sha256=__import__('hashlib').sha256(Path(__file__).read_bytes()).hexdigest()))
    print('PASS',len(census['sources']),'source maps',len(outcomes),'native exports')


def reproduce(destination):
    """Render every SVG solely from tracked catalogue/query/geometry derivatives."""
    import csv
    destination = Path(destination).resolve()
    assert destination.is_relative_to(LOCAL) and not destination.exists()
    destination.mkdir()
    rows = list(csv.DictReader((DOC/'catalogue.csv').open(encoding='utf8')))
    queries = list(csv.DictReader((DOC/'queries.csv').open(encoding='utf8')))
    for row in rows:
        for key in ('width','height','raster_masks','weight_classes'):
            row[key] = int(row[key])
    for q in queries:
        for key in ('x','y','mask'):
            q[key] = int(q[key])
    sources = [dict(catalogue=r,coordinates=[q for q in queries if q['source_id']==r['source_id']]) for r in rows]
    data = json.loads((DOC/'geometry.json').read_text(encoding='utf8'))
    palette,outcomes = data['palette'],data['outcomes']
    for source in sources:
        identity = source['catalogue']['source_id']
        (destination/(identity+'-support.svg')).write_text(support_map(source),encoding='utf8',newline='\n')
        variants = [o for o in outcomes if o['source_id']==identity and not o['admissibility'].startswith('COUNTERFACTUAL')]
        if variants:
            (destination/(identity+'-geometry.svg')).write_text(geometry_map(variants,palette,f'{identity} ordinary geometry variants'),encoding='utf8',newline='\n')
    (destination/'comparison.svg').write_text(comparison_svg(sources),encoding='utf8',newline='\n')
    for name,title,selected in [
        ('feynman-reference.svg','First and second Feynman V reference source contracts',[o for o in outcomes if o['source_id'] in ('U02','U25')]),
        ('weight-equivalence-control.svg','Counterfactual masks 1 and 3 · Nickel-family equivalence control',[o for o in outcomes if o['source_id']=='U01' and o['mask'] in (1,3)])]:
        (destination/name).write_text(geometry_map(selected,palette,title),encoding='utf8',newline='\n')
    assert {p.name for p in destination.glob('*.svg')} == {p.name for p in DOC.glob('*.svg')}
    assert all(p.read_bytes()==(DOC/p.name).read_bytes() for p in destination.glob('*.svg'))
    print('PASS: all SVGs reproduced byte-for-byte from tracked data')


if __name__ == '__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--from-data':
        reproduce(sys.argv[2])
    else:
        main()
