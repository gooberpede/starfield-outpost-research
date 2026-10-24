# SPDX-License-Identifier: GPL-3.0-or-later
"""Hash and retain the supplied first-party ZIP and JPEGs without interpreting.

Reads only the explicit archive argument; writes an exclusive ignored original
copy, safely named JPEG byte copies and a local manifest. Python stdlib only.
Does not alter ZIP metadata or source bytes. Visual comparison is a later step.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    out = args.output.resolve()
    assert out.is_relative_to(ROOT / '.local-work/resource-feynman-d5')
    out.mkdir(exist_ok=False)
    original = args.archive.read_bytes()
    (out / 'original.zip').write_bytes(original)
    rows = []
    with zipfile.ZipFile(args.archive) as archive:
        files = [v for v in archive.infolist() if not v.is_dir()]
        assert len(files) == 24
        assert len({Path(v.filename).name for v in files}) == 24
        for entry in files:
            name = Path(entry.filename).name
            assert re.fullmatch(r'20261025\d{6}_1\.jpg', name)
            assert entry.file_size < 30_000_000
            raw = archive.read(entry)
            assert raw[:3] == b'\xff\xd8\xff'
            (out / name).write_bytes(raw)
            rows.append(dict(member=entry.filename, filename=name,
                             bytes=len(raw), sha256=sha(raw)))
    manifest = dict(source=str(args.archive.resolve()), archive_sha256=sha(original),
                    images=sorted(rows, key=lambda r: r['filename']), interpreted=False)
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n',
                                     encoding='utf8', newline='\n')
    assert args.archive.read_bytes() == original
    print(json.dumps(dict(images=len(rows), archive_sha256=sha(original))))


if __name__ == '__main__':
    main()
