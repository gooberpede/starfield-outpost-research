"""SPDX-License-Identifier: GPL-3.0-or-later
Original offline extractor association, stdlib/project readers only. Reads bytes
and explicitly supplied static records; no I/O or target effects in this module.
Definition field relationships are observed, not name-based classifications.
Conditional case-5 REFR coverage; no claim of full player ownership/load authority.
See docs/experiments/extractor-resource-contract.md for the frozen contract.
"""
import collections
import struct
from outpost_record_framing import Reader, iter_records
from outpost_membership import initial_prefix, token_value
from validate_mature_outposts import directory


def fields(row, tag):
    return [bytes.fromhex(v) for k, v in row['fields'] if k == tag]


def one(row, tag):
    values = fields(row, tag)
    if len(values) != 1:
        raise ValueError('NONUNIQUE_FIELD:' + tag)
    return values[0]


def u32(value):
    if len(value) != 4:
        raise ValueError('FORM_FIELD_WIDTH')
    return int.from_bytes(value, 'little')


def qualified(plugin, fid, masters, plugin_flags=None):
    """File-relative ESM FormID, not save/load/runtime identity. Masters ordered."""
    if fid == 0:
        return None
    names = masters + [plugin]
    plugin_flags = plugin_flags or {}
    high = fid >> 24
    if high in (0xfd, 0xfe):
        mask = 0x400 if high == 0xfd else 0x100
        names = [n for n in names if plugin_flags.get(n, 0) & mask]
        slot = (fid >> 16) & 0xff if high == 0xfd else (fid >> 12) & 0xfff
        local = fid & (0xffff if high == 0xfd else 0xfff)
    else:
        names = [n for n in names if not plugin_flags.get(n, 0) & 0x500]
        slot, local = high, fid & 0xffffff
    if slot >= len(names):
        raise ValueError('ESM_MASTER_INDEX')
    return f'{names[slot].lower()}:{local:06x}'


def plugin_tables(b):
    """Observed modern header grammar with exact plugin-block closure.
    Full u8, small u16, medium u32 counts; optional creation metadata (three
    strings plus byte). Trailer is observed 0100. Unsupported versions fail.
    No regex-derived slot mapping. Only modern 1.16.244.0 samples qualified here.
    """
    if b[:12] != b'SFS_SAVEGAME':
        raise ValueError('SAVE_SIGNATURE')
    c = Reader(b, 16 + int.from_bytes(b[12:16], 'little'), len(b))
    version = c.take(1)[0]
    def string(cursor):
        n = int.from_bytes(cursor.take(2), 'little')
        return cursor.take(n).decode('utf8')
    builds = [string(c), string(c)]
    if builds != ['1.16.244.0'] * 2:
        raise ValueError('UNQUALIFIED_SAVE_HEADER_BUILD')
    size = int.from_bytes(c.take(4), 'little')
    start = c.p
    p = Reader(b, start, start + size)
    groups = {}
    for label, width in [('full', 1), ('small', 2), ('medium', 4)]:
        n = int.from_bytes(p.take(width), 'little')
        if n > (p.end - p.p) // 3:
            raise ValueError('PLUGIN_COUNT_BOUNDS')
        names = []
        for _ in range(n):
            name = string(p).lower()
            if not name.endswith(('.esm', '.esp', '.esl')):
                raise ValueError('PLUGIN_NAME')
            flag = p.take(1)[0]
            if flag == 1:
                for _ in range(3):
                    string(p)
                p.take(1)
            elif flag != 0:
                raise ValueError('PLUGIN_METADATA_FLAG')
            names.append(name)
        groups[label] = names
    trailer = p.take(p.end - p.p)
    if trailer != b'\x01\x00':
        raise ValueError('PLUGIN_BLOCK_TRAILER')
    allnames = sum(groups.values(), [])
    if len(set(allnames)) != len(allnames) or groups['full'][0] != 'starfield.esm':
        raise ValueError('PLUGIN_TABLE_IDENTITY')
    return dict(groups=groups, start=start, end=p.end, version=version,
                builds=builds, trailer=trailer.hex())


