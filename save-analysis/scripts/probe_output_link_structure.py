"""Post-preregistration follow-up for token remapping and entry reordering.

Reads hash-verified local L analysis and prior S3C/S4/S4C decoded streams.
Writes fresh structure.json locally; stdlib only, no live reads/target effects.
Endpoint matching uses prior main framing/base-like bytes and repeated token,
independently of the relationship lifecycle. All framing/ownership is provisional.
"""
from pathlib import Path
import json
import struct

from analyze_manual_corpus import sha, hits
from probe_manual_candidates import MAIN, TOKENS, LINK, BEACON_XYZ
from validate_output_link import OUT, PRIOR, write_json

BASE_LIKE = dict(beacon='6c60e9', storage='63aed9', extractor='45ef19', solar='6031e1')


def inspect(raw, label):
    endpoints = {}
    for role, base in BASE_LIKE.items():
        matches = []
        for base_pos in hits(raw, bytes.fromhex(base)):
            p = base_pos - 15
            if p < 0:
                continue
            token = raw[p+1:p+4]
            if (raw[p] == 0x3a and raw[p+4:p+8] == bytes.fromhex(MAIN[role])[4:8]
                    and raw[p+18:p+21] == token):
                matches.append(p)
        if len(matches) != 1:
            raise ValueError(f'Endpoint framing ambiguous/missing: {label}/{role}: {matches}')
        p = matches[0]
        token = raw[p+1:p+4]
        endpoints[role] = dict(main_offset=p, token=token.hex(),
            token_offsets=hits(raw, token), window_512_sha256=sha(raw[p:p+512]),
            first_128_hex=raw[p:p+128].hex(),
            beacon_xyz_offsets=hits(raw[p:p+512], BEACON_XYZ) if role == 'beacon' else [],
            solar_xyz_hex=raw[p+50:p+62].hex() if role == 'solar' else None)
    # Discovered narrow envelope; 0x79/0x7a are byte markers, not proven type IDs.
    envelopes = []
    for p in hits(raw, bytes.fromhex('79000000')):
        if p+8 > len(raw):
            continue
        length = struct.unpack_from('<I', raw, p+4)[0]
        end = p+8+length
        if length not in (12, 19) or raw[end:end+8] != bytes.fromhex('7a00000028000000'):
            continue
        payload = raw[p+8:end]
        if payload[:4] != b'\x04' + bytes.fromhex(endpoints['beacon']['token']):
            continue
        envelopes.append(dict(marker_offset=p, length_offset=p+4, payload_offset=p+8,
            payload_length=length, payload_hex=payload.hex(), end_offset=end,
            discriminator_offset=p+12, discriminator=payload[4],
            tail_entries_hex=[payload[i:i+7].hex() for i in range(5, len(payload), 7)]))
    if len(envelopes) != 1:
        raise ValueError(f'Envelope ambiguous/missing: {label}: {envelopes}')
    env = envelopes[0]
    edge = bytes.fromhex(endpoints['storage']['token']) + b'\x04' + bytes.fromhex(endpoints['extractor']['token'])
    remapped = b'\x04' + bytes.fromhex(endpoints['beacon']['token']) + b'\x08' + edge
    env.update(endpoint_pair_hex=edge.hex(), endpoint_pair_offsets=hits(raw, edge),
        endpoint_pair_in_payload=hits(bytes.fromhex(env['payload_hex']), edge),
        substituted_literal_offsets=hits(raw, remapped), original_literal_offsets=hits(raw, LINK))
    return dict(label=label, decoded_sha256=sha(raw), endpoints=endpoints, envelope=env)


def main():
    current = OUT / 'analysis-01'
    records = []
    for root, labels in ((PRIOR/'analysis-01', ['S3C', 'S4', 'S4C']),
                         (current, ['L0', 'L0C', 'L1', 'L1C', 'L2', 'L2C', 'exit'])):
        analysis = json.loads((root/'analysis.json').read_text())
        for label in labels:
            entry = next(x for x in analysis['samples'] if x['label'] == label)
            raw = (root/f'{label}.decoded.bin').read_bytes()
            if sha(raw) != entry['decoded_sha256']:
                raise ValueError('Decoded input hash mismatch')
            records.append(inspect(raw, label))
    write_json(OUT/'structure.json', dict(script_sha256=sha(Path(__file__).read_bytes()),
        method_status='POST_PREREGISTRATION_EXPLORATORY_STRUCTURAL_FOLLOWUP',
        samples=records))
    for r in records:
        e = r['envelope']
        print(r['label'], e['marker_offset'], e['payload_length'], e['payload_hex'],
              e['endpoint_pair_offsets'])


if __name__ == '__main__':
    main()
