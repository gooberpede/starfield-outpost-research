"""SPDX-License-Identifier: GPL-3.0-or-later
Repeatable offline comparison ledger. Reads frozen EXP0021 cases and optionally
existing Phase1 raw captures/fresh extraction receipt. Writes NEW ignored output
only after caller-available 40GB C:/D: checks. No game/process/database/native
execution, network, dependencies, save modification or expected-value retuning.
"""
import argparse
import csv
import ctypes
import hashlib
import json
from pathlib import Path
import struct
import sys

from durable_position_model import center, vector, reconstruct
from durable_position_v2 import reproduce
from position_quantizer_diagnostic import diagnose

ROOT = Path(__file__).resolve().parents[2]


def guard():
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.GetDiskFreeSpaceExW.argtypes = [ctypes.c_wchar_p,
        ctypes.POINTER(ctypes.c_ulonglong), ctypes.c_void_p, ctypes.c_void_p]
    kernel.GetDiskFreeSpaceExW.restype = ctypes.c_int
    result = {}
    for drive in ('C:/', 'D:/'):
        available = ctypes.c_ulonglong()
        if not kernel.GetDiskFreeSpaceExW(drive, ctypes.byref(available), None, None):
            raise OSError(ctypes.get_last_error(), 'DISK_QUERY_FAILED')
        if available.value < 40_000_000_000:
            raise RuntimeError('DISK_FLOOR_STOP')
        result[drive] = available.value
    return result


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def table(path, rows):
    with path.open('x', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def verify(output, session=None, extraction=None):
    space = guard()
    if output.exists():
        raise FileExistsError(output)
    frozen_root = ROOT/'docs/experiments/engine-oracle'
    protected = [frozen_root/'inputs.json', frozen_root/'predictions.json',
                 ROOT/'save-analysis/scripts/durable_position_model.py']
    inputs = json.loads(protected[0].read_text())
    frozen = json.loads(protected[1].read_text())
    before = {str(p): digest(p) for p in protected}
    if len(inputs) != 23 or len(frozen) != 23:
        raise ValueError('FROZEN_CASE_COVERAGE')
    ledger = []
    for data, expected in zip(inputs, frozen):
        old = reconstruct(data)
        result = reproduce(data)
        cell = [result['native_cell']['tag'], *result['native_cell']['xy']]
        passed = (old == expected and result['center_hex'] == expected['center_hex']
                  and cell == expected['cell'] and result['residual'] == expected['residual'])
        ledger.append(dict(sample=data['source']['sample'], token=data['identity']['saved_reference'],
            workshop=data['identity']['workshop_id'], body=data['identity']['body'],
            frame=hex(data['frame']), center_hex=result['center_hex'], cell=json.dumps(cell),
            residual_hex=result['residual_hex'], result='PASS' if passed else 'FAIL',
            expectation='FROZEN_MODEL_REGRESSION_NOT_NATIVE_ORACLE'))
    extraction_rows, diagnostics = [], []
    if extraction:
        protected.append(extraction)
        before[str(extraction)] = digest(extraction)
        samples = json.loads(extraction.read_text())
        for data in inputs:
            label = 'HIST-0267' if data['source']['sample'] == 'Save52' else data['source']['sample']
            sample = next(s for s in samples if s['label'] == label)
            matches = [r for r in sample['rows'] if r['role'] == 'beacon' and
                       r['workshop']['identifier98_hex'] == data['identity']['workshop_id']]
            if len(matches) != 1:
                raise ValueError('FRESH_EXTRACTION_IDENTITY_NOT_UNIQUE')
            row = matches[0]
            passed = (sample['metrics']['decoded_sha256'] == data['source']['decoded_sha256']
                and row['record']['offset'] == data['source']['record_offset']
                and row['xyz_hex'] == data['position_hex']
                and row['workshop']['delta_hex'] == data['compensation_hex']
                and row['initial_frame_flag'] == data['frame'])
            extraction_rows.append(dict(sample=data['source']['sample'],
                workshop=data['identity']['workshop_id'], result='PASS' if passed else 'FAIL',
                expectation='FRESH_ARCHIVE_BYTE_REDECODE_NOT_NATIVE_OUTPUT'))
            for point in row['association']['points']:
                diagnostic = diagnose(*point['pair'])
                for mode, candidate in diagnostic['dispatch_candidates'].items():
                    diagnostics.append(dict(sample=data['source']['sample'],
                        workshop=data['identity']['workshop_id'], mode=mode,
                        cell=json.dumps(candidate['cell']),
                        previous_derived_site=json.dumps(data['site_cell']),
                        derived_cell_equal=candidate['cell'] == data['site_cell'],
                        expectation='DERIVED_SITE_COMPATIBILITY_NOT_NATIVE_ORACLE'))
    native, loaded, origins = [], [], []
    raw_count = 0
    if session:
        sys.path.insert(0, str(ROOT/'runtime/beacon-observer'))
        from inspect_capture import inspect
        labels = list(csv.DictReader((frozen_root/'Phase1-checkpoints.csv').open()))
        for row in labels:
            guard()
            capture = session/row['label']
            inspected = inspect(capture)  # verifies every referenced byte section
            journal = capture/'records.jsonl'
            protected.append(journal)
            before[str(journal)] = digest(journal)
            records = [json.loads(line) for line in journal.read_text().splitlines()]
            raw = {r['root']: r for r in records if r.get('kind') == 'raw'}
            for r in raw.values():
                p = capture/r['file']
                protected.append(p)
                before[str(p)] = r['sha256']
            raw_count += inspected['raw_sections']
            if inspected['journal_truncated_final_line']:
                raise ValueError('TRUNCATED_CAPTURE')
            value = inspected['native_workshop_output']
            observed = value['before']['center_float32_hex']
            expected = next(i for i in inputs if i['source']['sample'] == 'Save'+row['save']
                and i['identity']['workshop_id'] == ('0efca066ee4c7b9b' if row['site'] == '003' else 'f1517de43e171745'))
            predicted_result = reproduce(expected)
            predicted = predicted_result['center_hex']
            terrain = inspected['terrain']
            selected = terrain['origins'][terrain['selected_origin_offset']]
            native_origin = [selected['tag']] + [192*c+12*s+f for c,s,f in zip(
                selected['coarse_xy'], selected['sub_xy'], selected['fine_xy'])]
            origin_equal = (native_origin == predicted_result['source_origin']['native']
                and terrain['body_candidate_formid'] == expected['identity']['body']
                and inspected['grid']['resolution'] == 256
                and inspected['grid']['block_plus_merge'] == 12)
            origins.append(dict(label=row['label'], mode=terrain['mode'],
                member=terrain['selected_origin_offset'], native_origin=json.dumps(native_origin),
                descriptor_origin=json.dumps(predicted_result['source_origin']['native']),
                body=terrain['body_candidate_formid'], result='PASS' if origin_equal else 'FAIL',
                expectation='ARCHIVED_SELECTED_TERRAIN_ORIGIN_NOT_WORKSHOP_POST_GRID'))
            native.append(dict(label=row['label'], observed_hex=observed, predicted_hex=predicted,
                exact_equal=observed == predicted,
                archived_table_equal=observed == row['native_center_le'],
                brackets_equal=value['equal_bracket_values'],
                classification=row['qualification'], native_grid='NOT_OBSERVED',
                qualified_fresh_oracle=False))
            for ref in inspected['references']:
                root = ref['root']
                if root+'.extra.workshop' not in raw:
                    continue
                wr = raw[root+'.extra.workshop']
                blob = (capture/wr['file']).read_bytes()
                workshop = blob[0x98:0xa0].hex()
                matching = [i for i in inputs if i['source']['sample'] == 'Save'+row['save']
                            and i['identity']['workshop_id'] == workshop]
                if len(matching) != 1:
                    raise ValueError('LOADED_WORKSHOP_JOIN')
                data = matching[0]
                phex, dhex = ref['xyz_float32_hex'], blob[0x60:0x6c].hex()
                computed, _ = center(vector(phex), vector(dhex))
                center_hex = struct.pack('<3f', *computed).hex()
                passed = (phex == data['position_hex'] and dhex == data['compensation_hex']
                          and center_hex == reproduce(data)['center_hex'])
                loaded.append(dict(label=row['label'], workshop=workshop,
                    position_hex=phex, compensation_hex=dhex, center_hex=center_hex,
                    result='PASS' if passed else 'FAIL',
                    expectation='INDEPENDENT_LOADED_INPUT_BITS_NOT_NATIVE_HELPER_EXECUTION'))
    after = {str(p): digest(p) for p in protected}
    if before != after:
        raise ValueError('INPUT_INTEGRITY_CHANGED')
    output.mkdir(parents=True)
    table(output/'regressions.csv', ledger)
    if extraction_rows:
        table(output/'archive-comparison.csv', extraction_rows)
        table(output/'angular-diagnostic.csv', diagnostics)
    if native:
        table(output/'native-comparison.csv', native)
        table(output/'loaded-input-comparison.csv', loaded)
        table(output/'origin-comparison.csv', origins)
    passed = all(r['result'] == 'PASS' for r in ledger+extraction_rows+loaded+origins)
    passed &= all(r['archived_table_equal'] and r['brackets_equal'] for r in native)
    receipt = dict(implementation_checks='PASS' if passed else 'FAIL', frozen_cases=len(ledger),
        archive_cases=len(extraction_rows), loaded_input_cases=len(loaded),
        native_checkpoints=len(native), source_origin_comparisons=len(origins), verified_raw_sections=raw_count,
        native_equal=sum(r['exact_equal'] for r in native),
        fresh_qualified_native_oracles=0, native_grid_outputs=0, blind_native_holdouts=0,
        native_equivalence='NOT TESTED', before=before, after=after, disk=space,
        python=sys.version, argv=sys.argv)
    (output/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf8', newline='\n')
    if not passed:
        raise ValueError('COMPARISON_FAILURE_SEE_LEDGER')
    return {k: v for k, v in receipt.items() if k not in ('before', 'after')}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--session', type=Path)
    parser.add_argument('--extraction', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.output, args.session, args.extraction), indent=2))


if __name__ == '__main__':
    main()
