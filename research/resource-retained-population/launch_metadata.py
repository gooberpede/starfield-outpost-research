# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare a review-required Plugins.txt timestamp derivative, never a live GO.

Reads an existing offline preflight, one fixed configuration file and the existing
lightweight admission guards. Writes one exclusive task-local derivative only
after validation. A verified temporary candidate is removed from task scratch.
No launch, attachment, process mutation, configuration/save write or Git effect.
The independent exact-derivative review and separate Phase B GO remain mandatory.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import time
from build import LOCAL,pin
from collect_native import admission_checks
from prepare_native import SOURCE
from preservation_native import PREFLIGHT_SCHEMA

KNOWN=Path('C:/Users/User/AppData/Local/Starfield/Plugins.txt')


def normalized(path):
    return os.path.normcase(os.path.normpath(str(path)))


def amend(pre, observed, provenance):
    """Change exactly one mtime guard, preserving content and launch chronology."""
    assert pre['schema']==PREFLIGHT_SCHEMA and pre['status']=='OFFLINE_CHECKED_NOT_AUTHORIZED'
    assert pre['source']==SOURCE and 'launch_metadata_bridge' not in pre
    guards=[k for k in pre['file_guards'] if normalized(k)==normalized(KNOWN)]
    config=[k for k in pre['config'] if normalized(k)==normalized(KNOWN)]
    assert len(guards)==len(config)==1, 'Exact known Plugins.txt identity required'
    key=guards[0]; original=pre['file_guards'][key]
    assert set(observed)=={'bytes','mtime_ns','sha256'}
    assert observed['bytes']==original['bytes'] and observed['sha256']==pre['config'][config[0]], 'Content change refused'
    assert observed['mtime_ns']!=original['mtime_ns'], 'No timestamp bridge needed'
    out=copy.deepcopy(pre)
    out['file_guards'][key]=dict(original,mtime_ns=observed['mtime_ns'])
    out['launch_metadata_bridge']=dict(schema='sor-d5m-launch-metadata/1',state='REVIEW_REQUIRED_NOT_EXECUTION_AUTHORITY',
        path=key,original_guard=original,observed=observed,provenance=provenance)
    return out


def other_metadata(pre):
    """Refuse every other metadata difference, including loose backup guards."""
    def same(path,expected):
        current=Path(path).stat()
        assert current.st_size==expected['bytes'] and current.st_mtime_ns==expected['mtime_ns'], ('Additional guard mismatch',path)
    for field in ('file_guards','installed','archive_guard'):
        for name,row in pre.get(field,{}).items():
            if field=='file_guards' and normalized(name)==normalized(KNOWN):continue
            same(name,row)
    for candidates in pre.get('backups',{}).values():
        for row in candidates:
            if row['kind']=='LOOSE_BACKUP':same(row['path'],row['metadata'])


