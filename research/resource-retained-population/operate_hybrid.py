# SPDX-License-Identifier: GPL-3.0-or-later
"""D5N offline preparation and separately authorized future collection adapter.

The prepare command inherits full_preservation and writes a fresh readiness
receipt/restoration copy; it never starts a target. The collect command requires
separate explicit Phase B GO and all inherited admission/ordinary-user gates.
It attaches and can terminate the admitted research target, patches thirteen
sites and writes DR0/RF plus owned RIP/TF. Do not invoke collect in Phase A.
No launch, download, install, save/configuration/analysis or Git mutations.
"""
import sys
import hybrid
import qualify_hybrid


def module(name):
    source = (hybrid.SRC/(name+'.py')).read_text(encoding='utf8')
    scope = dict(__name__='d5n_'+name, __file__=str(hybrid.SRC/(name+'.py')))
    if name=='collect_native':
        source = hybrid.replace(source, "{'software_int3_14','all_stop_and_peer_suspend'",
            "{'software_int3_13','hardware_dr0_grid_clear','all_stop_and_peer_suspend'")
        # Inject idle fixture failures only after readiness. A slow attach must
        # not turn the idle-pipe test into a write to an already closed pipe at
        # ARM_ACK; production collection has test_failure=None throughout.
        for fault in ('idle-collector-loss', 'idle-pipe-loss'):
            source = hybrid.replace(source, "if test_failure == '"+fault+"':",
                "if test_failure == '"+fault+"' and (output / 'READY.json').exists():")
    exec(compile(source, scope['__file__']+'[D5N adapted]', 'exec'), scope)
    if name=='prepare_native':
        scope['MODES'] = qualify_hybrid.namespace['MODES']
        scope['CARD'] = scope['ROOT']/'docs/experiments/resource-retained-population/run-card-d5n-v1.md'
    return scope


if __name__ == '__main__':
    command=sys.argv.pop(1)
    assert command in ('prepare','collect'), 'Explicit prepare or collect required'
    raise SystemExit(module('prepare_native' if command=='prepare' else 'collect_native')['main']())
