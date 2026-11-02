# SPDX-License-Identifier: GPL-3.0-or-later
"""Read pinned Save52 global type 7 and explicit installed ESM joins.

Reads the pinned controlled copy, ESM, owned decoders and policy. Writes fresh
ignored receipts and structured numeric state; removes decoded scratch.
Stdlib only. No game, database, save, configuration or Git mutations.
Native-backed framing is not runtime resolution or historical scheduling.
Requires a fresh local output and --esm. Count bounds derive from remaining bytes.
Owned lineage: frozen task-local d5ad_save_pcm.py; native semantics remain in the
source ledger. Structured state remains local-only; no general save decoder claim.
"""
from pathlib import Path
import importlib.util, sys, json, struct, hashlib, argparse
R = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('dest', R / 'research/resource-retained-population/d5ad_save_destination.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def parse(s):
    pos = 0

    def take(n):
        nonlocal pos
        if n < 0 or n > len(s) - pos:
            raise ValueError('BOUNDS')
        v = s[pos:pos + n]
        pos += n
        return v

    def u32():
        return int.from_bytes(take(4), 'little')

    def count(minimum):
        v = u32()
        if v > (len(s) - pos) // minimum:
            raise ValueError('COUNT_BOUND')
        return v
    seed = u32()
    outer = count(8)
    planets = []
    for oi in range(outer):
        key = u32()
        nb = count(29)
        blocks = []
        for bi in range(nb):
            blockoff = pos
            bk = u32()
            flag = take(1).hex()
            coords = take(16).hex()
            priority = u32()
            ne = count(34)
            items = []
            for ei in range(ne):
                itemoff = pos
                quantity = u32()
                kind = take(1).hex()
                state = u32()
                ids = [take(3).hex() for _ in range(3)]
                loc = take(16).hex()
                items.append(dict(offset=itemoff, u32_a=quantity, u8=kind, u32_b=state, ids=ids, location=loc))
            blocks.append(dict(offset=blockoff, key=bk, flag=flag, coords=coords, u32=priority, items=items))
        planets.append(dict(pndt_formid=key, blocks=blocks))
    nworld = count(7)
    worlds = []
    for wi in range(nworld):
        token = take(3).hex()
        nb = count(16)
        blocks = []
        for bi in range(nb):
            key = take(8).hex()
            state = u32()
            ne = count(20)
            items = []
            for ei in range(ne):
                ids = [take(3).hex() for _ in range(2)]
                data = take(14).hex()
                items.append(dict(ids=ids, data=data))
            blocks.append(dict(key=key, u32=state, items=items))
        worlds.append(dict(world_token=token, blocks=blocks))
    xyz = take(24).hex()
    last_count_offset = pos
    first = take(1)[0]
    kind = first & 3
    if kind == 0:
        n = first >> 2
    elif kind == 1:
        n = int.from_bytes(bytes([first]) + take(1), 'little') >> 2
    elif kind == 2:
        n = int.from_bytes(bytes([first]) + take(3), 'little') >> 2
    else:
        n = u32()
    if n > (len(s) - pos) // 3:
        raise ValueError('ID_COUNT_BOUND')
    ids = [take(3).hex() for _ in range(n)]
    if pos != len(s):
        raise ValueError('TRAILING')
    return dict(pcm_seed=seed, planets=planets, worlds=worlds, xyz=xyz, final_id_count_offset=last_count_offset, final_ids=ids, consumed=pos)

def main():
    if sys.flags.optimize:
        raise ValueError('OPTIMIZATION')
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output', type=Path)
    ap.add_argument('--esm', required=True, type=Path)
    args = ap.parse_args()
    o = args.output.resolve()
    if not o.is_relative_to(R / '.local-work') or o.exists():
        raise ValueError('FRESH_LOCAL_OUTPUT')
    pins = json.loads((R / 'research/resource-carinae-source-context/save_policy.json').read_text(encoding='utf-8'))['designated']
    n = next((n for n in pins if n.startswith('Save52_')))
    p = R / '.local-work/savegames' / n
    h = m.sha(p)
    if not h == pins[n]['sha256']:
        raise ValueError("Validation failed: h == pins[n]['sha256']")
    if not p.stat().st_size == pins[n]['bytes']:
        raise ValueError("Validation failed: p.stat().st_size == pins[n]['bytes']")
    m.D5Z.guard()
    esm = args.esm.resolve()
    eh = m.sha(esm)
    if not eh == '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7':
        raise ValueError("Validation failed: eh == '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'")
    o.mkdir(parents=True)
    with m.D5Z.decoded_save(p, o / 'scratch', seconds=float('inf'), guard=m.D5Z.guard) as (b, metrics):
        a, z = m.D5Z.global_suffix(b, m.D5Z.directory(b))[7]
        s = bytes(b[a:z])
        if not s == m.D5Z.independent_slice(p, a, z - a):
            raise ValueError('Validation failed: s == m.D5Z.independent_slice(p, a, z - a)')
        result = parse(s)
        if not struct.unpack_from('<III', s) == (result['pcm_seed'], len(result['planets']), result['planets'][0]['pndt_formid']):
            raise ValueError("Validation failed: struct.unpack_from('<III', s) == (result['pcm_seed'], len(result['planets']), result['planets'][0]['pndt_formid'])")
    empty = struct.pack('<III', 123, 0, 0) + bytes(25)
    empty_result = parse(empty)
    if not (empty_result['consumed'] == len(empty) and (not empty_result['planets']) and (not empty_result['worlds']) and (not empty_result['final_ids'])):
        raise ValueError("Validation failed: empty_result['consumed'] == len(empty) and (not empty_result['planets']) and (not empty_result['worlds']) and (not empty_result['final_ids'])")
    controls = {'positive_empty': True}
    for label, bad in [('truncated', s[:-1]), ('trailing', s + b'\x00'), ('bad_count', s[:4] + b'\xff' * 4 + s[8:])]:
        try:
            parse(bad)
        except ValueError as exc:
            controls[label] = str(exc)
        else:
            raise AssertionError(label)
    keys = {row['pndt_formid'] for row in result['planets']}
    joins = []
    sftrs = []
    for rec, fields in m.esm_records(esm, {b'PNDT', b'SFTR'}, repeated=True):
        fid = rec['formid']
        if rec['type'] == 'PNDT' and fid in keys:
            edid = next((v.rstrip(b'\x00').decode() for t, v in fields if t == b'EDID'), None)
            joins.append(dict(formid=fid, edid=edid))
        if rec['type'] == 'SFTR' and fid in (1539183, 1476628):
            blocks = []
            active = None
            for tag, value in fields:
                if tag == b'BFCB':
                    active = dict(name=value.rstrip(b'\x00').decode(), fields=[])
                    blocks.append(active)
                elif tag == b'BFCE':
                    active = None
                elif active is not None:
                    active['fields'].append(dict(tag=tag.decode(), bytes=len(value), hex=value.hex() if len(value) < 1024 else None))
            sftrs.append(dict(formid=fid, offset=rec['offset'], blocks=blocks))
    if not (m.sha(p) == h and m.sha(esm) == eh):
        raise ValueError('Validation failed: m.sha(p) == h and m.sha(esm) == eh')
    stats = dict(pcm_seed=result['pcm_seed'], pndt_count=len(result['planets']), pndt_join_count=len(joins), pndt_unmatched=sorted(keys - {j['formid'] for j in joins}), content_blocks=sum((len(r['blocks']) for r in result['planets'])), content_items=sum((len(b['items']) for r in result['planets'] for b in r['blocks'])), world_count=len(result['worlds']), world_blocks=sum((len(r['blocks']) for r in result['worlds'])), world_items=sum((len(b['items']) for r in result['worlds'] for b in r['blocks'])), final_ids=len(result['final_ids']), selected_planets=[dict(formid=r['pndt_formid'], blocks=len(r['blocks']), items=sum((len(b['items']) for b in r['blocks']))) for r in result['planets'] if r['pndt_formid'] in (386266, 385246, 259489)], final_count_logical=a + result['final_id_count_offset'])
    receipt = dict(source_sha256=h, esm_sha256=eh, script_sha256=m.sha(__file__), native_sources=['swap-export07', 'swap-export09', 'swap-export10', 'swap-export11'], logical_start=a, logical_end=z, payload_sha256=hashlib.sha256(s).hexdigest(), independent_zlib_match=True, independent_struct_prefix=True, source_and_esm_unchanged=True, controls=controls, stats=stats, esm_joins=joins, sftr_records=sftrs)
    (o / 'state.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    (o / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(stats))
if __name__ == '__main__':
    main()
