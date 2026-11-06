# SPDX-License-Identifier: GPL-3.0-or-later
"""Prospective D5AS target-source admission for the exact Pilot04 producer.

Read-only. Uses the project-owned D5AR decoder and D5AL/D5AQ authentication
under SOR-P-0002. The aggregate caller must separately check file publication,
startup/acquisition provenance, duplicate attempts and protected inputs.
"""

from io import BytesIO
import json
import re
from pathlib import Path
import zipfile

import d5ar_snapshot as raw
import d5ar_source_frames as frames

METHOD = 'sor-d5as-feynman-source-geometry/1'
NATIVE_BUILD = dict(
    game_version='1.16.244.0', game_exe_sha256=frames.EXE, sfse_sha256=frames.SFSE,
    plugin_sha256='207ff49ee06ab52b6cc5978247c4f45b09a41a676ab55b491fa8d7ace1acd401',
    source_lock_sha256='063117f8149060b0347ef475145c9306b49b924cf7d29fcef05216cdadb8eb24',
)
PILOT_CAPTURE_ID = 'da29fd41-c6c9-48f6-b6df-2010916aff1c'
PILOT_SESSION_ID = '7bbb78a8-a90c-48b9-bea6-c9f2ee6990b0'
PILOT_SNAPSHOT_SHA256 = '224f82e69a4a59f7758328e2ee029b450c7cca9cdf830ac5022e077a131a559e'
PILOT_ARCHIVE_SHA256 = 'fe3a7a07f9c48e60e25ce6496f88bab77280789afb41e9eccbf5b5c15363a504'
LOCAL = frames.ROOT / '.local-work/d5ar'
PILOT = LOCAL / 'pilot-vortex04-rework01'
PILOT_ARCHIVE = PILOT / 'Pilot04-operator-evidence01.zip'
PILOT_FILENAME = f'20261105T223212.279298Z_{PILOT_SESSION_ID}_{PILOT_CAPTURE_ID}.snapshot.json'
REFERENCE_BODIES = {
    'actual_a0': (4858, '7b66c2cce4b0c4c2d52a91a41d02997f12632d0c197681fcf4f21cb87bdbf653'),
    'mask0': (4966, 'bba4c877bc14d8abd3cfe36313e4cd62fd98e510dbf18441b250eacb57b942c4'),
    'mask3': (4858, '7b66c2cce4b0c4c2d52a91a41d02997f12632d0c197681fcf4f21cb87bdbf653'),
}
DEPENDENCY_PINS = {
    Path(raw.__file__): '90fc2b63b40ca48db0510745a2234b8aabd7a322c2b09baf600ef965a906ceae',
    Path(raw.geometry.__file__): '3be7937422c4f9c463c92291ce08c989f349c0321dae6a9d2a4796e33c89366e',
    Path(frames.__file__): 'ce7b86f545ef6ecc5b8c094df13108a14b104dd3a513fa7cbecc5ba301a14f3c',
    frames.ROOT / 'docs/experiments/resource-retained-population/d5ar-snapshot-schema.md':
        '2de16573080879943c2cacb125c7ac9c4405717f1cdd2194d359ec2765016549',
    frames.ROOT / 'docs/experiments/resource-retained-population/d5aq-request-mask-map.csv':
        'f637e277c0acb00c930cdbb0b42a45abb86684b75ca21aa639dc17b63d31f953',
}
# Pinned x64 producer layouts from capture.h: Holder, Resource, Region, point.
# The copier reserves for occupied records and copied words, not native capacity.
CAPTURE_STRIDES = (224, 32, 56, 16)
D5AG = frames.ROOT / '.local-work/d5ag'
D5AG_ORACLES = {
    D5AG / 'geometry01/control.json': 'b7f944d642e20e620de80799d52ebce441bcd038e8e3005b454ed8a555f9f893',
    D5AG / 'geometry02/control.json': '4f09a261f4f5a6ee202fd416cfb65feac3b0ca094a62d57672b8a93e3b5df387',
}
D5AG_VERIFICATION = D5AG / 'verify03/verification.json'
D5AG_VERIFICATION_SHA256 = 'b22611f2898fd500fd1724c460e98f2280ff4584fc215d86f3efa4f784e7fdba'


