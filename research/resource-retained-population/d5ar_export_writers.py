# SPDX-License-Identifier: GPL-3.0-or-later
"""Export data-root references and only native writer bodies from verified copy.

SOR-P-0002 adaptation of owned d5ar_export_roots.py. The same guarded read-only,
no-analysis export verifies all fifteen copied database cores before/after.
This narrows body selection to native WRITE references while retaining every
root-reference record; it does not weaken input/output/disk protections. Writes
exclusive ignored derivative/receipts only. No target, save or original DB opens.
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
        raise SystemExit('Usage: d5ar_export_writers.py FRESH-LABEL STATIC-ROOT')
    label=sys.argv[1]
    if not label or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in label):
        raise ValueError('Simple label required')
    if not sys.argv[2] or any(c not in '0123456789abcdef' for c in sys.argv[2]):
        raise ValueError('Explicit static root required')
    guard()
    original=Path(__file__).with_name('d5ar_export_roots.py')
    source=original.read_text(encoding='utf8')
    anchor="    generated = generated.replace('toAddr(\"145fd9c30\")', 'toAddr(args[1])')"
    if source.count(anchor)!=1:
        raise ValueError('Owned source anchor changed')
    injected=anchor+"\n    generated = generated.replace('if(f!=null)entries.add', 'if(f!=null&&r.getReferenceType().isWrite())entries.add')"
    derived=source.replace(anchor,injected)
    path=ROOT / '.local-work/d5ar' / (label+'.writer-method.py')
    if path.exists() or any(p.is_symlink() or p.is_junction() for p in (path,*path.parents)):
        raise ValueError('Fresh non-reparse derivative required')
    with path.open('x',encoding='utf8',newline='\n') as stream:stream.write(derived)
    namespace={'__file__':str(Path(__file__).resolve()),'__name__':'d5ar_writer_export_derivative'}
    exec(compile(derived,str(path),'exec'),namespace)
    namespace['main']()
    output=ROOT / '.local-work/d5ar' / label
    value=json.loads((output / 'result.json').read_bytes())
    value.update(wrapper_sha256=sha(__file__),inherited_source_sha256=sha(original),derived_method_sha256=sha(path),
                 scope='Every root reference retained; only WRITE-containing function bodies exported')
    with (output / 'writer-result.json').open('x',encoding='utf8',newline='\n') as stream:stream.write(json.dumps(value,indent=2)+'\n')


if __name__=='__main__':main()
