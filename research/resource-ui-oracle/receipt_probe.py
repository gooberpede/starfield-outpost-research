# SPDX-License-Identifier: GPL-3.0-or-later
"""Original synthetic receipt prototype; no game/process access or dependencies.

From repo root: python -B research/resource-ui-oracle/receipt_probe.py
  --self-test --output .local-work/resource-ui-oracle/test01
Exclusively creates that directory and synthetic test files; never cleans it.
Reads only its own files. Tests framing/copy/accounting/fsync/readback, not a
debugger, native ABI, lifetime, identity resolution or retail ancestry.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import unittest

HEADER = struct.Struct('<4sQI32s')
MAX_BYTES = 1024 * 1024
MAX_MEMBERS = 4096
TAGS = ('spatial', 'atmosphere', 'biome')


def bounded_copy(begin, end, capacity, read):
    """Synthetic u64 range contract. Failed/budgeted reads are never empty."""
    if not all(type(v) is int and 0 <= v < 2**64 for v in (begin, end, capacity)):
        raise ValueError('range domain')
    if not begin <= end <= capacity or (end-begin) % 8 or begin % 8:
        raise ValueError('range shape')
    n = (end-begin)//8
    if n > MAX_MEMBERS:
        raise ValueError('LOSS: copy budget')
    if n == 0:
        return []
    if begin == 0:
        raise ValueError('nonempty null')
    raw = read(begin, n*8)
    if len(raw) != n*8:
        raise ValueError('LOSS: short read')
    return list(struct.unpack('<'+'Q'*n, raw))


def frame(seq, record):
    payload = json.dumps(record, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    if len(payload) > MAX_BYTES:
        raise ValueError('LOSS: frame budget')
    return HEADER.pack(b'SRO1', seq, len(payload), hashlib.sha256(payload).digest()) + payload


def decode(raw):
    rows = []; offset = 0
    while offset < len(raw):
        if len(raw)-offset < HEADER.size:
            raise ValueError('partial header')
        magic, seq, size, digest = HEADER.unpack_from(raw, offset)
        offset += HEADER.size
        if magic != b'SRO1' or seq != len(rows)+1 or size > MAX_BYTES:
            raise ValueError('framing/sequence')
        payload = raw[offset:offset+size]; offset += size
        if len(payload) != size or hashlib.sha256(payload).digest() != digest:
            raise ValueError('partial/corrupt payload')
        rows.append(json.loads(payload))
    if not rows or rows[-1].get('kind') != 'END' or any(r.get('kind') == 'LOSS' for r in rows):
        raise ValueError('missing terminal or LOSS')
    if any(r.get('kind') == 'END' for r in rows[:-1]):
        raise ValueError('duplicate terminal')
    return rows


def persist(path, rows):
    """ACK only after close/fsync, full independent readback and SHA validation."""
    raw = b''.join(frame(i+1, r) for i, r in enumerate(rows))
    with path.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    actual = path.read_bytes(); decode(actual)
    if actual != raw:
        raise ValueError('readback mismatch')
    ack = dict(bytes=len(raw), sha256=hashlib.sha256(actual).hexdigest(),
               records=len(rows), status='DURABLE_READBACK', synthetic=True)
    with path.with_suffix('.ack.json').open('x', encoding='utf8', newline='\n') as f:
        json.dump(ack, f, sort_keys=True); f.write('\n'); f.flush(); os.fsync(f.fileno())
    return ack


def classify(sample, resource, case):
    """Scoped population answer. Catalogue/geometry never inferred from names."""
    if sample.get('case') != case or sample.get('identity') != 'BOUND':
        return 'UNKNOWN'
    pops = sample.get('populations', {})
    if set(pops) != set(TAGS):
        return 'UNKNOWN'
    for p in pops.values():
        if p.get('status') != 'COMPLETE' or not isinstance(p.get('members'), list):
            return 'UNKNOWN'
        if any(not isinstance(v, str) or ':' not in v for v in p['members']):
            return 'UNKNOWN'
    if resource in pops['spatial']['members']:
        fresh = pops['spatial'].get('freshness')
        return 'SPATIAL_THIS_REFRESH' if fresh == 'THIS_REFRESH_REPLACED' else 'SPATIAL_AGE_UNKNOWN_OR_RETAINED'
    if any(resource in pops[t]['members'] for t in ('atmosphere', 'biome')):
        return 'NONSPATIAL_PRESENT'
    return 'ABSENT_FROM_THREE_SAMPLED_LISTS'


def fixture():
    return dict(kind='SAMPLE', case='synthetic-P1', identity='BOUND',
                populations={t:dict(status='COMPLETE', freshness='THIS_REFRESH_REPLACED',
                                    members=['fixture.esm:000001'] if t == 'spatial' else []) for t in TAGS})


def run_tests(out):
    class Tests(unittest.TestCase):
        def test_roundtrip_durable(self):
            rows=[fixture(),dict(kind='END')]; p=out/'complete.bin'
            ack=persist(p, rows)
            self.assertEqual(decode(p.read_bytes()), rows)
            self.assertEqual(ack['sha256'], hashlib.sha256(p.read_bytes()).hexdigest())
        def test_truncated_and_corrupt(self):
            raw=frame(1, fixture())+frame(2, dict(kind='END'))
            for n in (1, HEADER.size-1, len(raw)-1):
                with self.assertRaises(ValueError): decode(raw[:n])
            bad=bytearray(raw); bad[HEADER.size+1] ^= 1
            with self.assertRaises(ValueError): decode(bad)
        def test_sequence_terminal_loss(self):
            for rows in ([frame(2, dict(kind='END'))], [frame(1,fixture())],
                         [frame(1,dict(kind='LOSS')),frame(2,dict(kind='END'))],
                         [frame(1,dict(kind='END')),frame(2,dict(kind='END'))]):
                with self.assertRaises(ValueError): decode(b''.join(rows))
        def test_no_ack_on_partial(self):
            p=out/'partial.bin'
            with self.assertRaises(ValueError): persist(p, [fixture()])
            self.assertFalse(p.with_suffix('.ack.json').exists())
        def test_copy_bounds(self):
            raw=struct.pack('<QQ', 17, 23)
            self.assertEqual(bounded_copy(8,24,24,lambda a,n:raw),[17,23])
            self.assertEqual(bounded_copy(0,0,0,lambda a,n: self.fail()),[])
            for args in ((0,8,8),(8,7,8),(8,17,24),(8,24,16),(-8,0,0),(8,2**64,2**64)):
                with self.assertRaises(ValueError): bounded_copy(*args,lambda a,n:raw)
            with self.assertRaises(ValueError): bounded_copy(8,24,24,lambda a,n:raw[:8])
            with self.assertRaises(ValueError): bounded_copy(8,8+(MAX_MEMBERS+1)*8,8+(MAX_MEMBERS+1)*8,lambda a,n:raw)
        def test_source_and_retention(self):
            s=fixture(); r='fixture.esm:000001'; c='synthetic-P1'
            self.assertEqual(classify(s,r,c),'SPATIAL_THIS_REFRESH')
            s['populations']['spatial']['freshness']='RETAINED'
            self.assertEqual(classify(s,r,c),'SPATIAL_AGE_UNKNOWN_OR_RETAINED')
            s['populations']['spatial']['members']=[]
            s['populations']['biome']['members']=[r]
            self.assertEqual(classify(s,r,c),'NONSPATIAL_PRESENT')
            s['populations']['biome']['members']=[]
            self.assertEqual(classify(s,r,c),'ABSENT_FROM_THREE_SAMPLED_LISTS')
        def test_unknown_not_absent(self):
            s=fixture(); r='fixture.esm:000001'
            self.assertEqual(classify(s,r,'wrong'),'UNKNOWN')
            for status in ('LOSS','UNOBSERVED','INVALID'):
                s['populations']['atmosphere']['status']=status
                self.assertEqual(classify(s,r,'synthetic-P1'),'UNKNOWN')
            s=fixture(); s['identity']='UNKNOWN'
            self.assertEqual(classify(s,r,'synthetic-P1'),'UNKNOWN')
        def test_frame_budget(self):
            with self.assertRaises(ValueError): frame(1,dict(x='x'*MAX_BYTES))
    return unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))


if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--self-test', action='store_true', required=True)
    ap.add_argument('--output', type=Path, required=True)
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[2]/'.local-work'
    dest=args.output.resolve()
    if not dest.is_relative_to(root.resolve()):
        ap.error('output must be a fresh directory under repository .local-work')
    dest.mkdir(parents=True, exist_ok=False)
    result=run_tests(dest)
    raise SystemExit(0 if result.wasSuccessful() else 1)
