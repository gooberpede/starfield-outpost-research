# SPDX-License-Identifier: GPL-3.0-or-later
"""R1 adaptation of research/cr1-crew/current.py (SOR-P-0002). Adds the
known fixed-u32 Extra9C before the first keyed link; other bounds unchanged.
Scoped CR1 actor-link evidence aid, not an importer or absence detector.

Reads supplied decoded memory/typed R3 records only. No I/O, dependencies outside
stdlib/owned save-analysis helpers, target execution or database/Git effects.
Caller qualifies the installed build, saved plugin tables and buffer version153.
Adapted from owned workshop_population.initial_prefix and workshop_inventory;
new Actor::LoadGame header and zero-change Extra2B branch follow pinned native
exports in .local-work/cr1-current/native. Unsupported branches fail closed.
Returns the FIRST explicit 4C block, not complete/default/loaded assignment state.
"""
import struct
from outpost_record_framing import Reader
from workshop_population import initial_prefix


def actor_prefix(data, record):
    if record['form_type'] != 0x4b or record['buffer_version'] != 153:
        raise ValueError('UNQUALIFIED_ACTOR_TYPE_OR_VERSION')
    # Components precede Actor::LoadGame; its private header precedes TESForm.
    p = initial_prefix(data, dict(record, flags=record['flags'] & ~1))
    c = Reader(data, p['form_prefix_end'], record['end'])
    start = c.p
    mask = int.from_bytes(c.take(4), 'little')
    c.take(4)
    if mask & 1:
        c.take(4)
    if mask & 2:
        c.take(1)
    c.take(5)
    p['actor_header'] = dict(start=start, end=c.p, mask=mask)
    if record['flags'] & 1:
        p['saved_flags_offset'] = c.p
        form, aux = struct.unpack('<IH', c.take(6))
        p.update(saved_form_flags=form, saved_aux_flags=aux,
                 disabled=bool(form & 0x800), deleted=bool(form & 0x20))
    p['form_prefix_end'] = c.p
    return p


def explicit_actor_links(data, record, resolve):
    p = actor_prefix(data, record)
    if record['flags'] & 0x10 or not record['flags'] & 0xa6071b40:
        raise ValueError('UNSUPPORTED_ACTOR_EXTRA_DISPATCH')
    c = Reader(data, p['form_prefix_end'], record['end'])
    ri = p['next_reference_index']
    trace = []

    def refs(n):
        nonlocal ri
        if not 0 <= n <= len(record['refs']) - ri:
            raise ValueError('ACTOR_QUEUE_BOUNDS')
        result = [resolve(t) for t in record['refs'][ri:ri+n]]
        ri += n
        return result

    count = c.count()
    for _ in range(count):
        start = c.p
        tag = c.take(1)[0]
        row = dict(type=f'{tag:02x}', start=start, queue_start=ri)
        if tag == 0xe6:
            n=int.from_bytes(c.take(4),'little')
            row['entries']=[dict(word=int.from_bytes(c.take(4),'little'),byte=c.take(1)[0]) for _ in range(n)]
        elif tag == 0x2b:
            row['source'] = refs(1)[0]
            n = c.count()
            if n != 15:
                raise ValueError('UNQUALIFIED_2B_TEMPLATE_COUNT')
            mask = c.take(2)
            if mask[1] & 0x80:
                raise ValueError('NONZERO_2B_MASK_PADDING')
            row['template_mask'] = mask.hex()
            row['templates'] = refs(sum(x.bit_count() for x in mask))
            row['created_npc'] = refs(1)[0]
            row['npc_flags_offset'] = c.p
            if int.from_bytes(c.take(4), 'little'):
                raise ValueError('UNSUPPORTED_2B_NPC_CHANGES')
            # Zero-change NPC load still consumes TESForm self from the queue.
            if refs(1)[0] != row['created_npc']:
                raise ValueError('NESTED_NPC_SELF_MISMATCH')
        elif tag == 0x84:
            n = c.count()
            row['references'] = refs(n)
            c.take(n)
        elif tag == 0x56:
            n = c.count()
            row['references'] = refs(n)
            c.take(n)
            refs(1)
            c.take(1)
            refs(1)
            c.take(1)
        elif tag == 0x0c:
            refs(c.count())
            c.take(c.count())
        elif tag == 0x1d:
            c.take(1)
        elif tag == 0x80:
            n = c.count()
            row['alternate_context'] = refs(n)
            c.take(n*4)
        elif tag == 0x33:
            flags = c.take(1)[0]
            if flags & ~3:
                raise ValueError('UNQUALIFIED_33_FLAGS')
            if flags & 1:
                c.take(2)
            if flags & 2:
                n = c.count()
                mask = c.take((3*n+7)//8)
                refs(n)
                c.take(sum(bool(mask[(i*3+j)//8] & (1 << ((i*3+j)%8)))
                           for i in range(n) for j in (0, 1)))
        elif tag == 0x9c:
            row['flags'] = int.from_bytes(c.take(4), 'little')
        elif tag == 0x4c:
            entries = []
            for _ in range(c.count()):
                key_index = ri
                key = refs(1)[0]
                at = c.p
                mode = c.take(1)[0]
                target = refs(1)[0]
                entries.append(dict(keyword=key, target=target, mode=mode,
                                    mode_offset=at, keyword_queue_index=key_index))
            row.update(end=c.p, queue_end=ri)
            trace.append(row)
            return dict(prefix=p, declared_extras=count, trace=trace,
                        entries=entries, complete_extras=False)
        else:
            raise ValueError(f'UNSUPPORTED_LEADING_EXTRA_{tag:02X}')
        row.update(end=c.p, queue_end=ri)
        trace.append(row)
    raise ValueError('NO_EXPLICIT_4C_IN_SUPPORTED_PREFIX_UNKNOWN_STATE')

