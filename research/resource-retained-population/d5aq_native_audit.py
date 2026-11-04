# SPDX-License-Identifier: GPL-3.0-or-later
"""Reproduce D5AQ's retained native-witness replay or owner byte audits.

Reads pinned owned D5S/D5AM methods and their authenticated local evidence.
Writes only a fresh directory in the D5AQ local scratch tree. Replay adapts the D5S
child command to -E -B and runs eleven retained methods in disposable processes.
Owner mode redirects the D5AM audit's output guard to fresh D5AQ paths, preserving
all source-receipt, per-instruction PE, receiver context and disk-floor checks.
SOR-P-0002: source-informed reuse of those maintainer-owned methods, not new
third-party code. Dependencies are stdlib and existing project methods only.

Requires pinned Python, nonoptimized execution, retained inputs and both-drive
40,000,000,000-byte floors. No target/observer/save/configuration operation,
database opening, install, network or Git mutation. Original inputs and old
receipts remain unchanged; private native mappings end with each child process.
"""
import os
import sys
if (not __debug__ or sys.flags.optimize
        or os.environ.get('PYTHONOPTIMIZE','0') not in ('','0')):
    raise SystemExit('Optimized Python is prohibited; invoke pinned Python -E -B')
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parents[2]
PYTHON=Path('C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe')
METHODS={
    'replay':('d5s_controls.py','8441b76dbcce7eed7f1176295dc2416e9ff703d452d92e03485d04336b5e45ea'),
    'owner':('d5am_owner_census_audit.py','50520a73a198e3bee19b216e091464ee297d7d53cbca966bb0f8fcbd240870f1'),
}


def require(condition,message):
    if not condition:
        raise ValueError(message)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=METHODS)
    parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args()
    require(Path(sys.executable).resolve()==PYTHON.resolve(),'Pinned Python path')
    require(sha(PYTHON)=='cce21c0e8710e304273e98ac4b2b0f5aceb639acbcd2343cbaa5c4e81619c45b','Pinned Python bytes')
    out=args.out.resolve()
    require(out.is_relative_to(ROOT/'.local-work/d5aq') and not out.exists(),'Fresh D5AQ output required')
    for part in (out,*out.parents):
        require(not part.is_symlink() and not part.is_junction(),'Reparse output prohibited')
    free={drive:shutil.disk_usage(drive).free for drive in ('C:/','D:/')}
    require(min(free.values())>=40_000_000_000,'Disk floor: '+str(free))
    filename,expected=METHODS[args.mode]
    method=ROOT/'research/resource-retained-population'/filename
    require(sha(method)==expected,'Owned method pin')
    text=method.read_text(encoding='utf8')
    sys.path.insert(0,str(method.parent))
    namespace={'__file__':str(method),'__name__':'d5aq_authenticated_owned_method'}
    if args.mode=='replay':
        require(text.count("[sys.executable, '-B',")==1,'Replay adaptation seam')
        text=text.replace("[sys.executable, '-B',","[sys.executable, '-E', '-B',")
        exec(compile(text,'owned-D5S-replay-with-E','exec'),namespace)
        namespace['replay'](ROOT/'.local-work/d5s',out)
    else:
        seam="not out.is_relative_to(ROOT/'.local-work/d5am')"
        require(text.count(seam)==1,'Owner audit adaptation seam')
        text=text.replace(seam,"not out.is_relative_to(ROOT/'.local-work/d5aq')")
        exec(compile(text,'owned-D5AM-audit-output-redirection','exec'),namespace)
        out.mkdir(parents=True,exist_ok=False)
        for number in range(2,11):
            sys.argv=[str(method),str(ROOT/f'.local-work/d5am/owner-census{number:02}'),str(out/f'owner-census{number:02}.json')]
            namespace['main']()
    result=dict(status='PASS',mode=args.mode,method=str(method),source_sha256=expected,
                driver_sha256=sha(__file__),floor_before=free,
                outputs={str(p.relative_to(out)):sha(p) for p in out.glob('*.json')})
    (out/'d5aq-invocation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print('PASS',args.mode,out)


if __name__=='__main__':
    main()
