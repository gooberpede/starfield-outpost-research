# SPDX-License-Identifier: GPL-3.0-or-later
"""D5O offline preparation and future collection through owned D5N admission.

Preparation reads all 55 exact-build cases, protected archive/save/content and
the D5O card, writing fresh ignored receipts and a rehearsal save COPY only.
Collection retains all original explicit Phase B approval/account/session gates
and interventions. Never invoke collect in Phase A. No launch, installation,
network, original save/configuration, analysis or Git mutations.
"""
import sys
import operate_hybrid
from qualify_coverage_hybrid import MODES


def module(command):
    scope = operate_hybrid.module(command)
    if command=='prepare_native':
        scope['MODES'] = MODES
        scope['CARD'] = scope['ROOT']/'docs/experiments/resource-retained-population/run-card-d5o-v1.md'
    return scope


if __name__ == '__main__':
    command = sys.argv.pop(1)
    assert command in ('prepare','collect'), 'Explicit prepare or collect required'
    raise SystemExit(module('prepare_native' if command=='prepare' else 'collect_native')['main']())
