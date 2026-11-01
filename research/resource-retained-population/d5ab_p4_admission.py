# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline modeled admission negatives and retained loss-tuple reconciliation.

Reads owned code and a retained P3 synthetic capture. Writes one fresh ignored
receipt. No live process, control files, protected saves or native execution.
Modeled retail identities test validation only; they are never installed/run.
"""
import copy
import json
from pathlib import Path
import sys
import subprocess

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
from p4_controller import RetailController, LIVE, telemetry_counts, sha, write_new, pinned_json
from worker_health import disk_guard
from read_capture import inspect


def main():
    out = Path(sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    out.mkdir(exist_ok=False)
    disk_guard()
    controller = RetailController.__new__(RetailController)
    nonce = 'a' * 64
    controller.session = LIVE / ('session-' + nonce)
    controller.identity_hash = 'f' * 64
    sites = [dict(index=i, rva=0x1000 + i * 32, guard_sha256='b' * 64) for i in range(18)]
    controller.expected = dict(schema='sor-d5x/4', retail=True, nonce=nonce, host_sha256='c' * 64,
                               sfse_sha256='d' * 64, dll_sha256='e' * 64, module_base=0x140000000,
                               sites=[dict(site, va=0x140000000 + site['rva']) for site in sites])
    controller.plan = dict(process_image='C:/example/Starfield.exe', game_sha256='c' * 64,
                           sfse_sha256='d' * 64, dll_sha256='e' * 64, sites=sites, plan_sha256='1' * 64)
    admission = dict(state='PASS_OFFLINE_PREFLIGHT', plan_sha256='1' * 64, receipt_sha256='2' * 64)
    approval = dict(authority='B2_EXPLICIT_MAINTAINER_GO', plan_sha256='1' * 64,
                    preflight_sha256='2' * 64, session=str(controller.session),
                    identity_sha256='f' * 64, one_process_one_load_one_direct_travel=True)
    controller.validate_target(admission, approval)
    tests = ['modeled-matching-retail-validator-only']
    for label, place, key, value in (
        ('no-go', 'approval', 'authority', 'NOT_AUTHORIZED'),
        ('wrong-plan', 'approval', 'plan_sha256', '0' * 64),
        ('wrong-preflight', 'approval', 'preflight_sha256', '0' * 64),
        ('wrong-session', 'approval', 'session', str(controller.session) + '-old'),
        ('wrong-start-identity', 'approval', 'identity_sha256', '0' * 64),
        ('scope-extension', 'approval', 'one_process_one_load_one_direct_travel', False),
        ('failed-preflight', 'admission', 'state', 'FAIL'),
        ('preflight-plan', 'admission', 'plan_sha256', '0' * 64),
        ('fixture', 'expected', 'retail', False),
        ('schema', 'expected', 'schema', 'sor-d5x/3'),
        ('game', 'expected', 'host_sha256', '0' * 64),
        ('sfse', 'expected', 'sfse_sha256', '0' * 64),
        ('dll', 'expected', 'dll_sha256', '0' * 64),
        ('image', 'plan', 'process_image', 'C:/example/Other.exe'),
        ('sites', 'plan', 'sites', sites[:17]),
    ):
        objects = dict(approval=copy.deepcopy(approval), admission=copy.deepcopy(admission),
                       expected=copy.deepcopy(controller.expected), plan=copy.deepcopy(controller.plan))
        objects[place][key] = value
        candidate = RetailController.__new__(RetailController)
        candidate.session, candidate.identity_hash = controller.session, controller.identity_hash
        candidate.expected, candidate.plan = objects['expected'], objects['plan']
        try:
            candidate.validate_target(objects['admission'], objects['approval'])
        except (AssertionError, KeyError):
            tests.append('reject-' + label)
        else:
            raise AssertionError('Bad modeled retail admission accepted: ' + label)
    build = ROOT / '.local-work/d5x/p3-native-final04'
    path = build / 'stop-under-production/flush.jsonl'
    retained = json.loads(path.read_bytes().splitlines()[2])
    try:
        telemetry_counts(retained)
    except AssertionError:
        tests.append('actual-retained-flush-line3-telemetry-rejected')
    else:
        raise AssertionError('Known sampled anomaly accepted')
    summary = inspect(path.parent, sha(build / 'SorConstructionWinner.dll'))
    assert summary['durable_records'] == 65553
    assert summary['complete_session'] is False
    assert 'LOSS_TELEMETRY_INCOMPLETE_OR_CONTRADICTORY' in summary['damage']
    tests.append('actual-byte-durability-preserved-scientific-completion-refused')
    zero = dict(drops=0, queue_full=0, contention_exhausted=0, reentrant_losses=0,
                loss_generation=0, first_loss_sampled_admission=0, last_loss_sampled_admission=0,
                loss_bounds_uncertain=False, flushed=10)
    positive = dict(zero, drops=1, queue_full=1, loss_generation=1,
                    first_loss_sampled_admission=2, last_loss_sampled_admission=5)
    telemetry_counts(positive)
    for label, current, previous in (
        ('generation-bool', dict(zero, loss_generation=False), None),
        ('zero-uncertain', dict(zero, loss_bounds_uncertain=True), None),
        ('zero-has-bound', dict(zero, last_loss_sampled_admission=1), None),
        ('missing-known-first', dict(positive, first_loss_sampled_admission=0), None),
        ('reversed-bounds', dict(positive, first_loss_sampled_admission=6), None),
        ('shrinking-first', dict(positive, first_loss_sampled_admission=3), positive),
        ('shrinking-last', dict(positive, last_loss_sampled_admission=4), positive),
        ('uncertainty-cleared', positive, dict(positive, loss_bounds_uncertain=True)),
    ):
        try:
            telemetry_counts(current, previous)
        except AssertionError:
            tests.append('reject-loss-' + label)
        else:
            raise AssertionError('Invalid sampled-loss metadata accepted: ' + label)
    large = out / 'large-static-preflight.json'
    write_new(large, dict(state='NOT_AUTHORIZED', diagnostic='x' * 70000))
    assert pinned_json(large, sha(large))['state'] == 'NOT_AUTHORIZED'
    tests.append('static-pinned-input-over-64k-supported')
    receipt = out / 'initial-cli-error.json'
    command = [sys.executable, '-B', str(ROOT / 'runtime/construction-winner/p4_controller.py'),
               'start', '--session', str(out / 'nonexistent-session'),
               '--plan', str(large), '--plan-sha256', '0' * 64,
               '--preflight', str(large), '--preflight-sha256', sha(large),
               '--approval', str(large), '--approval-sha256', sha(large), '--out', str(receipt)]
    result = subprocess.run(command, capture_output=True)
    assert result.returncode != 0
    value = json.loads(receipt.read_bytes())
    assert value['state'] == 'CHECK_ERROR' and value['scientific_firstness_qualified'] is False
    assert not (out / 'nonexistent-session').exists()
    (out / 'initial-cli-error.stderr').write_bytes(result.stderr)
    tests.append('initial-cli-pin-failure-durable-check-error-no-session-write')
    keys = ('drops', 'queue_full', 'contention_exhausted', 'reentrant_losses', 'loss_generation',
            'first_loss_sampled_admission', 'last_loss_sampled_admission', 'loss_bounds_uncertain')
    write_new(out / 'receipt.json', dict(schema='sor-d5ab-p4-modeled-admission/1', passed=True, tests=tests,
              source={str(p): sha(p) for p in (Path(__file__), ROOT / 'runtime/construction-winner/p4_controller.py')},
              actual_sample=dict(path=str(path), sha256=sha(path), line=3, tuple={k: retained[k] for k in keys}),
              reader=dict(durable_records=summary['durable_records'], complete_session=summary['complete_session'], damage=summary['damage']),
              scope='Modeled validator and retained synthetic evidence only; no retail validation.'))
    print(json.dumps(dict(passed=True, tests=len(tests), out=str(out))))


if __name__ == '__main__':
    main()
