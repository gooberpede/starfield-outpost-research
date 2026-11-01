# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise the unchanged schema-4 predicate using disposable event copies.

Reads the retained owned P3 normal capture and current owned reducers. Writes
exclusive local JSON only. No native execution or protected-file effects.
Uses SOR-P-0002 P1/P3 event-fixture methods; these are synthetic semantic
controls, not additional B2 observations. Requires Python -E -B and stdlib.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Invoke Python with -E -B')
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
import read_capture as reader
import reduce_v4 as reducer


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('out', type=Path)
    args = p.parse_args()
    if not args.out.resolve().is_relative_to(ROOT / '.local-work/d5ac'):
        raise ValueError('Local outputs only')
    path = ROOT / '.local-work/d5x/p3-native-final04/normal/events.bin'
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '35dfc013c059f98602549fdfe92b3e43df45352b69e09100eb37c4b5a37ccc4c'
    base = [reader.decode(raw[i+16:i+328]) for i in range(0, len(raw), 328)]
    results = []
    def at(es, kind):
        return next(e for e in es if e['kind'] == kind)
    def case(name, mutate, expected=0, loss=(0, 0)):
        es = copy.deepcopy(base)
        mutate(es)
        value = reducer.reduce(es, reader.reduce, reader.source_key, *loss)
        assert len(value['chains']) == expected, (name, value)
        results.append(dict(case=name, expected=expected, actual=len(value['chains']),
                            diagnostics=value['diagnostics'], events=es, loss=loss))
    def omit(es, kinds):
        es[:] = [e for e in es if e['kind'] not in kinds]
        for i, e in enumerate(es, 1):
            e['sequence'] = i
    case('valid-reset-triad', lambda es: None, 1)
    case('wrong-reset-owner', lambda es: [e.update(proc=e['proc']+8) for e in es if e['kind'] in (10,11,12)])
    case('missing-reset-unlock', lambda es: omit(es, (12,)))
    case('missing-reset-end', lambda es: omit(es, (11,)))
    case('unmatched-epoch', lambda es: at(es,12).update(epoch=999))
    case('constructor-empty-without-reset-witness', lambda es: omit(es, (10,11,12)))
    case('reset-end-after-entry-native-time', lambda es: at(es,11).update(ticks=at(es,1)['ticks']+1))
    case('cross-thread-reset-end', lambda es: at(es,11).update(thread=999))
    case('cross-thread-store', lambda es: at(es,17).update(thread=999))
    case('changed-owner-at-store', lambda es: at(es,17).update(proc=at(es,17)['proc']+8))
    case('omitted-essential-publication', lambda es: omit(es, (15,)))
    case('loss-through-store', lambda es: None, loss=(1,17))
    def earlier(es, collision=False, lookup=False):
        visit = at(es,3)
        prefix = [copy.deepcopy(at(es,k)) for k in (1,2,3)]
        for e in prefix:
            e.update(invocation=100, selection=101 if e['kind']!=1 else 0,
                     ticks=visit['ticks']-10+e['kind'])
        if collision:
            birth=copy.deepcopy(at(es,14)); pub=copy.deepcopy(at(es,15))
            birth.update(source=birth['source']+0x1000, selection=999)
            pub.update(source=birth['source'])
            for e in prefix:
                if e['kind']!=1:e['source']=birth['source']
            prefix=[birth,pub]+prefix
        if lookup:
            e=copy.deepcopy(at(es,4)); e.update(invocation=100,selection=101,ticks=visit['ticks']-6)
            prefix.append(e)
        pos=next(i for i,e in enumerate(es) if e['kind']==1)
        es[pos:pos]=prefix
        for i,e in enumerate(es,1):e['sequence']=i
    case('earlier-eligible-decision', earlier)
    case('earlier-map-access', lambda es: earlier(es,lookup=True))
    case('content-token-collision', lambda es: earlier(es,collision=True))
    def retirement(es):
        e=copy.deepcopy(at(es,10));e.update(a=3,thread=999,ticks=at(es,3)['ticks']+1,
                                           sequence=es[-1]['sequence']+1)
        es.append(e)
    case('retirement-delayed-admission', retirement)
    # A standalone lock/state oracle challenges the preferred lookup explanation.
    # Native exclusive intervals serialize lookup, insertion, generation and store.
    schedules = [
        dict(case='both-unvisited-miss-insert-store-hit', actions=['check-A','check-B','miss-B','insert-B','store-B','hit-A'], expect=True),
        dict(case='hit-without-insertion-from-empty', actions=['check-A','check-B','miss-B','hit-A'], expect=False),
        dict(case='different-pointer-insertion', actions=['check-A','check-B','miss-B','insert-C','hit-A'], expect=False),
        dict(case='erase-between-insert-and-hit', actions=['check-A','check-B','miss-B','insert-B','erase','hit-A'], expect=False)]
    for s in schedules:
        present=False; valid=True
        for action in s['actions']:
            if action=='insert-B':present=True
            if action=='erase':present=False
            if action=='hit-A' and not present:valid=False
        assert valid==s['expect']
        s['actual']=valid
    args.out.mkdir(parents=True, exist_ok=False)
    value=dict(input=str(path.relative_to(ROOT)), input_sha256=hashlib.sha256(raw).hexdigest(),
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               reducer_sha256=hashlib.sha256(Path(reducer.__file__).read_bytes()).hexdigest(),
               cases=results, schedules=schedules, passed=len(results)+len(schedules))
    (args.out/'controls.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(dict(passed=value['passed'], input_sha256=value['input_sha256'])))


if __name__ == '__main__':
    main()
