# SPDX-License-Identifier: GPL-3.0-or-later
"""Read legacy receipts/methods; write fresh ignored aggregate accounting only.

No historical payload rehash. Current stat sizes are expressly not historical I/O
measurements. Intake/reuse hashes cover every actual source used by this audit.
Calls the unchanged owned save-protection helper before/after; never repairs saves.
"""
import argparse
from collections import Counter, defaultdict
import csv
import datetime
import hashlib
import json
import ntpath
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '.local-work/preservation-verification'
DOC = ROOT / 'docs/experiments/preservation-verification-optimization'
FOLDERS = dict(D5C='resource-population-lifecycle', D5D='resource-construction-demand',
               D5E='resource-source-decisions', D5G='resource-predictability-contrast')


def pin(p):
    with Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('x', encoding='utf8', newline='\n') as f:
        json.dump(value, f, indent=2)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def norm(p):
    return ntpath.normcase(ntpath.normpath(p))


def sources():
    paths = [ROOT / p for p in ('AGENTS.md', 'README.md', 'WORKFLOW.md', 'THIRD_PARTY_POLICY.md',
        'docs/CHARTER.md', 'docs/RESEARCH_STATE.md', 'docs/EVIDENCE_STANDARD.md',
        'docs/RESEARCH_EXECUTION_PROTOCOL.md', 'docs/SAVE_PROTECTION.md', 'docs/EDITORIAL_STANDARD.md',
        'docs/PERMISSIONS.md', 'docs/PUBLICATION.md', 'docs/PROVENANCE.md',
        'docs/templates/completion-contract.md', 'docs/reviewers/research-completion-reviewer.md',
        'docs/implementation-briefs/CODEX_BRIEF_SOR_preservation_audit_optimization.md',
        'research/review_package.py', 'research/editorial/screen.py',
        'research/resource-tungsten-acquisition/protection.py',
        'research/resource-tungsten-acquisition/save_policy.py',
        'research/resource-tungsten-acquisition/save_policy.json',
        'research/resource-carinae-source-context/save_policy.py',
        'research/resource-carinae-source-context/save_policy.json',
        '.local-work/resource-carinae-source-context/protected-before.json')]
    for folder in (*FOLDERS.values(), 'resource-feynman-d5'):
        for n in ('audit-before.json', 'audit-after.json', 'audit-before-time.json', 'audit-after-time.json',
                  'audit-before-method.py', 'worktree-start.json', 'input-pins.json', 'protected-before.json', 'protected-after.json'):
            p = ROOT / '.local-work' / folder / n
            if p.is_file():
                paths.append(p)
        for p in (ROOT / 'research' / folder / 'audit.py', ROOT / 'docs/experiments' / folder / 'review.md'):
            if p.is_file():
                paths.append(p)
    paths.extend(ROOT / '.local-work/resource-source-decisions' / n for n in ('support.py', 'final_checks.py'))
    return sorted(set(paths))


