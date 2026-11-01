# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify the exact P1 native/consumer/test combination and local evidence pins.

Reads completed task receipts, protected installed/database identities and the
historical P2 preservation inventory. Writes a fresh ignored verification bundle
and authored source/test metadata under the P1 documentation prefix. Uses stdlib;
no native execution, game, saves, database edits, downloads or Git mutation.
Checksums authenticate bytes; the report and independent review assess semantics.
"""
import csv
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/'docs/experiments/resource-retained-population'
LOCAL=ROOT/'.local-work/d5ab'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def main():
    out=(ROOT/sys.argv[1]).resolve()
    assert out.is_relative_to(LOCAL)
    out.mkdir(parents=True,exist_ok=False)
    free={drive:shutil.disk_usage(drive).free for drive in ('C:/','D:/')}
    assert min(free.values())>=40_000_000_000
    baseline=read(LOCAL/'p1/baseline.json')
    assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()==baseline['head']
    assert sha(ROOT/'.git/index')==baseline['index_sha256']
    build=ROOT/'.local-work/d5x/p1-native03'
    native=read(build/'build.json')
    assert native['source_unchanged'] and native['compilation']['pass_exit']
    assert len(native['cases'])==66 and all(row['pass_exit'] for row in native['cases'])
    assert all(sha(path)==digest for path,digest in native['inputs'].items())
    assert all(sha(build/path)==digest for path,digest in native['outputs'].items())
    identity=read(ROOT/'.local-work/d5x/identity05/identity.json')
    for path,digest in {**identity['installed'],**identity['database']}.items():
        assert sha(path)==digest,path
    preserved=read(LOCAL/'p2-provenance02/preservation.json')
    for item in preserved:
        path=ROOT/item['path']
        assert path.exists()==item['exists'],item['path']
        if item['exists']:
            assert path.stat().st_size==item['bytes'] and sha(path)==item['sha256'],item['path']
    (out/'preservation.json').write_text(json.dumps(preserved,indent=2)+'\n',encoding='utf8',newline='\n')
    repro=ROOT/'.local-work/d5x/p1-repro01'
    reproduction=read(repro/'build.json')
    assert reproduction['source_unchanged'] and reproduction['inputs']==native['inputs']
    assert all(row['pass_exit'] for row in reproduction['cases']) and len(reproduction['cases'])==3
    dll=sha(build/'package-runtime/SorConstructionWinner.dll')
    assert dll==sha(repro/'package-runtime/SorConstructionWinner.dll')
    receipt_paths=[
        build/'build.json',repro/'build.json',LOCAL/'p1-reader-final03/receipt.json',
        LOCAL/'p1-regressions01/receipt.json',LOCAL/'p1-regressions01-controller/receipt.json',
        LOCAL/'p1-regressions01-sharing/receipt.json',LOCAL/'p1-regressions01-queue/receipt.json',
        LOCAL/'p1-native-instructions04/receipt.json',LOCAL/'p1-legacy-semantics01/receipt.json',
        LOCAL/'p1-worker-legacy01/receipt.json',LOCAL/'p1/funclet-parents-final01.json',
    ]
    consumer=read(receipt_paths[2]);assert consumer['passed'] and consumer['tests']==316
    assert consumer['final_build_consumer_match'] and consumer['dll_sha256']==dll
    for path,digest in consumer['inputs'].items():assert sha(path)==digest
    regression=read(receipt_paths[3]);assert regression['passed'] and regression['source_unchanged']
    for name,digest in regression['inputs'].items():assert sha(ROOT/name)==digest
    controller=read(receipt_paths[4]);assert controller['passed'] and len(controller['results'])==26
    for case in controller['results']:
        path=Path(case['receipt']);receipt_paths.append(path)
        assert sha(path)==case['receipt_sha256']
        case_receipt=read(path);assert case_receipt['passed'] and case_receipt['source_unchanged']
    sharing=read(receipt_paths[5]);assert sharing['passed']
    queue=read(receipt_paths[6]);assert len(queue['results'])==9 and queue['source_unchanged']
    assert all(row['passed'] and row['lossless_losses']==0 for row in queue['results'])
    instructions=read(receipt_paths[7]);assert instructions['passed'] and len(instructions['rows'])==11
    assert instructions['source_sha256']==sha(Path(__file__).with_name('d5ab_p1_native_controls.py'))
    legacy=read(receipt_paths[8]);assert legacy['passed'] and legacy['tests']==54
    for path,digest in legacy['inputs'].items():assert sha(path)==digest
    worker=read(receipt_paths[9]);assert worker['passed'] and len(worker['cases'])==9
    parents=read(receipt_paths[10]);assert len(parents['matches'])==12 and not parents['errors']
    assert not parents['unmapped_raw_references']
    assert parents['method_sha256']==sha(Path(__file__).with_name('d5ab_p1_exception_parents.py'))
    rows=[]
    exports=[LOCAL/'p1-export01',LOCAL/'p1-export02']+sorted(LOCAL.glob('p1-specialist-export[0-9][0-9]'))
    assert len(exports)==17
    for number,folder in enumerate(exports,1):
        path=folder/'native.tsv';preservation=read(folder/'preservation.json')
        assert preservation['database_unchanged'] and sha(path)==preservation['sha256']
        assert preservation['database']==identity['database']
        command=read(folder/'command.json')
        assert '-readOnly' in command and '-noanalysis' in command
        assert sha(command[0])==preservation['java_sha256']
        assert sha(folder/'ExploreD5S.java')==preservation['java_script_sha256']
        if folder.name=='p1-specialist-export15':
            assert sha(Path(__file__).with_name('d5ab_p1_cell_access.py'))==preservation['exporter_sha256']
        receipt_paths.append(folder/'preservation.json')
        lines=path.read_text(encoding='utf8').splitlines()
        assert lines[0]=='SHA256\t'+identity['installed'][str(Path(parents['executable_path']))]
        assert lines[-1]=='END'
        starts=[i for i,line in enumerate(lines) if line.startswith('FUNCTION\t')]
        for index,start in enumerate(starts):
            end=next(i for i in range(start,len(lines)) if lines[i]=='END_FUNCTION')
            fields=lines[start].split('\t')
            rows.append(dict(id=f'P1-E{number:02}-{index+1:03}',path=path.relative_to(ROOT).as_posix(),
                             sha256=sha(path),function='0x'+fields[1],first_line=start+1,last_line=end+1,
                             use='Pinned native receiver/argument/lifecycle evidence; see P1 matrix.',publication='LOCAL-ONLY'))
        if any(line.startswith('CELL_CENSUS\t') for line in lines):
            last=next(i for i,line in enumerate(lines) if line.startswith('CELL_CENSUS\t'))
            assert lines[last]=='CELL_CENSUS\t5083\t251'
            rows.append(dict(id=f'P1-E{number:02}-CENSUS',path=path.relative_to(ROOT).as_posix(),
                             sha256=sha(path),function='CELL_RECEIVER_CENSUS',first_line=2,last_line=last+1,
                             use='Bounded Grid receiver census; caller pointer flows require the full named bodies.',publication='LOCAL-ONLY'))
    with (DOC/'d5ab-p1-sources.csv').open('w',encoding='utf8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    representative=read(build/'representative/terminal.json')
    assert representative['drops']==0 and representative['output_faults']==0
    assert representative['enqueued']==representative['written']==representative['flushed']==representative['acknowledged']
    unchanged={name:sha(ROOT/name)==digest for name,digest in baseline['runtime'].items()
               if name.endswith(('bridges.asm','transport.cpp','transport.h','patch.h','controller.py','reduce_v3.py','queue_stress.cpp'))}
    assert all(unchanged.values())
    result=dict(schema='sor-d5ab-p1-qualified-components/1',scope='Offline P1 only; P3/P4 OPEN; B2 NOT AUTHORIZED',
                verifier_sha256=sha(__file__),
                head=baseline['head'],index_sha256=baseline['index_sha256'],dll_sha256=dll,
                receipts={path.relative_to(ROOT).as_posix():sha(path) for path in receipt_paths},
                components={Path(path).relative_to(ROOT).as_posix():digest for path,digest in native['inputs'].items()},
                unchanged_production_contracts=unchanged,native_cases=66,reproduction_cases=3,
                consumer_checks=316,controller_cases=26,queue_runs=9,file_sharing_controls=1,
                original_instruction_controls=11,legacy_semantic_controls=54,worker_controls=9,
                exception_parent_records=12,source_exports=17,
                source_function_records=sum(row['function'].startswith('0x') for row in rows),
                source_census_records=sum(row['function']=='CELL_RECEIVER_CENSUS' for row in rows),
                preserved_historical_records=len(preserved),initial_free=free,
                representative={key:representative[key] for key in ('enqueued','written','flushed','acknowledged','drops','queue_high_water_lower_bound','cell_bytes','capacity')})
    (out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    (DOC/'d5ab-p1-test-results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps({key:result[key] for key in ('native_cases','consumer_checks','controller_cases','queue_runs','preserved_historical_records','source_function_records','dll_sha256')}))


if __name__=='__main__':
    main()
