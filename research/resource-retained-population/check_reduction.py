# SPDX-License-Identifier: GPL-3.0-or-later
"""Adversarial derivatives of real D5L captures; no process or original writes.

Reads the caller's qualification/basic journal, mutates copies in memory and
writes one fresh task-local result. These are reducer tests, not new native
observations or substitutes for Windows breakpoint qualification.
"""
import copy
import json
from pathlib import Path
import sys
from build import LOCAL
from reduce import PACKET, FIELDS, reduce


def main():
    root, output = (Path(p).resolve() for p in sys.argv[1:])
    assert root.is_relative_to(LOCAL) and output.is_relative_to(LOCAL) and not output.exists()
    rows = [json.loads(line) for line in (root/'basic/events.jsonl').read_text().splitlines()]
    assert reduce(rows)['chains']
    checks = []

    def test(label, mutate):
        changed = copy.deepcopy(rows)
        mutate(changed)
        result = reduce(changed)
        assert not result['chains'], label
        checks.append(dict(test=label, passed=True))

    def sample(r, site):
        return next(x for x in r if x.get('site') == site)

    def packet(r, site, field, value):
        row = sample(r, site)
        p = dict(zip(FIELDS, PACKET.unpack(bytes.fromhex(row['raw_packet']))))
        p[field] = value
        row['raw_packet'] = PACKET.pack(*(p[k] for k in FIELDS)).hex()

    test('invalid visited operand', lambda r:packet(r, 3, 'branch', 99))
    def wrong_hit(r):
        row = next(x for x in r if x.get('site') == 4 and
                   PACKET.unpack(bytes.fromhex(x['raw_packet']))[-1] == 1)
        row.update(slot='00'*24, slot_read=True)
    test('wrong hit slot', wrong_hit)
    test('mask out of range', lambda r:packet(r, 7, 'mask', 16))
    test('nonempty partial geometry', lambda r:sample(r, 8).update(population=(1).to_bytes(8, 'little').hex()+'00'*32))
    test('wrong generated points', lambda r:sample(r, 8).update(population=(2).to_bytes(8, 'little').hex()+'00'*32))
    test('failed insertion', lambda r:sample(r, 5).update(slot='00'*24, slot_read=True))
    test('query changed', lambda r:packet(r, 7, 'qx', 1))
    test('source identity changed', lambda r:packet(r, 8, 'source', 1))
    test('missing initialization', lambda r:r.__setitem__(slice(None), [x for x in r if x.get('site') not in (0, 1)]))
    test('missing completion', lambda r:sample(r, 8).update(read_complete=False))
    def missing_mask(r):
        r.remove(sample(r, 7))
        capture = 0
        for x in r:
            if x['kind'] == 'SAMPLE':
                capture += 1;x['capture'] = capture
    test('mask absent despite continuous sequence', missing_mask)
    test('missing exit', lambda r:r.remove(next(x for x in r if x.get('site') == 11)))
    def rearm(r):
        at = next(i for i,x in enumerate(r) if x.get('site') == 7)
        r[at:at] = [dict(kind='GAP'),dict(kind='ARM_BARRIER', sites=12,readback=True,all_threads=3)]
    test('gap then rearm cannot recover old identity', rearm)
    def fence(r, site):
        at = next(i for i,x in enumerate(r) if x.get('site') == 7)
        row = copy.deepcopy(sample(r, 0));row['site'] = site
        r.insert(at, row)
        capture = 0
        for x in r:
            if x['kind'] == 'SAMPLE':
                capture += 1;x['capture'] = capture
    test('reset in flight', lambda r:fence(r, 9))
    test('source reuse in flight', lambda r:fence(r, 1))
    test('owner destruction in flight', lambda r:fence(r, 10))
    # A forged non-synthetic session must fail before lifetime reduction.
    changed = copy.deepcopy(rows);changed[0]['synthetic'] = False
    try:
        reduce(changed)
        raise AssertionError('Native session accepted')
    except ValueError:
        checks.append(dict(test='retail session refused', passed=True))
    output.write_text(json.dumps(checks, indent=2)+'\n', encoding='utf8', newline='\n')
    print(len(checks), 'reducer controls PASS')


if __name__ == '__main__':
    main()
