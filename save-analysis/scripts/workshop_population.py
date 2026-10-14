"""SPDX-License-Identifier: GPL-3.0-or-later
Original offline population rework helpers. Stdlib/project readers only.
Reads decoded saves; no target, filesystem, Git or network effects. Native
mapping is evidence for the pinned build, not a transferable schema.
"""
import collections
import struct
from outpost_record_framing import Reader, iter_records
from validate_mature_outposts import directory
from workshop_inventory import reference_prefix

# 141815620: index < 0x3b; bytes at static VA144a53290. Only59 map bytes.
CHANGE_TYPES = bytes.fromhex(
    '4a4b4c4e4f50495a5b321e1f22232425262728292c2f3031353637390c0d5d5784177f88758755535169333f604d1b3e9a0e34ae425254b7bebdd8')


def typed_records(b):
    """Join ordered footer runs, never infer types from optional version byte.

    Native141815620 reads directory+2c. Require index validity, exact count and
    record closure. Keep repeated runs in original order, including zero runs.
    """
    if int.from_bytes(b[16:20], 'little') != 27:
        raise ValueError('UNQUALIFIED_SAVE_FORMAT')
    d = directory(b)
    at = struct.unpack_from('<I', b, d['offset'] + 0x2c)[0]
    if not d['regions']['late_region'][0] <= at < len(b):
        raise ValueError('TYPE_REGISTRY_BOUNDS')
    c = Reader(b, at, len(b))
    runs = []
    for _ in range(c.count()):
        index = c.take(1)[0]
        if index >= len(CHANGE_TYPES): raise ValueError('TYPE_INDEX')
        runs.append(dict(change_type=index, form_type=CHANGE_TYPES[index], count=c.count()))
    if sum(r['count'] for r in runs) != d['words'][9]:
        raise ValueError('TYPE_COUNT_CLOSURE')
    records = iter_records(b, *d['regions']['region_R3'], d['words'][9])
    for run in runs:
        for _ in range(run['count']):
            r = next(records)
            # The historical reader field name remains untouched in old evidence.
            r['buffer_version_override'] = r.pop('explicit_type')
            r['buffer_version'] = r['buffer_version_override'] if r['buffer_version_override'] is not None else b[0x14]
            r['form_type'] = run['form_type']
            r['change_type'] = run['change_type']
            yield r
    try: next(records)
    except StopIteration: return
    raise ValueError('TYPE_RECORD_EXCESS')


def initial_case(r):
    """141832f00/140b36310: reference family only; case0 is valid static data."""
    if not 0x4a <= r['form_type'] <= 0x55: return None
    f = r['flags']
    if int(r['token'], 16) >> 22 == 2 and not f & 0x8000: return 5
    if f & 0x02000008: return 6
    if f & 6: return 4
    return 7 if f & 0x8000 else 0


def initial_prefix(b, r):
    case = initial_case(r)
    if case is None: raise ValueError('NOT_REFERENCE_FAMILY')
    if case: return reference_prefix(b, r, case)
    # Static case0 has no initial spatial/reference payload. The same component
    # envelope and generic TESForm self/flags prefix follows it.
    c=Reader(b,r['body'],r['end']);ri=0
    out=dict(case=0,base_token=None,disabled=None,deleted=None,
        saved_form_flags=None,saved_aux_flags=None,initial_end=c.p)
    if r['flags'] & 4:
        start=c.p;version=c.take(1)[0]
        nr,ns=struct.unpack('<HH',c.take(4)) if version>=4 else (0,0)
        size=c.count();body=c.p;c.take(size)
        if nr>len(r['refs']) or ns>len(r['strings']):raise ValueError('COMPONENT_QUEUE_BOUNDS')
        out['component']=dict(start=start,end=c.p,version=version,size=size,body=body,
            references=r['refs'][:nr],strings=r['strings'][:ns]);ri=nr
    if ri>=len(r['refs']) or r['refs'][ri]!=r['token']:raise ValueError('SELF_REFERENCE_MISMATCH')
    out.update(self_reference_index=ri,self_token=r['refs'][ri]);ri+=1
    if r['flags']&1:
        out['saved_flags_offset']=c.p
        form,aux=struct.unpack('<IH',c.take(6))
        out.update(saved_form_flags=form,saved_aux_flags=aux,disabled=bool(form&0x800),deleted=bool(form&0x20))
    out.update(form_prefix_end=c.p,next_reference_index=ri)
    return out


