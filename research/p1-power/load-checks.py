# SPDX-License-Identifier: GPL-3.0-or-later
"""Original stdlib-only offline load evidence audit.

Reads saved research receipts, stopped Ghidra exports, protected-input pins,
Git HEAD/index and changed text. Writes an exclusive ignored JSON receipt and
optional metadata-only source CSV. No target/tool launch, save decode/mutation,
network, database changes or Git writes. Nominal ratings are not current power.
"""
import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '.local-work/p1-load'


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, stderr=subprocess.PIPE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--pins', action='store_true')
    args = ap.parse_args()
    assert re.fullmatch('[a-zA-Z0-9]+', args.run)
    out = BASE / (args.run + '.json')
    assert not out.exists()
    checks, pins, notes = [], {}, []

    def check(ok, label):
        assert ok, label
        checks.append(label)

    def pin(path):
        p = Path(path)
        row = dict(path=str(p.resolve()), bytes=p.stat().st_size, sha256=sha(p))
        pins[row['path']] = row
        return row

    seed = read(BASE / 'baseline.json')
    check(git('rev-parse', 'HEAD').decode().strip() == seed['head'], 'HEAD unchanged')
    check(pin(ROOT / '.git/index')['sha256'] == seed['index']['sha256'], 'index unchanged')
    for row in read(BASE / 'protected-before.json'):
        check(pin(row['path'])['sha256'] == row['sha256'], 'protected unchanged ' + row['path'])
    db = read(BASE / 'db-before.json')
    for path, expected in db.items():
        check(pin(path)['sha256'] == expected, 'database unchanged ' + path)
    for row in seed['files']:
        p = BASE / 'baseline-tree' / Path(row['path']).relative_to(ROOT)
        check(pin(p)['sha256'] == row['sha256'], 'baseline copy ' + str(p))
    exe = '7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28'
    for folder, nums in [('native', range(1, 15)), ('native-r2', range(15, 23))]:
        check((BASE / folder / 'stop').exists(), 'stopped ' + folder)
        for n in nums:
            p = BASE / folder / f'{n:03}.request.tsv'
            check(p.with_suffix('.done').exists(), 'done ' + str(p))
            text = p.read_text(encoding='utf8')
            check('SHA256\t' + exe in text and 'BASE\t140000000' in text,
                  'native build/base ' + str(p))
            check('DECOMPILED\tfalse' not in text, 'no failed decompile ' + str(p))
            pin(p)
        for name in ['session.log', 'E2ReadSession.java', 'PowerLoadRtti.java']:
            pin(BASE / folder / name)
    notes.append('native/015 request was not executed before stop; copied and completed in native-r2. '
                 'Known large post-load decompiler switch and capped instruction output are not absence proofs.')
    rtti = BASE / 'native-r2/rtti01.tsv'
    rt = rtti.read_text(encoding='utf8')
    check('OFFSET\t72\t.?AVTESObjectREFRGameEventListener@Workshop@@' in rt,
          'RTTI Workshop subobject offset')
    check('MDISP\t72\t.?AV?$BSTEventSink@UTESObjectLoadedEvent@@@' in rt,
          'RTTI object-loaded sink binding')
    check('MDISP\t0\t.?AV?$BSTEventSink@UTESOpenCloseEvent@@@' in rt,
          'RTTI power sink open-close binding')
    pin(rtti)
    additions = read(BASE / 'register-additions.json')
    rows = list(csv.reader((ROOT / 'docs/experiments/native-availability-map/functions.csv')
                           .read_text(encoding='utf8').splitlines()))
    check(len({r[0] for r in rows[1:]}) == len(rows)-1, 'unique native keys')
    for row in additions:
        check(row in rows, 'registered ' + row[0])
        check(int(row[2], 16)-0x140000000 == int(row[3], 16), 'VA/RVA ' + row[0])
        check('FUNCTION\t' + row[2][2:] + '\t' in (ROOT / row[6]).read_text(encoding='utf8'),
              'function/source locator ' + row[0])
    native_text = '\n'.join(p.read_text(encoding='utf8') for p in
                            [BASE/'native/002.request.tsv', BASE/'native/003.request.tsv',
                             BASE/'native-r2/015.request.tsv', BASE/'native-r2/017.request.tsv'])
    for token in ['0x7ffffffd', 'FinishLoadGlobalData', 'FUN_1405810b0', 'FUN_14066f880']:
        check(token in native_text, 'positive native operand ' + token)
    graph_path = ROOT / '.local-work/p1-power/saved/graph03.json'
    graph = read(graph_path)
    pin(graph_path)
    for row in graph['inputs']:
        check(pin(row['path'])['sha256'] == row['sha256'], 'graph input unchanged ' + row['path'])
    screen = []
    for sample in graph['rows']:
        for component in sample['components']:
            loc = sample['record_locators']
            nodes = component['nodes']
            supply = sum(loc[n]['props'].get('00032e', 0) for n in nodes)
            demand = sum(loc[n]['props'].get('000330', 0) for n in nodes)
            missing = sorted(set(nodes) & set(sample['no_cb_target_nodes']))
            screen.append(dict(sample=sample['sample'], nodes=nodes,
                               nominal_supply=supply, nominal_demand=demand,
                               boundary=len(component['boundary_edges']),
                               missing_decoded_cb=missing, nominal_deficit=supply < demand))
    expected = {'HIST-0036': 17, 'HIST-0077': 15, 'mature-Save52': 17, 'HIST-0266': 14}
    for name, count in expected.items():
        selected = [r for r in screen if r['sample'] == name]
        check(len(selected) == count, 'mature component count ' + name)
        check(all(not r['boundary'] and not r['missing_decoded_cb'] and not r['nominal_deficit']
                  for r in selected), 'closed nominal non-deficit coverage ' + name)
    gaps = [r for r in screen if r['nominal_deficit'] and not r['boundary']]
    check({n for r in gaps for n in r['nodes']} ==
          {'DYNAMIC:ff0253b2', 'DYNAMIC:ff0253b3'}, 'two apparent closed deficits identified')
    check(all(r['missing_decoded_cb'] == r['nodes'] for r in gaps),
          'apparent isolated deficits have missing decoded CB')
    # A mathematical control, not a power simulation or repeated-load experiment.
    contributions = [{'a', 'b'}, {'b', 'c'}, {'d'}]
    import itertools
    check(all(set().union(*p) == {'a', 'b', 'c', 'd'} for p in itertools.permutations(contributions)),
          'fixed per-root contribution union permutation control')
    # Retained original inputs and prior verification receipts remain bound.
    for name in ['.local-work/p1-order/saved/inspection02.json',
                 '.local-work/p1-order/verification05.json',
                 '.local-work/p1-power/verification07.json',
                 '.local-work/p1-power/verification08.json',
                 '.local-work/p1-order/verification06.json',
                 '.local-work/p1-load/session-completion.json',
                 '.local-work/p1-order/package-final01.json',
                 '.local-work/p1-order/independent-review-final01.md']:
        pin(ROOT / name)
    for p in [Path(__file__), BASE/'register-additions.json', BASE/'export.py',
              ROOT/'ghidra/scripts/OutpostRecon.java', BASE/'baseline.json',
              BASE/'db-before.json', BASE/'protected-before.json']:
        pin(p)
    if args.pins:
        stream = io.StringIO(newline='')
        writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(['path', 'bytes', 'sha256', 'eligibility'])
        for row in sorted(pins.values(), key=lambda r: r['path']):
            try:
                label = Path(row['path']).relative_to(ROOT).as_posix()
            except ValueError:
                label = row['path']
            writer.writerow([label, row['bytes'], row['sha256'], 'LOCAL-ONLY evidence; metadata REVIEW-REQUIRED'])
        (ROOT/'docs/experiments/power/load-sources.csv').write_text(
            stream.getvalue(), encoding='utf8', newline='\n')
    names = sorted(set(git('diff', 'HEAD', '--name-only', '-z').decode().split('\0')[:-1]
                       + git('ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')[:-1]))
    docs = []
    for name in names:
        p = ROOT / name
        if p.suffix not in ('.md', '.csv'):
            continue
        data = p.read_bytes(); text = data.decode('utf8'); docs.append(name)
        check(not data.startswith(b'\xef\xbb\xbf') and '\ufffd' not in text, 'UTF8 ' + name)
        if 'docs/implementation-briefs/' not in name:
            check(b'\r' not in data, 'LF ' + name)
            check(all(line.rstrip() == line for line in text.splitlines()), 'whitespace ' + name)
        try:
            prior = git('show', 'HEAD:' + name).decode('utf8')
        except subprocess.CalledProcessError:
            prior = ''
        corrupt = [line for line in text.splitlines() if re.search('[\u00c3\u00c2]|\u00e2[\u0080-\u2122]', line)]
        check(all(line in prior.splitlines() for line in corrupt), 'no new mojibake ' + name)
        if corrupt:
            notes.append(dict(file=name, preexisting_corrupt_lines=len(corrupt), unchanged_HEAD_lines=True))
        if p.suffix == '.md':
            check(text.count('```') % 2 == 0, 'Markdown fences ' + name)
            new = '\n'.join(line for line in text.splitlines() if line not in prior.splitlines())
            check(not re.search(r'\b(?:retail|version|stride|word|operation|mask|offset)(?=[0-9])|ExtraFlags(?=[0-9])', new, re.I),
                  'notation/fused prose ' + name)
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                file = target.split('#')[0].strip('<>')
                if file and not re.match(r'[A-Za-z]+:', file):
                    check((p.parent / file).resolve().exists(), 'link ' + name + ' ' + target)
    subprocess.run(['git', 'diff', '--check'], cwd=ROOT, check=True, capture_output=True)
    check(sha(ROOT/'.git/index') == seed['index']['sha256'], 'final index unchanged')
    out.write_text(json.dumps(dict(checks=checks, pins=list(pins.values()),
        database_files=len(db), documentation_audited=docs, nominal_screen=screen,
        native_new_rows=len(additions), notes=notes,
        limits=['Pins/locators are integrity checks, not semantic proof',
                'Nominal screen retains missing adjacency and is not actual available supply',
                'No live reload observation; synthetic union control has algebraic scope only',
                'Manual full changed-prose review supplements automated patterns']), indent=2)+'\n',
        encoding='utf8', newline='\n')
    print('PASS', len(checks), 'checks;', len(docs), 'documents;', len(pins), 'pins;', len(db), 'database files')


if __name__ == '__main__':
    main()
