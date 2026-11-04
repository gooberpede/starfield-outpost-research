# N2 source-informed adaptation of owned d5ao_delivery.py; current clean baseline.
# SPDX-License-Identifier: GPL-3.0-or-later
"""Preserve D5AO source identities and export exact review patches offline.

SOR-P-0002: adapts owned d5am_delivery.py and export_review.py methods.
The initial D5AO fingerprint is projected without changing its original bytes.
Reads Git HEAD/index, changed UTF-8 text and task-local artifacts. Writes only
exclusive receipts under the D5AO local directory, local diff patches and
standalone review trees. Uses installed Python stdlib and Git; never stages, changes
refs, operates a game, opens databases or writes protected evidence. Baseline
must run before tracked edits. Export refuses unrelated source drift.
"""
import sys
import os
if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE', '') not in ('', '0'):
    raise RuntimeError('Use pinned Python -E -B without optimization')

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from d5ad_baseline import guard

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/d5ao/n2-live01'
ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_CEILING_DIRECTORIES=str(ROOT / '.local-work'))
BRIEF = 'docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AO_GC10_observer_perturbation_measurement_validity.md'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def hashes(paths):
    """Hash independent immutable inputs with bounded I/O concurrency."""
    with ThreadPoolExecutor(max_workers=4) as pool:
        return dict(zip(paths, pool.map(sha, paths)))


def git(*args, cwd=ROOT):
    p = subprocess.run(['git', '-c', 'core.autocrlf=false', *args], cwd=cwd,
                       env=ENV, capture_output=True)
    if p.returncode:
        raise RuntimeError((args, p.stderr.decode(errors='replace')))
    return p.stdout


def write(path, value):
    with path.open('x', encoding='utf8', newline='\n') as stream:
        stream.write(json.dumps(value, indent=2) + '\n')


def allowed(name):
    return name in {'docs/implementation-briefs/CODEX_AMENDMENT_SOR_D5AO_N2_live_2026-11-04.md', 'CREDITS.md', 'docs/SOURCES.md', 'docs/RESEARCH_STATE.md',
                    'docs/implementation-briefs/README.md',
                    'research/resource-retained-population/D5AMOwnerCensus.java',
                    'docs/experiments/resource-retained-population/resource-generation-gameplay-checklist.md'} or name.startswith((
                        'docs/experiments/resource-retained-population/d5ao-',
                        'docs/experiments/resource-retained-population/run-card-d5ao-',
                        'research/resource-retained-population/d5ao_',
                        'research/resource-retained-population/d5ao-',
                        'runtime/construction-winner/d5ao_'))


def baseline():
    guard()
    if any(p.is_symlink() or p.is_junction() for p in (LOCAL,*LOCAL.parents)):
        raise ValueError('Reparse output path')
    LOCAL.mkdir(parents=True, exist_ok=True)
    if git('diff', 'HEAD', '--name-only'):
        raise ValueError('Tracked changes already exist; inspect before preserving baseline')
    paths = git('ls-files', '-z').decode().split('\0')[:-1]
    result = dict(head=git('rev-parse', 'HEAD').decode().strip(),
                  index_sha256=sha(ROOT / '.git/index'),
                  supplied_brief=dict(path=BRIEF, sha256=sha(ROOT / BRIEF)),
                  tracked={n: sha(ROOT / n) for n in paths if (ROOT / n).is_file()},
                  scope='Tracked source preservation; raw/sealed provenance is separately authenticated by chronology audit.')
    write(LOCAL / 'source-baseline02.json', result)
    print(json.dumps(dict(head=result['head'], tracked=len(result['tracked']))))


