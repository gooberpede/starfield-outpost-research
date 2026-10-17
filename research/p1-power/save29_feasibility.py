# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline Save29 writer-feasibility probe; NOT a writer.

Run from repository root with CPython -B and a fresh --run NAME. Reads the exact
prior protected-save receipts, original Save3/29, installed exe/ESM and owned
readers. Writes only exclusive .local-work/p1-save29-derivatives/NAME/ JSON and
temporary .bin decoder probes (removed on exit). Never emits .sfs candidates,
changes originals, invokes game/native/database/network tools or writes Git.
Prerequisites: the existing P1 Save29 archive and inspection, unchanged pinned
inputs, installed stdlib, >=40 GB free on C:/D:. Identity mismatch stops.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
sys.path.insert(0, str(ROOT / 'research/p1-power'))
from stream_save import decoded_save, disk_guard
from analyze_manual_corpus import decode
from saved_instances import extra_view
from extractor_resources import plugin_tables, saved_form
from outpost_membership import token_value
from outpost_record_framing import iter_records
from validate_mature_outposts import directory
from workshop_inventory import reference_prefix


def pin(path):
    path = Path(path)
    with path.open('rb') as stream:
        return dict(path=str(path), bytes=path.stat().st_size,
                    sha256=hashlib.file_digest(stream, 'sha256').hexdigest())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True)
    args = parser.parse_args()
    if not args.run.isalnum():
        raise ValueError('run must be alphanumeric')
    base = ROOT / '.local-work/p1-save29-derivatives'
    base.mkdir(exist_ok=True)
    out = base / args.run
    out.mkdir()  # exclusive, preserves every previous run
    disk_guard(out)
    prior = ROOT / '.local-work/p1-save29'
    old = json.loads((prior / 'baseline.json').read_text())
    source = json.loads((prior / 'source.json').read_text())['source']
    protected = [r for r in old['protected'] if Path(r['path']).name.startswith(('Save3_', 'Save29_'))]
    protected.append(source)
    for row in protected:
        assert pin(row['path']) == row, ('PROTECTED_MISMATCH', row['path'])
    assert source['bytes'] == 2085680
    assert source['sha256'] == 'ab28c98940b019320cda4d6a0db54c9d88b721a18fba4c6a701fbed0966b42fe'
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip()
    index = pin(ROOT / '.git/index')
    raw_container = Path(source['path']).read_bytes()
    raw, chunks = decode(raw_container)  # distinct owned whole-buffer decoder
    with decoded_save(source['path'], out / 'scratch') as (mapped, metrics):
        assert mapped[:] == raw
    assert metrics['decoded_sha256'] == 'b236f22dd601b2dab59d5640967b12ab1f4dd5b3e4aac58cfae593bf43989579'
    d = directory(raw)
    a, _ = d['regions']['reference_u32']
    forms = struct.unpack_from('<' + 'I' * d['reference_count'], raw, a + 4)
    plugins = plugin_tables(raw)
    def resolve(token):
        return saved_form(token_value(token, forms), plugins)
    expected = {'DYNAMIC:ff022841': (1300005, 1300509, 1300167, 0x840),
                'DYNAMIC:ff022917': (1300577, 1301023, 1300659, 0x840),
                'DYNAMIC:ff02294d': (1301249, 1301671, 1301324, 0x800)}
    targets = []
    record_count = 0
    for record in iter_records(raw, *d['regions']['region_R3'], d['words'][9]):
        record_count += 1
        identity = resolve(record['token'])
        if identity not in expected:
            continue
        case = 5 if not record['flags'] & 0x8000 else 6 if record['flags'] & 0x02000008 else 4 if record['flags'] & 6 else 7
        prefix = reference_prefix(raw, record, case)
        extras = extra_view(raw, record, prefix, resolve)
        tag = next(e for e in extras['extras'] if e['type'] == '9c')
        start, end, off, flags = expected[identity]
        assert (record['offset'], record['end'], tag['offset'], tag['flags']) == (start, end, off, flags)
        assert start <= off and off + 5 <= end and extras['status'] == 'COUNT_CLOSED'
        assert raw[off:off+5] == b'\x9c' + struct.pack('<I', flags)
        targets.append(dict(identity=identity, base=resolve(prefix['base_token']),
                            record=[start, end], prefix=prefix, extras=extras,
                            powered_byte_offset=off+1, mask=0x40))
    assert len(targets) == 3
    # This counterexample tests validator COVERAGE, not whether the game accepts
    # the modified field. It is deliberately never named/delivered as a save.
    probe = bytearray(raw_container)
    probe[64] ^= 1
    altered, _ = decode(probe)
    assert altered == raw
    with tempfile.TemporaryDirectory(dir=out, prefix='coverage-') as temp:
        path = Path(temp) / 'opaque-header-probe.bin'
        path.write_bytes(probe)
        with decoded_save(path, Path(temp) / 'scratch') as (mapped, probe_metrics):
            assert mapped[:] == raw
    checksum_probes = {label: dict(crc32=f'{zlib.crc32(data):08x}',
                                  adler32=f'{zlib.adler32(data):08x}')
                       for label, data in [('decoded', raw), ('physical_body', raw_container[160:]),
                                           ('header_first64', raw_container[:64]),
                                           ('size_table', raw_container[72:160])]}
    pins = json.loads((prior / 'evidence-pins.json').read_text())
    installed = []
    for row in pins[-2:]:
        current = pin(row['path'])
        assert current == row, ('INSTALLED_MISMATCH', row['path'])
        installed.append(current)
    assert all(pin(r['path']) == r for r in protected)
    assert pin(ROOT / '.git/index') == index
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip() == head
    tools = [pin(Path(__file__)), pin(sys.executable)]
    for name in ('stream_save', 'analyze_manual_corpus', 'saved_instances', 'extractor_resources',
                 'outpost_membership', 'outpost_record_framing', 'validate_mature_outposts', 'workshop_inventory'):
        tools.append(pin(importlib.util.find_spec(name).origin))
    result = dict(outcome='NO_GO_UNQUALIFIED_CONTAINER_SERIALIZATION', head=head, index=index,
                  protected=protected, installed=installed, tools=tools,
                  python=sys.version, zlib_compile=zlib.ZLIB_VERSION, zlib_runtime=zlib.ZLIB_RUNTIME_VERSION,
                  container_header_hex=raw_container[:72].hex(), metrics=metrics,
                  chunks=chunks, checksum_probes=checksum_probes,
                  targets=targets, r3_records=record_count,
                  opaque_field_probe=dict(physical_offset=64, xor_mask=1,
                                          both_readers_accept=True, decoded_equal=True,
                                          game_acceptance='NOT_TESTED', temporary_probe_removed=True),
                  candidates=[], decoded_delta_audit='NOT_APPLICABLE_NO_CANDIDATES',
                  limits=['No checksum meaning assigned to +64',
                          'Readers share format assumptions; agreement is not independent game validation',
                          'No qualified writer; opaque-field preservation/update rules unresolved',
                          'No live action or scientific restoration/recalculation result'])
    with (out / 'feasibility.json').open('x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    disk_guard(out)
    print(json.dumps(dict(outcome=result['outcome'], records=record_count, targets=len(targets),
                          streams=len(chunks), candidates=0, protected_unchanged=True)))


if __name__ == '__main__':
    main()
