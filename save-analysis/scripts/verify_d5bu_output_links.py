# SPDX-License-Identifier: GPL-3.0-or-later
"""Verify the six selected D5BU output-link saves with owned window logic."""
import argparse
import csv
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from analyze_manual_corpus import decode, sha
from d5bt_reader import disk_guard, pin, require
from probe_output_link_structure import inspect

ROOT = Path(__file__).resolve().parents[2]
ORACLE = ROOT / 'docs/experiments/output-link-validation'
LABELS = ('L0', 'L0C', 'L1', 'L1C', 'L2', 'L2C')
ROLES = ('beacon', 'storage', 'extractor', 'solar')


def table(name, key):
    with (ORACLE / name).open(encoding='utf-8', newline='') as stream:
        return {key(row): row for row in csv.DictReader(stream)}


def offsets(value):
    return [int(offset) for offset in value.split(';') if offset]


def verify(paths, receipt_parent):
    manifest = table('manifest.csv', lambda row: row['label'])
    candidates = table('candidates.csv', lambda row: row['label'])
    comparisons = table('endpoint-windows.csv', lambda row: (row['before'], row['after']))
    rows = []
    differences = []
    previous_windows = None
    payloads = []
    original_storage = bytes.fromhex(candidates['L0']['storage_token'])
    for label, path in zip(LABELS, paths, strict=True):
        disk_guard(receipt_parent)
        expected = manifest[label]
        source = (int(expected['copy_size']), expected['copy_sha256'])
        with path.open('rb') as stream:
            physical = stream.read(source[0] + 1)
        require((len(physical), sha(physical)) == source, f'{label}: source identity')
        data, _ = decode(physical)
        require(len(data) == int(expected['decoded_size']) and sha(data) == expected['decoded_sha256'],
                f'{label}: decoded identity')
        found = inspect(data, label)
        oracle = candidates[label]
        envelope = found['envelope']
        for field in ('marker_offset', 'payload_offset', 'payload_length', 'discriminator'):
            require(envelope[field] == int(oracle[field]), f'{label}: {field}')
        for field in ('original_literal_offsets', 'substituted_literal_offsets', 'endpoint_pair_offsets'):
            require(envelope[field] == offsets(oracle[field]), f'{label}: {field}')
        start = int(oracle['payload_offset'])
        length = int(oracle['payload_length'])
        payload = data[start:start + length]
        require(data[start-8:start] == b'\x79\x00\x00\x00' + length.to_bytes(4, 'little')
                and data[start+length:start+length+8] == bytes.fromhex('7a00000028000000'),
                f'{label}: fixed envelope boundary')
        payloads.append(payload)
        windows = []
        for role in ROLES:
            point = int(oracle[f'{role}_main_offset'])
            window = data[point:point+512]
            endpoint = found['endpoints'][role]
            require(len(window) == 512 and sha(window) == oracle[f'{role}_window_512_sha256']
                    and endpoint['main_offset'] == point
                    and window[1:4].hex() == endpoint['token'] == oracle[f'{role}_token'],
                    f'{label}: {role} endpoint')
            require(len(endpoint['token_offsets']) == int(oracle[f'{role}_token_count']),
                    f'{label}: {role} token multiplicity')
            windows.append(window)
        collision = data.find(original_storage) if label != 'L0' else -1
        if label != 'L0':
            require(collision >= 0 and data.find(original_storage, collision+1) == -1
                    and collision != found['endpoints']['storage']['main_offset']+1,
                    f'{label}: historical storage-token collision')
        if previous_windows is not None:
            pair = (rows[-1]['label'], label)
            counts = [sum(a != b for a, b in zip(old, new, strict=True))
                      for old, new in zip(previous_windows, windows, strict=True)]
            require(counts == [int(comparisons[pair][f'{role}_unequal_positions_in_512'])
                               for role in ROLES], f'{pair}: window comparison')
            differences.append(dict(pair=pair, unequal_positions=dict(zip(ROLES, counts))))
        previous_windows = windows
        require(pin(path) == source, f'{label}: source changed')
        rows.append(dict(label=label, source_sha256=source[1], decoded_sha256=expected['decoded_sha256'],
                         historical_storage_token_collision=collision if collision >= 0 else None,
                         **{key: envelope[key] for key in (
                             'payload_offset', 'payload_length', 'discriminator',
                             'original_literal_offsets', 'substituted_literal_offsets', 'endpoint_pair_offsets')}))
    require(payloads[2] == payloads[3] and payloads[4] == payloads[5],
            'Same-session payload equality')
    return dict(rows=rows, window_differences=differences,
                same_session_payload_equal=[['L1', 'L1C'], ['L2', 'L2C']])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for label in LABELS:
        parser.add_argument(f'--{label.lower()}', type=Path, required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    require(sys.flags.isolated and sys.dont_write_bytecode, 'Use Python -I -B')
    paths = [getattr(args, label.lower()).resolve(strict=True) for label in LABELS]
    require(len(set(paths)) == len(LABELS), 'Duplicate input paths')
    disk_guard(args.receipt.parent)
    with args.receipt.open('x', encoding='utf-8', newline='\n') as stream:
        try:
            result = verify(paths, args.receipt.parent)
        except Exception as error:
            json.dump(dict(error=str(error)), stream)
            raise
        json.dump(result, stream, indent=2)
        stream.write('\n')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError) as error:
        print(f'Output-link verification failed ({type(error).__name__})', file=sys.stderr)
        raise SystemExit(1) from None
