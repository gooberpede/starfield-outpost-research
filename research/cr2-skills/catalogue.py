# SPDX-License-Identifier: GPL-3.0-or-later
"""Derive authored metadata tables from CR2's pinned local inventories.

Reads definitions01, quests-lists01, grants-pex01 and CR1 candidate CSV. Writes
UTF8/LF catalogue/population/entry metadata CSVs and an exclusive local receipt.
No source code/game text is copied into tables; IDs and analyst classifications
only. Stdlib, no target/save/database/Git/network effects. Definition templates
are recorded separately from direct or conditional grants, never runtime ranks.
"""
from pathlib import Path
import collections
import csv
import json
import struct

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.local-work/cr2-skills'
DOC = ROOT / 'docs/experiments/crew-skills'


def read(name):
    return json.loads((WORK / name).read_text(encoding='utf8'))


def entries(record):
    result = []
    current = None
    for key, value in record['fields']:
        if key == 'PRKE':
            raw = bytes.fromhex(value)
            current = dict(kind=raw[0], rank=raw[1] + 1, priority=raw[2], conditions=[], condition_group='UNSET')
            result.append(current)
        elif current is not None:
            if key == 'DATA':
                current['data'] = value
            elif key == 'PRKC':
                current['condition_group'] = int(value, 16)
            elif key == 'CTDA':
                raw = bytes.fromhex(value)
                current['conditions'].append(dict(group=current['condition_group'], flags=raw[0], comparison=struct.unpack_from('<f', raw, 4)[0],
                                                  function=int.from_bytes(raw[8:10], 'little'),
                                                  parameter=int.from_bytes(raw[12:16], 'little'),
                                                  parameter2=int.from_bytes(raw[16:20], 'little'),
                                                  run_on=int.from_bytes(raw[20:24], 'little'),
                                                  reference=int.from_bytes(raw[24:28], 'little'),
                                                  tail=int.from_bytes(raw[28:32], 'little')))
            elif key in ('EPFT', 'EPFB'):
                current[key] = int.from_bytes(bytes.fromhex(value), 'little')
            elif key == 'EPFD' and len(value) == 8:
                current['payload_float'] = struct.unpack('<f', bytes.fromhex(value))[0]
    return result


