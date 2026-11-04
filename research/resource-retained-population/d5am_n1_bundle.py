# SPDX-License-Identifier: GPL-3.0-or-later
"""Prepare fresh NOT_AUTHORIZED D5AM engineering plan; no live actions.

SOR-P-0002 source-informed D5AL bundle pinning. Reads authenticated original
plan, candidate native receipt/ZIP, owned sources and draft card/prediction;
writes only fresh D5AM plan/source snapshots/manifest. Never deploys or grants GO.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without PYTHONOPTIMIZE, -O or -OO')
import argparse
import copy
import hashlib
import importlib.util
import json
import struct
from pathlib import Path
import zipfile
import d5am_n1_stop as trusted
import d5am_n1_operations as operations
from d5ai_episode import ROOT,require,sha,strict_session_json
from common import fresh,guard

BASE=ROOT/'.local-work/d5al/package-final03/episode-b-plan.json'
BASE_SHA='98f3b73f0572f96d9eddce4467368461ebeb920e84dc781f8d6e7d1081093ac2'
BASE_MANIFEST_SHA='2c9425dbf39b8819f68e0e8731653d3cbc455f7e656adf97a01c9fe0a68bd0e2'

def prepare(build,package,card,prediction,out,review=None,review_hash=None):
    require(out.is_relative_to(ROOT/'.local-work/d5am'),'Fresh D5AM bundle output required')
    guard();require(sha(BASE)==BASE_SHA,'Original plan identity changed')
    base_manifest=BASE.with_name('manifest.json')
    require(sha(base_manifest)==BASE_MANIFEST_SHA,'Original D5AL bundle manifest changed')
    retained=json.loads(base_manifest.read_bytes())
    require(retained['new_plan']['sha256']==BASE_SHA and retained['authority']=='NONE','Original plan provenance mismatch')
    native=json.loads((build/'build.json').read_bytes())
    require(native.get('version')=='0.9.1-D5AM' and native.get('compilation')==0 and
            native.get('source_unchanged') is True and len(native.get('cases',[]))==157 and
            all(c.get('pass_exit') is True for c in native['cases']), 'Full 157-case candidate receipt required')
    original_build=ROOT/'.local-work/d5ai-recorder/build16/build.json'
    require(sha(original_build)=='15d10475806aeb593ac7236a48ea1b71f8e3614bf8cdd7e1ded830b0fcdbf457','Original regression roster changed')
    previous_cases=json.loads(original_build.read_bytes())['cases']
    cases={r['case']:r['expected'] for r in previous_cases}
    cases.update({name:0 for name in ('d5am-native-lock','d5am-native-stop','d5am-causal-counter','d5am-causal-loss','d5am-causal-owners','d5am-native-guard','d5am-native-operand')})
    cases.update({name:0 for name in ('d5am-guard-alias','d5am-guard-overlap','d5am-guard-outside','d5am-guard-relay','d5am-guard-preimage','d5am-guard-patch')})
    require(len(native['cases'])==len(cases) and {r['case'] for r in native['cases']}==set(cases) and
            all(r['expected']==r['exit']==cases[r['case']] for r in native['cases']),'Exact regression case/exit roster required')
    dll=build/'SorConstructionWinner.dll'
    require(sha(dll)==native['dll_sha256'],'Candidate DLL receipt mismatch')
    package_receipt=package.parent/'package.json'
    packaged=json.loads(package_receipt.read_bytes())
    require(packaged.get('schema')=='sor-d5am-candidate-package/1' and packaged.get('dll_sha256')==sha(dll) and
            packaged.get('source_build_sha256')==sha(build/'build.json') and
            Path(packaged['archive']).resolve()==package and packaged['archive_sha256']==sha(package) and
            packaged.get('reproduction',{}).get('byte_equal') is True,'Reproduced native package provenance required')
    with zipfile.ZipFile(package) as archive:
        names=archive.namelist();require(len({n.casefold() for n in names})==len(names),'Duplicate ZIP member')
        members=[n for n in names if n.lower().endswith('/sorconstructionwinner.dll')]
        require(len(members)==1 and hashlib.sha256(archive.read(members[0])).hexdigest()==sha(dll),'ZIP DLL differs')
        require(set(names)==set(packaged['archive_members']),'Exact native ZIP member roster required')
        for name,row in packaged['archive_members'].items():
            data=archive.read(name)
            require(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'Native ZIP member changed: '+name)
        require(archive.read('COPYING')==(ROOT/'LICENSE').read_bytes(),'GPL text changed')
    out.mkdir(parents=True,exist_ok=False)
    plan=copy.deepcopy(json.loads(BASE.read_bytes()))
    for key in list(plan):
        if key.startswith(('d5al_','d5ak_','d5aj_','episode_b_','checkpoint_source_lock')) or key in ('episode','controller_pins','phase_pins','operations_sha256','trusted_stop_sha256','checkpoint_method'):
            del plan[key]
    plan.update(schema=trusted.SCHEMA,state='PREDICTION_REVIEW_PENDING_NOT_AUTHORIZED',trial='N1',scope=trusted.SCOPE,
                review=dict(state='PENDING_INDEPENDENT_REVIEW'),native_version='0.9.1',dll=str(dll),dll_sha256=sha(dll),
                live_root=str(trusted.LIVE),run_card_path=str(card),run_card_sha256=sha(card),prediction_path=str(prediction),
                prediction_sha256=sha(prediction),package_zip=str(package),package_zip_sha256=sha(package),
                install_archive=str(package),install_archive_sha256=sha(package),package_filename=package.name,
                timestamp_policy=operations.content.POLICY,causal_schema='sor-d5am-causal/1',
                causal_bridge_admission_schema='sor-d5am-causal-bridge/1',
                scheduler_schema='sor-d5am-scheduler/1',scheduler_event_bytes=272,
                scheduler_bridge_admission_schema='sor-d5am-scheduler-bridge/1',
                scheduler_dispatch_argument_schema='r8-low-byte/1',
                scheduler_ready_serial_schema='consumed-r9/1',
                scheduler_vtable_guard_basis='preferred-image-vtable64/1',
                candidate_receipt=str(build/'build.json'),candidate_receipt_sha256=sha(build/'build.json'))
    plan.update(candidate_package_receipt=str(package_receipt),candidate_package_receipt_sha256=sha(package_receipt))
    # Guard hashes are independently re-read from the exact pinned PE, using
    # the existing owned read-only PE accessor, not copied from an agent report.
    spec=importlib.util.spec_from_file_location('d5am_plan_owned_pe',ROOT/'runtime/retained-population/build.py')
    pe=importlib.util.module_from_spec(spec);spec.loader.exec_module(pe)
    require(sha(pe.GAME/'Starfield.exe')==plan['game_sha256'],'Pinned game mismatch')
    image=(pe.GAME/'Starfield.exe').read_bytes()
    for name,(rvas,sizes) in trusted.EXTRA_RVAS.items():
        plan[name]=[dict(rva=r,bytes=n,guard_sha256=hashlib.sha256(pe.pe_read(image,r,32)).hexdigest()) for r,n in zip(rvas,sizes)]
    plan['scheduler_targets']=[]
    for i,expected in zip([0,1,2,3,9,10],[0x27e5630]*4+[0x76c560,0x7b5160]):
        rva=plan['scheduler_sites'][i]['rva'];call=pe.pe_read(image,rva,5)
        require(call[0]==0xe8,'Original typed call opcode mismatch')
        target=rva+5+struct.unpack_from('<i',call,1)[0]
        require(target==expected,'Original typed worker/registration destination mismatch')
        plan['scheduler_targets'].append(dict(site_index=i,rva=target,guard_sha256=hashlib.sha256(pe.pe_read(image,target,32)).hexdigest()))
    plan['scheduler_vtables']=[dict(rva=r,guard_sha256=hashlib.sha256(pe.pe_read(image,r,32)).hexdigest()) for r in [0x4b3d0e8,0x4b3d138,0x4b406b8]]
    plan['scheduler_callback']=dict(rva=0x27ec2e0,guard_sha256=hashlib.sha256(pe.pe_read(image,0x27ec2e0,32)).hexdigest())
    plan['causal_helpers']=[dict(rva=r,bytes=n,guard_sha256=hashlib.sha256(pe.pe_read(image,r,n)).hexdigest())
                            for r,n in [(0x22cc350,126),(0x22cc3d0,216),(0x2c45a0,81)]]
    originals=[('5ed302aea9da7dc2261163b3dd1816e670a3c2f39891f1ec8d20094afa72b3a1','60ab253002916e04cdce854345dfde49bb539dddea4dcf40f5f690704360beef'),
               ('4da7b6b6ed99fb240b3fd380ad5000e0ba4a39d73301dbff5be919e688e28af6','55244e50d337d4e3d594444c8c9c2e52427c0d69462bd4e6aeb46377672ea742'),
               ('4de28f061a4832dd9aeba105744574669b13fa20ff78c945308097a4c706cb26','91a9a5e2ce3e475c1feac6f2ce504e11d7c6d2e347b60f3a147d442c810a000e')]
    plan['prior_processes']=[]
    for nonce,expected_hash in originals:
        path=ROOT/'.local-work/d5x/live'/('session-'+nonce)/'identity.json';identity=strict_session_json(path)
        require(sha(path)==expected_hash and identity['nonce']==nonce,'Original authenticated process identity changed')
        plan['prior_processes'].append(dict(creation_filetime=identity['creation_filetime'],nonce=identity['nonce'],
                                           identity_sha256=sha(path),identity_path=str(path),pid=identity['pid']))
    failed_path=ROOT/'.local-work/d5am/live/session-318fd7736c2383bf15ee0060e8d20ef3915ec7b3896bf61731102e2554b1acb0/identity.json'
    require(sha(failed_path)=='a2624de5190feeed2cc0d472ad1a273f44747933f3482646cd707bec4c3d53bf','Failed N0 identity changed')
    failed=strict_session_json(failed_path)
    plan['prior_processes'].append(dict(pid=failed['pid'],creation_filetime=failed['creation_filetime'],nonce=failed['nonce'],identity_sha256=sha(failed_path),identity_path=str(failed_path)))
    prior_plan=ROOT/'.local-work/d5am/package-operations-reviewed01/n0-plan.json'
    require(sha(prior_plan)=='e4a29b9820b84a20be9b12a6723080d09c04a065127f1cb88b054eeace82ee6b','Prior N0 plan changed')
    import d5am_operations as prior_operations
    verified_prior=prior_operations.original.pinned_json(prior_plan,sha(prior_plan))
    prior_operations.verify_plan(verified_prior)
    prior_lock=prior_operations.source_pins(verified_prior)
    for field in ('game_sha256','sfse_sha256','save52_name','save52_sha256','deployed_dll','live_root','launch_pins'):
        require(plan[field]==verified_prior[field],'Unchanged protected/launch context differs: '+field)
    expected_scope=copy.deepcopy(trusted.SCOPE);expected_scope['labels']=['N0']
    require(expected_scope==verified_prior['scope'],'Only the trial label may change finite gameplay scope')
    plan.update(geometry_target_guard_basis='original32-exact-causal-overlap/1',
                accepted_disposition_sha256='ef7f24dc597daee786385194515212e79eeba63dfc259b5f63c360904b545d4e',
                prior_plan_path=str(prior_plan),prior_plan_sha256=sha(prior_plan))
    plan['d5am_n1_controller_pins']={str(p):sha(p) for p in sorted(trusted.minimal_sources())}
    # Preserve original package pins and add exact new producer receipt/ZIP/DLL
    # and every actual producer input, without rewriting original sources.
    for p,h in list(plan['package_pins'].items()):require(sha(p)==h,'Original package input changed: '+p)
    candidate_pins={Path(p).resolve():h for p,h in native['inputs'].items()}
    candidate_pins.update({Path(p).resolve():h for p,h in packaged['inputs'].items()})
    for row in packaged['selected_tools'].values():candidate_pins[Path(row['path']).resolve()]=row['sha256']
    candidate_pins.update({build/'candidate'/p:h for p,h in native['derived'].items()})
    candidate_pins.update({build/p:h for p,h in native['generated'].items()})
    for p,h in candidate_pins.items():require(sha(p)==h,'Candidate producer input changed: '+str(p))
    candidate_pins.update({dll:sha(dll),package:sha(package),build/'build.json':sha(build/'build.json'),
                           package_receipt:sha(package_receipt),ROOT/'LICENSE':sha(ROOT/'LICENSE')})
    candidate_pins.update({Path(p).resolve():h for p,h in prior_lock['sources'].items()})
    for key in ('d5am_source_lock','run_card_path','prediction_path'):
        historical=Path(verified_prior[key]).resolve();candidate_pins[historical]=sha(historical)
    qualification_pins={
        'guard-abi02/qualification.json':'cd5270a59072c7c987ec1d022d6450a4a4902a026c72ad4ef29b7f38f1ebaa60',
        'guard-replay02/qualification.json':'1f72c37120847aae4785f3f9bd7e7c40e932abece5a2e577e78814b40cd78413',
        'guard-replay02/native-replay/qualification.json':'a5e2ce867dde88aff59c47c453b6ded789fd19b06607376c44c092b8881caed4',
        'guard-optimization02.json':'6a6caca62bd4c7144831504892c6870fee17f5a4e0c63fbd0bb6d24cc842a1e0',
        'n0-reviews/closure-final01.md':'3134f48909565f23d6e8260754fac9a6a5d2ee592d8751ad43c6fe04eacdc4d4'}
    for name,digest in qualification_pins.items():
        path=ROOT/'.local-work/d5am'/name
        require(sha(path)==digest,'Corrected candidate qualification changed: '+name)
        candidate_pins[path]=digest
    candidate_pins[prior_plan]=sha(prior_plan)
    disposition=ROOT/'docs/experiments/resource-retained-population/d5am-maintainer-disposition-2026-11-04.md'
    require(sha(disposition)==plan['accepted_disposition_sha256'],'Historical accepted disposition changed')
    candidate_pins[disposition]=sha(disposition)
    host=build/'sor-d5x-fixture.exe';candidate_pins[host]=sha(host)
    plan['fixture_host_sha256']=sha(host)
    for item in plan['prior_processes']:
        candidate_pins[Path(item['identity_path'])]=item['identity_sha256']
    for stem,name in [('measurement','d5am-n1-measurement-adjudication.md'),
                      ('native_observation_rules','d5am-observation-adjudication.md')]:
        scientific=ROOT/'docs/experiments/resource-retained-population'/name
        candidate_pins[scientific]=sha(scientific)
        plan[stem+'_path']=str(scientific);plan[stem+'_sha256']=sha(scientific)
    plan['package_pins'].update({str(p):h for p,h in candidate_pins.items()})
    paths=operations.required_sources()|{Path(p).resolve() for p in plan['package_pins']}
    if review is not None or review_hash is not None:
        require(review is not None and review_hash is not None,'Both review receipt path/hash required')
        decision=operations.original.pinned_json(review,review_hash)
        require(decision.get('schema')=='sor-d5am-n1-readiness-review/1' and
                decision.get('verdict')=='ACCEPT_N1_TECHNICAL_READINESS' and
                decision.get('scope')=='D5AM_N1_0.9.1_READINESS' and
                decision.get('accepted_disposition_sha256')==plan['accepted_disposition_sha256'],
                'Exact scoped technical review required; historical full-contract AC01 failure cannot be erased')
        for key,value in [('prediction_sha256',sha(prediction)),('run_card_sha256',sha(card)),
                          ('dll_sha256',sha(dll)),('candidate_receipt_sha256',sha(build/'build.json'))]:
            require(decision.get(key)==value,'Reviewed freeze mismatch: '+key)
        require(decision.get('sources')=={str(p):sha(p) for p in sorted(paths)},'Review must bind exact entire source/input closure')
        plan.update(state='N1_TECHNICALLY_REVIEWED_REQUIRES_PREFLIGHT_AND_SESSION_GO',
                    review=dict(state='INDEPENDENTLY_REVIEWED_N1_TECHNICAL_ACCEPT',scope=decision['scope'],
                    receipt_path=str(review),receipt_sha256=review_hash,prediction_sha256=sha(prediction),run_card_sha256=sha(card)))
        plan['package_pins'][str(review)]=review_hash;paths.add(review)
    lock=out/'d5am-n1-source-lock.json'
    fresh(lock,dict(schema=operations.POLICY,interpreter=sys.executable,interpreter_sha256=sha(sys.executable),
                    dll_sha256=sha(dll),sources={str(p):sha(p) for p in sorted(paths)}))
    plan.update(d5am_n1_source_lock=str(lock),d5am_n1_source_lock_sha256=sha(lock))
    operations.verify_plan(plan)
    path=out/'n1-plan.json';fresh(path,plan)
    for source in sorted(paths|{card,prediction}):
        if not source.is_relative_to(ROOT) or source.suffix.lower() not in ('.py','.h','.cpp','.asm','.md','.json','.txt'):continue
        target=out/'source-snapshot'/source.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('xb') as stream:stream.write(source.read_bytes())
    fresh(out/'manifest.json',dict(schema='sor-d5am-n1-bundle/1',authority='NONE',state=plan['state'],
          plan=dict(path=str(path),sha256=sha(path)),original_plan=dict(path=str(BASE),sha256=BASE_SHA),
          original_manifest=dict(path=str(base_manifest),sha256=BASE_MANIFEST_SHA),
          candidate=dict(path=str(build/'build.json'),sha256=sha(build/'build.json')),files={p.relative_to(out).as_posix():
          dict(bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(out.rglob('*')) if p.is_file()}))
    return path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('build','package','card','prediction','out'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--review',type=Path);p.add_argument('--review-sha256')
    a=p.parse_args();path=prepare(*(getattr(a,n).resolve() for n in ('build','package','card','prediction','out')),
                                a.review.resolve() if a.review else None,a.review_sha256)
    print(json.dumps(dict(plan=str(path),sha256=sha(path),authority='NONE')))

if __name__=='__main__':main()