def saved_form(fid, plugins):
    """Save-era full/medium/small slots, before any load remap. Fail on bad slot."""
    if fid == 0:
        return None
    high = fid >> 24
    if high == 0xff:
        return f'DYNAMIC:{fid:08x}'
    if high == 0xfe:
        kind, slot, local = 'small', (fid >> 12) & 0xfff, fid & 0xfff
    elif high == 0xfd:
        kind, slot, local = 'medium', (fid >> 16) & 0xff, fid & 0xffff
    else:
        kind, slot, local = 'full', high, fid & 0xffffff
    names = plugins['groups'][kind]
    if slot >= len(names):
        raise ValueError('SAVE_PLUGIN_INDEX')
    return f'{names[slot]}:{local:06x}'


def definition_catalog(records):
    """Exact relationships: CONT KWDA extractor category; PRPS AVIF;
    IRES NAM1=AVIF, NAM2=resource COBJ; COBJ CNAM=created item.
    Retain multiple IRES or malformed/missing relationships as unknown.
    Caller provides ordered plugin records; last record per qualified key wins.
    """
    masters = {}
    plugin_flags = {r['plugin'].lower():r['flags'] for r in records if r['type']=='TES4'}
    for r in records:
        if r['type'] == 'TES4':
            masters[r['plugin'].lower()] = [v.rstrip(b'\0').decode('utf8').lower()
                                           for v in fields(r, 'MAST')]
    bykey = {}
    for r in records:
        if r['type'] == 'TES4':
            continue
        p = r['plugin'].lower()
        key = qualified(p, r['formid'], masters[p], plugin_flags)
        bykey[key] = r
    def q(r, value):
        p = r['plugin'].lower()
        return qualified(p, u32(value), masters[p], plugin_flags)
    resource_avs = collections.defaultdict(list)
    for key, r in bykey.items():
        if r['type'] != 'IRES' or not fields(r, 'NAM1'):
            continue
        av = q(r, one(r, 'NAM1'))
        if av not in bykey or bykey[av]['type'] != 'AVIF':
            continue
        entry = dict(resource_identity=key, resource_label=r['edid'],
                     resource_record_offset=r['offset'], resource_plugin=r['plugin'],
                     actor_value_identity=av, item_identity=None, item_label=None)
        try:
            recipe = q(r, one(r, 'NAM2'))
            cr = bykey[recipe]
            if cr['type'] != 'COBJ':
                raise ValueError('RESOURCE_RECIPE_TYPE')
            item = q(cr, one(cr, 'CNAM'))
            ir = bykey[item]
            entry.update(recipe_identity=recipe, recipe_offset=cr['offset'],
                         item_identity=item, item_label=ir['edid'])
        except (ValueError, KeyError) as e:
            entry['item_gap'] = str(e)
        resource_avs[av].append(entry)
    catalog = {}
    for key, r in bykey.items():
        if r['type'] != 'CONT':
            continue
        kw = b''.join(fields(r, 'KWDA'))
        if len(kw) % 4:
            raise ValueError('KEYWORD_WIDTH')
        keywords = [q(r, kw[i:i+4]) for i in range(0, len(kw), 4)]
        if 'starfield.esm:008406' not in keywords:
            continue
        associations = []
        for raw in fields(r, 'PRPS'):
            if len(raw) % 12:
                raise ValueError('PRPS_WIDTH')
            for i in range(0, len(raw), 12):
                av = q(r, raw[i:i+4])
                value = struct.unpack_from('<f', raw, i+4)[0]
                if value > 0 and av in resource_avs:
                    for resource in resource_avs[av]:
                        associations.append(dict(resource, property_index=i//12,
                                                 property_value=value))
        catalog[key] = dict(base_identity=key, label=r['edid'],
                            source_plugin=r['plugin'], record_offset=r['offset'],
                            associations=associations,
                            status='ASSOCIATED' if len(associations) == 1 else 'UNKNOWN')
    return catalog


def select_records(records, plugins):
    """Order by explicit save tables. DLC masters remain file-relative.
    Does not assert equivalence of installed and historical content versions.
    """
    names = sum(plugins['groups'].values(), [])
    order = {name: i for i, name in enumerate(names)}
    return sorted((r for r in records if r['plugin'].lower() in order),
                  key=lambda r: (order[r['plugin'].lower()], r['offset']))