def write(name, fields, rows):
    with (DOC / name).open('w', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def main():
    records = read('definitions01.json')['records']
    by = {r['formid']: r for r in records}
    grants = read('grants-pex01.json')['grants']
    candidates = list(csv.DictReader((ROOT / 'docs/experiments/crew/candidates.csv').open(encoding='utf8')))
    robot_ids = {0x4297c, 0xbd67e, 0x1f416e, 0x1d9250, 0x1d924e}
    candidates += [dict(base_formid=f'{fid:08x}') for fid in sorted(robot_ids)]
    population = []
    holders = collections.defaultdict(list)
    non_skill_holders = collections.defaultdict(list)
    ranks = collections.defaultdict(set)
    for candidate in candidates:
        fid = int(candidate['base_formid'], 16)
        record = by[fid]
        name = record['edid']
        if fid in robot_ids:
            qualification = 'CONSTRUCTIBLE_ROBOT_ACTOR'
        elif name.startswith('EncCrew_') and ('Template' not in name):
            qualification = 'GENERIC_ARCHETYPE'
        elif name.startswith(('Crew_Elite_', 'Companion_')) and 'OtherPlayer' not in name:
            qualification = 'NAMED_RECRUIT_CONDITIONAL_STORY'
        else:
            qualification = 'EXCLUDED_CATEGORY_OR_TEMPLATE_LEAD'
        direct = []
        for key, value in record['fields']:
            if key == 'PRKR':
                raw = bytes.fromhex(value)
                perk, rank = int.from_bytes(raw[:4], 'little'), raw[4]
                direct.append(f'{perk:08x}:{rank}')
                if qualification.startswith('EXCLUDED'):
                    continue
                root = bytes.fromhex(next(v for k, v in by[perk]['fields'] if k == 'DATA'))
                if root[3] & 8:
                    holders[perk].append(f'{fid:08x}:{rank}:DIRECT')
                    ranks[perk].add(rank)
                else:
                    non_skill_holders[perk].append(f'{fid:08x}:{rank}:DIRECT_NON_UI_HELPER')
                    ranks[perk].add(rank)
        family = name.removeprefix('Crew_Elite_').lower()
        conditional = [g for g in grants if family.startswith(Path(g['member']).stem.lower().split('qf_crew_elitecrew_')[-1].rsplit('_', 1)[0])]
        grouped = collections.Counter((g['quest'], g['function'], g['perk']) for g in conditional)
        for (quest, function, perk_hex), rank in grouped.items():
            perk = int(perk_hex, 16)
            holders[perk].append(f'{fid:08x}:{rank}:CONDITIONAL:{function}')
            ranks[perk].add(rank)
        population.append(dict(base_formid=f'{fid:08x}', editorid=name, qualification=qualification,
                               direct_perk_rank=';'.join(direct) or 'NONE_DIRECT',
                               conditional_grants=';'.join(f'{p}:{n}:{q}:{fn}' for (q, fn, p), n in grouped.items()) or 'NONE_FOUND_IN_SELECTED_PEX',
                               template_fields=';'.join(k + ':' + v for k, v in record['fields'] if k in ('TPLT', 'TPTA')),
                               esm_offset=record['offset'], historical_rank='UNKNOWN_UNLESS_SEPARATELY_DECODED'))
    catalogue = []
    effects = []
    qualifying_skill_count = len(holders)
    audit = set(holders) | {0x20d24f, 0x4297e, 0x4297f, 0x6b728, 0x26fe1a}
    for fid in sorted(audit):
        record = by[fid]
        root = bytes.fromhex(next(v for k, v in record['fields'] if k == 'DATA'))
        es = entries(record)
        mechanism = ';'.join(sorted({f'type{e["kind"]}:' + e.get('data', 'NO_DATA') for e in es})) or 'NO_PRKE_ENTRIES'
        if fid == 0x6b728:
            context = 'NON_SKILL_COMPANION_HELPER_EXCLUDED_FROM_SKILL_COUNT'
        elif fid == 0x26fe1a:
            context = 'TEMPLATE_TEST_ENTRY_EXCLUDED_BY_CLEAR_SPELL_PERK_FLAG3'
        elif fid in (0x21b8c3, 0x21b8c8, 0x4297e, 0x4297f):
            context = 'OUTPOST_PRODUCER_TIMER'
        elif fid == 0x20d24f:
            context = 'OUTPOST_POWER_MODEL_A03_ROBOT_NO_HUMAN_RECRUIT_GRANT'
        elif root[2] == 1:
            context = 'SHIP_ENVIRONMENT'
        elif fid == 0x20e35b:
            context = 'SCRIPTED_ACTOR_SLOT_COST'
        elif not es:
            context = 'DISPLAY_OR_SCRIPT_ROLE_NO_NATIVE_PERK_ENTRY'
        else:
            context = 'ACTOR_LOCAL_COMBAT_OR_ABILITY'
        catalogue.append(dict(perk_formid=f'{fid:08x}', editorid=record['edid'],
                              observed_definition_grant_ranks=';'.join(map(str, sorted(ranks[fid]))) or 'NO_RECRUIT_GRANT',
                              defined_entry_ranks=';'.join(map(str, sorted({e['rank'] for e in es}))) or 'NO_ENTRY',
                              representative_crew=';'.join(holders[fid] or non_skill_holders[fid]) or 'SUPPLEMENTAL_EFFECT_AUDIT_ONLY',
                              crew_ui_flag=bool(root[3] & 8), environment=root[2], mechanism=mechanism,
                              context=context, esm_offset=record['offset'], evidence='definitions01.json;grants-pex01.json;native.md'))
        for index, e in enumerate(es):
            data = e.get('data', '')
            effects.append(dict(perk_formid=f'{fid:08x}', entry=index, kind=e['kind'], selected_rank=e['rank'], priority=e['priority'],
                                entrypoint=data[:2] if e['kind'] == 2 else 'ABILITY_OR_QUEST',
                                operation=data[2:4] if e['kind'] == 2 else 'N/A', data_identity=data if e['kind'] != 2 else 'ENTRYPOINT_OPERATION_CONTEXT_COUNT',
                                epft=e.get('EPFT', 'N/A'), epfb=e.get('EPFB', 'N/A'),
                                payload=e.get('payload_float', 'FORM_OR_OTHER'),
                                conditions=json.dumps(e['conditions'], separators=(',', ':'))))
    write('population.csv', list(population[0]), population)
    write('catalogue.csv', list(catalogue[0]), catalogue)
    write('entries.csv', list(effects[0]), effects)
    inherited = []
    for p in population:
        if p['qualification'].startswith('EXCLUDED'):
            continue
        record = by[int(p['base_formid'], 16)]
        fs = dict(record['fields'])
        acbs = bytes.fromhex(fs['ACBS'])
        assert len(acbs) == 16
        mask = int.from_bytes(acbs[14:16], 'little')
        tpta = bytes.fromhex(fs.get('TPTA', ''))
        assert len(tpta) == 60
        vmad = bytes.fromhex(fs.get('VMAD', ''))
        inherited.append(dict(base_formid=p['base_formid'], template_flags=f'{mask:04x}',
                              spell_perk_inherit_flag3=bool(mask & 8),
                              spell_perk_tpta_slot3=f'{int.from_bytes(tpta[12:16], "little"):08x}',
                              recruitment_script=('ELITE_STARTER_QUEST_BINDING' if b'EliteCrew_StartQuestonLoadScript' in vmad
                                                  else 'COMPANION_ROLE_SCRIPT' if b'companionactorscript' in vmad.lower()
                                                  else 'OUTPOST_ACTOR_SCRIPT' if b'OutpostActorScript' in vmad
                                                  else 'TEMPLATE_OR_GENERIC_ROLE'),
                              evidence='native024:140cd77d0 slot3; native020/022 part selection; definitions01 ACBS/TPTA/VMAD'))
    write('inheritance.csv', list(inherited[0]), inherited)
    receipt = dict(population_rows=len(population), qualification_counts=dict(collections.Counter(p['qualification'] for p in population)),
                   distinct_qualifying_skills=qualifying_skill_count, supplemental=len(audit) - qualifying_skill_count, catalogue_rows=len(catalogue), entry_rows=len(effects))
    (WORK / 'catalogue01.json').open('x', encoding='utf8').write(json.dumps(receipt, indent=2) + '\n')
    print(receipt)


if __name__ == '__main__':
    main()
