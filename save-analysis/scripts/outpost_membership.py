"""SPDX-License-Identifier: GPL-3.0-or-later
Bounded offline membership prototype, source-informed by SOR-S-0127/0128.
Reads decoded bytes and an explicitly supplied definition catalog. No files,
writes, dependencies, live target effects or raw payload output. This is a
partial classifier: insufficient identity/registration/ownership coverage must
yield INDETERMINATE. Known gameplay labels are never inputs.
"""
import collections
import struct
from outpost_record_framing import Reader, iter_records
from validate_mature_outposts import directory

RESULTS = ('OUTPOSTS_PRESENT', 'NO_ACTIVE_OUTPOSTS', 'INDETERMINATE')


def token_value(token, table):
    """Saved identity domain, before engine load remapping; never a live ID.

    Tag 00 uses a one-based form array index; tags 01/10 are direct/static and
    dynamic respectively. Tag 11 is unsupported. Index zero is the null token.
    Array mapping remains conditional on the catalog's plugin/load-order basis.
    """
    n = int(token, 16)
    tag, value = n >> 22, n & 0x3fffff
    if tag == 0:
        if value == 0:
            return 0
        if value > len(table):
            raise ValueError('FORM_ARRAY_INDEX_OUT_OF_RANGE')
        return table[value - 1]
    if tag == 1:
        return value
    if tag == 2:
        return 0xff000000 | value
    raise ValueError('UNSUPPORTED_REFERENCE_TAG')


def initial_prefix(b, r, case):
    """Conditional REFR interpretation, not an inherited form-type resolver.
    Native selector 141832f00, readers 141835610/141835c20/1405dfa40.
    Tracks body and reference cursors separately; omission means unknown.
    """
    if case not in (4, 5, 6, 7):
        raise ValueError('UNSUPPORTED_INITIAL_CASE')
    c = Reader(b, r['body'], r['end'])
    refs = iter(enumerate(r['refs']))
    def ref():
        try:
            return next(refs)
        except StopIteration:
            raise ValueError('REFERENCE_QUEUE_EXHAUSTED') from None
    out = dict(case=case, base_token=None, disabled=None, deleted=None,
               saved_form_flags=None, saved_aux_flags=None)
    if case in (4, 5, 6):
        shape = c.take(1)[0]
        out.update(shape=shape, parent_token=ref()[1])
        out['xyz'] = list(struct.unpack('<3f', c.take(12)))
        for i in range(3):
            if shape & (1 << i):
                c.take(4)
        if not shape & 0x18:
            c.take(1)
        if case == 5:
            out['base_token'] = ref()[1]
        elif case == 6:
            out['placement_parent_token'] = ref()[1]
            out['placement_indices'] = list(struct.unpack('<2h', c.take(4)))
    else:
        out['initial_reference_token'] = ref()[1]
    out['initial_end'] = c.p
    # General form loader pops self even when saved form flags are omitted.
    out['self_reference_index'], out['self_token'] = ref()
    if out['self_token'] != r['token']:
        raise ValueError('SELF_REFERENCE_MISMATCH')
    if r['flags'] & 1:
        out['saved_flags_offset'] = c.p
        form, aux = struct.unpack('<IH', c.take(6))
        out.update(saved_form_flags=form, saved_aux_flags=aux,
                   disabled=bool(form & 0x800), deleted=bool(form & 0x20))
    out['form_prefix_end'] = c.p
    out['next_reference_index'] = out['self_reference_index'] + 1
    return out


