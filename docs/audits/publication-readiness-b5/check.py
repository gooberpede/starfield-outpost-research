"""Read-only B5 proposal validator, stdlib only. From repository root:
python -B docs/audits/publication-readiness-b5/check.py
Requires the temporary local-only .local-work/b5/deletion-candidates.json;
not distributed with a public checkout. No run required for delivery correction.
Reads authored ledgers, exact candidates and retained copies. Writes nothing,
executes no entrypoint or target, and supplies no B5-B deletion authority.
"""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOC = Path(__file__).resolve().parent


def check():
    proposal = json.loads((ROOT / '.local-work/b5/deletion-candidates.json').read_text(encoding='utf8'))
    assert proposal['status'] == 'PROPOSED, NOT AUTHORIZED'
    rows = proposal['candidates']
    assert len({r['id'] for r in rows}) == len(rows)
    paths = {Path(r['absolute_resolved_path']).resolve() for r in rows}
    assert len(paths) == len(rows)
    roots = {ROOT / '.local-work' / n for n in ('diffs', 'scratch', 'screengrabs', 'savegames')}
    assert not roots & paths
    cache = {}

    def digest(p):
        if p not in cache:
            with p.open('rb') as stream:
                cache[p] = hashlib.file_digest(stream, 'sha256').hexdigest()
        return cache[p]

    total = unblocked = 0
    for r in rows:
        p = Path(r['absolute_resolved_path'])
        owner = ROOT / r['relative_owner_root'] if r['relative_owner_root'] == '.local-work' else Path(r['relative_owner_root'])
        assert p == p.resolve() and p.is_relative_to(owner.resolve())
        for ancestor in (p, *p.parents):
            assert not ancestor.lstat().st_file_attributes & 0x400
            if ancestor == owner:
                break
        assert r['disposition'] in ('PROPOSED_NOT_AUTHORIZED', 'PROPOSED_BLOCKED_REFERENCE')
        if r['nature'] == 'file':
            assert p.is_file() and p.stat().st_size == r['measured_bytes']
            assert p.stat().st_ino == r['file_id'] and p.stat().st_dev == r['device']
            assert p.stat().st_nlink == r['link_count'] == 1
            assert digest(p) == r['sha256']
            assert p.suffix.lower() not in ('.sfs', '.zip', '.bin', '.wal', '.dmp', '.jpg', '.png', '.dll', '.json', '.gpr')
            recovery = r['duplication_proof']
            retained = Path(recovery['path']).resolve()
            assert retained not in paths and retained.is_file()
            assert retained.stat().st_size == r['measured_bytes']
            assert digest(retained) == r['sha256'] == recovery['sha256']
            assert r['estimated_recoverable_file_bytes'] == r['measured_bytes']
            assert bool(r['reference_audit']['exact_hits']) == (r['disposition'] == 'PROPOSED_BLOCKED_REFERENCE')
            total += r['measured_bytes']
            if r['disposition'] == 'PROPOSED_NOT_AUTHORIZED':
                unblocked += r['measured_bytes']
        else:
            assert r['nature'] == 'enumerated_empty_directory_tree'
            assert p.parent == Path('C:/Users/User/AppData/Local/Temp')
            descendants = list(p.rglob('*'))
            assert all(x.is_dir() and not x.lstat().st_file_attributes & 0x400 for x in descendants)
            assert sorted(x.relative_to(p).as_posix() for x in descendants) == r['enumerated_descendants']
            assert r['measured_bytes'] == r['estimated_recoverable_file_bytes'] == r['file_count'] == 0
    ledger = list(csv.DictReader((DOC / 'retention-ledger.csv').open(encoding='utf8')))
    top = [r for r in ledger if r['path'].count('/') == 1 or r['path'] == '.local-work [loose root files]']
    assert sum(int(r['measured_bytes']) for r in top) == 33_963_351_165
    assert sum(int(r['files']) for r in top) == 90_914
    assert sum(int(r['unblocked_proposed_file_bytes']) for r in top) == unblocked
    print(json.dumps(dict(candidate_entries=len(rows), duplicate_file_bytes=total,
                          unblocked_proposed_file_bytes=unblocked,
                          unique_files_rehashed=len(cache), top_level_accounting='PASS',
                          deletion_authorized=False)))


if __name__ == '__main__':
    check()
