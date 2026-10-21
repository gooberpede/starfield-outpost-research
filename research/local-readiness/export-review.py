# SPDX-License-Identifier: GPL-3.0-or-later
"""Owned review-export method adapted from runtime/session-tools/export_review.py
at HEAD 0906c66c950870a25869aaab522d22fb9c9d11e7. Reads Git/text and qualification logs;
writes exclusive ignored patches/manifests and .local-work/review-patches disposable apply trees.
No index/ref/stage/commit/push/network mutation. Exact byte verification both ways.
"""
import argparse
import difflib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'runtime/session-tools'))
from common import fresh, guard, sha

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT/'.local-work/local-readiness/review-01'
TASK = 'local-readiness-review01'
BRIEF = 'docs/implementation-briefs/CODEX_BRIEF_SOR_local_readiness_native_observation.md'
HEAD = '0906c66c950870a25869aaab522d22fb9c9d11e7'
ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_CEILING_DIRECTORIES=str(ROOT/'.local-work'))


def git(*args, cwd=ROOT):
    r = subprocess.run(['git', '-c', 'core.autocrlf=false', *args], cwd=cwd, env=ENV, capture_output=True)
    if r.returncode:
        raise RuntimeError(repr(args) + r.stderr.decode(errors='replace'))
    return r.stdout


def diff(name, old, new):
    parts = ['diff --git a/' + name + ' b/' + name + '\n']
    if old is None:
        parts.append('new file mode 100644\n')
    if new is None:
        parts.append('deleted file mode 100644\n')
    lines = difflib.unified_diff((old or b'').decode('utf8').splitlines(keepends=True),
                                 (new or b'').decode('utf8').splitlines(keepends=True),
                                 fromfile='/dev/null' if old is None else 'a/'+name,
                                 tofile='/dev/null' if new is None else 'b/'+name, lineterm='\n')
    for line in lines:
        parts.append(line if line.endswith('\n') else line+'\n\\ No newline at end of file\n')
    return ''.join(parts).encode('utf8')


