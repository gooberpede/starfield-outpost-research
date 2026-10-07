"""Archive only the invoked brief's saves; never parse or write live originals.

Reads: brief, named live files (hash/metadata), existing destination if present.
Writes: exclusive new copies and JSON manifest under ignored project-local roots.
Dependencies: installed CPython standard library. No target-process effects.
Run from repository root: python save-analysis/scripts/archive_manual_corpus.py
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path.home() / 'Documents/My Games/Starfield/Saves'
DEST = ROOT / '.local-work/savegames/manual-S0-S7C'
OUT = ROOT / '.local-work/manual-S0-S7C'
BRIEF = ROOT / 'docs/implementation-briefs/CODEX_RESEARCH_BRIEF_manual_save_corpus_S0-S7C.md'


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def metadata(path):
    s = path.stat()
    return dict(path=str(path), size=s.st_size, sha256=sha(path),
                creation_utc=dt.datetime.fromtimestamp(s.st_birthtime, dt.timezone.utc).isoformat(),
                mtime_utc=dt.datetime.fromtimestamp(s.st_mtime, dt.timezone.utc).isoformat(),
                mtime_ns=s.st_mtime_ns)


def main():
    matches = re.findall(r'^(S[0-7]C?|exit)\s+- (.+)\n([^\n]+\.sfs)$', BRIEF.read_text(encoding='utf-8'), re.M)
    assert len(matches) == 17
    DEST.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_path = OUT / 'manifest.json'
    if manifest_path.exists():
        raise SystemExit('Manifest already exists: use verification, not overwrite.')
    rows = []
    for i, (label, description, name) in enumerate(matches):
        source, dest = SOURCE / name, DEST / name
        before = metadata(source)
        if not dest.exists():
            with source.open('rb') as src, dest.open('xb') as dst:
                while chunk := src.read(1024 * 1024):
                    dst.write(chunk)
        copied, after = metadata(dest), metadata(source)
        assert before['sha256'] == copied['sha256'] == after['sha256'], label
        assert before['size'] == copied['size'] == after['size'], label
        assert before['mtime_ns'] == after['mtime_ns'], label
        rows.append(dict(sample_id=f'SOR-SAMPLE-{i+6:04}', label=label,
                         description=description, filename=name,
                         classification='INCIDENTAL_TERMINAL_SAMPLE' if label == 'exit' else
                         ('CONTROL' if label.endswith('C') else 'BASELINE' if label == 'S0' else 'ACTION'),
                         source_before=before, copy=copied, source_after=after, verified=True))
    result = dict(created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                  python=sys.version, executable=sys.executable, executable_sha256=sha(Path(sys.executable)),
                  script_sha256=sha(Path(__file__)), brief_sha256=sha(BRIEF), samples=rows)
    with manifest_path.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print(f'{len(rows)} source/copy/source checks passed; {manifest_path}')


if __name__ == '__main__':
    main()
