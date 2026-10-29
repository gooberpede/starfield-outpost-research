# SPDX-License-Identifier: GPL-3.0-or-later
"""Decode authenticated R1 demand failures offline; never operate on the target.

Reads an immutable capture using the existing independent framing/ACK reader.
Optional --out creates a new JSON result. Stdlib only. No repairs or live writes.
Predicate definitions and byte provenance: d5p-r2-decision.md at this revision.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/retained-population'))
from read_capture import inspect, decode, SIZE_V2

DLL = '503464d3670ff00422303c10652b036cd0bc891d3f8f7cba9a22d9d396fb5667'
PROFILE = 'r1-0.2.0-full-eleven-hooks-used-for-r2-diagnosis'
ORDER = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
         17, 18, 19, 24, 20, 21, 22, 25, 26, 23)
NAMES = ('OK SingletonRead SourcePointerRead QueryPointerRead ManagerProcRead '
         'ManagerProcMismatch ModeRead SourceBytesRead QueryWordsRead OwnerRead '
         'DescriptorRead ProcTypeRead ProcTypeMismatch IndexRead GridPointerRead '
         'GridTypeRead GridTypeMismatch GridCountRead GridCapacityRead GridExtent '
         'GridDataRead MemberRead NotMember ContextLifetime GridCoverageLimit '
         'RetainedGridRead GridChanged').split()
READS = {1: ('manager', 8), 2: ('source', 8), 3: ('query_pointer', 8),
         4: ('actual_proc', 8), 6: ('mode', 1), 7: ('source_bytes', 112),
         8: ('query_words', 8), 9: ('owner', 4), 10: ('descriptor', 44),
         11: ('proc_type', 8), 13: ('source_index', 8), 14: ('grid', 8),
         15: ('grid_type', 8), 17: ('grid_count', 4), 18: ('grid_capacity', 4),
         20: ('members', 8), 21: ('member_slots', 8), 25: ('retained_grid', 8)}


def diagnose(e, image_base=None):
    """Interpret only composite Visited records; validity follows short circuiting."""
    reason = e.get('reason')
    if e['kind'] != 1 or reason not in range(27):
        return dict(result='UNRESOLVED_UNSUPPORTED_RECORD')
    # Original R1 context-reasons includes direct primitive checks without a
    # source_context frame. Do not invent composite validity for those records.
    if not e['frame']:
        return dict(result='UNRESOLVED_NONCOMPOSITE_CONTEXT', reason=reason)
    if bool(reason) != bool(e['status'] & 1):
        return dict(result='UNRESOLVED_CONTRADICTORY_REASON_STATUS', reason=reason)
    if reason in READS and (e['read_requested'] != READS[reason][1] or
                            e['read_returned'] > e['read_requested']):
        return dict(result='UNRESOLVED_CONTRADICTORY_READ_TUPLE', reason=reason)
    passed = set(ORDER if reason == 0 else ORDER[:ORDER.index(reason)])
    values = dict(e, mode=e['args'][4], query_words=e['args'][0])
    fields = {}
    for predicate, (field, size) in READS.items():
        status = ('READ_VALID' if predicate in passed else
                  'READ_FAILED' if predicate == reason else 'NOT_REACHED')
        # R1 does not retain the successful query pointer or member values.
        retained = field not in ('query_pointer', 'member_slots')
        fields[field] = dict(validity=status, retained=retained,
                             value=values[field] if status == 'READ_VALID' and retained else None)
    out = dict(result='CONTEXT_PASSED' if reason == 0 else 'FIRST_FAILURE_IDENTIFIED',
               reason=reason, predicate=NAMES[reason], sequence=e['sequence'],
               invocation=e['invocation'], parent=e['parent'], thread=e['thread'],
               epoch_at_start=e['epoch'], hazards_at_start=e['hazards'],
               frame=e['frame'], invocation_proc=e['proc'], fields=fields,
               subcause='UNRESOLVED', identity='NOT_A_CERTIFIED_GEOGRAPHIC_IDENTITY')
    if reason in READS:
        out['failed_read'] = {k: e[k] for k in
                              ('read_address', 'read_requested', 'read_returned', 'read_error')}
        out['expected_read_size'] = READS[reason][1]
        out['read_class'] = ('RANGE_REFUSED' if e['read_address'] < 0x10000 or
                             e['read_address'] >= 0x7fffffffffff - e['read_requested'] else
                             'INCOMPLETE_READ')
        if reason == 21:
            delta = e['read_address'] - e['members']
            out['member_slot'] = delta // 8 if delta >= 0 and delta % 8 == 0 and delta // 8 < e['grid_count'] else None
    elif reason == 5:
        out['comparison'] = dict(expected=e['proc'], observed=e['actual_proc'])
    elif reason in (12, 16):
        offset, field = (0x4b3f3a8, 'proc_type') if reason == 12 else (0x4b67f48, 'grid_type')
        out['comparison'] = dict(expected=image_base + offset if image_base is not None else None,
                                 expected_image_rva=offset, observed=e[field])
    elif reason == 19:
        out['comparison'] = dict(count=e['grid_count'], capacity=e['grid_capacity'], relation='count <= capacity')
    elif reason == 24:
        out['comparison'] = dict(count=e['grid_count'], capacity=e['grid_capacity'], observer_limit=256)
    elif reason == 26:
        out['comparison'] = dict(expected=e['grid'], observed=e['retained_grid'])
    elif reason == 22:
        out['subcause'] = 'NO_SOURCE_EQUALITY_IN_SUCCESSFULLY_READ_BOUNDED_ARRAY'
    elif reason == 23:
        out['subcause'] = 'UNRESOLVED_START_OR_CURRENT_HAZARD_EPOCH_CHANGE_OR_BROKEN_RECORDER'
    return out


def capture(folder, image_base=None):
    """Authenticate first, then decode only the acknowledged contiguous prefix.

    This bounded-purpose adapter accepts the original single-file R1 stream.
    Segmented or concurrently changing files are refused rather than rejoined.
    """
    import hashlib
    folder = Path(folder)
    if (folder / 'segments.json').exists():
        raise ValueError('Use the original single-file stream for R2 diagnosis')
    raw_before = (folder / 'events.bin').read_bytes()
    result = inspect(folder, DLL)
    raw = (folder / 'events.bin').read_bytes()
    if raw_before != raw or hashlib.sha256(raw).hexdigest() != result['capture_sha256']:
        raise ValueError('Capture changed during offline authentication')
    if result['identity']['schema'] != 'sor-d5p/2':
        raise ValueError('R2 requires unchanged final R1 schema 2')
    # The original plugin does not store image base. Never infer it from a
    # rejected type pointer. An optional base must have independent provenance.
    diagnostics = []
    for i in range(result['independently_verified_durable_records']):
        at = i * (SIZE_V2 + 16) + 16
        e = decode(raw[at:at + SIZE_V2])
        if e['kind'] == 1:
            diagnostics.append(diagnose(e, image_base))
    return dict(schema='sor-d5p-r2-diagnosis/1', acquisition_profile=PROFILE,
                authentication=result, diagnostics=diagnostics,
                scientific_hypothesis='UNRESOLVED', image_base=image_base,
                image_base_provenance='EXTERNALLY_SUPPLIED_NOT_INFERRED' if image_base is not None else 'UNAVAILABLE')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('folder', type=Path)
    p.add_argument('--image-base', type=lambda value: int(value, 0))
    p.add_argument('--out', type=Path)
    a = p.parse_args()
    text = json.dumps(capture(a.folder, a.image_base), indent=2) + '\n'
    if a.out:
        with a.out.open('x', encoding='utf8', newline='\n') as f:
            f.write(text)
    print(text)


if __name__ == '__main__':
    main()
