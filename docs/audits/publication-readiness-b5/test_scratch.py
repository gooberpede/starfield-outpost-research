"""Safe B5 qualification of actual repaired scratch blocks, not historical runs.
Stdlib + installed Git; reads ten current sources, extracts only their context-
managed review-application phase. Uses synthetic text and repository-local
temporary fixtures; removes only fixtures created by this invocation. Receipts
are written outside temporary trees. No imports/execution of original entrypoint
prologues, protected inputs, native tools, network, index or refs.
Run from repository root: python -B docs/audits/publication-readiness-b5/test_scratch.py
"""
import ast
import hashlib
import json
import os
import pathlib
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / '.local-work/b5'
SCRATCH = ROOT / '.local-work/review-patches'
SOURCES = [
    'continuous-beacon-preview/export-review-package.py',
    'resource-availability/export-review-package.py',
    'resource-availability-milestone-b/export-review-package.py',
    'native-availability-map/export-review-package.py',
    'local-readiness/export-review.py', 'existing-reference-grid/package.py',
    'matching-source/package.py', 'x87-preservation/package.py',
    'internal-observation-qualification/package.py',
    'runtime/session-tools/export_review.py',
]


def run():
    OUT.mkdir(exist_ok=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    initial = set(SCRATCH.iterdir())
    results = []
    for source in SOURCES:
        p = ROOT / source if source.startswith('runtime/') else ROOT / 'research' / source
        text = p.read_text(encoding='utf8')
        assert 'GIT_CEILING_DIRECTORIES' in text, source
        tree = ast.parse(text)
        block = next(n for n in ast.walk(tree) if isinstance(n, ast.With)
                     and 'TemporaryDirectory' in ast.unparse(n.items[0].context_expr))
        assert any(k.arg == 'dir' and ast.unparse(k.value) == 'review_scratch'
                   for k in block.items[0].context_expr.keywords), source
        code = compile(ast.Module(body=[block], type_ignores=[]), str(p), 'exec')
        for fail in (False, True):
            created = []
            with tempfile.TemporaryDirectory(prefix='b5-fixture-', dir=SCRATCH) as fixture:
                root = Path(fixture)
                (root / 'fixture.txt').write_bytes(b'after\n')
                patch = root / 'fixture.diff'
                patch.write_bytes(b'diff --git a/fixture.txt b/fixture.txt\n'
                                  b'--- a/fixture.txt\n+++ b/fixture.txt\n'
                                  b'@@ -1 +1 @@\n-before\n+after\n')
                env = dict(os.environ, GIT_OPTIONAL_LOCKS='0',
                           GIT_CEILING_DIRECTORIES=str(ROOT / '.local-work'))
                # Ensure the synthetic workspace cannot discover the real repo.
                probe = subprocess.run(['git', 'rev-parse', '--show-toplevel'],
                                       cwd=root, env=env, capture_output=True)
                assert probe.returncode != 0

                def git(*args, cwd=root):
                    if args[0] == 'show':
                        result = subprocess.CompletedProcess(args, 0, b'before\n', b'')
                    else:
                        created.append(str(cwd))
                        if fail:
                            raise RuntimeError('B5_INJECTED_APPLY_FAILURE')
                        result = subprocess.run(['git', '-c', 'core.autocrlf=false', *args], cwd=cwd, env=env,
                                                capture_output=True)
                        assert result.returncode == 0, result.stderr
                    return result if source.startswith(('existing-reference-grid/', 'matching-source/')) else result.stdout

                def digest(path):
                    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

                namespace = dict(ROOT=root, R=root, root=root, Path=Path,
                                 tempfile=tempfile, pathlib=pathlib, review_scratch=SCRATCH,
                                 paths=['fixture.txt'], files=['fixture.txt'],
                                 changed=['fixture.txt'], tracked=['fixture.txt'],
                                 original={'fixture.txt': b'before\n'},
                                 oldset={'fixture.txt': b'before\n'},
                                 before={'fixture.txt': b'before\n'},
                                 old={'fixture.txt': b'before\n'},
                                 current={'fixture.txt': b'after\n'},
                                 cur={'fixture.txt': b'after\n'},
                                 path=patch, out=patch, target=patch, git=git,
                                 label='task-only', patches={}, sha=digest, digest=digest,
                                 data=patch.read_bytes())
                try:
                    exec(code, namespace)
                    assert not fail, 'injected failure was not exercised'
                    outcome = 'normal'
                except RuntimeError as e:
                    assert fail and str(e) == 'B5_INJECTED_APPLY_FAILURE'
                    outcome = 'exception'
                scratch = Path(namespace.get('scratch', namespace.get('tree', namespace.get('d', ''))))
                # x87 names its workspace tree, other sources use scratch or d.
                if source.startswith('x87-'):
                    scratch = Path(namespace['tree'])
                elif source.startswith('internal-'):
                    scratch = Path(namespace['d'])
                assert created and not scratch.exists(), (source, outcome, scratch)
                results.append(dict(source=str(p.relative_to(ROOT)), outcome=outcome,
                                    scratch=str(scratch), cleaned=True,
                                    parent_discovery_blocked=True,
                                    source_sha256=digest(p)))
                # Essential receipt deliberately lives outside both fixture trees.
                (OUT / 'scratch-tests.json').write_text(json.dumps(results, indent=2) + '\n',
                                                      encoding='utf8', newline='\n')
            assert set(SCRATCH.iterdir()) == initial
    assert len(results) == 20
    print(json.dumps(dict(cases=len(results), normal=10, exception=10,
                          residue=0, receipt_survives=True)))


if __name__ == '__main__':
    run()
