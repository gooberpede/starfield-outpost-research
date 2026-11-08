# SPDX-License-Identifier: GPL-3.0-or-later
"""D5BH stopped-evidence projection from exact locally retained original ZIPs.

Reads named historical ZIPs, seals, frozen prediction and local review inputs.
Writes a fresh candidate only after projecting and replaying the proof in memory.
CPython 3.14 standard library, Windows historical layout. Never extracts or
modifies originals. No live game, saved-state, process, Git or network effects.
"""
import argparse
import json
from pathlib import Path
import re
import struct
import sys
import zipfile
import zlib

import d5bh_verify as verifier
from d5ai_read_geometry import decode, loads_unique
from d5al_baseline import ANCHORS, ARCHIVE
from read_capture import decode as decode_core

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work'
OUTPUT_ROOT = LOCAL / 'd5bh'
ASSET = 'd5bh-episode-witness-v1.zip'
ARCHIVES = {
    'a': (ARCHIVE / 'episode-a.zip',
          'fe4bdbcfda8b0689e39444afbef5e9094cd78739787cc4fe2dfc7fd777bd9509',
          '852979e7d960ec0ed1a92c54c5f47a876929623a1219ed16ecc755b6cdb2ac5b', 164),
    'b': (LOCAL / 'd5al/b-live01-archive/episode-b.zip',
          '7ada51002e4311c6db49001f49e8c34b59aea6698eabbcb37473c67719ac19e5',
          '85eb157a7589a2a8f25268a5eab582bd5ce776d9d4e7aaf4490f097999e0a7fd', 107),
}
sys.path.insert(0, str(ROOT / 'runtime/session-tools'))
import archive

require, sha = verifier.require, verifier.sha


def encoded(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':')) + '\n').encode()


def pick(value, keys):
    return {key: value[key] for key in keys.split()}


