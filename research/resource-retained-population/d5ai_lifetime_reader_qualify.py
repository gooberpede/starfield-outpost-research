# SPDX-License-Identifier: GPL-3.0-or-later
"""Challenge lifetime framing, native prefix receipts and coverage binding offline.

Reads one complete native typed-ending session. Writes disposable altered copies
and explicitly modeled re-signed counter/CRC controls under ignored task output.
CRC controls check parser semantics, not resistance to a forged native producer.
No process, game, save, deployment, network or original evidence modification.
"""
from pathlib import Path
import copy
import json
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/construction-winner'))
from d5ai_read_lifetime import read_prefix, qualify_snapshot, EVENT, FRAME
from d5ai_read_geometry import read_session


def main():
    source, out = (Path(p).resolve() for p in sys.argv[1:3])
    if not out.is_relative_to(ROOT / '.local-work/d5ai-recorder'):
        raise ValueError('Fresh task-local output required')
    out.mkdir(exist_ok=False)
    checkpoint = json.loads((source / 'terminal.json').read_bytes())
    original = read_prefix(source, checkpoint)
    if original['records'] < 2:
        raise ValueError('Actual typed BEGIN and END native pair required')
    snapshots = read_session(source)['snapshots']
    checks = []

    def control(name, mutate, accepted=False):
        target = out / name
        target.mkdir()
        for leaf in ('identity.json', 'lifetimes.bin', 'lifetimes-flush.jsonl'):
            (target / leaf).write_bytes((source / leaf).read_bytes())
        state = copy.deepcopy(checkpoint)
        mutate(target, state)
        try:
            value = read_prefix(target, state)
        except (ValueError, KeyError, OSError):
            if accepted:
                raise
        else:
            if not accepted:
                raise AssertionError('Accepted altered ending evidence: ' + name)
            if value['raw_prefix_sha256'] != original['raw_prefix_sha256'] and name == 'unacknowledged-tail':
                raise AssertionError('Unacknowledged bytes entered authenticated prefix')
        checks.append(dict(name=name, passed=True, expected='ACCEPT_PRESERVED_PREFIX' if accepted else 'REFUSE'))

    def resign(target, state, data):
        count = (len(data) - 96) // 112
        row = copy.deepcopy(original['flush_row'])
        row.update(records=count, bytes=len(data), prefix_crc32=zlib.crc32(data))
        row['coverage_mark']['cursor'] = count
        row['coverage_mark']['generation_before'] = count
        row['coverage_mark']['generation_after'] = count
        for key in ('enqueued', 'written', 'flushed', 'acknowledged'):
            state['lifetime_' + key] = count
        state['lifetime_bytes'] = len(data)
        state['lifetime_prefix_crc32'] = row['prefix_crc32']
        (target / 'lifetimes.bin').write_bytes(data)
        (target / 'lifetimes-flush.jsonl').write_text(json.dumps(row) + '\n', encoding='utf8')

    def event_change(target, state, field, value):
        data = bytearray((target / 'lifetimes.bin').read_bytes()[:original['prefix_bytes']])
        values = list(EVENT.unpack_from(data, 112))
        values[field] = value
        EVENT.pack_into(data, 112, *values)
        struct.pack_into('<I', data, 108, zlib.crc32(data[112:208]))
        resign(target, state, data)

    for leaf in ('lifetimes.bin', 'lifetimes-flush.jsonl'):
        control('missing-' + leaf.replace('.', '-'), lambda target, state, leaf=leaf: (target / leaf).unlink())
    control('raw-crc-corruption', lambda target, state: (target / 'lifetimes.bin').write_bytes((target / 'lifetimes.bin').read_bytes()[:-1] + b'\x7f'))
    control('truncated-frame', lambda target, state: (target / 'lifetimes.bin').write_bytes((target / 'lifetimes.bin').read_bytes()[:-1]))
    control('whole-missing-pair', lambda target, state: (target / 'lifetimes.bin').write_bytes((target / 'lifetimes.bin').read_bytes()[:96]))
    control('unacknowledged-tail', lambda target, state: (target / 'lifetimes.bin').write_bytes((target / 'lifetimes.bin').read_bytes() + b'unpublished partial tail'), accepted=True)
    control('boolean-counter', lambda target, state: state.update(lifetime_flushed=True))
    for label, offset, value in (('frame-magic',96,0),('frame-size',100,95),('frame-sequence',104,2)):
        def frame_change(target,state,offset=offset,value=value):
            data=bytearray((target/'lifetimes.bin').read_bytes());struct.pack_into('<I',data,offset,value);resign(target,state,data)
        control(label,frame_change)
    def reordered(target,state):
        data=(target/'lifetimes.bin').read_bytes();resign(target,state,data[:96]+data[208:320]+data[96:208]+data[320:])
    control('reordered-native-pair',reordered)
    def reserved_header(target,state):
        data=bytearray((target/'lifetimes.bin').read_bytes());struct.pack_into('<Q',data,56,1);resign(target,state,data)
    control('header-reserved',reserved_header)
    control('wrong-receiver', lambda target, state: event_change(target, state, 7, 0x10000))
    control('BEGIN16-malformed', lambda target, state: event_change(target, state, 9, 16))
    control('unknown-kind', lambda target, state: event_change(target, state, 1, 4))
    control('missing-BEGIN', lambda target, state: event_change(target, state, 2, 1))

    def missing_end(target, state):
        data = (target / 'lifetimes.bin').read_bytes()
        resign(target, state, data[:208])
    control('missing-END', missing_end)

    def header_identity(target, state):
        data = bytearray((target / 'lifetimes.bin').read_bytes())
        data[64] ^= 1
        resign(target, state, data)
    control('header-identity', header_identity)

    def ledger_change(target, state, key, value):
        row = copy.deepcopy(original['flush_row'])
        row['coverage_mark'][key] = value
        (target / 'lifetimes-flush.jsonl').write_text(json.dumps(row) + '\n', encoding='utf8')
    for field, value in (('cursor', original['records'] + 1), ('ticks', original['qualified_through_ticks'] - 1),
                         ('active_before', 1), ('active_after', 1), ('generation_after', original['coverage_mark']['generation_before'] + 1),
                         ('loss', 1), ('failed', 1), ('cursor', True)):
        control('marker-' + field + '-' + str(value), lambda target, state, field=field, value=value: ledger_change(target, state, field, value))
    def in_range_cursor(target,state):
        row=copy.deepcopy(original['flush_row']);row['coverage_mark'].update(cursor=original['records']-1,generation_before=original['records']-1,generation_after=original['records']-1)
        (target/'lifetimes-flush.jsonl').write_text(json.dumps(row)+'\n',encoding='utf8')
    control('in-range-wrong-cursor',in_range_cursor)
    def equal_wrong_generation(target,state):
        row=copy.deepcopy(original['flush_row']);row['coverage_mark'].update(generation_before=original['records']+2,generation_after=original['records']+2)
        (target/'lifetimes-flush.jsonl').write_text(json.dumps(row)+'\n',encoding='utf8')
    control('equal-but-wrong-generation',equal_wrong_generation)
    def future_events(target,state):
        data=bytearray((target/'lifetimes.bin').read_bytes())
        for i in range(original['records']):
            start=96+i*112;values=list(EVENT.unpack_from(data,start+16));values[6]=original['qualified_through_ticks']+i+1;EVENT.pack_into(data,start+16,*values);struct.pack_into('<I',data,start+12,zlib.crc32(data[start+16:start+112]))
        resign(target,state,data)
    control('event-time-after-cursor-watermark',future_events)
    control('cutoff-watermark-tie', lambda target, state: state.update(lifetime_unlogged_cutoff_ticks=state['lifetime_qualified_through_ticks']))
    control('stale-watermark', lambda target, state: state.update(lifetime_qualified_through_ticks=state['lifetime_qualified_through_ticks'] - 1))
    control('ledger-missing', lambda target, state: (target / 'lifetimes-flush.jsonl').write_bytes(b''))

    def end_change(target,state,change):
        data=bytearray((target/'lifetimes.bin').read_bytes())
        begin=list(EVENT.unpack_from(data,112));end=list(EVENT.unpack_from(data,224));change(begin,end)
        EVENT.pack_into(data,224,*end);struct.pack_into('<I',data,220,zlib.crc32(data[224:320]));resign(target,state,data)
    control('intra-call-tie-exact-phase-pair',lambda target,state:end_change(target,state,lambda begin,end:end.__setitem__(6,begin[6])),accepted=True)
    control('decreasing-intra-call-time',lambda target,state:end_change(target,state,lambda begin,end:end.__setitem__(6,begin[6]-1)))
    for field,label in ((3,'invocation'),(4,'parent'),(5,'thread')):
        def mismatch(target,state,field=field):
            def change(begin,end):end[6]=begin[6];end[field]=begin[field]+1
            end_change(target,state,change)
        control('intra-tie-mismatched-'+label,mismatch)
    def receiver_mismatch(target,state):
        def change(begin,end):end[6]=begin[6];end[7]+=8;end[8]+=8
        end_change(target,state,change)
    control('intra-tie-mismatched-receiver-allocation',receiver_mismatch)
    def kind_mismatch(target,state):
        def change(begin,end):end[6]=begin[6];end[1]=2 if begin[1]==1 else 1;end[7]=end[8]+(16 if end[1]==1 else 8)
        end_change(target,state,change)
    control('intra-tie-mismatched-kind',kind_mismatch)

    # The raw history must retain exceptions. Scientific identity/lifetime
    # interpretation rejects their success consequence in the separate reducer.
    target = out / 'exception-preserved'
    target.mkdir()
    for leaf in ('identity.json', 'lifetimes.bin', 'lifetimes-flush.jsonl'):
        (target / leaf).write_bytes((source / leaf).read_bytes())
    state = copy.deepcopy(checkpoint)
    data = bytearray((target / 'lifetimes.bin').read_bytes())
    values = list(EVENT.unpack_from(data, 224))
    values[9] = 16
    EVENT.pack_into(data, 224, *values)
    struct.pack_into('<I', data, 220, zlib.crc32(data[224:320]))
    resign(target, state, data)
    assert read_prefix(target, state)['events'][1]['status'] == 16
    checks.append(dict(name='status16-retained-without-asserting-success', passed=True))
    baseline = snapshots[0]
    qualify_snapshot(baseline, original)
    for name, mutate in (
            ('late-onset', lambda journal: journal.update(qualified_from_ticks=baseline['header']['ticks_begin'] + 1)),
            ('short-query-coverage', lambda journal: journal.update(qualified_through_ticks=baseline['header']['completion_ticks'] - 1))):
        changed = copy.deepcopy(original)
        mutate(changed)
        try:
            qualify_snapshot(baseline, changed)
        except ValueError:
            checks.append(dict(name=name, passed=True))
        else:
            raise AssertionError(name)
    result = dict(schema='sor-d5ai-lifetime-reader-controls/1', status='PASS', native_prefix_sha256=original['raw_prefix_sha256'], reader_sha256=__import__('hashlib').sha256((ROOT/'runtime/construction-winner/d5ai_read_lifetime.py').read_bytes()).hexdigest(), native_dll_sha256=checkpoint['dll_sha256'], checks=checks)
    (out / 'qualification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(status='PASS', checks=len(checks))))


if __name__ == '__main__':
    main()