def protect(phase):
    space = {d: shutil.disk_usage(d).free for d in ('C:/', 'D:/')}
    if min(space.values()) < 40_000_000_000:
        raise RuntimeError('Free-space guard')
    if subprocess.check_output(['powershell', '-NoProfile', '-Command',
            '@(Get-Process Starfield -ErrorAction SilentlyContinue).Count'], text=True).strip() != '0':
        raise RuntimeError('Game is running; no process intervention authorized')
    sys.path.insert(0, str(ROOT / 'research/resource-tungsten-acquisition'))
    import protection
    t = time.perf_counter()
    result = protection.audit()
    write(OUT / f'protected-{phase}.json', result)
    if result['changes']:
        raise RuntimeError('Protected changes; stop without repair')
    return dict(wall_seconds=time.perf_counter()-t, rows=result['count'],
                transients=len(result['excluded_live_transients']), free_bytes=space, changes=0)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('phase', choices=['intake', 'reconstruct', 'reuse'])
    args = ap.parse_args()
    if args.phase == 'intake':
        OUT.mkdir(parents=True, exist_ok=True)
        write(OUT / 'start.json', dict(head=git('rev-parse', 'HEAD'),
            index_sha256=pin(ROOT / '.git/index'), status=subprocess.check_output(['git', 'status', '--short'], cwd=ROOT, text=True),
            utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), branch=git('branch', '--show-current')))
        write(OUT / 'input-pins.json', {str(p): pin(p) for p in sources()})
        write(OUT / 'protection-before-cost.json', protect('before'))
        return
    expected = json.loads((OUT / 'input-pins.json').read_text())
    # Navigation/state edits are outputs, so their before bytes remain in HEAD.
    mutable = {str(ROOT / 'docs/RESEARCH_STATE.md')}
    for p, digest in expected.items():
        if args.phase == 'reuse' and p in mutable:
            if hashlib.sha256(subprocess.check_output(['git', 'show', 'HEAD:docs/RESEARCH_STATE.md'], cwd=ROOT)).hexdigest() != digest:
                raise RuntimeError('Before-state not preserved in HEAD')
        elif pin(p) != digest:
            raise RuntimeError('Task input changed: ' + p)
    if args.phase == 'reuse':
        start = json.loads((OUT / 'start.json').read_text())
        assert git('rev-parse', 'HEAD') == start['head']
        assert pin(ROOT / '.git/index') == start['index_sha256']
        assert not git('diff', '--cached', '--name-only')
        write(OUT / 'protection-after-cost.json', protect('after'))
        write(OUT / 'reuse.json', dict(input_hashes_checked=len(expected), protected_changes=0, head_index_equal=True))
        return
    inventories = {}
    summary = {}
    allpaths = {}
    for label, folder in FOLDERS.items():
        local = ROOT / '.local-work' / folder
        before = json.loads((local / 'audit-before.json').read_text())
        after = json.loads((local / 'audit-after.json').read_text())
        assert before == after
        inventories[label] = {norm(p): digest for p, digest in before['pins'].items()}
        allpaths.update({norm(p): p for p in before['pins']})
        summary[label] = dict(logical_pins=len(before['pins']), normalized_paths=len(inventories[label]),
            before_after_equal=True, receipt_sha256=pin(local / 'audit-before.json'),
            completion_before=json.loads((local / 'audit-before-time.json').read_text())['utc'],
            completion_after=json.loads((local / 'audit-after-time.json').read_text())['utc'],
            elapsed_seconds='UNKNOWN', actual_bytes_read='UNKNOWN', cpu_seconds='UNKNOWN', peak_memory='UNKNOWN')
    reconciliation = []
    for a, b in (('D5C','D5D'), ('D5D','D5E'), ('D5E','D5G')):
        old, new = inventories[a], inventories[b]
        common = old.keys() & new.keys()
        reconciliation.append(dict(before=a, after=b, added=len(new.keys()-old.keys()),
            removed=len(old.keys()-new.keys()), changed=sum(old[p] != new[p] for p in common), common=len(common)))
    stats = {}
    t = time.perf_counter()
    for p in inventories['D5G']:
        try:
            s = Path(allpaths[p]).stat()
            stats[p] = dict(bytes=s.st_size, links=s.st_nlink, file_id=s.st_ino, device=s.st_dev)
        except OSError as exc:
            stats[p] = dict(bytes=None, error=type(exc).__name__)
    # Categories are explicit heuristics over paths, not semantic reclassification.
    used = {norm(p) for p in json.loads((ROOT / '.local-work/resource-predictability-contrast/input-pins.json').read_text())}
    rows = []
    for p in inventories['D5G']:
        rel = p.split('\\.local-work\\', 1)[-1] if '\\.local-work\\' in p else ''
        directory = '.local-work/' + rel.split('\\')[0] if rel else 'outside-local-work'
        ext = Path(p).suffix.lower() or '(none)'
        if ext == '.sfs' or '\\saves\\' in p or 'backup' in p:
            category = 'critical-original-or-backup-candidate'
        elif p in used:
            category = 'explicit-D5G-input-pin'
        elif ext in ('.exe', '.esm', '.ba2', '.gdt', '.gbf', '.ulock', '.db') or 'ghidra' in p:
            category = 'critical-installed-or-analysis-candidate'
        elif any(n in p for n in ('\\review', '\\build', '\\qualification', 'audit-', 'checks', 'receipt', 'package', 'manifest')):
            category = 'historical-derivative-or-diagnostic'
        elif ext in ('.raw', '.sro1', '.tsv', '.jsonl', '.png', '.bin', '.zip', '.7z'):
            category = 'historical-evidence-candidate'
        else:
            category = 'other-or-unknown'
        rows.append(dict(path=p, directory=directory, extension=ext, category=category,
                         protection='strict-historical-pin', **stats[p]))
    groups = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        for dimension in ('directory','extension','category','protection'):
            g = groups[(dimension,r[dimension])]
            g[0] += 1
            if r['bytes'] is None:
                g[2] += 1
            else:
                g[1] += r['bytes']
    DOC.mkdir(parents=True, exist_ok=True)
    with (DOC / 'inventory-breakdown.csv').open('x', encoding='utf8', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['dimension','group','logical_pins','current_stat_bytes','missing_stat'])
        for (dimension, group), values in sorted(groups.items()):
            writer.writerow([dimension,group,*values])
    union = {}
    for folder in ('resource-feynman-d5','resource-construction-demand'):
        union.update(json.loads((ROOT / f'.local-work/{folder}/audit-after.json').read_text())['pins'])
    summary['D5G']['expected_verification_calls_before'] = len(union)
    summary['D5G']['inventory_hash_calls_before'] = len(inventories['D5G'])
    summary['D5G']['inventory_hash_calls_after'] = len(inventories['D5G'])
    summary['D5G']['normalized_inherited_expected'] = len({norm(p) for p in union})
    first = json.loads((ROOT / '.local-work/resource-feynman-d5/audit-after.json').read_text())['pins']
    second = json.loads((ROOT / '.local-work/resource-construction-demand/audit-after.json').read_text())['pins']
    summary['D5G']['expected_union_conflicts'] = sum(1 for p,d in first.items() if p in second and second[p] != d)
    write(OUT / 'reconstruction.json', dict(summary=summary, reconciliation=reconciliation,
        metadata_scan_seconds=time.perf_counter()-t, unique_current_file_ids=len({(r.get('device'),r.get('file_id')) for r in rows if r['bytes'] is not None}),
        metadata_only=True, current_size_total=sum(r['bytes'] or 0 for r in rows),
        note='Current stat sizes, not measured historical read I/O; path categories overlap scientific roles.'))
    write(OUT / 'private-inventory.json', rows)
    print(json.dumps(dict(summary=summary, reconciliation=reconciliation), indent=2))


if __name__ == '__main__':
    main()
