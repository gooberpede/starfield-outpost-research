# SPDX-License-Identifier: GPL-3.0-or-later
"""Scoped native-backed Actor perk-tail diagnostic, not a complete Actor decoder.

Pure decoder reads supplied typed buffer153 Actor bytes/queue and CR1 prefix.
Requires the native Actor suffix layout (141916b30/141917e40) with no bit24
byte, bit25 vector present and a present clock float. Establishes the suffix
from the independent record end; enumerates possible three-list starts and
requires a unique nonempty rank list whose identities are known PERKs. No
assumed quest ranks or fixed perk byte patterns participate in acceptance.
Unknown layouts and ambiguous candidates fail closed. No I/O or target effects.
"""
import struct
from outpost_record_framing import Reader


def perk_tail(data, record, prefix, resolve, perk_ids):
    if record['form_type'] != 0x4b or record['buffer_version'] != 153:
        raise ValueError('UNQUALIFIED_TYPE_OR_VERSION')
    mask = prefix['actor_header']['mask']
    if not mask & (1 << 22):
        raise ValueError('NO_EXPLICIT_ADDITIONAL_PERK_BLOCK_NOT_ZERO_RANK')
    if mask & (1 << 24) or not mask & (1 << 25):
        raise ValueError('UNSUPPORTED_SUFFIX_MASK')
    # Native suffix: translated vector12, raw12, flag1+float4, vector12, bool1.
    # Reference writes go to the separate relocation queue in this R3 mode.
    end = record['end']
    suffix = end - 42
    if suffix < prefix['form_prefix_end']:
        raise ValueError('TRUNCATED_SUFFIX')
    if data[suffix + 24] != 1 or data[end - 1] not in (0, 1):
        raise ValueError('UNQUALIFIED_CLOCK_OR_BOOL_SUFFIX')
    refs_after = 2 + bool(mask & (1 << 21)) + bool(mask & (1 << 23))
    queue_end = len(record['refs']) - refs_after
    matches = []
    for start in range(prefix['form_prefix_end'], suffix):
        c = Reader(data, start, suffix)
        try:
            n = c.count()
            if not 0 < n <= queue_end:
                continue
            rank_start = c.p
            ranks = list(c.take(n))
            n2 = c.count()
            n3 = c.count()
            if n2 + n3 + n > queue_end:
                continue
            third_values = [struct.unpack('<I', c.take(4))[0] for _ in range(n3)]
            if c.p != suffix:
                continue
            qstart = queue_end - n - n2 - n3
            identities = [resolve(t) for t in record['refs'][qstart:queue_end]]
            if not all(v in perk_ids for v in identities) or not all(1 <= k <= 255 for k in ranks):
                continue
            matches.append(dict(start=start, end=suffix, queue_start=qstart,
                                rank_offsets=list(range(rank_start, rank_start + n)),
                                ranked=[dict(perk=p, rank=k) for p, k in zip(identities[:n], ranks)],
                                second_identity_list=identities[n:n+n2],
                                third_identity_values=list(zip(identities[n+n2:], third_values)),
                                suffix_start=suffix, suffix_end=end, header_mask=mask))
        except (ValueError, struct.error):
            continue
    if len(matches) != 1:
        raise ValueError(f'AMBIGUOUS_OR_MISSING_PERK_TAIL:{len(matches)}')
    return matches[0]
