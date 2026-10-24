# SPDX-License-Identifier: GPL-3.0-or-later
"""Native small-list rarity ordering; pure original analytical implementation.

STATIC 0x1407af4a9/0x1407af569 and 0x1407af582–0x1407af76c select stable
insertion for at most 32 pointer entries. Larger unequal-identity ties remain
unsupported. Inputs are resolved numeric IRES identities, not native pointers.
"""


def candidates(root, mapping, rarities):
    if root not in rarities:
        return dict(status='UNRESOLVED_ROOT', before_sort=[], ordered=[])
    if not root or root not in mapping:
        return dict(status='NO_ROOT_MAP_ENTRY', before_sort=[], ordered=[])
    before = [root] + mapping[root]
    resolved = [fid for fid in before if fid in rarities]
    tied = any(fid != other and rarities[fid] == rarities[other]
               for fid in resolved for other in resolved)
    if len(resolved) > 32 and tied:
        return dict(status='UNRESOLVED_LARGE_LIST_TIE_ORDER', before_sort=before, ordered=None)
    # Strictly greater rarity shifts predecessors; equality preserves encounter order.
    ordered = []
    for fid in resolved:
        position = len(ordered)
        while position and rarities[fid] > rarities[ordered[position - 1]]:
            position -= 1
        ordered.insert(position, fid)
    return dict(status='CONDITIONAL', before_sort=before, ordered=ordered)