def queue_census(records, resolve, known_members):
    """Independent necessary-condition test: saved4C keys enter reference queue.
    Absence excludes that serialized edge only, never defaults or construction.
    """
    counts = collections.Counter()
    leads = []
    for r in records:
        ft = r['form_type']; counts['type_%02x' % ft] += 1
        case = initial_case(r); counts['case_' + str(case)] += 1
        refs = [resolve(t) for t in r['refs']]
        if 'starfield.esm:054ba6' in refs:
            identity = resolve(r['token'])
            leads.append(dict(identity=identity, offset=r['offset'], form_type=ft,
                case=case, baseline_member=identity in known_members,
                references=refs, flags=r['flags']))
    return dict(counts=dict(counts), keyword_queue_leads=leads,
        additional_leads=[r for r in leads if not r['baseline_member']],
        scope='Necessary condition for saved4C only; defaults and alias routes separate')


def additional_single(r, identity_counts):
    """1421c6f90→1421c71b0 single path, without inventing omitted9C=0.

    CLOSED saved4C replaces its array (140547c90/140562ef0); absent192 thus
    makes the foundation conjunction false independently of9C. The absence of
    DA,191,dummy and80 closes this row's group/default inputs. This predicate
    deliberately proves a positive only, not a population-completeness claim.
    """
    x = r.get('linked_prefix', {})
    if not r.get('owner_identity'): raise ValueError('OWNER_UNQUALIFIED')
    if identity_counts[r['saved_reference']] != 1: raise ValueError('IDENTITY_NOT_UNIQUE')
    if x.get('following_extras') != 'CLOSED': raise ValueError('EXTRAS_NOT_CLOSED')
    if 0x4c not in x.get('types', []): raise ValueError('NO_REPLACEMENT_4C_ARRAY')
    if x.get('alternate_groups'): raise ValueError('ALIAS_INPUT_PRESENT')
    if x.get('packin') or r.get('base_identity') == 'starfield.esm:015804':
        raise ValueError('GROUP_INPUT_PRESENT')
    keys = {e.get('keyword_identity') for e in x.get('entries', [])}
    if keys & {'starfield.esm:000191', 'starfield.esm:000192'}:
        raise ValueError('RELATION_INPUT_PRESENT')
    if 'starfield.esm:054ba6' not in keys: raise ValueError('NO_DIRECT_OWNER')
    return dict(instance_identity=r['saved_reference'], instance_token=r['token'],
        owner_identity=r['owner_identity'], base_identity=r.get('base_identity'),
        construction_definition=r.get('base_identity'), root_kind='SINGLE_ROOT',
        member_identities=[r['saved_reference']], member_offsets=[r['offset']],
        editor_name=r.get('editor_name'), definition_provenance=r.get('definition_provenance'),
        record_offset=r['offset'], record_end=r['end'], form_type=0x4a,
        buffer_version=153, offset_domain='DECODED_LOGICAL_STREAM',
        raw_position=r['prefix'].get('xyz'), saved_disabled=r['prefix']['disabled'],
        saved_deleted_bit=r['prefix']['deleted'], saved_form_flags=r['prefix'].get('saved_form_flags'),
        saved_aux_flags=r['prefix'].get('saved_aux_flags'), extra_flags=x.get('extra_flags'),
        reason='CLOSED_4C_NO_192_FOUNDATION_NO_GROUP_INPUTS_NATIVE_SINGLE_PATH',
        completeness='POSITIVE_ROOT_ONLY_POPULATION_ACCEPTANCE_SEPARATE')
