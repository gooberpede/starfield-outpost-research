# SPDX-License-Identifier: GPL-3.0-or-later
"""Current successor for retired task-bound review exporters.

From repository root: python -B research/review_package.py --label NAME
    --baseline clean-start.json [--supplied-brief repository/relative.md]
Baseline schema: head, index_sha256, status from a read-only starting receipt.
Only an initially clean tree plus the supplied untracked brief is supported.
Mixed/prior work needs a separately scoped exporter with exact before bytes.
Stdlib and existing Git only. Reads HEAD/index, changed tracked and untracked
UTF-8 text; writes exclusive ignored patches and a JSON/status receipt. Rejects
binary data and reparse paths. Applies only to newly allocated self-cleaning
plain trees under .local-work/review-patches with parent Git discovery blocked.
No target execution, network, index/ref writes, or cleanup of existing files.
Original implementation for B5; method follows WORKFLOW's review contract.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0',
           GIT_CEILING_DIRECTORIES=str(ROOT / '.local-work'))


def git(*args, cwd=ROOT, allowed=(0,)):
    p = subprocess.run(['git', '-c', 'core.autocrlf=false', '--no-pager', *args],
                       cwd=cwd, env=ENV, capture_output=True)
    if p.returncode not in allowed:
        raise RuntimeError((args, p.returncode, p.stderr.decode(errors='replace')))
    return p.stdout


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def guarded(path):
    path = Path(path).absolute()
    assert path.is_relative_to(ROOT), path
    for p in (path, *path.parents):
        if p.exists():
            assert not p.lstat().st_file_attributes & 0x400, p
        if p == ROOT:
            break
    assert path.resolve().is_relative_to(ROOT.resolve()), path
    return path


def package(label, baseline, supplied_brief=None):
    assert re.fullmatch(r'[a-z0-9][a-z0-9-]*', label)
    space = {d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}
    assert min(space.values()) >= 40_000_000_000
    head = git('rev-parse', 'HEAD').decode().strip()
    index = pin(ROOT / '.git/index')
    start = json.loads(Path(baseline).read_text(encoding='utf8'))
    assert start['head'] == head and start['index_sha256'] == index
    expected_status = '?? ' + supplied_brief if supplied_brief else ''
    assert start['status'].strip() == expected_status, 'Prior work requires an exact before-tree exporter'
    changed = git('diff', 'HEAD', '--name-only', '-z').decode().split('\0')[:-1]
    new = git('ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')[:-1]
    names = sorted(set(changed + new))
    assert names
    if supplied_brief:
        assert supplied_brief in new
    current = {}
    for n in names:
        p = guarded(ROOT / n)
        data = p.read_bytes() if p.is_file() else None
        if data is not None:
            assert b'\0' not in data, ('binary requires explicit exclusion', n)
            data.decode('utf8')
            if n != supplied_brief:
                text = data.decode('utf8')
                assert not text.startswith('\ufeff') and '\r' not in text, n
                added = text if n in new else '\n'.join(line[1:] for line in git('diff', 'HEAD', '--', n).decode().splitlines()
                                                       if line.startswith('+') and not line.startswith('+++'))
                assert all(line.rstrip() == line for line in added.splitlines()), n
                if n.endswith('.md'):
                    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', added):
                        link = target.split('#')[0].strip('<>')
                        if link and not re.match(r'[A-Za-z]+:', link):
                            assert (p.parent / link).resolve().is_file() or (p.parent / link).resolve().is_dir(), (n, target)
        current[n] = data
    git('diff', '--check')
    old = {n: git('show', 'HEAD:' + n) if n in changed else None for n in names}
    out = guarded(ROOT / '.local-work/diffs')
    scratchroot = guarded(ROOT / '.local-work/review-patches')
    receipts = guarded(ROOT / '.local-work/review-deliveries')
    for p in (out, scratchroot, receipts):
        p.mkdir(parents=True, exist_ok=True)
    receipt = receipts / (label + '.json')
    status = receipts / (label + '-status.txt')
    targets = [out / f'{label}-{kind}.diff' for kind in ('complete', 'task-only')]
    assert not any(p.exists() for p in [receipt, status, *targets]), 'Choose a fresh label'
    patches = {}
    for kind, target in zip(('complete', 'task-only'), targets):
        paths = [n for n in names if kind == 'complete' or n != supplied_brief]
        selected = [n for n in paths if n in changed]
        data = git('diff', '--no-ext-diff', '--no-textconv', 'HEAD', '--', *selected) if selected else b''
        for n in paths:
            if n in new:
                data += git('diff', '--no-index', '--', '/dev/null', n, allowed=(1,))
        inventory = re.findall(rb'^diff --git a/(.*?) b/', data, re.M)
        assert sorted(n.decode() for n in inventory) == paths
        with target.open('xb') as f:
            f.write(data)
        with tempfile.TemporaryDirectory(prefix=label + '-', dir=scratchroot) as temporary:
            tree = Path(temporary)
            for n in paths:
                if old[n] is not None:
                    p = tree / n
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_bytes(old[n])
            git('apply', '--no-index', '--check', '--whitespace=nowarn', str(target), cwd=tree)
            git('apply', '--no-index', '--whitespace=nowarn', str(target), cwd=tree)
            assert sorted(p.relative_to(tree).as_posix() for p in tree.rglob('*') if p.is_file()) == [n for n in paths if current[n] is not None]
            assert all((tree / n).read_bytes() == current[n] if current[n] is not None else not (tree / n).exists() for n in paths)
            git('apply', '--no-index', '--reverse', '--check', str(target), cwd=tree)
            git('apply', '--no-index', '--reverse', str(target), cwd=tree)
            assert all((tree / n).read_bytes() == old[n] if old[n] is not None else not (tree / n).exists() for n in paths)
        git('apply', '--reverse', '--check', '--whitespace=nowarn', str(target))
        patches[kind] = dict(path=str(target), sha256=pin(target), bytes=len(data),
                             paths=paths, exact_forward_reverse=True,
                             actual_tree_reverse=True, scratch_removed=not tree.exists())
    assert git('rev-parse', 'HEAD').decode().strip() == head
    assert pin(ROOT / '.git/index') == index
    assert all(pin(ROOT / n) == hashlib.sha256(data).hexdigest()
               for n, data in current.items() if data is not None)
    result = dict(head=head, index_sha256=index, free_bytes=space,
                  files=[dict(path=n, bytes=len(current[n]) if current[n] is not None else 0,
                              sha256=hashlib.sha256(current[n]).hexdigest() if current[n] is not None else None,
                              kind='supplied brief' if n == supplied_brief else 'new text' if n in new else 'tracked change') for n in names],
                  patches=patches, exclusions=['All ignored local raw/binary/private evidence, tools, saves and analysis state',
                                               'Review receipts and patches themselves remain ignored'],
                  scientific_or_target_execution=False, no_staging_commit_push=True)
    with receipt.open('x', encoding='utf8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    with status.open('xb') as f:
        f.write(git('status', '--short', '--untracked-files=all'))
    print(json.dumps(dict(receipt=str(receipt), files=len(names), patches=patches), indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--label', required=True)
    parser.add_argument('--baseline', required=True)
    parser.add_argument('--supplied-brief')
    args = parser.parse_args()
    package(args.label, args.baseline, args.supplied_brief)
