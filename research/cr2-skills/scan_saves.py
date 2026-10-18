# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only CR2 positive-corpus acquisition; stdlib plus owned save readers.

Reads seven existing protected originals via CR1 corpus source pins. Decodes to
ignored guarded scratch through stream_save, reads typed Actor records, writes
exclusive ignored JSON and authored numeric save-join CSV. No source-save writes,
game/load/project/Git/network actions. Local primary data are not publishable.
Requires definitions01 and CR1's corpus receipts; unsupported Actor branches
remain UNKNOWN. Scan selects named actors and explicit perk-reference leads,
not a complete crew census or a negative assignment oracle.
"""
from pathlib import Path
import csv
import json
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / '.local-work/cr2-skills'
sys.path[:0] = [str(Path(__file__).parent), str(ROOT / 'save-analysis/scripts'),
               str(ROOT / 'research/cr1-crew'), str(ROOT / '.local-work/cr1-crew')]
from definitions import pin
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from validate_mature_outposts import directory
from workshop_population import typed_records
from current import actor_prefix, explicit_actor_links
from saved import perk_tail


def main():
    guard()
    definitions = json.loads((WORK / 'definitions01.json').read_text())['records']
    perks = {f'starfield.esm:{r["formid"]:06x}' for r in definitions if r['type'] == 'PERK'}
    targets = {'starfield.esm:' + p for p in ['005639', '00563c', '005986', '005788', '29d488', '0059a9']}
    crew_perks = {f'starfield.esm:{r["formid"]:06x}' for r in definitions if r['type'] == 'PERK' and r['edid'].lower().startswith('crew')}
    all_rows = []
    for label in ['HIST-0255', 'HIST-0021', 'HIST-0022', 'HIST-0024', 'HIST-0036', 'HIST-0077', 'Save52']:
        old = ROOT / '.local-work/cr1-current/corpus' / (label + '.json')
        if not old.exists():
            old = ROOT / '.local-work/cr1-crew' / (label + '-crew03.json')
        source_pin = json.loads(old.read_text())['source']
        source = Path(source_pin['path'])
        before = pin(source)
        assert before['sha256'] == source_pin['sha256']
        rows = []
        with decoded_save(source, WORK / 'scratch-saves') as (data, decoded):
            d = directory(data)
            forms = struct.unpack_from('<' + 'I' * d['reference_count'], data, d['regions']['reference_u32'][0] + 4)
            plugins = plugin_tables(data)

            def resolve(token):
                return saved_form(token_value(token, forms), plugins)

            for record in typed_records(data):
                if record['form_type'] != 0x4b:
                    continue
                identity = resolve(record['token'])
                queue = [resolve(t) for t in record['refs']]
                if identity not in targets and not crew_perks.intersection(queue):
                    continue
                row = dict(sample=label, identity=identity, record_offset=record['offset'],
                           record_end=record['end'], perk_state='UNKNOWN', assignment_state='UNKNOWN')
                try:
                    prefix = actor_prefix(data, record)
                    row['prefix'] = prefix
                    row['tail'] = perk_tail(data, record, prefix, resolve, perks)
                    row['perk_state'] = 'EXPLICIT_RANKS_DECODED'
                except (ValueError, struct.error) as error:
                    row['rank_gap'] = str(error)
                try:
                    row['links'] = explicit_actor_links(data, record, resolve)
                    row['assignment_state'] = 'EXPLICIT_LINK_BLOCK_DECODED'
                except (ValueError, struct.error) as error:
                    row['link_gap'] = str(error)
                rows.append(row)
        assert pin(source) == before
        out = dict(source=before, decoded=decoded, rows=rows, source_unchanged=True)
        (WORK / (label + '-ranks01.json')).open('x', encoding='utf8').write(json.dumps(out, indent=2) + '\n')
        all_rows.extend(rows)
        print(label, 'selected', len(rows), 'rank blocks', sum('tail' in r for r in rows), flush=True)
        guard()
    fields = ['sample', 'actor', 'perk', 'saved_rank', 'rank_byte_decoded_offset', 'perk_block_start', 'perk_block_end', 'assignment_evidence']
    with (ROOT / 'docs/experiments/crew-skills/saved-ranks.csv').open('w', encoding='utf8', newline='') as stream:
        writer = csv.DictWriter(stream, fields, lineterminator='\n')
        writer.writeheader()
        for row in all_rows:
            for entry, offset in zip(row.get('tail', {}).get('ranked', []), row.get('tail', {}).get('rank_offsets', [])):
                writer.writerow(dict(sample=row['sample'], actor=row['identity'], perk=entry['perk'], saved_rank=entry['rank'],
                                     rank_byte_decoded_offset=offset, perk_block_start=row['tail']['start'],
                                     perk_block_end=row['tail']['end'], assignment_evidence='CR1 current-witnesses.csv; local links'))


if __name__ == '__main__':
    main()