def self_test(output):
    before=dict(schema=PREFLIGHT_SCHEMA,status='OFFLINE_CHECKED_NOT_AUTHORIZED',source=SOURCE,
        created_filetime_100ns=123,config={str(KNOWN):'a'*64},file_guards={str(KNOWN):dict(bytes=480,mtime_ns=1),'unrelated':dict(bytes=7,mtime_ns=9)})
    observed=dict(bytes=480,mtime_ns=2,sha256='a'*64); original=copy.deepcopy(before)
    after=amend(before,observed,dict(synthetic=True)); restored=copy.deepcopy(after)
    restored.pop('launch_metadata_bridge');restored['file_guards'][str(KNOWN)]['mtime_ns']=1
    checks=dict(only_one_guard_changed=restored==before,original_immutable=before==original,
        original_prelaunch_time_retained=after['created_filetime_100ns']==123,
        review_not_authority=after['launch_metadata_bridge']['state']=='REVIEW_REQUIRED_NOT_EXECUTION_AUTHORITY')
    for name,change in [('changed_hash',dict(sha256='b'*64)),('changed_size',dict(bytes=481)),('unchanged_time',dict(mtime_ns=1))]:
        try:amend(before,dict(observed,**change),{})
        except AssertionError:checks[name+'_refused']=True
        else:checks[name+'_refused']=False
    changed=copy.deepcopy(before);changed['launch_metadata_bridge']={}
    try:amend(changed,observed,{})
    except AssertionError:checks['second_bridge_refused']=True
    else:checks['second_bridge_refused']=False
    output.parent.mkdir(parents=True,exist_ok=True)
    scratch=Path(tempfile.mkdtemp(prefix='d5m-bridge-test-',dir=output.parent)).resolve();assert scratch.is_relative_to(LOCAL)
    other=scratch/'other.bin'
    try:
        other.write_bytes(b'1234567');stat=other.stat()
        fixture=dict(file_guards={str(KNOWN):dict(bytes=480,mtime_ns=1),str(other):dict(bytes=7,mtime_ns=stat.st_mtime_ns)})
        other_metadata(fixture);checks['other_guards_checked']=True
        other.write_bytes(b'changed-size')
        try:other_metadata(fixture)
        except AssertionError:checks['additional_guard_change_refused']=True
        else:checks['additional_guard_change_refused']=False
    finally:
        assert scratch.resolve().is_relative_to(LOCAL)
        other.unlink(missing_ok=True);scratch.rmdir()
    with output.open('x',encoding='utf8',newline='\n') as f:
        json.dump(dict(synthetic_only=True,no_target_operations=True,checks=checks,method_sha256=pin(__file__)),f,indent=2);f.write('\n')
    assert all(checks.values());print(len(checks),'timestamp-bridge controls PASS; no execution authority')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--preflight',type=Path);p.add_argument('--output',type=Path);p.add_argument('--self-test',type=Path)
    a=p.parse_args()
    if a.self_test:
        output=a.self_test.resolve();assert output.is_relative_to(LOCAL);self_test(output);return
    assert a.preflight and a.output
    source,output=a.preflight.resolve(),a.output.resolve()
    assert source.is_relative_to(LOCAL) and output.is_relative_to(LOCAL) and source!=output and not output.exists()
    assert min(shutil.disk_usage(d).free for d in ('C:/','D:/'))>=40000000000
    raw=source.read_bytes();source_sha256=hashlib.sha256(raw).hexdigest();before=json.loads(raw)
    stat1=KNOWN.stat(); digest=pin(KNOWN); stat2=KNOWN.stat()
    assert (stat1.st_size,stat1.st_mtime_ns)==(stat2.st_size,stat2.st_mtime_ns), 'Configuration changed during read'
    provenance=dict(original_preflight=dict(path=str(source),sha256=source_sha256),method_sha256=pin(__file__),
        recorded_filetime_100ns=time.time_ns()//100+116444736000000000,
        scope='Only known Plugins.txt mtime; original launch timestamp and all byte expectations retained')
    after=amend(before,dict(bytes=stat2.st_size,mtime_ns=stat2.st_mtime_ns,sha256=digest),provenance)
    other_metadata(before)
    output.parent.mkdir(parents=True,exist_ok=True)
    candidate=Path(tempfile.mkdtemp(prefix='d5m-metadata-',dir=output.parent)).resolve();assert candidate.is_relative_to(LOCAL)
    temp=candidate/'candidate.json'
    try:
        data=(json.dumps(after,indent=2)+'\n').encode('utf8');temp.write_bytes(data)
        # In-memory validation-shaped fields invoke no collector main, process
        # operation, GO-file creation or consumption. All existing light guards
        # must pass; no other metadata mismatch receives an exception.
        gate=dict(status='GO',phase='B',source=SOURCE,synthetic=True,
            approval_reference='SYNTHETIC GUARD VALIDATION ONLY; NO AUTHORITY',cloud_confirmed=True,used=False,
            creation_filetime_100ns=before['created_filetime_100ns']+1,
            run_card=before['run_card'],build_manifest=before['build_manifest'],preflight=dict(path=str(temp),sha256=pin(temp)),
            allowed_interventions=['software_int3_14','all_stop_and_peer_suspend','owned_rip_tf_rearm','termination_teardown'])
        admission_checks(gate)
        assert pin(source)==source_sha256
        with output.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    finally:
        assert candidate.resolve().is_relative_to(LOCAL)
        temp.unlink(missing_ok=True);candidate.rmdir()
    assert pin(source)==provenance['original_preflight']['sha256']
    print('Derivative prepared; independent exact review required before admission:',output,pin(output))


if __name__=='__main__':main()
