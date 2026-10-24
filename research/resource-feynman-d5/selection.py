# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure descriptor traversal for the qualified BIOM-key creation route.

Reads caller-provided installed records and initialized component rows. Returns
the selected DNAM and an ordered rejection/selection ledger. No I/O, target or
save access. Creation-route and historical-population qualification are external.
"""
import hashlib
import struct


def entries(records, rsgd):
    active = None
    for tag, value in records[rsgd][1]:
        if tag == b'RNAM':
            active = int.from_bytes(value, 'little')
        elif tag == b'DNAM':
            yield active, value


def qualify_everywhere(records, rsgd):
    """Preserve D3/D4E rejection of effective nonzero Everywhere geometry."""
    for resource, raw in entries(records, rsgd):
        rarity = next(value[0] for tag, value in reversed(records[resource][1]) if tag == b'SNAM')
        if rarity == 6 and struct.unpack_from('<f', raw, 40 * 13 + 28)[0] != 0:
            raise ValueError('NONZERO_EVERYWHERE')


def descriptor(records, rows, biome):
    if len({r['biome'] for r in rows}) != len(rows):
        raise ValueError('DUPLICATE_CREATION_KEY')
    current = next(r for r in rows if r['biome'] == biome)
    root, effective = current['root'], current['rsgd']
    if not root:
        raise ValueError('NO_ASSIGNED_FAMILY_REQUIRES_DESCRIPTOR_REVIEW')
    trace = []

    def search(rid, stage, candidate):
        for ordinal, (resource, raw) in enumerate(entries(records, rid)):
            selected = resource == root
            trace.append(dict(stage=stage, biome=candidate, rsgd=rid,
                ordinal=ordinal, resource=resource,
                outcome='SELECTED' if selected else 'RESOURCE_MISMATCH'))
            if selected:
                return raw, dict(root=f'{root:08x}', rsgd=f'{rid:08x}',
                    supplier_biome=f'{candidate:08x}', descriptor_route=stage,
                    dnam_sha256=hashlib.sha256(raw).hexdigest(), trace=trace)
        return None

    result = search(effective, 'CURRENT_EFFECTIVE', biome)
    if result:
        return result
    for tag, value in records[biome][1]:
        if tag == b'RNAM':
            result = search(int.from_bytes(value, 'little'), 'CURRENT_BIOME_RNAM', biome)
            if result:
                return result
    for row in sorted(rows, key=lambda r: r['biome']):
        other = row['biome']
        if other == biome or row['root'] != root:
            trace.append(dict(stage='ALTERNATE_VISIT', biome=other,
                outcome='CURRENT_BIOME' if other == biome else 'ROOT_MISMATCH'))
            continue
        # Native 0x14079c5e0 reuses the CURRENT effective RSGD context.
        # The alternate's own effective override is not substituted here.
        result = search(effective, 'ALTERNATE_CURRENT_EFFECTIVE', other)
        if result:
            return result
        for tag, value in records[other][1]:
            if tag == b'RNAM':
                result = search(int.from_bytes(value, 'little'), 'ALTERNATE_BIOME_RNAM', other)
                if result:
                    return result
        trace.append(dict(stage='ALTERNATE_VISIT', biome=other, outcome='NO_DESCRIPTOR'))
    for tag, value in records[biome][1]:
        if tag != b'RNAM':
            continue
        rid = int.from_bytes(value, 'little')
        first = next(iter(entries(records, rid)), None)
        if first:
            resource, raw = first
            trace.append(dict(stage='FIRST_CURRENT_FALLBACK', biome=biome,
                              rsgd=rid, resource=resource, outcome='SELECTED'))
            return raw, dict(root=f'{root:08x}', rsgd=f'{rid:08x}',
                supplier_biome=f'{biome:08x}', descriptor_route='FIRST_CURRENT_FALLBACK',
                dnam_sha256=hashlib.sha256(raw).hexdigest(), trace=trace)
    raise ValueError('MISSING_FIRST_BIOME_DESCRIPTOR')


def special(records, current):
    """Search effective and current BIOM lists only for the initialized Special."""
    resource = current['slots'][4]
    if not resource:
        return None
    refs = [current['rsgd']] + [int.from_bytes(v, 'little')
        for t, v in records[current['biome']][1] if t == b'RNAM']
    for rid in refs:
        for fid, raw in entries(records, rid):
            if fid == resource:
                return resource, raw
    raise ValueError('MISSING_SPECIAL_CURRENT_BIOME_DESCRIPTOR')
