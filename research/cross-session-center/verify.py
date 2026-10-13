# SPDX-License-Identifier: GPL-3.0-or-later
"""Independent, original stdlib-only decoding of the two sealed native captures.

Reads fixed raw records/journals, seals, build/source pins and saved audit pins.
Writes only a new ignored output directory; no native calls, dependency imports,
target access, analysis DB changes or original writes. Run from repository root.
The owned stream_save reader supplies decompression only. Selected saved fields
are read independently at pinned stream offsets; its provenance is recorded.
"""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import shutil
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
WIDS = {'f1517de43e171745': 'SOR-002', '0efca066ee4c7b9b': 'SOR-003'}
SESSIONS = {
    5: ROOT / '.local-work/native-oracle-live/session-17008-144157125',
    6: ROOT / '.local-work/position-write-history/live/session-40616-164222546',
}
NAMES5 = 'ref base extra cell world context_raw source candidate translation landscape center input_hierarchy floor_xy result block merge scale'.split()
NAMES6 = 'ref base extra cell world operand aux output'.split()


def sha(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def decode(data, version):
    """Schema offsets independently taken from C++ Event/Blob declarations."""
    size, header, stride, maximum, names = ((17768, 88, 1040, 1024, NAMES5)
        if version == 5 else (3328, 128, 400, 384, NAMES6))
    if len(data) != size:
        raise ValueError('record length')
    fields = ('sequence invocation parent qpc reference context thread kind status mxcsr last_error'
        if version == 5 else 'sequence invocation parent thread qpc site kind phase reference command result status arg0 arg1 arg2 arg3').split()
    e = dict(zip(fields, struct.unpack_from('<' + 'Q' * len(fields), data)))
    e['blobs'] = {}
    for i, name in enumerate(names):
        off = header + stride * i
        address, length, ok = struct.unpack_from('<QII', data, off)
        if length > maximum or ok not in (0, 1):
            raise ValueError('blob bounds/status')
        e['blobs'][name] = (address, data[off+16:off+16+length] if ok else None)
    return e


def blob(e, name, length=0):
    b = e['blobs'][name][1]
    if b is None or len(b) < length:
        raise ValueError('missing ' + name)
    return b


def identity(e):
    if e['status']:
        raise ValueError('incoherent identity')
    ref, base, extra = blob(e, 'ref', 0x98), blob(e, 'base', 0x2c), blob(e, 'extra', 0xa0)
    if struct.unpack_from('<I', base, 0x28)[0] != 0x2c60e9:
        raise ValueError('not ordinary beacon')
    wid = extra[0x98:0xa0].hex()
    if wid not in WIDS:
        raise ValueError('other Workshop')
    return wid, struct.unpack_from('<I', ref, 0x28)[0]


def ancestor(e, invocations, kind):
    p = invocations.get(e['parent'])
    if p is None or p['kind'] != kind or p['thread'] != e['thread'] or p['sequence'] >= e['sequence']:
        raise ValueError('missing/conflicting ancestry')
    return p


def compatible_samples(a, b):
    """A disagreement splits candidate identity; agreement never proves lifetime."""
    return all(a[k] == b[k] for k in ('session', 'pointer', 'form', 'base', 'workshop'))


def order_claim(a, b):
    if a['thread'] != b['thread']:
        return 'NO_TOTAL_NATIVE_ORDER'
    return 'SAME_THREAD_SAMPLE_ORDER' if a['qpc'] <= b['qpc'] else 'TIMESTAMP_CONFLICT'


def frame_claim(d3, own_cell, query_key):
    if d3 is None:
        return 'FLAG_UNOBSERVED'
    if not own_cell or query_key is None:
        return 'COMMON_3D_FRAME_UNPROVEN'
    return 'SAMPLED_FIELDS_ONLY_REQUIRES_SELECTED_EDGE'


def records(version):
    root = SESSIONS[version]
    size = 17768 if version == 5 else 3328
    with (root/'events.bin').open('rb') as f, (root/'records.jsonl').open('rb') as j:
        for number, line in enumerate(j, 1):
            assert line.endswith(b'\n'), 'journal tail'
            x = json.loads(line)
            assert (x['sequence'], x['offset'], x['length']) == (number, (number-1)*size, size)
            data = f.read(size)
            assert hashlib.sha256(data).hexdigest() == x['sha256'], number
            e = decode(data, version)
            assert e['sequence'] == number
            e['offset'], e['record_sha256'] = x['offset'], x['sha256']
            yield e
        assert not f.read(1), 'unjournaled raw tail'


def row(e, version, wid, boundary):
    ref = blob(e, 'ref', 0x98)
    extra = e['blobs']['extra'][1]
    out = e['blobs']['center' if version == 5 else 'output'][1]
    return dict(version=f'0.{version}.0', workshop=WIDS[wid], workshop_id=wid,
        sequence=e['sequence'], invocation=e['invocation'], parent=e['parent'],
        thread=e['thread'], qpc=e['qpc'], raw_offset=e['offset'], record_sha256=e['record_sha256'],
        raw_file=str(SESSIONS[version].relative_to(ROOT)/'events.bin'),
        boundary=boundary, call_rva='AD0C36' if version == 5 else f"{e['site']:X}",
        pointer=hex(e['reference']), form=f"{struct.unpack_from('<I',ref,0x28)[0]:08X}",
        reference_xyz=ref[0x8c:0x98].hex(), reference_values=list(struct.unpack_from('<3f',ref,0x8c)),
        compensation=extra[0x60:0x6c].hex() if extra and len(extra)>=0x6c else None,
        output_xyz=out.hex() if out is not None and len(out)==12 else None,
        d3=ref[0xd3] if len(ref)>0xd3 else None,
        own_b0=hex(struct.unpack_from('<Q',ref,0xb0)[0]) if len(ref)>=0xb8 else None,
        cell=hex(e['blobs']['cell'][0]), world=hex(e['blobs']['world'][0]),
        status=e['status'], identity_scope='sampled candidate; continuous lifetime UNPROVEN')


def run(out):
    disk = {drive: shutil.disk_usage(drive).free for drive in ('C:/', 'D:/')}
    assert min(disk.values()) >= 40_000_000_000
    out.mkdir(parents=True, exist_ok=False)
    pins = []

    def pin(p, expected=None):
        p = Path(p)
        h = sha(p)
        assert expected is None or h == expected, str(p)
        pins.append(dict(path=str(p), size=p.stat().st_size, sha256=h))

    seals = [ROOT/'.local-work/ship-relocation-050/live-20261013T031605991759Z/sealed-session-files.json',
        ROOT/'.local-work/position-write-history/run-20261013T085008190141Z/sealed-session-files.json']
    seal_hashes=['e73dbe60db556b3654831a966aababe7026fc098e158674ea556cc97e02d16a3',
        '36e41f96bcea41c49927b54d758ec3e57c56d2afdf438b334f415d68c5118b1e']
    for version, p, h in zip((5, 6), seals, seal_hashes):
        pin(p,h)
        seal = json.loads(p.read_bytes())
        entries = seal if version == 5 else [dict(path=str(SESSIONS[6]/n), **v) for n,v in seal['files'].items()]
        for item in entries:
            assert Path(item['path']).stat().st_size == item['length']
            pin(item['path'], item['sha256'])
    builds = [ROOT/'.local-work/native-oracle-050/builds/qualification-03/build.json',
        ROOT/'.local-work/position-write-history/builds/qualification-11/build.json']
    build_data = []
    build_hashes=['d7b1bf845bbdd770f1088e8d59c51409d24312fe8fdadac4b7857b0d7eaca501',
        '5aa022529772285369aca2a7cafa4be240368ed83e94f635fdfb463ea2c803a8']
    for p,h in zip(builds,build_hashes):
        pin(p,h)
        b = json.loads(p.read_bytes()); build_data.append(b)
        for name, h in b['sources'].items():
            pin(ROOT/name, h)
    assert build_data[0]['game_hash'] == build_data[1]['game_hash']
    pin('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe', build_data[0]['game_hash'])
    saved = json.loads((ROOT/'.local-work/workshop-z-restoration/saved-audit.json').read_bytes())
    for p in saved['pins'][:2]:
        pin(p['path'], p['sha256'])
    sys.path.insert(0,str(ROOT/'save-analysis/scripts'))
    from stream_save import decoded_save
    pin(ROOT/'save-analysis/scripts/stream_save.py')
    saved_fields=[]
    fields=list(csv.DictReader((ROOT/'docs/experiments/workshop-z-restoration/saved-fields.csv').open()))
    for label,p in zip(('Save25','Save26'),saved['pins'][:2]):
        with decoded_save(Path(p['path']),out/'scratch') as (b,m):
            assert m['decoded_sha256']==p['decoded_sha256']
            for x in fields:
                if x['sample']!=label:continue
                off=int(x['z_stream_offset'])-8;comp=int(x['compensation_stream_offset'])-8
                xyz=bytes(b[off:off+12]);c=bytes(b[comp:comp+12])
                assert xyz[8:].hex()==x['reference_z_hex'] and c[8:].hex()==x['compensation_z_hex']
                saved_fields.append(dict(sample=label,workshop=x['workshop_id'],xyz=xyz.hex(),compensation=c.hex(),xyz_stream_offset=off,compensation_stream_offset=comp,decoded_sha256=m['decoded_sha256']))

    all5 = list(records(5)); inv = {e['invocation']:e for e in all5 if e['kind'] in (1,7,10)}
    selected5 = []; d3_coverage = 0
    for e in all5:
        if e['kind'] != 2:
            continue
        wid, form = identity(e)
        cb = inv[e['invocation']]
        assert cb['kind'] == 1 and cb['reference'] == e['reference'] and cb['thread'] == e['thread']
        en = ancestor(cb, inv, 10); q = ancestor(en, inv, 7)
        r = row(e,5,wid,'native center return; post-call context sample')
        r['query_invocation'] = q['invocation']; r['enumeration_invocation'] = en['invocation']
        world = blob(q,'world',0x318)
        r['query_key'] = world[0x310:0x318].hex()
        r['translation_xy'] = blob(e,'translation',8)[:8].hex()
        assert r['reference_xyz'] == r['output_xyz'] and r['compensation'] == '00'*12
        for x in all5:
            for address, content in x['blobs'].values():
                if content is not None and address <= e['reference']+0xd3 < address+len(content):
                    d3_coverage += 1
        selected5.append(r)
    assert len(selected5)==40 and d3_coverage==0
    # Retrospective pointers from independently read coherent center identity.
    selected_ptrs = {0x1f7e3ea0000:'f1517de43e171745',0x1f7e3f55b20:'0efca066ee4c7b9b'}
    site_counts = collections.Counter(); selected_counts = collections.Counter()
    outputs = collections.defaultdict(collections.Counter); all_outputs=collections.defaultdict(collections.Counter)
    rows6=[]; pending={}; pairs=0; site_examples={}; selected_pair_bad=set()
    quarantine=[]; inversions=0; previous=None
    for e in records(6):
        site_counts[(e['kind'],e['site'],e['phase'])] += 1
        if previous and previous['qpc']>e['qpc'] and previous['thread']!=e['thread']:
            inversions += 1
        previous = {k:e[k] for k in ('qpc','thread')}
        key=e['invocation']; signature=tuple(e[k] for k in ('thread','site','kind','parent','reference'))
        if e['phase']==1:
            assert key not in pending
            pending[key]=signature
        else:
            assert e['phase'] in (2,3) and pending.pop(key)==signature
            pairs+=1
        if e['reference'] not in selected_ptrs:
            continue
        wid=selected_ptrs[e['reference']]
        selected_counts[(wid,e['kind'],e['phase'])]+=1
        if e['kind']==8 and e['phase']==2:
            all_outputs[wid][blob(e,'output',12).hex()]+=1
        if e['status']:
            quarantine.append(e['sequence'])
            selected_pair_bad.add(e['invocation'])
        elif e['kind']==8:
            assert identity(e)[0]==wid
            r=row(e,6,wid,'before' if e['phase']==1 else 'native center return')
            if e['phase']==2:
                outputs[wid][r['output_xyz']]+=1
                assert r['reference_xyz']==r['output_xyz'] and r['compensation']=='00'*12 and r['d3']==2
                if (wid,e['site']) not in site_examples:
                    rows6.append(r)
                    site_examples[(wid,e['site'])]=r
        if e['kind']==10:
            r=row(e,6,wid,'initial setter before' if e['phase']==1 else 'initial setter return')
            r['operand_xyz']=blob(e,'operand',12).hex();rows6.append(r)
    assert not pending and pairs==281163
    assert quarantine==[206095,321083,330833,401602]
    expected={'f1517de43e171745':'a266f542eb858843efd19241','0efca066ee4c7b9b':'0369b243f0b019457220ffc1'}
    # Incoherent identity events cannot certify arithmetic, but their output blob
    # remains available and is independently checked in the ledger below.
    for wid, triple in expected.items():
        assert set(outputs[wid])=={triple}
        assert set(all_outputs[wid])=={triple}
        assert next(x['xyz'] for x in saved_fields if x['sample']=='Save25' and x['workshop']==wid)==triple
        for r in [x for x in selected5 if x['workshop_id']==wid]:
            xy=struct.unpack('<2f',bytes.fromhex(r['reference_xyz'])[:8]);t=struct.unpack('<2f',bytes.fromhex(r['translation_xy']))
            assert struct.pack('<2f',*(xy[i]+t[i] for i in range(2))).hex()==triple[:16]
    rows=selected5+rows6
    # Context difference is reported as module identities, never a causal verdict.
    mods={}
    for v in (5,6):
        p=SESSIONS[v]/'modules-final.jsonl'
        if not p.exists(): p=SESSIONS[v]/'modules-9.jsonl'
        pin(p); mods[v]=[json.loads(line) for line in p.read_bytes().splitlines()]
    module_sets={v:{Path(x['path']).name.lower():x for x in m} for v,m in mods.items()}
    changed_modules=[]
    for name in sorted(set(module_sets[5])|set(module_sets[6])):
        a,b=module_sets[5].get(name),module_sets[6].get(name)
        if a is None or b is None or a.get('sha256')!=b.get('sha256'):
            changed_modules.append(dict(name=name,hash5=a.get('sha256') if a else None,hash6=b.get('sha256') if b else None))
    for p in sorted({ROOT/x['raw_file'] for x in rows}): pin(p)
    pin(Path(__file__))
    summary=dict(result='B candidate, subject to independent review',disk=disk,
        python=sys.version,records5=len(all5),pairs6=pairs,records6=pairs*2,
        centers5=40,coherent_return_counts6={k:dict(v) for k,v in outputs.items()},
        all_return_counts6={k:dict(v) for k,v in all_outputs.items()},incoherent_pairs6=len(selected_pair_bad),
        selected_counts=[dict(workshop=k[0],kind=k[1],phase=k[2],count=v) for k,v in sorted(selected_counts.items())],
        sites6=[dict(kind=k[0],site=f'{k[1]:X}',phase=k[2],count=v) for k,v in sorted(site_counts.items())],
        d3_coverage5=d3_coverage,quarantine6=quarantine,cross_thread_qpc_inversions6=inversions,
        module_counts={k:len(v) for k,v in mods.items()},
        changed_modules=changed_modules,saved_fields=saved_fields,
        game_hash=build_data[0]['game_hash'],sources_verified=[len(x['sources']) for x in build_data],
        limits=['identity continuity not proven','no equivalent AD0C36 occurrence in 060 unless sites6 says otherwise',
            'saved framing semantics inherited; decompression and selected fields freshly checked',
            'no noninterference proof; journal order is serialized emission order'])
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8')
    (out/'ledger.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf8')
    (out/'pins.json').write_text(json.dumps(pins,indent=2)+'\n',encoding='utf8')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True)
    run(ap.parse_args().output)
