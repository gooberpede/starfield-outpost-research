"""SPDX-License-Identifier: GPL-3.0-or-later
D1 single-batch offline research. Reads frozen inventory, authorized current saves,
project catalogs/readers and existing native exports. Writes NEW ignored receipts
under .local-work/disappearing-deposits/run01; decoder scratch is removed. No game,
analysis-project, save, network or Git mutation. Stdlib/project only. Requires
installed CPython and existing local catalogs. C:/D: 40 GB guard; triage <=64 MiB.
Names are leads; deep identification uses saved beacon/body/owner relationships.
"""
import collections
import json
from pathlib import Path
import struct
import sys

from inventory_historical_saves import identity, guard, metadata, framing, transform
from stream_save import decoded_save
from validate_mature_outposts import directory, pool
from research_two_outpost_anchors import inspect
from research_workshop_origin import workshop_prefix
from research_durable_center import resource_rows, compensated
from extractor_resources import inventory, plugin_tables, select_records, definition_catalog
from workshop_inventory import audit, ownership_ledger
from test_outpost_record_framing import independent

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.local-work/disappearing-deposits/run01'


def write(name, value):
    with (OUT / name).open('x', encoding='utf8', newline='\n') as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write('\n')


def main():
    guard()
    OUT.mkdir(parents=True, exist_ok=False)
    hp = ROOT / '.local-work/historical-inventory/scan-04/inventory.json'
    cp = ROOT / '.local-work/save-capacity-location/esm-index-verified.json'
    sp = ROOT / '.local-work/extractor-resource/run01/static-records.json'
    historical = json.loads(hp.read_text())
    catalog = json.loads(cp.read_text())
    static = json.loads(sp.read_text())
    frozen = {r['inventory_id']: r for r in historical}
    # Preserve old and current inventory separately: a rotated autosave is not the
    # old sample simply because its path survives.
    current = sorted(Path('C:/Users/User/Documents/My Games/Starfield/Saves').glob('*.sfs'))
    write('accessible-files.json', [dict(path=str(p), size=p.stat().st_size,
        mtime_ns=p.stat().st_mtime_ns) for p in current])
    pins = [hp, cp, sp, Path(catalog['source']['path'])]
    pins += [Path(r['path']) for r in static['sources']]
    pins += list(Path(__file__).parent.glob('*.py'))
    pins += [Path(sys.executable), ROOT/'docs/implementation-briefs/CODEX_BRIEF_SOR_D1_disappearing_deposits_reconnaissance.md']
    before = {str(p): identity(p) for p in dict.fromkeys(pins)}
    write('tools-and-inputs-before.json', before)
    for old in [catalog['source']] + static['sources']:
        if before[str(Path(old['path']))]['sha256'] != old['sha256']:
            raise ValueError('DEFINITION_SOURCE_HASH_CHANGED')
    triage = []
    for old in historical:
        p = Path(old['source']['path'])
        row = dict(id=old['inventory_id'], source=old['source'])
        if not p.exists():
            row['status'] = 'MISSING_OLD_PATH'
        else:
            pin = identity(p)
            if pin['sha256'] != old['source']['sha256']:
                row['status'] = 'PATH_REPLACED_NOT_OLD_SAMPLE'
                row['current_sha256'] = pin['sha256']
            elif old.get('framing', {}).get('declared_decoded_size', 2**63) > 64*1024**2:
                row['status'] = 'DECODED_BOUND_EXCLUDED'
            else:
                guard()
                try:
                    raw_physical = p.read_bytes()
                    _, spans = framing(raw_physical)
                    b = transform(raw_physical, spans, True)
                    d = directory(b)
                    _, strings = pool(b, d)
                    row.update(status='STRING_TRIAGE_ONLY', metadata=metadata(b),
                        hits=[s for s in strings if any(t in s['text'].lower()
                            for t in ('decaran', 'au sb', 'vytinium'))])
                    del b, raw_physical
                except ValueError as e:
                    row.update(status='UNSUPPORTED', error=str(e))
                if identity(p) != pin:
                    raise ValueError('TRIAGE_INPUT_CHANGED')
        triage.append(row)
    write('triage.json', triage)
    print('TRIAGE', dict(collections.Counter(r['status'] for r in triage)), flush=True)
    cases = [(sid, Path(frozen[sid]['source']['path']), frozen[sid]['source']['sha256'])
        for sid in ('HIST-0249','HIST-0250','HIST-0251','HIST-0265','HIST-0266','HIST-0267')]
    manual = json.loads((ROOT/'.local-work/manual-S0-S7C/manifest.json').read_text())
    cases += [(r['label'], Path(r['copy']['path']), r['copy']['sha256'])
        for r in manual['samples'] if r['label'] in ('S3','S3C','S7')]
    save_pins = {str(p): identity(p) for _, p, _ in cases}
    write('saves-before.json', save_pins)
    for label, p, expected in cases:
        if save_pins[str(p)]['sha256'] != expected:
            raise ValueError('PRIMARY_SAVE_HASH_CHANGED')
        with decoded_save(p, OUT/'scratch') as (b, metrics):
            row = dict(label=label, source=save_pins[str(p)], metadata=metadata(b), decode=metrics)
            try:
                ex = inspect(b, catalog['records'])
                row['sites'] = []
                for beacon in ex['beacons']:
                    r = beacon['record']
                    t = dict(beacon)
                    try:
                        t['workshop'] = workshop_prefix(b, r, beacon['prefix'], resource_rows)
                        t['center'] = compensated(beacon['local_xyz'],
                            struct.unpack('<3f', bytes.fromhex(t['workshop']['delta_hex'])))
                    except ValueError as e:
                        t['workshop_error'] = str(e)
                    row['sites'].append(t)
            except ValueError as e:
                row['site_error'] = str(e)
            try:
                plugins = plugin_tables(b)
                cat = definition_catalog(select_records(static['records'], plugins))
                row['extractors'] = inventory(b, cat, plugins)
                raw = audit(b)
                d = directory(b)
                walk = independent(b, *d['regions']['region_R3'], d['words'][9])
                if [(r['offset'],r['end'],r['token'],r['change_flags']) for r in raw['records']] != [r[:4] for r in walk]:
                    raise RuntimeError('INDEPENDENT_RECORD_WALK_MISMATCH')
                ledger = ownership_ledger(raw)
                members = {r['saved_reference']: r for r in ledger['instances']}
                for obj in row['extractors']['instances']:
                    member = members.get(obj['saved_reference'], {})
                    obj['direct_owner'] = member.get('owner_identity')
                    obj['direct_owner_evidence'] = member.get('ownership_evidence', [])
                    obj['owner_reason'] = member.get('reason', 'NO_QUALIFIED_EDGE')
                row['ownership_coverage'] = ledger['coverage']
                row['independent_record_walk'] = True
                del raw, ledger
            except ValueError as e:
                row['extractor_or_ownership_error'] = str(e)
        write(label+'.json', row)
        print(label, 'sites', len(row.get('sites', [])), 'extractors',
            len(row.get('extractors', {}).get('instances', [])),
            row.get('site_error'), row.get('extractor_or_ownership_error'), flush=True)
    after = {str(p): identity(p) for p in dict.fromkeys(pins)}
    saves_after = {str(p): identity(p) for _, p, _ in cases}
    write('preservation.json', dict(inputs_equal=before == after,
        saves_equal=save_pins == saves_after, inputs_after=after, saves_after=saves_after))
    if before != after or save_pins != saves_after:
        raise ValueError('PROTECTED_INPUT_CHANGED')
    guard()


if __name__ == '__main__':
    main()
