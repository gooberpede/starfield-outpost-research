# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate immutable D5AK A0 and compare a separately approved B0.

SOR-P-0002: adapts the owned D5AK independent wire oracle and reviewed D5AJ
source-Grid reducer. Reads original sealed evidence, prediction and pinned plans;
writes exclusive derivatives/receipts only on explicit offline prepare/compare.
No game/process operation, original write, deployment, network or dependency.
Independent fixed-offset geometry parsing cross-checks all represented bytes.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')
import argparse
import hashlib
import json
from pathlib import Path
import struct
import zipfile
import d5aj_reduce as reducer
import d5ai_geometry as canonical
import d5ai_episode as original
from d5ai_episode import require, sha, pinned_json
ROOT = Path(__file__).resolve().parents[2]
SESSION = ROOT / '.local-work/d5x/live/session-4da7b6b6ed99fb240b3fd380ad5000e0ba4a39d73301dbff5be919e688e28af6'
NOTES = ROOT / '.local-work/d5ak/a-live01'
ARCHIVE = ROOT / '.local-work/d5ak/a-live01-archive'
TARGET = '0:37536:20928:0029d20e'
DLL = '9df5a04ef770887b402dca7c61ee3af52f6046711fcd4e997b66922055bbe67c'
IDENTITY = '55244e50d337d4e3d594444c8c9c2e52427c0d69462bd4e6aeb46377672ea742'
NORMALIZED = '0c05d4a4c458b533d1ec7ae3acc8b34698ac48b91ff2965224e5c37ca055da96'
PREDICTION = 'aa3a5605c3724c042e3d2cd7bc71ca40c23bb46cf8016df6d4112a1b1fe56b80'
ANCHORS = {
    SESSION / 'identity.json': IDENTITY,
    SESSION / 'geometry-1.bin': '747947b097c6a22b5e047c036137c24e12a07e16787a965fab76950e4f50809a',
    NOTES / 'receipts/checkpoint-1793680114040295400.json': '48c89dacd38718828a16634536c857419ccaca9dbfc4fd31bc1926e488ae9f6a',
    ARCHIVE / 'seal.json': '852979e7d960ec0ed1a92c54c5f47a876929623a1219ed16ecc755b6cdb2ac5b',
    ARCHIVE / 'episode-a.zip': 'fe4bdbcfda8b0689e39444afbef5e9094cd78739787cc4fe2dfc7fd777bd9509',
    ROOT / 'docs/experiments/resource-retained-population/d5ai-prediction-text-v1.md': PREDICTION,
    ROOT / '.local-work/d5ai/prediction-freeze01.json': '0ecbeafbcda9f71ae9cfb4fae30a5e6713e5bc67581630dd305b4a9c5f9aaa73',
    ROOT / '.local-work/d5ai/review-prefreeze04.md': 'c7fdc7eb2c782b33a6c998582b49e75071c33f81dd7482aa382db1f2dd9af52e',
}

def geometry(data):
    require(len(data) >= 456, 'Partial geometry header')
    h = struct.unpack_from('<22Q', data)
    require(h[0] == 0x3149413544524f53 and h[1] == 2 and h[10] == 0,
            'Unsupported or unsuccessful geometry')
    require(h[16] == len(data) - 456 and h[12] <= h[11], 'Geometry size/census')
    at, totals, holders = 456, [0, 0, 0], {}
    for _ in range(h[12]):
        require(at + 40 <= len(data), 'Truncated holder')
        source, holder, capacity, count, a, b = struct.unpack_from('<4Q2I', data, at)
        at += 40
        require(source not in holders and source and holder and count <= capacity, 'Holder identity/shape')
        resources = []
        for _ in range(count):
            require(at + 40 <= len(data), 'Truncated resource')
            form, reserved, collection, regions, capacity, region_data = struct.unpack_from('<II4Q', data, at)
            at += 40
            require(not reserved and collection and regions <= capacity, 'Resource identity/shape')
            represented = []
            for ordinal in range(regions):
                require(at + 56 <= len(data), 'Truncated region')
                header = data[at:at + 24]
                count_points, capacity, point_data, address = struct.unpack_from('<4Q', data, at + 24)
                at += 56
                require(count_points <= capacity and address == region_data + ordinal * 48 and
                        struct.unpack_from('<I', header, 16)[0] == form, 'Region identity/shape')
                require(at + count_points * 16 <= len(data), 'Truncated points')
                points = data[at:at + count_points * 16]
                at += len(points)
                represented.append(dict(header=header.hex(), count=count_points, points=points.hex()))
                totals[1] += 1
                totals[2] += count_points
            resources.append(dict(resource=f'{form:08x}', regions=represented))
            totals[0] += 1
        require(len({r['resource'] for r in resources}) == len(resources), 'Duplicate resource')
        holders[source] = dict(holder=holder, resources=resources)
    require(at == len(data) and totals == list(h[13:16]), 'Complete geometry end/census')
    return dict(holders=holders, totals=totals, bytes=at, snapshot=h[3])


