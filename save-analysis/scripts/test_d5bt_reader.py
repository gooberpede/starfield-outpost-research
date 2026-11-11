# SPDX-License-Identifier: GPL-3.0-or-later
"""D5BT controls. Optional exact staged originals are read-only, with RAM mutations."""
import argparse
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from d5bt_reader import PINS, context, disk_guard, extra_view, pin, power, require, select
from d5bt_display import display, extras, sections, slot
from stream_save import decoded_save
from validate_mature_outposts import directory
from workshop_components import component_sections
from workshop_inventory import linked_prefix


def rejects(label, expected, operation):
    try:
        operation()
    except ValueError as error:
        require(expected in str(error), f'{label}: unexpected refusal: {error}')
        print(f'PASS {label}: {error}')
        return
    raise AssertionError(f'{label}: unexpectedly accepted')


def extra_fixture(body, refs, strings=()):
    return dict(flags=0x40, end=len(body), refs=list(refs), strings=list(strings))


def synthetic():
    prefix = dict(form_prefix_end=0, next_reference_index=0)
    # Count 3. 4C zero entries, BC zero resource groups and object list,
    # one BC flag + string queue + 24-byte tail, then one CB word.
    valid = b'\x0c\x4c\x00\xbc' + bytes(30) + b'\xcb\x04\x01\0\0\0'
    record = extra_fixture(valid, ['822778'], [0])
    checked = extra_view(valid, record, prefix, str, workshop_resources=True)
    alternate = linked_prefix(valid, record, prefix)
    require((checked['body_end'], checked['next_reference_index']) ==
            (40, 1) == (alternate['end'], alternate['next_reference_index']), 'SYNTHETIC_CURSOR')
    require(extra_view(valid, record, prefix, str)['extras'][-1]['type'] == 'bc', 'SYNTHETIC_LEGACY')
    print('PASS synthetic BC then CB, distinct cursors and legacy gap')
    for label, body, refs, strings, expected in (
        ('truncated BC', valid[:30], ['822778'], [0], 'boundary'),
        ('invalid BC group count', valid[:4] + b'\xff'*4 + valid[8:], ['822778'], [0], 'GROUP_BOUNDS'),
        ('missing BC string', valid, ['822778'], [], 'STRING_QUEUE_BOUNDS'),
        ('truncated CB word', valid[:-1], ['822778'], [0], 'boundary'),
        ('missing CB reference', valid, [], [0], 'QUEUE_BOUNDS'),
        ('invalid extra count', bytes([3]) + valid[1:], ['822778'], [0], 'count tag'),
    ):
        record = extra_fixture(body, refs, strings)
        for name, check in (
            ('view', lambda: extra_view(body, record, prefix, str, workshop_resources=True)),
            ('linked', lambda: linked_prefix(body, record, prefix)),
        ):
            rejects(f'{label} ({name})', expected, check)

    rejects('unsupported header format', 'UNSUPPORTED_FORMAT', lambda: context(bytes(30)))
    rejects('wrong display slot token', 'DISPLAY_SLOT',
            lambda: slot(dict(offset=0, id_word=1, index=0, flag=1, groups=[[2]]), 0, '1', '3'))
    body = b'\x04\xeb'
    rejects('unsupported display EB', 'DISPLAY_EXTRA_UNSUPPORTED',
            lambda: extras(body, extra_fixture(body, []), prefix, str))
    body = b'\x04\x96\x01'
    rejects('unsupported display 96 flags', 'UNQUALIFIED_96_FLAGS',
            lambda: extras(body, extra_fixture(body, []), prefix, str))
    body = b'\x04\x33\x80'
    rejects('unsupported display 33 flags', 'UNQUALIFIED_33_FLAGS',
            lambda: extras(body, extra_fixture(body, []), prefix, str))
    rejects('truncated type6 tables', 'boundary',
            lambda: component_sections(bytes(4), 0, 4, buffer_version=153,
                                       activity_custom_payloads=True, pending_dialogue=True))


def mutate(data, offset, replacement, expected, operation, label):
    original = data[offset:offset+len(replacement)]
    require(original != replacement, 'INEFFECTIVE_CONTROL_MUTATION')
    data[offset:offset+len(replacement)] = replacement
    try:
        rejects(label, expected, lambda: operation(data))
    finally:
        data[offset:offset+len(replacement)] = original


