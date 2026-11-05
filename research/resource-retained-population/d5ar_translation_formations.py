# SPDX-License-Identifier: GPL-3.0-or-later
"""Inventory original executable LEA boundaries around the translation header.

Owned SOR-P-0002 derivative of D5AR's guarded copy exporter. Reads every existing
instruction boundary in executable blocks; selects LEA references to the bounded
8 KiB neighborhood, retaining every root. Exports bodies/callers only for the
nearest previously unexamined preferred VA range [0x1461fad80, 0x1461fae00),
leaving the wider roots as an inventory. No new analysis, disassembly, target
execution, original database edits or network. Exclusive
ignored outputs and unchanged fifteen-copy-core guards remain inherited.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import json
from pathlib import Path
from d5ad_baseline import ROOT, guard, sha


def main():
    if len(sys.argv)!=2:raise SystemExit('Usage: d5ar_translation_formations.py FRESH-LABEL')
    label=sys.argv[1]
    if not label or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in label):
        raise ValueError('Simple fresh label required')
    guard()
    original=Path(__file__).with_name('d5ar_export_roots.py')
    source=original.read_text(encoding='utf8')
    anchor="    generated = generated.replace('toAddr(\"145fd9c30\")', 'toAddr(args[1])')"
    old=('ReferenceIterator rr=currentProgram.getReferenceManager().getReferencesTo(toAddr(args[1]));\n'
         '                while(rr.hasNext()){Reference r=rr.next();roots.add(r.toString());Function f=currentProgram.getFunctionManager().getFunctionContaining(r.getFromAddress());if(f!=null)entries.add(f.getEntryPoint().toString());}')
    new=('InstructionIterator all=currentProgram.getListing().getInstructions(true);long scanned=0;\n'
         '                while(all.hasNext()){Instruction inst=all.next();if(!currentProgram.getMemory().getBlock(inst.getAddress()).isExecute())continue;++scanned;'
         'if(!inst.getMnemonicString().equals("LEA"))continue;for(Reference r:inst.getReferencesFrom()){long target=r.getToAddress().getOffset();'
         'if(target>=0x1461f9e80L&&target<0x1461fbe80L){roots.add(r.toString());Function f=currentProgram.getFunctionManager().getFunctionContaining(inst.getAddress());'
         'if(f!=null&&target>=0x1461fad80L&&target<0x1461fae00L)entries.add(f.getEntryPoint().toString());}}}roots.add("EXECUTABLE_EXISTING_BOUNDARIES "+scanned);')
    if source.count(anchor)!=1:raise ValueError('Owned exporter anchor changed')
    injection=anchor+'\n    formation_old='+repr(old)+'\n    formation_new='+repr(new)+'\n    if generated.count(formation_old)!=1: raise ValueError("Owned Java root loop changed")\n    generated=generated.replace(formation_old,formation_new)'
    derived=source.replace(anchor,injection)
    path=ROOT/'.local-work/d5ar'/(label+'.formation-method.py')
    if path.exists() or any(p.is_symlink() or p.is_junction() for p in (path,*path.parents)):
        raise ValueError('Fresh non-reparse derivative required')
    with path.open('x',encoding='utf8',newline='\n') as stream:stream.write(derived)
    namespace={'__file__':str(Path(__file__).resolve()),'__name__':'d5ar_formation_derivative'}
    exec(compile(derived,str(path),'exec'),namespace)
    prior=sys.argv
    try:
        sys.argv=[str(Path(__file__).resolve()),label,'1461fae80']
        namespace['main']()
    finally:sys.argv=prior
    output=ROOT/'.local-work/d5ar'/label
    value=json.loads((output/'result.json').read_bytes())
    value.update(wrapper_sha256=sha(__file__),inherited_source_sha256=sha(original),derived_method_sha256=sha(path),
                 scope='All existing executable LEA references to [1461f9e80,1461fbe80); bodies only for [1461fad80,1461fae00); computed aliases unresolved')
    with (output/'formation-result.json').open('x',encoding='utf8',newline='\n') as stream:
        stream.write(json.dumps(value,indent=2)+'\n')


if __name__=='__main__':main()
