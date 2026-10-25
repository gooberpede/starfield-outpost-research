# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline adversarial native-adapter/reducer checks with invented memory bytes.

Reads project-owned Python modules, writes one exclusive ignored JSON receipt.
No native target execution, proprietary input, save, configuration or Git effects.
These fixtures qualify refusal rules, not retail layouts or runtime safety.
"""
import copy
import json
import struct
import argparse
from build import LOCAL
import native_reduce
from reduce import reduce as fixture_reduce


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    assert args.label and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in args.label)
    session = dict(kind='SESSION', synthetic=False, schema='sor-d5e/1', pid=123,
        module_base=0x140000000, image_sha256='7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28')
    source, manager = bytearray(0x70), bytearray(0x200)
    struct.pack_into('<I', source, 0, 0x29d20e)
    struct.pack_into('<Q', source, 0x68, 77)
    struct.pack_into('<I', manager, 0x80, 0x5e0de)
    struct.pack_into('<i', manager, 0xc8+4, 195)
    struct.pack_into('<i', manager, 0xc8+8, 109)
    struct.pack_into('<i', manager, 0xc8+0x14, 8)
    def field(raw):
        return dict(complete=True, address=0x10000, raw=bytes(raw).hex())
    row = dict(kind='SAMPLE', native=True, native_read_complete=True, frame_valid=True,
        capture=1, site=1, tid=1, thread_lifetime=1, provider_working_rsp=0x100000,
        rip=0x14079fcd0, decision_operand=8, source=field(source), source_again=field(source),
        manager=field(manager), manager_again=field(manager),
        manager_pointer=field(struct.pack('<Q', 0x20000)),
        manager_pointer_again=field(struct.pack('<Q', 0x20000)),
        original_query=field(struct.pack('<2i', 10, 20)),
        original_query_again=field(struct.pack('<2i', 10, 20)),
        capacity=field(struct.pack('<Q', 8)))
    barrier = dict(kind='ARM_BARRIER', readback=True, slots=4, all_threads=1)
    rows = [session, barrier, row]
    results = []
    def check(name, condition):
        results.append(dict(case=name, pass_=bool(condition)))
        assert condition, name
    output = native_reduce.reduce(rows)
    check('native_miss_C_only', output['tier']=='C' and output['observations'][0]['decision']=='MAP_MISS' and output['first_ever']=='UNKNOWN')
    check('native_session_and_coverage', output['session']==session and output['coverage'][0]['state']=='ARMED')
    check('no_session', native_reduce.reduce(rows[1:])['tier']=='D')
    for name, mutated in [('multiple_sessions', rows+[session]),
                          ('wrong_image', [dict(session, image_sha256='wrong'), barrier, row]),
                          ('synthetic_session', [dict(session, synthetic=True), barrier, row])]:
        try:
            native_reduce.reduce(mutated)
        except ValueError:
            check(name, True)
        else:
            check(name, False)
    for field_name in ('source', 'capacity', 'manager'):
        mutated = copy.deepcopy(rows)
        mutated[-1][field_name]['complete'] = False
        output = native_reduce.reduce(mutated)
        check('missing_'+field_name, output['tier']=='D' and output['rejected'][0]['reason']==field_name+':incomplete_read')
    mutated = copy.deepcopy(rows)
    mutated[-1]['original_query']['complete'] = False
    output = native_reduce.reduce(mutated)
    check('decision_with_missing_query_C', output['tier']=='C' and 'original_query:incomplete_read' in output['observations'][0]['missing'])
    mutated = copy.deepcopy(rows)
    mutated[-1]['capture'] = 2
    check('lost_native_sequence', native_reduce.reduce(mutated)['coverage'][-1]['reason']=='capture_sequence')
    mutated = copy.deepcopy(rows)
    mutated[-1].update(site=2, rip=0x14079b8ed, decision_operand=3, geographic_query=field(bytes(0x18)))
    check('unjoined_mask_is_D', native_reduce.reduce(mutated)['tier']=='D')
    mutated = copy.deepcopy(rows)
    mutated[-1]['rip'] += 1
    check('wrong_native_site', native_reduce.reduce(mutated)['rejected'][0]['reason']=='native_site_address')
    try:
        fixture_reduce(rows)
    except ValueError:
        check('native_cannot_use_fixture_epochs', True)
    else:
        check('native_cannot_use_fixture_epochs', False)
    with (LOCAL / (args.label + '.json')).open('x', encoding='utf8', newline='\n') as stream:
        json.dump(results, stream, indent=2)
        stream.write('\n')
    print(len(results), 'PASS; invented bytes only')


if __name__ == '__main__':
    main()
