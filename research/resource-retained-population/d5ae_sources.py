# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate inherited native locators and record D5AE primary inputs.

Reads owned source ledgers and exact LOCAL-ONLY exports, then writes an authored
locator CSV and a fresh local hash receipt. No game, save, Ghidra, network or
Git effects. SOR-P-0002: D5S/W/AA/AD source-ledger methods and evidence.
Native data stays local. Stop on missing function or hash mismatch. Requires
Python -E -B and the retained proprietary corpus; no download is attempted.
"""
import csv
import importlib.util
import json
from pathlib import Path
import re
import sys
import struct

from d5ad_baseline import guard, sha

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / 'docs/experiments/resource-retained-population'
FUNCTIONS = '''140593280 1407873d0 14094e3d0 140779610 140779760
14077c470 14187f9d0 14187fbd0 141898210 14059ac20 141893ee0
14078b030 14078af30 14078bc30 1407b2390 1407b30c0 1407b3aa0
1407b2880 14079c900 1407af790 14079ce00 1407b1460 1407b19f0
1407afd70 1407b1420 14079d080 1407af970 1403625e0 1407b5a00
1407b4bb0 1407a1260 14076cd40 1427e5630 1427eaf50 1427ec100
1427e6a00 1427e56d0 1427eb6b0 1428d3960 1428d2b80 1428d3b90
1428d96c0 1428d9560 1428d89b0 14076c560 1407a1940
1407b5160 14079f860 14079b520 140771f30 140478a30 1427d4be0
140478030 142339340 140982d90 140982b70 1409829b0 14079ddf0
141a278a0 141a20380 141a67830 140aed020 141429880
1427eecf0 1427e5a00 1427e5e80 1427e70e0 1427e6f40 1427e6d10
1427ec300 1403623a0 1403623b0 1427e6830 1427e6b90 1427eb030
1403623f0 1427e4950 1427ecdd0 1427e49a0 1427e6330
1402b56d0 1407b58a0 1407b55b0 1427eecc0 1406dd4f0 1406db950
1427edc20 1427e7180 140422e10 142426790 140d25a30
1424250d0 14041f4b0 140d13b80 140d14f40 142425540 1424266f0'''.split()


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    out = Path(sys.argv[1]).resolve()
    if out.exists() or not out.is_relative_to(ROOT / '.local-work/d5ae'):
        raise ValueError('Fresh task-local receipt required')
    guard()
    candidates = {}
    for name in ('d5ad-sources.csv', 'd5w-sources.csv', 'd5s-sources.csv', 'd5aa-sources.csv'):
        for row in csv.DictReader((DOC / name).read_text(encoding='utf8').splitlines()):
            va = (row.get('static_va') or row.get('preferred_va') or row.get('preferred_static_va') or row.get('locator') or '').lower().removeprefix('0x')
            if va in FUNCTIONS:
                candidates.setdefault(va, []).append((row, name))
    rows = []
    used = {}
    # Fresh exports take precedence for the specifically investigated gaps.
    fresh = {}
    for p in sorted((ROOT / '.local-work/d5ae').glob('export*/native.tsv')):
        t = p.read_text(encoding='utf8')
        if not t.endswith('END\n'):
            continue
        for m in re.finditer(r'^FUNCTION\t([^\t]+).*?^END_FUNCTION\s*$', t, re.M|re.S):
            fresh[m[1]] = dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),
                              first_line=t.count('\n',0,m.start())+1,
                              last_line=t.count('\n',0,m.end())+1, id='D5AE fresh export')
    for va in FUNCTIONS:
        if va in fresh:
            row, origin = fresh[va], 'D5AE disposable-copy export'
        else:
            available = candidates.get(va, [])
            if not available:
                raise ValueError('Missing native source: ' + va)
            row, origin = available[0]
        p = Path(row['path'])
        if not p.is_absolute():
            p = ROOT / p
        actual = used.setdefault(str(p), sha(p))
        if actual != row['sha256']:
            raise ValueError('Native source drift: ' + str(p))
        start = row.get('first_line') or row.get('line_start')
        end = row.get('last_line') or row.get('line_end')
        origin_label = '`' + origin + '`' if origin.endswith('.csv') else origin
        rows.append(dict(id=f'D5AE-N{len(rows)+1:03}',path=row['path'].replace('\\','/'),
                         sha256=actual,static_va='0x'+va,first_line=start,last_line=end,
                         origin=origin_label+': `'+row['id']+'`',use='Native boundary in D5AE maps; semantics require contextual reading',
                         eligibility='LOCAL-ONLY'))
    direct = [ROOT / '.local-work/d5ae/inputs01.json',
              ROOT / '.local-work/d5ae/baseline.json',
              ROOT / '.local-work/d5ac/d5ae-reconstruction01/summary.json',
              ROOT / '.local-work/d5ac/d5ae-reconstruction01/target.json',
              ROOT / '.local-work/d5ae/d5s-replay01/replay.json',
              ROOT / '.local-work/d5ae/incremental01.json',
              ROOT / '.local-work/d5ae/readiness01/control.json',
              ROOT / '.local-work/d5ae/append01/control.json',
              ROOT / '.local-work/d5ae/controls03/controls.json',
              ROOT / '.local-work/d5ae/rank01/control.json',
              ROOT / '.local-work/d5ad/d5ae-chronology01/chronology.json',
              ROOT / '.local-work/d5x/live/session-5ed302aea9da7dc2261163b3dd1816e670a3c2f39891f1ec8d20094afa72b3a1/events.bin']
    for i, p in enumerate(direct,1):
        rows.append(dict(id=f'D5AE-E{i:03}',path=p.relative_to(ROOT).as_posix(),sha256=sha(p),
                         static_va='',first_line='',last_line='',origin='Retained owned experiment or D5AE replay',
                         use='Identity/control evidence; see methods and tests for limits',eligibility='LOCAL-ONLY'))
    out.mkdir(parents=True)
    # Getter lacks a database function definition. Read exact PE bytes instead.
    method = ROOT / 'runtime/retained-population/build.py'
    spec = importlib.util.spec_from_file_location('d5ae_pe', method)
    pe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pe)
    exe = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Starfield.exe')
    data = exe.read_bytes()
    import hashlib
    if hashlib.sha256(data).hexdigest() != '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28':
        raise ValueError('Wrong image')
    getter = pe.pe_read(data, 0x28d1880, 16)
    if getter.hex() != '488b0561939203480540010000c3cccc':
        raise ValueError('Pool getter bytes changed')
    slots = {hex(va): hex(struct.unpack('<Q', pe.pe_read(data, va-0x140000000, 8))[0])
             for va in (0x144b3d100, 0x144b406d0)}
    if set(slots.values()) != {'0x1402b56d0'}:
        raise ValueError('Priority callback binding changed')
    receipt = out / 'priority-slots.json'
    receipt.write_text(json.dumps(dict(getter_bytes=getter.hex(), slots=slots,
        pe_reader_sha256=sha(method), executable_sha256=sha(exe)),indent=2)+'\n',encoding='utf8',newline='\n')
    rows.append(dict(id='D5AE-PE01',path=receipt.relative_to(ROOT).as_posix(),sha256=sha(receipt),
                     static_va='0x1428d1880',first_line='',last_line='',origin='Installed PE; owned build.py reader',
                     use='Getter bytes and density/layer virtual +0x18 bindings',eligibility='LOCAL-ONLY'))
    with (DOC / 'd5ae-sources.csv').open('w',encoding='utf8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)
    (out / 'sources.json').write_text(json.dumps(dict(rows=rows,script_sha256=sha(__file__),
        inventory_sha256=sha(DOC / 'd5ae-sources.csv')),indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(native_functions=len(FUNCTIONS),total=len(rows))))


if __name__ == '__main__':
    main()
