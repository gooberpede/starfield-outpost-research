# D5AO source-informed derivative of d5an_readiness.py under SOR-P-0002.
# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare a proposed N2 source binding; never grants or executes live authority.

Reads the immutable N1 plan, exact D5AO native/package receipts and authored N2
adapters/card. Writes a fresh local source lock, proposal plan and manifest.
Uses the maintainer-owned N1 bundle pinning method under SOR-P-0002 with an
explicit admission-only delta. No deployment, game, protected-file mutation,
Git write, download, prediction amendment or new prediction freeze occurs.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0'):
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B')
import argparse
import copy
import json
from pathlib import Path
import zipfile
import d5ao_n2_operations as operations
import d5ao_n2_stop as trusted
from d5ao_counter_package import RELEASE_CASES
from d5am_lock_qualify import ROOT,guard,sha

OLD=ROOT/'.local-work/d5am/n1-package-reviewed01/n1-plan.json'
OLD_SHA='54aa54665772c90007340bd6467f7b46a305171da910debebd71ea0e2aba6bf8'

def require(value,message):
    if not value:raise RuntimeError(message)

def fresh(path,value):
    with path.open('x',encoding='utf8',newline='\n') as stream:
        json.dump(value,stream,indent=2);stream.write('\n')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('build','package','card','out'):
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--qualification',type=Path,action='append',default=[])
    args=parser.parse_args();build=args.build.resolve();package=args.package.resolve();out=args.out.resolve();card=args.card.resolve()
    require(all(p.is_relative_to(ROOT/'.local-work/d5ao') for p in (build,package,out)),'D5AO local paths required')
    require(not any(p.is_symlink() or p.is_junction() for q in (build,package,out,card) for p in (q,*q.parents)),'Reparse paths refused')
    free=guard();require(sha(OLD)==OLD_SHA,'Original N1 plan changed')
    native=json.loads((build/'build.json').read_bytes());packed=json.loads((package.parent/'package.json').read_bytes())
    dll=build/'SorConstructionWinner.dll'
    require(native['version']=='0.9.3-D5AO-NOT-AUTHORIZED' and native['compilation']==0 and native['source_unchanged'],'Exact D5AO native build required')
    require(len(native['cases'])>=157 and all(c['pass_exit'] and c['exit']==c['expected'] for c in native['cases']),'Full native regression required')
    require(RELEASE_CASES<={c['case'] for c in native['cases']},'All D5AN adverse/integrated controls required')
    require(packed['version']=='0.9.3-D5AO-NOT-AUTHORIZED' and packed['reproduction']['byte_equal'] is True,'Byte-identical package reproduction required')
    require(packed['dll_sha256']==native['dll_sha256']==sha(dll) and packed['archive_sha256']==sha(package),'Candidate byte mismatch')
    require(packed['source_build_sha256']==sha(build/'build.json'),'Package/build binding mismatch')
    with zipfile.ZipFile(package) as archive:
        require(set(archive.namelist())==set(packed['archive_members']),'Package roster mismatch')
        require(archive.read('Data/SFSE/Plugins/SorConstructionWinner.dll')==dll.read_bytes(),'ZIP/DLL differ')
        require(archive.read('COPYING')==(ROOT/'LICENSE').read_bytes(),'GPL text differs')
    plan=copy.deepcopy(json.loads(OLD.read_bytes()))
    old_scope=copy.deepcopy(plan['scope']);old_scope['labels']=['N2']
    require(old_scope==trusted.SCOPE,'Only the finite trial label may change gameplay scope')
    for key in list(plan):
        if key.startswith('d5am_n1_'):del plan[key]
    plan.update(schema=trusted.SCHEMA,trial='N2',scope=trusted.SCOPE,state='PROPOSED_NOT_AUTHORIZED',
        review=dict(state='PENDING_INDEPENDENT_REVIEW'),native_version='0.9.3',
        counter_schema='sor-d5an-counter/1',timestamp_policy=operations.content.POLICY,
        counter_helper_rva=packed['pe_metadata']['exports']['D5AN_counter_next'],
        counter_leave_rva=packed['pe_metadata']['exports']['D5AN_counter_leave'],
        counter_image_bytes=packed['pe_metadata']['image_bytes'],
        dll=str(dll),dll_sha256=sha(dll),fixture_host_sha256=sha(build/'sor-d5x-fixture.exe'),
        run_card_path=str(card),run_card_sha256=sha(card),package_zip=str(package),package_zip_sha256=sha(package),
        install_archive=str(package),install_archive_sha256=sha(package),package_filename=package.name,
        candidate_receipt=str(build/'build.json'),candidate_receipt_sha256=sha(build/'build.json'),
        candidate_package_receipt=str(package.parent/'package.json'),candidate_package_receipt_sha256=sha(package.parent/'package.json'),
        prior_plan_path=str(OLD),prior_plan_sha256=OLD_SHA,
        prospective_trial_decision=dict(state='PENDING_MAINTAINER_DECISION',trial='N2',prediction_mode='HISTORICAL_REFERENCE_ONLY'),
        prediction_decision='N1 frozen prediction is historical. Future trial/prediction binding requires a separate prospective maintainer decision; no new freeze here.')
    prior=ROOT/'.local-work/d5am/live/session-838701ec716cd8bccf0929c4beb9f7e8bfe816b5fb77328007ba9e1cb77b06a8/identity.json'
    identity=json.loads(prior.read_bytes())
    require(sha(prior)=='64ef24ee77740373750824ac07be1f337db64f527f5cd22d51c9c3af2d5345e9','Failed N1 identity changed')
    plan['prior_processes'].append(dict(pid=identity['pid'],creation_filetime=identity['creation_filetime'],nonce=identity['nonce'],identity_sha256=sha(prior),identity_path=str(prior)))
    pins={Path(p):h for p,h in plan['package_pins'].items()}
    pins.update({Path(p):h for p,h in native['inputs'].items()})
    pins.update({build/'candidate'/p:h for p,h in native['derived'].items()})
    pins.update({build/p:h for p,h in native['generated'].items()})
    pins.update({Path(p):h for p,h in packed['inputs'].items()})
    for row in packed['selected_tools'].values():pins[Path(row['path'])]=row['sha256']
    for p in (OLD,prior,dll,package,package.parent/'package.json',build/'build.json',build/'sor-d5x-fixture.exe',card):pins[p]=sha(p)
    qualifications={}
    for given in args.qualification:
        p=given.resolve();require(p.is_relative_to(ROOT/'.local-work/d5ao') and p.suffix=='.json' and p.is_file(),'Task-local qualification receipt required')
        pins[p]=sha(p);qualifications[str(p)]=sha(p)
    for folder in ('runtime/construction-winner','research/resource-retained-population'):
        for p in (ROOT/folder).glob('d5ao*'):
            if p.is_file():pins[p]=sha(p)
    require(all(sha(p)==h for p,h in pins.items()),'Frozen inherited or candidate source changed')
    plan['package_pins']={str(p):h for p,h in sorted(pins.items())}
    plan['offline_qualification_pins']=qualifications
    plan['d5ao_n2_controller_pins']={str(p):sha(p) for p in sorted(trusted.minimal_sources())}
    paths=operations.required_sources()|set(pins)
    lock=dict(schema=operations.POLICY,interpreter=sys.executable,interpreter_sha256=sha(sys.executable),
        dll_sha256=sha(dll),sources={str(p):sha(p) for p in sorted(paths)})
    out.mkdir(parents=True,exist_ok=False);lockpath=out/'d5ao-n2-source-lock.json';fresh(lockpath,lock)
    plan.update(d5ao_n2_source_lock=str(lockpath),d5ao_n2_source_lock_sha256=sha(lockpath))
    operations.verify_plan(plan)
    planpath=out/'n2-plan-proposal.json';fresh(planpath,plan)
    fresh(out/'manifest.json',dict(schema='sor-d5ao-readiness-proposal/1',authority='NONE',
        plan=dict(path=str(planpath),sha256=sha(planpath)),source_lock=dict(path=str(lockpath),sha256=sha(lockpath)),
        historical_prediction_unchanged=True,independent_future_review='REQUIRED',initial_free=free,final_free=guard()))
    print(json.dumps(dict(plan=str(planpath),sha256=sha(planpath),sources=len(paths),authority='NONE')))

if __name__=='__main__':main()
