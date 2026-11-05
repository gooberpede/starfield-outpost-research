# SPDX-License-Identifier: GPL-3.0-or-later
"""Read original instruction scalar references to one explicit fourcc.

SOR-P-0002 adaptation of owned export_roots, guarded disposable readOnly/noanalysis
copy only. Reads existing instructions; writes fresh ignored export/receipts.
No new analysis, original DB/game/save/install/network/Git mutation. Refuses more
than twelve containing functions rather than broadening the native export.
"""
import os,sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):
    raise RuntimeError('Use pinned Python -E -B')
from pathlib import Path
from d5ad_baseline import ROOT,sha

def main():
    if len(sys.argv)!=3 or sys.argv[2] not in ('4c464552','46494452','5453494c'):
        raise ValueError('Explicit REFL/RDIF/LIST scalar required')
    inherited=Path(__file__).with_name('d5ar_export_roots.py')
    source=inherited.read_text(encoding='utf8')
    anchor="    generated = generated.replace('toAddr(\"145fd9c30\")', 'toAddr(args[1])')"
    old='ReferenceIterator rr=currentProgram.getReferenceManager().getReferencesTo(toAddr(args[1]));\n                while(rr.hasNext()){Reference r=rr.next();roots.add(r.toString());Function f=currentProgram.getFunctionManager().getFunctionContaining(r.getFromAddress());if(f!=null)entries.add(f.getEntryPoint().toString());}'
    new='''long wanted=Long.parseUnsignedLong(args[1],16);InstructionIterator ii=currentProgram.getListing().getInstructions(true);
                while(ii.hasNext()){Instruction ins=ii.next();boolean hit=false;for(int op=0;op<ins.getNumOperands();op++){for(Object obj:ins.getOpObjects(op)){if(obj instanceof ghidra.program.model.scalar.Scalar && ((ghidra.program.model.scalar.Scalar)obj).getUnsignedValue()==wanted)hit=true;}}if(hit){roots.add(ins.getAddress()+" scalar "+ins.toString());Function f=currentProgram.getFunctionManager().getFunctionContaining(ins.getAddress());if(f!=null)entries.add(f.getEntryPoint().toString());}}
                if(entries.size()>12)throw new Exception("Bounded scalar census requires narrower design");'''
    injection=anchor+'\n    scalar_old='+repr(old)+'\n    scalar_new='+repr(new)+'\n    if generated.count(scalar_old)!=1:raise ValueError("Owned Java anchor changed")\n    generated=generated.replace(scalar_old,scalar_new)'
    if source.count(anchor)!=1:raise ValueError('Owned exporter anchor changed')
    derived=source.replace(anchor,injection)
    path=ROOT/'.local-work/d5ar'/(sys.argv[1]+'.scalar-method.py')
    if path.exists() or any(p.is_symlink() or p.is_junction() for p in (path,*path.parents)):
        raise ValueError('Fresh ignored method required')
    with path.open('x',encoding='utf8',newline='\n') as stream:stream.write(derived)
    ns={'__file__':str(Path(__file__).resolve()),'__name__':'d5ar_scalar_derivative'}
    exec(compile(derived,str(path),'exec'),ns);ns['main']()

if __name__=='__main__':main()
