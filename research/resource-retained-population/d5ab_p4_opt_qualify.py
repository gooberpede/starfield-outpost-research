# SPDX-License-Identifier: GPL-3.0-or-later
"""Test optimization refusal before operational imports and side effects.

Reads original project Python source and guarded entry points. Executes only
disposable Python probes and negative CLI fixtures; writes fresh ignored sources,
traces, sentinel files, stdout/stderr and a receipt. No game, protected data,
deployment, native process contact, network or dependency installation.
"""
import sys

if not __debug__ or sys.flags.optimize != 0:
    raise RuntimeError('Python optimization is forbidden; invoke with -E -B and no -O/-OO')

import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
GUARDED = [
    *['runtime/construction-winner/' + name for name in
      ('build.py','controller.py','p4_controller.py','worker_health.py',
       'read_capture.py','reduce_v3.py','reduce_v4.py')],
    *['runtime/session-tools/' + name for name in ('common.py','archive.py','session.py')],
    'runtime/retained-population/protect.py',
    'research/resource-carinae-source-context/save_policy.py',
    'research/resource-retained-population/prepare_native.py',
]
GUARDED += [p.relative_to(ROOT).as_posix() for p in
            sorted((ROOT / 'research/resource-retained-population').glob('d5ab_p4_*.py'))]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    out = (ROOT / sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT / '.local-work/d5ab')
    out.mkdir(parents=True, exist_ok=False)
    guarded = sorted(set(GUARDED))
    rows, audit = [], []
    snapshots = out / 'sources'
    for name in guarded:
        path = ROOT / name
        source = path.read_text(encoding='utf8')
        tree = ast.parse(source)
        body = tree.body[1:] if isinstance(tree.body[0], ast.Expr) else tree.body
        # Exact ordinary guard must dominate all other imports and module work.
        assert isinstance(body[0], ast.Import) and [n.name for n in body[0].names] == ['sys'], name
        guard = body[1]
        assert isinstance(guard, ast.If) and any(isinstance(n, ast.Raise) for n in ast.walk(guard)), name
        assert '__debug__' in ast.unparse(guard.test) and 'sys.flags.optimize' in ast.unparse(guard.test), name
        target = snapshots / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())
        assertions = [n for n in ast.walk(tree) if isinstance(n, ast.Assert)]
        audit.append(dict(path=name, sha256=sha(path), assertions=len(assertions),
            calls=[dict(line=n.lineno, expression=ast.unparse(n.test)) for n in assertions
                   if any(isinstance(c, ast.Call) for c in ast.walk(n.test))],
            guard_end_line=guard.end_lineno))

        for mode, flags, env_value in (
            ('explicit-O', ['-E','-B','-O'], None),
            ('explicit-OO', ['-E','-B','-OO'], None),
            ('inherited-1', ['-B'], '1'), ('inherited-2', ['-B'], '2')):
            case = out / (path.stem + '-' + str(len(rows)))
            case.mkdir()
            output = case / 'must-not-exist'
            env = dict(os.environ)
            env.pop('PYTHONOPTIMIZE', None)
            if env_value:
                env['PYTHONOPTIMIZE'] = env_value
            command = [sys.executable, *flags, str(path), '--out', str(output)]
            result = subprocess.run(command, cwd=case, env=env, capture_output=True)
            assert result.returncode != 0 and b'Python optimization is forbidden' in result.stderr, (name,mode,result.stderr)
            assert not output.exists() and not list(case.iterdir()), (name, mode)
            rows.append(dict(path=name, mode=mode, passed=True, side_effect_files=0))
            (case / 'stderr.txt').write_bytes(result.stderr)

        # Run the complete module code under a normal interpreter but explicitly
        # optimized compile(), while trapping every import except sys. This
        # distinguishes code-object optimization from process sys.flags alone.
        for optimize in (1, 2):
            imports = []
            def safe_import(module, *args, **kwargs):
                imports.append(module)
                if module != 'sys':
                    raise AssertionError('Import reached before optimization refusal: ' + module)
                return sys
            try:
                exec(compile(source, str(path), 'exec', optimize=optimize),
                     {'__name__':'optimization_probe', '__file__':str(path),
                      '__builtins__':dict(__import__=safe_import, RuntimeError=RuntimeError)})
            except RuntimeError as error:
                assert 'Python optimization is forbidden' in str(error)
            else:
                raise AssertionError('Optimized module executed: ' + name)
            assert imports == ['sys']
            rows.append(dict(path=name, mode='optimized-code-object-' + str(optimize),
                             passed=True, reached_imports=imports, side_effect_files=0))

        # Exercise the actual parsed guard prefix with a disposable marker.
        prefix = '\n'.join(source.splitlines()[:guard.end_lineno])
        probe = out / ('normal-' + str(len(rows)) + '.py')
        marker = out / (probe.stem + '.marker')
        probe.write_text(prefix + '\nfrom pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("guard passed")\n', encoding='utf8', newline='\n')
        for env_value in ('', '1', '2'):
            env = dict(os.environ, PYTHONOPTIMIZE=env_value)
            result = subprocess.run([sys.executable,'-E','-B',str(probe)], env=env, capture_output=True)
            assert result.returncode == 0 and marker.read_text() == 'guard passed'
            marker.unlink()
            rows.append(dict(path=name, mode='E-B-normal-inherited-' + (env_value or 'none'),
                             passed=True, optimize=0))

    # Full real controller CLI: -E must retain its ordinary pin rejection and
    # durable error receipt with inherited optimization, without a session write.
    for value in ('1', '2'):
        case = out / ('normal-controller-' + value); case.mkdir()
        plan = case / 'plan.json'; plan.write_text('{}', encoding='utf8')
        receipt = case / 'receipt.json'; session = case / 'session'
        command = [sys.executable,'-E','-B',str(ROOT / 'runtime/construction-winner/p4_controller.py'),
            'start','--session',str(session),'--plan',str(plan),'--plan-sha256','0'*64,
            '--preflight',str(plan),'--preflight-sha256',sha(plan),
            '--approval',str(plan),'--approval-sha256',sha(plan),'--out',str(receipt)]
        result = subprocess.run(command, env=dict(os.environ,PYTHONOPTIMIZE=value), capture_output=True)
        assert result.returncode != 0 and json.loads(receipt.read_bytes())['state'] == 'CHECK_ERROR'
        assert not session.exists()
        rows.append(dict(path='p4_controller.py',mode='E-B-full-CLI-inherited-' + value,
                         passed=True, pin_failure_before_session=True))
    result = dict(schema='sor-d5ab-p4-optimization-tests/1',passed=True,rows=rows,
                  audit=audit,inputs={n:sha(ROOT/n) for n in guarded},
                  method_sha256=sha(__file__),scope='Python-only refusal and assertion audit; no target contacts')
    (out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(passed=True,guarded_modules=len(guarded),tests=len(rows),assertions=sum(r['assertions'] for r in audit))))


if __name__ == '__main__':
    main()
