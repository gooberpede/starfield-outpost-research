# SPDX-License-Identifier: GPL-3.0-or-later
"""Read pinned R3 inputs and export existing native analysis, offline only.

Reads installed build pins, R2 ledgers, the existing analysis database and owned
ExploreD5L.java. Writes a fresh ignored R3 child and tool logs/exports. Executes
only the installed Ghidra reader with -readOnly -noanalysis. No analysis edits,
game, deployment, save/configuration operations, downloads or Git writes.
Requires installed CPython, Java/Ghidra and existing project build helpers.
"""
import csv
import json
import re
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'runtime/retained-population'))
from build import sha, guard


def write(path, value):
    with path.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')


def git(*args):
    return subprocess.check_output(['git', '--no-optional-locks', *args], cwd=ROOT).decode().strip()


def main():
    label = sys.argv[1]
    assert re.fullmatch('[a-z0-9-]+', label)
    out = ROOT / '.local-work/d5p-r3' / label
    out.mkdir(parents=True, exist_ok=False)
    start = dict(utc=datetime.now(timezone.utc).isoformat(), free=guard(),
                 head=git('rev-parse', 'HEAD'), status=git('status', '--short'),
                 index_sha256=sha(ROOT / '.git/index'))
    build = json.loads((ROOT / '.local-work/d5p/r1-build04/build.json').read_text())
    installed = {p: sha(p) for p in build['installed']}
    assert installed == build['installed']
    sources = {p: sha(p) for p in build['sources']}
    assert sources == build['sources']
    assert sha(ROOT / '.local-work/d5p/r1-build04/SorRetainedPopulation.dll') == build['dll_sha256']
    evidence = {}
    for name in ('d5p-phase-b-sources.csv', 'd5p-r1-sources.csv', 'd5p-r2-retail-sources.csv'):
        with (ROOT / 'docs/experiments/resource-retained-population' / name).open(encoding='utf8') as stream:
            for row in csv.DictReader(stream):
                if row['path'].startswith('.local-work/'):
                    assert sha(ROOT / row['path']) == row['sha256'], row['path']
                    evidence[row['path']] = row['sha256']
    write(out / 'initial.json', dict(**start, installed=installed, sources=sources, evidence=evidence))
    old = ROOT / '.local-work/resource-retained-population'
    baseline = json.loads((old / 'db-final.json').read_text())
    before = {p: sha(p) for p in baseline}
    write(out / 'db-before.json', before)
    command = json.loads((old / 'native-owner-command04.json').read_text())
    # Reuse the owned reader; all settings/cache/log output belongs to this task.
    command = [s.replace(str(old), str(out)) for s in command]
    for name in ('ghidra-settings', 'ghidra-cache', 'java-tmp', 'java-home'):
        (out / name).mkdir()
    at = command.index('-postScript')
    command = command[:at] + ['-postScript', 'ExploreD5L.java', str(out / 'native.tsv'),
                             '14079f860', '1409828d5', '140982930', '1409829b0',
                             '140982d90', '140985870', '1422cc0d0',
                             '1402c5b80', '1402c5bd0', '140988240',
                             '1422c8d10', '1402ba340',
                             '1422cba00', '140988ab0', '1402ba260',
                             '-log', str(out / 'ghidra.log'),
                             '-scriptlog', str(out / 'script.log')]
    write(out / 'command.json', command)
    with (out / 'stdout.log').open('xb') as stdout, (out / 'stderr.log').open('xb') as stderr:
        result = subprocess.run(command, cwd=ROOT, stdout=stdout, stderr=stderr,
                                creationflags=subprocess.CREATE_NO_WINDOW)
    after = {p: sha(p) for p in baseline}
    write(out / 'db-after.json', after)
    assert before == after, 'analysis database changed'
    assert result.returncode == 0, result.returncode
    native = (out / 'native.tsv').read_text(encoding='utf8')
    assert native.startswith('SHA256\t' + next(h for p, h in installed.items() if p.endswith('Starfield.exe')))
    assert native.endswith('END\n')
    assert git('rev-parse', 'HEAD') == start['head'] and sha(ROOT / '.git/index') == start['index_sha256']
    write(out / 'result.json', dict(exit=result.returncode, free=guard(),
          native_sha256=sha(out / 'native.tsv'), database_unchanged=True,
          reader_sha256=sha(ROOT / 'research/resource-retained-population/ExploreD5L.java')))
    print(out)


if __name__ == '__main__':
    main()
