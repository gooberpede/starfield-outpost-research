# SPDX-License-Identifier: GPL-3.0-or-later
"""Bounded P1 saved-instance inspection; project-owned readers, stdlib only.

Reads explicit existing source receipts, hash-pinned original saves, installed
definition cache and selected power catalogue. Writes exclusive local JSON under
.local-work/p1-power/saved and temporary decoded scratch removed by decoded_save.
No game/tool invocation, original modification, database, network or Git effects.
Preserves unsupported extras as gaps, never absence. Offsets: decoded logical
stream unless explicitly marked definition original-file offset. Run from repo
with CPython -B; --run alphanumeric --sample HIST-0036 or mature-Save52.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inventory_historical_saves import guard
from stream_save import decoded_save
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from outpost_record_framing import Reader, iter_records
from validate_mature_outposts import directory
from workshop_inventory import reference_prefix


def pin(path):
    with path.open('rb') as f:
        return dict(path=str(path), bytes=path.stat().st_size,
                    sha256=hashlib.file_digest(f, 'sha256').hexdigest())


def extra_view(data, record, prefix, resolve, *, workshop_resources=False):
    """Scoped adaptation of owned workshop_inventory.linked_prefix grammar.

    Returns all recognized extras even without 4C. BF values retain section and
    bit identity, not an invented effective-value sum. Unknown type stops parsing.
    """
    c = Reader(data, prefix['form_prefix_end'], record['end'])
    ri = prefix['next_reference_index']
    si = len(prefix.get('component', {}).get('strings', []))
    def strings(n):
        nonlocal si
        if not 0 <= n <= len(record['strings']) - si:
            raise ValueError('EXTRA_STRING_QUEUE_BOUNDS')
        si += n
    def refs(n):
        nonlocal ri
        if not 0 <= n <= len(record['refs']) - ri:
            raise ValueError('EXTRA_QUEUE_BOUNDS')
        tokens = record['refs'][ri:ri+n]
        ri += n
        return [resolve(t) for t in tokens]
    if record['flags'] & 0x80:
        refs(1)
        if not record['flags'] & 0xa6031f40:
            refs(1)
    if record['flags'] & 0x10:
        c.take(4)
    if not record['flags'] & 0xa6031f40:
        return dict(status='NO_EXTRA_DISPATCH')
    count = c.count()
    rows = []
    for _ in range(count):
        start = c.p
        tag = c.take(1)[0]
        row = dict(type=f'{tag:02x}', offset=start)
        if tag == 0x9c:
            row['flags'] = int.from_bytes(c.take(4), 'little')
        elif tag == 0xbf:
            row['sections'] = []
            for bits in (1, 3):
                n = c.count()
                mask = c.take((bits*n+7)//8)
                avs = refs(n)
                values = []
                for i in range(n*bits):
                    if mask[i//8] & (1 << (i%8)):
                        values.append(dict(av=avs[i//bits], bit=i%bits,
                                           offset=c.p, value=struct.unpack('<f', c.take(4))[0]))
                row['sections'].append(dict(bits=bits, avs=avs, values=values))
        elif tag == 0x4c:
            row['entries'] = []
            for _ in range(c.count()):
                key = refs(1)[0]
                off = c.p
                flag = c.take(1)[0]
                row['entries'].append(dict(keyword=key, target=refs(1)[0], mode=flag, offset=off))
        elif tag in (0x45, 0x83):
            row['references'] = refs(1)
        elif tag == 0x84:
            n = c.count(); row['references'] = refs(n); c.take(n)
        elif tag == 0x80:
            row['entries'] = []
            for _ in range(c.count()):
                row['entries'].append(dict(base=refs(1)[0], group=int.from_bytes(c.take(4), 'little')))
        elif tag in (0x54, 0x57, 0x2a):
            row['u32'] = int.from_bytes(c.take(4), 'little')
        elif tag == 0x1f:
            row['references'] = refs(2); row['byte'] = c.take(1)[0]
        elif tag == 0x61:
            c.take(32)
        elif tag == 0xda:
            row['references'] = refs(4); row['flag'] = c.take(1)[0]
            row['references'] += refs(1); row['word'] = int.from_bytes(c.take(4), 'little')
        elif tag == 0xbc and workshop_resources:
            # Same observed grammar as workshop_inventory.linked_prefix.
            groups = int.from_bytes(c.take(4), 'little')
            if groups > (c.end - c.p) // 4:
                raise ValueError('WORKSHOP_RESOURCE_GROUP_BOUNDS')
            for _ in range(groups):
                refs(1)
                entries = int.from_bytes(c.take(4), 'little')
                if entries > (c.end - c.p) // 17:
                    raise ValueError('WORKSHOP_RESOURCE_ROW_BOUNDS')
                refs(entries * 2)
                c.take(entries * 17)
            refs(c.count())
            c.take(1)
            strings(1)
            c.take(24)
        elif tag == 0xcb:
            n = c.count(); row['references'] = refs(n)
            row['words_offset'] = c.p
            row['words'] = list(struct.unpack('<'+'I'*n, c.take(n*4)))
        elif tag == 0xca:
            row['string_queue_count'] = c.count()
            if workshop_resources:
                strings(row['string_queue_count'])
        elif tag == 0x30:
            row['references'] = refs(1)
            row['node_count'] = c.count()
            if row['node_count']:
                row['unparsed_bytes'] = record['end'] - c.p
                rows.append(row)
                return dict(status='UNSUPPORTED_POLYMORPHIC_NODES', count=count, extras=rows,
                            next_reference_index=ri)
        elif tag == 0x0c:
            row['references'] = refs(c.count()); c.take(c.count())
        else:
            row['unparsed_bytes'] = record['end'] - start
            row['opaque_hex'] = bytes(data[start:record['end']]).hex()
            rows.append(row)
            return dict(status='UNSUPPORTED_EXTRA', count=count, extras=rows, next_reference_index=ri)
        row['end'] = c.p
        rows.append(row)
    return dict(status='COUNT_CLOSED', count=count, extras=rows,
                body_end=c.p, record_end=record['end'], next_reference_index=ri,
                queue_count=len(record['refs']))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sample', required=True)
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    assert args.run.isalnum()
    base = ROOT / '.local-work/p1-power/saved'
    base.mkdir(parents=True, exist_ok=True)
    out = base / (args.run + '.json')
    assert not out.exists()
    guard()
    if args.sample == 'mature-Save52':
        prior = ROOT / '.local-work/resource-availability/saves01/mature-Save52.json'
    else:
        assert args.sample.startswith('HIST-') and args.sample[5:].isdigit()
        prior = ROOT / '.local-work/e3-fabricators/saved01' / (args.sample + '.json')
    old = json.loads(prior.read_text())
    source = Path(old['source']['path'])
    before = pin(source)
    assert before['sha256'] == old['source']['sha256']
    assert before['bytes'] == old['source'].get('bytes', old['source'].get('size'))
    cache = ROOT / '.local-work/e2-organic/inventory02.json'
    definitions = {r['formid']: r for r in json.loads(cache.read_text())['records']}
    power_cache = ROOT / '.local-work/p1-power/definitions02.json'
    power_definitions = {int(r['formid'], 16): r for r in json.loads(power_cache.read_text())['candidates']}
    # P1 specialist's positive, independently inspected base identity leads.
    generators = {0x30238, 0x2031e2, 0x2031e1, 0x2031e0, 0x3023a, 0x2031df,
                  0x2031de, 0x2031dd, 0x3023c, 0x2031e4, 0x2031e3,
                  0x1c5149, 0x1c5148, 0x1c5147, 0x7f7b, 0x1c514b, 0x2b063a, 0x8c54a}
    switches = {0x1b1862, 0x1b1863}
    connectors = {0x140b2e, 0x1ae412}
    lamps = set(range(0x33c9ba, 0x33c9c7)) | {0xdd784, 0x25250a}
    known = generators | switches | connectors | lamps
    rows, gaps, reference_index = [], collections.Counter(), {}
    with decoded_save(source, base / 'scratch') as (data, decoded):
        d = directory(data)
        a, z = d['regions']['reference_u32']
        forms = struct.unpack_from('<'+'I'*d['reference_count'], data, a+4)
        plugins = plugin_tables(data)
        def resolve(t):
            return saved_form(token_value(t, forms), plugins)
        for r in iter_records(data, *d['regions']['region_R3'], d['words'][9]):
            if int(r['token'], 16) >> 22 != 2:
                continue
            if r['explicit_type'] is not None and not 0x4a <= r['explicit_type'] <= 0x55:
                continue
            try:
                case = 5 if not r['flags'] & 0x8000 else 6 if r['flags'] & 0x02000008 else 4 if r['flags'] & 6 else 7
                p = reference_prefix(data, r, case)
                identity = resolve(r['token'])
                bidentity = resolve(p['base_token']) if p['base_token'] else None
                bid = int(bidentity.split(':')[1], 16) if bidentity and bidentity.startswith('starfield.esm:') else None
                definition = definitions.get(bid, {})
                fields = dict(definition.get('fields', []))
                props = {f'{i:06x}': v for i, v, tail in struct.iter_unpack('<IfI', bytes.fromhex(fields.get('PRPS', '')))}
                if bid in power_definitions:
                    definition = power_definitions[bid]
                    props = {f'{int(k,16):06x}': v for k, v in definition['properties'].items()}
                reference_index[identity] = dict(base=bidentity, offset=r['offset'], end=r['end'],
                    base_edid=definition.get('edid'), definition_offset=definition.get('offset'),
                    disabled=p['disabled'], deleted=p['deleted'])
                if bid not in known and not props.get('000330', 0) > 0:
                    continue
                kind = ('GENERATOR' if bid in generators else 'SWITCH' if bid in switches else
                        'CONNECTOR' if bid in connectors else 'LAMP' if bid in lamps else 'CONSUMER')
                row = dict(identity=identity, base=bidentity, kind=kind, record_offset=r['offset'],
                           record_end=r['end'], reference_queue_offset=r['reference_start'],
                           reference_queue=r['refs'], resolved_queue=[resolve(t) for t in r['refs']],
                           prefix=p, definition_edid=definition.get('edid'), base_props=props,
                           change_flags=r['flags'])
                try:
                    row['extra_view'] = extra_view(data, r, p, resolve)
                except (ValueError, IndexError) as e:
                    row['extra_gap'] = str(e)
                rows.append(row)
            except (ValueError, IndexError) as e:
                gaps[str(e)] += 1
    assert pin(source) == before
    targets = {t for r in rows for e in r.get('extra_view', {}).get('extras', [])
               for t in e.get('references', []) if isinstance(t, str)}
    result = dict(sample=args.sample, source=before, source_unchanged=True, prior=pin(prior),
                  definitions=pin(cache), tool=pin(Path(__file__)), decoded=decoded,
                  power_definitions=pin(power_cache),
                  referenced_endpoints={t: reference_index.get(t) for t in sorted(targets)},
                  header_versions=old.get('header_versions'), rows=rows, prefix_gaps=dict(gaps),
                  counts=dict(collections.Counter(r['kind'] for r in rows)),
                  limits=['Positive ordinary inline-base reference subset; not exhaustive constructions',
                          'Candidate family identity supplied by P1 installed-definition specialist',
                          'No electrical meaning inferred from arbitrary queued references or transfer links',
                          'No current loaded state measured; parsed flag words have separate bit semantics'])
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2); f.write('\n')
    guard()
    print(json.dumps(dict(sample=args.sample, rows=len(rows), counts=result['counts'], source_unchanged=True)))


if __name__ == '__main__':
    main()
