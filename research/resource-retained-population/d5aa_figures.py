# SPDX-License-Identifier: GPL-3.0-or-later
"""Render three original SVG research diagrams from sanitized D5AA backing data.

Reads the specified JSON/CSV directory; creates a fresh output directory and SVGs.
CPython stdlib only. No target, raw evidence, database, observer or Git effects.
Chronology positions use measured relative QPC; graph positions are schematic.
"""
import csv
import html
import json
from pathlib import Path
import sys

COLORS={'OBSERVED':'#187b84','PROVEN STATIC':'#3f51a1','CONDITIONAL':'#9a6919','UNKNOWN':'#8b5367'}

def text(x,y,value,size=17,color='#202b3d'):
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{color}">{html.escape(str(value))}</text>'

def start(title,height):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="{height}" viewBox="0 0 1280 {height}" role="img"><title>{html.escape(title)}</title>',f'<rect width="1280" height="{height}" fill="#f6f8fc"/>',text(36,42,title,26)]

def legend(parts,y):
    for i,(label,color) in enumerate(COLORS.items()):
        parts.append(f'<line x1="{36+i*304}" y1="{y}" x2="{66+i*304}" y2="{y}" stroke="{color}" stroke-width="4"'+(' stroke-dasharray="6 4"' if label in ('UNKNOWN','CONDITIONAL') else '')+'/>')
        parts.append(text(74+i*304,y+5,label,14,color))

def graph(title,rows,out):
    p=start(title,150+len(rows)*88);legend(p,80)
    p.append(text(36,114,'Schematic causal edges; row order is not an event timestamp.',15))
    for i,row in enumerate(rows):
        y=140+i*88;c=COLORS[row['basis']]
        p.append(f'<rect x="36" y="{y}" width="1208" height="74" rx="8" fill="white" stroke="{c}" stroke-width="2"'+(' stroke-dasharray="6 4"' if row['basis'] in ('UNKNOWN','CONDITIONAL') else '')+'/>')
        p.append(text(52,y+25,row['from']+' → '+row['to'],18,c))
        p.append(text(52,y+52,row['qualification'],15))
    out.write_text('\n'.join(p+['</svg>'])+'\n',encoding='utf8',newline='\n')

def state_machine(out):
    p=start('One source: visited and source-map state machine',1160);legend(p,80)
    p.append('<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="#59667b"/></marker></defs>')
    nodes={
        'empty':(44,150,'Unvisited after clear','PROVEN STATIC'),
        'reset':(900,150,'Broad reset (live owner)','PROVEN STATIC'),
        'select':(44,290,'Select source; compare token','PROVEN STATIC'),
        'bypass':(900,290,'Visited hit: bypass map','OBSERVED'),
        'map':(44,430,'Unvisited: exclusive lookup','PROVEN STATIC'),
        'hit':(460,430,'Map hit: reuse, no append','OBSERVED'),
        'generate':(44,570,'Map miss: insert / generate','OBSERVED'),
        'sample':(460,570,'Ordinary sample, if eligible','OBSERVED'),
        'reserve':(44,710,'After return: reserve visit','PROVEN STATIC'),
        'store':(460,710,'Success: store token (static)','PROVEN STATIC'),
        'failure':(44,850,'Failure: no token store','PROVEN STATIC'),
        'later':(900,710,'Later matching-token bypass','CONDITIONAL'),
        'retire':(460,850,'Retire: erase map only','PROVEN STATIC')}
    for x,y,label,basis in nodes.values():
        c=COLORS[basis]
        p.append(f'<rect x="{x}" y="{y}" width="320" height="64" rx="8" fill="white" stroke="{c}" stroke-width="2"'+(' stroke-dasharray="6 4"' if basis in ('UNKNOWN','CONDITIONAL') else '')+'/>')
        p.append(text(x+12,y+36,label,17,c))
    def line(points,label,tx,ty,dashed=False):
        p.append('<polyline points="'+points+'" fill="none" stroke="#59667b" stroke-width="2" marker-end="url(#arrow)"'+(' stroke-dasharray="6 4"' if dashed else '')+'/>');p.append(text(tx,ty,label,14))
    line('204,214 204,290','next demand',218,252)
    line('364,322 900,322','token matches',560,311)
    line('204,354 204,430','no match; release shared lock',218,398)
    line('364,462 460,462','hit',398,451)
    line('204,494 204,570','miss',218,538)
    line('364,602 460,602','eligible',381,592)
    line('204,634 204,710','returned attempt',218,678)
    line('364,742 460,742','reserved',379,732)
    line('204,774 204,850','0xffffffff',218,816)
    line('780,742 900,742','next query',795,732,True)
    line('620,774 620,850','lifecycle',635,816,True)
    line('364,882 460,882','may retire',377,871,True)
    line('900,182 410,182 410,125 204,125 204,150','clear both stores',493,169)
    p.append(text(44,962,'Reset is a guarded lifecycle transition from relevant states; source retirement leaves visited membership intact.',17))
    p.append(text(44,994,'No B1 append-success witness. Later bypass identity is conditional; no complete first-to-bypass chain is authenticated.',16,'#8b5367'))
    p.append(text(44,1026,'Map hits can follow an earlier unvisited check while another thread generates. No second visited scan occurs under exclusive lock.',16))
    p.append(text(44,1058,'Arrows show scoped state transitions, not elapsed time. Sampler success does not prove complete geometry or successful marking.',16))
    p.append(text(44,1090,'Direct B1 observations apply to non-target paths; target first processing, append and lifetime remain unknown.',16))
    p.append(text(44,1124,'Destruction ends the owner lifetime; a new owner starts through construction.',16))
    out.write_text('\n'.join(p+['</svg>'])+'\n',encoding='utf8',newline='\n')

