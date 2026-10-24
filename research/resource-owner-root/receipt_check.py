# SPDX-License-Identifier: GPL-3.0-or-later
"""Bind persisted diagnostic output to original framed native source identities.

Reads existing local prediction and seven original D4A receipt/ACK pairs.
Writes a fresh local receipt. Uses owned D4A independent decoder; no target,
source, analysis or Git mutation. Execute only after the D4C input freeze.
"""
import argparse
import json
from pathlib import Path
import struct
import sys

from audit import ROOT, pin, write
sys.path.insert(0, str(ROOT / 'research/resource-tungsten-acquisition'))
from qualify import independent


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--validation', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    assert args.output.resolve().is_relative_to(ROOT / '.local-work')
    result = json.loads((args.validation / 'conditional-prediction.json').read_text())
    attempt = ROOT / '.local-work/resource-tungsten-acquisition/retail-attempt01'
    checked, accepted, calls = [], [], []
    for capture in (86, 87, 88, 89, 829, 2881, 2941):
        path = attempt / f'capture-{capture:05d}.bin'
        session, row, end = independent(path)
        assert end['complete'] and row['capture'] == capture
        ack = json.loads(path.with_suffix('.ack.json').read_text())
        checked.append(dict(capture=capture, receipt_sha256=pin(path),
                            ack_sha256=pin(path.with_suffix('.ack.json'))))
        if capture < 100:
            calls.append(dict(capture=capture,
                resource=struct.unpack_from('<I', bytes.fromhex(row['ires']['raw']), 0x28)[0],
                weight_bits=row['effective_weight_bits']))
            continue
        raw = bytes.fromhex(row['source_context']['raw_source'])
        ox, oy = result['request']['descriptor']
        x, y = struct.unpack_from('<2i', raw, 0x10)
        source = f'0:{ox+x}:{oy+y}:{struct.unpack_from("<I", raw)[0]:08x}'
        fid = f'{struct.unpack_from("<I", bytes.fromhex(row["selected"]["raw_resource"]), 0x28)[0]:08x}'
        matches = [r for r in result['regions'] if r['resource'] == fid
            and r['ordered_xyzw_le'] == row['geometry']['ordered_xyzw']
            and r['native_bound_le'] == row['geometry']['raw_region'][:32]]
        assert len(matches) == 1
        accepted.append(dict(capture=capture, native_source=source, resource=fid,
            predicted_source=matches[0]['source'], shape_matches=1,
            source_identity_equal=matches[0]['source'] == source,
            status='SOURCE_AND_SHAPE_EXACT' if matches[0]['source'] == source
                   else 'SHAPE_EXACT_SOURCE_ID_DIFFERENT'))
    assert len(calls) == 4 and calls[0]['weight_bits'] == calls[1]['weight_bits'] == 0
    write(args.output, dict(primary=checked, geometry=accepted, calls=calls,
        zero_weight_water_has_no_generated_paths=True, historical_epoch='UNKNOWN',
        prediction_sha256=pin(args.validation / 'conditional-prediction.json')))
    print(json.dumps(accepted))


if __name__ == '__main__':
    main()
