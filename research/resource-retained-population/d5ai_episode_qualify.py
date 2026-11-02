# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise separate episode authority and owned operations source gates offline.

Writes fresh ignored modeled plans and receipts only. No processes, live saves,
deployment, game actions, network or approval are created by these controls.
Actual native worker controls are reported separately by the recorder suite.
"""
from pathlib import Path
import copy
import json
import sys

from d5ai_episode import SCHEMA, CONTROL_PATHS, scope_for_episode, validate_authority, verify_controller_pins, sha, SessionController, strict_session_json
from d5ai_operations import PHASES, LEGACY_PHASES, phase_pins, legacy_plan, worker_json

ROOT = Path(__file__).resolve().parents[2]


def main():
    out = Path(sys.argv[1]).resolve()
    if not out.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Fresh task-local output required')
    out.mkdir(exist_ok=False)
    checks = []

    def good(name, action):
        action()
        checks.append(dict(name=name, passed=True))

    def refuses(name, action):
        try:
            action()
        except (ValueError, KeyError):
            checks.append(dict(name=name, passed=True))
        else:
            raise AssertionError(name)

    for episode in ('A', 'B'):
        plan = dict(schema=SCHEMA, episode=episode, scope=scope_for_episode(episode), plan_sha256='a' * 64,
                    run_card_sha256='b' * 64, save52_sha256='c' * 64)
        admission = dict(state='PASS_OFFLINE_PREFLIGHT', plan_sha256='a' * 64, receipt_sha256='d' * 64)
        session = out / ('modeled-session-' + episode)
        approval = dict(authority=f'D5AI_EPISODE_{episode}_EXPLICIT_MAINTAINER_GO', episode=episode,
                        scope=scope_for_episode(episode), plan_sha256='a' * 64, preflight_sha256='d' * 64,
                        session=str(session), identity_sha256='e' * 64, run_card_sha256='b' * 64,
                        save52_sha256='c' * 64)
        good(episode + ' exact modeled authority', lambda: validate_authority(plan, admission, approval, session, 'e' * 64))
        for field in ('authority', 'episode', 'plan_sha256', 'preflight_sha256', 'session', 'identity_sha256', 'run_card_sha256', 'save52_sha256'):
            wrong = copy.deepcopy(approval)
            wrong[field] = 'B2_EXPLICIT_MAINTAINER_GO' if field == 'authority' else 'foreign'
            refuses(episode + ' wrong ' + field,
                    lambda wrong=wrong: validate_authority(plan, admission, wrong, session, 'e' * 64))
        for field, value in (('automatic_repeats', 1), ('new_saves', 1), ('forced_regeneration', True),
                             ('processes', 2), ('query_checkpoints', 3), ('processes', True)):
            wrong = copy.deepcopy(plan)
            wrong['scope'][field] = value
            refuses(episode + ' scope ' + field + repr(value), lambda wrong=wrong: validate_authority(wrong, admission, approval, session, 'e' * 64))
    plan = dict(controller_pins={str(p): sha(p) for p in CONTROL_PATHS},
                phase_pins={str(p): sha(p) for p in PHASES},
                operations_sha256=sha(Path(__file__).with_name('d5ai_operations.py')))
    good('exact controller source closure', lambda: verify_controller_pins(plan))
    good('exact operations source closure', lambda: phase_pins(plan))
    for key in ('controller_pins', 'phase_pins'):
        wrong = copy.deepcopy(plan)
        wrong[key].pop(next(iter(wrong[key])))
        refuses('missing ' + key, lambda wrong=wrong, key=key: verify_controller_pins(wrong) if key == 'controller_pins' else phase_pins(wrong))
    projected = legacy_plan(plan)
    if {Path(p).resolve() for p in projected['phase_pins']} != LEGACY_PHASES:
        raise AssertionError('Legacy component projection')
    checks.append(dict(name='component projection pins exact owned legacy helpers', passed=True))
    same = out / 'same-qpc.json'
    same.write_text('{"qpc_frequency":100,"qpc_frequency":100}', encoding='utf8')
    good('identical legacy QPC duplicate accepted', lambda: worker_json(same))
    for text in ('{"qpc_frequency":100,"qpc_frequency":101}', '{"geometry_schema":1,"geometry_schema":1}',
                 '{"lifetime_failed":false,"lifetime_failed":false}'):
        path = out / ('duplicate-' + str(len(checks)) + '.json')
        path.write_text(text, encoding='utf8')
        refuses('ambiguous worker JSON ' + str(len(checks)), lambda path=path: worker_json(path))
    import p4_controller as historical_p4
    for method in ('__init__','poll','terminal'):
        if getattr(SessionController,method).__globals__['read_json'] is not strict_session_json:
            raise AssertionError('Private inherited method parser: '+method)
    if historical_p4.read_json is strict_session_json:
        raise AssertionError('Historical P4 parser was mutated')
    checks.append(dict(name='inherited methods use isolated strict single parser',passed=True))
    for label,text in (('nonfinite','{"value":NaN}'),('boolean-legacy-QPC','{"qpc_frequency":true,"qpc_frequency":1}'),('oversize',' '*65537)):
        path=out/(label+'.json');path.write_text(text,encoding='utf8')
        refuses(label+' refused',lambda path=path:strict_session_json(path))
    result = dict(schema='sor-d5ai-episode-controls/1', status='PASS', checks=checks,
                  scope='Modeled authority/source/JSON controls only; no actual preflight, process, worker or live action')
    (out / 'qualification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(status='PASS', checks=len(checks))))


if __name__ == '__main__':
    main()