def main():
    global BASE, TASK
    ap=argparse.ArgumentParser();ap.add_argument('--name',required=True);a=ap.parse_args()
    assert re.fullmatch('[a-z0-9-]+',a.name)
    BASE=ROOT/'.local-work/local-readiness'/a.name;TASK='local-readiness-'+a.name
    guard()
    BASE.mkdir(parents=True, exist_ok=False)
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    index_pin = sha(ROOT/'.git/index')
    assert not git('diff', '--cached', '--name-only')
    changed = git('diff', 'HEAD', '--name-only', '-z').decode().split('\0')[:-1]
    new = git('ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')[:-1]
    names = sorted(set(changed+new))
    allowed = {'README.md','CREDITS.md','docs/README.md','docs/RESEARCH_STATE.md','docs/SOURCES.md','docs/function-register.md','docs/state-register.md','docs/subsystems/initial-map.md','docs/experiments/README.md','docs/experiments/evidence/README.md','docs/implementation-briefs/README.md','runtime/README.md',BRIEF}
    assert all(n in allowed or n.startswith(('runtime/session-tools/','runtime/local-readiness-080/','docs/experiments/local-readiness/','research/local-readiness/')) for n in names)
    current = {n: (ROOT/n).read_bytes() if (ROOT/n).exists() else None for n in names}
    before = {n: git('show', 'HEAD:'+n) if n in changed else None for n in names}
    task = [n for n in names if n != BRIEF]
    link_checks = 0
    for n in names:
        text = (current[n] or b'').decode('utf8')
        if n in task:
            assert not text.startswith('\ufeff'), n
            assert '\r' not in text, n
            if n in new:
                assert all(line.rstrip() == line for line in text.splitlines()), n
        if n in task and n.endswith('.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                path = target.split('#')[0].strip('<>')
                if not path or re.match('[A-Za-z]+:', path):
                    continue
                if not (ROOT/n).parent.joinpath(path).resolve().exists():
                    assert target in (before[n] or b'').decode('utf8'), (n, target)
                link_checks += 1
    git('diff', '--check')
    tests = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', str(ROOT/'runtime/session-tools'),
                            '-p', 'test_*.py', '-v'], capture_output=True)
    (BASE/'tests.txt').write_bytes(tests.stdout+tests.stderr)
    assert tests.returncode == 0
    patches = {}
    for label, paths in [('task-only', task), ('complete', names)]:
        data = b''.join(diff(n, before[n], current[n]) for n in paths)
        path = ROOT/('.local-work/diffs/'+TASK+'-'+label+'.diff')
        path.parent.mkdir(exist_ok=True)
        with path.open('xb') as f:
            f.write(data)
        # Independent path inventory plus byte-for-byte reconstruction, not only
        # reverse applicability against a possibly incomplete working-tree patch.
        patch_names = re.findall(rb'^diff --git a/(.*?) b/', data, re.M)
        assert [n.decode() for n in patch_names] == paths
        review_scratch = ROOT / '.local-work/review-patches'
        review_scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='sor-session-review-', dir=review_scratch) as scratch_directory:
            scratch = Path(scratch_directory)
            for n in paths:
                if before[n] is not None:
                    p = scratch/n
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_bytes(before[n])
            git('apply', '--no-index', '--check', str(path), cwd=scratch)
            git('apply', '--no-index', str(path), cwd=scratch)
            assert all((scratch/n).read_bytes() == current[n] if current[n] is not None else not (scratch/n).exists() for n in paths)
            git('apply', '--no-index', '--reverse', '--check', str(path), cwd=scratch)
            git('apply', '--no-index', '--reverse', str(path), cwd=scratch)
            assert all((scratch/n).read_bytes() == before[n] if before[n] is not None else not (scratch/n).exists() for n in paths)
            patches[label] = dict(path=str(path), sha256=sha(path), bytes=len(data), paths=paths,
                                  scratch=str(scratch), forward_check=True, forward_apply_exact=True,
                                  reverse_check=True, reverse_apply_exact=True)
    (BASE/'git-status-short.txt').write_bytes(git('status', '--short'))
    evidence=ROOT/'.local-work/local-readiness'
    private_receipts=[evidence/'baseline.json',evidence/'save-menu.json',evidence/'checks-01/qualification.json',evidence/'reference-070/coverage.json']
    build=evidence/'builds/qualification-03'
    private_receipts += [p for p in build.glob('*') if p.is_file() and p.suffix in ('.json','.txt','.zip','.dll')]
    exclusions=[dict(path=str(evidence),kind='LOCAL-ONLY raw fixtures/build DLL ZIP/private metadata and failure receipts',hashes=[dict(path=str(p),sha256=sha(p)) for p in private_receipts]),
                dict(path=str(ROOT/'.local-work'),kind='Original protected saves/captures/native exports and prior build trees excluded',hash_inventory=str(evidence/'baseline.json')),
                dict(path='D:/ReverseEngineering; installed game/save directories; D:/tools; .local-work/review-patches',kind='Proprietary originals/databases and disposable review apply trees excluded')]
    fresh(BASE/'exclusions.json', exclusions)
    fresh(BASE/'changed-files.json', [dict(path=n, sha256=sha(ROOT/n), classification='supplied unchanged brief' if n == BRIEF else 'task-authored or modified text') for n in names])
    fresh(BASE/'package.json', dict(status='PASS', head=HEAD, index_sha256=index_pin, staged_changes=False,
                                   complete_paths=names, task_paths=task, patches=patches, internal_links_checked=link_checks,
                                   new_file_whitespace=True, git_diff_check=True, tests_returncode=tests.returncode,
                                   exclusions='exclusions.json', content_manifest='changed-files.json'))
    assert sha(ROOT/'.git/index') == index_pin
    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    assert not git('diff', '--cached', '--name-only')
    print(json.dumps(dict(status='PASS', complete_files=len(names), task_files=len(task),
                          package=str(BASE/'package.json'), patches=patches), indent=2))


if __name__ == '__main__':
    main()
