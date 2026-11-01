# SPDX-License-Identifier: GPL-3.0-or-later
"""Bind affected P2 regression drivers to the exact schema-4 source combination.

Reads a completed disposable build, all runtime sources and the owned P2 drivers.
Runs their queue, actual controller and file-sharing tests in disposable hosts.
Writes only fresh ignored outputs, source snapshots and child logs. No game,
deployment, saves, database, downloads or Git mutation. Source pins include the
new reducer even though the historical driver inventories predate that file.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    build=(ROOT/sys.argv[1]).resolve()
    label=sys.argv[2]
    assert build.is_relative_to(ROOT/'.local-work/d5x') and label.replace('-','').isalnum()
    out=ROOT/'.local-work/d5ab'/label
    out.mkdir(exist_ok=False)
    source=ROOT/'runtime/construction-winner'
    research=ROOT/'research/resource-retained-population'
    drivers=['d5ab_p2_controller.py','d5ab_p2_file_sharing.py','d5ab_queue.py']
    paths=[p for p in source.iterdir() if p.is_file()]+[research/name for name in drivers]+[Path(__file__)]
    inputs={str(p.relative_to(ROOT)):sha(p) for p in paths}
    for name in inputs:
        snapshot=out/'sources'/name
        snapshot.parent.mkdir(parents=True,exist_ok=True)
        snapshot.write_bytes((ROOT/name).read_bytes())
    native=json.loads((build/'build.json').read_bytes())
    assert native['source_unchanged'] and native['compilation']['pass_exit']
    assert all(sha(path)==digest for path,digest in native['inputs'].items())
    commands=[
        [sys.executable,'-B',str(research/drivers[0]),'--parallel',str(build),label+'-controller'],
        [sys.executable,'-B',str(research/drivers[1]),str(build),label+'-sharing'],
        [sys.executable,'-B',str(research/drivers[2]),'.local-work/d5ab/'+label+'-queue','8000'],
    ]

    def run(item):
        index,command=item
        assert min(shutil.disk_usage(d).free for d in ('C:/','D:/'))>=40_000_000_000
        with (out/f'{index}.stdout.log').open('xb') as stdout,(out/f'{index}.stderr.log').open('xb') as stderr:
            result=subprocess.run(command,cwd=ROOT,stdout=stdout,stderr=stderr)
        return dict(command=command,exit=result.returncode,passed=result.returncode==0)

    with ThreadPoolExecutor(max_workers=3) as pool:
        results=list(pool.map(run,enumerate(commands)))
    unchanged=all(sha(ROOT/name)==digest for name,digest in inputs.items())
    receipt=dict(schema='sor-d5ab-p1-regressions/1',passed=unchanged and all(row['passed'] for row in results),
                 inputs=inputs,build=str(build),build_sha256=sha(build/'build.json'),
                 dll_sha256=sha(build/'package-runtime/SorConstructionWinner.dll'),
                 source_unchanged=unchanged,results=results)
    (out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(passed=receipt['passed'],results=results),indent=2))
    assert receipt['passed']


if __name__=='__main__':
    main()
