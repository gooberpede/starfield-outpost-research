# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline readiness audit; never grants GO, launches, attaches or restores saves.

Reads active archive-backed scientific pins, protected saves/backup records,
Steam metadata, installed inputs, build and qualification. Writes fresh ignored
receipts and one Save52 restoration rehearsal COPY. Stdlib and owned helpers.
No game, original, configuration, analysis-project, network or Git mutations.
"""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from build import ROOT,LOCAL,pin
from verify_native import sites
from preservation_native import verify_build_files, PREFLIGHT_SCHEMA
from reliability_contract import MODES

GAME=Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
LIVE=Path('C:/Users/User/Documents/My Games/Starfield/Saves')
CARD=ROOT/'docs/experiments/resource-retained-population/run-card-d5m-v1.md'
SOURCE='0:37536:20928:0029d20e'
EXE='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
ESM='1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
BA2='2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5'


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def write(path,value):
    with path.open('x',encoding='utf8',newline='\n') as s:
        json.dump(value,s,indent=2);s.write('\n');s.flush();os.fsync(s.fileno())


def full_preservation(out):
    sys.path.insert(0,str(ROOT/'research/resource-query-reachability'))
    m=load('d5l_remaining','research/resource-query-reachability/remaining_inputs.py');m.LOCAL=out
    write(out/'start.json',dict(head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),index_sha256=pin(ROOT/'.git/index')))
    argv=sys.argv
    try:sys.argv=['remaining_inputs.py',str(out/'remaining-inputs.json')];m.main()
    finally:sys.argv=argv
    sys.path.insert(0,str(ROOT/'research/resource-carinae-source-context'))
    protection=load('d5l_protection','research/resource-carinae-source-context/protection.py')
    from save_policy import load_policy,policy_hash,snapshot,partition
    # The old protection.audit enters the strict removed-ZIP namespace census.
    # Use the just-completed scoped surviving-input proof; never repair or waive
    # that strict FAIL. Authenticate archive rows for independent backup lookup.
    from cutover import trusted_configuration,transaction
    tx=transaction(trusted_configuration())
    with tx.store.authenticated() as (entry,archive,members):
        archived={os.path.normcase(os.path.normpath(str(ROOT/r['path']))):r['sha256'] for r in entry['rows']}
        archive_guard={str(f):dict(bytes=f.stat().st_size,mtime_ns=f.stat().st_mtime_ns) for f in (archive,tx.store.index)}
    audit=json.loads((out/'remaining-inputs.json').read_text());policy=load_policy()
    sync=protection.sync_snapshot(policy);write(out/'sync-audit.json',sync)
    assert not audit['protected_policy_differences'] and audit['live_comparison']['ok'] and sync['scientific_inputs_match'] and not sync['other']
    previous_sync=json.loads((ROOT/'.local-work/resource-carinae/sync-paths-preflight02.json').read_text())
    sync['historical_remotecache_sha256']=previous_sync['remotecache_sha256']
    # Preserve the historical failed comparison; metadata identity is diagnostic
    # under the prospective amendment, never a new scientific input baseline.
    live=snapshot(LIVE,policy);protected=partition(live,policy)['protected']
    old=json.loads((ROOT/'.local-work/resource-carinae-source-context/protected-before.json').read_text())
    backups={}
    for name,row in protected.items():
        candidates=[]
        for r in old:
            p=Path(r['path'])
            if p.name!=name or not p.is_relative_to(ROOT/'.local-work') or r['sha256']!=row['sha256']:continue
            key=os.path.normcase(os.path.normpath(str(p)))
            actual=archived.get(key) if key in archived else pin(p) if p.is_file() else None
            if actual==row['sha256']:candidates.append(dict(path=str(p),sha256=actual,kind='AUTHENTICATED_ARCHIVE_MEMBER' if key in archived else 'LOOSE_BACKUP',metadata=None if key in archived else dict(bytes=p.stat().st_size,mtime_ns=p.stat().st_mtime_ns)))
        assert candidates,('No verified independent protected backup',name)
        backups[name]=candidates
    save52=next(n for n in policy['designated'] if n.startswith('Save52_'))
    backup=next(Path(r['path']) for r in backups[save52] if r['kind']=='LOOSE_BACKUP')
    shutil.copyfile(backup,out/'restore-rehearsal.sfs');assert pin(out/'restore-rehearsal.sfs')==protected[save52]['sha256']
    known={str(Path(r['path'])):r['sha256'] for r in old}
    definitions={str(p):pin(p) for p in (GAME/'Data').iterdir() if p.suffix.lower() in ('.esm','.esp','.esl')}
    assert set(definitions)=={p for p in known if Path(p).parent==GAME/'Data' and Path(p).suffix.lower() in ('.esm','.esp','.esl') and known[p] is not None}
    config={}
    for folder in (GAME,LIVE.parent,Path('C:/Users/User/AppData/Local/Starfield')):
        for p in folder.iterdir():
            if p.is_file() and (p.suffix.lower()=='.ini' or p.name.lower() in ('plugins.txt','loadorder.txt')):config[str(p)]=pin(p)
    assert set(config)=={p for p in known if Path(p).parent in (GAME,LIVE.parent,Path('C:/Users/User/AppData/Local/Starfield')) and (Path(p).suffix.lower()=='.ini' or Path(p).name.lower() in ('plugins.txt','loadorder.txt')) and known[p] is not None}
    assert all(known[p]==h for p,h in (definitions|config).items())
    assert pin(GAME/'Starfield.exe')==EXE and pin(GAME/'Data/Starfield.esm')==ESM
    ba=GAME/'Data/Starfield - PlanetData.ba2';assert pin(ba)==BA2
    return dict(save_policy=policy,save_policy_sha256=policy_hash(policy),protected_live=protected,live_path=str(LIVE),save52=save52,
        backups=backups,archive_guard=archive_guard,sync=sync,definitions=definitions,config=config,
        file_guards={f:dict(bytes=Path(f).stat().st_size,mtime_ns=Path(f).stat().st_mtime_ns) for f in definitions|config},
        installed={str(p):dict(sha256=pin(p),bytes=p.stat().st_size,mtime_ns=p.stat().st_mtime_ns) for p in (GAME/'Starfield.exe',GAME/'Data/Starfield.esm',ba)},
        restore_rehearsal_sha256=pin(out/'restore-rehearsal.sfs'))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('build','qualification','sites'):p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--name',required=True);a=p.parse_args();assert re.fullmatch('[a-z0-9-]+',a.name)
    assert subprocess.check_output(['powershell','-NoProfile','-Command','@(Get-Process Starfield -ErrorAction SilentlyContinue).Count'],text=True).strip()=='0'
    assert min(shutil.disk_usage(d).free for d in ('C:/','D:/'))>=40_000_000_000
    out=LOCAL/a.name;out.mkdir(exist_ok=False);build=a.build.resolve();assert build.is_relative_to(LOCAL)
    manifest=json.loads((build/'build.json').read_text());assert manifest['exit_code']==0
    operational_sources=verify_build_files(manifest)
    q=json.loads((a.qualification/'results.json').read_text());assert len(q)==len(MODES) and all(r['passed'] for r in q)
    assert {r['mode'] for r in q}==set(MODES), 'Complete D5M qualification required'
    assert len({r['mode'] for r in q})==len(q) and all(r['build_sha256']==pin(build/'build.json') for r in q)
    verified=sites(build,a.sites.resolve());write(out/'sites.json',verified)
    result=full_preservation(out)
    result.update(schema=PREFLIGHT_SCHEMA,status='OFFLINE_CHECKED_NOT_AUTHORIZED',source=SOURCE,
        operational_sources=operational_sources,
        code_pins={str(f):pin(f) for folder in (Path(__file__).parent,ROOT/'research/resource-carinae-source-context') for f in folder.glob('*.py')},
        created_filetime_100ns=time.time_ns()//100+116444736000000000,
        build_manifest=dict(path=str(build/'build.json'),sha256=pin(build/'build.json')),
        qualification=dict(path=str(a.qualification.resolve()/'results.json'),sha256=pin(a.qualification/'results.json')),
        run_card=dict(path=str(CARD),sha256=pin(CARD)),cloud_current='UNKNOWN_REQUIRES_FRESH_OPERATOR_CONFIRMATION',
        free_bytes={d:shutil.disk_usage(d).free for d in ('C:/','D:/')})
    write(out/'preflight.json',result);print(out,'offline only')


if __name__=='__main__':main()
