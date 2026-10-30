# SPDX-License-Identifier: GPL-3.0-or-later
"""Repeat positive/adversarial controls on the identical packaged DLL and reader.

Reads a qualified local build. Runs only its disposable native host and writes
fresh local-only sessions/logs/results. No rebuild, game, installed/save/database,
configuration, network or Git mutation. One control intentionally crashes only
its own disposable process after a durable direct sample.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    build=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve()
    assert build.is_relative_to(ROOT/'.local-work/d5x') and out.is_relative_to(ROOT/'.local-work/d5x')
    out.mkdir(exist_ok=False)
    runtime=build/'package-runtime'
    dll=runtime/'SorConstructionWinner.dll';host=runtime/'sor-d5x-fixture.exe';reader=runtime/'read_capture.py'
    pins={str(path):sha(path) for path in (dll,host,reader,runtime/'emitter-input.bin')}
    spec=importlib.util.spec_from_file_location('replayed_reader',reader)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    expected={'normal':1,'mask-zero':1,'edge':2,'corner':4,'nested':1,'concurrent':9,
              'descriptor-collision':0,'interrupt':0,'in-flight-loss':0,'loss-one':2,
              'loss-many':2,'unexpected-mask':0,'crash-sample':1,'descriptor-change':1,'unrelated-conversion':0,'sequence-wrap':1,'post-reset-old-provider':0,
              'schedule-old-first':0,'schedule-fresh-first':1,'reset-closeout':0,'temporary-descriptor':0,'stop-under-production':1}
    def run(case):
        process=subprocess.run([str(host),str(dll),str(out/case),case],capture_output=True)
        (out/(case+'.log')).write_bytes(process.stdout+process.stderr)
        result=module.inspect(out/case,pins[str(dll)])
        (out/(case+'.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
        return dict(case=case,exit=process.returncode,chains=len(result['chains']),
                    passed=process.returncode==(73 if case=='crash-sample' else 0) and len(result['chains'])==expected[case])
    with ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(run,expected))
    assert all(sha(path)==digest for path,digest in pins.items())
    result=dict(schema='sor-d5x-replay/1',pins=pins,method_sha256=sha(__file__),cases=results,passed=all(row['passed'] for row in results))
    (out/'replay.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(result,indent=2))
    return 0 if result['passed'] else 1


if __name__=='__main__':raise SystemExit(main())