def export(label):
    if not re.fullmatch('[a-z0-9-]+', label):
        raise ValueError('Simple fresh label required')
    guard()
    if any(p.is_symlink() or p.is_junction() for p in (LOCAL,*LOCAL.parents)):
        raise ValueError('Reparse output path')
    baseline = json.loads((LOCAL / 'source-baseline02.json').read_bytes())
    if git('rev-parse', 'HEAD').decode().strip() != baseline['head'] or sha(ROOT / '.git/index') != baseline['index_sha256']:
        raise ValueError('HEAD/index drift')
    if sha(ROOT / BRIEF) != baseline['supplied_brief']['sha256']:
        raise ValueError('Supplied brief changed')
    changed = git('diff', 'HEAD', '--name-only', '-z').decode().split('\0')[:-1]
    untracked = git('ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')[:-1]
    names = sorted(set(changed + untracked))
    task = [n for n in names if n != BRIEF]
    if any(not allowed(n) for n in task):
        raise ValueError('Unattributable source changes: ' + repr([n for n in task if not allowed(n)]))
    protected=[n for n in baseline['tracked'] if n not in task]
    preserved=hashes([ROOT/n for n in protected])
    for n in protected:
        if preserved[ROOT/n] != baseline['tracked'][n]:
            raise ValueError('Protected tracked source changed: ' + n)
    current = {n: (ROOT / n).read_bytes() if (ROOT / n).is_file() else None for n in names}
    old = {n: git('show', 'HEAD:' + n) if n in changed else None for n in names}
    links = []
    for n in names:
        text = (current[n] or b'').decode('utf8')
        if n in task and (text.startswith('\ufeff') or '\r' in text or any(s.rstrip() != s for s in text.splitlines())):
            raise ValueError('Authored encoding/whitespace: ' + n)
        if n.endswith('.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                path = target.split('#')[0].strip('<>')
                if not path or re.match('[A-Za-z]+:', path):
                    continue
                exists = (ROOT / n).parent.joinpath(path).resolve().exists()
                if not exists and n in task and target not in (old[n] or b'').decode('utf8'):
                    raise ValueError('New broken link: ' + n + ' ' + target)
                links.append(dict(file=n, target=target, exists=exists))
    git('diff', '--check')
    spec = importlib.util.spec_from_file_location('owned_diff', ROOT / 'runtime/retained-population/export_review.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    out = LOCAL / label
    out.mkdir(exist_ok=False)
    patchdir = ROOT / '.local-work/diffs'
    patchdir.mkdir(exist_ok=True)
    parent = ROOT / '.local-work/review-patches'
    parent.mkdir(exist_ok=True)
    patches = {}
    for coverage, paths in (('task-only', task), ('complete', names)):
        guard()
        payload = b''.join(module.diff(n, old[n], current[n]) for n in paths)
        if [n.decode() for n in re.findall(rb'^diff --git a/(.*?) b/', payload, re.M)] != paths:
            raise ValueError('Patch path coverage')
        patch = patchdir / f'd5ao-n2-{label}-{coverage}.diff'
        with patch.open('xb') as stream:
            stream.write(payload)
        scratch = Path(tempfile.mkdtemp(prefix='d5ao-' + coverage + '-', dir=parent)).resolve()
        if not scratch.is_relative_to(parent.resolve()):
            raise ValueError('Scratch containment')
        for n in paths:
            if old[n] is not None:
                p = scratch / n
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(old[n])
        git('apply', '--check', str(patch), cwd=scratch)
        git('apply', str(patch), cwd=scratch)
        if any(((scratch / n).read_bytes() if (scratch / n).exists() else None) != current[n] for n in paths):
            raise ValueError('Forward bytes differ')
        git('apply', '--reverse', '--check', str(patch), cwd=scratch)
        git('apply', '--reverse', str(patch), cwd=scratch)
        if any(((scratch / n).read_bytes() if (scratch / n).exists() else None) != old[n] for n in paths):
            raise ValueError('Reverse bytes differ')
        patches[coverage] = dict(path=str(patch), sha256=sha(patch), paths=paths, forward_reverse_exact_bytes=True)
    excluded_paths=[p for p in sorted(LOCAL.rglob('*')) if p.is_file() and out not in p.parents]
    excluded_hashes=hashes(excluded_paths)
    exclusions = [dict(path=p.relative_to(ROOT).as_posix(), bytes=p.stat().st_size, sha256=excluded_hashes[p]) for p in excluded_paths]
    result = dict(head=baseline['head'], index_sha256=baseline['index_sha256'],
                  files={n: dict(sha256=hashlib.sha256(current[n]).hexdigest() if current[n] is not None else None,
                                 bytes=len(current[n] or b''), task_authored=n in task, supplied_brief=n == BRIEF) for n in names},
                  patches=patches, links=links, exclusions=exclusions,
                  other_exclusions='Original raw sessions, archives, saves, databases and prior candidates remain local; chronology receipts bind selected protected inputs. This is source patch coverage, not publication clearance.',
                  checks=dict(inventory='PASS', forward_reverse_exact_bytes='PASS', encoding_whitespace='PASS', links='PASS', git_diff_check='PASS'),
                  method_sha256=sha(__file__))
    if any(((ROOT / n).read_bytes() if (ROOT / n).is_file() else None) != current[n] for n in names):
        raise ValueError('Authored source changed during snapshot export; retain partial outputs and use a fresh label')
    latest=sorted(set(git('diff','HEAD','--name-only','-z').decode().split('\0')[:-1]+
                      git('ls-files','--others','--exclude-standard','-z').decode().split('\0')[:-1]))
    if latest!=names or hashes([ROOT/n for n in protected])!=preserved:
        raise ValueError('Source inventory or unrelated tracked bytes changed during export')
    guard()
    with (out / 'status.txt').open('xb') as stream:
        stream.write(git('status', '--short', '--untracked-files=all'))
    write(out / 'delivery.json', result)
    if sha(ROOT / '.git/index') != baseline['index_sha256'] or git('rev-parse', 'HEAD').decode().strip() != baseline['head']:
        raise ValueError('HEAD/index drift during export')
    print(json.dumps(dict(out=str(out), files=len(names), task_files=len(task), checks=result['checks'])))


if __name__ == '__main__':
    if sys.argv[1:] == ['baseline']:
        baseline()
    elif len(sys.argv) == 3 and sys.argv[1] == 'export':
        export(sys.argv[2])
    else:
        raise SystemExit('Usage: d5am_delivery.py baseline | export FRESH_LABEL')
