# SPDX-License-Identifier: GPL-3.0-or-later
"""Finite offline CR2 evidence verification; installed CPython, repository cwd.

Reads protected pins, local receipts, authored tables and actual ESM headers/
fields. Exercises the pure saved-tail reader using existing original-derived
records and adversarial mutations of temporary in-memory copies. Writes one
exclusive ignored JSON (--run NAME). Stdlib/owned readers only; no game, save,
database, Git/index, dependency or network changes. Checks integrity/framing and
specific definition facts, not runtime effect realization or exhaustive semantics.
"""
from pathlib import Path
import argparse
import copy
import csv
import hashlib
import json
import struct
import subprocess
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.local-work/cr2-skills'
sys.path[:0] = [str(Path(__file__).parent), str(ROOT / 'save-analysis/scripts')]
from definitions import pin
from saved import perk_tail
from catalogue import entries
from inspect_outpost_definitions import subrecords
from inventory_historical_saves import guard


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    assert args.run.isalnum()
    guard()
    checks = []

    def check(label, value):
        assert value, label
        checks.append(label)

    baseline = json.loads((WORK / 'baseline.json').read_text())
    for source in baseline['protected'] + [baseline['brief'], baseline['index']]:
        check('protected ' + source['path'], pin(Path(source['path'])) == source)
    check('HEAD unchanged', subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip() == baseline['head'])
    defs = json.loads((WORK / 'definitions01.json').read_text())
    records = defs['records']
    by = {r['formid']: r for r in records}
    check('all 502 main PERKs framed', sum(r['type'] == 'PERK' for r in records) == 502)
    catalogue = list(csv.DictReader((ROOT / 'docs/experiments/crew-skills/catalogue.csv').open(encoding='utf8')))
    pop = list(csv.DictReader((ROOT / 'docs/experiments/crew-skills/population.csv').open(encoding='utf8')))
    check('56 candidates plus five robots preserved', len(pop) == 61)
    check('14 generic specialist archetypes', sum(r['qualification'] == 'GENERIC_ARCHETYPE' for r in pop) == 14)
    check('five constructible robot archetypes', sum(r['qualification'] == 'CONSTRUCTIBLE_ROBOT_ACTOR' for r in pop) == 5)
    inheritance = list(csv.DictReader((ROOT / 'docs/experiments/crew-skills/inheritance.csv').open(encoding='utf8')))
    human_ids = {r['base_formid'] for r in pop if r['qualification'] in ('NAMED_RECRUIT_CONDITIONAL_STORY', 'GENERIC_ARCHETYPE')}
    check('42 human spell/perk inheritance flags clear', len(human_ids) == 42 and all(r['spell_perk_inherit_flag3'] == 'False' for r in inheritance if r['base_formid'] in human_ids))
    check('ModelA03 actual outpost Fusion rank1', dict(by[0x1d924e]['fields'])['PRKR'] == '4fd2200001')
    check('non-UI helper retained separately', next(r for r in catalogue if r['perk_formid'] == '0006b728')['crew_ui_flag'] == 'False')
    # Independent physical field rereads, including repeated/condition-group tags.
    reread = [by[int(r['perk_formid'], 16)] for r in catalogue]
    reread += [by[int(r['base_formid'], 16)] for r in pop]
    with Path(defs['source']['path']).open('rb') as stream:
        for r in reread:
            stream.seek(r['offset'])
            header = stream.read(24)
            size, flags, fid = struct.unpack_from('<III', header, 4)
            check('ESM identity ' + hex(fid), fid == r['formid'] and header[:4].decode() == r['type'])
            body = stream.read(size)
            if flags & 0x40000:
                expected = int.from_bytes(body[:4], 'little')
                body = zlib.decompress(body[4:])
                check('ESM decompressed size ' + hex(fid), len(body) == expected)
            check('ESM all ordered fields ' + hex(fid), [(k.decode(), v.hex()) for k, v in subrecords(body)] == [tuple(v) for v in r['fields']])
    fusion = entries(by[0x20d24f])
    check('outpost Fusion three rank1 entries', [e['rank'] for e in fusion] == [1, 1, 1])
    check('outpost Fusion DB add payloads', [e['data'] for e in fusion] == ['db0202'] * 3 and [e['payload_float'] for e in fusion] == [1, 2, 3])
    check('outpost Fusion group1 conditions retained', all(c['group'] == 1 for e in fusion for c in e['conditions']))
    check('crew Geology has no PRKE', entries(by[0x21b8cc]) == [])
    check('ship Fusion type1 identity', entries(by[0x222f83])[0]['data'] == 'b68b1900')
    check('Payloads four rank entries all multiply', all(e['data'] == 'aa0302' for e in entries(by[0x222f84])) and len(entries(by[0x222f84])) == 4)
    check('normal Engineering only manufactured keyword', {c['parameter'] for e in entries(by[0x21b8c8]) for c in e['conditions']} == {0x23ceb6})
    grants = json.loads((WORK / 'grants-pex01.json').read_text())
    check('ten fully closed compiled grant members', len(grants['members']) == 10 and all(o['end'] == o['declared_end'] for v in grants['members'].values() for o in v['decoded']['objects']))
    check('40 actual compiled AddPerk calls', len(grants['grants']) == 40)
    check('outpost Fusion not granted in selected compiled bodies', all(g['perk'] != '0020d24f' for g in grants['grants']))
    focused = json.loads((WORK / 'focused01.json').read_text())['records']
    robot_recipes = json.loads((WORK / 'robot-recipes01.json').read_text())
    check('five actual robot recipe products', {int.from_bytes(bytes.fromhex(dict(r['fields'])['CNAM']), 'little') for r in robot_recipes} == {0x4297c, 0xbd67e, 0x1f416e, 0x1d9250, 0x1d924e})
    check('fresh compiled-grant replay byte exact', (WORK / 'grants-pex01.json').read_bytes() == (WORK / 'grants-pex-replay01.json').read_bytes())
    for label in ['HIST-0255', 'HIST-0021', 'HIST-0022', 'HIST-0024', 'HIST-0036', 'HIST-0077', 'Save52']:
        receipt = json.loads((WORK / (label + '-ranks01.json')).read_text())
        check('selected original unchanged ' + label, pin(Path(receipt['source']['path'])) == receipt['source'])
    pad = next(r for r in focused if r['formid'] == 0x219523)
    keywords = {v[0] for v in struct.iter_unpack('<I', bytes.fromhex(dict(pad['fields'])['KWDA']))}
    check('fuel marker excludes all five resource families', not keywords & {0x299548, 0x299549, 0x29954a, 0x2c5a95, 0x23ceb6})
    # Existing independently framed, original-derived Actor records.
    witness = json.loads((ROOT / '.local-work/cr1-current/HIST-0255-witness06.json').read_text())
    perk_ids = {f'starfield.esm:{r["formid"]:06x}' for r in records if r['type'] == 'PERK'}
    for identity, wanted in [('starfield.esm:005639', [('starfield.esm:21b8e3', 1), ('starfield.esm:21b8c3', 3)]),
                             ('starfield.esm:00563c', [('starfield.esm:21b8cc', 1), ('starfield.esm:21b8c8', 3)])]:
        row = next(r for r in witness['rows'] if r['identity'] == identity)
        data = bytes.fromhex(row['body_hex'])
        record = copy.deepcopy(row['record'])
        base = record['body']
        record.update(body=0, end=record['end'] - base)
        prefix = copy.deepcopy(row['prefix'])
        prefix['form_prefix_end'] -= base
        mapping = dict(zip(row['record']['refs'], row['queue']))
        resolve = mapping.__getitem__
        actual = perk_tail(data, record, prefix, resolve, perk_ids)
        check('independent actor rank bytes ' + identity, [(e['perk'], e['rank']) for e in actual['ranked']] == wanted)
        variants = []
        r = copy.deepcopy(record); r['form_type'] = 0x40; variants.append(('wrong type', data, r, prefix, perk_ids))
        r = copy.deepcopy(record); r['buffer_version'] = 152; variants.append(('wrong version', data, r, prefix, perk_ids))
        r = copy.deepcopy(record); r['end'] -= 1; variants.append(('truncated record', data[:-1], r, prefix, perk_ids))
        p = copy.deepcopy(prefix); p['actor_header']['mask'] &= ~(1 << 22); variants.append(('missing owned-rank bit', data, record, p, perk_ids))
        p = copy.deepcopy(prefix); p['actor_header']['mask'] |= 1 << 24; variants.append(('unsupported suffix', data, record, p, perk_ids))
        b = bytearray(data); b[actual['suffix_start'] + 24] = 2; variants.append(('unsupported clock', b, record, prefix, perk_ids))
        b = bytearray(data); b[actual['rank_offsets'][0]] = 0; variants.append(('zero saved rank', b, record, prefix, perk_ids))
        variants.append(('non-PERK identities', data, record, prefix, set()))
        for label, b, r, p, ids in variants:
            try:
                perk_tail(b, r, p, resolve, ids)
            except ValueError:
                check('reject ' + identity + ' ' + label, True)
            else:
                check('reject ' + identity + ' ' + label, False)
    fresh = json.loads((WORK / 'HIST-0255-ranks01.json').read_text())
    check('fresh original-derived scan agrees with retained witness', [(e['perk'], e['rank']) for r in fresh['rows'] if r['identity'] == 'starfield.esm:00563c' for e in r['tail']['ranked']] == [('starfield.esm:21b8cc', 1), ('starfield.esm:21b8c8', 3)])
    saved_rows = list(csv.DictReader((ROOT / 'docs/experiments/crew-skills/saved-ranks.csv').open(encoding='utf8')))
    check('nine explicit rows across four actors', len(saved_rows) == 9 and len({(r['sample'], r['actor']) for r in saved_rows}) == 4)
    check('both-drive guard final', guard() is None)
    out = dict(check_count=len(checks), checks=checks, physical_records_reread=len(reread),
               limits='Integrity, actual definition bytes and supported save grammar only; no live semantic oracle')
    (WORK / ('verification-' + args.run + '.json')).open('x', encoding='utf8').write(json.dumps(out, indent=2) + '\n')
    print('PASS', len(checks), 'checks;', len(reread), 'physical records reread')


if __name__ == '__main__':
    main()
