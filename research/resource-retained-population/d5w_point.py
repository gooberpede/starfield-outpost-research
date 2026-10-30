# SPDX-License-Identifier: GPL-3.0-or-later
"""Discriminate fixed-point admission using supplied historical U25 alternatives.

Reuses the owned D5V native setup up to its predicate bindings, with exact hash
checked against its retained receipt. Reads the pinned executable and authored
geometry. Runs only original point-predicate instructions in this disposable
process. Writes fresh ignored method/receipt files; no game, save, installed,
database, network or Git operation. See the active ledger's experiment plan.
"""
from pathlib import Path
import hashlib
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    output = Path(sys.argv[1]).resolve()
    assert output.is_relative_to(ROOT / '.local-work') and not output.exists()
    method = Path(__file__).with_name('d5v_native.py')
    old = json.loads((ROOT / '.local-work/d5v/native05.json').read_text())
    assert sha(method) == old['code_sha256']
    source = method.read_text(encoding='utf8').split('    rows = []', 1)[0]
    source = source.replace("destination = LOCAL/sys.argv[1]", "destination = Path(sys.argv[1]).resolve()")
    source = source.replace("assert destination.parent == LOCAL and not destination.exists()",
                            "assert destination.is_relative_to(ROOT/'.local-work') and not destination.exists()")
    tail = '''
    source_path = ROOT/'docs/experiments/resource-retained-population/d5u/outposts/D2-84e101.json'
    model = json.loads(source_path.read_text())
    layers = {r['mask']:r for r in model['layers'] if r['source_id']=='U25'}
    low = [r for r in layers[0]['regions'] if r['resource']=='000057d4']
    high = [r for r in layers[3]['regions'] if r['resource']=='000057d4']
    center = model['reference']['center']
    import math
    candidate = next(p[:3] for r in high for p in r['points'] if p[3]>0
                     and math.dist(p[:2],center[:2])<150
                     and all(math.dist(p[:2],v['native_bound'][:2])>v['native_bound'][3] for v in low))
    results = []
    for mask, regions in [(0,low),(3,high)]:
        verdicts = []
        for r in regions:
            points = (C.c_float*(4*len(r['points'])))(*(v for p in r['points'] for v in p))
            region = C.create_string_buffer(48)
            C.memmove(region,struct.pack('<4f',*r['native_bound']),16)
            C.c_uint32.from_buffer(region,24).value=len(r['points'])
            C.c_void_p.from_buffer(region,32).value=C.addressof(points)
            query = (C.c_float*3)(*candidate)
            accepted = bool(point_callback(C.addressof(region),C.addressof(query)) & 255)
            verdicts.append(dict(accepted=accepted,geometry_sha256=hashlib.sha256(bytes.fromhex(r['native_bound_le']+r['ordered_xyzw_le'])).hexdigest()))
        results.append(dict(mask=mask,accepted=any(v['accepted'] for v in verdicts),regions=verdicts))
    assert [r['accepted'] for r in results]==[False,True]
    assert not errors,errors
    result = dict(schema='sor-d5w-point/1',game_process=False,query=candidate,
                  frame='Qualified historical native descriptor frame; current loaded epoch unknown',
                  resource='000057d4',outpost_center=center,distance_xy=math.dist(candidate[:2],center[:2]),
                  results=results,functions=functions,executable_sha256=initial['installed'][exe],
                  source_geometry_sha256=sha(source_path),scope='Point-resource predicate only; produced-resource intersection and other placement gates are conditional',
                  inherited_method_sha256=sha(ROOT/'research/resource-retained-population/d5v_native.py'))
    destination.write_text(json.dumps(result,indent=2)+'\\n',encoding='utf8',newline='\\n')
    print(json.dumps(dict(query=candidate,point_admission=[r['accepted'] for r in results]),indent=2))

main()
'''
    derived = output.with_suffix('.method.py')
    assert not derived.exists()
    derived.write_text(source + tail, encoding='utf8', newline='\n')
    namespace = {'__file__': str(method), '__name__': 'd5w_disposable_point'}
    exec(compile(source + tail, str(derived), 'exec'), namespace)
    receipt = json.loads(output.read_text())
    receipt.update(wrapper_sha256=sha(__file__), derived_method_sha256=sha(derived))
    output.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')


if __name__ == '__main__':
    main()
