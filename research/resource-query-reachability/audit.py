# SPDX-License-Identifier: GPL-3.0-or-later
"""D5H postflight via the active archive-level preservation boundary.

Reads the existing protection policy, immutable expectations, target inputs and
initial HEAD/index receipt. Writes an exclusive ignored receipt. No restoration,
save, target, configuration, analysis-content or Git mutation. Stdlib/owned code.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/resource-query-reachability'


def pin(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write(path, value):
    with Path(path).open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def main():
    output = Path(sys.argv[1]).resolve()
    assert output.is_relative_to(ROOT / '.local-work') and not output.exists()
    before = json.loads((LOCAL / 'start.json').read_text())
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40000000000
    sys.path.insert(0, str(ROOT / 'research/resources-evidence-consolidation'))
    from resources_preservation import verify_historical
    protection = verify_historical()
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    assert head == before['head'] and pin(ROOT / '.git/index') == before['index_sha256']
    assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'])
    installed = {}
    base = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield')
    for relative, expected in [('Starfield.exe', '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'),
        ('Data/Starfield.esm', '1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7'),
        ('Data/Starfield - PlanetData.ba2', '2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5')]:
        actual = pin(base / relative)
        assert actual == expected
        installed[relative] = actual
    write(output, dict(head=head, index_sha256=before['index_sha256'], protection=protection,
        installed=installed, staged_changes=False, free={d:shutil.disk_usage(d).free for d in ('C:/', 'D:/')}))
    print('Postflight PASS; active archive boundary; HEAD/index and installed identities unchanged')


if __name__ == '__main__':
    main()
