# SPDX-License-Identifier: GPL-3.0-or-later
"""Run D5M's real Windows matrix with the D5N controller and hybrid reducer.

Reads an exact hybrid build and owned qualification/transport methods. Writes
fresh ignored receipts, ACKs, control logs and reductions. Creates, attaches,
pauses, patches thirteen sites and changes DR0/RF/TF only in sibling disposable
processes. Failures/STOP may terminate those processes. No retail entry point,
network, installation, save/configuration/analysis or Git changes.
"""
import hybrid
import qualify_native

source = (hybrid.SRC/'qualify_native.py').read_text(encoding='utf8')
source = hybrid.replace(source, "'cleanup-close-diagnostic-failure')",
                       "'cleanup-close-diagnostic-failure','hardware-loss','slot-pressure')")
source = hybrid.replace(source, "('failed','copy-failed','prereq','bad-read'):",
                       "('failed','copy-failed','prereq','bad-read','early-crash'):")
source = hybrid.replace(source, "if mode=='alternate-frame':", """if mode=='early-crash':
            checks['crash_before_construction']=not reduction['decisions'] and any(r['kind']=='GAP' and r['reason']=='unexpected_exit' for r in rows)
        if mode=='alternate-frame':""")
# The early crash has no MISS to classify as incomplete.
source = hybrid.replace(source, "checks['incomplete_preserved']=any(",
                       "checks['incomplete_preserved']=mode=='early-crash' or any(")
source = hybrid.replace(source, "if mode in ('queued-same','queued-different'):",
                       "if mode in ('queued-same','queued-different','queued-hardware'):")
namespace = dict(__name__='d5n_qualification', __file__=str(hybrid.SRC/'qualify_native.py'))
exec(compile(source, namespace['__file__']+'[D5N adapted]', 'exec'), namespace)
namespace['reduce'] = hybrid.reducer().reduce
namespace['MODES'] = (*qualify_native.MODES, 'early-crash', 'hardware-loss', 'slot-pressure', 'queued-hardware')

if __name__ == '__main__':
    raise SystemExit(namespace['main']())
