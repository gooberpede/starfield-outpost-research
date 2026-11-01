# SPDX-License-Identifier: GPL-3.0-or-later
"""Independently count final native frames, ACK prefixes and sampled telemetry.

Reads only completed disposable build evidence and exact packaged consumer.
Writes fresh ignored accounting/phase receipts and a source snapshot. Uses
stdlib; no process, native execution, game/save/database/network/Git effect.
Counter snapshots are sampled, not asserted atomic. Exact terminal and host
offer oracles are separate from intermediate ACK consistency observations.
"""
import collections
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import sys
import zlib

ROOT=Path(__file__).resolve().parents[2]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    build,out=[(ROOT/a).resolve() for a in sys.argv[1:3]]
    assert build.is_relative_to(ROOT/'.local-work/d5x')
    assert out.is_relative_to(ROOT/'.local-work/d5ab')
    out.mkdir(parents=True,exist_ok=False)
    (out/'source.py').write_bytes(Path(__file__).read_bytes())
    manifest=json.loads((build/'build.json').read_bytes())
    assert manifest['source_unchanged'] and all(r['pass_exit'] for r in manifest['cases'])
    spec=importlib.util.spec_from_file_location('p3_transport_reader',build/'package-runtime/read_capture.py')
    reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
    dll=sha(build/'package-runtime/SorConstructionWinner.dll')
    rows=[]
    for item in manifest['cases']:
        name=item['case'];session=build/name
        if not (session/'identity.json').exists():continue
        identity=json.loads((session/'identity.json').read_bytes())
        raw=(session/'events.bin').read_bytes()
        kinds=collections.Counter();ticks=[];valid=0
        for offset in range(0,len(raw),328):
            frame=raw[offset:offset+328]
            if len(frame)!=328:break
            magic,size,low,crc=struct.unpack_from('<4I',frame)
            seq,kind=struct.unpack_from('<2Q',frame,16)
            assert magic==0x31505253 and size==312 and seq==identity['sequence_origin']+offset//328+1
            assert low==seq&0xffffffff and crc==zlib.crc32(frame[16:])
            kinds[kind]+=1;ticks.append(struct.unpack_from('<Q',frame,16+5*8)[0]);valid+=328
        acks=[];incoherent=[]
        for line_number,line in enumerate((session/'flush.jsonl').read_bytes().splitlines(),1):
            a=json.loads(line);count=a['records'];end=a['bytes']
            assert end==count*328 and end<=valid
            assert a['prefix_crc32']==zlib.crc32(raw[:end])
            assert a['identity_sha256']==sha(session/'identity.json')
            coherent=(a['drops']==sum(a[k] for k in ('queue_full','contention_exhausted','reentrant_losses'))
                      and a['loss_generation']==a['drops'])
            if not coherent:incoherent.append(line_number)
            acks.append(a)
        result=reader.inspect(session,dll)
        terminal=result['terminal']
        if terminal:
            assert terminal['drops']==sum(terminal[k] for k in ('queue_full','contention_exhausted','reentrant_losses'))
            assert terminal['loss_generation']==terminal['drops']
            assert terminal['acknowledged']<=terminal['flushed']<=terminal['written']<=valid//328
            if not terminal['failed']:
                assert terminal['acknowledged']==terminal['flushed']==terminal['written']==valid//328
        if name in ('normal','representative','burst'):
            assert result['complete_session'] and terminal['drops']==0 and not incoherent
        duration=(max(ticks)-min(ticks))/identity['qpc_frequency'] if len(ticks)>1 else 0
        rows.append(dict(case=name,valid_records=valid//328,raw_bytes=len(raw),
            per_kind=dict(kinds),ack_prefixes=len(acks),sampled_incoherent_ack_lines=incoherent,
            terminal_drops=terminal['drops'] if terminal else None,
            complete_durable_admitted_session=result['complete_session'],
            damage=result['damage'],firstness_refusals=result['firstness_refusals'],
            event_tick_span_seconds=duration,
            retained_records_per_second=(valid//328)/duration if duration else None,
            terminal_metrics=({k:terminal[k] for k in ('worker_timing_ticks','qpc_frequency',
                'queue_high_water_lower_bound','producer_retries','queue_full','contention_exhausted',
                'reentrant_losses','drain_snapshot_high_water')} if terminal else None),
            raw_sha256=sha(session/'events.bin'),ack_sha256=sha(session/'flush.jsonl')))
    result=dict(schema='sor-d5ab-p3-independent-transport-audit/1',passed=True,
        build=str(build),build_sha256=sha(build/'build.json'),method_sha256=sha(__file__),
        scope='Complete original native session bytes; retained rate is not offered or universal retail rate.',
        rows=rows,incoherent_ack_cases=[r['case'] for r in rows if r['sampled_incoherent_ack_lines']])
    (out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(passed=True,sessions=len(rows),incoherent_ack_cases=result['incoherent_ack_cases'])))


if __name__=='__main__':
    main()
