# SPDX-License-Identifier: GPL-3.0-or-later
"""Test D5AK interpreter admission and content guards on disposable owned files.

Reads the actual operational closure and immutable historical qualification
receipts; writes fresh ignored fixtures and a receipt. Subprocesses invoke only
Python help/refusal paths with effect sentinels. No game, native host, deployment,
protected-save write, controller request, network or Git mutation. Uses owned
D5AI content guards under SOR-P-0002. Invoke the pinned interpreter with -E -B.
"""
import sys
if not __debug__ or sys.flags.optimize:
    raise RuntimeError('Use the pinned Python interpreter with -E -B; optimization is forbidden')

import argparse
import ast
import json
import os
from pathlib import Path
import subprocess

import d5ak_operations as operations


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    operations.require(out.is_relative_to(operations.ROOT / '.local-work/d5ak'), 'Fresh D5AK output required')
    free = operations.guard()
    out.mkdir(parents=True, exist_ok=False)
    rows = []

    def check(name, condition, basis):
        rows.append(dict(name=name, passed=bool(condition), basis=basis))
        if not condition:
            raise AssertionError(name)

    guard = operations.content.content_guard
    for label, always in (('configuration', True), ('large-definition', False)):
        file = out / (label + '.owned')
        file.write_bytes(b'owned content guard fixture')
        pin = operations.sha(file)
        metadata = dict(bytes=file.stat().st_size, mtime_ns=file.stat().st_mtime_ns)
        before = guard(file, metadata, pin, always)
        check(label + '-unchanged', before is not None if always else before is None, 'ACTUAL owned file')
        os.utime(file, ns=(metadata['mtime_ns'], metadata['mtime_ns'] + 2_000_000_000))
        value = guard(file, metadata, pin, always)
        check(label + '-timestamp-only-positive-rehash', value['timestamp_changed'] and value['content_sha256_verified'] == pin, 'ACTUAL timestamp change, original bytes')
        file.write_bytes(b'X' + file.read_bytes()[1:])
        os.utime(file, ns=(metadata['mtime_ns'], metadata['mtime_ns'] + 4_000_000_000))
        try:
            guard(file, metadata, pin, always)
        except (ValueError, AssertionError):
            failed = True
        else:
            failed = False
        check(label + '-changed-content-refused', failed, 'ACTUAL changed owned bytes')

    # Every optimization attempt must fail before parsing command arguments or
    # creating the requested output; -E must ignore inherited PYTHONOPTIMIZE.
    clis = [operations.ROOT / 'research/resource-retained-population' / name for name in
            ('d5ak_episode.py', 'd5ak_operations.py', 'd5ak_bundle.py', 'd5aj_checkpoint.py', 'd5aj_reduce.py', 'd5ak_qualify.py', 'd5ai_episode.py')]
    clis += [operations.ROOT / 'runtime/session-tools' / name for name in ('session.py', 'archive.py')]
    commands = []
    for cli in clis:
        for flags, inherited, succeeds in ((['-E', '-B'], '2', True),
                                            (['-B'], '1', False),
                                            (['-E', '-B', '-O'], '', False),
                                            (['-E', '-B', '-OO'], '', False)):
            env = dict(os.environ, PYTHONOPTIMIZE=inherited)
            sentinel = out / (cli.stem + '-' + '-'.join(flags) + '.must-not-exist')
            command = [sys.executable, *flags, str(cli), '--help']
            result = subprocess.run(command, env=env, capture_output=True)
            refusal = result.returncode != 0 and (b'optimization' in result.stderr.lower() or b'Use Python -E -B' in result.stderr)
            check(cli.stem + '-' + '-'.join(flags) + '-env-' + inherited,
                  (result.returncode == 0 if succeeds else refusal)
                  and not sentinel.exists(), 'ACTUAL subprocess help path')
            # An optimized invalid operation with a real output argument must
            # fail at the guard before argument parsing can create any effects.
            if not succeeds:
                effect = subprocess.run([sys.executable, *flags, str(cli), 'invalid-operation', '--out', str(sentinel)], env=env, capture_output=True)
                check(cli.stem + '-failure-before-effect-' + '-'.join(flags),
                      effect.returncode != 0 and not sentinel.exists() and
                      (b'optimization' in effect.stderr.lower() or b'Use Python -E -B' in effect.stderr),
                      'ACTUAL optimized invalid operation with output sentinel')
            commands.append(dict(command=command, inherited_pythonoptimize=inherited,
                                 returncode=result.returncode, stdout=result.stdout.decode(errors='replace'),
                                 stderr=result.stderr.decode(errors='replace')))

    # Inventory assertions rather than claiming their absence. Calls inside an
    # assertion can disappear under optimization; entry guards are indispensable.
    audit = []
    for path in sorted(operations.required_sources()):
        if path.suffix != '.py':
            continue
        tree = ast.parse(path.read_text(encoding='utf8'))
        assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
        calls = [dict(line=node.lineno, expression=ast.unparse(node.test)) for node in assertions
                 if any(isinstance(n, ast.Call) for n in ast.walk(node.test))]
        audit.append(dict(path=str(path), sha256=operations.sha(path), assertions=len(assertions), call_bearing_assertions=calls,
                          imports=[ast.unparse(node) for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]))
    for cli in clis:
        body = ast.parse(cli.read_text(encoding='utf8')).body
        if cli.stem == 'd5ai_episode':
            # Frozen fallback imports the guarded P4 controller before defining
            # operational classes or dispatching any argument-selected effects.
            guarded = ast.parse((operations.ROOT / 'runtime/construction-winner/p4_controller.py').read_text(encoding='utf8')).body
            check('frozen-stop-imports-guarded-p4-before-controller-effects',
                  any(isinstance(node, ast.ImportFrom) and node.module == 'p4_controller' for node in body) and
                  isinstance(guarded[1], ast.Import) and guarded[1].names[0].name == 'sys' and
                  isinstance(guarded[2], ast.If) and any(isinstance(n, ast.Raise) for n in ast.walk(guarded[2])),
                  'STATIC import-chain guard; subprocess tests establish failure before requested output effects')
            continue
        if cli.stem == 'd5aj_reduce':
            # The versioned reducer first imports a pure predicate module that
            # defines functions/constants only. Its guard precedes I/O imports.
            check('d5aj-pure-predicate-before-guard',
                  isinstance(body[2], ast.ImportFrom) and body[2].module == 'd5aj_scope' and
                  isinstance(body[3], ast.If) and any(isinstance(n, ast.Raise) for n in ast.walk(body[3])),
                  'STATIC pure method import; no predicate is called at import')
            continue
        check(cli.stem + '-ordinary-guard-before-non-sys-imports',
              isinstance(body[1], ast.Import) and [n.name for n in body[1].names] == ['sys'] and
              isinstance(body[2], ast.If) and any(isinstance(node, ast.Raise) for node in ast.walk(body[2])),
              'STATIC AST entry-point order')

    inputs = {}
    for relative in ('.local-work/d5aj/d5ak-audit01/preservation.json',
                     '.local-work/d5aj/d5ak-qualify01/qualification.json',
                     '.local-work/d5aj/d5ak-native01.json',
                     '.local-work/d5ai-a/d5ak-timestamp01/receipt.json',
                     '.local-work/d5ak/qualification/erase01.json',
                     '.local-work/d5ak/qualification/consumer01.json'):
        path = operations.ROOT / relative
        inputs[relative] = dict(sha256=operations.sha(path), bytes=path.stat().st_size)
    receipt = dict(schema='sor-d5ak-qualification/1', tests=rows, passed=len(rows), method_sha256=operations.sha(__file__),
                   free_bytes=free, interpreter=dict(path=sys.executable, sha256=operations.sha(sys.executable), version=sys.version),
                   commands=commands, imported_source_audit=audit, prior_fresh_receipts=inputs,
                   limitations='Entry subprocess refusals and owned content guards only. Import assertions are inventoried, not removed. Native ownership controls and historical wire/source oracles are separately pinned receipts; no retail observation or real pre/postflight is claimed.')
    operations.fresh(out / 'receipt.json', receipt)
    print(json.dumps(dict(passed=len(rows), out=str(out))))


if __name__ == '__main__':
    main()
