# SPDX-License-Identifier: GPL-3.0-or-later
"""Pure component initialization projection for the pinned main-file route.

Reads caller-supplied installed records and owned selection results. No I/O or
runtime answers. The six slots are descendants 1–4, Special 5 and BIOM-local
Everywhere 6. Container order is conditional on the documented creation route.
"""


def first_everywhere(records, biome):
    """Scan BIOM RNAM lists and RSGD entries in order, without chance or RNG."""
    for tag, raw in records[biome][1]:
        if tag != b'RNAM':
            continue
        rsgd = int.from_bytes(raw, 'little')
        for field, value in records[rsgd][1]:
            if field != b'RNAM':
                continue
            resource = int.from_bytes(value, 'little')
            rarity = next(v[0] for t, v in reversed(records[resource][1]) if t == b'SNAM')
            if rarity == 6:
                return resource, rsgd
    return 0, None


def components(records, prediction):
    rows = []
    for selected in prediction.biome_results:
        state = selected.orchestration
        biome = int(str(state.biome.form_id), 16)
        slots = [0] * 6
        family = selected.common_assignment.family
        if family:
            for descendant in family.emitted_descendants:
                resource = int(str(descendant.form_id), 16)
                rarity = next(v[0] for t, v in reversed(records[resource][1]) if t == b'SNAM')
                if rarity not in (1, 2, 3, 4) or slots[rarity - 1]:
                    raise ValueError('UNSUPPORTED_DESCENDANT_SLOT')
                slots[rarity - 1] = resource
        if state.special_selection:
            slots[4] = int(str(state.special_selection.form_id), 16)
        slots[5], supplier = first_everywhere(records, biome)
        rows.append(dict(identity=f'{biome:08x}', biome=biome,
            root=int(str(family.root.form_id), 16) if family else 0,
            slots=slots, rsgd=int(str(state.effective_rsgd.form_id), 16),
            everywhere_rsgd=supplier, installed_order=state.biome.index,
            assignment=str(selected.common_assignment.mechanism)))
    rows.sort(key=lambda row: row['biome'])
    if len({row['biome'] for row in rows}) != len(rows):
        raise ValueError('DUPLICATE_CREATION_KEY')
    return rows
