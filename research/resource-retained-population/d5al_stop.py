# SPDX-License-Identifier: GPL-3.0-or-later
"""Trusted D5AL owned STOP with a separately pinned minimal controller closure.

SOR-P-0002 adaptation of frozen D5AI admission. Reads pinned plan, approval,
preflight and existing session ownership; writes only an authenticated STOP and
exclusive receipt. No launch, deployment, extra geometry, save or network action.
Safety-sensitive imports occur only after explicit optimization refusal.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without PYTHONOPTIMIZE, -O or -OO')
import copy
from pathlib import Path
import d5ai_episode as original


def authority(plan, admission, approval, session, identity_hash):
    original.require(plan.get('episode') == 'B', 'B-only plan required')
    original.require(approval.get('authority') == 'D5AL_EPISODE_B_EXPLICIT_MAINTAINER_GO',
                     'New episode-specific D5AL B maintainer GO required')
    original.require(approval.get('profile') == 'Starfield - SFSE' and approval.get('steam_cloud') == 'DISABLED',
                     'Fresh intended profile and disabled Steam Cloud confirmation required')
    legacy = copy.deepcopy(approval)
    legacy['authority'] = 'D5AI_EPISODE_B_EXPLICIT_MAINTAINER_GO'
    original.validate_authority(plan, admission, legacy, session, identity_hash)
    return legacy


def distinct(identity, plan, identity_hash):
    baseline = plan['d5ak_a_process']
    original.require(identity['creation_filetime'] != baseline['creation_filetime'] and
                     identity_hash != baseline['identity_sha256'] and identity['nonce'] != baseline['nonce'],
                     'New process birth and session positively distinct from successful D5AK A required')


class TrustedController(original.EpisodeController):
    def validate_target(self, admission, approval):
        original.verify_controller_pins(self.plan)
        original.require(original.sha(__file__) == self.plan['trusted_stop_sha256'], 'Trusted STOP source changed')
        distinct(self.expected, self.plan, self.identity_hash)
        legacy = authority(self.plan, admission, approval, self.session, self.identity_hash)
        super().validate_target(admission, legacy)


def main():
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=('stop',))
    for name in ('plan', 'preflight', 'approval'):
        p.add_argument('--' + name, type=Path, required=True)
        p.add_argument('--' + name + '-sha256', required=True)
    p.add_argument('--session', type=Path, required=True)
    p.add_argument('--reason', default='operator-directed D5AL trusted fallback STOP')
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    original.require(a.out.resolve().is_relative_to(original.ROOT / '.local-work/d5al'), 'Exclusive D5AL receipt required')
    plan = original.pinned_json(a.plan, a.plan_sha256)
    plan['plan_sha256'] = a.plan_sha256
    before = original.pinned_json(a.preflight, a.preflight_sha256)
    before['receipt_sha256'] = a.preflight_sha256
    controller = TrustedController(a.session, original.strict_session_json(a.session / 'identity.json'),
                                   plan, before, original.pinned_json(a.approval, a.approval_sha256), 'stop')
    try:
        original.write_new(a.out, controller.request_stop(a.reason))
    finally:
        controller.close()

if __name__ == '__main__':
    main()
