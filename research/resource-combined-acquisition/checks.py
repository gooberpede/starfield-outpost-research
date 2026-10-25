# SPDX-License-Identifier: GPL-3.0-or-later
"""Check fresh debugger receipts, fixed comparisons and corrupt-copy refusal.

Reads local synthetic captures and frozen D5A predictions. Writes fresh ignored
comparison outputs and controlled corrupt derivatives; never changes originals.
Executes the pinned disposable fixture through the shared operational pump and
tests a denied retail gate before process access. Uses Python stdlib only; no
retail operation, save, configuration, network or Git effects.
"""
import argparse
import ast
import json
from pathlib import Path
import shutil
import subprocess
import sys
from build import ROOT, LOCAL, pin
from qualify import write


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--qualification', type=Path, required=True)
    parser.add_argument('--name', required=True)
    args = parser.parse_args()
    assert args.name and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in args.name)
    out = LOCAL / args.name
    out.mkdir(exist_ok=False)
    q = args.qualification.resolve()
    assert q.is_relative_to(LOCAL)
    summary = json.loads((q/'summary.json').read_text(encoding='utf8'))
    assert summary['passed']
    runs = []
    for case in summary['cases']:
        command = [sys.executable,'-B',str(Path(__file__).with_name('compare.py')),
                   '--receipts',str(q/case['mode']),'--output',str(out/(case['mode']+'.json'))]
        run = subprocess.run(command,cwd=ROOT,capture_output=True)
        assert run.returncode == 0,run.stderr.decode()
        result = json.loads((out/(case['mode']+'.json')).read_text(encoding='utf8'))
        assert result['fit_performed'] is False and len(result['alternatives']) == 2
        assert [r['mask'] for r in result['alternatives']] == [0,3]
        assert result['native_link'] is None
        assert result['evidence_status'] == case['status']
        runs.append(dict(command=command,exit_code=run.returncode,sha256=pin(out/(case['mode']+'.json'))))
    for mode in ('corrupt-copy','truncated-copy'):
        dest = out/mode
        shutil.copytree(q/'mask0',dest)
        path = next(dest.glob('capture-*.bin'))
        raw = path.read_bytes()
        path.write_bytes(raw[:-1] if mode=='truncated-copy' else raw[:60]+bytes([raw[60]^1])+raw[61:])
        command = [sys.executable,'-B',str(Path(__file__).with_name('compare.py')),
                   '--receipts',str(dest),'--output',str(out/(mode+'.json'))]
        run = subprocess.run(command,cwd=ROOT,capture_output=True)
        assert run.returncode == 0,run.stderr.decode()
        assert json.loads((out/(mode+'.json')).read_text(encoding='utf8'))['evidence_status']=='INVALID'
        runs.append(dict(command=command,exit_code=run.returncode,sha256=pin(out/(mode+'.json'))))
    build = Path(json.loads((q/'mask0/process.json').read_text(encoding='utf8'))['command'][0]).parent
    for mode, stop in (('mask0',True),('combined',False),('cache-multi',False),('wrong-key',False)):
        folder=out/('operational-'+mode)
        command=[sys.executable,'-B',str(Path(__file__).with_name('collect.py')),'--synthetic-qualification',
                 '--build',str(build),'--output',str(folder),'--mode',mode]
        if stop:
            command += ['--stop-after-construction']
        run=subprocess.run(command,cwd=ROOT,capture_output=True)
        (out/(mode+'-operational-stdout.txt')).write_bytes(run.stdout)
        (out/(mode+'-operational-stderr.txt')).write_bytes(run.stderr)
        assert run.returncode==0,run.stderr.decode()
        result=json.loads((folder/'accounting.json').read_text(encoding='utf8'))
        assert result['scientific_result']=={'mask0':'CONSTRUCTION_ONLY','combined':'CONSTRUCTION_AND_CONSUMPTION_UNLINKED','cache-multi':'CONSUMER_ONLY','wrong-key':'UNBOUND'}[mode]
        if stop:
            assert result['success_ack'] and result['stop_requested']
        runs.append(dict(command=command,exit_code=run.returncode,sha256=pin(folder/'accounting.json')))
    write(out/'denied-gate.json',dict(status='DENIED',human_instruction='No retail authority.',stop_after_construction=False))
    write(out/'invalid-preflight.json',{})
    command=[sys.executable,'-B',str(Path(__file__).with_name('collect.py')),'--retail-pilot',
             '--approval',str(out/'denied-gate.json'),'--preflight',str(out/'invalid-preflight.json'),
             '--build',str(build),'--pid','1','--launch-utc','2026-10-25T00:00:00+00:00','--output',str(out/'forbidden-output')]
    run=subprocess.run(command,cwd=ROOT,capture_output=True)
    (out/'retail-gate-refusal-stderr.txt').write_bytes(run.stderr)
    assert run.returncode!=0 and b"approval['status']" in run.stderr
    assert not (out/'forbidden-output').exists() and not (out/'denied-gate.consumed.json').exists()
    runs.append(dict(command=command,exit_code=run.returncode,expected='REFUSED_BEFORE_ANY_PROCESS_QUERY_OR_ATTACHMENT'))
    current = LOCAL/'inherited01/geometry'
    previous = ROOT/'.local-work/resource-construction-mask-selection/regression01'
    exact = []
    for path in current.rglob('*-stdout.json'):
        old = previous/path.relative_to(current)
        assert old.is_file() and json.loads(path.read_text(encoding='utf8')) == json.loads(old.read_text(encoding='utf8')), str(path)
        exact.append(dict(path=str(path), previous=str(old), exact_semantic_equality=True))
    assert len(exact) == 38
    write(out/'frozen-d5a-equality.json', exact)
    for path in Path(__file__).parent.glob('*.py'):
        ast.parse(path.read_text(encoding='utf8'), filename=str(path))
    write(out/'summary.json',dict(passed=True,commands=runs,corrupt_originals_modified=False,
                                 python_version=sys.version,qualification_sha256=pin(q/'summary.json')))
    print(len(runs),'fixed-alternative and corrupt-copy checks PASS')


if __name__ == '__main__':
    main()