def normalized(source, frame, resources):
    prefix = json.dumps(source, sort_keys=True, separators=(',', ':')).encode()
    framed = json.dumps(frame, sort_keys=True, separators=(',', ':')).encode()
    result = bytearray(struct.pack('<I', len(prefix)) + prefix + struct.pack('<I', len(framed)) + framed)
    result += struct.pack('<I', len(resources))
    for resource in sorted(resources, key=lambda row: int(row['resource'], 16)):
        result += bytes.fromhex(resource['resource']) + struct.pack('<I', len(resource['regions']))
        for region in resource['regions']:
            result += bytes.fromhex(region['header'])[:21] + struct.pack('<I', region['count']) + bytes.fromhex(region['points'])
    return bytes(result)


def baseline_observation():
    """Requalify snapshot 1; never choose an observation by equal content hash."""
    for path, digest in ANCHORS.items():
        require(sha(path) == digest, 'Immutable baseline/prediction changed: ' + str(path))
    identity = canonical.load(SESSION / 'identity.json')
    require(identity['retail'] is True and identity['pid'] == 45128 and
            identity['creation_filetime'] == 134381533873950860,
            'Wrong completed retail process')
    report = reducer.inspect(SESSION, DLL, TARGET, 0x5e0de)
    found = [o for o in report['observations'] if o['envelope']['snapshot_id'] == '1']
    require(len(found) == 1, 'Initial A0 did not qualify')
    observation = found[0]
    value, proof = observation['envelope'], observation['proof']
    require(value['session_id'] == IDENTITY and proof['source']['allocation'] == 932 and
            proof['source']['birth_sequence'] == 2082 and proof['source']['publication_sequence'] == 2083 and
            proof['generation']['generate_sequence'] == 8099 and not proof['unknown_other_holders'],
            'A0 source/construction/census provenance differs')
    wire = geometry((SESSION / 'geometry-1.bin').read_bytes())
    require(wire['snapshot'] == 1 and len(wire['holders']) == 36 and wire['totals'] == [102, 2984, 7372],
            'Complete original resident-map census differs')
    # Validate every source attribution, not only the target selected by key.
    census = []
    for pointer, holder in wire['holders'].items():
        source = reducer.source_identity(report['events'], pointer, proof['header'])
        require(source['key'] and holder['holder'], 'Unattributed resident holder')
        census.append(dict(source_pointer=pointer, holder=holder['holder'], source=source))
    target = wire['holders'][proof['source']['source_pointer']]
    require(target['holder'] == proof['holder_pointer'], 'Wrong target holder')
    full = normalized(value['source'], value['frame'], target['resources'])
    require(full == canonical.normalize(value) and len(full) == 5090 and
            hashlib.sha256(full).hexdigest() == NORMALIZED, 'Complete A0 normalized bytes differ')
    certificate = canonical.load(NOTES / 'receipts/checkpoint-1793680114040295400.json')
    require(certificate['snapshot_id'] == 1 and certificate['identity_sha256'] == IDENTITY and
            certificate['snapshot_sha256'] == observation['raw_sha256'] and
            certificate['state'] == 'BASELINE_PREFIX_QUALIFIED' and
            certificate['envelope'] == value, 'Original A0 prefix certificate differs')
    raw = (SESSION / 'events.bin').read_bytes()
    require(hashlib.sha256(raw[:certificate['acknowledged_bytes']]).hexdigest() ==
            certificate['raw_prefix_sha256'], 'Original A0 prefix changed')
    return observation, full, census


