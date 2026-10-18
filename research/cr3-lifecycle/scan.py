# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded CR3 evidence acquisition; run from repository cwd with CPython3.14.

Reads all CR1 earlier-corpus receipts, then protected originals with nonempty E2.
Owned reuse: CR1 current/crew_extras, CR2 perk_tail and mature-save streaming.
Stdlib only. Writes exclusive ignored per-save JSON, corpus/instance CSV metadata
and guarded decoded scratch, never originals. No target/database/network/Git writes.
Unsupported template/rank branches remain explicit UNKNOWN, never zero/absent.
"""
from pathlib import Path
import collections
import csv
import json
import struct
import sys

ROOT = Path.cwd()
WORK = ROOT / '.local-work/cr3-lifecycle'
sys.path[:0] = [str(ROOT / p) for p in ['research/cr2-skills',
    'research/cr1-crew', 'save-analysis/scripts', '.local-work/cr1-crew']]
from definitions import pin
from current import actor_prefix, explicit_actor_links
from saved import perk_tail
from crew_extras import extra_view
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from validate_mature_outposts import directory
from workshop_population import typed_records, initial_prefix


def write_csv(name, rows):
    path = ROOT / 'docs/experiments/crew-lifecycle' / name
    with path.open('w', encoding='utf8', newline='') as f:
        w = csv.DictWriter(f, list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def main():
    guard()
    defs = json.loads((ROOT / '.local-work/cr2-skills/definitions01.json').read_text())
    perks = {f'starfield.esm:{r["formid"]:06x}' for r in defs['records'] if r['type'] == 'PERK'}
    corpus, instances = [], []
    for path in sorted((ROOT / '.local-work/cr1-current/corpus').glob('*.json')):
        old = json.loads(path.read_text())
        pairs = [(r['identity'], e['members']) for r in old.get('rows', [])
                 for e in r.get('extras', {}).get('extras', [])
                 if e['type'] == 'e2' and e.get('members')]
        label = path.stem
        corpus.append(dict(sample=label, sha256=old['source']['sha256'],
            prior_status=old.get('error', 'FRAMED'), positive_owners=len(pairs),
            selected=bool(pairs), new_receipt=f'.local-work/cr3-lifecycle/{label}.json' if pairs else 'NOT_REREAD'))
        if not pairs:
            continue
        dest = WORK / (label + '.json')
        if dest.exists():
            rows = json.loads(dest.read_text())['rows']
        else:
            guard()
            source = Path(old['source']['path'])
            before = pin(source)
            assert before['sha256'] == old['source']['sha256']
            ids = {owner for owner, _ in pairs} | {a for _, members in pairs for a in members}
            ids |= {'starfield.esm:005639', 'starfield.esm:00563c', 'starfield.esm:005986'}
            rows = []
            with decoded_save(source, WORK / 'scratch') as (data, decoded):
                d = directory(data)
                forms = struct.unpack_from('<' + 'I' * d['reference_count'], data, d['regions']['reference_u32'][0] + 4)
                plugins = plugin_tables(data)

                def resolve(t):
                    return saved_form(token_value(t, forms), plugins)

                for r in typed_records(data):
                    identity = resolve(r['token'])
                    if identity not in ids:
                        continue
                    row = dict(identity=identity, record=r, queue=[resolve(t) for t in r['refs']])
                    try:
                        p = actor_prefix(data, r) if r['form_type'] == 0x4b else initial_prefix(data, r)
                        row['prefix'] = p
                        row['extras'] = extra_view(data, r, p, resolve)
                    except (ValueError, struct.error) as e:
                        row['prefix_gap'] = str(e)
                    if r['form_type'] == 0x4b:
                        try:
                            row['links'] = explicit_actor_links(data, r, resolve)
                            for t in row['links']['trace']:
                                if t['type'] == '2b':
                                    mask = int.from_bytes(bytes.fromhex(t['template_mask']), 'little')
                                    slots = [i for i in range(15) if mask & (1 << i)]
                                    row['template_parts'] = dict(zip(map(str, slots), t['templates']))
                        except (ValueError, struct.error) as e:
                            row['link_gap'] = str(e)
                        try:
                            row['ranks'] = perk_tail(data, r, actor_prefix(data, r), resolve, perks)
                        except (ValueError, struct.error) as e:
                            row['rank_gap'] = str(e)
                    row['body_hex'] = bytes(data[r['body']:r['end']]).hex()
                    rows.append(row)
            assert pin(source) == before
            dest.open('x', encoding='utf8').write(json.dumps(dict(source=before, decoded=decoded,
                rows=rows, source_unchanged=True), indent=2) + '\n')
        byid = {r['identity']: r for r in rows}
        for owner, members in pairs:
            actual = byid[owner]
            e2 = [e for e in actual.get('extras', {}).get('extras', []) if e['type'] == 'e2']
            assert len(e2) == 1 and e2[0]['members'] == members
            for actor in members:
                r = byid.get(actor, {})
                links = [e for e in r.get('links', {}).get('entries', []) if e['keyword'] == 'starfield.esm:26beac']
                reciprocal = len(links) == 1 and links[0]['target'] == owner
                instances.append(dict(sample=label, actor=actor, owner=owner,
                    actor_record=r.get('record', {}).get('offset', 'UNKNOWN'),
                    reciprocal=reciprocal, mode_offset=links[0]['mode_offset'] if links else 'UNKNOWN',
                    slot3=r.get('template_parts', {}).get('3', 'UNKNOWN'),
                    nested_npc=next((t['created_npc'] for t in r.get('links', {}).get('trace', []) if t['type'] == '2b'), 'UNKNOWN'),
                    explicit_ranks=json.dumps(r.get('ranks', {}).get('ranked', []), separators=(',', ':')),
                    rank_status='EXPLICIT' if 'ranks' in r else r.get('rank_gap', 'UNKNOWN'),
                    link_status='DECODED' if 'links' in r else r.get('link_gap', 'MISSING_ACTOR'),
                    local_receipt=str(dest.relative_to(ROOT)).replace('\\', '/')))
        print(label, 'actors', len(members), 'records', len(rows), flush=True)
    write_csv('corpus.csv', corpus)
    write_csv('instances.csv', instances)
    guard()
    print('COMPLETE', len(corpus), 'corpus rows', len(instances), 'E2 member witnesses', collections.Counter(r['slot3'] for r in instances))


if __name__ == '__main__':
    main()
