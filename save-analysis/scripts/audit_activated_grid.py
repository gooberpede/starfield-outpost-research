"""SPDX-License-Identifier: GPL-3.0-or-later
SOR-EXP-0019 original selected numeric audit, source-informed by installed native
functions recorded in the report. Reads pinned ESM/executable and verified prior
terrain snapshots. Writes a NEW output directory of selected numeric tables and
hash receipts; no raw assets, target, save, database, network or Git effects.
Stdlib and existing project readers only. Requires 40 GB free on C: and D:.
Not a continuous planetary-position API. DNAM sizes are not metres.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import struct

from inventory_historical_saves import guard, identity
from inspect_outpost_definitions import esm_records
from audit_beacon_projection import audit
from audit_durable_center import table

EXE_SHA = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
ESM_SHA = '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'
N = 49152


def hierarchy(i, block=12):
    if not 0 <= i < 16*block*256:
        raise ValueError('INDEX_RANGE')
    coarse, rest = divmod(i, 16*block)
    sub, fine = divmod(rest, block)
    return coarse, sub, fine


def signed_remainder(value, divisor):
    """Integer C/C++ remainder; avoids a floating division for large values."""
    return (1 if value >= 0 else -1)*(abs(value) % divisor)


def offset(tag, i, j, dx, dy, n=N):
    """96f5c0's bounded per-axis remainder/wrap and four-tag transitions."""
    if tag not in range(4) or not (0 <= i < n and 0 <= j < n):
        raise ValueError('INVALID_GRID')
    x, y = i+signed_remainder(dx, n), j+signed_remainder(dy, n)
    cross_x, cross_y = not 0 <= x < n, not 0 <= y < n
    return tag ^ int(cross_x) ^ (3*int(cross_y)), x % n, y % n


def transform(matrix, x, y, width=16, height=16):
    # 851d20 uses a centred float coordinate then truncates toward zero.
    a, b, c, d = matrix
    hx, hy = (width-1)*.5, (height-1)*.5
    return int(a*(x-hx)+b*(y-hy)+hx), int(c*(x-hx)+d*(y-hy)+hy)