def reference_bundle():
    """Authenticate the existing A0 and fixed native inputs, plus byte domains."""
    raw.guard()
    for path, expected in DEPENDENCY_PINS.items():
        raw.require(frames.sha(path) == expected, f'Pinned dependency differs: {path.name}')
    result = frames.reference_bundle()
    wires = {}
    for key, pin in REFERENCE_BODIES.items():
        wire = frames.body_bytes(result[key + '_population'])
        raw.require((len(wire), raw.digest(wire)) == pin, f'Canonical reference differs: {key}')
        wires[key] = wire
    # The inherited authentication already checks the repeated D5AQ native
    # hosts. Rejoin their exact bodies to both earlier D5AG native oracles.
    verification_bytes = D5AG_VERIFICATION.read_bytes()
    raw.require(raw.digest(verification_bytes) == D5AG_VERIFICATION_SHA256,
                'D5AG independent verification differs')
    verification = json.loads(verification_bytes, object_pairs_hook=raw.unique_pairs)
    for path, expected in D5AG_ORACLES.items():
        data = path.read_bytes()
        raw.require(raw.digest(data) == expected == verification['inputs'][str(path)],
                    'D5AG oracle differs')
        oracle = json.loads(data, object_pairs_hook=raw.unique_pairs)
        raw.require(not oracle['errors'] and [row['low_mask'] for row in oracle['runs']] == [0, 3, 3],
                    'D5AG oracle masks or completion differ')
        for run in oracle['runs']:
            wire = frames.body_bytes(run['population'])
            raw.require(wire == wires[f"mask{run['low_mask']}"] and
                        all(row['exact_points_bounds'] for row in run['planar_model_comparison']),
                        'D5AG full body or point/bounds bridge differs')
    result['d5as_method'] = METHOD
    result['inputs'].update({str(path): digest for path, digest in
                             (DEPENDENCY_PINS | D5AG_ORACLES | {D5AG_VERIFICATION: D5AG_VERIFICATION_SHA256}).items()})
    return result


def pilot_snapshot():
    """Rejoin the exact Pilot04 final file to its sealed archive and receipts."""
    raw.guard()
    archive_bytes = PILOT_ARCHIVE.read_bytes()
    raw.require(raw.digest(archive_bytes) == PILOT_ARCHIVE_SHA256, 'Pilot04 archive differs')
    with zipfile.ZipFile(BytesIO(archive_bytes)) as archive:
        manifest = json.loads(archive.read('manifest.json'), object_pairs_hook=raw.unique_pairs)['files']
        names = archive.namelist()
        raw.require(len(names) == len(set(names)) == len(manifest) + 1 and
                    set(names) == set(manifest) | {'manifest.json'}, 'Pilot04 archive inventory differs')
        for name, pin in manifest.items():
            member = archive.read(name)
            raw.require(len(member) == pin['bytes'] and raw.digest(member) == pin['sha256'],
                        f'Pilot04 archive member differs: {name}')
        captured = archive.read('capture/' + PILOT_FILENAME)
        obs = json.loads(archive.read('preflight/capture-observation.json'))
        startup = json.loads(archive.read('preflight/startup-admission.json'))
        after = json.loads(archive.read('postflight/postflight.json'))
        packaging = json.loads(archive.read('package/packaging.json'))
        raw.require(raw.digest(archive.read('package/source-lock.json')) == NATIVE_BUILD['source_lock_sha256'],
                    'Pilot04 archived producer source lock differs')
    value, digest = raw.read_snapshot(PILOT / 'capture' / PILOT_FILENAME)
    raw.require(digest == raw.digest(captured) == PILOT_SNAPSHOT_SHA256 == obs['sha256'] ==
                after['capture_pins'][PILOT_FILENAME], 'Pilot04 snapshot join differs')
    raw.require(value['capture_id'] == PILOT_CAPTURE_ID == obs['capture_id'] == after['capture_id'] and
                value['session_id'] == PILOT_SESSION_ID == obs['session_id'] == startup['session_id'] and
                value['process'] == obs['process'] == {k: startup[k] for k in ('pid', 'creation_filetime')} and
                value['build'] == NATIVE_BUILD and
                packaging['artifacts']['SorOutpostGeometrySnapshot.dll'] == NATIVE_BUILD['plugin_sha256'] and
                packaging['artifacts']['source-lock.json'] == NATIVE_BUILD['source_lock_sha256'] and
                after['pilot_result'] == 'PASS_TECHNICAL_CAPTURE', 'Pilot04 acquisition identity differs')
    return value