def load_sources(episode):
    path, archive_pin, seal_pin, count = ARCHIVES[episode]
    seal_bytes = path.with_name('seal.json').read_bytes()
    require(sha(seal_bytes) == seal_pin, 'Original seal changed')
    seal = loads_unique(seal_bytes)
    require(seal['status'] == 'COMPLETE' and len(seal['files']) == count, 'Wrong archive procedure')
    archive.verify(path, seal, archive_pin)
    require(archive.collect(seal['roots']) == seal['files'], 'Loose original inventory changed')
    with zipfile.ZipFile(path) as packed:
        require(packed.read(archive.MANIFEST) == seal_bytes, 'Seal bytes differ from archived manifest')
        # Archive reader hashes every original member first. Re-read selected
        # operands with size/hash binding at the point of use.
        def read(name):
            raw = packed.read(name)
            require(seal['files'][name] == {'size': len(raw), 'sha256': sha(raw)},
                    'Selected original member pin changed')
            return raw

        def raw(name):
            return read(f'raw/{name}')

        copied = {f'{episode}/{name}': raw(name) for name in verifier.SESSION_FILES}
        stream = raw('events.bin')
        rows, events, padding = [], [], {}
        crc = previous = 0
        acknowledgments = {row['records']: row for row in map(loads_unique, raw('flush.jsonl').splitlines())}
        for index, offset in enumerate(range(0, len(stream), 328), 1):
            frame = stream[offset:offset + 328]
            magic, size, sequence, frame_crc = struct.unpack_from('<4I', frame)
            event = decode_core(frame[16:])
            require((magic, size, sequence) == (0x31505253, 312, index) and
                    event['sequence'] == index and len(frame) == 328 and
                    frame_crc == zlib.crc32(frame[16:]), 'Original core CRC/sequence mismatch')
            rows.append(encoded(verifier.project_event(event, padding)))
            if event['kind'] in verifier.FIELDS:
                events.append(event)
            if index in acknowledgments:
                crc = zlib.crc32(stream[previous:offset + 328], crc)
                require(crc == acknowledgments[index]['prefix_crc32'], 'Original core prefix CRC mismatch')
                previous = offset + 328
        require(previous == len(stream) and len(rows) == verifier.COUNTS[episode][0],
                'Original core extent differs')
        copied[f'{episode}/events.jsonl'] = b''.join(rows)
        projected = verifier.event_rows(rows, len(rows))
        require([verifier.project_event(row, {})['sequence'] for row in events] ==
                [row['sequence'] for row in projected], 'Projected relevant row coverage differs')
        # An opaque pad class preserves the original byte equality partition.
        original_descriptors = {row['descriptor'] for row in events if row['kind'] in (5, 6, 8)}
        new_descriptors = {row['descriptor'] for row in projected if row['kind'] in (5, 6, 8)}
        require(len(original_descriptors) == len(new_descriptors), 'Descriptor projection collapsed equality')
        for label, (group, number, pin) in verifier.CAPTURES.items():
            if group != episode:
                continue
            geometry_bytes = raw(f'geometry-{number}.bin')
            require(sha(geometry_bytes) == pin, 'Wrong original Raw2')
            geometry = decode(geometry_bytes)
            header = geometry['header']
            value, proof = verifier.reducer.envelope(
                geometry, events, verifier.PROCESSES[episode][2], verifier.TARGET, verifier.OWNER)
            holders = []
            for holder in geometry['holders']:
                resources = holder['resources']
                counts = [len(resources), sum(len(row['regions']) for row in resources),
                          sum(region['count'] for row in resources for region in row['regions'])]
                summary = pick(holder, 'source_pointer holder_pointer resource_capacity')
                summary['counts'] = counts
                summary['resources'] = []
                if holder['holder_pointer'] == proof['holder_pointer']:
                    for resource in resources:
                        item = pick(resource, 'resource collection_pointer region_capacity region_data region_storage')
                        item['regions'] = [dict(row, header=row['header'][:42] + '000000')
                                           for row in resource['regions']]
                        summary['resources'].append(item)
                holders.append(summary)
            # Retain the exact consumer query words used by qualification.
            del header['descriptor_hex']
            header['query_hex'] = header['query_hex'][:24]
            copied[f'{label}/geometry.json'] = encoded(dict(header=header, holders=holders))
            copied[f'{label}/original-receipt.json'] = raw(f'geometry-{number}.json')
            saved_name = ('notes/B0.normalized.bin' if episode == 'b' else
                          f'notes/oracle-snapshot-{number}.normalized.bin')
            normalized = read(saved_name)
            require(verifier.normalize(value) == normalized and len(normalized) == 5090,
                    'Historical normalized bytes do not match original Raw2')
            copied[f'{label}/normalized.bin'] = normalized
        originals = {
            'archive_sha256': archive_pin, 'archive_bytes': path.stat().st_size,
            'seal_sha256': seal_pin, 'sealed_payloads': count,
            'members': seal['files'],
        }
        proof_inputs = {name: loads_unique(read(f'notes/{name}')) for name in
                        ('preflight01/receipt.json', 'postflight01/receipt.json', 'approval.json')}
        label = episode + '0'
        prefix_name, prefix_pin = verifier.PREFIX_PINS[label]
        prefix_bytes = read(f'notes/receipts/{prefix_name}')
        require(sha(prefix_bytes) == prefix_pin, 'Original qualified prefix differs')
        prefix = loads_unique(prefix_bytes)
        proof_inputs['prefix'] = {
            **pick(prefix, 'state identity_sha256 snapshot_id snapshot_sha256 acknowledged_bytes raw_prefix_sha256'),
            'envelope_source': prefix['envelope']['source'],
            'envelope_frame': prefix['envelope']['frame'],
        }
        if episode == 'b':
            copied['b/geometry-request-1.json'] = raw('geometry-request-1.json')
            state = loads_unique(raw('p4-state.json'))
            record = state['geometry_request']
            owners = {}
            proof_inputs['owned_request'] = {
                **pick(state, 'identity_sha256 d5al_arms geometry_last_request'),
                'owner_class': owners.setdefault(state['owner'], len(owners)),
                'record': {
                    **pick(record, 'request_id label identity_sha256 receipt'),
                    'owner_class': owners.setdefault(record['owner'], len(owners)),
                },
            }
        return copied, originals, proof_inputs


