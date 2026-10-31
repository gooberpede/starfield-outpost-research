# SPDX-License-Identifier: GPL-3.0-or-later
"""Pin existing native evidence and installed bytes without executing game code.

Reads the installed pinned PE, owned PE reader, historical native exports and
policy/source inputs. Writes a fresh ignored site/identity receipt and an authored
CSV provenance index. No Ghidra process/database changes, target reads, save writes,
network, dependency installation, staging or Git mutation. Proprietary instruction
bytes remain exclusively in the local JSON receipt, never the authored CSV.
"""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    out = (ROOT / sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    out.mkdir(parents=True, exist_ok=False)
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    baseline = json.loads((ROOT / '.local-work/d5ab/initial.json').read_text())
    installed = {p: h for p, h in baseline['inputs'].items() if not Path(p).is_relative_to(ROOT)}
    assert all(sha(p) == h for p, h in installed.items())
    method = ROOT / 'runtime/retained-population/build.py'
    spec = importlib.util.spec_from_file_location('d5ab_owned_pe_reader', method)
    pe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pe)
    image = (pe.GAME / 'Starfield.exe').read_bytes()
    sites = [(0x79f860, 7), (0x79fa90, 8), (0x79fca3, 9), (0x79fccb, 5),
             (0x79feaf, 5), (0x79ff18, 5), (0x79b8e8, 5), (0x79ddf0, 5),
             (0x79d910, 5), (0x975030, 8), (0x9829b0, 5), (0x982b70, 5),
             (0x79dec4, 5), (0x78d6f4, 5), (0x9830cd, 12), (0x983177, 11),
             (0x79ff3e, 5), (0x79ff59, 11)]
    records = []
    for index, (rva, length) in enumerate(sites):
        window = pe.pe_read(image, rva, 32)
        record = dict(index=index, rva=hex(rva), preferred_static_va=hex(0x140000000 + rva),
                      length=length, original_bytes=window[:length].hex(),
                      guard_sha256=hashlib.sha256(window).hexdigest())
        if index in (3, 4, 5, 6, 12, 13, 16):
            assert window[0] == 0xe8
            record['call_target_rva'] = hex(rva + 5 + struct.unpack_from('<i', window, 1)[0])
        records.append(record)
    paths = [method, ROOT / 'runtime/construction-winner/observer.h',
             ROOT / '.local-work/d5v/functions/140982d90.txt',
             ROOT / '.local-work/d5v/functions/140982b70.txt',
             ROOT / '.local-work/d5v/functions/1409829b0.txt',
             ROOT / '.local-work/d5w/functions/14079f860.txt',
             ROOT / '.local-work/d5z-visited/export01/native.tsv',
             ROOT / 'docs/experiments/resource-retained-population/d5s-query-winner-model.md',
             ROOT / 'docs/experiments/resource-retained-population/d5z-report.md',
             ROOT / 'docs/experiments/resource-retained-population/d5y-report.md',
             ROOT / 'docs/experiments/resource-retained-population/d5aa-report.md',
             ROOT / 'research/resource-retained-population/d5z_append_control.py',
             ROOT / 'runtime/retained-population/protect.py',
             ROOT / 'research/resource-retained-population/prepare_native.py',
             ROOT / 'research/review_package.py',
             ROOT / 'runtime/exp0002/third_party/sfse/PluginAPI.h',
             ROOT / 'runtime/exp0002/third_party/sfse/LICENSE.txt']
    source_pins = {str(p.relative_to(ROOT)): sha(p) for p in paths}
    record = dict(schema='sor-d5ab-native-sites/1', installed=installed,
                  image_base='0x140000000', sites=records, sources=source_pins,
                  effect='Read existing exports and installed PE only; no game/native code or analysis process execution.')
    (out / 'sites.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf8', newline='\n')
    dest = ROOT / 'docs/experiments/resource-retained-population/d5ab-sources.csv'
    with dest.open('x', encoding='utf8', newline='') as stream:
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['id', 'path', 'sha256', 'use', 'eligibility'])
        for n, (path, digest) in enumerate(source_pins.items(), 1):
            private = path.startswith('.local-work/')
            purpose = 'Existing native primary evidence; no redistribution' if private else 'Owned method/source consultation or approved unchanged SFSE header; scope recorded in D5AB report'
            writer.writerow([f'D5AB-S{n:03}', path, digest, purpose, 'LOCAL-ONLY' if private else 'REVIEW-REQUIRED'])
    assert all(sha(p) == h for p, h in installed.items())
    print(json.dumps(dict(out=str(out), sites=len(records), sources=len(source_pins))))


if __name__ == '__main__':
    main()
