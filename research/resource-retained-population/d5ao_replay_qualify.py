# SPDX-License-Identifier: GPL-3.0-or-later
# D5AN source-informed owned adaptation of d5am_guard_qualify.py under SOR-P-0002.
"""Check frozen 0.9.3 alias recordings with independent retained readers.

Reads a completed owned candidate and its stopped native fixtures. Writes only
a fresh local receipt and the retained replay method's explicitly mutated copies.
No game, live command, deployment, configuration/save, network or Git write.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import d5am_join_causal as join
from d5am_lock_qualify import ROOT,guard,sha


def require(value,message):
    if not value:
        raise ValueError(message)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('build',type=Path);parser.add_argument('out',type=Path)
    args=parser.parse_args();build=args.build.resolve();out=args.out.resolve()
    require(build.is_relative_to(ROOT/'.local-work/d5ao') and out.is_relative_to(ROOT/'.local-work/d5ao'),'Task-local paths required')
    require(not any(p.is_symlink() or p.is_junction() for p in (build,*build.parents,out,*out.parents)),'No reparse path')
    free=guard();out.mkdir(exist_ok=False)
    receipt=json.loads((build/'build.json').read_bytes())
    require(receipt['version']=='0.9.3-D5AO-NOT-AUTHORIZED' and receipt['source_unchanged'] and receipt['compilation']==0,'Frozen new build required')
    require(len(receipt['cases'])>=157 and all(c['pass_exit'] for c in receipt['cases']),'Completed native regression receipt required')
    dll=sha(build/'SorConstructionWinner.dll');require(dll==receipt['dll_sha256'],'Actual DLL identity')
    inputs={str(build/'build.json'):sha(build/'build.json'),str(Path(__file__)):sha(__file__),str(Path(join.__file__)):sha(join.__file__),sys.executable:sha(sys.executable)}
    support=ROOT/'research/resource-retained-population/d5am_lock_qualify.py';inputs[str(support)]=sha(support)
    for name in ('d5am_read_causal.py','d5am_read_scheduler.py'):
        p=ROOT/'runtime/construction-winner'/name;inputs[str(p)]=sha(p)
    causal=join.load('d5am_read_causal');scheduler=join.load('d5am_read_scheduler')
    results={};checks=[]
    for case in ('alias','overlap','outside','relay','preimage','patch'):
        path=build/('d5am-guard-'+case)
        inventory={str(p):sha(p) for p in path.rglob('*') if p.is_file()};inputs.update(inventory)
        identity=json.loads((path/'identity.json').read_bytes());terminal=json.loads((path/'terminal.json').read_bytes())
        require(identity['retail'] is False and identity['dll_sha256']==dll,'Owned exact producer identity')
        require(identity['geometry_target_guard_basis']=='original32-exact-causal-overlap/1','Declared new guard semantics')
        require((path/'ready.json').is_file(),'Positive startup composition reached READY')
        require(terminal['resident_inert'] is True and terminal['causal_bridge_active']==0,'Owned inert terminal')
        if case=='alias':
            require(terminal['failed'] is False and terminal['output_fault']=='none','Healthy alias producer')
        else:
            require(terminal['failed'] is True and terminal['output_fault']==('geometry_guard' if case=='preimage' else 'causal_or_scheduler_guard'),'Foreign change triggers actual worker guard failure')
        c=causal.read(path,dll);s=scheduler.read(path,dll)
        require(c['integrity']=='AUTHENTICATED_FRAMES','Causal wire framing authenticated')
        if case=='alias':
            require(c['native_bridge_accounting_complete'] and s['native_bridge_accounting_complete'],'Healthy native accounting complete')
        else:
            require(not c['native_bridge_accounting_complete'] and not s['native_bridge_accounting_complete'],'Protective guard failure remains refused by readers')
        results[case]=dict(ready=True,failed=terminal['failed'],output_fault=terminal['output_fault'],resident_inert=True,
                           causal_records=len(c['events']),scheduler_records=len(s['events']),causal=c,scheduler=s)
        checks.append(case+'-actual-ready-guard-terminal-and-readers')
    replay=ROOT/'research/resource-retained-population/d5ao_native_replay.py';inputs[str(replay)]=sha(replay)
    command=[sys.executable,'-E','-B',str(replay),'--native',str(build/'d5am-native-lock'),'--stop',str(build/'d5am-native-stop'),
             '--operand',str(build/'d5am-native-operand'),'--dll-sha256',dll,'--out',str(out/'native-replay')]
    run=subprocess.run(command,capture_output=True)
    (out/'replay.stdout').write_bytes(run.stdout);(out/'replay.stderr').write_bytes(run.stderr)
    require(run.returncode==0,'Retained exact native/STOP/operand111 replay controls')
    require(all(sha(p)==h for p,h in inputs.items()),'All read inputs unchanged')
    result=dict(schema='sor-d5an-guard-replay-qualification/1',result='PASS',dll_sha256=dll,checks=checks,
                inputs=inputs,results=results,native_replay=str(out/'native-replay/qualification.json'),
                free_before=free,free_after=guard(),scope='Owned native composition and retained reader controls; retail startup NOT TESTED')
    with (out/'qualification.json').open('x',encoding='utf8',newline='\n') as stream:
        json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(result='PASS',checks=len(checks),dll_sha256=dll)))


if __name__=='__main__':
    main()
