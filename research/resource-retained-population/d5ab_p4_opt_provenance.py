# SPDX-License-Identifier: GPL-3.0-or-later
"""Requalify corrected P4 provenance or trace its offline full preflight.

Reads exact builds, current sources, original export/preservation records and new
test receipts. Writes fresh ignored verification and Python module-execution
inventory. Preflight delegates the existing full preservation procedure, writing
only a new restoration COPY and receipts. No game, deployment, protected-original,
analysis-database, network or Git mutation. Owned P4 methods, SOR-P-0002.
"""
import sys

if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')

import ast
import csv
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_bytes())


def write(path, value):
    with Path(path).open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def trace_preflight():
    plan, digest, output = sys.argv[2:5]
    out = (ROOT / output).resolve()
    assert out.is_relative_to(ROOT / '.local-work/d5ab') and not out.exists()
    executed = {}
    def capture(event, args):
        if event == 'exec':
            path = Path(args[0].co_filename).resolve()
            if path.is_relative_to(ROOT) and path.is_file():
                name = path.relative_to(ROOT).as_posix()
                if name not in executed:
                    executed[name] = sha(path)
    sys.addaudithook(capture)
    sys.path.insert(0, str(Path(__file__).parent))
    import d5ab_p4_operations as operations
    sys.argv = [str(Path(operations.__file__)), 'preflight', '--plan', plan,
                '--plan-sha256', digest, '--out', str(out)]
    operations.main()
    audit = []
    for name, pin in sorted(executed.items()):
        path = ROOT / name
        assert sha(path) == pin
        tree = ast.parse(path.read_bytes())
        assertions = [n for n in ast.walk(tree) if isinstance(n, ast.Assert)]
        audit.append(dict(path=name, sha256=pin, assertions=len(assertions),
            calls=[dict(line=n.lineno, expression=ast.unparse(n.test)) for n in assertions
                   if any(isinstance(c, ast.Call) for c in ast.walk(n.test))],
            code_generation=[dict(line=n.lineno,expression=ast.unparse(n)) for n in ast.walk(tree)
                if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('compile','exec')]))
    write(out / 'python-closure.json', dict(passed=True, method_sha256=sha(__file__),
        executed_modules=executed, assertion_inventory=audit,
        interpreter=dict(path=sys.executable, sha256=sha(sys.executable),
                         optimize=sys.flags.optimize, ignore_environment=sys.flags.ignore_environment,
                         dont_write_bytecode=sys.dont_write_bytecode),
        scope='Actual own-process Python module executions during offline preflight; no retail instrumentation.'))


def verify():
    out = (ROOT / sys.argv[2]).resolve()
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    out.mkdir(parents=True, exist_ok=False)
    baseline = read(ROOT / '.local-work/d5ab/p4-opt/baseline.json')
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip() == baseline['head']
    assert sha(ROOT / '.git/index') == baseline['index_sha256']
    build = ROOT / '.local-work/d5x/p4-opt-native01'
    repro = ROOT / '.local-work/d5x/p4-opt-repro01'
    native, repeated = read(build/'build.json'), read(repro/'build.json')
    assert len(native['cases']) == 90 and len(repeated['cases']) == 4
    for folder, data in ((build,native),(repro,repeated)):
        assert data['source_unchanged'] and data['compilation']['pass_exit']
        assert all(row['pass_exit'] for row in data['cases'])
        for path,pin in data['inputs'].items():
            assert sha(path) == pin, path
        for path,pin in data['outputs'].items():
            assert sha(folder/path) == pin, path
    assert native['inputs'] == repeated['inputs']
    original = read(ROOT/'.local-work/d5x/p3-native-final04/build.json')
    compiler = {path:pin for path,pin in original['inputs'].items()
                if Path(path).suffix.lower() in ('.cpp','.h','.asm')}
    assert len(compiler) == 13 and all(sha(path)==pin for path,pin in compiler.items())
    dll = sha(build/'package-runtime/SorConstructionWinner.dll')
    assert dll == sha(repro/'package-runtime/SorConstructionWinner.dll') == sha(ROOT/'.local-work/d5x/p3-native-final04/package-runtime/SorConstructionWinner.dll')
    receipts = {}
    for label in ('p4-opt-optimization-final01','p4-opt-admission01','p4-opt-procedures01',
                  'p4-opt-controller01','p4-opt-legacy-controller01','p4-opt-inherited-worker01',
                  'p4-opt-reader01','p4-opt-compat01','p4-opt-native-controls01',
                  'p4-opt-abi01','p4-opt-legacy03','p4-opt-worker01'):
        path=ROOT/'.local-work/d5ab'/label/'receipt.json'
        data=read(path)
        assert not data.get('failures',[]), label
        if 'passed' in data:
            assert data['passed'] is True, label
        if 'source_unchanged' in data:
            assert data['source_unchanged'] is True, label
        for source,pin in data.get('inputs',{}).items():
            assert sha(source)==pin,(label,source)
        if label in ('p4-opt-controller01','p4-opt-legacy-controller01'):
            expected = 28 if label=='p4-opt-controller01' else 26
            assert len(data['results']) == expected
            for row in data['results']:
                child=read(row['receipt'])
                assert sha(row['receipt']) == row['receipt_sha256'] and child['passed'] and child['source_unchanged']
                for source,pin in child['inputs'].items():
                    assert sha(source)==pin,(label,source)
        receipts[label]=dict(path=str(path),sha256=sha(path))
    preservation=read(ROOT/'.local-work/d5ab/p2-provenance02/preservation.json')
    for row in preservation:
        path=ROOT/row['path']
        assert path.exists()==row['exists']
        if row['exists']:
            assert path.stat().st_size==row['bytes'] and sha(path)==row['sha256']
    with (ROOT/'docs/experiments/resource-retained-population/d5ab-p1-sources.csv').open(encoding='utf8') as stream:
        exports=list(csv.DictReader(stream))
    for row in exports:
        assert sha(ROOT/row['path'])==row['sha256']
    write(out/'receipt.json',dict(passed=True,method_sha256=sha(__file__),head=baseline['head'],
        index_sha256=baseline['index_sha256'],dll_sha256=dll,native_cases=90,reproduction_cases=4,
        compiled_source_pins=compiler,build_input_pins=native['inputs'],receipts=receipts,
        preserved_historical_records=len(preservation),preserved_p1_exports=len(exports),
        scope='Corrected Python support requalified; identical native DLL. No retail occurrence or authorization.'))
    print(json.dumps(dict(passed=True,receipts=len(receipts),native_compiler_inputs=len(compiler))))


if __name__ == '__main__':
    if sys.argv[1] == 'trace-preflight':
        trace_preflight()
    elif sys.argv[1] == 'verify':
        verify()
    else:
        raise ValueError('Expected trace-preflight or verify')
