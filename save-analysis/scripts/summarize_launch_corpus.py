"""Read frozen ignored scan-03; create only independent numeric review tables.

Also independently audit shortlisted physical stream lengths/alignment/checksums,
directory closure and counted string lengths. Stdlib only; no target effects.
Reads extracted sources by frozen locator; verifies identity before/after.
Writes fresh docs tables and ignored spot-check receipt. Never emits payloads.
"""
from pathlib import Path
import csv
import hashlib
import json
import struct
import zlib
import inventory_launch_corpus as launch

ROOT = launch.ROOT
SCAN = ROOT/'.local-work/third-party/the-daily-xperience-1798/scan-03'
DEST = ROOT/'docs/experiments/launch-era-third-party-corpus'
SELECTED = [13, 14, 24, 80, 1]
REASONS = [
    'Advanced level-41 empty unit; provisional negative indicators; paired with 0014',
    'Same name/version/level and nearby time as 0013; nonempty groups; branch uncertainty',
    'Distinct name label; early level-1 empty unit; observational negative calibration lead',
    'Largest observed group/endpoint profile (8/16); challenges outpost specificity',
    'RicherMerchants.esp header lead; mod-free assumption counterexample',
]


def csv_write(name, rows):
    with (DEST/name).open('x', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)


def independent(row):
    p = Path(row['source']['path'])
    if launch.inv.identity(p) != row['source']:
        raise ValueError('spot source mismatch')
    b = p.read_bytes()
    size = int.from_bytes(b[32:40], 'little')
    count = (size+262143)//262144
    pos = int.from_bytes(b[24:32], 'little')
    parts = []
    for i in range(count):
        n = int.from_bytes(b[72+4*i:76+4*i], 'little')
        dec = zlib.decompressobj()
        raw = dec.decompress(b[pos:pos+n], min(262144, size-262144*i)+1)
        if not dec.eof or dec.unused_data or dec.unconsumed_tail or len(raw) != min(262144, size-262144*i):
            raise ValueError('independent physical stream mismatch')
        parts.append(raw)
        pos = ((pos+n+15)//16)*16
    raw = b''.join(parts)
    if pos != len(b) or len(raw) != size or hashlib.sha256(raw).hexdigest() != row['decoded_sha256']:
        raise ValueError('independent size/EOF/hash mismatch')
    f = row['fingerprint']; d = f['directory']; offset = d['offset']
    words = struct.unpack_from('<10I', raw, offset)
    refs = int.from_bytes(raw[words[0]:words[0]+4], 'little')
    if words[0]+4+4*refs != words[1] or list(words) != d['words']:
        raise ValueError('independent directory mismatch')
    field = d['regions']['region_R1'][0]+4
    start = int.from_bytes(raw[field:field+4], 'little')
    strings = int.from_bytes(raw[start:start+2], 'little'); q = start+2
    for _ in range(strings):
        n = int.from_bytes(raw[q:q+2], 'little'); q += 2+n
        if q > len(raw):
            raise ValueError('independent string bound')
    if q != f['shared_strings']['end'] or strings != f['shared_strings']['count']:
        raise ValueError('independent string consumption')
    audits = launch.audit(raw, f)
    if launch.inv.identity(p) != row['source']:
        raise ValueError('spot preservation mismatch')
    return dict(id=row['inventory_id'], sha256=row['source']['sha256'], streams=count,
                decoded_sha256=row['decoded_sha256'], directory_offset=offset,
                string_count=strings, string_end=q, grammar=audits, checks='PASS')


def main():
    launch.inv.guard()
    rows = json.loads((SCAN/'inventory.json').read_text())
    DEST.mkdir(exist_ok=False)
    public = []
    labels = {}
    for row in rows:
        f = row['fingerprint']; m = row['metadata']; e = f['envelopes'][0]
        name = m['character_name']['text']
        labels.setdefault(name, f'LABEL-{len(labels)+1}')
        public.append(dict(id=row['inventory_id'], sha256=row['source']['sha256'],
            size=row['source']['size'], decoded_sha256=row['decoded_sha256'],
            decoded_size=row['framing']['declared_decoded_size'], streams=row['framing']['streams'],
            status=row['status'], version_1=m['build_strings'][0]['text'], version_2=m['build_strings'][1]['text'],
            header_word_16=m['header_word_16']['value'], character_label_group=labels[name],
            level_candidate=m['level_candidate']['value'],
            classification=row['classification'], directory_offset=f['directory']['offset'],
            r2_start=f['directory']['regions']['region_R2'][0], r2_end=f['directory']['regions']['region_R2'][1],
            r3_start=f['directory']['regions']['region_R3'][0], r3_end=f['directory']['regions']['region_R3'][1],
            string_start=f['shared_strings']['start'], string_end=f['shared_strings']['end'],
            string_count=f['shared_strings']['count'], envelope_offset=e['offset'], payload_offset=e['payload_offset'],
            payload_length=e['length'], payload_end=e['end'], consumed=e['parsed']['consumed'],
            collection_beacons=f['beacon_collection_count'], keyed_groups=f['keyed_groups'], endpoints=f['endpoints'],
            beacon_windows=f['beacon_count'], cargo_marker_windows=f['marker_count'],
            animation_entries=f['animation_string_count'], reciprocal_pairs=len(f['reciprocal_pairs']),
            richer_merchants_header_lead='RicherMerchants.esp' in row['plugin_string_leads'],
            independent_grammar_audit='PASS'))
    csv_write('manifest.csv', public)
    shortlist = []
    audits = []
    for rank, (n, reason) in enumerate(zip(SELECTED, REASONS), 1):
        sid = f'TDX1798-{n:04d}'
        row = next(r for r in rows if r['inventory_id'] == sid)
        shortlist.append(dict(rank=rank, id=sid, sha256=row['source']['sha256'], size=row['source']['size'], rationale=reason))
        audits.append(independent(row))
    csv_write('shortlist.csv', shortlist)
    launch.inv.write(SCAN/'independent-spot-checks.json', audits)
    # Verify selection-only serialization has not exposed private source paths/names.
    for p in DEST.glob('*.csv'):
        text = p.read_text()
        if any(name in text for name in labels) or 'C:\\Users' in text or '.sfs' in text:
            raise ValueError('private locator/character leak')
    print('Published review tables only:', len(public), 'rows; independent spots', len(audits))


if __name__ == '__main__':
    main()
