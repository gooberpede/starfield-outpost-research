# SPDX-License-Identifier: GPL-3.0-or-later
"""Finite offline C2 transit calculations and protected-input audit.

Reads pinned local baseline/definition receipts, installed EXE and Git identity.
Writes one exclusively created ignored JSON receipt. No target invocation,
analysis/save/configuration mutation, dependencies or network. See README.md.
"""
import argparse
import json
import math
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'research/s1-storage'))
from catalog import pin
from inventory_historical_saves import guard


def f32(x):
    return struct.unpack('<f', struct.pack('<f', x))[0]


def crossing(delta, threshold):
    if not math.isfinite(delta) or delta <= 0 or not math.isfinite(threshold) or threshold < 0:
        raise ValueError('finite positive delta and finite nonnegative threshold required')
    a = 0.0
    n = 0
    while a <= threshold:
        b = f32(a + delta)
        if b <= a:
            raise ValueError('binary32 accumulator cannot advance')
        a = b
        n += 1
    return dict(updates=n, accumulator=a, ideal_delivered_seconds=n * delta)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    assert args.run.isalnum()
    guard()
    work = ROOT / '.local-work/c2-transit'
    baseline = json.loads((work / 'baseline.json').read_text(encoding='utf8'))
    checks = []

    def check(label, condition):
        assert condition, label
        checks.append(label)

    for item in baseline['protected']:
        check('protected unchanged: ' + item['path'], pin(item['path']) == item)
    for key in ('index', 'brief'):
        check(key + ' unchanged', pin(baseline[key]['path']) == baseline[key])
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT,
                                  env=dict(os.environ, GIT_OPTIONAL_LOCKS='0')).decode().strip()
    check('HEAD unchanged', head == baseline['head'])
    definitions = json.loads((work / 'definitions01.json').read_text(encoding='utf8'))
    check('fresh definitions source pinned', pin(definitions['source']['path']) == definitions['source'])
    scales = {}
    for row in definitions['rows']:
        if row['edid'] in ('fCalendarTimeScaleGround', 'fCalendarTimeScaleSpace'):
            data = next(bytes.fromhex(v) for k, v in row['fields'] if k == 'DATA')
            scales[row['edid']] = struct.unpack('<f', data)[0]
    check('installed ground15 space5', scales == dict(fCalendarTimeScaleGround=15.0,
                                                     fCalendarTimeScaleSpace=5.0))
    exe = Path(baseline['protected'][0]['path'])
    constants = {}
    with exe.open('rb') as stream:
        stream.seek(0x3c)
        pe = int.from_bytes(stream.read(4), 'little')
        stream.seek(pe + 6)
        count = int.from_bytes(stream.read(2), 'little')
        stream.seek(pe + 20)
        optional = int.from_bytes(stream.read(2), 'little')
        stream.seek(pe + 24 + optional)
        sections = [struct.unpack_from('<4I', stream.read(40), 8) for _ in range(count)]
        for va, expected in ((0x144f04768, 2.0), (0x144f04980, 4.0)):
            rva = va - 0x140000000
            vs, section, raw_size, raw = next(s for s in sections if s[1] <= rva < s[1] + s[2])
            offset = raw + rva - section
            stream.seek(offset)
            data = stream.read(4)
            value = struct.unpack('<f', data)[0]
            check('native constant ' + hex(va), value == expected)
            constants[hex(va)] = dict(file_offset=offset, bytes=data.hex(), value=value)
    durations = []
    for source_seconds in (30.0, 15.0):
        hours = f32(f32(source_seconds / 3600.0) * scales['fCalendarTimeScaleGround'])
        ticks = math.trunc(f32(max(hours, f32(0.03333333507180214)) * f32(41.66666793823242)))
        durations.append(ticks)
    check('load5 departure2 ticks', durations == [5, 2])
    controls = 0
    for delta, threshold in ((0, 6), (-1, 6), (math.nan, 6), (math.inf, 6), (1, -1), (1, math.nan)):
        try:
            crossing(delta, threshold)
        except ValueError:
            controls += 1
        else:
            raise AssertionError('invalid input accepted')
    check('six invalid arithmetic inputs rejected', controls == 6)
    check('strict boundary counterexample', crossing(1.0, 6.0)['updates'] == 7)
    detached = {str(rate): dict(first=crossing(f32(1.0 / rate), 2.0),
                                complete=crossing(f32(1.0 / rate), 6.0)) for rate in (1, 30, 60)}
    examples = []
    for scale in (15.0, 5.0):
        tick_seconds = 86.4 / scale
        # Ideal continuous clock, immediate handlers, exactly6 wall seconds/leg.
        # Departure deadlines are integer ticks; movement creates the next arm phase.
        arrival_ticks = 0.0
        cycles = []
        for _ in range(3):
            begin_ticks = arrival_ticks
            for leg in range(2):
                departure_ticks = math.floor(arrival_ticks) + sum(durations)
                arrival_ticks = departure_ticks + 6.0 / tick_seconds
            cycles.append((arrival_ticks - begin_ticks) * tick_seconds)
        steady = (2 * sum(durations) + 2 * math.floor(6.0 / tick_seconds)) * tick_seconds
        check('ideal steady phase recurrence ' + str(scale), math.isclose(cycles[-1], steady))
        top = 2 * sum(durations) * 86.4 / scale
        low = (2 * sum(durations) - 4) * 86.4 / scale
        examples.append(dict(calendar_scale=scale, dock_phase_envelope_open_low=low,
                             dock_phase_envelope_closed_high=top,
                             detached_two_leg_nominal_seconds=12.0,
                             conditional_roundtrip_open_low=low + 12.0,
                             conditional_roundtrip_closed_high=top + 12.0,
                             ideal_first_three_roundtrips_seconds=cycles,
                             ideal_steady_roundtrip_seconds=steady,
                             assumptions='fresh detached paths; movement seconds/wall seconds=1; '
                             'no fuel/queue/admission/action extra time; ideal monotonic integer '
                             'calendar; arbitrary arm phase; movement overshoot/float drift omitted'))
    guard()
    result = dict(checks=checks, count=len(checks), baseline=pin(work / 'baseline.json'),
                  definitions=pin(work / 'definitions01.json'), helper=pin(__file__),
                  constants=constants, dock_ticks=durations, scales=scales,
                  detached_fixed_delta=detached, examples=examples,
                  scope='finite arithmetic and byte/integrity checks; not native execution, '
                  'clock admission proof, measured tolerance or save-history reconstruction')
    (work / (args.run + '.json')).open('x', encoding='utf8', newline='\n').write(json.dumps(result, indent=2) + '\n')
    print('PASS', len(checks), 'checks;', json.dumps(examples))


if __name__ == '__main__':
    main()
