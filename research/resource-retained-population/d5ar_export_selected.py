# SPDX-License-Identifier: GPL-3.0-or-later
"""Read a bounded explicit set of existing native bodies without expanding callers.

SOR-P-0002 adaptation of the guarded single-body exporter. Reads the verified
disposable readOnly/noanalysis copy, writes fresh ignored evidence only. No game,
save, original DB, installation, network or Git mutation.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B')
from pathlib import Path
from d5ad_baseline import ROOT


def main():
    if not 3 <= len(sys.argv) <= 18:
        raise ValueError('Fresh label and one to sixteen explicit native addresses required')
    label, *addresses = sys.argv[1:]
    if not label or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in label):
        raise ValueError('Simple fresh label required')
    if len(set(addresses)) != len(addresses) or any(not a or any(c not in '0123456789abcdef' for c in a) for a in addresses):
        raise ValueError('Distinct explicit native addresses required')
    inherited = Path(__file__).with_name('d5ar_export_roots.py')
    source = inherited.read_text(encoding='utf8')
    anchor = "    generated = generated.replace('toAddr(\"145fd9c30\")', 'toAddr(args[1])')"
    old = ('ReferenceIterator rr=currentProgram.getReferenceManager().getReferencesTo(toAddr(args[1]));\n'
           '                while(rr.hasNext()){Reference r=rr.next();roots.add(r.toString());Function f=currentProgram.getFunctionManager().getFunctionContaining(r.getFromAddress());if(f!=null)entries.add(f.getEntryPoint().toString());}')
    values = ','.join('"' + a + '"' for a in addresses)
    new = ('for(String a:new String[]{'+values+'}){Function selected=currentProgram.getFunctionManager().getFunctionContaining(toAddr(a));'
           'if(selected==null||!selected.getEntryPoint().equals(toAddr(a)))throw new Exception("Exact existing function entry required: "+a);'
           'entries.add(selected.getEntryPoint().toString());}')
    injection = anchor + '\n    selected_old=' + repr(old) + '\n    selected_new=' + repr(new) + '\n    if generated.count(selected_old)!=1:raise ValueError("Owned Java anchor changed")\n    generated=generated.replace(selected_old,selected_new)'
    if source.count(anchor) != 1:
        raise ValueError('Owned exporter anchor changed')
    derived = source.replace(anchor, injection)
    path = ROOT / '.local-work/d5ar' / (label + '.selected-method.py')
    if path.exists() or any(p.is_symlink() or p.is_junction() for p in (path, *path.parents)):
        raise ValueError('Fresh ignored method required')
    with path.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(derived)
    namespace = {'__file__': str(Path(__file__).resolve()), '__name__': 'owned_selected_export'}
    original_arguments = sys.argv
    try:
        sys.argv = [original_arguments[0], label, addresses[0]]
        exec(compile(derived, str(path), 'exec'), namespace)
        namespace['main']()
    finally:
        sys.argv = original_arguments


if __name__ == '__main__':
    main()
