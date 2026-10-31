# SPDX-License-Identifier: GPL-3.0-or-later
"""Run the unchanged owned D5AB semantic fixtures against final P2 consumers.

Reads a pinned build, packaged/current consumer hashes and the exact semantic AST
block in d5ab_qualify.py. Executes only that pure synthetic block; does not run
its historical native-session final-chain oracles, damaged-session code or main.
Writes source snapshots, selected source and results to a fresh ignored directory.
CPython stdlib only; no native execution, game, saves, network or Git writes.
"""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import shutil
import struct
import sys
import time

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    build, out = [Path(value).resolve() for value in sys.argv[1:]]
    assert build.is_relative_to(ROOT / '.local-work/d5x')
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    out.mkdir(exist_ok=False)
    source = Path(__file__).with_name('d5ab_qualify.py')
    src = ROOT / 'runtime/construction-winner'
    package = build / 'package-runtime'
    manifest = json.loads((build / 'build.json').read_bytes())
    assert manifest['source_unchanged'] and manifest['compilation']['pass_exit']
    for name in ('read_capture.py', 'reduce_v3.py'):
        assert sha(package / name) == sha(src / name)
    inputs = {str(p): sha(p) for p in (Path(__file__), source, src / 'read_capture.py', src / 'reduce_v3.py', build / 'build.json')}
    for name in inputs:
        path = Path(name)
        destination = out / 'sources' / path.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(path.read_bytes())
    text = source.read_text(encoding='utf8')
    tree = ast.parse(text, filename=str(source))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'main')
    def assignment(node, name):
        return isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == name for target in node.targets)
    first = next(index for index, node in enumerate(function.body) if assignment(node, 'base'))
    last = next(index for index, node in enumerate(function.body) if assignment(node, 'damage'))
    selected = function.body[first:last]
    assert selected and first < last
    start_line, end_line = selected[0].lineno, selected[-1].end_lineno
    fragment = ''.join(text.splitlines(keepends=True)[start_line - 1:end_line])
    (out / 'selected-source.txt').write_text(fragment, encoding='utf8', newline='\n')
    namespace = dict(build=build, out=out, copy=copy, time=time, hashlib=hashlib,
                     json=json, random=random, struct=struct,
                     reader=load('p2_legacy_fixture_reader', package / 'read_capture.py'),
                     reducer=load('p2_legacy_fixture_reducer', package / 'reduce_v3.py'))
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(source), 'exec'), namespace)
    results = namespace['results']
    required = {'equal-token-different-source', 'different-token-same-geography',
                'same-key-token-different-ancestry', 'out-of-order-arrival',
                'unmatched-lifecycle-contradicts-zero-hazard', 'loss-before-new-empty-boundary'}
    assert required <= {row['case'] for row in results}
    assert len(results) == 54 and all(row['passed'] for row in results)
    assert all(sha(path) == digest for path, digest in inputs.items())
    receipt = dict(schema='sor-d5ab-p2-legacy-semantics/1', passed=True, tests=len(results),
                   inputs=inputs, build=str(build), dll_sha256=sha(package / 'SorConstructionWinner.dll'),
                   selected_lines=[start_line, end_line], selected_sha256=sha(out / 'selected-source.txt'),
                   execution_scope='Exact original semantic AST block only; historical main and native final-chain API oracles not executed.',
                   native_source_lifetime_qualified=False, rows=results)
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(passed=True, tests=len(results), selected_lines=[start_line, end_line])))


if __name__ == '__main__':
    main()
