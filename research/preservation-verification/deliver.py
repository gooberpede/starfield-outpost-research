# SPDX-License-Identifier: GPL-3.0-or-later
"""Bind authored review snapshots and local exclusions without staging.

Reads final text, existing receipts, tool identities and Git; invokes the owned
editorial screen and exact patch exporter. Writes fresh ignored delivery records.
No target operation, evidence rewrite, dependency download or index/ref write.
"""
import argparse
import ast
import datetime
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
LOCAL=ROOT / '.local-work/preservation-verification'
BRIEF='docs/implementation-briefs/CODEX_BRIEF_SOR_preservation_audit_optimization.md'


def pin(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f,'sha256').hexdigest()


def write(path,value):
    with path.open('x',encoding='utf8',newline='\n') as f:
        json.dump(value,f,indent=2)
        f.write('\n')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--label',required=True)
    args=ap.parse_args()
    if not args.label.isalnum():
        raise ValueError('Fresh alphanumeric label required')
    out=LOCAL / args.label
    out.mkdir(exist_ok=False)
    scripts=sorted((ROOT / 'research/preservation-verification').glob('*.py'))
    for path in scripts:
        ast.parse(path.read_text(encoding='utf8'),filename=str(path))
    screen=subprocess.run([sys.executable,'-B','research/editorial/screen.py','--changed'],
                          cwd=ROOT,capture_output=True)
    (out / 'editorial-screen.json').write_bytes(screen.stdout)
    (out / 'editorial-stderr.txt').write_bytes(screen.stderr)
    if screen.returncode:
        raise RuntimeError('Editorial suspects; inspect preserved screen')
    label='preservation-'+args.label
    result=subprocess.run([sys.executable,'-B','research/review_package.py','--label',label,
        '--baseline',str(LOCAL / 'export-baseline.json'),'--supplied-brief',BRIEF],
        cwd=ROOT,capture_output=True)
    (out / 'package-stdout.json').write_bytes(result.stdout)
    (out / 'package-stderr.txt').write_bytes(result.stderr)
    if result.returncode:
        raise RuntimeError('Package failure; inspect preserved diagnostics')
    package=ROOT / '.local-work/review-deliveries' / (label+'.json')
    payload=json.loads(package.read_text())
    write(out / 'changed-files.json',payload['files'])
    # Hash receipt/control artifacts; synthetic payloads are enumerated with sizes
    # and are already covered by qualified fixture manifests. Do not reread raw
    # historical payloads to construct an exclusion inventory.
    exclusions=[]
    for path in sorted(LOCAL.rglob('*')):
        if path.is_file() and not path.is_relative_to(out):
            role='Synthetic disposable payload/manifest' if any(part in ('performance','cases','counterexample','independent01','supplement01') for part in path.parts) else 'Local receipt, diagnostic, raw manifest or review snapshot'
            row=dict(path=path.relative_to(ROOT).as_posix(),bytes=path.stat().st_size,reason=role)
            if role.startswith('Local'):
                row['sha256']=pin(path)
            exclusions.append(row)
    write(out / 'exclusions.json',dict(task_local=exclusions,
        inherited_inventory=dict(path='.local-work/resource-predictability-contrast/audit-before.json',
            sha256=pin(ROOT / '.local-work/resource-predictability-contrast/audit-before.json'),
            reason='93,334 inherited raw/save/native/database/build pins; not exported or rehashed here'),
        additional_roots=['Original active saves/backups, installed game inputs and analysis projects remain local under existing policy',
                          'Unrelated ignored repository data is outside task write/export scope'],
        later_receipts='This output directory, later reviewer/closure records and patches are bound separately by final delivery',
        publication_clearance=False))
    sdk=Path('C:/Program Files (x86)/Windows Kits/10/Include/10.0.26100.0/um/winioctl.h')
    write(out / 'environment.json',dict(python=sys.version,python_exe_sha256=pin(sys.executable),
        windows=platform.platform(),git=subprocess.check_output(['git','--version'],text=True).strip(),
        sdk_header=dict(version='10.0.26100.0',filename='winioctl.h',sha256=pin(sdk)),
        method_syntax_pass={p.relative_to(ROOT).as_posix():pin(p) for p in scripts},
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
    write(out / 'snapshot.json',dict(package=str(package),package_sha256=pin(package),
        files=payload['files'],patches=payload['patches'],
        snapshot_files={p.name:pin(p) for p in out.iterdir() if p.is_file()},
        head=payload['head'],index_sha256=payload['index_sha256'],
        scope='Exact text and local review outputs only; no policy activation or Git write'))
    print(json.dumps(dict(snapshot=str(out / 'snapshot.json'),files=len(payload['files']),patches=payload['patches']),indent=2))


if __name__=='__main__':
    main()
