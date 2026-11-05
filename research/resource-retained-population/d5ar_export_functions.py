# SPDX-License-Identifier: GPL-3.0-or-later
"""Read explicit existing containing function and direct root caller bodies.

SOR-P-0002 adaptation of owned d5ar_export_roots.py. Exports one explicit existing containing function plus all direct root callers. Same verified copied
database, readOnly/noanalysis, fresh output and both-drive guards remain intact.
No original project, game, saves, install, network or Git mutation.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import json
from pathlib import Path
from d5ad_baseline import ROOT, guard, sha


def main():
    if len(sys.argv)!=3:
        raise SystemExit('Usage: d5ar_export_functions.py FRESH-LABEL STATIC-CENTER')
    label=sys.argv[1]
    if not label or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in label):
        raise ValueError('Simple label required')
    if not sys.argv[2] or any(c not in '0123456789abcdef' for c in sys.argv[2]):
        raise ValueError('Explicit static root required')
    guard()
    original=Path(__file__).with_name('d5ar_export_roots.py')
    source=original.read_text(encoding='utf8')
    anchor="    generated = generated.replace('toAddr(\"145fd9c30\")', 'toAddr(args[1])')"
    old=('ReferenceIterator rr=currentProgram.getReferenceManager().getReferencesTo(toAddr(args[1]));\n'
         '                while(rr.hasNext()){Reference r=rr.next();roots.add(r.toString());Function f=currentProgram.getFunctionManager().getFunctionContaining(r.getFromAddress());if(f!=null)entries.add(f.getEntryPoint().toString());}')
    new=('Function chosen=currentProgram.getFunctionManager().getFunctionContaining(toAddr(args[1]));if(chosen!=null)entries.add(chosen.getEntryPoint().toString());'+old)
    if source.count(anchor)!=1:
        raise ValueError('Owned exporter anchor changed')
    injection=anchor+'\n    alias_old='+repr(old)+'\n    alias_new='+repr(new)+'\n    if generated.count(alias_old)!=1: raise ValueError("Owned Java root loop changed")\n    generated=generated.replace(alias_old,alias_new)'
    derived=source.replace(anchor,injection)
    path=ROOT / '.local-work/d5ar' / (label+'.function-method.py')
    if path.exists() or any(p.is_symlink() or p.is_junction() for p in (path,*path.parents)):
        raise ValueError('Fresh non-reparse derivative required')
    with path.open('x',encoding='utf8',newline='\n') as stream:stream.write(derived)
    namespace={'__file__':str(Path(__file__).resolve()),'__name__':'d5ar_alias_export_derivative'}
    exec(compile(derived,str(path),'exec'),namespace)
    namespace['main']()
    output=ROOT / '.local-work/d5ar' / label
    value=json.loads((output / 'result.json').read_bytes())
    value.update(wrapper_sha256=sha(__file__),inherited_source_sha256=sha(original),derived_method_sha256=sha(path),
                 scope='Explicit existing containing function plus direct callers; no analysis')
    with (output / 'alias-result.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(value,indent=2)+'\n')


if __name__=='__main__':main()
