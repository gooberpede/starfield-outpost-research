"""Bounded descriptive S0-S7C analysis; no save editing or schema assertions.

Reads only hash-verified archived copies from manifest.json. Writes new raw
derivatives and local JSON into a caller-selected fresh directory beneath the
ignored analysis root. CPython standard library only. No process interaction.
BCPS layout is a corpus-specific empirical hypothesis validated by bounds,
zlib checksums/EOF, exact chunk lengths and complete file consumption.
Content-defined regions are analysis units, NEVER game records.
"""
from pathlib import Path
from collections import Counter
import argparse
import difflib
import hashlib
import json
import math
import re
import struct
import zlib

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '.local-work/manual-S0-S7C'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def decode(b):
    if len(b) < 72 or b[:8] != b'BCPS\x01\x00\x00\x00' or b[68:72] != b'ZIP ':
        raise ValueError('Unsupported BCPS header')
    table, start, total, block = (struct.unpack_from('<Q', b, p)[0] for p in (8, 24, 32, 48))
    if table != 72 or block != 262144 or not 0 < total <= 64 * 1024 * 1024:
        raise ValueError('Outside observed bounded layout')
    count = math.ceil(total / block)
    if table + count * 4 != start or start > len(b):
        raise ValueError('Size table bounds mismatch')
    pos, parts, chunks = start, [], []
    for i in range(count):
        size = struct.unpack_from('<I', b, table + 4 * i)[0]
        if size <= 0 or pos + size > len(b):
            raise ValueError('Chunk bounds')
        dec = zlib.decompressobj()
        raw = dec.decompress(b[pos:pos+size], block+1)
        expected = min(block, total-i*block)
        if not dec.eof or dec.unused_data or dec.unconsumed_tail or len(raw) != expected:
            raise ValueError('Chunk EOF/length mismatch')
        end = (pos+size+15)//16*16
        if end > len(b):
            raise ValueError('Padding out of bounds')
        chunks.append(dict(index=i, file_offset=pos, compressed_size=size,
                           decoded_offset=i*block, decoded_size=len(raw),
                           decoded_sha256=sha(raw), padding_hex=b[pos+size:end].hex()))
        parts.append(raw)
        pos = end
    if pos != len(b):
        raise ValueError('Unconsumed file bytes')
    raw = b''.join(parts)
    if not raw.startswith(b'SFS_SAVEGAME'):
        raise ValueError('Unexpected inner signature')
    return raw, chunks


def regions(b):
    """32-byte rolling sum, boundary low 9 bits zero, min64/max4096.

    Deliberately simple original analysis partition. Re-synchronizes after
    insertions; collisions can affect partition, not equality (SHA-256).
    """
    start, roll, result = 0, 0, []
    for i, value in enumerate(b):
        roll += value
        if i >= 32:
            roll -= b[i-32]
        n = i+1-start
        if n >= 64 and ((roll & 511) == 0 or n >= 4096):
            result.append((start, i+1, sha(b[start:i+1])))
            start = i+1
    if start < len(b):
        result.append((start, len(b), sha(b[start:])))
    return result


def hits(b, pattern):
    return [m.start() for m in re.finditer(re.escape(pattern), b)]


