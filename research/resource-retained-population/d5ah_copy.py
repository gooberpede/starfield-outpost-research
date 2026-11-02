# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise native deep-copy failures in a disposable D5AH Python process.

SOR-P-0002: adapts authenticated D5S native_probe.py private-page harness.
Reads retained metadata, installed PE and pinned D5S methods; writes only fresh
ignored receipts. Uses supplied allocators, including deliberate failures.
No retail process, save, database, observer, network or Git mutation. Requires
Windows x64 CPython; stop on inherited identity/disk/ABI/callback failure.
Process exit releases private mappings. The parent retains exit and fault logs.
"""
from pathlib import Path
import csv
import hashlib
import json
import os
import subprocess
import sys

from d5ae_baseline import guard

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def child(out):
    sys.path.insert(0, str(out))
    source = (out / 'native_probe.py').read_text().split('receipt=json.loads')[0]
    source = source.replace('fail_alloc=False;fail_append=False',
                            'fail_alloc=False;fail_append=False;fail_point_after=None')
    source = source.replace('if fail_append:return 0xffffffff',
                            'if fail_append or (fail_point_after is not None and stride == 16 '
                            'and C.c_uint32.from_address(v).value >= fail_point_after):return 0xffffffff')
    ns = {'__file__': str(out / 'native_probe.py'), '__name__': 'd5ah_native_copy'}
    exec(compile(source, 'owned-D5S-probe-prefix', 'exec'), ns)
    C = ns['C']
    points = (C.c_float * 8)(1, 2, 3, 4, 5, 6, 7, 8)
    region = C.create_string_buffer(48)
    C.memmove(C.addressof(region), points, 16)
    C.c_uint32.from_buffer(region, 16).value = 0x57d4
    C.c_uint8.from_buffer(region, 20).value = 3
    C.c_uint32.from_buffer(region, 24).value = 2
    C.c_uint32.from_buffer(region, 28).value = 2
    C.c_void_p.from_buffer(region, 32).value = C.addressof(points)
    original = bytes(points)
    rows = []
    keep = []
    for name in ('success', 'outer-append-fails', 'inner-reserve-fails', 'inner-partial-copy'):
        ns['fail_alloc'] = name == 'inner-reserve-fails'
        ns['fail_append'] = name == 'outer-append-fails'
        ns['fail_point_after'] = 1 if name == 'inner-partial-copy' else None
        collection = C.create_string_buffer(16)
        # Preallocate only the outer region vector so the inner failure is isolated.
        outer = C.create_string_buffer(48)
        C.c_uint32.from_buffer(collection, 4).value = 1
        C.c_void_p.from_buffer(collection, 8).value = C.addressof(outer)
        keep.extend((collection, outer))
        index = ns['region_append'](C.addressof(collection), C.addressof(region))
        count = C.c_uint32.from_buffer(collection).value
        n = C.c_uint32.from_buffer(outer, 24).value if count else 0
        pointer = C.c_void_p.from_buffer(outer, 32).value if count else None
        copied = C.string_at(pointer, n * 16) if n else b''
        expected_index = 0xffffffff if name == 'outer-append-fails' else 0
        expected_n = {'success': 2, 'outer-append-fails': 0,
                      'inner-reserve-fails': 0, 'inner-partial-copy': 1}[name]
        assert index == expected_index and n == expected_n
        assert copied == original[:n * 16]
        if n:
            assert pointer != C.addressof(points)
        rows.append(dict(case=name, outer_index=index, outer_count=count,
                         copied_points=n, point_bytes=copied.hex(),
                         complete=n == 2, native_outer_success=index != 0xffffffff))
    # Verify deep ownership after mutating only the synthetic source allocation.
    success_points = C.c_void_p.from_buffer(keep[1], 32).value
    points[0] = 999
    assert C.string_at(success_points, 32) == original
    result = dict(cases=rows, source_mutation_does_not_change_copy=True,
                  native_pins=ns['pins'], harness_sha256=sha(out / 'native_probe.py'),
                  transformed_prefix_sha256=hashlib.sha256(source.encode()).hexdigest(),
                  method_sha256=sha(__file__), free=guard(),
                  scope='Actual native region append/copy; supplied allocator faults; no retail or whole generator')
    (out / 'copy.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf8', newline='\n')


def main():
    if not __debug__ or sys.flags.optimize:
        raise RuntimeError('Use Python -E -B')
    guard()
    if sys.argv[1] == '--child':
        return child(Path(sys.argv[2]))
    out = (ROOT / '.local-work/d5ah' / sys.argv[1]).resolve()
    if out.exists() or not out.is_relative_to(ROOT / '.local-work/d5ah'):
        raise ValueError('Fresh task-local output required')
    out.mkdir()
    old = ROOT / '.local-work/d5s'
    rows = list(csv.DictReader((ROOT / 'docs/experiments/resource-retained-population/d5s-sources.csv').open(encoding='utf8')))
    for name in ('native_probe.py', 'start.py', 'initial.json'):
        path = old / name
        pin = next(r['sha256'] for r in rows if Path(r['path']).resolve() == path.resolve())
        if sha(path) != pin:
            raise ValueError('D5S input drift: ' + name)
        (out / name).write_bytes(path.read_bytes())
    (out / 'functions').mkdir()
    for name in ('1402fbc20', '142346f80', '1407ac0d0', '1407ac2f0', '1407aedd0'):
        path = old / 'functions' / (name + '.txt')
        (out / 'functions' / path.name).write_bytes(path.read_bytes())
    env = dict(os.environ, D5S_OUTPUT=str(out))
    run = subprocess.run([sys.executable, '-E', '-B', __file__, '--child', str(out)],
                         cwd=ROOT, env=env, capture_output=True,
                         creationflags=subprocess.CREATE_NO_WINDOW)
    (out / 'stdout.log').write_bytes(run.stdout)
    (out / 'stderr.log').write_bytes(run.stderr)
    (out / 'execution.json').write_text(json.dumps(dict(exit=run.returncode,
        method_sha256=sha(__file__)), indent=2) + '\n', encoding='utf8', newline='\n')
    if run.returncode or b'Exception ignored' in run.stderr:
        raise RuntimeError('Copy control failed; preserve logs')
    print((out / 'copy.json').read_text())


if __name__ == '__main__':
    main()
