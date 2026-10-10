"""SPDX-License-Identifier: GPL-3.0-or-later
Original pinned-build packed world identity decoder (EXP0020).
Source-informed by Starfield 1.16.244.0 VA 14096fb40; see trace-notes.md.
Pure stdlib arithmetic, no I/O or target effects. Returns the encoded chart
indices, not a continuous position, FormID or active loaded-frame selection.
The consumer masks 18 system bits; reserved high bits are retained explicitly.
"""


def unpack_world_key(value):
    if type(value) is not int or not 0 <= value < 1 << 64:
        raise ValueError('UINT64_REQUIRED')
    if value == (1 << 64)-1:
        raise ValueError('INVALID_WORLD_KEY')
    upper = value >> 32
    return dict(x=value & 0xffff, y=(value >> 16) & 0xffff,
                tag=upper & 7, body_index=(upper >> 3) & 63,
                system_id=(upper >> 9) & 0x3ffff, reserved=upper >> 27)


def qualified_grid(value, n=49152):
    """Reject unsupported tags/ranges; preserve the source chart convention.

    Native 14096fb40 reverses encoded axes for tags 2/3 before hierarchical
    lookup. This result deliberately retains encoded axes and tag, compatible
    with audit_activated_grid.offset; it does not silently canonicalize them.
    """
    result = unpack_world_key(value)
    if result['reserved'] or result['tag'] > 3:
        raise ValueError('UNSUPPORTED_WORLD_KEY')
    if not 0 < n <= 65536 or result['x'] >= n or result['y'] >= n:
        raise ValueError('GRID_RANGE')
    return result


def find_unit3_context(buffer, region_start, unit4_header):
    """Scoped envelope decoder, anchored to an independently framed unit 4.

    Reads a bytes-like decoded save only. Native mask 0x0c (1418236c0):
    compact string-reference count, uint16 indices, uint32 body length.
    A unique matching envelope is required; this is not a full save parser.
    Returns selected numeric fields, never raw body data. Reader bounds cap
    every access; the scan cannot extend beyond the caller's proven R1 span.
    """
    from outpost_record_framing import Reader

    if not 0 <= region_start < unit4_header <= len(buffer):
        raise ValueError('ENVELOPE_BOUNDS')
    matches = []
    q = region_start
    while (q := buffer.find(b'\x03\0\0\0', q, unit4_header)) >= 0:
        try:
            reader = Reader(buffer, q+4, unit4_header)
            count = reader.count()
            reader.take(count*2)
            length = int.from_bytes(reader.take(4), 'little')
            if length >= 12 and reader.p+length == unit4_header:
                key = int.from_bytes(reader.take(8), 'little')
                checksum = int.from_bytes(reader.take(4), 'little')
                matches.append(dict(header=q, start=reader.p-12, length=length,
                                    strings=count, key=f'{key:016x}',
                                    checksum=checksum, **qualified_grid(key)))
        except ValueError:
            pass
        q += 1
    if len(matches) != 1:
        raise ValueError('UNIT3_ENVELOPE_NOT_UNIQUE')
    return matches[0]


def unit3_world_descriptors(buffer, context):
    """Read the scoped generated-world descriptor array following key/checksum.

    14132d260/14132d500 and 1403a5560: uint32 count, then body uint32,
    key uint64 and legacy three-byte reference token. Two queued string refs
    per descriptor live in the envelope table. This does not remap a token to
    a live FormID or parse the later lists/typed world component payload.
    """
    from outpost_record_framing import Reader

    reader = Reader(buffer, context['start']+12,
                    context['start']+context['length'])
    count = int.from_bytes(reader.take(4), 'little')
    if count > (reader.end-reader.p)//15 or count*2 > context['strings']:
        raise ValueError('WORLD_DESCRIPTOR_BOUNDS')
    rows = []
    for ordinal in range(count):
        start = reader.p
        body = int.from_bytes(reader.take(4), 'little')
        key = int.from_bytes(reader.take(8), 'little')
        token = bytes(reader.take(3)).hex()
        rows.append(dict(ordinal=ordinal, offset=start, body=f'{body:08X}',
                         key=f'{key:016x}', world_token=token,
                         **qualified_grid(key)))
    return rows, reader.p
