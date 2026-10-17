# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded historical E3 producer/topology audit, adapted from owned E2 saved.py.
Reads frozen 278-save inventory, hash-pinned originals under 64 MiB decoded and
E3 catalogue. Scans positive outpost-bearing profiles (not Save52 alone); decodes
one at a time using existing cleaned scratch. Writes exclusive ignored per-save
JSON, flushed progress and summary; no original, game, configuration or Git writes.
Stdlib/project readers only. A parser gap is UNKNOWN, never fabricator absence.
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
from research_resource_availability import audit
from stream_save import decoded_save
from extractor_resources import plugin_tables,saved_form
from outpost_membership import token_value
from validate_mature_outposts import directory,envelopes


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);ap.add_argument('--resume',action='store_true');args=ap.parse_args()
    assert args.run.isalnum()
    out=ROOT/'.local-work/e3-fabricators'/args.run;out.mkdir(exist_ok=args.resume)
    catalog_path=ROOT/'.local-work/e3-fabricators/catalog02.json'
    cat=json.loads(catalog_path.read_text())
    manufactured={'starfield.esm:'+r['formid'][2:]:r for r in cat['resources']}
    inventory_path=ROOT/'.local-work/historical-inventory/scan-04/inventory.json'
    inv=json.loads(inventory_path.read_text())
    candidates=[r for r in inv if r.get('depth')=='FULL_BOUNDED_FINGERPRINT' and
                r.get('fingerprint',{}).get('beacon_count',0)>0]
    summary=[]
    with (out/('progress-resume.jsonl' if args.resume else 'progress.jsonl')).open('x',encoding='utf8',newline='\n') as progress:
        for old in candidates:
            guard();source=Path(old['source']['path'])
            previous=out/(old['inventory_id']+'.json')
            if args.resume and previous.exists():
                row=json.loads(previous.read_text())
                assert row['source']['sha256']==old['source']['sha256']
                if source.exists():assert pin(source)==row['source']
                summary.append(dict(inventory_id=old['inventory_id'],status=row['status'],groups=len(row.get('groups',[])),
                    producers=sum(len(g['producers']) for g in row.get('groups',[])),gaps=len(row.get('beacon_gaps',[])),
                    source_sha256=row['source']['sha256']))
                continue
            if not source.exists():
                compact=dict(inventory_id=old['inventory_id'],status='UNAVAILABLE_FROZEN_SOURCE',groups=0,producers=0,gaps=0,
                             source_sha256=old['source']['sha256'])
                summary.append(compact);progress.write(json.dumps(compact)+'\n');progress.flush();continue
            before=pin(source)
            assert before['sha256']==old['source']['sha256'] and before['bytes']==old['source']['size']
            row=dict(inventory_id=old['inventory_id'],source=before,
                     header_versions=old['metadata']['build_strings'])
            try:
                with decoded_save(source,out/'scratch') as (data,metadata):
                    fresh=audit(data);d=directory(data)
                    es=[e for e in envelopes(data,d) if e['qualifies'] and 'parsed' in e]
                    a,z=d['regions']['reference_u32']
                    forms=struct.unpack_from('<'+'I'*d['reference_count'],data,a+4);plugins=plugin_tables(data)
                    def resolve(t):return saved_form(token_value(t,forms),plugins)
                    edges=[(resolve(s),resolve(g['key'])) for e in es for g in e['parsed']['groups'] for s in g['refs']]
                    groups=[dict(owner=b['identity'],resource=g['resource_identity'],
                                 resource_edid=manufactured[g['resource_identity']]['edid'],
                                 count_offset=g['count_offset'],producers=g['rows'])
                            for b in fresh['beacons'] for g in b.get('workshop',{}).get('resource_rows',[])
                            if g['resource_identity'] in manufactured]
                    starts={p['reference_identities'][0] for g in groups for p in g['producers']}
                    incoming=collections.defaultdict(list);outgoing=collections.defaultdict(list)
                    for s,t in edges:incoming[t].append(s);outgoing[s].append(t)
                    traces=[]
                    for start in sorted(starts):
                        seen={start};q=collections.deque([[start]]);paths=[];cycles=[];terminals=[]
                        while q:
                            path=q.popleft();node=path[-1]
                            if node!=start and node in starts:paths.append(path)
                            if not incoming[node]:terminals.append(dict(identity=node,path=path,classification='UNKNOWN_ENDPOINT_TYPE'))
                            for nxt in incoming[node]:
                                if nxt in path:cycles.append(path+[nxt])
                                elif nxt not in seen:seen.add(nxt);q.append(path+[nxt])
                        traces.append(dict(producer=start,incoming=incoming[start],outgoing=outgoing[start],
                                           reached_manufactured_producers=paths,cycles=cycles,terminals=terminals))
                    row.update(decoded=metadata,beacon_count=len(fresh['beacons']),
                               beacon_gaps=[dict(identity=b['identity'],gap=b.get('gap')) for b in fresh['beacons'] if b.get('gap')],
                               groups=groups,traces=traces,directed_edges=edges,
                               status='PARSED_ORDINARY_BEACON_SUBSET')
            except (ValueError,AssertionError,IndexError,KeyError) as e:
                row.update(status='UNKNOWN_PARSER_GAP',error=repr(e))
            assert pin(source)==before
            with (out/(old['inventory_id']+'.json')).open('x',encoding='utf8',newline='\n') as f:
                json.dump(row,f,indent=2);f.write('\n')
            compact=dict(inventory_id=old['inventory_id'],status=row['status'],
                         groups=len(row.get('groups',[])),producers=sum(len(g['producers']) for g in row.get('groups',[])),
                         gaps=len(row.get('beacon_gaps',[])),source_sha256=before['sha256'])
            summary.append(compact);progress.write(json.dumps(compact)+'\n');progress.flush()
            print(json.dumps(compact),flush=True)
    with (out/'summary.json').open('x',encoding='utf8',newline='\n') as f:
        json.dump(dict(inventory=pin(inventory_path),catalogue=pin(catalog_path),tool=pin(Path(__file__)),
                       inventory_count=len(inv),candidate_count=len(candidates),rows=summary,
                       limits=['Ordinary inline-base beacon producer rows only','Historical current saved state, not loaded operation',
                               'No inventory totals or cargo supply traversal','All matching headers are provenance, not executable identity']),f,indent=2);f.write('\n')
    guard()


if __name__=='__main__':main()
