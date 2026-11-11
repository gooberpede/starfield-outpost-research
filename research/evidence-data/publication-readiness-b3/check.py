"""Original B3 metadata check, CPython stdlib only. From repository root:
python -B research/evidence-data/publication-readiness-b3/check.py
Reads manifests, selected source, new Markdown and baseline metadata; prints
JSON to stdout, writes no files, imports no archival entrypoints. No real-data,
target, native/tool, network, Git index/ref or installed-directory operations.
Does not establish source authorship, semantic truth or publication clearance.
"""
import ast
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DOCS = Path(__file__).resolve().parent


def rows(name):
    return list(csv.DictReader((DOCS / name).open(encoding='utf8')))


def check_destinations(candidates):
    for row in candidates:
        name = row['tracked_destination']
        if not name:
            continue
        path = (ROOT / name).resolve()
        assert path.is_relative_to(ROOT) and path.is_file(), (row['id'], name)


def main():
    candidates = rows('source-selection.csv')
    check_destinations(candidates)
    # Regression for review01's false installed-script routes. No fixture files.
    try:
        check_destinations([dict(id='synthetic-missing-route',
                                 tracked_destination='xedit/B3-NONEXISTENT-FIXTURE.pas')])
    except AssertionError:
        missing_destination_rejected = True
    else:
        raise AssertionError('missing source destination accepted')
    external = [r for r in candidates if r['id'] in {'B3-C0332', 'B3-C0399'}]
    assert len(external) == 2 and all(r['decision'] == 'DEFERRED EXTERNAL' and
                                    not r['tracked_destination'] and
                                    r['ownership'].startswith('UNKNOWN') for r in external)
    sources = rows('promoted-sources.csv')
    unique = {r['tracked_path']: r['tracked_sha256'] for r in sources}
    for r in sources:
        assert r['origin_sha256'] == r['tracked_sha256'], r['origin']
    for name, expected in unique.items():
        data = (ROOT / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == expected, name
        assert b'\x00' not in data and not data.startswith(b'\xef\xbb\xbf'), name
        data.decode('utf8')
        if name.endswith('.py'):
            ast.parse(data.decode('utf8'), filename=name)
    reconciled = rows('historical-source-reconciliation.csv')
    assert len(reconciled) == 26
    assert len({r['literal_path'] for r in reconciled}) == 23
    assert all(r['state'] == 'EXACT RECOVERED' and
               r['expected_sha256'] == r['verified_historical_sha256'] and
               r['current_sha256'] != r['expected_sha256'] for r in reconciled)
    links = 0
    authored = [ROOT / name for name in ('docs/reference/b3-baseline.md', 'docs/reference/b3-methods.md',
                                     'research/historical-methods/b3/README.md')]
    for path in authored:
        data = path.read_bytes()
        assert not data.startswith(b'\xef\xbb\xbf') and b'\r' not in data, str(path)
        text = data.decode('utf8')
        assert text.count('```') % 2 == 0, str(path)
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if re.match(r'^[a-z]+:', target) or target.startswith('#'):
                continue
            destination = (path.parent / target.split('#')[0]).resolve()
            assert destination.is_relative_to(ROOT) and destination.exists(), (path, target)
            links += 1
    inputs = rows('baseline-inputs.csv')
    exes = [r for r in inputs if r['path'].endswith('Starfield.exe')]
    assert len(exes) == 1 and exes[0]['sha256'] == '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
    test = json.loads((DOCS / 'synthetic-qualification.json').read_text(encoding='utf8'))
    assert test['returncode'] == 0 and test['source_tree_unchanged']
    assert 'Ran 6 tests' in test['stderr'] and test['stderr'].rstrip().endswith('OK')
    for row in test['sources']:
        assert hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest() == row['sha256']
    print(json.dumps(dict(result='PASS', source_origins=len(sources),
                          distinct_source_routes=len(unique),
                          historical_occurrences=len(reconciled),
                          input_identities=len(inputs), relative_links=links,
                          selected_candidates=len(candidates),
                          source_destination_checks='PASS',
                          missing_destination_rejected=missing_destination_rejected), indent=2))


if __name__ == '__main__':
    main()
