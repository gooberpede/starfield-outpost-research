# SPDX-License-Identifier: GPL-3.0-or-later
"""Finite CR1 evidence checks, stdlib and project-owned readers only.

Reads ignored acquisition receipts, protected inputs and HEAD/index. Writes one
exclusive ignored JSON receipt. No game/VM/native execution, network, analysis
database change, original/save mutation or Git mutation. Run with installed
CPython -B from repository root. See README.md for prerequisites and limitations.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.local-work/cr1-crew'
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
sys.path.insert(0, str(WORK))
from inventory_historical_saves import guard
from crew_extras import extra_view


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(name):
    return json.loads((WORK / name).read_text(encoding='utf8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    assert args.run.isalnum()
    guard()
    checks = []

    def check(name, value):
        assert value, name
        checks.append(dict(name=name, result='PASS'))

    baseline = read('baseline.json')
    check('HEAD unchanged', subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip() == baseline['head'])
    check('index unchanged', sha(ROOT / '.git/index') == baseline['index']['sha256'])
    for pin in baseline['protected'] + [baseline['brief']]:
        check('protected ' + pin['path'], sha(pin['path']) == pin['sha256'])
    interface = read('interface01.json')
    check('interface archive unchanged', sha(interface['source']['path']) ==
          interface['source']['sha256'])
    for member in interface['members']:
        check('interface member ' + member['member'], sha(member['local']['path']) ==
              member['local']['sha256'])
    check('132 selected ESM physical rereads', read('definition-reread01.json')[
        'physical_rereads'] == 132)
    defs = {r['formid']: r for r in read('definitions02.json')['rows']}
    defaults = {r['edid']: dict(r['fields']) for r in read('defaults01.json')}
    for name, value in [('CrewAssignment_DO', 0x26beac),
                        ('SpaceshipCrewCommandSkillAV_DO', 0x160030),
                        ('SpaceshipCrewSlotCostAV_DO', 0x172f8f),
                        ('SpaceshipCrewSlotsAV_DO', 0x2cc9ea),
                        ('SpaceshipCrewReassignDisabledAV_DO', 0x172f8e)]:
        check('installed default ' + name,
              int.from_bytes(bytes.fromhex(defaults[name]['DATA']), 'little') == value)
    check('station build global initially three',
          struct.unpack('<f', bytes.fromhex(dict(defs[0x1b4bb2]['fields'])['FLTV']))[0] == 3)
    check('COBJ station product', dict(defs[0x2ab8f7]['fields'])['CNAM'] == '599f2900')
    check('COBJ station limit global', dict(defs[0x2ab8f7]['fields'])['JNAM'] == 'b24b1b00')
    for fid, magnitude in [(0x9b24, 1), (0x9b25, 2), (0x9b28, 3), (0x9b29, 5)]:
        fields = dict(defs[fid]['fields'])
        check('command ability ' + hex(fid), fields['EFID'] == '209b0000' and
              struct.unpack('<f', bytes.fromhex(fields['EFIT'])[:4])[0] == magnitude)
    quest = bytes.fromhex(dict(defs[0x2c59e4]['fields'])['VMAD'])
    check('installed quest property three overrides source default one',
          b'OutpostManagementBonus\x03\x01\x03\x00\x00\x00' in quest)
    player = next(r for r in read('definitions-extra01.json') if r['formid'] == 7)
    props = {i: value for key, value_hex in player['fields'] if key == 'PRPS'
             for i, value, tail in struct.iter_unpack('<IfI', bytes.fromhex(value_hex))}
    check('Player command baseline three', props[0x160030] == 3)
    pex = read('pex06.json')
    check('24 selected PEX close without errors', len(pex['members']) == 24 and
          not pex['errors'])

    def method(member, name):
        return next(fn for obj in pex['members'][member]['decoded']['objects']
                    for state, functions in obj['states'] for method_name, fn in functions
                    if method_name.lower() == name.lower())

    def calls(member, name):
        return [(op['offset'], op['args'][0][1]) for op in method(member, name)['ops']
                if op['op'] == 23]

    crew = 'Scripts/SQ_CrewScript.pex'
    cleanup = calls(crew, 'TestAndHandleUnloadedUnassignedGenericCrew')
    names = [name for offset, name in cleanup]
    check('generic cleanup tests keyword and current assignment',
          'HasKeyword' in names and 'GetCrewAssignment' in names)
    check('generic cleanup clears role before disabling/deleting',
          names.index('SetRoleUnavailable') < names.index('DisableNoWait') < names.index('Delete'))
    removal = method(crew, 'CheckCrewCountAtOutpost')
    check('removal reads slots and unassigns',
          {'GetValueInt', 'GetCrewAssignedToOutpost', 'UnassignCrew'}.issubset(
              {name for offset, name in calls(crew, 'CheckCrewCountAtOutpost')}))
    check('removal opcode44 consumes just array operand',
          any(op['op'] == 44 and op['args'] == [[1, 'assignedCrew']] for op in removal['ops']))
    check('removal locks/unlocks', {48, 49}.issubset({op['op'] for op in removal['ops']}))
    check('assignment has loaded and movement branches',
          {'Is3DLoaded', 'MoveTo', 'SetLinkedRef'}.issubset(
              {name for offset, name in calls(crew, 'HandleOnCrewAssigned')}))
    check('dismissal rereads current assignment', any(name == 'GetCrewAssignment'
          for offset, name in calls(crew, 'HandleOnCrewDismissed')))
    menu = read('menu01.json')
    check('86 selected ABC bodies fully decoded', len(menu['methods']) == 86 and
          all(r['decoded_bytes'] == r['code_bytes'] and
              not any(op[1] == 'UNKNOWN_STOP' for op in r['instructions'])
              for r in menu['methods']))
    methods = {r['method']: r for r in menu['methods']}
    check('installed movie subscription', 'ShipCrewData' in str(methods[1003]['instructions'])
          and 'Subscribe' in str(methods[1003]['instructions']))
    check('installed list population', 'CrewInfoA' in str(methods[1007]['instructions'])
          and 'InitializeEntries' in str(methods[1007]['instructions']))
    check('installed category filter', 'uAssignmentType' in str(methods[1008]['instructions']))
    check('installed sort dispatch', 'ShipCrewMenu_SetSort' in str(methods[1017]['instructions']))
    joins = read('save-joins01.json')
    check('17 unique exact station roots', len(joins['roots']) == 17 and
          len({r['root'] for r in joins['roots']}) == 17)
    check('exact first station/owner/mode-byte offset', any(
        r['root'] == 'DYNAMIC:ff01fa66' and r['owner'] == 'DYNAMIC:ff01a75b' and
        r['owner_link_offset'] == 3164683 for r in joins['roots']))
    check('54 closed beacons with zero sampled E2', sum(r['beacons'] for r in joins['summary']) ==
          54 and all(r['e2_lists'] == 0 for r in joins['summary']))
    check('sampled beacon saved base slots two', all(
        v['value'] == 2 for row in joins['summary'] for slot in row['saved_slots']
        for v in slot['values']))
    for sample in ['Save52', 'HIST-0036', 'HIST-0077']:
        result = read(sample + '-crew03.json')
        check(sample + ' actor grammar exclusions retained', any(
            r.get('status') == 'ACTOR_OR_NPC_GRAMMAR_UNQUALIFIED' for r in result['rows']))
        check(sample + ' source unchanged', sha(result['source']['path']) ==
              result['source']['sha256'])
    # Synthetic E2 wire/control cases exercise queue bounds, not live semantics.
    prefix = dict(form_prefix_end=0, next_reference_index=0)
    record = dict(flags=0x40, end=3, refs=['actorA', 'actorB'])
    result = extra_view(b'\x04\xe2\x08', record, prefix, lambda token: token)
    check('E2 positive wire fixture', result['status'] == 'COUNT_CLOSED' and
          result['extras'][0]['members'] == ['actorA', 'actorB'])
    record['refs'] = ['actorA']
    try:
        extra_view(b'\x04\xe2\x08', record, prefix, lambda token: token)
    except ValueError as error:
        check('E2 short queue rejected', str(error) == 'EXTRA_QUEUE_BOUNDS')
    else:
        raise AssertionError('E2 short queue accepted')
    for number in range(1, 21):
        check('native job completed ' + str(number),
              (WORK / 'native' / f'{number:03}.request.done').exists())
    guard()
    output = dict(result='PASS', checks=checks, count=len(checks),
                  python=sys.version, tool_sha256=sha(__file__),
                  limits='Evidence/framing and selected path checks; no game, VM, runtime, '
                         'historical crew semantics or whole-source equivalence oracle')
    with (WORK / (args.run + '.json')).open('x', encoding='utf8', newline='\n') as stream:
        json.dump(output, stream, indent=2)
        stream.write('\n')
    print('PASS', len(checks), 'finite CR1 checks')


if __name__ == '__main__':
    main()
