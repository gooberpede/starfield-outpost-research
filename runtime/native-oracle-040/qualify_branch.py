# SPDX-License-Identifier: GPL-3.0-or-later
"""Read disposable actual wrapper output; write exclusive synthetic case journals
and decoder qualification receipt. No game/process access or original mutation.
"""
import json
from pathlib import Path
import sys
from inspect_events import SIZE,decode,digest,inspect
from branch_inspect import analyze

def main():
    source=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(exist_ok=False)
    data=source.read_bytes();assert len(data)%SIZE==0
    chunks=[data[i:i+SIZE] for i in range(0,len(data),SIZE)]
    decoded=[decode(b) for b in chunks]
    roots=[e for e in decoded if e['kind']==7 and e['parent']==0]
    assert len(roots)==12
    expected=['FALLBACK_NULL','FALLBACK_TYPE_NOT_56','OVERLAY_NULL','LANDSCAPE_NULL_STATIC_PATH',
              'HIERARCHY_MISMATCH_AT_0x0','OVERLAY_BIT0_CLEAR_STATIC_PATH','E_ENTERED','E_ENTERED',
              'capture_incomplete_or_unhealthy','capture_incomplete_or_unhealthy',
              'OVERLAY_BIT0_CLEAR_STATIC_PATH','OVERLAY_BIT0_CLEAR_STATIC_PATH']
    receipt=[]
    for i,root in enumerate(roots):
        stop=next(e['sequence'] for e in decoded if e['invocation']==root['invocation'] and e['kind'] in (8,9))
        parts=[b for b,e in zip(chunks,decoded) if root['sequence']<=e['sequence']<=stop]
        case=out/str(i);case.mkdir();(case/'events.bin').write_bytes(b''.join(parts))
        rows=[]
        for j,b in enumerate(parts):
            e=decode(b);rows.append(dict(offset=j*SIZE,length=SIZE,sha256=digest(b),**{k:e[k] for k in ('sequence','invocation','kind')}))
        (case/'records.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows),encoding='utf8')
        (case/'ready.json').write_text(json.dumps(dict(component='SorNativePositionOracle',version='0.3.0',schema=3,event_size=SIZE,synthetic=True)),encoding='utf8')
        report=analyze(inspect(case));actual=report['rows'][0]
        assert actual['reason']==expected[i],(i,actual)
        if i in (7,10):assert actual['final_delta']==[-17,23]
        receipt.append(dict(case=i,expected=expected[i],actual=actual,raw_sha256=digest(b''.join(parts))))
    (out/'qualification.json').write_text(json.dumps(dict(input_sha256=digest(data),cases=receipt,native_equivalence='NOT_TESTED'),indent=2)+'\n',encoding='utf8')
    print('PASS 12 actual wrapper output cases through journal/hash/schema/ancestry/path decoder')
if __name__=='__main__':main()