def pe_matrices(path):
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != EXE_SHA:
        raise ValueError('EXE_HASH')
    pe = struct.unpack_from('<I', data, 60)[0]
    count, optional = struct.unpack_from('<H', data, pe+6)[0], struct.unpack_from('<H', data, pe+20)[0]
    start = pe+24+optional
    rva = 0x5907c10  # static VA 145907c10 minus image base 140000000
    for i in range(count):
        _, va, size, raw = struct.unpack_from('<4I', data, start+40*i+8)
        if va <= rva and rva+128 <= va+size:
            return [struct.unpack_from('<4i', data, raw+rva-va+16*j) for j in range(8)]
    raise ValueError('PE_TABLE_RANGE')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--exe', type=Path, required=True)
    ap.add_argument('--esm', type=Path, required=True)
    ap.add_argument('--session', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    guard(a.output.parent)  # guard checks free space on both C: and D: itself.
    before = [identity(p) for p in (a.exe, a.esm)]
    if before[0]['sha256'] != EXE_SHA or before[1]['sha256'] != ESM_SHA:
        raise ValueError('PINNED_INPUT_HASH')
    if a.output.exists():
        raise FileExistsError(a.output)
    matrices = pe_matrices(a.exe)
    expected = [(1,0,0,1),(0,-1,1,0),(-1,0,0,-1),(0,1,-1,0),
                (1,0,0,-1),(0,1,1,0),(-1,0,0,1),(0,-1,-1,0)]
    if matrices != expected:
        raise ValueError('ORIENTATION_TABLE_MISMATCH')
    dimensions = collections.Counter()
    examples, blocks, patterns = {}, {}, []
    for r, fields in esm_records(a.esm, {b'SFBK', b'SFPT'}):
        if r['type'] == 'SFBK':
            size = struct.unpack('<2I', fields[b'DNAM'])
            dimensions[size] += 1
            examples.setdefault(size, f"{r['formid']:08X}")
            blocks[r['formid']] = size
        else:
            patterns.append((r, fields))
    dims = [dict(x=x, y=y, records=count, example=examples[(x,y)],
                 span_x=((x-2)&0xffffffff)//12, span_y=((y-2)&0xffffffff)//12,
                 status='unsigned arithmetic only; zero/undersized not footprint proof' if min(x,y)<14 else 'positive span under pinned B=12 merge=2')
            for (x,y), count in sorted(dimensions.items())]
    placements = []
    for r, fields in patterns:
        refs, flags = fields.get(b'FNAM', b''), fields.get(b'GNAM', b'')
        if len(refs) != 1024 or len(flags) != 256:
            raise ValueError('PATTERN_SHAPE')
        for index, fid in enumerate(struct.unpack('<256I', refs)):
            if flags[index]&8 and fid in blocks and min(blocks[fid]) >= 14:
                size = blocks[fid]
                placements.append(dict(pattern=f"{r['formid']:08X}", block=f'{fid:08X}',
                    slot=index, x=index//16, y=index%16, raw_x=size[0], raw_y=size[1],
                    span_x=(size[0]-2)//12, span_y=(size[1]-2)//12,
                    orientation=flags[index]>>5))
    terrain = []
    labels = ('baseline-003','control-003','premove-003','moved-003','saved-003',
              'reloaded-003','reload-control-003','visit-002','control-002')
    captured_inputs = []
    for label in labels:
        folder = a.session/label
        manifest = folder/'records.jsonl'
        captured_inputs.append(identity(manifest))
        records = [json.loads(s) for s in manifest.read_text().splitlines()]
        r = next(r for r in records if r.get('kind')=='raw' and r.get('root')=='terrain')
        path = folder/r['file']; saved = identity(path); captured_inputs.append(saved)
        if saved['sha256'] != r['sha256'] or path.stat().st_size != r['bytes']:
            raise ValueError('CAPTURE_HASH')
        data = path.read_bytes()
        mode = struct.unpack_from('<I', data, 0x20)[0]
        member = 0x1a8 if mode==3 else 0xb0
        pair = struct.unpack_from('<2d', data, member)
        result = audit(pair)
        terrain.append(dict(label=label, mode=mode, member=hex(member), **result,
            shift_to_SOR002=[10465-result['i'],21122-result['j']],
            shift_to_SOR003=[10467-result['i'],21144-result['j']]))
        assert (result['tag'], result['i'], result['j']) == (1,10464,21120)
    after = [identity(p) for p in (a.exe,a.esm)]
    if before != after:
        raise ValueError('INPUT_CHANGED')
    if captured_inputs != [identity(Path(v['path'])) for v in captured_inputs]:
        raise ValueError('CAPTURE_CHANGED')
    a.output.mkdir(parents=True)
    table(a.output/'block-dimensions.csv', dims)
    selected, seen = [], set()
    selected_counts = collections.Counter()
    for row in placements:
        span = (row['span_x'], row['span_y'])
        key = (row['pattern'], row['block'])
        if key not in seen and selected_counts[span] < 8:
            selected.append(row); seen.add(key); selected_counts[span] += 1
    table(a.output/'pattern-positive-spans.csv', selected)
    table(a.output/'active-terrain-pairs.csv', terrain)
    table(a.output/'orientation-matrices.csv', [dict(index=i, a=m[0], b=m[1], c=m[2], d=m[3]) for i,m in enumerate(matrices)])
    summary = dict(before=before, after=after, capture_inputs=captured_inputs,
        blocks=sum(dimensions.values()), patterns=len(patterns), nonsquare_blocks=sum(c for (x,y),c in dimensions.items() if x!=y),
        positive_span_placements=len(placements), selected_placements=len(selected), spans=dict(collections.Counter(f"{r['span_x']}x{r['span_y']}" for r in placements)),
        captured_active_pairs=len(terrain), maximum_angle_error=max(max(abs(r['longitude_error_rad']),abs(r['latitude_error_rad'])) for r in terrain),
        conclusion='DISCRETE FRAME/FOOTPRINT AUDIT; CONTINUOUS CENTER OPEN')
    (a.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in ('before','after','capture_inputs')},indent=2))


if __name__ == '__main__':
    main()
