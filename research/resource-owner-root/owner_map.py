# SPDX-License-Identifier: GPL-3.0-or-later
"""Logical array transitions from pinned FUN_1407bc3d0; stdlib only.

Input is already ordered component records, never an installed ESM or save.
No target effects or I/O. Capacity/allocation policy and native container keys
are outside this logical evaluator; failed appends can be supplied explicitly.
"""


def reconstruct(components, failed_appends=()):
    """Preserve duplicates, zero-root carry and displaced arrays across records."""
    maps, staging, trace = {}, [], []
    failures = set(failed_appends)
    for ordinal, row in enumerate(components):
        root, slots = row['root'], row['slots']
        if type(root) is not int or not 0 <= root <= 0xffffffff or len(slots) != 6:
            raise ValueError('COMPONENT_DOMAIN')
        before = staging.copy()
        appended, refused = [], []
        for slot, fid in enumerate(slots):
            if type(fid) is not int or not 0 <= fid <= 0xffffffff:
                raise ValueError('SLOT_DOMAIN')
            if fid:
                if (ordinal, slot) in failures:
                    refused.append(slot)
                else:
                    staging.append(fid)
                    appended.append(fid)
        installed = staging.copy()
        previous = maps.get(root, []).copy() if root else None
        created = root != 0 and root not in maps
        if root:
            maps[root], staging = staging, maps.get(root, [])
        trace.append(dict(ordinal=ordinal, identity=row.get('identity'), root=root,
                          slots=list(slots), staging_before=before,
                          appended=appended, refused_slots=refused,
                          created=created, destination_before=previous,
                          destination_after=installed if root else None,
                          staging_after=staging.copy()))
    return dict(maps=maps, trace=trace, discarded_staging=staging.copy())


def ordinary_candidates(root, mapping, rarities):
    """Root precedes extras; reject unequal identities tied in native rarity sort.

Identical duplicate pointers survive; their relative interchange is immaterial
to identity order. Missing root-map keys stop the ordinary native path.
"""
    if root not in rarities:
        return dict(status='UNRESOLVED_ROOT', before_sort=[], ordered=[])
    if not root or root not in mapping:
        return dict(status='NO_ROOT_MAP_ENTRY', before_sort=[], ordered=[])
    before = [root] + mapping[root]
    resolved = [fid for fid in before if fid in rarities]
    for fid in resolved:
        if any(fid != other and rarities[fid] == rarities[other] for other in resolved):
            return dict(status='UNRESOLVED_EQUAL_RARITY_SORT', before_sort=before, ordered=None)
    return dict(status='CONDITIONAL', before_sort=before,
                ordered=sorted(resolved, key=lambda fid: -rarities[fid]))