def compare(a, b, ra, rb):
    opcodes = difflib.SequenceMatcher(None, [r[2] for r in ra], [r[2] for r in rb], autojunk=False).get_opcodes()
    changes = []
    stable = 0
    for kind, i, j, k, l in opcodes:
        if kind == 'equal':
            stable += sum(x[1]-x[0] for x in ra[i:j])
            continue
        a0, a1 = (ra[i][0] if i < len(ra) else len(a)), (ra[j-1][1] if j > i else (ra[i][0] if i < len(ra) else len(a)))
        b0, b1 = (rb[k][0] if k < len(rb) else len(b)), (rb[l-1][1] if l > k else (rb[k][0] if k < len(rb) else len(b)))
        # Trim byte-identical edges of aligned unequal analysis regions.
        while a0 < a1 and b0 < b1 and a[a0] == b[b0]:
            a0 += 1; b0 += 1; stable += 1
        while a0 < a1 and b0 < b1 and a[a1-1] == b[b1-1]:
            a1 -= 1; b1 -= 1; stable += 1
        if a0 != a1 or b0 != b1:
            changes.append(dict(kind='insert' if a0 == a1 else 'delete' if b0 == b1 else 'replace',
                                before=[a0,a1], after=[b0,b1]))
    return dict(matched_bytes=stable, regions=changes, region_count=len(changes),
                before_unmatched_bytes=len(a)-stable, after_unmatched_bytes=len(b)-stable,
                operations=dict(Counter(x['kind'] for x in changes)))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--run', required=True); args = ap.parse_args()
    if not re.fullmatch(r'[a-zA-Z0-9_-]+', args.run):
        raise SystemExit('Use a simple fresh run name')
    out = BASE / args.run; out.mkdir(exist_ok=False)
    manifest = json.loads((BASE/'manifest.json').read_text())
    decoded, partitions, entries = [], [], []
    for s in manifest['samples']:
        p = Path(s['copy']['path']).resolve()
        if not p.is_relative_to((ROOT/'.local-work/savegames/manual-S0-S7C').resolve()):
            raise ValueError('Copy path outside authorized archive')
        b = p.read_bytes()
        if sha(b) != s['copy']['sha256']:
            raise ValueError('Copy hash mismatch')
        raw, chunks = decode(b); decoded.append(raw)
        (out/f"{s['label']}.decoded.bin").write_bytes(raw)
        r = regions(raw); partitions.append(r)
        strings = [(x.start(), x.group().decode('ascii')) for x in re.finditer(rb'[ -~]{5,}',raw)]
        (out/f"{s['label']}.strings.json").write_text(json.dumps(strings,indent=2)+'\n', encoding='utf-8')
        selected = [(p,t) for p,t in strings if re.search(r'SOR-001|Kreet|Narion|latitude|longitude|outpost|workshop|solar|harvester|7mm',t,re.I)]
        entries.append(dict(label=s['label'], source_sha256=sha(b), file_size=len(b),
                            decoded_size=len(raw), decoded_sha256=sha(raw), chunks=chunks,
                            partition_count=len(r), probes=selected,
                            rename_ascii=hits(raw,b'SOR-001'), rename_utf16le=hits(raw,'SOR-001'.encode('utf-16le'))))
    transitions=[]
    for i in range(16):
        d=compare(decoded[i],decoded[i+1],partitions[i],partitions[i+1])
        d.update(before=entries[i]['label'], after=entries[i+1]['label'],
                 classification='INCIDENTAL' if i==15 else 'CONTROL' if i%2==0 else 'ACTION',
                 file_delta=entries[i+1]['file_size']-entries[i]['file_size'],
                 decoded_delta=len(decoded[i+1])-len(decoded[i]))
        # Region persistence through next control by exact-byte search, not offset.
        if i%2 and i<15:
            next_data=decoded[i+2]
            for change in d['regions']:
                lo,hi=change['after']; segment=decoded[i+1][lo:hi]
                change['following_control_exact_hits'] = hits(next_data,segment) if 8<=len(segment)<=65536 else None
        transitions.append(d)
    output=dict(script_sha256=sha(Path(__file__).read_bytes()), zlib_runtime=zlib.ZLIB_RUNTIME_VERSION,
                manifest_sha256=sha((BASE/'manifest.json').read_bytes()), samples=entries,transitions=transitions)
    (out/'analysis.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    for d in transitions:
        print(d['before'],d['after'],d['classification'],d['file_delta'],d['decoded_delta'],d['region_count'],d['after_unmatched_bytes'])
    print('Saved',out/'analysis.json')


if __name__ == '__main__':
    main()
