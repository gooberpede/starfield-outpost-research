# SPDX-License-Identifier: GPL-3.0-or-later
"""BM2 read-only evidence verification, CPython stdlib and owned ESM framing.

Run from repo root with -B and --run <fresh label>. Reads pinned BM2 receipts,
installed EXE/ESM/add-on/Interface.ba2, protected existing analysis files, authored
CSVs and prior owned UI derivatives. Writes one exclusive ignored JSON receipt.
No game/native/Flash execution, save/database/config/index changes or network.
Both-drive 40GB guard applies. Checks bytes and scoped structural/numeric claims;
it is not an independent semantic oracle, load-order merger or runtime test.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import re
import struct
import subprocess
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '.local-work/build-catalogue'
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inventory_historical_saves import guard
from inspect_outpost_definitions import subrecords


def pin(path):
    path = Path(path)
    with path.open('rb') as f:
        return dict(path=str(path), bytes=path.stat().st_size,
                    sha256=hashlib.file_digest(f, 'sha256').hexdigest())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    args = ap.parse_args()
    assert re.fullmatch('[a-zA-Z0-9-]+', args.run)
    out = BASE / ('verification-' + args.run + '.json')
    assert not out.exists()
    guard()
    baseline = json.loads((BASE / 'baseline.json').read_text(encoding='utf8'))
    checks = []

    def check(ok, label):
        assert ok, label
        checks.append(label)

    for expected in baseline['protected'] + [baseline['brief'], baseline['index']]:
        check(pin(expected['path']) == expected, 'protected identity ' + expected['path'])
    check(subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == baseline['head'], 'HEAD unchanged')
    check(not subprocess.check_output(['git', 'diff', '--cached', '--name-only']), 'no staged changes')
    inv = json.loads((BASE / 'definitions.json').read_text(encoding='utf8'))
    source = Path(inv['source']['path'])
    check(pin(source) == inv['source'], 'main ESM source identity')
    by = {r['formid']: r for r in inv['records']}

    def fields(r, k):
        return [bytes.fromhex(v) for t, v in r['fields'] if t == k]

    def field(r, k):
        a = fields(r, k)
        assert len(a) <= 1
        return a[0] if a else b''

    def ids(r, k='LNAM'):
        return [i[0] for b in fields(r, k) for i in struct.iter_unpack('<I', b)]

    def number(r, k):
        return int.from_bytes(field(r, k), 'little')

    def reread(src, records):
        with src.open('rb') as f:
            for r in records:
                f.seek(r['offset'])
                h = f.read(24)
                n, flags, fid = struct.unpack_from('<III', h, 4)
                check((h[:4].decode(), flags, fid) == (r['type'], r['flags'], r['formid']), 'physical header ' + str(src.name) + ':' + f'{fid:08x}')
                assert n <= 16 * 1024 * 1024
                b = f.read(n)
                if flags & 0x40000:
                    size = int.from_bytes(b[:4], 'little')
                    assert size <= 16 * 1024 * 1024
                    d = zlib.decompressobj()
                    b = d.decompress(b[4:], size + 1)
                    assert len(b) == size and d.eof and not d.unused_data and not d.unconsumed_tail
                check([(k.decode(), v.hex()) for k, v in subrecords(b)] == [tuple(x) for x in r['fields']], 'ordered physical fields ' + src.name + ':' + f'{fid:08x}')

    # All selected physical records, not just a few named examples.
    reread(source, inv['records'])
    check(sum(r['type'] == 'COBJ' for r in inv['records']) == inv['counts']['COBJ'] == 3009, 'complete physical COBJ inventory')
    cats = ids(by[0x58606])
    check(len(cats) == 15 and number(by[0x58607], 'DATA') == 0x58606, 'root default and ordered 15 category positions')
    roots = [r for r in by.values() if r['type'] == 'COBJ' and ids(r, 'FNAM') and ids(r, 'FNAM')[0] in cats and not r['flags'] & 0x20]
    check(len(roots) == 204, 'first-FNAM physical root qualification')
    graph = json.loads((BASE / 'graph02.json').read_text(encoding='utf8'))
    reached = set()

    def walk(i, stack=()):
        check(i not in stack, 'acyclic selected CNAM/FLST path ' + f'{i:08x}')
        if i in reached or i not in by:
            return
        reached.add(i)
        r = by[i]
        if r['type'] == 'COBJ':
            walk(number(r, 'CNAM'), (*stack, i))
        elif r['type'] == 'FLST':
            for j in ids(r):
                walk(j, (*stack, i))

    for r in roots:
        walk(r['formid'])
    closure = [by[i] for i in reached if by[i]['type'] == 'COBJ']
    check(len(closure) == graph['reached_cobj'] == 545, 'recipe closure with explicit selected-type terminals')
    vocab = {struct.unpack_from('<H', b, 8)[0] for r in closure for b in fields(r, 'CTDA')}
    check(vocab == {0x3b, 0x4a, 0x21f, 0x338, 0x35a, 0x36a}, 'bounded direct COBJ condition vocabulary')
    check(number(by[0x296338], 'CNAM') == 0x296339 and len(ids(by[0x296339])) == 35, 'chair grouped list')
    check(number(by[0x2951f9], 'CNAM') == 0x259f5c and len(ids(by[0x259f5c])) == 4, 'sleeping bag list')
    check(number(by[0x293ad1], 'CNAM') == 0x293ae0 and len(ids(by[0x293ae0])) == 27, 'small table list')
    check(all(by[i]['flags'] & 0x4000000 for i in (0x296338, 0x2951f9, 0x293ad1)), 'group preservation flags')
    check(0x100c57 in ids(by[0x296339]) and not fields(by[0x100c57], 'FNAM') and number(by[0x100c57], 'CNAM') == 0x12a735, 'non-root chair child recipe')
    for i, k, operand in ((0x2331e3, 0x36a, 0x389f13), (0x636e8, 0x21f, 0x23f810), (0x6d72e, 0x4a, 0x6d73d), (0x3023d, 0x35a, 0x295eaa)):
        check(any(struct.unpack_from('<H', b, 8)[0] == k and int.from_bytes(b[12:16], 'little') == operand for b in fields(by[i], 'CTDA')), 'condition control ' + f'{i:08x}')
    check(len(fields(by[0x23baa6], 'CTDA')) == 3 and all(b[0] & 1 for b in fields(by[0x23baa6], 'CTDA')), 'Armillary three OR stage entries')
    check(not fields(by[0x299547], 'CTDA') and not fields(by[0x299547], 'JNAM'), 'unlocked unquotaed storage control')
    # Recheck the installed add-on control rather than assuming its old source pin.
    addon = json.loads((ROOT / '.local-work/sd2-shared/definitions01.json').read_text(encoding='utf8'))
    addon_pin = addon['addon_source']
    check(pin(addon_pin['path']) == addon_pin, 'SD2 add-on current installed identity')
    selected = [r for r in addon['addon_records'] if r['formid'] in (0x0102af79, 0x0102af77)]
    check(len(selected) == 2, 'two add-on primary controls')
    reread(Path(addon_pin['path']), selected)
    recipe = next(r for r in selected if r['type'] == 'COBJ')
    check(len(fields(recipe, 'CTDA')) == 3 and all(b[0] == 0 for b in fields(recipe, 'CTDA')), 'shared-storage compound AND condition bytes')
    # Actual source-derived floating arithmetic, rounding after every native op.
    f32 = lambda x: struct.unpack('<f', struct.pack('<f', x))[0]
    bits = lambda x: struct.pack('<f', x).hex()
    def props(r):
        return {i: v for i, v, tail in struct.iter_unpack('<IfI', field(r, 'PRPS'))}
    def global_seconds(ires):
        gid = number(by[ires], 'NAM3')
        return gid, f32(struct.unpack('<f', field(by[gid], 'FLTV'))[0] * 3600)
    alkprops = props(by[0x20a8b4])
    alk = [r for r in by.values() if r['type'] == 'IRES' and number(r, 'NAM1') in alkprops and 'Alkanes' in r['edid']]
    check(len(alk) == 1, 'atmospheric Alkanes typed IRES/property join')
    examples = [(0x5ef19, 0x57c7, False), (0x20a8b4, alk[0]['formid'], False), (0x2965f7, 0x777e6, True), (0x27319f, 0x245775, False)]
    numeric = []
    total = 0.0
    check(struct.unpack('<f', field(by[0x8407], 'NAM0'))[0] == 1, 'HarvesterRateMult default 1')
    for base, resource, configured in examples:
        p = props(by[base])
        av = number(by[resource], 'NAM1')
        check(av in p, 'example supports resource ' + f'{base:08x}')
        q = 1.0 if configured else p[av]
        check(q == 1 and (p[av] == 0 if configured else p[av] == 1), 'explicit selection baseline ' + f'{base:08x}')
        gid, seconds = global_seconds(resource)
        mult = f32(1.0 + p.get(0x8407, 0))
        interval = f32(seconds * mult)
        rate = f32(f32(60.0 / interval) * q)
        total = f32(total + rate)
        numeric.append(dict(base=f'{base:08x}',ires=f'{resource:08x}',av=f'{av:08x}',global_id=f'{gid:08x}',base_seconds=seconds,multiplier=mult,interval=interval,rate=rate,rate_bits_le=bits(rate),cumulative=total,cumulative_bits_le=bits(total),configured_example=configured))
    check([r['interval'] for r in numeric] == [36,108,36,f32(7.92)], 'four definition-grounded different-interval terms')
    # Rebind important native float constants and vtable pointers to the real PE.
    exe = Path(next(p['path'] for p in baseline['protected'] if p['path'].endswith('Starfield.exe')))
    blob = exe.read_bytes()
    pe = struct.unpack_from('<I', blob, 60)[0]
    n = struct.unpack_from('<H', blob, pe+6)[0]
    opt = struct.unpack_from('<H', blob, pe+20)[0]
    secs = [struct.unpack_from('<8sIIII',blob,pe+24+opt+i*40) for i in range(n)]
    def raw(va, length):
        for _,_,rva,size,off in secs:
            if rva <= va-0x140000000 < rva+size-length+1:
                p = off+va-0x140000000-rva
                return blob[p:p+length]
        raise ValueError('not file backed')
    check(struct.unpack('<f',raw(0x144f04c30,4))[0] == 60, 'native 60f constant')
    check(struct.unpack('<f',raw(0x144f04f78,4))[0] == 3600, 'native 3600f constant')
    check(struct.unpack('<Q',raw(0x144c24a20,8))[0] == 0x140f4cc70, 'real PE grouped-node visitor vtable')
    for p in sorted((BASE/'native').glob('*.request')):
        check(p.with_name(p.name+'.done').exists(), 'completed export '+p.name)
        text = p.with_name(p.name+'.tsv').read_text(encoding='utf8')
        check('SHA256\t'+baseline['protected'][2]['sha256'] in text and 'BASE\t140000000' in text, 'native imported source identity '+p.name)
    for name, tokens in [('001.request.tsv',['VDIVSS','VMULSS','1421f3839\tVADDSS','1421f383e\tVMOVSS','FUN_140f7cb70']),('008.request.tsv',['>> 0x1a & 1','WorkshopMenuNodeBuildableObject']),('006.request.tsv',['140a0239b\tADD RCX,0x150']),('017.request.tsv',['KeywordOutpostCargoLinkReservedTarget_DO','KeywordOutpostCargoLinkTarget_DO','WorkshopItem']),('019.request.tsv',['"aObjectVariants"','"aBuildRequirements"','"sOutpostLocation"'])]:
        text = (BASE/'native'/name).read_text(encoding='utf8')
        for token in tokens:
            check(token in text,'native selected-operation locator '+name+':'+token)
    ui = json.loads((BASE/'ui.json').read_text(encoding='utf8'))
    check(pin(ui['archive']['path']) == ui['archive'], 'installed interface archive unchanged')
    with Path(ui['archive']['path']).open('rb') as f:
        for asset in ui['assets']:
            for k in ('swf','abc','uncompressed'):
                check(pin(asset[k]['path']) == asset[k], 'UI derivative pin '+k+':'+asset['member'])
            # Read current original archive entry directly using its pinned header.
            f.seek(32+asset['archive_index']*36)
            entry=f.read(36)
            off,packed,size=struct.unpack_from('<QII',entry,16)
            f.seek(off);data=f.read(packed or size)
            data=zlib.decompress(data) if packed else data
            check(data == Path(asset['swf']['path']).read_bytes(), 'fresh archive member equality '+asset['member'])
            swf=Path(asset['uncompressed']['path']).read_bytes()
            for block in json.loads(Path(asset['abc']['path']).read_text(encoding='utf8')):
                for body in block['bodies']:
                    code=bytes.fromhex(body['code_hex']);p=block['swf_abc_offset']+body['abc_code_offset']
                    check(swf[p:p+len(code)] == code,'ABC body span '+asset['member']+':'+str(body['method']))
    for name in ('definitions.csv','categories.csv'):
        with (ROOT/'docs/experiments/build-catalogue'/name).open(encoding='utf8',newline='') as f:
            for row in csv.DictReader(f):
                i=int(row.get('formid',row.get('id')),16)
                check(i in by, 'authored definition identity '+name+':'+f'{i:08x}')
                if 'physical_offset' in row:
                    check(int(row['physical_offset']) == by[i]['offset'] and row['editorid'] == by[i]['edid'], 'authored physical locator '+f'{i:08x}')
    check(pin(source) == inv['source'] and pin(addon_pin['path']) == addon_pin, 'ESM originals unchanged after rereads')
    guard()
    result=dict(status='PASS',checks=len(checks),check_labels=checks,physical_records_reread=len(inv['records'])+len(selected),root_recipes=len(roots),reached_cobj=len(closure),numeric_example=numeric,total=total,total_bits_le=bits(total),ui_method_spans=sum(x['all_method_spans_verified'] for x in ui['assets']),script=pin(Path(__file__)),extra_protected_inputs=[addon_pin,ui['archive']],limits=['Byte equality and selected structural/numeric checks; not a semantic or runtime oracle','No save read, current menu snapshot, override merger or throughput measurement'])
    out.open('x',encoding='utf8',newline='\n').write(json.dumps(result,indent=2)+'\n')
    print('PASS',len(checks),'checks;',result['physical_records_reread'],'records;',result['root_recipes'],'roots;',result['reached_cobj'],'reachable COBJ; total',total)


if __name__ == '__main__':
    main()
