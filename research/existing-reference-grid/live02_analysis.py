# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline supplementary analysis of immutable schema4 evidence.
Reads session raw/journal/health/retirement and frozen predictions through the
qualified inspector. Writes exclusive derivative JSON/CSV only; stdlib/project
code, no process access, native execution, original or model changes.
The original inspector's two-boundary Q pairing includes legitimate kind20
auxiliary records; retain that output and validate complete lifetimes separately.
"""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'runtime/native-oracle-040'))
import route_inspect as r
from build import guard


def diagnostic_lifetimes(events):
    groups={}
    for event in events:groups.setdefault(event['invocation'],[]).append(event)
    qs={i:sorted(g,key=lambda e:e['sequence']) for i,g in groups.items() if any(e['kind'] in (7,8,9) for e in g)}
    es={i:sorted(g,key=lambda e:e['sequence']) for i,g in groups.items() if any(e['kind'] in (10,11,12) for e in g)}
    for i,g in qs.items():
        if [e['kind'] for e in g] not in ([7,8],[7,20,8]):raise ValueError('Q_stages:'+str(i))
        if not r.pair([g[0],g[-1]],7,8,9)[0]:raise ValueError('Q_boundary:'+str(i))
        for a,b in zip(g,g[1:]):
            if a['sequence']>=b['sequence'] or a['qpc']>b['qpc']:raise ValueError('Q_order')
        if any(any(e[k]!=g[0][k] for k in ('invocation','parent','thread','reference','context')) for e in g):raise ValueError('Q_identity')
        children=[v for v in es.values() if v[0]['parent']==i]
        if len(g)==2 and children:raise ValueError('E_without_Q_entry')
        if len(g)==3:
            if len(children)!=1:raise ValueError('Q_entry_without_one_E')
            child=children[0]
            if not (g[1]['sequence']<child[0]['sequence']<child[-1]['sequence']<g[-1]['sequence']):raise ValueError('E_window')
            if not (g[1]['qpc']<=child[0]['qpc']<=child[-1]['qpc']<=g[-1]['qpc']):raise ValueError('E_QPC_window')
    for i,g in es.items():
        if not r.pair(g,10,11,12)[0]:raise ValueError('E_boundary:'+str(i))
        parent=qs.get(g[0]['parent'])
        if parent is None or len(parent)!=3 or g[0]['thread']!=parent[0]['thread']:raise ValueError('E_parent')
    return dict(Q_normal=len(qs),Q_with_E_entry=sum(len(g)==3 for g in qs.values()),E_normal=len(es),diagnostic_lifetimes_complete=True)


def main(session,out):
    guard();session=Path(session);out=Path(out);out.mkdir(exist_ok=True)
    frozen=r.inspect(session);events,integrity=r.records(session)
    lifetimes=diagnostic_lifetimes(events)
    for kind in (22,23,26,28,30,32,33,34):
        if sum(e['kind']==kind for e in events)!=1:raise ValueError('single_route_scope:'+str(kind))
    supplemented=(frozen['worker_complete'] and frozen['retirement_complete'] and not frozen['incomplete_roots']
        and not frozen['unpaired_or_orphan_children'] and all(s['paired_normal'] for s in frozen['selections']) and not (session/'failure.json').exists())
    grid_event=next(e for e in events if e['kind']==33)
    base=r.raw(grid_event,'base',0x30);chosen=r.u64(grid_event,'context_raw',0x18)
    bykind={e['kind']:e for e in events if e['kind'] in (22,23,26,28,30,32,33,34)}
    predictions=json.loads((ROOT/'docs/experiments/engine-oracle/predictions.json').read_text(encoding='utf8'))
    ledger=[]
    for index,p in enumerate(predictions,1):
        ledger.append(dict(row=index,sample=p['source']['sample'],body=p['body'],saved_parent=p['identity']['parent'],
            workshop_id=p['identity']['workshop_id'],cell=json.dumps(p['cell']),center_hex=p['center_hex'],
            applicability='UNASSESSED_NO_SELECTED_OR_SAVED_LOAD_JOIN',frame='UNASSESSED',compensation='NOT_CAPTURED',outcome='NOT_TESTED_GENERIC_COMPONENT_IS_NOT_WORKSHOP_ORACLE'))
    report=dict(original_inspector=frozen,integrity=integrity,diagnostics=lifetimes,
        supplemented_capture_complete=bool(supplemented),
        original_false_positive_invocations=frozen['incomplete_diagnostics'],
        diagnostic_explanation='Each flagged Q has normal7/8 boundaries plus valid kind20 E-entry observation; exactly one nested normal10/11 E. No original receipt is rewritten.',
        kind_counts=dict(sorted(collections.Counter(e['kind'] for e in events).items())),
        Q_return_low32=dict(collections.Counter(r.raw(e,'result',4)[:4].hex() for e in events if e['kind']==8)),
        route_component_replay=r.reconcile(events,int(json.loads((session/'ready.json').read_text(encoding='utf8'))['module_base'],16))['routes'],
        route=dict(eligibility_AL=r.u64(bykind[26],'result')&255,search_return=r.u64(bykind[28],'result'),fallback_return=r.u64(bykind[30],'result'),chosen_reference=chosen,
            chosen_base_formid=hex(struct.unpack_from('<I',base,0x28)[0]),ordinary_base=struct.unpack_from('<I',base,0x28)[0]==0x2c60e9,
            request_angles_hex=r.raw(bykind[22],'source',16)[:16].hex(),final_angles_hex=r.raw(bykind[23],'center',16)[:16].hex(),
            translation_xyz_hex=r.raw(bykind[33],'translation',12).hex(),source_world_pointer=hex(grid_event['blobs']['world']['address']),
            reference_parent_world_pointer=hex(grid_event['blobs']['center']['address']),
            source_world_packed_hex=r.raw(grid_event,'world',0x318)[0x310:0x318].hex(),reference_parent_packed_hex=r.raw(grid_event,'center',0x318)[0x310:0x318].hex(),
            runtime_domains='All pointer values are this session only; base FormID is sampled runtime base identity, never a serialized save token.'),
        frozen_prediction_ledger=ledger,full_native_equivalence='NOT TESTED',selected_SOR003_binding='NOT ESTABLISHED',saved_load_mapping='NOT ESTABLISHED',
        session_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(session.iterdir()) if p.is_file()})
    with (out/'analysis.json').open('x',encoding='utf8',newline='\n') as f:json.dump(report,f,indent=2);f.write('\n')
    with (out/'frozen-predictions.csv').open('x',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(ledger[0]),lineterminator='\n');w.writeheader();w.writerows(ledger)
    print(json.dumps(dict(records=len(events),supplemented_capture_complete=supplemented,diagnostics=lifetimes)))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--session',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();main(a.session,a.out)
