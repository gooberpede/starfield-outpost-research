# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline verification of two exact selected saved-state witnesses."""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'research/p1-power'))

from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from outpost_record_framing import Reader
from saved_instances import extra_view
from stream_save import FREE, decoded_save, header
from validate_mature_outposts import directory
from workshop_inventory import linked_prefix
from workshop_population import initial_prefix, typed_records

# Source and decoded pins from D5BF, Save29 authority and SD1 component receipt.
PINS = {
    'save29': (2085680, 'ab28c98940b019320cda4d6a0db54c9d88b721a18fba4c6a701fbed0966b42fe',
               5539576, 'b236f22dd601b2dab59d5640967b12ab1f4dd5b3e4aac58cfae593bf43989579'),
    'hist-0021': (17016320, '8ad36c6bfa6035c66f0a1c62d64a704496d2ae01f7d1fac567ea979a4f7404ec',
                  40291019, '9bf6c3c4068adbfd274cf4b194891151ec732377ad79bce081689ef449d66887'),
}

POWER = {
    'ff022778': ('2c60e9', (1298916, 1299344), (1299159, 1299173), (1299043, 1299048),
                 ['ff022841', 'ff022917', 'ff02294d'], 0x840),
    'ff022841': ('2031e1', (1300005, 1300509), (1300178, 1300184), (1300167, 1300172),
                 ['ff022778'], 0x840),
    'ff022917': ('05ef19', (1300577, 1301023), (1300678, 1300684), (1300659, 1300664),
                 ['ff022778'], 0x840),
    'ff02294d': ('05ef19', (1301249, 1301671), (1301343, 1301349), (1301324, 1301329),
                 ['ff022778'], 0x800),
}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def pin(path):
    with path.open('rb') as stream:
        return path.stat().st_size, hashlib.file_digest(stream, 'sha256').hexdigest()


def disk_guard(scratch, reserve=0):
    """Use the caller-available counter, including on a quota-limited volume."""
    api = ctypes.WinDLL('kernel32', use_last_error=True).GetDiskFreeSpaceExW
    api.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_ulonglong),
                    ctypes.c_void_p, ctypes.c_void_p]
    api.restype = ctypes.c_int
    free = {}
    for drive in sorted({'C:/', 'D:/', Path(scratch).resolve().anchor.replace('\\', '/')}):
        value = ctypes.c_ulonglong()
        if not api(drive, ctypes.byref(value), None, None):
            raise ctypes.WinError(ctypes.get_last_error())
        require(value.value >= FREE + reserve, 'CALLER_AVAILABLE_DISK_FLOOR')
        free[drive] = value.value
    return free


def context(data):
    require(data[16:21] == b'\x1b\0\0\0\x99', 'UNSUPPORTED_FORMAT_OR_BUFFER')
    plugins = plugin_tables(data)
    d = directory(data)
    forms = struct.unpack_from(f'<{d["reference_count"]}I', data, d['regions']['reference_u32'][0]+4)

    def resolve(token):
        return saved_form(token_value(token, forms), plugins)

    return resolve, d['words'][9]


def select(data, resolve, ids):
    selected = {}
    for record in typed_records(data):
        if int(record['token'], 16) >> 22 != 2:
            continue
        identity = resolve(record['token'])
        if identity not in ids:
            continue
        require(identity not in selected, 'DUPLICATE_SELECTED_RECORD')
        require(record['form_type'] == 0x4a and record['buffer_version'] == 153,
                'UNSUPPORTED_SELECTED_RECORD_TYPE_OR_BUFFER')
        prefix = initial_prefix(data, record)
        require(prefix['case'] == 5, 'UNSUPPORTED_SELECTED_PREFIX')
        selected[identity] = record, prefix
    require(selected.keys() == ids, 'MISSING_SELECTED_RECORD')
    return selected


def unique(rows, tag):
    result = [row for row in rows if row['type'] == tag]
    require(len(result) == 1, 'MISSING_OR_DUPLICATE_EXTRA_' + tag)
    return result[0]


def span(row):
    return row['offset'], row['end']


def predict(consumers):
    """Ordinary one-generator branch, with the attributed 6 and 5 base values."""
    total = 0
    eligible = []
    for consumer in consumers:
        total += 5
        if total <= 6:
            eligible.append(consumer)
    return eligible


