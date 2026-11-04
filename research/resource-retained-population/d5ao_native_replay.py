# SPDX-License-Identifier: GPL-3.0-or-later
# Owned D5AM replay method under SOR-P-0002; separate D5AN-local outputs.
"""Independently replay final owned native/STOP/invalid-operand recordings.

Reads three stopped, non-retail recordings and an external DLL SHA. Writes a
fresh local receipt plus explicitly mutated COPIES for adverse join tests.
Original inventories are checked before/after. Uses stdlib and owned readers;
no native execution, game, live commands, save, database, network or Git writes.
Raw CRC/accounting does not prove coverage; the actual invalid operand must be
preserved and refused semantically. These tests establish no retail frequency.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct
import zlib
import d5am_join_causal as join
from d5ad_baseline import guard,sha

ROOT=Path(__file__).resolve().parents[2]


def require(value,message):
    if not value:
        raise ValueError(message)


def inventory(folder):
    require(not any(p.is_symlink() or p.is_junction() for p in (folder,*folder.parents)),'No reparse input')
    result={}
    for path in sorted(folder.rglob('*')):
        require(not path.is_symlink() and not path.is_junction(),'No reparse member')
        if path.is_file():
            result[path.relative_to(folder).as_posix()]=dict(bytes=path.stat().st_size,sha256=sha(path))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('native','stop','operand','out'):
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--dll-sha256',required=True)
    a=parser.parse_args();out=a.out.absolute()
    require(out.resolve().is_relative_to(ROOT/'.local-work/d5ao') and not out.exists() and
            not any(p.is_symlink() or p.is_junction() for p in (out,*out.parents)),'Fresh non-reparse local output')
    free=guard();out.mkdir()
    source_paths=[Path(__file__),Path(join.__file__),ROOT/'research/resource-retained-population/d5ad_baseline.py']
    source_paths.extend(ROOT/'runtime/construction-winner'/name for name in
        ('d5am_read_causal.py','d5am_read_scheduler.py','read_capture.py','reduce_v3.py','reduce_v4.py',
         'd5ai_read_geometry.py','d5ai_read_lifetime.py'))
    source_pins={str(path):sha(path) for path in source_paths}
    inputs={name:Path(getattr(a,name)).absolute() for name in ('native','stop','operand')}
    before={name:inventory(path) for name,path in inputs.items()}
    for path in inputs.values():
        identity=json.loads((path/'identity.json').read_bytes())
        require(identity['retail'] is False and identity['dll_sha256']==a.dll_sha256,'Only the pinned owned fixtures qualify')
    causal=join.load('d5am_read_causal');scheduler=join.load('d5am_read_scheduler')
    geometry=join.load('d5ai_read_geometry')
    checks=[];results={}
    def check(name,value):
        require(value,name);checks.append(name)
    for name in ('native','stop'):
        path=inputs[name];c=causal.read(path,a.dll_sha256);s=scheduler.read(path,a.dll_sha256);j=join.inspect(path,a.dll_sha256)
        g=geometry.read_session(path)
        check(name+'-native-and-byte-accounting',c['native_bridge_accounting_complete'] and s['native_bridge_accounting_complete'])
        check(name+'-one-exact-native-task-core-join',j['joined']==1 and j['task_joined']==1 and len(j['observations'])==2)
        check(name+'-legacy-mock-path-not-promoted',sum(r['boundary_join']=='INCOMPLETE' for r in j['observations'])==1)
        check(name+'-complete-owned-geometry',not g['errors'] and any(r['complete_representation'] and
              (r['header']['resources'],r['header']['regions'],r['header']['points'])==(3,78,180) for r in g['snapshots']))
        results[name]=dict(causal=c,scheduler=s,joins=j,geometry=[dict(sha256=r['sha256'],complete=r['complete_representation']) for r in g['snapshots']])
    check('controlled-overtaking-native-interval',any(w['interpretation']=='PRIOR_PENDING_WRITER_OVERTAKEN'
          for h in results['native']['causal']['histories'] for w in h['registration_witnesses']))
    for name in ('changed-family','changed-key','consistent-task-request-but-wrong-core'):
        destination=out/name;shutil.copytree(inputs['native'],destination)
        raw=bytearray((destination/'scheduler.bin').read_bytes())
        target=next(e for e in results['native']['scheduler']['events'] if e['kind']==9 and e['allocation'])
        for offset in range(96,len(raw),280):
            payload=bytearray(raw[offset+8:offset+280]);values=struct.unpack('<24Q2i6I6Q',payload)
            if (values[4],values[5])!=(target['node'],target['allocation']):
                continue
            if name=='consistent-task-request-but-wrong-core':
                struct.pack_into('<i',payload,192,values[24]+1)
            elif values[1]==9:
                if name=='changed-family':struct.pack_into('<Q',payload,48,2 if values[6]==1 else 1)
                else:struct.pack_into('<I',payload,200,values[26]^1)
            raw[offset+8:offset+280]=payload;struct.pack_into('<I',raw,offset+4,zlib.crc32(payload))
        (destination/'scheduler.bin').write_bytes(raw)
        replay=join.inspect(destination,a.dll_sha256)
        issue='MAPPED_WORKER_ORIGINAL_REQUEST_MISMATCH' if name.startswith('consistent') else 'RECORDED_TYPED_TASK_HISTORY_UNQUALIFIED'
        check(name+'-refused-despite-valid-CRC-and-clean-producer-status',replay['task_joined']==0 and
              any(issue in r['task_issues'] for r in replay['observations']))
        results[name]=replay
    path=inputs['operand'];raw=(path/'causal.bin').read_bytes();identity=(path/'identity.json').read_bytes()
    check('operand-header-and-identity-binding',len(raw)>=96 and struct.unpack_from('<4Q',raw)==(0x31434c4d41354453,1,128,0) and
          raw[32:96]==hashlib.sha256(identity).hexdigest().encode() and (len(raw)-96)%136==0)
    invalid=[]
    for sequence,offset in enumerate(range(96,len(raw),136),1):
        size,crc=struct.unpack_from('<II',raw,offset);payload=raw[offset+8:offset+136]
        check('operand-frame-'+str(sequence),size==128 and zlib.crc32(payload)==crc and struct.unpack_from('<Q',payload)[0]==sequence)
        row=dict(zip(causal.NAMES,struct.unpack_from('<15Q',payload)))
        if row['kind']==7 and row['status']&4 and row['new_state']==(row['old_state']-1)&0xffffffff:
            invalid.append(row)
    terminal=json.loads((path/'terminal.json').read_bytes())
    check('actual-invalid-delta-retained-with-sticky-failure',len(invalid)==1 and terminal['causal_failed'] is True and
          terminal['causal_written']==(len(raw)-96)//136 and terminal['causal_bridge_active']==0)
    try:
        causal.read(path,a.dll_sha256)
    except ValueError as error:
        check('actual-invalid-delta-reader-refusal',str(error)=='Contradictory recorded atomic operands')
        results['operand']=dict(expected_refusal=str(error),invalid_records=invalid,frames=(len(raw)-96)//136)
    else:
        raise ValueError('Actual unsupported native delta was silently accepted')
    check('all-original-fixture-bytes-preserved',all(inventory(inputs[name])==pins for name,pins in before.items()))
    check('all-method-and-reader-source-bytes-preserved',all(sha(path)==pin for path,pin in source_pins.items()))
    receipt=dict(schema='sor-d5an-actual-replay-qualification/1',result='PASS',checks=checks,inputs=before,
                 input_paths={name:str(path) for name,path in inputs.items()},dll_sha256=a.dll_sha256,
                 method_sha256=sha(__file__),sources=source_pins,
                 interpreter=dict(path=sys.executable,sha256=sha(sys.executable)),
                 results=results,free_before=free,free_after=guard(),
                 scope='Actual owned producer spools plus explicitly mutated derivative copies. Not whole-engine task execution, a retail observation or universal coverage proof.')
    with (out/'qualification.json').open('x',encoding='utf8',newline='\n') as stream:
        json.dump(receipt,stream,indent=2);stream.write('\n')
    print(json.dumps(dict(result='PASS',checks=len(checks),out=str(out))))


if __name__=='__main__':
    main()
