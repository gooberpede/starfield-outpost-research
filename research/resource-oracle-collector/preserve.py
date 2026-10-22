# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only preservation audit; writes one fresh ignored JSON receipt.

Reads intake tracked-file inventory, inherited protected evidence, current files,
Git metadata and local synthetic artifacts. No native target execution, network,
save/config/database/index writes or cleanup. Requires completed start/preflight.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-oracle-collector'
ALLOWED = {'CREDITS.md','docs/SOURCES.md','docs/RESEARCH_STATE.md',
           'docs/experiments/README.md','docs/implementation-briefs/README.md'}


def pin(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args(); out=args.output.resolve()
    assert out.is_relative_to(LOCAL.resolve()) and not out.exists()
    start=json.loads((LOCAL/'start.json').read_text())
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    index=pin(ROOT/'.git/index')
    assert head==start['head'] and index==start['index_sha256']
    changed=[]
    for name,digest in start['tracked'].items():
        now=pin(ROOT/name)
        if now!=digest:
            assert name in ALLOWED, ('unrelated tracked change',name)
            changed.append(dict(path=name,before=digest,after=now))
    protected=[]
    for row in json.loads((LOCAL/'protected-preflight.json').read_text()):
        assert pin(row['path'])==row['sha256'], row['path']
        protected.append(row)
    space={d:shutil.disk_usage(d).free for d in ('C:/','D:/')}
    assert min(space.values())>=40_000_000_000
    # Query names only; no attachment, termination or game operations.
    command=['powershell','-NoProfile','-Command',
             "@(Get-Process -Name 'sor-c1c-*' -ErrorAction SilentlyContinue).Count"]
    active=subprocess.check_output(command,text=True).strip()
    assert active=='0', ('disposable process still present',active)
    artifacts={str(p.relative_to(ROOT)):dict(bytes=p.stat().st_size,sha256=pin(p))
               for p in LOCAL.rglob('*') if p.is_file() and p.resolve()!=out}
    result=dict(status='PASS',head=head,index_sha256=index,space=space,tracked_count=len(start['tracked']),
                permitted_edits=changed,protected=protected,artifacts=artifacts,
                disposable_process_count=active,process_query=command,
                limits='Hash checks prove preservation of named bytes; no system-wide filesystem tracing. '
                       'Target/controller source has no target file-write API; wrapper/compiler outputs are scoped. '
                       'Windows OS bookkeeping/crash reporting is outside this application-output inventory.')
    with out.open('x',encoding='utf8',newline='\n') as f:
        json.dump(result,f,indent=2); f.write('\n')
    print(len(start['tracked']),'tracked; protected',len(protected),'artifacts',len(artifacts),'PASS')


if __name__=='__main__':
    main()
