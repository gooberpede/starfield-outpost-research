# SPDX-License-Identifier: GPL-3.0-or-later
"""Render D5Y authored scientific SVGs from authenticated analysis aggregates.

Reads a completed ignored d5y_forensics output; writes a fresh destination with
small structured aggregates and SVGs. Stdlib only. No raw event payload, pointer,
native export or binary is copied into tracked graphics. No target/native calls.
SVG raster previews use an existing standalone renderer separately, without
incorporating its implementation. Output remains REVIEW-REQUIRED.
"""
import argparse
import csv
import hashlib
from html import escape
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
COLORS = ['#316c9b','#21a08b','#e7ae3b','#8555a1','#a96d46']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class SVG:
    def __init__(self, title, subtitle, height=690):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}">',
            '<title>'+escape(title)+'</title>',
            '<style>text{font-family:Arial,sans-serif;fill:#223247;font-size:15px}.small{font-size:13px}.title{font-size:26px;font-weight:bold}.sub{font-size:16px}.axis{stroke:#8b97a5;stroke-width:1}</style>',
            f'<rect width="1200" height="{height}" fill="#f8fafc"/>']
        self.text(32,40,title,'title')
        self.text(32,70,subtitle,'sub')

    def text(self,x,y,value,cls='small',**extra):
        attrs = ' '.join(f'{k}="{v}"' for k,v in extra.items())
        self.parts.append(f'<text x="{x}" y="{y}" class="{cls}" {attrs}>{escape(str(value))}</text>')

    def rect(self,x,y,w,h,fill,opacity=1):
        self.parts.append(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{fill}" opacity="{opacity}"/>')

    def line(self,x1,y1,x2,y2,color='#8b97a5',dash=''):
        self.parts.append(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{color}" stroke-dasharray="{dash}"/>')

    def save(self,path):
        path.write_text('\n'.join(self.parts+['</svg>'])+'\n',encoding='utf8',newline='\n')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('analysis',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    source=args.analysis.resolve();out=args.output.resolve()
    assert source.is_relative_to(ROOT/'.local-work/d5y')
    assert out.is_relative_to(ROOT) and not out.exists()
    out.mkdir(parents=True)
    read=lambda n:json.loads((source/n).read_text(encoding='utf8'))
    analysis=read('analysis.json');markers=read('checkpoints.json')
    rows=list(csv.DictReader((source/'chronology.csv').open(encoding='utf8')))
    progress=list(csv.DictReader((source/'writer-progress.csv').open(encoding='utf8')))
    for name in ('chronology.csv','writer-progress.csv','pointer-envelopes.csv','conditional-target.csv',
                 'spatial-controls.json','source-depth.csv','requests.csv','replay.json','isolated-pauses.json'):
        shutil.copyfile(source/name,out/name)
    # Only schema/labels and aggregates, without private path/hash inventory.
    summary={k:analysis[k] for k in ('schema','archive_sha256','raw_sha256','identity_sha256','qpc_frequency','t0',
        'span_seconds','authenticated_records','flush_prefixes','kinds','target_positive_records',
        'target_first_positive','target_last_positive','target_deepest_stage','qpc_admission_inversions','terminal')}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8',newline='\n')
    (out/'checkpoints.json').write_text(json.dumps(markers,indent=2)+'\n',encoding='utf8',newline='\n')
    categories=[('Provider',['entry','returned']),('Selected',['selected']),('Visited',['visited']),
                ('Construction',['lookup','descriptor','generating','sample','generated']),
                ('Lifecycle / READY',['fence_begin','fence_end','cold','ready'])]
    svg=SVG('B1 admitted chronology: dense travel-period bursts',
        'Retail primary evidence; 1-second QPC buckets. Empty admitted bins do not establish native inactivity.',760)
    for i,(name,_) in enumerate(categories):
        svg.rect(36+i*225,93,15,15,COLORS[i]);svg.text(57+i*225,106,name)
    def panel(left,top,width,height,lo,hi,ymax,title,ticks):
        sx=lambda x:left+(x-lo)/(hi-lo)*width
        sy=lambda y:top+height-y/ymax*height
        svg.text(left,top-12,title,'sub')
        # Broad loss region is a support envelope, not measured drop timestamps.
        a,b=max(lo,221.517),min(hi,228.259)
        if a<b:svg.rect(sx(a),top,sx(b)-sx(a),height,'#e78a8a',0.18)
        for y in (0,ymax//2,ymax):
            svg.line(left,sy(y),left+width,sy(y),'#d9e0e7');svg.text(left-8,sy(y)+4,y,**{'text-anchor':'end'})
        for row in rows:
            x=int(row['second'])
            if not lo<=x<hi:continue
            acc=0
            for i,(_,kinds) in enumerate(categories):
                value=sum(int(row[k]) for k in kinds)
                svg.rect(sx(x),sy(acc+value),max(1,width/(hi-lo)*0.85),value/ymax*height,COLORS[i]);acc+=value
        for tick in ticks:
            svg.text(sx(tick),top+height+20,tick,**{'text-anchor':'middle'})
        svg.line(left,top+height,left+width,top+height)
        svg.text(left+width/2,top+height+43,'Seconds from first admitted event (QPC)',**{'text-anchor':'middle'})
        svg.text(left,top-31,'Admitted records per 1-second bin')
        return sx
    sx=panel(80,174,1040,150,0,255,6000,'Full session and external checkpoint bounds',[0,50,100,150,200,250])
    for first,last,label in ((53.0659,57.4424,'main menu'),(159.6,165.1588,'loaded / pre-travel'),(245.0537,249.9573,'arrival')):
        svg.rect(sx(first),174,sx(last)-sx(first),150,'#536980',0.1)
        svg.text(sx((first+last)/2),193,label,**{'text-anchor':'middle'})
    svg.line(sx(250.1425),174,sx(250.1425),324,'#b53838','4 3')
    svg.text(1100,391,'STOP at 250.14 s',**{'text-anchor':'end'})
    panel(80,452,1040,160,220,232,6000,'Travel-period detail; peak bin contains 5,445 admitted records',list(range(220,233,2)))
    svg.text(32,685,'Red band: admission-boundary proxy for the lossy portion, not exact loss-time bounds; drop times and types are unknown.')
    svg.text(32,711,'Load and travel transitions are operator reports bounded by checks. No exact transition timestamp is inferred.')
    svg.text(32,737,'Source: capture01.zip / events.bin + authenticated external checkpoints; 19,780 admitted records, 9,957 reported losses.')
    svg.save(out/'chronology.svg')
    svg=SVG('B1 recorder loss and durable writer progress',
        'Retail cumulative counters by flush-ledger ordinal. The horizontal axis is not elapsed time.',700)
    left,top,width,height=85,145,1020,250
    sx=lambda x:left+(x-1)/38*width
    sy=lambda y:top+height-y/20000*height
    for y in (0,5000,10000,15000,20000):
        svg.line(left,sy(y),left+width,sy(y),'#d9e0e7');svg.text(left-10,sy(y)+4,f'{y:,}',**{'text-anchor':'end'})
    for field,color,label in [('records',COLORS[0],'Durable raw prefix'),('drops','#c33d48','Cumulative reported drops')]:
        previous=None
        for row in progress:
            x=sx(int(row['ack_ordinal']));y=sy(int(row[field]))
            if previous:
                svg.line(previous[0],previous[1],x,previous[1],color);svg.line(x,previous[1],x,y,color)
            previous=(x,y)
        svg.text(135 if field=='records' else 490,117,label,'sub',fill=color)
    for x in (1,5,10,15,20,25,30,35,39):svg.text(sx(x),418,x,**{'text-anchor':'middle'})
    svg.text(80,452,'Cumulative maximum FlushFileBuffers duration (raw and ACK calls combined):')
    for row in progress:
        x=sx(int(row['ack_ordinal']));h=float(row['max_flush_ms'])/1300*95
        svg.rect(x,565-h,18,h,'#8555a1')
    svg.text(80,585,'33.82 ms initially; 287.58 ms by ACK 2; 1,206.57 ms by ACK 20. Timing of the maximum call is unresolved.')
    svg.text(80,616,'Queue high-water lower bound reaches 1,024; no retry-exhaustion or output fault. 89 producer retries are reported.')
    svg.text(80,642,'Counter snapshots are non-atomic. ACK metrics precede their own append/flush; their acknowledged field lags one ACK.')
    svg.text(80,668,'39 validated prefixes finalize all admitted records. No lost-event rate or exact queue-occupancy trace is available.')
    svg.save(out/'writer-progress.svg')
    svg=SVG('B1 target observation depth and conditional spatial control',
        'Direct copied identity, conditional attribution and known non-target paths have different evidence strength.',720)
    bands=[(125,'Exact target key: 0:37536:20928:0029d20e','#e9edf2',[
        'No copied target identity in any of the 116 valid source-bearing records.',
        'First / last positive: unavailable. Selection, bypass, lookup and sample identity remain unqualified.',
        'This does not establish zero native executions or zero target selections.']),
        (285,'P20: conditional target candidate; no copied geographic identity','#fff2d5',[
        '228 selections → 228 visited bypasses; 227 status/hazard-valid paired observations.',
        '119 valid singleton-support selections / 97 distinct cells → 119 valid paired bypasses.',
        'First / last singleton selection: 3297 / 10445. No lookup, descriptor or sample for this pointer.',
        'Requires the frozen frame/content/current-Grid premises; losses precede this candidate.']),
        (475,'Byte-identified same-owner non-target controls','#e1f1eb',[
        '24 protected map decisions → 19 misses + 5 hits → 19 consumed descriptors → 19 samples.',
        '19 complete ordinary paths, all owner FormID 0x0005e0de; none has the target source key.',
        'Across 36 selected pointer values, 17 have no source-byte copy; no cross-loss lifetime claim.'])]
    for y,title,color,lines in bands:
        svg.rect(32,y,1136,135 if len(lines)==3 else 163,color)
        svg.text(50,y+27,title,'sub')
        for i,line in enumerate(lines):svg.text(50,y+55+i*25,line)
    svg.text(32,658,'119 singleton paths provide conditional visited-depth evidence, not an authenticated map decision or historical winner.')
    svg.text(32,687,'Frozen B1 outcome remains PARTIAL NATIVE COVERAGE; D5R OPEN. No retry, B2, deployment or publication authority.')
    svg.save(out/'target-depth.svg')
    meta=dict(schema='sor-d5y-figures/1',classification='REVIEW-REQUIRED; publication ON HOLD',
        analysis_sha256=sha(source/'analysis.json'),renderer_sha256=sha(__file__),
        inputs={p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file()},
        replay='Run the same figure command into a fresh ignored directory and compare bytes.',
        geographic_overlay='Omitted: bypass-only invocations lack direct frame/Grid witnesses; historical outpost centre is not a fresh runtime join.')
    (out/'figures.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(output=str(out),files=len(meta['inputs'])),indent=2))


if __name__=='__main__':main()