def prepare(out):
    """Offline full original/archive verification and exclusive manifest creation."""
    from d5ae_baseline import guard
    guard()
    require(out.resolve().is_relative_to((ROOT / '.local-work/d5al').resolve()), 'Isolated D5AL output required')
    observation, full, census = baseline_observation()
    seal_path = ARCHIVE / 'seal.json'
    seal = canonical.load(seal_path)
    pins = {str(p): digest for p, digest in ANCHORS.items()}
    require(seal['status'] == 'COMPLETE' and len(seal['files']) == 164, 'Wrong completed archive inventory')
    with zipfile.ZipFile(ARCHIVE / 'episode-a.zip') as archive:
        require(len(archive.namelist()) == 165 and len(set(archive.namelist())) == 165 and
                set(archive.namelist()) == set(seal['files']) | {'SOR-MANIFEST.json'} and
                archive.read('SOR-MANIFEST.json') == seal_path.read_bytes(), 'Archive manifest/inventory mismatch')
        for name, row in seal['files'].items():
            root, relative = name.split('/', 1)
            path = Path(seal['roots'][root]['path']) / relative
            data = path.read_bytes()
            require(len(data) == row['size'] and hashlib.sha256(data).hexdigest() == row['sha256'] and
                    archive.read(name) == data, 'Sealed original/archive payload differs: ' + name)
            pins[str(path)] = row['sha256']
    out.mkdir(parents=True, exist_ok=False)
    normalized_path = out / 'a0.normalized.bin'
    normalized_path.write_bytes(full)
    manifest = dict(schema='sor-d5al-a0/1', session=str(SESSION), identity_sha256=IDENTITY,
                    snapshot_id=1, prediction_sha256=PREDICTION, pins=pins,
                    normalized_path=str(normalized_path.resolve()), normalized_sha256=NORMALIZED,
                    observation=observation, complete_holder_attribution=census,
                    process=reducer.process_certificate(canonical.load(SESSION / 'identity.json')),
                    scope='Completed D5AK-A initial A0 only; no Episode B observation or authorization')
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf8', newline='\n')
    return dict(state='BASELINE_AUTHENTICATED', path=str(out / 'manifest.json'),
                sha256=sha(out / 'manifest.json'), normalized_bytes=len(full), holders=len(census))


def authenticate(plan):
    """Verify the source-locked manifest and all original evidence before admission."""
    manifest = pinned_json(plan['d5al_baseline'], plan['d5al_baseline_sha256'])
    validate_binding(manifest)
    for path, digest in manifest['pins'].items():
        require(sha(path) == digest, 'Original evidence changed: ' + path)
    observation, full, census = baseline_observation()
    require(manifest['observation'] == observation and manifest['complete_holder_attribution'] == census and
            Path(manifest['normalized_path']).read_bytes() == full, 'Baseline derivative/source mismatch')
    return manifest


def validate_binding(manifest):
    """Reject alternate sessions/snapshots even when normalized bytes are equal."""
    require(manifest.get('schema') == 'sor-d5al-a0/1' and manifest.get('snapshot_id') == 1 and
            manifest.get('session') == str(SESSION) and manifest.get('identity_sha256') == IDENTITY and
            manifest.get('prediction_sha256') == PREDICTION, 'Wrong immutable A0 manifest')
    for path, digest in ANCHORS.items():
        require(manifest['pins'].get(str(path)) == digest, 'Missing original baseline anchor')
    seal = canonical.load(ARCHIVE / 'seal.json')
    expected = {str(p) for p in ANCHORS}
    for name, row in seal['files'].items():
        root, relative = name.split('/', 1)
        path = str(Path(seal['roots'][root]['path']) / relative)
        expected.add(path)
        require(manifest['pins'].get(path) == row['sha256'], 'Missing sealed original pin')
    require(set(manifest['pins']) == expected, 'Exact original evidence closure required')
    observation = manifest['observation']
    require(observation['envelope']['session_id'] == IDENTITY and
            observation['envelope']['snapshot_id'] == '1' and
            observation['raw_sha256'] == ANCHORS[SESSION / 'geometry-1.bin'] and
            observation['proof']['process_identity'] == manifest['process'] and
            manifest['process']['pid'] == 45128 and
            manifest['process']['creation_filetime'] == 134381533873950860 and
            observation['proof']['source']['allocation'] == 932 and
            observation['envelope']['source'] == dict(key=TARGET, body_formid='0005e0de') and
            manifest['normalized_sha256'] == NORMALIZED and
            canonical.normalize(observation['envelope']) == Path(manifest['normalized_path']).read_bytes() and
            sha(manifest['normalized_path']) == NORMALIZED,
            'Wrong A0 snapshot, process, source or complete normalized derivative')


