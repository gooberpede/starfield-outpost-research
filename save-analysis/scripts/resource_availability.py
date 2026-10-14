"""SPDX-License-Identifier: GPL-3.0-or-later
Original conditional UI-row projection, source-informed by pinned retail static
141578500/1421f8120/14042e250. Pure stdlib, no I/O or target effects.
This cannot generate terrain operands or certify extractor placement. See the
resource-availability report/typed contract. Pointer equality is deliberately
different from FormID equality. Synthetic operands never become measured sets.
"""
from dataclasses import dataclass
from typing import Optional
import math
import struct
import random

EXE_SHA256 = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'


def generation_seed(packed_cell_key, manager_owner_key):
    """14079a330 raw CRC32 fold: key u64 then manager+80 u32, LE.
    Polynomial/table 0xedb88320, initial 0, no final xor. Typed domain is the
    native generation key, NOT an arbitrary saved-token or point grid key.
    """
    if type(packed_cell_key) is not int or not 0 <= packed_cell_key < 2**64:
        raise ValueError('GENERATION_KEY_DOMAIN')
    if type(manager_owner_key) is not int or not 0 <= manager_owner_key < 2**32:
        raise ValueError('MANAGER_OWNER_KEY_DOMAIN')
    crc = 0
    for byte in struct.pack('<QI', packed_cell_key, manager_owner_key):
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ (0xedb88320 if crc & 1 else 0)
    return crc


def first_mt_word(seed):
    """Native classic MT seed recurrence and first tempered output.
    Delegates twist/tempering to existing CPython stdlib after explicitly
    setting 624 seed words/index 624. Source-informed by pinned native and owned
    resource-reproducer/prng.py; its test supplies the seed-5489 reference word.
    No implementation is copied. This is not
    Python's seed() mapping; probability conversion is handled separately.
    """
    if type(seed) is not int or not 0 <= seed < 2**32: raise ValueError('MT_SEED_DOMAIN')
    state = [seed]
    for i in range(1, 624):
        previous = state[-1]
        state.append((1812433253*(previous^(previous>>30))+i) & 0xffffffff)
    rng = random.Random(0)
    rng.setstate((3, tuple(state)+(624,), None))
    return rng.getrandbits(32)


def generation_first_gate(packed_cell_key, manager_owner_key, chance, weight):
    """Conditional first 14079a330 stochastic gate only, NOT resource spawn.
    Missing operands stay UNKNOWN; chance comes from qualified DNAM rarity block
    (rarity+7)*40+28, and weight from the actual caller. Later stochastic count,
    positions, overlaps and region assembly remain outside this calculation.
    """
    if any(v is None for v in (packed_cell_key, manager_owner_key, chance, weight)):
        return dict(status='UNKNOWN', first_gate_pass=None, local_availability='NOT_EVALUATED')
    chance, weight = _normal_f32(chance), _normal_f32(weight)
    if chance < 0 or weight < 0: raise ValueError('GENERATION_SCALAR_DOMAIN')
    seed = generation_seed(packed_cell_key, manager_owner_key)
    word = first_mt_word(seed)
    # Native canonical can round 1.0; exact range upper is f32 bits 0x3f7fff58.
    canonical = _normal_f32(_normal_f32(word)/4294967296.0)
    upper = struct.unpack('<f', bytes.fromhex('58ff7f3f'))[0]
    probability = _normal_f32(canonical*upper)
    draw100 = _normal_f32(probability*100.0)
    threshold = _normal_f32(weight*chance)
    return dict(status='PARTIAL_GENERATION_FIRST_GATE', seed=seed, first_word=word,
                probability=probability, threshold=threshold, draw100=draw100,
                first_gate_pass=threshold > draw100, local_availability='NOT_EVALUATED')


