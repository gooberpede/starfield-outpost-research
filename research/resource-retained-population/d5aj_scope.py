# SPDX-License-Identifier: GPL-3.0-or-later
"""Version 1 source-Grid continuity for the pinned ordinary native graph.

Owned analytical predicate; no I/O or target effect. A fence's proc field is
its raw receiver: reason 3 is Grid, 4 source, 2 map, 5/6 manager. Only the
demonstrated disjoint owning-Grid case crosses a fence in this version. Other
cases refuse rather than infer harmlessness from unlike numeric addresses.
Native premises and contrary schedules are in the D5AJ invalidation matrix.
"""
METHOD = 'sor-d5aj-source-grid/1'


def continuity(events, start, stop, start_epoch, stop_epoch, grid):
    """Return a complete paired epoch bridge or reject ambiguous/relevant history.

    QPC establishes interval order; core sequence authenticates admission, which
    need not be causal order. Ambiguous fence timestamps and nested callbacks
    are refused. No missing epoch or unknown fence can become a positive proof.
    """
    if not (start < stop and 0x10000 <= grid < 0x7fffffffffff):
        raise ValueError('Invalid source interval or owning Grid')
    fences = sorted((e for e in events if e['kind'] in (10, 11)),
                    key=lambda e: (e['ticks'], e['sequence']))
    opened = None
    epoch = start_epoch
    crossed = []
    for e in fences:
        if e['ticks'] < start:
            continue
        if e['ticks'] > stop:
            break
        if (e['ticks'] in (start, stop) or e['status'] or e['a'] != 3 or
                not 0x10000 <= e['proc'] < 0x7fffffffffff or e['proc'] == grid):
            raise ValueError('Relevant, unknown or boundary-tied lifecycle fence')
        if e['epoch'] != epoch + 1:
            raise ValueError('Missing, crossed or ambiguously ordered epoch transition')
        epoch = e['epoch']
        if e['kind'] == 10:
            if opened is not None or e['hazards'] != 1:
                raise ValueError('Overlapping or nested lifecycle scope')
            opened = e
        else:
            if (opened is None or e['hazards'] or e['thread'] != opened['thread'] or
                    e['proc'] != opened['proc'] or e['ticks'] <= opened['ticks'] or
                    e['sequence'] <= opened['sequence']):
                raise ValueError('Unpaired or ambiguous lifecycle scope')
            crossed.append(dict(begin=opened['sequence'], end=e['sequence'],
                                grid=e['proc'], receiver_domain='Grid'))
            opened = None
    if opened is not None or epoch != stop_epoch:
        raise ValueError('Unclosed scope or unexplained global epoch difference')
    return dict(method=METHOD, owning_grid=grid, crossed=crossed,
                rule='Disjoint owning-Grid clears preserve this source; shared ProcGen slot relocation is permitted')