def _observe(value, references, synthetic):
    raw.validate(value)
    raw.require(value['build'] == NATIVE_BUILD, 'D5AS direct-worker producer profile differs')
    role = 'SYNTHETIC' if synthetic else 'UNQUALIFIED_NATIVE'
    raw.require(value['evidence_basis'] == role, 'D5AS evidence role differs')
    context = value['capture_diagnostics']
    raw.require(value['status'] == 'COPIED_UNQUALIFIED',
                f"Producer refusal: {context['copy_status']}")
    lock = raw.geometry.uint(context['lock_state'], 32)
    raw.require(context['epoch_begin'] == context['epoch_end'] > 0 and
                bool(lock & 0xfff) and not (lock & 0xffc00000) and
                context['copy_begin_filetime'] > 0 and context['copy_end_filetime'] > 0,
                'Incomplete native reader, lifecycle or copy interval')
    owner = value['owner_context']
    before, after = owner['before'], owner['after']
    raw.require(before['complete'] and after['complete'] and before == after,
                'Incomplete or changed current owner binding')
    frames.pointer(before['manager_pointer_token'], 'runtime-pointer-')
    proc = frames.pointer(before['attached_proc_token'], 'proc-pointer-')
    raw.require(before['attached_proc_token'] == context['proc_identity_token'] and proc % 4 == 0,
                'Copy ProcGen differs from the admitted owner or is misaligned')
    body = int.from_bytes(bytes.fromhex(before['owner_formid_word']), 'little')
    raw.require(before['mode'] == 2 and body == 0x0005e0de,
                'Current owner mode or body outside the qualified Feynman frame')
    # Direct 0.2.0 never captures the older area/selection hook. Their absence
    # supplies no physical-area or historical selected-reference premise.
    outpost = value['outpost']
    raw.require(outpost['status'] == 'UNKNOWN' and outpost['reference'] is None and
                outpost['area_context'].get('operation_complete') is False and
                outpost['area_context'].get('status') == 'NOT_CAPTURED',
                'Unexpected area operation claim in a direct-worker capture')

    candidates, unreadable = [], []
    previous_index = -1
    holder_bytes, slot_bytes, region_bytes, point_bytes = CAPTURE_STRIDES
    copied_bytes = holder_bytes * len(value['sources'])
    for source in value['sources']:
        entry = source['map_entry_id']
        raw.require(re.fullmatch(r'map-entry-(0|[1-9][0-9]*)', entry),
                    'Noncanonical native map-entry token')
        index = raw.geometry.uint(int(entry.removeprefix('map-entry-')), 64)
        raw.require(index > previous_index, 'Native map-slot order differs')
        previous_index = index
        payload = source['geometry']
        raw.require(source['owning_grid'] is None and source['source_disposition'] in ('ALLOCATION_UNKNOWN', 'EMPTY'),
                    f'Unexpected direct-worker source disposition at {entry}')
        if payload is not None:
            raw.require(payload['source'] is None and payload['frame'] is None and
                        payload['generation_quality'] == 'UNKNOWN' and payload['capture']['resource_slots'] > 0,
                        f'Unexpected direct-worker geometry overlay or empty slots at {entry}')
            counts = payload['capture']
            copied_bytes += (slot_bytes * counts['resource_slots'] + region_bytes * counts['region_total'] +
                             point_bytes * counts['point_total'])
        diagnostic = source['source_diagnostics']
        key = raw.candidate_source_key(diagnostic)
        if key is None:
            unreadable.append(f"{entry} ({diagnostic['status']})")
            continue
        frames.pointer(source['allocation_id'], 'source-pointer-')
        frames.pointer(source['holder_id'], 'holder-pointer-')
        if key == frames.TARGET:
            candidates.append(source)
    raw.require(len(candidates) == 1, f'Expected one Feynman geographic source, found {len(candidates)}')
    raw.require(not unreadable, 'Unidentified resident entries may conceal a competing target: ' + ', '.join(unreadable))
    raw.require(context['required_bytes'] == copied_bytes,
                'Native required bytes contradict the represented census')
    selected = candidates[0]
    basis = frames.frame_record(selected['source_diagnostics'], f'{body:08x}')
    raw.require(basis == references['actual_a0_frame'],
                'Target descriptor, origin or coordinate basis differs from authenticated A0')
    payload = selected['geometry']
    raw.require(payload is not None and payload['capture']['point_total'] > 0,
                'Target holder has no nonempty complete geometry')
    population = payload['population']
    wire = frames.body_bytes(population)
    return dict(method=METHOD, eligible=True, role=role, selected_entry=selected['map_entry_id'],
                readable_source_count=len(value['sources']), source_frame=basis,
                body_sha256=raw.digest(wire), body_length=len(wire), geometry_counts=payload['capture'],
                historical_sampled_mask='UNKNOWN', physical_outpost_area='UNKNOWN',
                effective_generation_input_equivalence='NOT_ESTABLISHED',
                clock_adjustment_diagnostic=context['copy_end_filetime'] < context['copy_begin_filetime']), wire, population


def admit(value, references, *, synthetic=False):
    """Evaluate eligibility without reading or comparing reference bodies."""
    try:
        return _observe(value, references, synthetic)[0]
    except (ValueError, TypeError, KeyError) as error:
        return dict(method=METHOD, eligible=False, class_name='INVALID_OR_INCONCLUSIVE', reason=str(error))


def classify(value, references, *, synthetic=False):
    """Compare full admitted canonical bytes to both frozen references."""
    try:
        result, wire, population = _observe(value, references, synthetic)
    except (ValueError, TypeError, KeyError) as error:
        return dict(method=METHOD, eligible=False, class_name='INVALID_OR_INCONCLUSIVE', reason=str(error))
    mask0 = frames.body_bytes(references['mask0_population'])
    mask3 = frames.body_bytes(references['mask3_population'])
    raw.require((len(mask0), raw.digest(mask0)) == REFERENCE_BODIES['mask0'] and
                (len(mask3), raw.digest(mask3)) == REFERENCE_BODIES['mask3'],
                'Frozen canonical reference body differs')
    result['class_name'] = ('MATCH_MASK0_REFERENCE' if wire == mask0 else
                            'MATCH_MASK3_REFERENCE' if wire == mask3 else 'OTHER_QUALIFIED_GEOMETRY')
    result['canonical_body_hex'] = wire.hex()
    for key in ('mask0', 'mask3'):
        result['first_difference_from_' + key] = raw.first_field_difference(
            dict(population=population), dict(population=references[key + '_population']))
    return result
