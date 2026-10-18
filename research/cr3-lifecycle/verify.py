# SPDX-License-Identifier: GPL-3.0-or-later
"""CR3 finite integrity, selected-template and retained-body checks.

Reads protected originals by hash, local CR1/CR2/CR3 receipts, actual installed
ESM record bytes, HEAD/index and authored CSVs. Replays owned Actor prefix/link
and rank readers on retained bodies; corrupts only in-memory copies. Writes an
exclusive local verification receipt, definition-backed witness CSV and register.
Stdlib/owned helpers only; no live semantic oracle or target/database/Git writes.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import struct
import subprocess
import sys
import zlib

ROOT = Path.cwd()
WORK = ROOT / '.local-work/cr3-lifecycle'
sys.path[:0] = [str(ROOT / p) for p in ['research/cr2-skills',
    'research/cr1-crew', 'save-analysis/scripts', '.local-work/cr1-crew']]
from definitions import pin
from current import actor_prefix, explicit_actor_links
from saved import perk_tail
from inspect_outpost_definitions import subrecords
from inventory_historical_saves import guard


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    assert args.run.isalnum()
    guard()
    checks, witnesses, rereads = [], [], []

    def check(name, value):
        assert value, name
        checks.append(name)

    seed = json.loads((WORK / 'baseline.json').read_text())
    for p in seed['protected'] + [seed['brief'], seed['index']]:
        check('protected ' + p['path'], pin(Path(p['path'])) == p)
    check('HEAD unchanged', subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip() == seed['head'])
    defs = json.loads((ROOT / '.local-work/cr2-skills/definitions01.json').read_text())
    by = {r['formid']: r for r in defs['records']}
    wanted = [0x26f937, 0x2e91c, 0x2fdf7, 0x26f93b, 0x21b8c3, 0x21b8c8, 0x27df98]
    with Path(defs['source']['path']).open('rb') as f:
        for fid in wanted:
            r = by[fid]
            f.seek(r['offset'])
            h = f.read(24)
            size, flags, formid = struct.unpack_from('<III', h, 4)
            check('physical ESM identity ' + hex(fid), formid == fid and h[:4].decode() == r['type'])
            raw = f.read(size)
            if flags & 0x40000:
                expected = struct.unpack_from('<I', raw)[0]
                raw = zlib.decompress(raw[4:])
                check('decompressed ESM size ' + hex(fid), len(raw) == expected)
            fields = [(k.decode(), v.hex()) for k, v in subrecords(raw)]
            check('physical ESM fields ' + hex(fid), fields == [tuple(x) for x in r['fields']])
            rereads.append(dict(formid=f'{fid:08x}', offset=r['offset'], edid=r['edid']))
    root_mask = int.from_bytes(bytes.fromhex(dict(by[0x26f937]['fields'])['ACBS'])[14:16], 'little')
    check('spawn root enables perk template part3', bool(root_mask & 8))
    corpus = list(csv.DictReader((ROOT / 'docs/experiments/crew-lifecycle/corpus.csv').open(encoding='utf8')))
    check('203 original earlier corpus receipts retained', len(corpus) == 203)
    check('97 prior build rejects are not negative samples', sum('UNQUALIFIED_SAVE_HEADER_BUILD' in r['prior_status'] for r in corpus) == 97)
    instances = list(csv.DictReader((ROOT / 'docs/experiments/crew-lifecycle/instances.csv').open(encoding='utf8')))
    check('43 E2 member witnesses', len(instances) == 43)
    selected = [r for r in corpus if r['selected'] == 'True']
    check('all 23 positive E2 inputs reread', len(selected) == 23)
    qualified = []
    for c in selected:
        receipt = json.loads((WORK / (c['sample'] + '.json')).read_text())
        check('original rehash ' + c['sample'], pin(Path(receipt['source']['path'])) == receipt['source'])
        check('acquisition before/after ' + c['sample'], receipt['source_unchanged'])
        for r in receipt['rows']:
            if r['record']['form_type'] != 0x4b or 'links' not in r:
                continue
            record = r['record']
            data = bytearray(record['end'])
            data[record['body']:record['end']] = bytes.fromhex(r['body_hex'])
            mapping = dict(zip(record['refs'], r['queue']))
            resolve = mapping.__getitem__
            links = explicit_actor_links(data, record, resolve)
            check('retained body replay ' + c['sample'] + '/' + r['identity'], links == r['links'])
            for t in links['trace']:
                if t['type'] != '2b' or '3' not in r.get('template_parts', {}):
                    continue
                # Independent direct byte/queue selection, not list membership.
                at = t['start']
                check('2B tag and compact count15', data[at:at+2] == bytes([0x2b, 60]))
                mask = int.from_bytes(data[at+2:at+4], 'little')
                check('saved slot3 enabled', bool(mask & 8) and not mask & 0x8000)
                queue_index = t['queue_start'] + 1 + (mask & 7).bit_count()
                chosen = r['queue'][queue_index]
                check('independent selected part3 ' + r['identity'], chosen == r['template_parts']['3'])
                check('zero nested NPC change mask', data[t['npc_flags_offset']:t['npc_flags_offset']+4] == b'\0'*4)
                if chosen not in {'starfield.esm:02e91c', 'starfield.esm:02fdf7', 'starfield.esm:26f93b'}:
                    continue
                template = by[int(chosen.split(':')[1], 16)]
                fields = dict(template['fields'])
                check('selected specialist does not inherit unrelated perk part', not int.from_bytes(bytes.fromhex(fields['ACBS'])[14:16], 'little') & 8)
                grants = [struct.unpack('<IB', bytes.fromhex(v)) for k, v in template['fields'] if k == 'PRKR']
                assignment = next(e for e in links['entries'] if e['keyword'] == 'starfield.esm:26beac')
                instance = next(i for i in instances if i['sample'] == c['sample'] and i['actor'] == r['identity'])
                check('real reciprocal owner ' + r['identity'], instance['reciprocal'] == 'True' and assignment['target'] == instance['owner'])
                for perk, rank in grants:
                    witnesses.append(dict(sample=c['sample'], actor=r['identity'], owner=instance['owner'],
                        selected_part3=chosen, selected_template_queue_offset=record['reference_start']+3*queue_index,
                        created_npc=t['created_npc'], template_edid=template['edid'],
                        perk=f'{perk:08x}', definition_rank=rank, rank_basis='SELECTED_PART3_DIRECT_PRKR_NOT_ABSENT_RANK_ZERO',
                        mode_offset=assignment['mode_offset'], native_basis='1405d4a00/140cd77d0/141955080/141955400'))
                qualified.append(chosen)
                # Decoder guard, mutation occurs only in this temporary bytearray.
                bad = dict(record, buffer_version=152)
                try:
                    explicit_actor_links(data, bad, resolve)
                except ValueError:
                    check('wrong Actor version rejected', True)
                else:
                    check('wrong Actor version rejected', False)
    check('21 Engineering witnesses', qualified.count('starfield.esm:02e91c') == 21)
    check('2 Management witnesses', qualified.count('starfield.esm:02fdf7') == 2)
    check('9 Security witnesses', qualified.count('starfield.esm:26f93b') == 9)
    guard()
    with (ROOT / 'docs/experiments/crew-lifecycle/witnesses.csv').open('w', encoding='utf8', newline='') as f:
        w = csv.DictWriter(f, list(witnesses[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(witnesses)
    result = dict(checks=checks, passed=len(checks), definition_rereads=rereads,
        generic_witnesses=len(witnesses), scope='Integrity/grammar/selected base grants; actual loaded contribution NOT TESTED')
    (WORK / ('verification-' + args.run + '.json')).open('x', encoding='utf8').write(json.dumps(result, indent=2) + '\n')
    print('PASS', len(checks), 'checks;', len(witnesses), 'generic witnesses')


if __name__ == '__main__':
    main()
