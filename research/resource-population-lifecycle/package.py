# SPDX-License-Identifier: GPL-3.0-or-later
"""Adapt owned session-tools exact patch exporter under SOR-P-0002.

Reads Git/text and D5C integrity receipts; writes fresh ignored review patches, manifests
and disposable forward/reverse application trees. No index/ref/network writes.
Requires the baseline audit and a completed editorial screen. Stdlib only.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'research/resource-population-lifecycle'))
from audit import ROOT, pin, write
sys.path.insert(0, str(ROOT / 'runtime/session-tools'))
from export_review import diff, git


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--label', required=True)
    args = ap.parse_args()
    assert re.fullmatch('[a-z0-9-]+', args.label)
    local = ROOT / '.local-work/resource-population-lifecycle'
    out = local / args.label
    out.mkdir(exist_ok=False)
    before = json.loads((local / 'audit-before.json').read_text(encoding='utf8'))
    assert git('rev-parse', 'HEAD').decode().strip() == before['head']
    assert pin(ROOT / '.git/index') == before['index_sha256']
    assert not git('diff', '--cached', '--name-only')
    changed = git('diff', 'HEAD', '--name-only', '-z').decode().split('\0')[:-1]
    new = git('ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')[:-1]
    names = sorted(set(changed + new))
    brief = 'docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5C_resource_source_population_lifecycle.md'
    shared = {'CREDITS.md', 'docs/PERMISSIONS.md', 'docs/SOURCES.md', 'docs/RESEARCH_STATE.md',
              'docs/experiments/README.md', 'docs/subsystems/README.md',
              'docs/implementation-briefs/README.md', brief}
    assert all(n in shared or n.startswith(('research/resource-population-lifecycle/',
               'docs/experiments/resource-population-lifecycle/')) for n in names)
    current = {n: (ROOT / n).read_bytes() for n in names}
    old = {n: git('show', 'HEAD:' + n) if n in changed else None for n in names}
    links = 0
    for n in names:
        text = current[n].decode('utf8')
        if n != brief:
            assert not text.startswith('\ufeff') and '\r' not in text, n
            if n in new:
                assert all(line.rstrip() == line for line in text.splitlines()), n
        if n.endswith('.md'):
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                path = target.split('#')[0].strip('<>')
                if not path or re.match('[A-Za-z]+:', path):
                    continue
                if not (ROOT / n).parent.joinpath(path).resolve().exists():
                    assert target in (old[n] or b'').decode('utf8'), (n, target)
                links += 1
    git('diff', '--check')
    screen = subprocess.run([sys.executable, '-B', str(ROOT / 'research/editorial/screen.py'), '--changed'],
                            cwd=ROOT, capture_output=True)
    (out / 'editorial-screen.json').write_bytes(screen.stdout)
    assert screen.returncode == 0, screen.stdout.decode()
    patches = {}
    for label, paths in [('complete', names), ('task-only', [n for n in names if n != brief])]:
        data = b''.join(diff(n, old[n], current[n]) for n in paths)
        path = ROOT / f'.local-work/diffs/rg2-d5c-{args.label}-{label}.diff'
        path.parent.mkdir(exist_ok=True)
        with path.open('xb') as stream:
            stream.write(data)
        assert re.findall(rb'^diff --git a/(.*?) b/', data, re.M) == [n.encode() for n in paths]
        scratch_root = ROOT / '.local-work/review-patches'
        scratch_root.mkdir(exist_ok=True)
        scratch = Path(tempfile.mkdtemp(prefix='rg2-d5c-', dir=scratch_root)).resolve()
        assert scratch.is_relative_to(scratch_root.resolve())
        for n in paths:
            if old[n] is not None:
                p = scratch / n
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(old[n])
        git('apply', '--no-index', '--check', str(path), cwd=scratch)
        git('apply', '--no-index', str(path), cwd=scratch)
        assert all((scratch / n).read_bytes() == current[n] for n in paths)
        git('apply', '--no-index', '--reverse', '--check', str(path), cwd=scratch)
        git('apply', '--no-index', '--reverse', str(path), cwd=scratch)
        assert all((scratch / n).read_bytes() == old[n] if old[n] is not None
                   else not (scratch / n).exists() for n in paths)
        patches[label] = dict(path=str(path), sha256=pin(path), files=len(paths),
                              forward_reverse_exact=True, scratch=str(scratch))
    (out / 'git-status-short.txt').write_bytes(git('status', '--short'))
    write(out / 'changed-files.json', [dict(path=n, bytes=len(current[n]), sha256=pin(ROOT / n),
          classification='supplied unchanged brief' if n == brief else 'task-authored/modified text') for n in names])
    write(out / 'complete-manifest.json', [dict(path=n, sha256=pin(ROOT / n)) for n in names])
    write(out / 'task-only-manifest.json', [dict(path=n, sha256=pin(ROOT / n)) for n in names if n != brief])
    exports = ROOT / '.local-work/workshop-population-rework/specialist'
    excluded = [p for p in local.rglob('*') if p.is_file() and not p.is_relative_to(out)]
    excluded += list(exports.glob('d5c-*'))
    write(out / 'exclusions.json', dict(task_local_files=[dict(path=str(p), bytes=p.stat().st_size,
        sha256=pin(p), reason='LOCAL-ONLY evidence, diagnostic, receipt or native export') for p in sorted(excluded)],
        inherited=[dict(path=str(ROOT / '.local-work'), inventory=str(local / 'audit-before.json'),
                       reason='Prior raw/native/save/corpus/build payloads; immutable inventory retained'),
                   dict(path='D:/ReverseEngineering; D:/tools; installed game and save directories',
                        reason='Proprietary inputs, analysis databases, separate tools and protected saves'),
                   dict(path=str(scratch_root), reason='Disposable exact patch application trees')]))
    write(out / 'package.json', dict(head=before['head'], index_sha256=before['index_sha256'],
        patches=patches, complete_paths=names, task_paths=[n for n in names if n != brief],
        path_inventory_exact=True, git_diff_check=True, new_file_whitespace=True,
        internal_links_checked=links, editorial_screen=True, staged_changes=False))
    assert pin(ROOT / '.git/index') == before['index_sha256']
    assert all(pin(ROOT / n) == __import__('hashlib').sha256(current[n]).hexdigest() for n in names)
    print(json.dumps(patches, indent=2))


if __name__ == '__main__':
    main()
