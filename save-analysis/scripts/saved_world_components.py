"""SPDX-License-Identifier: GPL-3.0-or-later
Original EXP0020 scoped typed world-array locator. Source-informed by native
140ad5f20/140ad6150. Reads supplied decoded memory only; no I/O/target effects.
Requires independently qualified parent tokens, installed system/body index
map and saved generated-world descriptors. This is not a generic unit6 decoder.
The native zero-terminated 37-byte grammar, maximal contiguous run, all parent
coverage and independently checked identities jointly qualify one run.
"""
import struct


def find_world_components(buffer, start, end, parents, body_keys, descriptors):
    if not 0 <= start < end <= len(buffer) or not parents:
        raise ValueError('WORLD_COMPONENT_INPUT_BOUNDS')
    if any(type(p) is not int or not 0 < p < 1 << 24 for p in parents):
        raise ValueError('PARENT_TOKEN_RANGE')
    worlds = {}
    for descriptor in descriptors:
        token = int(descriptor['world_token'], 16)
        if token in worlds:
            raise ValueError('DUPLICATE_WORLD_DESCRIPTOR')
        worlds[token] = descriptor['body']

    def row(q):
        if not start <= q <= end-37:
            return None
        v = struct.unpack_from('<5IB4i', buffer, q)
        body = body_keys.get((v[2], v[3]))
        if v[0] >= 1 << 24 or v[0] & 0xc00000 != 0x800000 or body is None:
            return None
        if v[4] and worlds.get(v[4]) != body:
            return None
        if v[5] > 3 or v[6] > v[7] or v[8] > v[9]:
            return None
        return dict(offset=q, world=f'{v[0]:06x}', linked=f'{v[1]:06x}',
                    system_id=v[2], body_index=v[3], secondary=f'{v[4]:06x}',
                    flags=v[5], xmin=v[6], xmax=v[7], ymin=v[8], ymax=v[9],
                    body=body)

    runs = {}
    for parent in parents:
        q = start
        while (q := buffer.find(parent.to_bytes(4, 'little'), q, end)) >= 0:
            if row(q):
                first = q
                while row(first-37):
                    first -= 37
                p, rows = first, []
                while (value := row(p)) is not None:
                    rows.append(value)
                    p += 37
                covered = {int(r['world'], 16) for r in rows}
                if (p+4 <= end and bytes(buffer[p:p+4]) == bytes(4)
                        and parents <= covered and len(covered) == len(rows)):
                    runs[first] = dict(start=first, end=p+4, rows=rows)
            q += 1
    if len(runs) != 1:
        raise ValueError('WORLD_COMPONENT_RUN_NOT_UNIQUE')
    return next(iter(runs.values()))
