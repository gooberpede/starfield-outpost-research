# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise geometry arming state transitions with an independent channel oracle.

Reads owned controller sources. Writes new ignored disposable request/receipt
files and a result. Uses a modeled challenge channel, explicitly separate from
the actual worker/file-arm controls in the native candidate suite. No process,
save, deployment, network or analysis-database operations.
"""
from pathlib import Path
import copy
import hashlib
import json
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
from d5ai_controller import arm, poll_geometry, validate_geometry_plan, read_json


class Channel:
    def __init__(self, session):
        self.session = session
        self.lock = object()
        self.lease = SimpleNamespace(alive=lambda: True)
        self.expected = dict(geometry_schema='sor-d5ai-raw/2', geometry_header_bytes=456,
                             geometry_sites=[{}, {}, {}], context_schema='sor-d5ai-context/1', context_sites=[{}, {}], lifetime_schema='sor-d5ai-lifetime/1', lifetime_sites=[{}, {}, {}])
        self.identity_hash = 'a' * 64
        self.state = dict(owner='b' * 32, challenge=None)
        self.ready = False
        self.worker_armed = 0
        self.requests = 0
        self.saved = []

    def save(self):
        self.saved.append(copy.deepcopy(self.state))

    def request(self):
        if self.state['challenge'] is None:
            self.requests += 1
            self.state['challenge'] = f'{self.requests:032x}'
        return dict(state='REQUESTED', nonce=self.state['challenge'])

    def poll(self):
        if not self.ready:
            return dict(state='ALIVE_ACK_PENDING')
        if self.state['challenge'] is None:
            return dict(state='ALIVE_UNCHALLENGED')
        nonce = self.state['challenge']
        self.state['challenge'] = None
        return dict(state='HEALTHY_ACK', ack=dict(request_nonce=nonce, geometry_failed=False,
                                                geometry_armed=self.worker_armed, lifetime_failed=False, lifetime_unlogged_cutoff_ticks=0))


def main():
    out = Path(sys.argv[1]).resolve()
    if not out.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Fresh task-local output required')
    out.mkdir(exist_ok=False)
    checks = []

    def expect(name, value):
        if not value:
            raise AssertionError(name)
        checks.append(dict(name=name, passed=True))

    def refuses(name, callback):
        try:
            callback()
        except ValueError:
            checks.append(dict(name=name, passed=True))
        else:
            raise AssertionError(name)

    session = out / 'delayed-worker'
    session.mkdir()
    c = Channel(session)
    expect('fresh health challenge precedes publication', arm(c, 'A0')['state'] == 'GEOMETRY_CHALLENGE_PENDING')
    expect('no arm file before healthy ACK', not (session / 'geometry-arm.txt').exists())
    c.ready = True
    expect('publication is pending, never armed', arm(c, 'A0')['state'] == 'GEOMETRY_ARM_PUBLICATION_PENDING')
    expect('publication bytes bind session and request', (session / 'geometry-arm.txt').read_bytes() == (c.identity_hash + '\n1').encode())
    old_nonce = c.requests
    expect('new post-publication challenge is pending', arm(c, 'A0')['state'] == 'GEOMETRY_ARM_ACK_PENDING' and c.requests > old_nonce)
    expect('fresh ACK with worker not armed remains pending', arm(c, 'A0')['state'] == 'GEOMETRY_ARM_ACK_PENDING')
    expect('stale previous healthy ACK cannot arm', c.state['geometry_request']['state'] == 'PUBLICATION_PENDING')
    # Simulate reconnect without discarding the persisted challenge/request.
    reconnect = Channel(session)
    reconnect.state = copy.deepcopy(c.state)
    reconnect.requests = c.requests
    reconnect.ready = True
    reconnect.worker_armed = 1
    expect('reconnect requests a fresh challenge', arm(reconnect, 'A0')['state'] == 'GEOMETRY_ARM_ACK_PENDING')
    answer = arm(reconnect, 'A0')
    expect('only consumed request in fresh ACK becomes armed', answer['state'] == 'GEOMETRY_ARMED')
    expect('acknowledged request identity is exact', answer['geometry_request']['arm_ack']['geometry_armed'] == 1)
    refuses('different checkpoint cannot replace pending arm', lambda: arm(reconnect, 'A1'))
    # A natural scan may consume the arm before the challenge returns. It is a
    # captured checkpoint to inspect, never authority to trigger a second query.
    receipt = dict(schema='sor-d5ai-raw/2', identity_sha256=c.identity_hash,
                   request_id=1, snapshot_id=1, flushed=True)
    (session / 'geometry-request-1.json').write_text(json.dumps(receipt), encoding='utf8')
    reconnect.worker_armed = 0
    arm(reconnect, 'A0')
    expect('consumption before ACK prevents another operator query', arm(reconnect, 'A0')['state'] == 'GEOMETRY_CAPTURED_BEFORE_ARM_ACK')
    expect('capture receipt stays byte-unverified', poll_geometry(reconnect)['raw_verified'] is False)
    broken = copy.deepcopy(receipt)
    broken['identity_sha256'] = 'c' * 64
    (session / 'geometry-request-1.json').write_text(json.dumps(broken), encoding='utf8')
    refuses('foreign geometry receipt refused', lambda: poll_geometry(reconnect))
    c.lease = SimpleNamespace(alive=lambda: False)
    refuses('dead worker cannot arm', lambda: arm(c, 'A0'))
    expected = dict(geometry_schema='sor-d5ai-raw/2', geometry_header_bytes=456,
                    module_base=0x140000000, geometry_sites=[])
    plan = dict(geometry_schema='sor-d5ai-raw/2', geometry_sites=[])
    expected.update(context_schema='sor-d5ai-context/1', context_sites=[])
    plan.update(context_schema='sor-d5ai-context/1', context_sites=[])
    for rva, size in ((0x21e09ed, 5), (0x21e0aa5, 5), (0x21e0a7e, 9)):
        plan['geometry_sites'].append(dict(rva=rva, bytes=size, preimage_sha256='d' * 64))
        expected['geometry_sites'].append(dict(va=expected['module_base'] + rva, bytes=size, preimage_sha256='d' * 64))
    for rva, reason in ((0x789ce0, 5), (0x788e70, 6)):
        plan['context_sites'].append(dict(rva=rva, bytes=5, reason=reason, guard_sha256='f' * 64))
        expected['context_sites'].append(dict(va=expected['module_base'] + rva, bytes=5, reason=reason, guard_sha256='f' * 64))
    expected.update(lifetime_schema='sor-d5ai-lifetime/1', lifetime_header_bytes=96, lifetime_event_bytes=96, lifetime_capacity=32768, lifetime_sites=[])
    plan.update(lifetime_schema='sor-d5ai-lifetime/1', lifetime_sites=[])
    for rva, kind, adjustment in ((0x7aab10,'HOLDER_RESOURCE_MAP',16),(0x7ac260,'COLLECTION_GEOMETRY',8),(0x7ac2f0,'COLLECTION_MUTATION',8)):
        row=dict(rva=rva,bytes=5,kind=kind,allocation_adjustment=adjustment,guard_sha256='a'*64)
        plan['lifetime_sites'].append(row)
        actual=dict(row);actual['va']=expected['module_base']+rva;expected['lifetime_sites'].append(actual)
    validate_geometry_plan(expected, plan)
    expect('all three geometry native sites bind to exact plan', True)
    changed = copy.deepcopy(plan)
    changed['geometry_sites'][2]['preimage_sha256'] = 'e' * 64
    refuses('pre-unlock site drift refused', lambda: validate_geometry_plan(expected, changed))
    changed = copy.deepcopy(plan)
    changed['geometry_sites'].pop()
    refuses('missing geometry site refused', lambda: validate_geometry_plan(expected, changed))
    changed = copy.deepcopy(plan)
    changed['context_sites'].pop()
    refuses('missing whole-context site refused', lambda: validate_geometry_plan(expected, changed))
    changed = copy.deepcopy(plan)
    changed['context_sites'][1] = copy.deepcopy(changed['context_sites'][0])
    altered = copy.deepcopy(expected)
    altered['context_sites'][1] = copy.deepcopy(altered['context_sites'][0])
    refuses('duplicate context site refused even when plan agrees', lambda: validate_geometry_plan(altered, changed))
    changed = copy.deepcopy(plan)
    changed['context_sites'].reverse()
    altered = copy.deepcopy(expected)
    altered['context_sites'].reverse()
    refuses('reordered context site refused even when plan agrees', lambda: validate_geometry_plan(altered, changed))
    for fault in ('missing', 'duplicate', 'reorder', 'width', 'receiver'):
        changed=copy.deepcopy(plan)
        if fault=='missing':changed['lifetime_sites'].pop()
        elif fault=='duplicate':changed['lifetime_sites'][1]=copy.deepcopy(changed['lifetime_sites'][0])
        elif fault=='reorder':changed['lifetime_sites'].reverse()
        elif fault=='width':changed['lifetime_sites'][0]['bytes']=6
        else:changed['lifetime_sites'][0]['allocation_adjustment']=8
        refuses('lifetime '+fault+' refused', lambda changed=changed:validate_geometry_plan(expected,changed))
    duplicate = out / 'duplicate.json'
    duplicate.write_text('{"geometry_schema":"sor-d5ai-raw/2","geometry_schema":"sor-d5ai-raw/2"}', encoding='utf8')
    refuses('identical duplicate new JSON key refused', lambda: read_json(duplicate))
    pins = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in
            (Path(__file__), ROOT / 'runtime/construction-winner/d5ai_controller.py')}
    result = dict(schema='sor-d5ai-controller-qualification/1', source_pins=pins, checks=checks,
                  status='PASS', scope='Modeled independent challenge oracle; actual worker parsing and output exercised separately in native suite')
    (out / 'qualification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(checks=len(checks), status='PASS')))


if __name__ == '__main__':
    main()
