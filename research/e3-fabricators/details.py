# SPDX-License-Identifier: GPL-3.0-or-later
"""Detailed saved E3 state/topology; adapts owned E2 selected-state/saved readers.
Reads explicit prior E3 saved receipt, its pinned original, E2 definition cache
and E3 catalogue04. Writes exclusive ignored JSON; decoded scratch is cleaned.
Stdlib/project only. No inventory totals, native execution, save/config/Git writes.
Usage: CPython -B research/e3-fabricators/details.py --sample HIST-0036 --run detail01
"""
import argparse
import collections
import json
from pathlib import Path
import struct
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from catalog import ROOT,pin
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value
from outpost_record_framing import Reader,iter_records
from validate_mature_outposts import directory
from workshop_inventory import reference_prefix,linked_prefix
from research_resource_availability import audit


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--sample',required=True);ap.add_argument('--run',required=True)
    args=ap.parse_args();assert args.run.isalnum() and args.sample.startswith('HIST-') and args.sample[5:].isdigit()
    base=ROOT/'.local-work/e3-fabricators';out=base/(args.run+'.json');assert not out.exists();guard()
    receipt_path=base/'saved01'/(args.sample+'.json');receipt=json.loads(receipt_path.read_text())
    catpath=base/'catalog04.json';cat=json.loads(catpath.read_text())
    cachepath=ROOT/'.local-work/e2-organic/inventory02.json';cache=json.loads(cachepath.read_text())
    definitions={r['formid']:r for r in cache['records']}
    resources={'starfield.esm:'+r['formid'][2:]:r for r in cat['resources']}
    source=Path(receipt['source']['path']);before=pin(source);assert before==receipt['source']
    incoming=collections.defaultdict(list);outgoing=collections.defaultdict(list)
    for s,t in receipt['directed_edges']:incoming[t].append(s);outgoing[s].append(t)
    nodes={x for e in receipt['directed_edges'] for x in e}
    expected={p['reference_identities'][0]:g['resource'] for g in receipt['groups'] for p in g['producers']}
    endpoints={};selected=[]
    with decoded_save(source,base/'scratch-details') as (data,metadata):
        d=directory(data);a,z=d['regions']['reference_u32']
        forms=struct.unpack_from('<'+'I'*d['reference_count'],data,a+4);plugins=plugin_tables(data)
        def resolve(t):return saved_form(token_value(t,forms),plugins)
        fresh=audit(data);producer_resources=collections.defaultdict(list)
        for b in fresh['beacons']:
            for g in b.get('workshop',{}).get('resource_rows',[]):
                for p in g['rows']:producer_resources[p['reference_identities'][0]].append(g['resource_identity'])
        for r in iter_records(data,*d['regions']['region_R3'],d['words'][9]):
            identity=resolve(r['token'])
            if identity not in nodes and identity not in expected:continue
            try:
                case=5 if not r['flags']&0x8000 else 6 if r['flags']&0x02000008 else 4 if r['flags']&6 else 7
                prefix=reference_prefix(data,r,case)
                bidentity=resolve(prefix['base_token']) if prefix['base_token'] else None
                definition=definitions.get(int(bidentity.split(':')[1],16)) if bidentity and bidentity.startswith('starfield.esm:') else None
                kws=[int.from_bytes(bytes.fromhex(v)[i:i+4],'little') for k,v in definition['fields'] if k=='KWDA'
                     for i in range(0,len(bytes.fromhex(v)),4)] if definition else []
                if bidentity in {'starfield.esm:100b62','starfield.esm:219173','starfield.esm:2a6c3b'}:kind='INCOMING_CARGO_BOUNDARY'
                elif bidentity in {'starfield.esm:100b63','starfield.esm:219171','starfield.esm:2a6c3a'}:kind='OUTGOING_CARGO_BOUNDARY'
                elif producer_resources[identity]:kind='LOCAL_PRODUCER_REACHED'
                elif definition and definition['type']=='CONT' and definition['edid'].startswith('OutpostStorage'):kind='STORAGE_BUFFER_BOUNDARY'
                else:kind='UNKNOWN'
                endpoints[identity]=dict(identity=identity,base_identity=bidentity,record_offset=r['offset'],record_end=r['end'],
                    definition=({k:definition[k] for k in ['type','edid','offset']} if definition else None),
                    keywords=[dict(formid=f'{i:08x}',edid=definitions.get(i,{}).get('edid')) for i in kws],
                    classification=kind,producer_resources=producer_resources[identity])
                if identity not in expected:continue
                closure=linked_prefix(data,r,prefix)
                endpoints[identity]['extra_types']=closure['types']
                endpoints[identity]['following_extras']=closure['following_extras']
                av='starfield.esm:'+resources[expected[identity]]['av']['formid'][2:]
                if 0xbf not in closure['types'] and closure['following_extras']=='CLOSED':
                    sheet={f'{i:06x}':v for k,raw in definition['fields'] if k=='PRPS'
                           for i,v,tail in struct.iter_unpack('<IfI',bytes.fromhex(raw))}
                    assert sheet[av.split(':')[1]]==1.0
                    selected.append(dict(identity=identity,resource=expected[identity],selected_av=av,selected_value=1.0,
                        evidence_kind='SAVED_BASE_AND_PRODUCER_CORROBORATED; DEFINITION_DERIVED_AV',
                        record_offset=r['offset'],extra_types=closure['types'],following_extras='CLOSED',
                        base_identity=bidentity,base_definition_offset=definition['offset']))
                    continue
                c=Reader(data,prefix['form_prefix_end'],r['end']);ri=prefix['next_reference_index']
                if r['flags']&0x80:
                    ri+=1
                    if not r['flags']&0xa6031f40:ri+=1
                if r['flags']&0x10:c.take(4)
                count=c.count()
                for extra_index in range(count):
                    bf_offset=c.p;tag=c.take(1)
                    if tag==b'\xbf':break
                    if tag==b'\x84':
                        n=c.count();ri+=n;c.take(n)
                    elif tag in (b'\x45',b'\x83'):ri+=1
                    else:raise ValueError('PRE_BF_EXTRA_UNSUPPORTED_'+tag.hex())
                else:raise ValueError('NO_BF_WITHIN_EXTRA_COUNT')
                sections=[]
                for bits in (1,3):
                    n=c.count();mask=c.take((bits*n+7)//8);tokens=r['refs'][ri:ri+n];assert len(tokens)==n;ri+=n
                    vals=[]
                    for i in range(bits*n):
                        present=bool(mask[i//8]&(1<<(i%8)));off=c.p
                        vals.append(dict(value=struct.unpack('<f',c.take(4))[0] if present else None,offset=off if present else None))
                    sections.append(dict(bits=bits,av_identities=[resolve(t) for t in tokens],values=vals))
                av='starfield.esm:'+resources[expected[identity]]['av']['formid'][2:]
                initial=sections[0]
                if all(av not in s['av_identities'] for s in sections):
                    sheet={f'{i:06x}':v for k,raw in definition['fields'] if k=='PRPS'
                           for i,v,tail in struct.iter_unpack('<IfI',bytes.fromhex(raw))}
                    assert sheet[av.split(':')[1]]==1.0
                    selected.append(dict(identity=identity,resource=expected[identity],selected_av=av,selected_value=1.0,
                        evidence_kind='SAVED_BASE_AND_PRODUCER_CORROBORATED; DEFINITION_DERIVED_AV; NO_BF_OVERRIDE',
                        record_offset=r['offset'],bf_offset=bf_offset,bf_end=c.p,sections=sections,
                        following_extras=closure['following_extras'],base_identity=bidentity,
                        base_definition_offset=definition['offset']))
                    continue
                i=initial['av_identities'].index(av)
                assert initial['values'][i]['value']==1.0,('SAVED_SELECTED_AV_NOT_ONE',initial['values'][i])
                selected.append(dict(identity=identity,resource=expected[identity],selected_av=av,selected_value=1.0,
                    evidence_kind='SAVED_EXPLICIT_BF_BASE_AV',
                    record_offset=r['offset'],bf_offset=bf_offset,bf_end=c.p,sections=sections,
                    following_extras=closure['following_extras']))
            except (ValueError,AssertionError,KeyError,IndexError) as e:
                endpoints.setdefault(identity,dict(identity=identity,record_offset=r['offset'],classification='UNKNOWN'))
                endpoints[identity]['detail_gap']=repr(e)
        traces=[]
        for start,resource in sorted(expected.items()):
            seen={start};q=collections.deque([[start]]);paths=[];cycles=[];adjacency=[]
            required={x['formid']:x for x in resources[resource]['inputs']}
            needed={'starfield.esm:'+x[2:] for x in required}
            while q:
                path=q.popleft();node=path[-1];info=endpoints.get(node,dict(identity=node,classification='UNKNOWN'))
                matches=sorted(needed.intersection(info.get('producer_resources',[])))
                if node!=start and (matches or info['classification'] in ['STORAGE_BUFFER_BOUNDARY','INCOMING_CARGO_BOUNDARY','UNKNOWN']):
                    paths.append(dict(path=path,classification='LOCAL_REQUIRED_PRODUCER_REACHED' if matches else info['classification'],matched_resources=matches))
                if info['classification']=='INCOMING_CARGO_BOUNDARY':continue
                adjacency.append(dict(node=node,incoming=incoming[node]))
                for nxt in incoming[node]:
                    if nxt in path:cycles.append(path+[nxt])
                    elif nxt not in seen:seen.add(nxt);q.append(path+[nxt])
            traces.append(dict(producer=start,selected_resource=resource,required_inputs=list(required.values()),
                current_incoming=incoming[start],current_outgoing=outgoing[start],paths=paths,cycles=cycles,
                visited_adjacency=adjacency,unreached_required_resources=sorted(needed-{x for p in paths for x in p['matched_resources']})))
    assert pin(source)==before
    with out.open('x',encoding='utf8',newline='\n') as f:
        json.dump(dict(source=before,prior=pin(receipt_path),catalogue=pin(catpath),definitions=pin(cachepath),
            tool=pin(Path(__file__)),decoded=metadata,endpoints=endpoints,selected_rows=selected,traces=traces,
            limits=['One BFS witness per reached node; full visited adjacency retained','Boundary recognition is a positive definition join, UNKNOWN elsewhere',
                    'Structural local paths can pass buffers; cargo traversal stops at incoming endpoint',
                    'No inventory amounts, sustained inputs or loaded operation inferred']),f,indent=2);f.write('\n')
    guard();print(json.dumps(dict(endpoints=len(endpoints),selected_rows=len(selected),producers=len(expected),
        required_producer_paths=sum(p['classification']=='LOCAL_REQUIRED_PRODUCER_REACHED' for t in traces for p in t['paths']))))


if __name__=='__main__':main()