def eligible(proof_a, proof_b):
    def projection(proof):
        raw = proof['preflight01/receipt.json']['protection']
        return {
            'definitions': {str(i): raw['definitions'][key] for i, key in enumerate(sorted(raw['definitions']))},
            'config': {str(i): raw['config'][key] for i, key in enumerate(sorted(raw['config']))},
            'installed': {str(i): raw['installed'][key]['sha256'] for i, key in enumerate(sorted(raw['installed']))},
            'save52': raw['protected_live'][raw['save52']],
        }

    first, second = (proof['preflight01/receipt.json']['protection'] for proof in (proof_a, proof_b))
    for group in ('definitions', 'config', 'installed'):
        require(first[group].keys() == second[group].keys(), 'Original starting-input key roster differs')
    require(first['save52'] == second['save52'], 'Original Save52 roster differs')
    post = proof_b['postflight01/receipt.json']
    require(post['session'] == str(Path(loads_unique(
                ARCHIVES['b'][0].with_name('seal.json').read_bytes())['roots']['raw']['path'])),
            'Postflight session differs from seal')
    freeze_path = LOCAL / 'd5ai/prediction-freeze01.json'
    freeze_bytes = freeze_path.read_bytes()
    require(sha(freeze_bytes) == ANCHORS[freeze_path], 'Original prediction freeze changed')
    freeze = loads_unique(freeze_bytes)
    for path, pin in ANCHORS.items():
        require(sha(path.read_bytes()) == pin, 'Immutable A0 or original prediction anchor changed')
    return {
        **pick(proof_b['approval.json'], 'profile steam_cloud'),
        'prefixes': {'a0': proof_a['prefix'], 'b0': proof_b['prefix']},
        'b0_owned_request': proof_b['owned_request'],
        'starting_inputs': [projection(proof) for proof in (proof_a, proof_b)],
        'postflight': {
            **pick(post, 'schema action episode process_state status protection_errors capture_errors plan_sha256 preflight_sha256'),
            'identity_sha256': post['owned_finalization']['identity_sha256'],
        },
        'freeze': pick(freeze, 'prediction_id text_version text_sha256 phase_b_results_accessed head utc'),
    }


def build(out):
    data, originals, inputs = {}, {}, {}
    for episode in ARCHIVES:
        members, originals[episode], inputs[episode] = load_sources(episode)
        data.update(members)
    prediction = ROOT / 'docs/experiments/resource-retained-population/d5ai-prediction-text-v1.md'
    data['prediction.txt'] = prediction.read_bytes()
    data['eligibility.json'] = encoded(eligible(inputs['a'], inputs['b']))
    require(data.keys() == verifier.MEMBERS, 'Wrong proposed member inventory')
    for name, raw in data.items():
        if name.endswith(('.json', '.jsonl')):
            require(not re.search(rb'(?i)[a-z]:[\\/]|users[\\/]|steamid|accountid', raw),
                    'Potential private path or account data in ' + name)
    result = verifier.verify_members(data)
    if out is None:
        return dict(result='IN_MEMORY_FEASIBILITY', **result)
    # The local seal lists paths separately. Include only pins for operands
    # actually used by the public projection.
    relevant = {
        'raw/events.bin', 'notes/approval.json', 'notes/preflight01/receipt.json',
        'notes/postflight01/receipt.json',
        *(f'raw/{name}' for name in verifier.SESSION_FILES),
    }
    for episode, original in originals.items():
        names = relevant | {f'raw/geometry-{number}.{extension}'
                            for _, (group, number, _) in verifier.CAPTURES.items() if group == episode
                            for extension in ('bin', 'json')}
        names.add('notes/receipts/' + verifier.PREFIX_PINS[episode + '0'][0])
        names.update(('notes/B0.normalized.bin', 'raw/geometry-request-1.json', 'raw/p4-state.json')
                     if episode == 'b' else
                     ('notes/oracle-snapshot-1.normalized.bin', 'notes/oracle-snapshot-2.normalized.bin'))
        original['members'] = {name: row for name, row in original['members'].items() if name in names}
    manifest = dict(
        schema=verifier.SCHEMA, originals=originals,
        members={name: {'bytes': len(raw), 'sha256': sha(raw)} for name, raw in data.items()},
        scope='Bounded original-data projection. The source-to-output audit uses authorized retained originals.',
        classification='LOCAL-ONLY candidate. Rights, exact release clearance, B6 and hosting pending.',
    )
    data['manifest.json'] = encoded(manifest)
    out.mkdir(exist_ok=False)
    target = out / ASSET
    with zipfile.ZipFile(target, 'x') as asset:
        for name, raw in sorted(data.items()):
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            asset.writestr(info, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    digest = sha(target.read_bytes())
    require(verifier.verify_members(verifier.read_zip(target, digest)) == result, 'ZIP replay differs')
    return dict(result='LOCAL_CANDIDATE', asset=ASSET, bytes=target.stat().st_size, sha256=digest,
                **result, member_count=len(data), manifest_sha256=sha(data['manifest.json']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, help='Fresh immediate child of .local-work/d5bh')
    args = parser.parse_args()
    if args.out is not None:
        require(args.out.resolve().parent == OUTPUT_ROOT.resolve() and not args.out.exists(),
                'Fresh isolated output required')
    print(json.dumps(build(args.out), indent=2))


if __name__ == '__main__':
    main()
