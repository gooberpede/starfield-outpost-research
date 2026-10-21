"""B5 full successor control flow with synthetic Git-read responses.
Executes real Git diff/apply against synthetic text only; no init/add/commit.
Creates/cleans only this invocation's project-local fixtures, retaining receipts
outside them. No native inputs/processes, installed writes, network or index use.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / '.local-work/b5'
SCRATCH = ROOT / '.local-work/review-patches'


def run():
    spec = importlib.util.spec_from_file_location('b5_successor', ROOT / 'research/review_package.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    results = []
    initial = set(SCRATCH.iterdir())
    for mode in ('normal', 'apply-failure', 'prior-work', 'output-collision'):
        with tempfile.TemporaryDirectory(prefix='b5-successor-test-', dir=SCRATCH) as td:
            root = Path(td)
            (root / '.git').mkdir()
            (root / '.git/index').write_bytes(b'synthetic index identity; never passed to Git')
            (root / 'notes.md').write_bytes(b'Synthetic fixture.\n')
            baseline = root / 'baseline.json'
            baseline.write_text(json.dumps(dict(head='synthetic-head',
                index_sha256=hashlib.sha256((root / '.git/index').read_bytes()).hexdigest(),
                status=' M earlier.txt\n' if mode == 'prior-work' else '')), encoding='utf8')
            module.ROOT = root
            module.ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0',
                              GIT_CEILING_DIRECTORIES=str(ROOT / '.local-work'))
            real_git = module.git
            calls = []

            def git(*args, cwd=None, allowed=(0,)):
                cwd = root if cwd is None else cwd
                calls.append(args)
                if args == ('rev-parse', 'HEAD'):
                    return b'synthetic-head\n'
                if args == ('diff', 'HEAD', '--name-only', '-z'):
                    return b''
                if args == ('ls-files', '--others', '--exclude-standard', '-z'):
                    return b'notes.md\0'
                if args == ('diff', '--check'):
                    return b''
                if args[:2] == ('status', '--short'):
                    return b'?? notes.md\n'
                if mode == 'apply-failure' and args[0] == 'apply':
                    raise RuntimeError('B5_SYNTHETIC_APPLY_FAILURE')
                return real_git(*args, cwd=cwd, allowed=allowed)

            module.git = git
            if mode == 'output-collision':
                collision = root / '.local-work/review-deliveries/synthetic.json'
                collision.parent.mkdir(parents=True)
                collision.write_bytes(b'preserve-existing-receipt')
            try:
                result = module.package('synthetic', baseline)
                assert mode == 'normal'
                assert all(x['scratch_removed'] for x in result['patches'].values())
                assert len(result['files']) == 1
                outcome = 'PASS full synthetic control flow'
            except (RuntimeError, AssertionError) as e:
                if mode == 'apply-failure':
                    assert str(e) == 'B5_SYNTHETIC_APPLY_FAILURE'
                    assert (root / '.local-work/diffs/synthetic-complete.diff').is_file()
                    outcome = 'PASS exception cleanup; completed patch retained'
                elif mode == 'prior-work':
                    assert 'Prior work' in str(e)
                    outcome = 'PASS rejects ambiguous prior work'
                elif mode == 'output-collision':
                    assert 'fresh label' in str(e)
                    assert collision.read_bytes() == b'preserve-existing-receipt'
                    outcome = 'PASS exclusive outputs preserved'
                else:
                    raise
            local = root / '.local-work/review-patches'
            assert not local.exists() or not list(local.iterdir())
            results.append(dict(mode=mode, outcome=outcome, git_calls=len(calls)))
            (OUT / 'successor-tests.json').write_text(json.dumps(results, indent=2) + '\n',
                                                    encoding='utf8', newline='\n')
            module.git = real_git
        assert set(SCRATCH.iterdir()) == initial
    print(json.dumps(results))


if __name__ == '__main__':
    run()
