"""SPDX-License-Identifier: GPL-3.0-or-later
Original read-only native-default research census. Reads qualified installed
ESMs through owned reader; writes exclusively new ignored numeric/link receipt.
No class/name predicate for construction; this audits the REFR/ACHR XLKR input
to native reference-default restoration, not a construction detector. No assets,
game/save/database/Git/network writes. Stdlib/project only. Both40GB guards.
"""
import argparse
import collections
import json
import struct
from pathlib import Path
from extractor_resources import qualified
from inspect_outpost_definitions import esm_records
from inventory_historical_saves import ROOT, guard, identity


def scan(paths):
    guard()
    sources=[identity(p) for p in paths]
    headers={}
    for p in paths:
        r,fs=next(esm_records(p,{b'TES4'},repeated=True))
        headers[p.name.lower()]=dict(flags=r['flags'],masters=[v.rstrip(b'\0').decode('utf8').lower()
            for tag,v in fs if tag==b'MAST'])
    flags={k:v['flags'] for k,v in headers.items()}
    counts=collections.Counter();keys=collections.Counter();links=[];malformed=[]
    for p in paths:
        guard();h=headers[p.name.lower()]
        def q(fid):return qualified(p.name.lower(),fid,h['masters'],flags)
        for r,fs in esm_records(p,{b'REFR',b'ACHR'},repeated=True):
            counts[p.name+':'+r['type']]+=1
            for tag,raw in fs:
                if tag!=b'XLKR':continue
                if len(raw)%8:
                    malformed.append(dict(plugin=p.name,offset=r['offset'],size=len(raw)))
                    continue
                for i in range(0,len(raw),8):
                    keyword,target=struct.unpack_from('<II',raw,i)
                    key=q(keyword);keys[key]+=1
                    if key in ('starfield.esm:054ba6','starfield.esm:000191','starfield.esm:000192','starfield.esm:1c5edd'):
                        links.append(dict(reference=q(r['formid']),plugin=p.name,offset=r['offset'],
                            record_type=r['type'],keyword=key,target=q(target),field_relative=i))
        print(p.name,dict(counts),flush=True)
    after=[identity(p) for p in paths]
    if sources!=after:raise ValueError('ESM_SOURCE_CHANGED')
    if malformed:raise ValueError(('XLKR_WIDTH_UNQUALIFIED',malformed))
    return dict(schema='reference-default-link-census/1',sources=sources,counts=dict(counts),
        keyword_counts=[dict(keyword=k,entries=v) for k,v in sorted(keys.items(),key=lambda kv:str(kv[0]))],
        relevant_links=links,workshop_links=[r for r in links if r['keyword']=='starfield.esm:054ba6'],
        malformed=malformed,complete_selected_type_walk=True,
        population_completeness=False,scope='Installed REFR/ACHR XLKR variants; no historical-content equivalence claim')


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--context',type=Path,required=True)
    ap.add_argument('--run',required=True)
    args=ap.parse_args()
    if not args.run.isascii() or not args.run.replace('-','').isalnum():raise ValueError('RUN_NAME')
    ctx=json.loads(args.context.read_text(encoding='utf8'))
    paths=[Path(r['path']) for r in ctx['sources']]
    if [identity(p) for p in paths]!=ctx['sources']:raise ValueError('CONTEXT_SOURCES_CHANGED')
    result=scan(paths)
    out=ROOT/'.local-work/workshop-population-rework'/('default-links-'+args.run+'.json')
    with out.open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
    print('PASS',sum(result['counts'].values()),'reference definitions,',len(result['workshop_links']),'Workshop links')