def power(data, resolve, count):
    require(count == 20825, 'SAVE29_R3_COUNT')
    selected = select(data, resolve, {'DYNAMIC:' + key for key in POWER})
    rows = []
    for form, (base, record_span, cb_span, flags_span, targets, word) in POWER.items():
        identity = 'DYNAMIC:' + form
        record, prefix = selected[identity]
        view = extra_view(data, record, prefix, resolve, workshop_resources=True)
        require(view['status'] == 'COUNT_CLOSED', 'POWER_EXTRA_UNSUPPORTED')
        independent = linked_prefix(data, record, prefix)
        require(independent['following_extras'] == 'CLOSED' and
                (independent['end'], independent['next_reference_index']) ==
                (view['body_end'], view['next_reference_index']), 'POWER_EXTRA_CURSOR_DISAGREEMENT')
        cb = unique(view['extras'], 'cb')
        flags = unique(view['extras'], '9c')
        require(span(record) == record_span and span(cb) == cb_span and span(flags) == flags_span,
                'POWER_OFFSET_MISMATCH')
        require(resolve(prefix['base_token']) == 'starfield.esm:' + base, 'POWER_BASE_MISMATCH')
        require(cb['references'] == ['DYNAMIC:' + x for x in targets], 'POWER_TARGET_ORDER')
        require(cb['words'] == [1] * len(targets) and flags['flags'] == word, 'POWER_WORD_MISMATCH')
        rows.append(dict(form_id=form, token=record['token'], base_form_id=base, record=record_span,
                         cb=cb_span, targets=targets, words=cb['words'], extra9c=flags_span,
                         extra9c_word=word, counted_end=view['body_end'],
                         extra_types=[row['type'] for row in view['extras']],
                         reference_cursor=view['next_reference_index'], reference_count=view['queue_count']))
    legacy = extra_view(data, *selected['DYNAMIC:ff022778'], resolve)
    require(legacy['status'] == 'UNSUPPORTED_EXTRA' and legacy['extras'][-1]['type'] == 'bc',
            'SAVE29_LEGACY_CONTROL')
    consumers = rows[0]['targets'][1:]
    return dict(rows=rows, legacy_refusal='bc', supply=6, demand_each=5,
                eligible=predict(consumers), eligible_swapped=predict(reversed(consumers)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('witness', choices=PINS)
    parser.add_argument('--save', type=Path, required=True)
    parser.add_argument('--output-directory', type=Path, required=True)
    args = parser.parse_args()
    require(sys.flags.isolated and sys.dont_write_bytecode and __debug__, 'USE_PYTHON_I_B')
    size, digest, decoded_size, decoded_digest = PINS[args.witness]
    source = args.save.resolve(strict=True)
    output = args.output_directory.resolve()
    disk_guard(output.parent, decoded_size + 131072)
    output.mkdir(exist_ok=False)
    try:
        require(source.stat().st_size == size and pin(source) == (size, digest), 'SOURCE_IDENTITY')
        with source.open('rb') as stream:
            require(header(stream)['declared_decoded_size'] == decoded_size, 'DECODED_SIZE')
        with decoded_save(source, output, scratch_budget=decoded_size, guard=disk_guard) as (data, metrics):
            require(metrics['decoded_sha256'] == decoded_digest, 'DECODED_IDENTITY')
            resolve, count = context(data)
            if args.witness == 'save29':
                result = power(data, resolve, count)
            else:
                from d5bt_display import display
                result = display(data, resolve)
        require(pin(source) == (size, digest), 'SOURCE_CHANGED')
        disk_guard(output, 65536)
        with (output / 'result.json').open('x', encoding='utf-8', newline='\n') as stream:
            json.dump(dict(schema='d5bt-selected/1', witness=args.witness, source_sha256=digest,
                           decoded_sha256=decoded_digest, build='1.16.244.0',
                           save_format=27, buffer_version=153, offset_domain='decoded logical stream',
                           record_count=count, result=result), stream, indent=2)
            stream.write('\n')
    except Exception as error:
        with (output / 'failure.txt').open('x', encoding='utf-8') as stream:
            stream.write(f'{type(error).__name__}: {error}\n')
        raise
    print(f'{args.witness}: selected saved-state checks passed')


if __name__ == '__main__':
    main()