def original_controls(save, witness, scratch):
    size, digest, decoded_size, decoded_digest = PINS[witness]
    require(pin(save) == (size, digest), 'CONTROL_SOURCE_IDENTITY')
    with decoded_save(save, scratch, scratch_budget=decoded_size, guard=disk_guard) as (mapped, info):
        require(info['decoded_sha256'] == decoded_digest, 'CONTROL_DECODED_IDENTITY')
        data = bytearray(mapped)
    resolve, count = context(data)
    if witness == 'save29':
        record, _ = select(data, resolve, {'DYNAMIC:ff022778'})['DYNAMIC:ff022778']
        tokens = b'\x82\x29\x17\x82\x29\x4d'
        queue_end = record['string_start']
        require(data[queue_end-6:queue_end] == tokens, 'CONTROL_ORDER_LOCATION')
        def check(value):
            return power(value, resolve, count)
        mutate(data, queue_end-6, tokens[3:]+tokens[:3], 'POWER_TARGET_ORDER', check, 'swapped CB consumers')
        mutate(data, 1299161, struct.pack('<I', 2), 'POWER_WORD_MISMATCH', check, 'changed CB word')
        mutate(data, 1301325, struct.pack('<I', 0x840), 'POWER_WORD_MISMATCH', check, 'changed 9C word')
        def invalid_resolve(token):
            return resolve('c00000' if token == '822778' else token)
        rejects('invalid selected resolution', 'UNSUPPORTED_REFERENCE_TAG',
                lambda: power(data, invalid_resolve, count))
        # Independently locate the footer run for the selected record ordinal.
        d = directory(data)
        cursor = struct.unpack_from('<I', data, d['offset'] + 0x2c)[0]
        runs, cursor = compact(data, cursor)
        ordinal = record['ordinal']
        for _ in range(runs):
            index_offset = cursor
            length, cursor = compact(data, cursor + 1)
            if ordinal < length:
                break
            ordinal -= length
        require(data[index_offset] == 0, 'CONTROL_FOOTER_REFR_INDEX')
        mutate(data, index_offset, b'\x01', 'UNSUPPORTED_SELECTED_RECORD_TYPE_OR_BUFFER',
               check, 'wrong footer type')
    else:
        def check(value):
            return display(value, resolve)
        mutate(data, 1579800, struct.pack('<I', 0x85bb93), 'DISPLAY_SLOT', check, 'wrong Nested item')
        # Keep the extra list and queue well formed while resolving the backlink elsewhere.
        rec, _ = select(data, resolve, {'DYNAMIC:ff05bb92'})['DYNAMIC:ff05bb92']
        candidate_indices = [i for i, token in enumerate(rec['refs']) if token == '85bb90']
        require(len(candidate_indices) == 2, 'CONTROL_BACKLINK_QUEUE')
        mutate(data, rec['reference_start'] + 3*candidate_indices[0], bytes.fromhex('85bb91'),
               'DISPLAY_BACKLINK', check, 'wrong Extra36 target')
        mutate(data, 5861620, b'\x37\x04', 'MISSING_OR_DUPLICATE_EXTRA_36', check,
               'well-formed list missing Extra36')
        mutate(data, 5861620, b'\xeb', 'DISPLAY_EXTRA_UNSUPPORTED', check, 'unsupported item extra')
        # A zero-count Extra37 is accepted by the historical general parser.
        mutate(data, 5861608, b'\x37\0', 'DISPLAY_EXTRA_SEQUENCE', check,
               'well-formed extra outside the selected subset')
        rejects('legacy pending-dialogue refusal', 'PAYLOAD_UNQUALIFIED',
                lambda: component_sections(data, 1323741, 1603619, buffer_version=153,
                                           activity_custom_payloads=True))
        mutate(data, 1485413, struct.pack('<I', 6), 'boundary', sections,
               'malformed pending-dialogue count')
        mutate(data, 1579785, struct.pack('<I', 0xffffffff), 'boundary', check, 'malformed Nested count')
        mutate(data, 5861374, b'\x04', 'DISPLAY_INVENTORY_COUNT', check, 'nonzero fixture stock')
    require(pin(save) == (size, digest), 'CONTROL_SOURCE_CHANGED')


def compact(data, offset):
    width = (1, 2, 4)[data[offset] & 3]
    return int.from_bytes(data[offset:offset+width], 'little') >> 2, offset + width


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--save29', type=Path)
    parser.add_argument('--hist-0021', type=Path)
    parser.add_argument('--scratch', type=Path)
    args = parser.parse_args()
    require(sys.flags.isolated and sys.dont_write_bytecode and __debug__, 'USE_PYTHON_I_B')
    synthetic()
    if args.save29 or args.hist_0021:
        require(args.scratch is not None, 'EXPLICIT_CONTROL_SCRATCH_REQUIRED')
        disk_guard(args.scratch.parent, 41_000_000)
        args.scratch.mkdir(exist_ok=False)
        for witness, save in [('save29', args.save29), ('hist-0021', args.hist_0021)]:
            if save is not None:
                original_controls(save, witness, args.scratch)


if __name__ == '__main__':
    main()
