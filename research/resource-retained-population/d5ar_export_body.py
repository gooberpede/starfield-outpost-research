# SPDX-License-Identifier: GPL-3.0-or-later
"""Read exactly one existing native function from the guarded disposable copy.

SOR-P-0002 adaptation of export_roots. No caller expansion, analysis, original
database/game/save/install/network/Git mutation. Writes fresh ignored exports.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B')
from pathlib import Path
from d5ad_baseline import ROOT


def main():
    if len(sys.argv) != 3:
        raise ValueError('Fresh label and explicit native address required')
    inherited = Path(__file__).with_name('d5ar_export_roots.py')
    source = inherited.read_text(encoding='utf8')
    anchor = "    generated = generated.replace('toAddr(\"145fd9c30\")', 'toAddr(args[1])')"
    old = ('ReferenceIterator rr=currentProgram.getReferenceManager().getReferencesTo(toAddr(args[1]));\n'
           '                while(rr.hasNext()){Reference r=rr.next();roots.add(r.toString());Function f=currentProgram.getFunctionManager().getFunctionContaining(r.getFromAddress());if(f!=null)entries.add(f.getEntryPoint().toString());}')
    new = ('Function selected=currentProgram.getFunctionManager().getFunctionContaining(toAddr(args[1]));'
           'if(selected==null)throw new Exception("Existing native body required");entries.add(selected.getEntryPoint().toString());')
    injection = anchor + '\n    body_old=' + repr(old) + '\n    body_new=' + repr(new) + '\n    if generated.count(body_old)!=1:raise ValueError("Owned Java anchor changed")\n    generated=generated.replace(body_old,body_new)'
    if source.count(anchor) != 1:
        raise ValueError('Owned exporter anchor changed')
    derived = source.replace(anchor, injection)
    path = ROOT / '.local-work/d5ar' / (sys.argv[1] + '.body-method.py')
    if path.exists() or any(p.is_symlink() or p.is_junction() for p in (path, *path.parents)):
        raise ValueError('Fresh ignored method required')
    with path.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(derived)
    namespace = {'__file__': str(Path(__file__).resolve()), '__name__': 'owned_body_export'}
    exec(compile(derived, str(path), 'exec'), namespace)
    namespace['main']()


if __name__ == '__main__':
    main()