def main(data,out):
    data,out=Path(data),Path(out);assert not out.exists();out.mkdir(parents=True)
    backing=json.loads((data/'graph-data.json').read_text(encoding='utf8'))
    events=list(csv.DictReader((data/'chronology-points.csv').open(encoding='utf8')))
    p=start('B1 retained chronology: observations and checkpoint windows',800);legend(p,80)
    p.append(text(36,118,'Seconds after first admitted QPC sample; no invented travel or target-first timestamp.',16))
    x=lambda seconds:84+float(seconds)*4.25
    for i,window in enumerate(backing['windows']):
        y=150+i*70
        p.append(text(36,y,window['label'],16))
        p.append(f'<rect x="{x(window["start"])}" y="{y+10}" width="{max(2,(window["end"]-window["start"])*4.25)}" height="20" fill="#d7e5f0" stroke="#187b84"/>')
        p.append(text(84,y+46,f'{window["start"]:.7f}–{window["end"]:.7f} s; receipt collection interval',13))
    axis_y=399
    p.append(f'<line x1="84" y1="{axis_y}" x2="{x(260)}" y2="{axis_y}" stroke="#738099"/>')
    for sec in (0,50,100,150,200,250):
        p.append(text(x(sec)-8,axis_y+24,str(sec),14))
    loss=next(e for e in events if e['label']=='Admission at first sampled loss boundary')
    p.append(f'<rect x="{x(loss["second"])}" y="435" width="{x(231)-x(loss["second"])}" height="238" fill="#f6d8cd" opacity="0.65"/>')
    for i,e in enumerate(events):
        y=454+i*27;basis=e['basis'];c=COLORS[basis]
        p.append(f'<circle cx="{x(e["second"])}" cy="{y-5}" r="4" fill="{c}"/>')
        p.append(text(110 if e['sequence']=='1' else 36,y,e['label']+' · seq '+e['sequence']+' · '+e['second']+' s',14,c))
    p.append(text(36,710,'Shading: retained events after the first sampled loss boundary; lost events have no known individual times.',15,'#8b5367'))
    p.append(text(36,739,'UNKNOWN: actual travel confirmation, target first query/mask, append and visual arrival instants.',16,'#8b5367'))
    p.append(text(36,768,'9,957 queue-full losses; 13 QPC/admission inversions. A checkpoint is not a native transition.',15))
    (out/'chronology.svg').write_text('\n'.join(p+['</svg>'])+'\n',encoding='utf8',newline='\n')
    graph('Load / Lodge → travel → resource demand / arrival',backing['causality'],out/'causality.svg')
    state_machine(out/'source-state.svg')

if __name__=='__main__':main(*sys.argv[1:])
