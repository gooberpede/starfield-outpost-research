"""SPDX-License-Identifier: GPL-3.0-or-later
Original offline availability evidence probe. Reads explicit hash-pinned archive
manifest, installed-definition cache and its original ESM sources. Writes a fresh
ignored run directory and temporary decoded scratch (cleaned by project reader).
Stdlib/project only. No game, process, Ghidra, network, Git or original mutations.
40 GB C:/D: guard before each decode and at completion. Body bytes/paths stay local.
This audits ordinary case-5 Workshop resource groups, NOT availability sets.
"""
import argparse
import collections
import json
from pathlib import Path
import struct

from extractor_resources import plugin_tables, saved_form, definition_catalog, select_records
from inventory_historical_saves import ROOT, identity, guard
from outpost_membership import initial_prefix, token_value
from outpost_record_framing import iter_records
from research_workshop_origin import workshop_prefix
from stream_save import decoded_save
from validate_mature_outposts import directory


def saved_resource_groups(c, refs, count):
    """Observed native 140f50880/140f515a0 wire grammar; semantics separate.
    Each outer group queues a form, u32 count; row queues two forms +17 bytes.
    Does not name any row as a deposit or certify omitted groups as empty terrain.
    """
    if count > (c.end-c.p)//4:
        raise ValueError('RESOURCE_GROUP_BOUNDS')
    groups = []
    for _ in range(count):
        key = refs(1)[0]
        offset = c.p
        n = int.from_bytes(c.take(4), 'little')
        if n > (c.end-c.p)//17:
            raise ValueError('RESOURCE_ROW_BOUNDS')
        rows = []
        for _ in range(n):
            start = c.p
            tokens = refs(2)
            raw = c.take(17)
            rows.append(dict(offset=start, references=tokens, payload_hex=raw.hex()))
        groups.append(dict(resource=key, count_offset=offset, rows=rows))
    return groups


def audit(b):
    plugins = plugin_tables(b)
    d = directory(b)
    a, _ = d['regions']['reference_u32']
    class Forms:
        def __len__(self): return d['reference_count']
        def __getitem__(self, i):
            if not 0 <= i < len(self): raise IndexError(i)
            return struct.unpack_from('<I', b, a+4+4*i)[0]
    forms = Forms()
    def resolve(t): return saved_form(token_value(t, forms), plugins)
    beacons, gaps = [], collections.Counter()
    total = 0
    for r in iter_records(b, *d['regions']['region_R3'], d['words'][9]):
        total += 1
        if r['flags'] & 0x8000 or len(r['refs']) < 3:
            continue
        try:
            base = resolve(r['refs'][1])
        except ValueError:
            gaps['UNRESOLVED_BASE'] += 1
            continue
        if base != 'starfield.esm:2c60e9':
            continue
        row = dict(token=r['token'], identity=resolve(r['token']),
                   record_offset=r['offset'], record_end=r['end'], base=base)
        try:
            p = initial_prefix(b, r, 5)
            row['prefix'] = p
            w = workshop_prefix(b, r, p, saved_resource_groups)
            for g in w['resource_rows']:
                g['resource_identity'] = resolve(g['resource'])
                for v in g['rows']:
                    v['reference_identities'] = [resolve(t) for t in v['references']]
            row['workshop'] = w
        except ValueError as e:
            row['gap'] = str(e)
        beacons.append(row)
    return dict(plugins=plugins, record_count=total, beacons=beacons,
                gaps=dict(gaps), availability_status='NOT_EVALUATED',
                coverage='ordinary inline-base case-5 candidates only; no full extra/body closure')


def write(p, obj):
    with p.open('x', encoding='utf8', newline='\n') as f:
        json.dump(obj, f, indent=2, sort_keys=True)
        f.write('\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--inputs', type=Path, required=True)
    ap.add_argument('--static', type=Path, required=True)
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    if not args.run.replace('-', '').isalnum(): raise ValueError('RUN_NAME')
    out = ROOT/'.local-work/resource-availability'/args.run
    guard(); out.mkdir(parents=True, exist_ok=False)
    pins = {str(p): identity(p) for p in (args.inputs, args.static)}
    source = json.loads(args.static.read_text(encoding='utf8'))
    for s in source['sources']:
        now = identity(Path(s['path']))
        if now['sha256'] != s['sha256'] or now['size'] != s['size']:
            raise ValueError('ESM_PIN_CHANGED')
        pins[s['path']] = now
    inputs = json.loads(args.inputs.read_text(encoding='utf8'))
    for v in inputs:
        p = Path(v['pin']['path']); now = identity(p)
        if now['sha256'] != v['pin']['sha256']:
            raise ValueError('SAVE_PIN_CHANGED')
        pins[str(p)] = now
    write(out/'before.json', pins)
    results = []
    for v in inputs:
        guard()
        with decoded_save(Path(v['pin']['path']), out/'scratch') as (b, m):
            data = audit(b)
            catalog = definition_catalog(select_records(source['records'], data['plugins']))
            resource_keys = {g['resource_identity'] for row in data['beacons']
                             for g in row.get('workshop', {}).get('resource_rows', [])}
            controls = {k: x for k, x in catalog.items()
                        if any(a['resource_identity'] in resource_keys for a in x['associations'])}
            result = dict(label=v['label'], series=v['series'], source=v['pin'],
                          metrics=m, data=data, group_definition_associations=controls)
        name = v['series']+'-'+v['label']+'.json'
        write(out/name, result)
        results.append(dict(label=v['label'], series=v['series'], file=name,
                            record_count=data['record_count'],
                            beacons=[dict(token=r['token'], gap=r.get('gap'),
                                resource_count=r.get('workshop', {}).get('resource_count'),
                                groups=r.get('workshop', {}).get('resource_rows')) for r in data['beacons']]))
        print(v['label'], [(x['token'], x['resource_count'], x['gap']) for x in results[-1]['beacons']], flush=True)
    write(out/'summary.json', results)
    after = {p: identity(Path(p)) for p in pins}
    if after != pins: raise ValueError('INPUT_CHANGED')
    write(out/'preservation.json', dict(before=pins, after=after))
    guard()


if __name__ == '__main__': main()
