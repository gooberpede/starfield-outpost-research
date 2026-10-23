# SPDX-License-Identifier: GPL-3.0-or-later
"""C2D witness-blind ordinary-map selector and bounded block resolver.

Pure calculations using owned RG1 binary32/CRC/MT helpers. No file, network,
target or analysis-project effects. Caller supplies ordered registry, effective
map and settings. Definition order/defaults yield conditional predictions only.
No expected SFPT, observed anchor or geometry score is accepted by this API.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'resource-geometry'))
import context
from geometry import Draws, f32, mul
import struct


def eligible(registry, style):
    """Preserve pointer-array order, skipping nulls and unmatched style pointers.

    Style integers here are qualified definition identities standing in for the
    resolved native pointers. Native registry contents must be supplied, not
    inferred by sorting these IDs. A zero BIOM style has no eligible candidates.
    """
    return [r['id'] for r in registry if r is not None and style and r['style'] == style]


def predict(m, styles, registry, system, body_index, targets, *, surface_seed,
            rotate, qualification):
    """Return every ordinary coarse slot plus receipts for requested cells.

    Targets are (chart, coarse X, coarse Y). Entire preceding map traversal is
    retained because eligibility and optional orientation affect draw position.
    Qualification describes independently established inputs; it cannot change
    numeric decisions. Unsupported effective inputs leave the outcome unresolved.
    """
    seed = context.crc_bytes(struct.pack('<III', body_index, system, surface_seed))
    rng = Draws(seed)
    tables, traces = [], []
    for chart, face in enumerate(m['faces']):
        table = [(0, 0)] * 65536
        for ordinal, biome in enumerate(face['values']):
            x, y = ordinal % 256, 255 - ordinal // 256
            candidates = eligible(registry, styles.get(biome))
            start = len(rng.words)
            uniform = rng.uniform() if len(candidates) > 1 else None
            index = int(mul(f32(len(candidates)), uniform)) if uniform is not None else 0
            selected = candidates[index] if candidates else 0
            flags = 8 if candidates else 0
            if candidates and rotate:
                flags |= int(mul(rng.uniform(), 4.0)) * 32
                while True:
                    word = rng.rng.getrandbits(32)
                    rng.words.append(word)
                    if word != 0xffffffff:
                        break
                if word < 0x7fffffff:
                    flags |= 128
            table[x * 256 + y] = selected, flags
            if (chart, x, y) in targets:
                traces.append(dict(chart=chart, coarse=[x, y], raster_ordinal=ordinal,
                    biome=f'0x{biome:08x}', style=styles.get(biome),
                    candidate_order=[f'0x{v:08x}' for v in candidates],
                    draw_start=start, words=rng.words[start:], uniform=uniform,
                    candidate_index=index if candidates else None,
                    selected=f'0x{selected:08x}', flags=f'0x{flags:02x}'))
        tables.append(table)
    return dict(tables=tables, seed=seed, draw_count=len(rng.words), traces=traces,
                qualification=qualification,
                outcome='QUALIFIED' if all(qualification.values()) else 'UNRESOLVED_EFFECTIVE_INPUTS')


def resolve_slot(entries, sx, sy, blocks, default_block=None):
    """Model one backlink followed by typed lookup, not recursive anchor repair.

    Qualified interior slots only. Native 0x140784e95..0x140784fcd translates
    once, then tests resolved form/type. Bit 8 is not retested after translation.
    A missing default pointer is UNKNOWN, never a predicted empty source.
    """
    if not (0 <= sx < 16 and 0 <= sy < 16):
        raise ValueError('interior slot required')
    initial = entries[sx * 16 + sy]
    fid, flags = initial
    if not flags & 8:
        sx -= (flags >> 4) & 3
        sy -= (flags >> 6) & 3
        if not (0 <= sx < 16 and 0 <= sy < 16):
            return dict(status='UNKNOWN_NEIGHBOUR_CHART', initial=initial)
        fid, flags = entries[sx * 16 + sy]
    if fid in blocks:
        return dict(status='RESOLVED_TYPED_BLOCK', initial=initial, slot=[sx, sy],
                    block=fid, flags=flags, used_fallback=False)
    if default_block is None:
        return dict(status='UNKNOWN_DEFAULT_BLOCK', initial=initial,
                    resolved_slot=[sx, sy], resolved_form=fid, resolved_flags=flags)
    if default_block == 0:
        return dict(status='NO_CALLBACK_NULL_DEFAULT', initial=initial)
    if default_block not in blocks:
        return dict(status='UNKNOWN_DEFAULT_DEFINITION', initial=initial,
                    default_block=default_block)
    return dict(status='RESOLVED_DEFAULT', initial=initial, block=default_block,
                used_fallback=True)


def source_at(tag, x, y, origin, selected, patterns, blocks):
    """Resolve a raw-pattern interior cell, preserving unsupported fallback state.

    Formula lineage: owned context.source_at; native frame unchanged. The sole
    changed eligibility rule accepts a typed block after the single backlink.
    Rotated-pattern inputs fail explicitly rather than guessing their mapping.
    """
    cx, cy = x // 192, y // 192
    pid, pflags = selected['tables'][tag][cx * 256 + cy]
    if pflags != 8:
        raise ValueError('raw-pattern qualification required')
    sx, sy = (x % 192) // 12, (y % 192) // 12
    r = resolve_slot(patterns[pid]['entries'], sx, sy, blocks)
    if r['status'] != 'RESOLVED_TYPED_BLOCK':
        return None, r
    sx, sy = r['slot']
    fid = r['block']
    ax, ay = cx * 192 + sx * 12, cy * 192 + sy * 12
    dimensions = [v - 4 for v in blocks[fid]['dimensions']]
    if min(dimensions) <= 0:
        return None, dict(r, status='NO_CALLBACK_NONPOSITIVE_DIMENSIONS')
    local = [ax - origin[0], ay - origin[1]]
    native = [100 * (v - 2) for v in local]
    source = dict(id=f'{tag}:{ax}:{ay}:{fid:08x}', block=fid, pattern=pid,
        coarse_pattern_flags=pflags, source_flags=r['flags'], dimensions=dimensions,
        geographic_origin=[ax, ay], local_cell_origin=local, padding=2,
        origin=native, clip_center=[native[k] + dimensions[k] // 2 * 100 for k in (0, 1)] + [0],
        clip_half=[v // 2 * 100 + 200 for v in dimensions] + [0],
        cell_bounds=[1, dimensions[0] + 3, 1, dimensions[1] + 3],
        resource_biome=context.map_lookup(selected['map'], tag, ax, ay))
    return source, r
