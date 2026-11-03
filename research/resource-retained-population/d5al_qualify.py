# SPDX-License-Identifier: GPL-3.0-or-later
"""Focused D5AL guard tests on isolated owned files and guarded Python entries.

Reads actual candidate sources and emits fresh local fixture/negative receipts.
Runs Python refusal/help subprocesses only, no game, deployment, original-save
write or network. SOR-P-0002 adapts the D5AK content and interpreter controls.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without PYTHONOPTIMIZE, -O or -OO')
import argparse
import ast
import json
from pathlib import Path
import subprocess
import d5al_operations as operations


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('out',type=Path)
    a=p.parse_args()
    out=a.out.resolve()
    operations.require(out.is_relative_to(operations.ROOT/'.local-work/d5al'),'D5AL output required')
    free=operations.guard()
    out.mkdir(parents=True,exist_ok=False)
    checks=[]; commands=[]
    def check(name,value):
        checks.append(dict(name=name,passed=bool(value)))
        operations.require(value,name)
    def refuse(name,fn):
        try: fn()
        except (ValueError,AssertionError,OSError): check(name,True)
        else: check(name,False)
    from common import guard as disk_floor
    for drive in ('C:/','D:/'):
        refuse('floor-refuses-'+drive,lambda drive=drive:disk_floor(query=lambda name:39_999_999_999 if name==drive else 40_000_000_000))
        def failed_query(name,drive=drive):
            if name==drive:raise OSError('owned injected caller-available query failure')
            return 40_000_000_000
        refuse('query-failure-refuses-'+drive,lambda:disk_floor(query=failed_query))
    check('exact-both-drive-floor-accept',disk_floor(query=lambda name:40_000_000_000)=={'C:/':40_000_000_000,'D:/':40_000_000_000})
    guard=operations.content.content_guard
    for label in ('configuration','definition','installed'):
        file=out/(label+'.owned'); file.write_bytes(b'owned same-metadata guard bytes')
        pin=operations.sha(file); st=file.stat(); row=dict(bytes=st.st_size,mtime_ns=st.st_mtime_ns)
        check(label+'-unchanged-positive-hash',guard(file,row,pin)['content_sha256_verified']==pin)
        os.utime(file,ns=(st.st_atime_ns,st.st_mtime_ns+2_000_000_000))
        check(label+'-timestamp-only-accept',guard(file,row,pin)['timestamp_changed'])
        original_sha=operations.content.sha
        def touching_sha(path):
            digest=original_sha(path)
            for offset in range(1,5):
                os.utime(path,ns=(st.st_atime_ns,st.st_mtime_ns+offset*2_000_000_000))
            return digest
        operations.content.sha=touching_sha
        try:
            unstable=guard(file,row,pin)
            check(label+'-repeated-metadata-changes-during-positive-content-read-accept',unstable['metadata_unstable_during_read'] and unstable['content_sha256_verified']==pin)
        finally:operations.content.sha=original_sha
        replaced=file.with_suffix('.prior-inode');replacement=file.with_suffix('.replacement-inode')
        def replacing_sha(path):
            digest=original_sha(path);data=path.read_bytes();path.rename(replaced);path.write_bytes(data);return digest
        operations.content.sha=replacing_sha
        try:refuse(label+'-identity-replacement-refused-even-equal-bytes',lambda:guard(file,row,pin))
        finally:
            operations.content.sha=original_sha
            file.rename(replacement);replaced.rename(file)
        file.write_bytes(b'X'+file.read_bytes()[1:]); os.utime(file,ns=(st.st_atime_ns,st.st_mtime_ns))
        refuse(label+'-equal-length-same-metadata-changed-bytes',lambda:guard(file,row,pin))
        file.unlink(); refuse(label+'-missing-file',lambda:guard(file,row,pin))
    clis=['d5al_episode.py','d5al_operations.py','d5al_stop.py','d5al_archive.py','d5al_bundle.py','d5al_qualify.py','d5al_baseline.py','d5al_baseline_qualify.py','d5al_integration_qualify.py','d5al_closeout_qualify.py','d5al_scope_qualify.py','d5al_compare_qualify.py']
    for name in clis:
        path=Path(__file__).with_name(name)
        for flags,env_value,success in ((['-E','-B'],'',True),(['-E','-B'],'1',False),(['-B'],'1',False),(['-E','-B','-O'],'',False),(['-E','-B','-OO'],'',False)):
            env=dict(os.environ,PYTHONOPTIMIZE=env_value)
            for mode in ('help','effect') if not success else ('help',):
                sentinel=out/(name+str(len(commands))+'.must-not-exist')
                args=['--help'] if mode=='help' else ['invalid-operation','--out',str(sentinel)]
                result=subprocess.run([sys.executable,*flags,str(path),*args],env=env,capture_output=True)
                refused=result.returncode!=0 and (b'Use' in result.stderr or b'optimization' in result.stderr)
                check(name+' '+str(flags)+' env='+env_value+' '+mode,(result.returncode==0 if success else refused) and not sentinel.exists())
                commands.append(dict(cli=name,flags=flags,PYTHONOPTIMIZE=env_value,mode=mode,exit=result.returncode,stdout=result.stdout.decode(errors='replace'),stderr=result.stderr.decode(errors='replace')))
    audit=[]
    for path in sorted(operations.required_sources()):
        if path.suffix=='.py':
            tree=ast.parse(path.read_text(encoding='utf8'))
            assertions=[n for n in ast.walk(tree) if isinstance(n,ast.Assert)]
            audit.append(dict(path=str(path),sha256=operations.sha(path),assertions=len(assertions),call_bearing=[n.lineno for n in assertions if any(isinstance(x,ast.Call) for x in ast.walk(n.test))]))
    operations.fresh(out/'qualification.json',dict(status='PASS',checks=checks,commands=commands,assertion_inventory=audit,free=free,limits='Owned file and actual subprocess entry controls; no retail observation or full protection audit.'))
    print(json.dumps(dict(status='PASS',checks=len(checks))))

if __name__=='__main__':main()
