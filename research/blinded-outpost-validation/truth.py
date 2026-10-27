# SPDX-License-Identifier: GPL-3.0-or-later
"""Generic offline adapter for previously qualified positive consumer chains.

Reuses unchanged D5B consumer ancestry checks on copied rows. The body
and target IRES selector are parameters rather than Feynman constants. Caller
must independently authenticate capture bytes and bind exact Workshop identity.
Returns positive-only evidence; never emits a complete native census. No I/O,
target calls, new observer, save writes or third-party dependencies.
"""
import copy
import hashlib
import struct
import types
from bridge import loads


def reduce_positive(journal, expected_journal_sha256, tracker_module, body_formid, resources, workshop_le, expected_source, descriptor):
    """Return selected positive regions, preserving capture/callback ancestry.

    tracker_module must be the frozen owned D5B consumer module. A private globals
    dictionary avoids changing its published constants or imported module state.
    Workshop bytes come from raw_binding_extra's qualified +0x98 identity.
    Source/descriptor decoding follows the D5B interior chart-0 contract. Each
    named resource replays the unchanged chain independently to avoid the old
    first-matching-member projection losing other selected positive controls.
    """
    if hashlib.sha256(journal).hexdigest() != expected_journal_sha256:
        raise ValueError('INDEPENDENT_JOURNAL_MISMATCH')
    rows = [loads(line) for line in journal.splitlines() if line]
    # Authenticate the whole transcript; callers must not silently project away
    # intervening invalidations. An independently registered original digest is
    # essential. Per-receipt SRO1/ACK byte verification remains a prerequisite.
    seen, acks = {}, set()
    for position, row in enumerate(rows):
        if row.get('kind') == 'SAMPLE':
            if row['capture'] in seen:
                raise ValueError('DUPLICATE_SAMPLE')
            seen[row['capture']] = position
        if row.get('kind') == 'ACK_ACCEPTED' and row.get('accepted') is True:
            capture = row['capture']
            if capture not in seen or capture in acks:
                raise ValueError('ACK_BEFORE_SAMPLE_OR_DUPLICATE')
            acks.add(capture)
    original = tracker_module.Tracker.feed
    selected, gaps = [], 0
    for resource in resources:
        namespace = dict(vars(tracker_module), BODY=int(body_formid, 16), TARGETS=(int(resource, 16),))
        feed = types.FunctionType(original.__code__, namespace, original.__name__, original.__defaults__, original.__closure__)
        tracker = tracker_module.Tracker()
        for original_row in rows:
            row = copy.deepcopy(original_row)
            if row.get('kind') in ('PHASE', 'LOSS', 'EXCEPTION', 'THREAD_END'):
                tracker.active.clear(); gaps += 1
            if row.get('kind') == 'SAMPLE' and row.get('site') == 'updater_entry':
                # A new observed updater is an interval boundary; do not project
                # an older parent chain across it, even if stack nesting could
                # otherwise retain the parent's tracker entry.
                tracker.active.clear()
            if row.get('decision') in ('ACCEPT', 'REJECT'):
                try:
                    manager = bytes.fromhex(row['source_context']['raw_manager'])
                    source = bytes.fromhex(row['source_context']['raw_source'])
                    at = 0x1c0 if manager[0x20] == 3 else 0xc8
                    desc = manager[at:at+0x2c]
                    if len(source) != 0x70 or len(desc) != 0x2c or desc[0] != 0 or descriptor[0] != 0:
                        raise ValueError('UNQUALIFIED_SOURCE_CHART')
                    anchor = [sum(struct.unpack_from('<i', desc, off)[0] * scale
                        for off, scale in ((4+k*4, 192), (0x14+k*4, 12), (0x24+k*4, 1))) for k in range(2)]
                    xy = struct.unpack_from('<2i', source, 0x10)
                    key = f'0:{anchor[0]+xy[0]}:{anchor[1]+xy[1]}:{struct.unpack_from("<I", source)[0]:08x}'
                    valid = (anchor == descriptor[1:] and key == expected_source and
                        bytes.fromhex(row['raw_binding_extra'])[0x98:0xa0].hex() == workshop_le)
                except (ValueError, KeyError, IndexError, struct.error):
                    valid = False
                if not valid:
                    row['required_reads_complete'] = False
            key = (row.get('pid'), row.get('tid'), row.get('thread_lifetime'), row.get('updater_token'))
            entry_capture = tracker.active.get(key, {}).get('entry', {}).get('capture')
            if feed(tracker, row):
                accepted = tracker.last_match
                if not {entry_capture, accepted.get('capture'), row.get('capture')} <= acks:
                    continue
                raw = bytes.fromhex(accepted['geometry']['raw_region'])
                closure = bytes.fromhex(accepted['raw_closure'])
                selected.append(dict(source=expected_source, resource=resource,
                    points_le=accepted['geometry']['ordered_xyzw'], bound_le=raw[:16].hex(),
                    count=struct.unpack_from('<I', raw, 24)[0], updater_token=accepted['updater_token'],
                    accept_capture=accepted['capture'], transfer_capture=row['capture'],
                    query_descriptor_le=accepted['raw_descriptor'], radius_le=closure[16:20].hex(),
                    upper_le=closure[20:24].hex()))
        gaps += tracker.gaps
    return dict(schema='sor-blind-positive/1', coverage='SELECTED_POSITIVES_ONLY',
        complete=False, body_formid=body_formid, workshop=workshop_le,
        journal_sha256=expected_journal_sha256,
        regions=selected, absence='UNKNOWN', source_census='UNKNOWN',
        gaps=gaps, native_lifetime_epoch='UNKNOWN')
