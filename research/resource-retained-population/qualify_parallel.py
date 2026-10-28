# SPDX-License-Identifier: GPL-3.0-or-later
"""Run the existing disposable matrix in three bounded independent batches.

Reads an exact native build and owned qualification scripts. Launches only the
existing fixture runner with fixed case lists; at most three disposable targets
run concurrently. Writes fresh ignored batch receipts and a lossless aggregate
copy, preserving original batches and verifying every copied file. No retail
entry point, downloads, protected inputs, Git or analysis-project mutations.
The batch count limits engineering concurrency; it is not a capture quota.
"""
import concurrent.futures
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from build import LOCAL,pin
from reliability_contract import MODES


def main():
    build=Path(sys.argv[1]).resolve(); label=sys.argv[2]
    assert build.is_relative_to(LOCAL) and re.fullmatch('[a-z0-9-]+',label)
    assert min(shutil.disk_usage(d).free for d in ('C:/','D:/'))>=40000000000
    output=LOCAL/label; output.mkdir(exist_ok=False)
    # Keep the large stress case separate; other cases retain their own process.
    remaining=[m for m in MODES if m!='grid-stress']
    groups=[['grid-stress'],remaining[::2],remaining[1::2]]
    def run(number,modes):
        folder=LOCAL/f'{label}-batch{number}'
        command=[sys.executable,'-B',str(Path(__file__).with_name('qualify_native.py')),str(build),str(folder),*modes]
        with (output/f'batch{number}.log').open('xb') as log:
            result=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
        return dict(number=number,folder=str(folder),command=command,exit_code=result.returncode)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures=[pool.submit(run,i+1,modes) for i,modes in enumerate(groups)]
        batches=[future.result() for future in futures]
    results=[]; copies=[]
    for batch in batches:
        source=Path(batch['folder'])
        rows=json.loads((source/'results.json').read_text())
        for row in rows:
            original=source/row['mode']; target=output/row['mode']
            shutil.copytree(original,target)
            original_files={p.relative_to(original).as_posix():pin(p) for p in original.rglob('*') if p.is_file()}
            copied_files={p.relative_to(target).as_posix():pin(p) for p in target.rglob('*') if p.is_file()}
            assert original_files==copied_files
            copies.append(dict(mode=row['mode'],original=str(original),copy=str(target),files=original_files))
        results.extend(rows)
    assert len(results)==len(MODES) and {r['mode'] for r in results}==set(MODES)
    passed=all(b['exit_code']==0 for b in batches) and all(r['passed'] for r in results)
    for name,value in [('results.json',results),('aggregate.json',dict(passed=passed,batches=batches,copies=copies,
        method_sha256=pin(__file__),build_manifest_sha256=pin(build/'build.json'),originals_preserved=True))]:
        with (output/name).open('x',encoding='utf8',newline='\n') as f:
            json.dump(value,f,indent=2);f.write('\n')
    print(len(results),'real-process cases; lossless aggregate; PASS' if passed else 'FAIL',flush=True)
    return 0 if passed else 1


if __name__=='__main__':raise SystemExit(main())