def inventory(b, catalog, plugins):
    d = directory(b)
    a, _ = d['regions']['reference_u32']
    class FormArray:
        def __len__(self): return d['reference_count']
        def __getitem__(self, i):
            if not 0 <= i < len(self): raise IndexError(i)
            return struct.unpack_from('<I', b, a + 4 + 4*i)[0]
    table = FormArray()
    def resolve(t): return saved_form(token_value(t, table), plugins)
    rows, leads, rejected = [], [], []
    unresolved = collections.Counter()
    count = 0
    for r in iter_records(b, *d['regions']['region_R3'], d['words'][9]):
        count += 1
        occurrences = []
        for i, t in enumerate(r['refs']):
            try:
                identity = resolve(t)
            except ValueError:
                unresolved['UNRESOLVED_REFERENCE_TOKEN'] += 1
                continue
            if identity in catalog:
                occurrences.append(dict(queue_index=i, base_identity=identity))
        dynamic = int(r['token'], 16) >> 22 == 2
        if not dynamic or r['flags'] & 0x8000 or len(r['refs']) < 3:
            if occurrences:
                leads.append(dict(token=r['token'], offset=r['offset'],
                                  occurrences=occurrences, reason='NON_CASE5_OR_NON_DYNAMIC'))
            if dynamic:
                unresolved['DYNAMIC_NONINLINE_REPRESENTATION'] += 1
            continue
        try:
            base = resolve(r['refs'][1])
        except ValueError:
            unresolved['UNRESOLVED_BASE_IDENTITY'] += 1
            continue
        if base not in catalog:
            if occurrences:
                leads.append(dict(token=r['token'], offset=r['offset'],
                                  occurrences=occurrences, reason='BASE_OCCURS_OUTSIDE_BASE_SLOT'))
            unresolved['DYNAMIC_OTHER_BASE'] += 1
            continue
        try:
            if r['explicit_type'] is not None and not 0x4a <= r['explicit_type'] <= 0x55:
                raise ValueError('EXPLICIT_NON_REFR')
            p = initial_prefix(b, r, 5)
        except ValueError as e:
            rejected.append(dict(token=r['token'], offset=r['offset'], reason=str(e)))
            continue
        context = []
        for i, t in enumerate(r['refs'][:-1]):
            try:
                if resolve(t) == 'starfield.esm:054ba6':
                    context.append(dict(keyword_queue_index=i, beacon_token=r['refs'][i+1],
                                        beacon_identity=resolve(r['refs'][i+1])))
            except ValueError:
                unresolved['UNRESOLVED_CONTEXT_TOKEN'] += 1
        definition = catalog[base]
        rows.append(dict(token=r['token'], saved_reference=resolve(r['token']),
                         reference_domain='TAGGED_SAVE_TOKEN_BEFORE_LOAD_REMAP',
                         offset=r['offset'], end=r['end'], ordinal=r['ordinal'],
                         offset_domain='DECODED_LOGICAL_STREAM',
                         base_token=p['base_token'], base_identity=base,
                         definition=definition, prefix=p,
                         type_basis='CONDITIONAL_REFR' if r['explicit_type'] is None else 'EXPLICIT',
                         context_leads=context, containing_outpost='UNRESOLVED',
                         context_basis='QUEUED_KEYWORD_REFERENCE_ADJACENCY_NOT_OWNERSHIP',
                         confidence='STRONG_SCOPED_PROPOSED',
                         production_state='NOT_ESTABLISHED', load_authority='UNKNOWN'))
    return dict(schema='extractor-resources/1', instances=rows, unresolved_leads=leads,
                rejected=rejected, coverage=dict(framed_records=count, exact_r3_closure=True,
                unresolved=dict(unresolved), complete_player_population=False,
                supported='DYNAMIC_CASE5_INLINE_CONT_WITH_EXTRACTOR_CATEGORY'),
                resource_counts=dict(collections.Counter(
                    r['definition']['associations'][0]['resource_label']
                    if r['definition']['status']=='ASSOCIATED' else 'UNKNOWN' for r in rows)))