def _normal_f32(value):
    """Qualified scalar domain: finite binary32 normal/zero, no FTZ ambiguity."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError('BINARY32_DOMAIN')
    try:
        result = struct.unpack('<f', struct.pack('<f', value))[0]
    except (OverflowError, struct.error):
        raise ValueError('BINARY32_DOMAIN') from None
    if not math.isfinite(result) or (result != 0 and abs(result) < 2**-126):
        raise ValueError('BINARY32_DOMAIN')
    return result


def region_broadphase(center_xy, region_xy, region_radius, query_radius, point_count):
    """Partial 1421e0f50 predicate, instruction sites 1421e1119..1154.
    Both XY positions MUST already be in the callback's translated frame.
    Only normal/zero binary32 intermediates and nonnegative radii qualified.
    A one-point passing region is accepted by this callback; multiple points
    still require the native descriptor/segment checks. No footprint verdict.
    """
    if len(center_xy) != 2 or len(region_xy) != 2: raise ValueError('XY_ARITY')
    if type(point_count) is not int or not 0 <= point_count < 2**32:
        raise ValueError('POINT_COUNT_DOMAIN')
    cx, cy = map(_normal_f32, center_xy)
    rx, ry = map(_normal_f32, region_xy)
    rr, qr = _normal_f32(region_radius), _normal_f32(query_radius)
    if rr < 0 or qr < 0: raise ValueError('RADIUS_DOMAIN')
    dx, dy = _normal_f32(rx-cx), _normal_f32(ry-cy)
    yy, xx = _normal_f32(dy*dy), _normal_f32(dx*dx)
    distance2 = _normal_f32(yy+xx)
    reach = _normal_f32(rr+qr)
    reach2 = _normal_f32(reach*reach)
    passes = distance2 <= reach2
    candidate = False if not passes or point_count == 0 else True if point_count == 1 else None
    return dict(distance2=distance2, reach2=reach2, broadphase_pass=passes,
                callback_candidate=candidate,
                status='PARTIAL_CALLBACK_PREDICATE' if candidate is not None else 'MISSING_DESCRIPTOR_SEGMENT_TESTS',
                extractor_placement='NOT_EVALUATED')


def harvester_resource_gate(produced_pointers, first, second, special, *,
                            place_anywhere_present, atmosphere_present, skip_vein_present):
    """Partial 1421f68f0 qualified harvester/property branch, not placement.
    Presence booleans are the result of 14044b610 with resolved AVIF defaults;
    numeric property value does not replace key presence. The caller must prove
    category/base/property resolution, one lifetime and successful resource-list
    construction. Null signifies an unobserved list/property, never an empty set.
    """
    props = (place_anywhere_present, atmosphere_present, skip_vein_present)
    if any(x is not None and type(x) is not bool for x in props):
        raise ValueError('PROPERTY_PRESENCE_DOMAIN')
    if place_anywhere_present is None:
        return dict(status='UNKNOWN', passes=None, selected_source=None, extractor_placement='NOT_EVALUATED')
    if place_anywhere_present:
        return dict(status='CONDITIONAL_RESOURCE_GATE', passes=True, selected_source='BYPASS', extractor_placement='NOT_EVALUATED')
    if skip_vein_present is None or (not skip_vein_present and atmosphere_present is None):
        return dict(status='UNKNOWN', passes=None, selected_source=None, extractor_placement='NOT_EVALUATED')
    name = 'special' if skip_vein_present else 'second' if atmosphere_present else 'first'
    available = dict(first=first, second=second, special=special)[name]
    if produced_pointers is None or available is None:
        return dict(status='UNKNOWN', passes=None, selected_source=name, extractor_placement='NOT_EVALUATED')
    for values in (produced_pointers, available):
        if not isinstance(values, tuple) or any(type(v) is not int or not 0 < v < 2**64 for v in values):
            raise ValueError('NONNULL_POINTER_TUPLE_REQUIRED')
    return dict(status='CONDITIONAL_RESOURCE_GATE', passes=bool(set(produced_pointers).intersection(available)),
                selected_source=name, extractor_placement='NOT_EVALUATED')


def biome_rnam_resources(biome_identity, definitions):
    """Partial BIOM RNAM -> RSGD RNAM -> IRES definition identity projection.
    Input entries must carry actual kind and ordered qualified RNAM identities,
    from independently decoded installed records in one qualified load context.
    Missing/ambiguous (None) entries do not become empty. No chance, family/RNG,
    local region generation, PNDT override or spatial biome selection is applied.
    """
    gaps, resources = [], []
    biome = definitions.get(biome_identity)
    if biome is None or biome.get('kind') != 'BIOM' or biome.get('rnam') is None:
        return dict(status='UNKNOWN', resource_occurrences=None, resource_set=None,
                    missing=[biome_identity], local_availability='NOT_EVALUATED')
    if not isinstance(biome['rnam'], tuple): raise ValueError('ORDERED_RNAM_REQUIRED')
    for generation in biome['rnam']:
        rsgd = definitions.get(generation)
        if rsgd is None or rsgd.get('kind') != 'RSGD' or rsgd.get('rnam') is None:
            gaps.append(generation); continue
        if not isinstance(rsgd['rnam'], tuple): raise ValueError('ORDERED_RNAM_REQUIRED')
        for resource in rsgd['rnam']:
            ires = definitions.get(resource)
            if ires is None or ires.get('kind') != 'IRES': gaps.append(resource)
            else: resources.append(resource)
    return dict(status='UNKNOWN' if gaps else 'CONDITIONAL_BIOM_RNAM_PROJECTION',
                resource_occurrences=None if gaps else resources,
                resource_set=None if gaps else sorted(set(resources)), missing=gaps,
                local_availability='NOT_EVALUATED')


@dataclass(frozen=True)
class ResourceOperand:
    pointer: int  # runtime VA in the one declared session; zero is null
    form_id: Optional[int]  # same-session runtime FormID; not saved token/RVA
    qualified_identity: Optional[str] = None  # independently resolved, never guessed

    def __post_init__(self):
        if type(self.pointer) is not int or not 0 <= self.pointer < 2**64:
            raise ValueError('POINTER_DOMAIN')
        if self.pointer == 0:
            if self.form_id is not None or self.qualified_identity is not None:
                raise ValueError('NULL_OPERAND_HAS_IDENTITY')
        elif type(self.form_id) is not int or not 0 <= self.form_id < 2**32:
            raise ValueError('FORM_ID_DOMAIN')
        if self.qualified_identity is not None and not self.qualified_identity.strip():
            raise ValueError('EMPTY_QUALIFIED_IDENTITY')


@dataclass(frozen=True)
class UIInputs:
    exe_sha256: str
    session: str
    evidence: str
    first: Optional[tuple[ResourceOperand, ...]]
    second: Optional[tuple[ResourceOperand, ...]]
    special: Optional[tuple[ResourceOperand, ...]]
    selector_observed: bool
    selected_form_id: Optional[int]  # observed null selector versus unobserved
    allocations_complete: Optional[bool] = None  # fold/row allocations; absent is unknown


def project_ui_rows(inputs: UIInputs) -> dict:
    """Execute the recovered final identity fold, conditional on actual operands.
    Missing ranges/selector produce UNKNOWN, never empty. Does not model row
    display fields, event timing, locking, lifetime, terrain query or eligibility.
    """
    if inputs.exe_sha256 != EXE_SHA256: raise ValueError('UNQUALIFIED_BUILD')
    if not inputs.session.strip() or not inputs.evidence.strip(): raise ValueError('PROVENANCE_REQUIRED')
    if type(inputs.selector_observed) is not bool: raise ValueError('SELECTOR_STATE')
    if not inputs.selector_observed and inputs.selected_form_id is not None:
        raise ValueError('UNOBSERVED_SELECTOR_HAS_VALUE')
    if inputs.allocations_complete is not None and type(inputs.allocations_complete) is not bool:
        raise ValueError('ALLOCATION_STATE')
    if inputs.selected_form_id is not None and (type(inputs.selected_form_id) is not int or not 0 <= inputs.selected_form_id < 2**32):
        raise ValueError('SELECTOR_FORM_ID_DOMAIN')
    missing = [name for name in ('first','second','special') if getattr(inputs, name) is None]
    if not inputs.selector_observed: missing.append('selected_special_resource')
    if inputs.allocations_complete is None: missing.append('successful_native_allocations')
    if missing:
        return dict(status='UNKNOWN', missing=missing, ui_rows=None, ui_form_set=None,
                    extractor_placement='NOT_EVALUATED')
    if not inputs.allocations_complete:
        return dict(status='INCOMPLETE_NATIVE_ALLOCATION', missing=[], ui_rows=None,
                    ui_form_set=None, extractor_placement='NOT_EVALUATED')
    for name in ('first','second','special'):
        vector = getattr(inputs, name)
        if not isinstance(vector, tuple) or not all(isinstance(v, ResourceOperand) for v in vector):
            raise ValueError('TYPED_VECTOR_REQUIRED')
    # Conflicting dereferences of one pointer invalidate the snapshot, rather
    # than silently selecting either lifetime/state.
    by_pointer = {}
    for item in inputs.first+inputs.second+inputs.special:
        if item.pointer and item.pointer in by_pointer and by_pointer[item.pointer] != item:
            raise ValueError('INCONSISTENT_POINTER_SNAPSHOT')
        by_pointer[item.pointer] = item
    merged, seen = [], set()
    for item in inputs.first+inputs.second:
        if item.pointer not in seen:
            merged.append(item); seen.add(item.pointer)
    if inputs.selected_form_id is not None:
        for item in inputs.special:
            # Native special loop dereferences each element before filtering;
            # a null special entry is invalid, not an empty valid resource.
            if not item.pointer: raise ValueError('NULL_SPECIAL_DEREFERENCE')
            if item.form_id == inputs.selected_form_id: merged.append(item)
    rows = [x for x in merged if x.pointer]
    return dict(status='CONDITIONAL_UI_PROJECTION', missing=[],
                ui_rows=[dict(pointer=x.pointer, runtime_form_id=x.form_id,
                              qualified_identity=x.qualified_identity) for x in rows],
                ui_form_set=sorted({x.form_id for x in rows}),
                extractor_placement='NOT_EVALUATED')


def compare_sets(expected, observed):
    """Caller must supply independently acquired, same-domain identity sets.
    None means unavailable ground truth; unlike an observed empty set.
    """
    if expected is None or observed is None:
        return dict(status='NOT_TESTED', exact=None, false_positives=None, false_negatives=None)
    if not isinstance(expected, (set, frozenset)) or not isinstance(observed, (set, frozenset)):
        raise ValueError('SET_REQUIRED')
    return dict(status='COMPARED', exact=expected == observed,
                false_positives=sorted(observed-expected), false_negatives=sorted(expected-observed))


def evaluate_json(request):
    """Explicit JSON contract for offline invocation; never samples the game."""
    if request.get('schema') != 'sor-resource-ui-input/1': raise ValueError('SCHEMA')
    def vector(name):
        rows = request[name]
        if rows is None: return None
        if not isinstance(rows, list): raise ValueError('VECTOR_JSON_ARRAY_REQUIRED')
        return tuple(ResourceOperand(**row) for row in rows)
    inputs = UIInputs(request['exe_sha256'], request['session'], request['evidence'],
                      vector('first'), vector('second'), vector('special'),
                      request['selector_observed'], request['selected_form_id'],
                      request.get('allocations_complete'))
    result = project_ui_rows(inputs)
    return dict(schema='sor-resource-ui-result/1', session=inputs.session,
                evidence=inputs.evidence, **result)


if __name__ == '__main__':
    import argparse
    import json
    from pathlib import Path
    ap = argparse.ArgumentParser(description='Conditional offline native UI identity fold; no terrain query or placement verdict')
    ap.add_argument('input', type=Path)
    args = ap.parse_args()
    print(json.dumps(evaluate_json(json.loads(args.input.read_text(encoding='utf8'))), indent=2, sort_keys=True))