def assess(before, after, lineage, executed=True, inputs_equivalent=True):
    """Pure frozen-oracle evaluation; fixture classifications are never retail results."""
    if not executed:
        return dict(prediction='NOT TESTED', observation='NOT TESTED', content_equal=None)
    if not inputs_equivalent:
        return dict(prediction='INCONCLUSIVE', observation='INCONCLUSIVE', reason='Starting inputs are not equivalent')
    a, b = before.get('proof', {}).get('process_identity'), after.get('proof', {}).get('process_identity')
    if not a or not b or (a['pid'], a['creation_filetime']) == (b['pid'], b['creation_filetime']):
        return dict(prediction='INCONCLUSIVE', observation='INCONCLUSIVE', reason='Distinct native process birth required')
    result = canonical.compare(before['envelope'], after['envelope'], lineage)
    outcome = result['outcome']
    prediction = {'REBUILT_IDENTICAL': 'CONFIRMED', 'REBUILT_DIFFERENT': 'CONTRADICTED'}.get(outcome, 'INCONCLUSIVE')
    return dict(prediction=prediction, observation=outcome, comparison=result,
                frozen_prediction_sha256=PREDICTION)


def validate_producer(identity, plan, session):
    """Pure full retail producer/site check adapted from D5AI validate_target."""
    require(Path(session).resolve().parent == Path(plan['live_root']).resolve() and
            Path(session).name == 'session-' + identity['nonce'], 'Wrong B live session namespace')
    require(identity.get('retail') is True and identity.get('schema') == 'sor-d5x/4' and
            identity.get('host_sha256') == plan['game_sha256'] and
            identity.get('sfse_sha256') == plan['sfse_sha256'] and
            identity.get('dll_sha256') == plan['dll_sha256'] and
            Path(plan['process_image']).name == 'Starfield.exe', 'Exact retail game/SFSE/B producer required')
    require(len(identity['sites']) == len(plan['sites']) == 18, 'All base sites required')
    for observed, pinned in zip(identity['sites'], plan['sites']):
        require(observed['index'] == pinned['index'] and observed['rva'] == pinned['rva'] and
                observed['guard_sha256'] == pinned['guard_sha256'] and
                observed['va'] == identity['module_base'] + pinned['rva'], 'B lifecycle site mismatch')
    original.validate_geometry_plan(identity, plan)


def validate_capture_binding(session, identity_hash, observation):
    """Bind the sole native request to the owned B0 label and flushed receipt."""
    state = original.strict_session_json(Path(session) / 'p4-state.json')
    record = state['geometry_request']
    receipt = original.strict_session_json(Path(session) / 'geometry-request-1.json')
    require(state['identity_sha256'] == identity_hash and state['d5al_arms'] == {'B0': 1} and
            state['geometry_last_request'] == 1 and record['request_id'] == 1 and
            record['label'] == 'B0' and record['identity_sha256'] == identity_hash and
            record['owner'] == state['owner'] and
            observation['proof']['header']['request'] == 1 and
            receipt['request_id'] == receipt['snapshot_id'] == 1 and
            receipt['identity_sha256'] == identity_hash and receipt['flushed'] is True and
            receipt['sha256'] == observation['raw_sha256'] and record['receipt'] == receipt,
            'Initial B0 owned arm/request/capture binding differs')