def extra_prefix(b, r, prefix, buffer_version=None):
    """Walk only statically confirmed leading extras; stop at first unknown.
    Native REFR LoadGame conditional fields must already have been consumed.
    ExtraPromotedRef is explicitly NOT player ownership. ExtraWorkshop's start
    is recorded but its variable/versioned contents are not skipped or decoded.
    """
    c = Reader(b, prefix['form_prefix_end'], r['end'])
    ri = prefix['next_reference_index']
    out = dict(types=[], promoted_references=[], workshop_offset=None,
               ownership=None, complete=False)
    if r['flags'] & (0x80 | 0x10):
        out['stop_reason'] = 'REFR_PRE_EXTRA_FIELDS_UNSUPPORTED'
        return out
    if not r['flags'] & 0xa6031f40:
        out['stop_reason'] = 'NO_EXTRA_DISPATCH_BY_CHANGE_MASK'
        return out
    count = c.count()
    out['declared_count'] = count
    for _ in range(count):
        start = c.p
        typ = c.take(1)[0]
        out['types'].append(typ)
        if typ == 0x84:  # ExtraPromotedRef; reader 14054c2f0
            n = c.count()
            if n > len(r['refs']) - ri:
                raise ValueError('PROMOTED_REFERENCE_QUEUE_EXHAUSTED')
            for _ in range(n):
                out['promoted_references'].append(dict(token=r['refs'][ri], flag=c.take(1)[0]))
                ri += 1
        elif typ == 0x9c:  # ExtraFlags modern uint32, reader 140545e40
            if buffer_version is None or 0x42 <= buffer_version <= 0x59:
                out['stop_reason'] = 'EXTRA_FLAGS_BUFFER_VERSION_UNSUPPORTED'
                break
            out['extra_flags'] = int.from_bytes(c.take(4), 'little')
        elif typ in (0x4c, 0x80):
            # Readers 140547c90/14054b4b0: only the empty array case.
            if c.count() != 0:
                out['stop_reason'] = f'NONEMPTY_EXTRA_{typ:02X}_UNSUPPORTED'
                break
        elif typ == 0xbc:
            out['workshop_offset'] = start
            out['stop_reason'] = 'VARIABLE_EXTRAWORKSHOP_NOT_RECONSTRUCTED'
            break
        else:
            out['stop_reason'] = f'EXTRA_TYPE_{typ:02X}_NOT_DECODED'
            break
    else:
        out['complete'] = True
        out['stop_reason'] = 'LEADING_EXTRAS_CONSUMED'
    out.update(end=c.p, next_reference_index=ri)
    return out


