# SPDX-License-Identifier: GPL-3.0-or-later
"""Read existing instruction boundaries in explicit bounded copied-DB ranges.

Owned SOR-P-0002 derivative of D5AR guarded exporter, for CRT thunks without a
defined function, plus direct existing references to each explicit start. No
analysis or boundary creation. Each explicit start reads existing boundaries for
at most 64 bytes; no native execution, target/save/original
DB edits. Inherits fifteen-copy-core, fresh-output and both-drive guards.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import json
from pathlib import Path
from d5ad_baseline import ROOT,guard,sha


def main():
    if not 3<=len(sys.argv)<=18:raise SystemExit('Usage: d5ar_explicit_instructions.py FRESH-LABEL STATIC-START...')
    label=sys.argv[1];starts=sys.argv[2:]
    if not label or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in label):raise ValueError('Simple fresh label')
    if any(not a or any(c not in '0123456789abcdef' for c in a) for a in starts):raise ValueError('Explicit static starts')
    guard();original=Path(__file__).with_name('d5ar_export_roots.py');source=original.read_text(encoding='utf8')
    anchor="    generated = generated.replace('toAddr(\"145fd9c30\")', 'toAddr(args[1])')"
    old=('ReferenceIterator rr=currentProgram.getReferenceManager().getReferencesTo(toAddr(args[1]));\n'
         '                while(rr.hasNext()){Reference r=rr.next();roots.add(r.toString());Function f=currentProgram.getFunctionManager().getFunctionContaining(r.getFromAddress());if(f!=null)entries.add(f.getEntryPoint().toString());}')
    explicit=','.join('0x'+a+'L' for a in starts)
    new=('for(long at:new long[]{'+explicit+'}){ReferenceIterator refs=currentProgram.getReferenceManager().getReferencesTo(toAddr(at));while(refs.hasNext())roots.add("ADDRESS_XREF "+refs.next());InstructionIterator chosen=currentProgram.getListing().getInstructions(toAddr(at),true);'
         'while(chosen.hasNext()){Instruction inst=chosen.next();if(inst.getAddress().getOffset()>=at+64)break;'
         'byte[] bytes=inst.getBytes();StringBuilder hex=new StringBuilder();for(byte b:bytes)hex.append(String.format("%02x",b&255));'
         'roots.add("EXISTING_BOUNDARY "+inst.getAddress()+" "+inst+" BYTES "+hex);for(Reference r:inst.getReferencesFrom())roots.add(r.toString());}}')
    if source.count(anchor)!=1:raise ValueError('Owned anchor changed')
    injection=anchor+'\n    range_old='+repr(old)+'\n    range_new='+repr(new)+'\n    if generated.count(range_old)!=1:raise ValueError("Owned Java loop changed")\n    generated=generated.replace(range_old,range_new)'
    derived=source.replace(anchor,injection);path=ROOT/'.local-work/d5ar'/(label+'.range-method.py')
    if path.exists() or any(p.is_symlink() or p.is_junction() for p in (path,*path.parents)):raise ValueError('Fresh nonreparse derivative')
    with path.open('x',encoding='utf8',newline='\n') as stream:stream.write(derived)
    namespace={'__file__':str(Path(__file__).resolve()),'__name__':'d5ar_range_derivative'};exec(compile(derived,str(path),'exec'),namespace)
    prior=sys.argv
    try:
        sys.argv=[str(Path(__file__).resolve()),label,starts[0]];namespace['main']()
    finally:sys.argv=prior
    output=ROOT/'.local-work/d5ar'/label;value=json.loads((output/'result.json').read_bytes())
    value.update(wrapper_sha256=sha(__file__),inherited_source_sha256=sha(original),derived_method_sha256=sha(path),explicit_starts=starts,
                 scope='Direct existing references to each explicit start and existing instruction boundaries for64-byte intervals; no new analysis')
    with (output/'range-result.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(value,indent=2)+'\n')


if __name__=='__main__':main()