def postflight_eligible(value, args, plan, identity_hash):
    """Forecast eligibility follows the already-required full protected postflight."""
    return (value.get('schema') == 'sor-d5ai-postflight/1' and value.get('episode') == 'B' and
            value.get('session') == str(args.session) and value.get('plan_sha256') == plan['plan_sha256'] and
            value.get('preflight_sha256') == args.preflight_sha256 and
            value.get('process_state') == 'EXITED' and value.get('status') == 'PASS_POSTFLIGHT' and
            value.get('protection_errors') == [] and value.get('capture_errors') == [] and
            value.get('owned_finalization', {}).get('identity_sha256') == identity_hash)


def compare(args, plan):
    """Read stopped B and actual approval/preflight; do not manufacture qualification."""
    import d5al_stop as trusted
    baseline = authenticate(plan)
    require(getattr(args, 'before_snapshot', '1') in ('1', 1) and
            getattr(args, 'after_snapshot', '1') in ('1', 1), 'Only A0=1/B0=1 comparison is permitted')
    preflight = pinned_json(args.preflight, args.preflight_sha256)
    preflight['receipt_sha256'] = args.preflight_sha256
    approval = pinned_json(args.approval, args.approval_sha256)
    postflight = pinned_json(args.postflight, args.postflight_sha256)
    identity = canonical.load(args.session / 'identity.json')
    trusted.distinct(identity, plan, sha(args.session / 'identity.json'))
    trusted.authority(plan, preflight, approval, args.session, sha(args.session / 'identity.json'))
    validate_producer(identity, plan, args.session)
    try:
        report = reducer.inspect(args.session, plan['dll_sha256'], TARGET, 0x5e0de)
    except (ValueError, KeyError, TypeError, OSError) as error:
        return dict(state='COMPARISON_REPORTED', prediction='INCONCLUSIVE', observation='INCONCLUSIVE',
                    reason=str(error), integrity_qualified=False,
                    scope='Preserved failed B intake; no clean terminal or second attempt inferred')
    require(len(report['observations']) + len(report['refused']) == 1, 'Exactly one initial B0 capture required')
    found = [o for o in report['observations'] if o['envelope']['snapshot_id'] == '1']
    if len(found) != 1:
        return dict(state='COMPARISON_REPORTED', prediction='INCONCLUSIVE', observation='INCONCLUSIVE',
                    refused=report['refused'], reason='Initial B0 did not qualify')
    before, after = baseline['observation'], found[0]
    validate_capture_binding(args.session, sha(args.session / 'identity.json'), after)
    lineage = reducer.relation(before, after, [], report['events'], report['lifetime'])
    first_inputs = canonical.load(NOTES / 'preflight01/receipt.json')['protection']
    current_inputs = preflight['protection']
    mismatches = []
    for group in ('definitions', 'config'):
        if first_inputs[group] != current_inputs[group]:
            mismatches.append(group)
    for name, row in first_inputs['installed'].items():
        if current_inputs['installed'].get(name, {}).get('sha256') != row['sha256']:
            mismatches.append(name)
    save = first_inputs['save52']
    if (current_inputs['save52'] != save or
            current_inputs['protected_live'].get(save) != first_inputs['protected_live'][save] or
            approval.get('profile') != 'Starfield - SFSE' or approval.get('steam_cloud') != 'DISABLED'):
        mismatches.append('save52/profile/cloud')
    if not postflight_eligible(postflight, args, plan, sha(args.session / 'identity.json')):
        mismatches.append('full-protected-postflight')
    result = assess(before, after, lineage, inputs_equivalent=not mismatches)
    return dict(state='COMPARISON_REPORTED', result=result, before=before, after=after,
                certificate=lineage, refused=report['refused'],
                input_equivalence_mismatches=mismatches,
                qualified_geometry_comparison=canonical.compare(before['envelope'], after['envelope'], lineage),
                authority='No retry, extra query or further episode authority')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(prepare(args.prepare), indent=2))


if __name__ == '__main__':
    main()


