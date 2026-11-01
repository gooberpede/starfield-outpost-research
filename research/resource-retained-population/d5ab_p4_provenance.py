# SPDX-License-Identifier: GPL-3.0-or-later
"""Revalidate unchanged P3 candidate evidence for the current P4 admission.

Adapted from owned d5ab_p3_provenance.py under SOR-P-0002.
Origin SHA-256: 090bd915e99d0b0ef9533c553f8cb8fd33d235eb9ca7c4466d6176a18ad5f2b8.

Reads an explicit local qualification plan, completed receipts, source snapshots,
installed pins, unchanged analysis databases and historical preservation records.
Writes fresh ignored verification output and selected authored test metadata.
No game/process/save/database/Git mutation, network or new dependency. Owned
P1 provenance/receipt methods adapted under SOR-P-0002; hashes prove identity,
not semantics, test coverage or review acceptance.
"""

import sys

# Safety checks below require assertions, including when imported as a helper.
if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')
import csv
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[2]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def main():
    plan_path=(ROOT/sys.argv[1]).resolve()
    out=(ROOT/sys.argv[2]).resolve()
    assert plan_path.is_relative_to(ROOT/'.local-work/d5ab')
    assert out.is_relative_to(ROOT/'.local-work/d5ab')
    out.mkdir(parents=True,exist_ok=False)
    plan=read(plan_path)
    baseline=read(ROOT/'.local-work/d5ab/p4/baseline.json')
    free={d:shutil.disk_usage(d).free for d in ('C:/','D:/')}
    assert min(free.values())>=40_000_000_000
    assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==baseline['head']
    assert sha(ROOT/'.git/index')==baseline['index_sha256']
    build=ROOT/plan['build'];repro=ROOT/plan['reproduction']
    native,reproduction=read(build/'build.json'),read(repro/'build.json')
    assert len(native['cases'])==len({r['case'] for r in native['cases']})==90
    assert {r['case'] for r in reproduction['cases']}=={
        'normal','p3-positive-bypass','p3-unwind-probe','p3-store-access-fault'}
    for folder,data in ((build,native),(repro,reproduction)):
        assert data['compilation']['pass_exit'] and data['source_unchanged']
        assert all(r['pass_exit'] for r in data['cases'])
        assert all(sha(p)==digest for p,digest in data['inputs'].items())
        assert all(sha(folder/p)==digest for p,digest in data['outputs'].items())
    assert native['inputs']==reproduction['inputs']
    dll=sha(build/'package-runtime/SorConstructionWinner.dll')
    assert dll==sha(repro/'package-runtime/SorConstructionWinner.dll')
    names=('read_capture.py','reduce_v3.py','reduce_v4.py','controller.py','worker_health.py')
    for name in names:
        assert sha(build/'package-runtime'/name)==sha(ROOT/'runtime/construction-winner'/name)
    installed=read(ROOT/'.local-work/d5x/identity05/identity.json')
    for p,digest in {**installed['installed'],**installed['database']}.items():
        assert sha(p)==digest,p
    preservation=read(ROOT/'.local-work/d5ab/p2-provenance02/preservation.json')
    for item in preservation:
        p=ROOT/item['path']
        assert p.exists()==item['exists'],item['path']
        if item['exists']:
            assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],item['path']
    with (ROOT/'docs/experiments/resource-retained-population/d5ab-p1-sources.csv').open(encoding='utf8') as stream:
        exports={row['path']:row['sha256'] for row in csv.DictReader(stream)}
    for p,digest in exports.items():
        assert sha(ROOT/p)==digest,p
    receipts={}
    mandatory={'native','original-reader','p3-reader','controller','sharing','queue',
               'capacity','protection','query-join','legacy','worker','original-instructions','bridge-abi','transport-audit','erase-proof'}
    assert mandatory <= set(plan['receipts']), 'Missing mandatory qualification receipt'
    for role,name in plan['receipts'].items():
        path=ROOT/name;data=read(path)
        assert not data.get('failures',[]),role
        if 'passed' in data:assert data['passed'] is True,role
        if 'source_unchanged' in data:assert data['source_unchanged'] is True,role
        for p,digest in data.get('inputs',{}).items():
            assert sha(ROOT/p)==digest,(role,p)
        if role=='queue':
            assert len(data['results'])==9
            assert all(r['passed'] and r['lossless_losses']==0 for r in data['results'])
        if role=='controller':
            assert len(data['results'])==26
            for row in data['results']:
                child=ROOT/row['receipt']
                assert sha(child)==row['receipt_sha256']
                assert read(child)['passed'] and read(child)['source_unchanged']
        if role=='original-reader':assert data['final_build_consumer_match'] and data['tests']==316
        if role=='p3-reader':assert data['final_packaged_consumer_match']
        if role=='native':assert data['development'] is False and data['build_sha256']==sha(build/'build.json')
        methods={
            'native':('script_sha256','research/resource-retained-population/d5ab_p3_native_qualify.py'),
            'capacity':('method_sha256','research/resource-retained-population/d5ab_p3_capacity.py'),
            'transport-audit':('method_sha256','research/resource-retained-population/d5ab_p3_transport_audit.py'),
            'query-join':('method_sha256','research/resource-retained-population/d5ab_p3_query_join.py'),
            'worker':('script_sha256','runtime/construction-winner/worker_health.py'),
            'bridge-abi':('source_sha256','research/resource-retained-population/d5ab_p3_bridge_abi.py'),
            'original-instructions':('source_sha256','research/resource-retained-population/d5ab_p1_native_controls.py')}
        if role in methods:
            field,method=methods[role]
            assert data[field]==sha(ROOT/method),(role,field)
        if role=='protection':
            assert data['driver_sha256']==sha(ROOT/'research/resource-retained-population/d5ab_p3_protection.py')
            assert data['method_sha256']==sha(ROOT/'research/resource-carinae-source-context/save_policy.py')
            assert data['policy_sha256']==sha(ROOT/'research/resource-carinae-source-context/save_policy.json')
            assert data['common_guard_sha256']==sha(ROOT/'runtime/session-tools/common.py')
        if role=='bridge-abi':
            assert data['object_sha256']==sha(build/'bridges.obj')
            assert len(data['checks'])==13 and all(data['checks'].values())
        if role=='erase-proof':
            assert data['method_sha256']==sha(ROOT/'.local-work/d5ab/p3/erase-tail-proof.py')
            assert data['pe_reader_sha256']==sha(ROOT/'runtime/retained-population/build.py')
        count_unit={
            'native':(len(data.get('rows',[])),'native checks'),
            'original-reader':(data.get('tests'),'consumer checks'),
            'p3-reader':(data.get('tests'),'consumer checks'),
            'controller':(len(data.get('results',[])),'worker/controller scenarios'),
            'sharing':(1,'sharing control'), 'queue':(len(data.get('results',[])),'compiled queue runs'),
            'capacity':(len(data.get('rows',[])),'scenario/capacity combinations'),
            'protection':(len(data.get('rows',[])),'disposable guard controls'),
            'query-join':(len(data.get('facts',[])),'static instruction facts'),
            'legacy':(data.get('tests'),'semantic checks'),
            'worker':(len(data.get('cases',[])),'own-thread controls'),
            'original-instructions':(len(data.get('rows',[])),'original-instruction controls'),
            'bridge-abi':(len(data.get('checks',{})),'object ABI checks'),
            'transport-audit':(len(data.get('rows',[])),'native sessions audited'),
            'erase-proof':(None,'static guard/def-use proof')}
        count,unit=count_unit[role]
        receipts[role]=dict(path=name,sha256=sha(path),count=count,unit=unit)
    baseline_sources={n.replace('\\','/'):digest for n,digest in baseline['inputs'].items()}
    expected_unchanged={'runtime/construction-winner/'+name for name in (
        'observer.h','transport.cpp','controller.py','worker_health.py','reduce_v3.py','queue_stress.cpp')}
    assert expected_unchanged <= set(baseline_sources)
    unchanged={n:sha(ROOT/n)==baseline_sources[n] for n in sorted(expected_unchanged)}
    assert set(unchanged)==expected_unchanged and all(unchanged.values())
    repro_unwind=read(repro/'p3-unwind-probe/unwind-probe.json')
    assert len(repro_unwind)==226 and all(r['correct'] and r['actual_RtlVirtualUnwind'] for r in repro_unwind)
    platform_path=ROOT/'.local-work/d5ab/p3/platform.json'
    platform=read(platform_path)
    assert sha(platform['ntdll_loaded_path'])==platform['ntdll_file_sha256']
    result=dict(schema='sor-d5ab-p4-revalidated-components/1',scope='Offline P4 evidence reuse after exact unchanged-input checks; B2 NOT AUTHORIZED.',
        head=baseline['head'],index_sha256=baseline['index_sha256'],method_sha256=sha(__file__),
        plan_sha256=sha(plan_path),build=str(build),build_sha256=sha(build/'build.json'),
        reproduction_build_sha256=sha(repro/'build.json'),dll_sha256=dll,
        components={Path(p).relative_to(ROOT).as_posix():h for p,h in native['inputs'].items()},
        receipts=receipts,native_cases=len(native['cases']),reproduction_cases=len(reproduction['cases']),
        platform_receipt_sha256=sha(platform_path),host_os=platform['os'],
        ntdll_file_sha256=platform['ntdll_file_sha256'],
        unchanged_components=unchanged,preserved_historical_records=len(preservation),
        preserved_p1_exports=len(exports),initial_free=free,final_free={d:shutil.disk_usage(d).free for d in free})
    assert min(result['final_free'].values())>=40_000_000_000
    (out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(dll_sha256=dll,native_cases=result['native_cases'],receipts=len(receipts),preserved=len(preservation))))


if __name__=='__main__':
    main()
