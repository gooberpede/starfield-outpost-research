# SPDX-License-Identifier: GPL-3.0-or-later
"""Authenticate the conditional A0-to-C1 packed-cell-key reconstruction.

Reads pinned actual A0 source/frame evidence, the prior original key control,
the pinned main definition and current scoped clip/static context receipts.
Uses owned main-file reader/tree-link methods under SOR-P-0002. No geometry
outcome is used to select an input. No native execution, database, save,
configuration, installation, network or Git mutation. Writes one fresh ignored
receipt; stops on input/source drift or either caller-available drive floor.
"""
import os
import sys
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import json
from pathlib import Path
import struct

from d5ad_baseline import ROOT, guard, sha
sys.path.insert(0, str(ROOT / 'research/resource-pattern-selection'))
from installed import ESM, esm_records, planet_tree


def need(condition, reason):
    if not condition:
        raise ValueError(reason)


def main():
    before = guard()
    out = Path(sys.argv[1]).absolute()
    need(out.resolve().is_relative_to(ROOT / '.local-work/d5ar') and out.parent.is_dir() and not out.exists(),
         'Fresh ignored output required')
    need(not any(p.is_symlink() or p.is_junction() for p in (out, *out.parents)), 'No reparse output')
    relative = {
        '.local-work/d5ar/source-planar-references05.json': 'ddd15d14e11af176e7317561f9baeb85217b6655128f1be5511656e87758c83b',
        '.local-work/d5ar/a0-file-inputs05.json': '69e41a455d097ab20ee1525c0c21c01288e372215ef3c0fd9ca09c69af6b64ff',
        '.local-work/d5ar/stitch-config02.json': '728bb52f5c7f6b02d27c5044ff7c910ea653abf874d849d21b64e3ca0c6a12e3',
        '.local-work/d5ar/clip-native02/qualification.json': 'd65284650b97cb35757ce10a84ca35b7897da42e81c5e414bce9b1abafe100c5',
        '.local-work/d5ar/key-context-native02/receipt.json': 'cfd0397605fbcf4419eb076aae1501ad531fcae8a005a823d756dfcd83f266fd',
        '.local-work/d5s/native-keys03.json': 'fe0201cec2fb43d79bd3ba8cb4cfc23bc048146f05b33b5199286ef9d49bf7be',
        '.local-work/d5s/geometry.json': '9594ab2aa34856bcc3b8ecb249b46b0063ef4b5d1af80d4e557542f2d6657ccf',
        '.local-work/d5t/functions/14078d7b0.txt': 'f595d79cfa540c05e2a161995bef5112c6d160372bdf3b55f53a25e30864df71',
    }
    inputs = {str(ROOT / path): digest for path, digest in relative.items()}
    need(all(sha(path) == digest for path, digest in inputs.items()), 'Prior input identity changed')
    sources = {str(Path(module.__file__).resolve()): sha(module.__file__)
               for module in tuple(sys.modules.values()) if getattr(module, '__file__', None) and
               Path(module.__file__).suffix == '.py' and Path(module.__file__).resolve().is_relative_to(ROOT)}
    reference, files, stitch, clip, context, keys, model = [json.loads((ROOT / name).read_bytes())
        for name in tuple(relative)[:7]]
    for output in context['outputs']:
        path = ROOT / '.local-work/d5ar/key-context-native02' / output['file']
        need(output['exit'] == 0 and sha(path) == output['sha256'], 'Original context window changed')
        inputs[str(path)] = output['sha256']
    frame = reference['actual_a0_frame']
    body = int(frame['body_formid'], 16)
    tree = 0x168814
    main_pin = files['inputs'][str(ESM)]
    need(files['definition_files'] == 39 and sha(ESM) == main_pin, 'Pinned definition identity changed')
    for fid, kind in ((body, 'PNDT'), (tree, 'SFTR')):
        matches = [r for r in files['records'] if r['header']['type'] == kind and
                   r['header']['formid'] & 0xffffff == fid and r['master'].lower() == 'starfield.esm']
        need(len(matches) == 1 and Path(matches[0]['file']) == ESM, 'Body/tree override or missing primary record')
    rows = {h['formid']: (h, fs) for h, fs in esm_records(ESM, {b'PNDT', b'SFTR'}, repeated=True)
            if h['formid'] in (body, tree)}
    need(set(rows) == {body, tree} and planet_tree(rows[body][1]) == tree, 'PNDT tree binding differs')
    gnam = [v for t, v in rows[body][1] if t == b'GNAM' and len(v) == 12]
    resolution = [v for t, v in rows[tree][1] if t == b'DNAM']
    need(len(gnam) == len(resolution) == 1 and len(resolution[0]) == 4, 'Ambiguous tuple/resolution')
    system, parent, index = struct.unpack('<III', gnam[0])
    width = struct.unpack('<I', resolution[0])[0]
    need((system, index, width) == (86469, 5, 256), 'Different typed body/tree tuple')
    chart, anchor_x, anchor_y, terrain = frame['geographic_key'].split(':')
    need(chart == '0' and keys['target']['source'] == frame['geographic_key'], 'Unsupported chart/source')
    constants = stitch['native_default']
    merge, block = (constants[name] for name in ('uBlockMergeZoneSize:Stitching', 'uBlockSize:Stitching'))
    face = width * (block + merge) * 16
    native_clip = clip['checks'][0]
    origin_x, origin_y = frame['native_origin_i32']
    need(native_clip['origin'] == [origin_x, origin_y] and native_clip['stitch'] == merge,
         'Clip/origin/stitch join differs')
    low_x, high_x, low_y, high_y = native_clip['cell_bounds']
    ordered = []
    for x in range(low_x, high_x):
        for y in range(low_y, high_y):
            px, py = int(anchor_x) + origin_x + x, int(anchor_y) + origin_y + y
            need(0 <= px < face < 65536 and 0 <= py < face, 'Unsupported seam or packed-field range')
            ordered.append(dict(cell=[x, y], key=((system << 6 | index) << 3) << 32 | py << 16 | px))
    need(len(ordered) == native_clip['cells'] == 144 and ordered == keys['packed_keys'],
         'Original native packed key control differs')
    encoded = {','.join(map(str, row['cell'])): row['key'] for row in ordered}
    need(all(row['request']['packed_keys'] == encoded and row['request']['owner_key'] == body
             for row in model['results']), 'Fixed generator request keys/owner differ')
    inputs[str(ESM)] = main_pin
    need(all(sha(path) == digest for path, digest in (inputs | sources).items()), 'Source or input changed')
    receipt = dict(status='PASS_CONDITIONAL_KEYS_EQUAL', source=frame['geographic_key'], body=f'{body:08x}',
        tree=f'{tree:08x}', system=system, parent_index=parent, body_index=index, tree_width=width,
        ordered_keys=ordered, inputs=inputs, source_sha256=sources, floors_before=before, floors_after=guard(),
        premises=['Ordinary initialized typed tree bound to the actual owner',
                  'Stable consumed descriptor in every per-cell conversion', 'Ordinary effective stitching settings'],
        historical_per_cell_reads_observed=False, effective_input_equivalence='NOT_ADJUDICATED_BY_THIS_CONTROL')
    with out.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(receipt, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(status=receipt['status'], ordered_keys=len(ordered))))


if __name__ == '__main__':
    main()
