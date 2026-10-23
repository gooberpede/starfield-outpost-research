# SPDX-License-Identifier: GPL-3.0-or-later
"""Audit Python inference reads with an explicit code/data/stdlib allowlist.

Run as a fresh -I -S -B interpreter from an empty working directory. Reads only
specified completed corpus, request and flat authored code; emits audit JSON to
stderr and predictor JSON to stdout. Guard probes are deliberate denied reads.
This is an auditable Python boundary, not an operating-system security sandbox.
The predictor launches no subprocess or custom native library. CPython's
standard-library native modules remain part of the allowed interpreter runtime.
"""
import argparse
import json
import os
from pathlib import Path
import runpy
import sys


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--code',type=Path,required=True)
    parser.add_argument('--corpus',type=Path,required=True)
    parser.add_argument('--request',type=Path,required=True)
    parser.add_argument('--load-only',action='store_true')
    args=parser.parse_args()
    code=args.code.resolve(); data={args.corpus.resolve(),args.request.resolve()}
    runtime=Path(sys.base_prefix).resolve()
    events=[]; phase='guard_probe'
    def audit(event, operands):
        if event in ('open','os.listdir','os.scandir'):
            name=operands[0]
            if isinstance(name,int):
                raise PermissionError('file descriptor access is not allowlisted')
            p=Path(os.fsdecode(name)).resolve()
            allowed=p in data or p.is_relative_to(code) or (p.is_relative_to(runtime) and 'site-packages' not in p.parts)
            if event=='open':
                mode=operands[1];flags=operands[2]
                allowed=allowed and not (isinstance(mode,str) and any(v in mode for v in 'wax+'))
                allowed=allowed and not flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND)
            events.append(dict(phase=phase,event=event,path=str(p),allowed=allowed))
            if not allowed: raise PermissionError('FORBIDDEN_ACCESS: '+str(p))
        elif event.startswith(('subprocess.','socket.','ctypes.')) or event in ('os.system','os.chdir'):
            events.append(dict(phase=phase,event=event,allowed=False))
            raise PermissionError('FORBIDDEN_OPERATION: '+event)
    sys.addaudithook(audit)
    forbidden=[Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm'),
        Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe'),
        Path('D:/ReverseEngineering/Starfield/GhidraProject'),Path('D:/tools/xEdit.4.1.5p'),
        Path('D:/Projects/starfield-outpost-research/.local-work/resource-geometry/native/001.request.tsv'),
        Path('D:/Projects/starfield-outpost-research/.local-work/resource-carinae/retail-attempt02/capture-01270.bin'),
        Path('D:/Projects/starfield-outpost-research/.local-work/resource-geometry-mature-context/site-feynman-initial02.json'),
        Path('D:/Projects/starfield-outpost-research/.local-work/resource-pattern-selection/validation05.geometry.json')]
    for path in forbidden:
        try: path.read_bytes()
        except PermissionError: pass
        else: raise AssertionError('guard failed')
    phase='inference'
    sys.path=[str(code),*[p for p in sys.path if Path(p).resolve().is_relative_to(runtime)]]
    sys.argv=[str(code/'predictor.py'),'--corpus',str(args.corpus),'--request',str(args.request)]
    try:
        if args.load_only:
            import predictor
            predictor.validate(json.loads(args.corpus.read_text(encoding='utf8')))
            print(json.dumps(dict(status='LOADED_AND_VALIDATED')))
        else:
            runpy.run_path(str(code/'predictor.py'),run_name='__main__')
    finally:
        print(json.dumps(dict(schema='sor-d1-isolation/1',boundary='Python audit hook; no OS isolation claimed',
            events=events,inference_forbidden=[e for e in events if e['phase']=='inference' and not e['allowed']],
            denied_probes=sum(e['phase']=='guard_probe' and not e['allowed'] for e in events))),file=sys.stderr)


if __name__=='__main__':
    main()
