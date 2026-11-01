# SPDX-License-Identifier: GPL-3.0-or-later
"""Run original schema-3 semantic oracles with corrected optimization-safe consumers.

Reads immutable old schema-3 capture/build snapshots and the new qualified native
build's current packaged readers. Executes the unchanged owned semantic AST block
against old capture data and new consumers; records both producer and interpreter
identities explicitly. Writes fresh ignored snapshots/results only; no historical
capture, package or receipt is edited. No native/game/save/network/Git action.
Adapted from d5ab_p1_legacy_semantics.py under SOR-P-0002.
Origin SHA-256: 528191e5640244a1241dedb6a4af6239edcd0795821beb619bb35e23bacfc234.
"""
import sys

if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')

import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import shutil
import struct
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
    build, consumer_build, out = [Path(value).resolve() for value in sys.argv[1:]]
    assert consumer_build.is_relative_to(ROOT / '.local-work/d5x')
    assert build.is_relative_to(ROOT / '.local-work/d5x')
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40_000_000_000
    out.mkdir(exist_ok=False)
    source = Path(__file__).with_name('d5ab_qualify.py')
    src = ROOT / 'runtime/construction-winner'
    package = build / 'package-runtime'
    manifest = json.loads((build / 'build.json').read_bytes())
    assert manifest['source_unchanged'] and manifest['compilation']['pass_exit']
    # Authenticate the old producer's original outputs and frozen source inputs.
    for name, digest in manifest['outputs'].items():
        assert sha(build / name) == digest, name
    for name, digest in manifest['inputs'].items():
        frozen = build / 'sources' / Path(name).relative_to(ROOT)
        assert sha(frozen) == digest, str(frozen)
    consumer_manifest = json.loads((consumer_build / 'build.json').read_bytes())
    assert consumer_manifest['source_unchanged'] and consumer_manifest['compilation']['pass_exit']
    for name in ('read_capture.py', 'reduce_v3.py', 'reduce_v4.py'):
        assert sha(consumer_build / 'package-runtime' / name) == sha(src / name)
    old_reducer = ast.parse((package / 'reduce_v3.py').read_text(encoding='utf8'))
    new_reducer = ast.parse((src / 'reduce_v3.py').read_text(encoding='utf8'))
    # Only the new sys import and mandatory module-entry guard may differ.
    original_new_body = list(new_reducer.body)
    new_reducer.body = [node for node in original_new_body if not (
        isinstance(node, ast.Import) and node.lineno < 20 and any(a.name == 'sys' for a in node.names)
        or isinstance(node, ast.If) and node.lineno < 20 and 'optimize' in ast.unparse(node.test))]
    removed = [node for node in original_new_body if node not in new_reducer.body]
    assert len(removed) == 2 and isinstance(removed[0], ast.Import) and isinstance(removed[1], ast.If)
    expected_guard = ast.parse('not __debug__ or sys.flags.optimize != 0', mode='eval').body
    assert ast.dump(removed[1].test) == ast.dump(expected_guard)
    assert len(removed[1].body) == 1 and isinstance(removed[1].body[0], ast.Raise)
    assert ast.dump(old_reducer, include_attributes=False) == ast.dump(new_reducer, include_attributes=False)
    captured_raw_sha256 = sha(build / 'normal/events.bin')
    normalized_outputs = {Path(name).as_posix(): digest for name, digest in manifest['outputs'].items()}
    assert normalized_outputs['normal/events.bin'] == captured_raw_sha256
    inputs = {str(p): sha(p) for p in (Path(__file__), source, src / 'read_capture.py', src / 'reduce_v3.py', build / 'build.json', consumer_build / 'build.json')}
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
                     reader=load('p2_legacy_fixture_reader', src / 'read_capture.py'),
                     reducer=load('p2_legacy_fixture_reducer', src / 'reduce_v3.py'))
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(source), 'exec'), namespace)
    results = namespace['results']
    required = {'equal-token-different-source', 'different-token-same-geography',
                'same-key-token-different-ancestry', 'out-of-order-arrival',
                'unmatched-lifecycle-contradicts-zero-hazard', 'loss-before-new-empty-boundary'}
    assert required <= {row['case'] for row in results}
    assert len(results) == 54 and all(row['passed'] for row in results)
    assert all(sha(path) == digest for path, digest in inputs.items())
    receipt = dict(schema='sor-d5ab-p4-opt-legacy-semantics/1', passed=True, tests=len(results),
                   inputs=inputs, capture_build=str(build), consumer_build=str(consumer_build),
                   capture_raw_sha256=captured_raw_sha256, consumer_dll_sha256=sha(consumer_build / 'package-runtime/SorConstructionWinner.dll'),
                   reducer_behavior_ast_equal=True, historical_outputs_verified=True,
                   dll_sha256=sha(package / 'SorConstructionWinner.dll'),
                   selected_lines=[start_line, end_line], selected_sha256=sha(out / 'selected-source.txt'),
                   execution_scope='Exact original semantic AST block only; historical main and native final-chain API oracles not executed.',
                   native_source_lifetime_qualified=False, rows=results)
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8', newline='\n')
    print(json.dumps(dict(passed=True, tests=len(results), selected_lines=[start_line, end_line])))


if __name__ == '__main__':
    main()
