# SPDX-License-Identifier: GPL-3.0-or-later
"""Compare the complete compiled producer at the two smaller queue capacities.

Reads a final 32,768-cell build and exact current owned sources. Calls the owned
build recipe for disposable 1,024/8,192-cell normal/representative/burst hosts.
Writes fresh ignored builds/receipts only. No game, saves, deployment, database,
network or Git mutation. Existing compiler/SDK/stdlibrary; no new dependency.
Counts/CRC/ACK authentication uses the exact packaged independent reader.
"""
import collections
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    final=(ROOT/sys.argv[1]).resolve()
    label=sys.argv[2]
    assert label.replace('-','').isalnum()
    out=ROOT/'.local-work/d5ab'/label
    out.mkdir(parents=True,exist_ok=False)
    baseline=json.loads((final/'build.json').read_bytes())
    assert baseline['queue_capacity']==32768 and baseline['source_unchanged']
    assert all(sha(p)==digest for p,digest in baseline['inputs'].items())
    builds={32768:final}
    commands=[]
    for capacity in (1024,8192):
        env=dict(os.environ,SOR_QUEUE_CAPACITY=str(capacity))
        command=[sys.executable,'-B',str(ROOT/'runtime/construction-winner/build.py'),
                 label+'-'+str(capacity),'normal','representative','burst']
        result=subprocess.run(command,cwd=ROOT,env=env,capture_output=True)
        (out/(str(capacity)+'.stdout')).write_bytes(result.stdout)
        (out/(str(capacity)+'.stderr')).write_bytes(result.stderr)
        commands.append(dict(command=command,capacity=capacity,exit=result.returncode))
        assert result.returncode==0,commands[-1]
        builds[capacity]=ROOT/'.local-work/d5x'/(label+'-'+str(capacity))
    rows=[]
    for capacity,build in sorted(builds.items()):
        manifest=json.loads((build/'build.json').read_bytes())
        assert manifest['inputs']==baseline['inputs'] and manifest['source_unchanged']
        assert all(r['pass_exit'] for r in manifest['cases'])
        dll=sha(build/'package-runtime/SorConstructionWinner.dll')
        spec=importlib.util.spec_from_file_location('p3_capacity_reader',build/'package-runtime/read_capture.py')
        reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
        for name in ('normal','representative','burst'):
            session=build/name
            result=reader.inspect(session,dll)
            raw=(session/'events.bin').read_bytes()
            kinds=collections.Counter(reader.decode(raw[i+16:i+328])['kind'] for i in range(0,len(raw),328))
            terminal=result['terminal']
            assert terminal['failed'] is False and terminal['output_faults']==0
            assert result['durable_records']==len(raw)//328
            assert not set(result['damage'])-{'LOSS_TELEMETRY_INCOMPLETE_OR_CONTRADICTORY'}
            assert terminal['drops']==sum(terminal[k] for k in ('queue_full','contention_exhausted','reentrant_losses'))
            assert terminal['written']==terminal['flushed']==terminal['acknowledged']==len(raw)//328
            offered=None
            if name in ('representative','burst'):
                oracle=json.loads((session/'host-offers.json').read_bytes())
                expected=[0]*18
                for kind in (*range(1,10),16,17):expected[kind]=1
                expected[10]=expected[11]=expected[12]=1
                expected[13]=12002 if name=='burst' else 2
                expected[14]=expected[15]=1
                if name=='representative':
                    for kind in (*range(1,10),16):expected[kind]=2001
                    expected[17]=1025
                    expected[10]=expected[11]=6
                    expected[12]=2
                    expected[14]=expected[15]=5
                assert oracle['per_kind']==expected and oracle['total']==sum(expected)
                offered=oracle['total']
                assert offered==len(raw)//328+terminal['drops']
                assert all(kinds[k]<=expected[k] for k in range(18))
                if not terminal['drops']:assert dict(kinds)=={k:n for k,n in enumerate(expected) if n}
            if terminal['drops'] or result['damage']:
                assert not result['chains']
            if result['damage']:
                assert not result['reset_scoped_chains']
            # These envelopes were declared by P2. Smaller capacities are
            # deliberate capacity counterexamples, not declared lossless runs.
            if capacity==32768:
                assert terminal['drops']==0 and not result['firstness_refusals']
            if name=='representative' and capacity==32768:
                assert set(kinds)==set(range(1,18))
            rows.append(dict(capacity=capacity,scenario=name,build=str(build),dll_sha256=dll,
                records=len(raw)//328,category_records=dict(kinds),
                independent_offered_records=offered,
                source_build_sha256=sha(build/'build.json'),
                metrics={k:terminal[k] for k in ('drops','queue_full','contention_exhausted','reentrant_losses',
                    'queue_high_water_lower_bound','worker_timing_ticks','cell_bytes','capacity',
                    'qpc_frequency','drain_snapshot_high_water')},
                raw_sha256=sha(session/'events.bin'),ack_sha256=sha(session/'flush.jsonl'),
                complete_durable_admitted_prefix=result['durable_records']==len(raw)//328,
                complete_session=result['complete_session'],damage=result['damage'],
                firstness_refusals=result['firstness_refusals']))
    assert all(sha(p)==digest for p,digest in baseline['inputs'].items())
    receipt=dict(schema='sor-d5ab-p3-integrated-capacity/1',passed=True,commands=commands,
                 inputs=baseline['inputs'],method_sha256=sha(__file__),rows=rows,
                 scope='Finite emulated-host complete producer workloads; not a universal retail lossless rate.')
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(passed=True,runs=len(rows),out=str(out))))


if __name__=='__main__':
    main()
