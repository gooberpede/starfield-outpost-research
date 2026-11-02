# SPDX-License-Identifier: GPL-3.0-or-later
"""Audit fixed native exports: complete direct registration-xref census, exact
registered names including the inline singleton; fresh local receipt.
No native execution, network, database or target mutation. Stdlib only;
reads source-ledger-pinned exports. Rejects optimized execution and disk-floor
failure. Owned lineage: frozen task-local d5ad_swap_registry.py. Static ordinary
registry coverage does not assert unobserved live registries or indirect callers.
"""
from pathlib import Path
import re, json, hashlib, sys, csv
from d5ad_baseline import guard
R = Path(__file__).resolve().parents[2]
B = R / '.local-work/d5ad-save'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def funcs(p):
    if p.relative_to(R).as_posix() not in PINS or sha(p) != PINS[p.relative_to(R).as_posix()]:
        raise ValueError('EXPORT_IDENTITY')
    s = p.read_text(encoding='utf-8')
    if not s.endswith('END\n'):
        raise ValueError("Validation failed: s.endswith('END\\n')")
    return (s, re.findall('^FUNCTION\\t[^\\n]*\\n.*?^END_FUNCTION$', s, re.M | re.S))

def main():
    if sys.flags.optimize:
        raise ValueError('OPTIMIZATION')
    guard()
    o = Path(sys.argv[1]).resolve()
    if not o.is_relative_to(R / '.local-work') or o.exists():
        raise ValueError('FRESH_LOCAL_OUTPUT')
    global PINS
    ledger = R / 'docs/experiments/resource-retained-population/d5ad-sources.csv'
    PINS = {}
    for row in csv.DictReader(ledger.read_text(encoding='utf8').splitlines()):
        if row['path'] in PINS and PINS[row['path']] != row['sha256']:
            raise ValueError('CONFLICTING_SOURCE_PINS')
        PINS[row['path']] = row['sha256']
    s, fs = funcs(B / 'swap-export06/native.tsv')
    calls = re.findall('^XREF\\tFrom: (\\w+) To: 1404613d0 Type: UNCONDITIONAL_CALL', s, re.M)
    if not len(calls) == 74:
        raise ValueError('Validation failed: len(calls) == 74')
    _, regs = funcs(B / 'swap-export08/native.tsv')
    if not len(regs) == 74:
        raise ValueError('Validation failed: len(regs) == 74')
    _, getters = funcs(B / 'swap-export10/native.tsv')
    getters = {f.split('\n')[0].split('\t')[1]: f.split('DECOMPILE\n')[1] for f in getters}
    _, extra = funcs(B / 'swap-export12/native.tsv')
    lens = next((f for f in extra if f.startswith('FUNCTION\t14000f770'))).split('DECOMPILE\n')[1]
    lensname = re.findall('\\(byte \\*\\)"([^"]+)"', lens)
    if not len(lensname) == 1:
        raise ValueError('Validation failed: len(lensname) == 1')
    rows = []
    for f in regs:
        lines = f.splitlines()
        entry = lines[0].split('\t')[1]
        instructions = {x.split('\t')[0] for x in lines if re.match('^[0-9a-f]{9}\\t', x)}
        cs = set(calls) & instructions
        if not len(cs) == 1:
            raise ValueError('Validation failed: len(cs) == 1')
        d = f.split('DECOMPILE\n')[1]
        reg = d.split('FUN_1404613d0')[0]
        if entry == '14000f7a0':
            name = lensname[0]
            getter = '14000f770'
        else:
            getter = re.findall('FUN_(\\w+)\\(\\);', reg)[-1]
            ns = re.findall('\\(byte \\*\\)"([^"]+)"', getters[getter])
            if not len(ns) == 1:
                raise ValueError('Validation failed: len(ns) == 1')
            name = ns[0]
        rows.append(dict(callsite=next(iter(cs)), initializer=entry, name_source=getter, name=name))
    if not {r['callsite'] for r in rows} == set(calls):
        raise ValueError("Validation failed: {r['callsite'] for r in rows} == set(calls)")
    result = dict(
        scope='Every direct call to native name-to-form-factory registration '
              '0x1404613d0 in the fixed existing database. Four noncall '
              'code-pointer references remain in the source; indirect or '
              'unobserved mutations are not promoted to runtime fact.',
        direct_registration_calls=74, covered=74,
        target='SurfaceTreePatternSwapInfo_Component',
        exact_matches=[r for r in rows if r['name'] == 'SurfaceTreePatternSwapInfo_Component'],
        rows=rows,
        input_hashes={f'swap-export{n:02d}/native.tsv': sha(B / f'swap-export{n:02d}/native.tsv')
                      for n in (6, 8, 10, 12)},
        script_sha256=sha(Path(__file__)))
    o.mkdir(parents=True)
    (o / 'receipt.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('covered', len(rows), 'target matches', len(result['exact_matches']))
if __name__ == '__main__':
    main()