def classify(b, catalog, diagnostics=False):
    """Catalog: direct_bases {saved FormID: label}; templates {saved FormID: base}.
    Explicit caller supplies save-era mapping; no filename/name/count oracle.
    R1 adjacency is returned as a lead, never authoritative template resolution.
    """
    d = directory(b)
    a, z = d['regions']['reference_u32']
    table_start = a
    class FormArray:
        def __len__(self): return d['reference_count']
        def __getitem__(self, i):
            if not 0 <= i < len(self): raise IndexError(i)
            return struct.unpack_from('<I', b, table_start + 4 + 4*i)[0]
    table = FormArray()
    a, z = d['regions']['region_R3']
    rs = iter_records(b, a, z, d['words'][9])
    bases = catalog['direct_bases']
    templates = catalog.get('templates', {})
    candidates, errors, reference_leads = [], [], []
    a1, z1 = d['regions']['region_R1']
    # Search only template tokens whose resolved IDs occur in the supplied
    # catalog. These are evidence leads, not a replacement for the R1 grammar.
    template_tokens = {i + 1: fid for i, fid in enumerate(table) if fid in templates}
    leads = collections.defaultdict(list)
    for i, fid in template_tokens.items():
        tok = i.to_bytes(3, 'big')
        p = a1
        while (p := b.find(tok, p, z1)) >= 0:
            if p >= a1 + 3:
                dynamic = b[p-3:p].hex()
                if int(dynamic, 16) >> 22 == 2:
                    leads[dynamic].append(dict(offset=p-3, template_token=tok.hex(),
                        template_formid=fid, base_formid=templates[fid]))
            p += 1
    unresolved_paths = collections.Counter()
    framed_count = 0
    for r in rs:
        framed_count += 1
        if diagnostics:
            occurrences = []
            for i, token in enumerate(r['refs']):
                try:
                    fid = token_value(token, table)
                except ValueError:
                    continue
                if fid in bases:
                    occurrences.append(dict(queue_index=i, token=token, formid=fid))
            if occurrences:
                reference_leads.append(dict(token=r['token'], offset=r['offset'],
                    end=r['end'], body=r['body'], ordinal=r['ordinal'],
                    flags=r['flags'], explicit_type=r['explicit_type'],
                    occurrences=occurrences))
        if int(r['token'], 16) >> 22 != 2:
            continue
        # A base position or adjacency may justify attempting a conditional
        # REFR decode. Other reference occurrences are counted as unresolved.
        direct = None
        if len(r['refs']) > 1:
            try:
                fid = token_value(r['refs'][1], table)
                direct = fid if fid in bases else None
            except ValueError:
                pass
        assoc = leads.get(r['token'], [])
        if direct is None and not assoc:
            unresolved_paths['DYNAMIC_RECORD_BASE_NOT_RECONSTRUCTED'] += 1
            continue
        if r['explicit_type'] is not None and not 0x4a <= r['explicit_type'] <= 0x55:
            errors.append(dict(offset=r['offset'], reason='EXPLICIT_NON_REFR_DECOY'))
            continue
        flags = r['flags']
        case = 5 if not flags & 0x8000 else 6 if flags & 0x02000008 else 4 if flags & 6 else 7
        row = dict(token=r['token'], offset=r['offset'], end=r['end'], body=r['body'],
                   flags=flags, explicit_type=r['explicit_type'],
                   type_basis='EXPLICIT' if r['explicit_type'] is not None else 'CONDITIONAL_REFR',
                   identity_basis='INLINE_BASE' if case == 5 and direct else 'R1_TEMPLATE_ADJACENCY_LEAD',
                   base_formid=direct if case == 5 else None, template_leads=assoc)
        if diagnostics:
            row.update(ordinal=r['ordinal'], reference_start=r['reference_start'],
                       string_start=r['string_start'])
        try:
            prefix = initial_prefix(b, r, case)
            row['prefix'] = prefix
            if case == 5 and direct:
                row['identity_label'] = bases[direct]
            row['extra_prefix'] = extra_prefix(b, r, prefix)
        except ValueError as e:
            row['decode_error'] = str(e)
        candidates.append(row)
    result = dict(status='INDETERMINATE', reason_codes=[
        'INHERITED_FORM_TYPES_AND_NONINLINE_BASES_INCOMPLETE',
        'R1_TEMPLATE_MAP_NOT_FULLY_DECODED',
        'WORKSHOP_REGISTRATION_AND_PLAYER_OWNERSHIP_UNVALIDATED',
        'SAVE_ERA_CONTENT_MAPPING_UNVERIFIED'],
        coverage=dict(framed_records=framed_count, exact_r3_closure=True,
            unresolved_dynamic_records=dict(unresolved_paths),
            supported_conditional_prefix_cases=[4, 5, 6, 7],
            extra_prefix_types=[0x84, 0x9c, 0xbc, 0x4c, 0x80],
            complete_beacon_enumeration=False, complete_ownership=False),
        candidate_count=len(candidates), candidates=candidates, rejected=errors,
        enabled_saved_candidates=sum(r.get('prefix', {}).get('disabled') is False for r in candidates),
        disabled_saved_candidates=sum(r.get('prefix', {}).get('disabled') is True for r in candidates),
        unknown_disabled_candidates=sum(r.get('prefix', {}).get('disabled') is None for r in candidates),
        isdeleted_set_records=[dict(token=r['token'], offset=r['offset']) for r in candidates
                              if r.get('prefix', {}).get('deleted') is True])
    if diagnostics:
        result['reference_leads'] = reference_leads
    return result
