# SPDX-License-Identifier: GPL-3.0-or-later
"""Challenge D5AJ qualification using copies of authenticated D5AK A0 history.

SOR-P-0002 adaptation of D5AJ qualification methods. Reads the successful retained
A0 raw stream, creates in-memory adverse histories and fresh local receipts.
No original bytes, native execution, save, process, deployment or network writes.
These tests establish predicate refusal, not new observed engine histories.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without PYTHONOPTIMIZE, -O or -OO')
import argparse
import copy
from pathlib import Path
import d5al_baseline as baseline
import d5aj_reduce as scoped
from d5ae_baseline import ROOT,guard
sys.path.insert(0,str(ROOT/'runtime/session-tools'))
from common import fresh


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('out',type=Path);a=p.parse_args()
    out=a.out.resolve();baseline.require(out.is_relative_to(ROOT/'.local-work/d5al'),'New D5AL output required');guard();out.mkdir(parents=True,exist_ok=False)
    report=scoped.inspect(baseline.SESSION,baseline.DLL,baseline.TARGET,0x5e0de)
    observation=next(v for v in report['observations'] if v['envelope']['snapshot_id']=='1')
    snapshot=scoped.d5ai_read_geometry.read_session(baseline.SESSION)['snapshots'][0]
    events=report['events'];target=observation['proof']['source'];h=snapshot['header'];tests=[]
    def check(name,condition,basis):
        tests.append(dict(name=name,passed=bool(condition),basis=basis));baseline.require(condition,name)
    check('actualA0-crosses-source-disjoint-grid-pairs',len(target['continuity']['crossed'])==9,'ACTUAL successful A0 interpreted by versioned D5AJ')
    def refuse(name,mutate):
        ev=copy.deepcopy(events);sn=copy.deepcopy(snapshot);li=copy.deepcopy(report['lifetime']);mutate(ev,sn,li)
        try:
            envelope,proof=scoped.envelope(sn,ev,report['session_id'],baseline.TARGET)
            proof['lifetime_coverage']=scoped.d5ai_read_lifetime.qualify_snapshot(sn,li)
            scoped.qualify_construction(proof,li)
        except (ValueError,KeyError):check(name,True,'SYNTHETIC in-memory adverse copy of actual A0')
        else:check(name,False,'SYNTHETIC in-memory adverse copy of actual A0')
    find=lambda ev,seq:next(e for e in ev if e['sequence']==seq)
    fence=target['continuity']['crossed'][0]['begin'];birth=target['birth_sequence'];pub=target['publication_sequence']
    def field(seq,key,value):return lambda ev,sn,li:find(ev,seq).__setitem__(key,value)
    for name,key,value in (('owning-grid-clear','proc',target['owning_grid']),('map-erase','a',2),('retirement','a',4),('procgen-clear','a',0),('procgen-destruction','a',1),('owner-replacement','a',5),('manager-reset','a',6),('unknown-grid-origin','proc',0),('exceptional-fence','status',16),('ambiguous-fence-overlap','hazards',2),('unexplained-epoch','epoch',1000)):
        refuse(name,field(fence,key,value))
    refuse('missing-source-birth',lambda ev,sn,li:ev.remove(find(ev,birth)))
    refuse('missing-publication',lambda ev,sn,li:ev.remove(find(ev,pub)))
    refuse('missing-fence-begin',lambda ev,sn,li:ev.remove(find(ev,fence)))
    def aba(ev,sn,li):
        a=copy.deepcopy(find(ev,birth));b=copy.deepcopy(find(ev,pub));a.update(sequence=max(e['sequence'] for e in ev)+1,selection=999999,ticks=h['ticks_begin']-100);b.update(sequence=a['sequence']+1,ticks=h['ticks_begin']-90);ev.extend((a,b))
    refuse('pointer-reallocation-ABA',aba)
    generation = observation['proof']['generation']
    generate_sequence = generation['generate_sequence']
    descriptor = next(e for e in events if e['kind'] == 5 and e['invocation'] == generation['invocation'] and e['selection'] == generation['selection'])
    for name, seq, field_name, wrong in (('wrong-generating-owner', generate_sequence, 'a', 0), ('wrong-generating-holder', generate_sequence, 'd', 0), ('wrong-generating-proc', generate_sequence, 'proc', 0), ('wrong-consumed-descriptor', descriptor['sequence'], 'descriptor', '00' * 44)):
        refuse(name, field(seq, field_name, wrong))
    for name,field_name,wrong in (('wrong-consumer-owner','owner_formid',1),('wrong-boundary-kind','boundary',1),('missing-consumer','consumer',0),('missing-manager','manager',0),('missing-procgen','proc',0),('incomplete-consumer-scan','scan_result',0),('capture-loss','loss',1)):
        refuse(name,lambda ev,sn,li,key=field_name,wrong=wrong:sn['header'].__setitem__(key,wrong))
    refuse('nonfinite-query',lambda ev,sn,li:sn['header'].__setitem__('query_hex','0000c07f'+sn['header']['query_hex'][8:]))
    refuse('incomplete-representation',lambda ev,sn,li:sn.__setitem__('complete_representation',False))
    other=next(v for v in snapshot['holders'] if v['source_pointer']!=target['source_pointer'])
    other_id=scoped.source_identity(events,other['source_pointer'],h)
    refuse('unknown-occupied-holder',lambda ev,sn,li:ev.remove(find(ev,other_id['birth_sequence'])))
    refuse('lifetime-cutoff',lambda ev,sn,li:li.__setitem__('qualified_from_ticks',h['ticks_begin']))
    def content_event(kind, allocation):
        def mutate(ev, sn, li):
            begin = dict(li['events'][0], kind=kind, allocation=allocation, phase='BEGIN', invocation=999999, thread=999999, ticks=h['ticks_begin']-10)
            li['events'].extend([begin, dict(begin, phase='END', ticks=h['ticks_begin']-5)])
        return mutate
    refuse('holder-resource-map-ending',content_event('HOLDER_RESOURCE_MAP',observation['proof']['holder_pointer']))
    refuse('collection-geometry-ending',content_event('COLLECTION_GEOMETRY',observation['proof']['collection_pointers'][0]))
    refuse('collection-geometry-mutation',content_event('COLLECTION_MUTATION',observation['proof']['collection_pointers'][0]))
    fresh(out/'qualification.json',dict(status='PASS',tests=tests,source=str(baseline.SESSION),scope='Actual initial A0 positive; adverse event/snapshot/lifetime copies are synthetic predicate controls; no new native histories'))
    print({'status':'PASS','checks':len(tests)})

if __name__=='__main__':main()
