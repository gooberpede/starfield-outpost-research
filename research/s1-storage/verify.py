# SPDX-License-Identifier: GPL-3.0-or-later
"""S1 integrity and bounded real-data regressions. Reads final receipts, protected
inputs, native exports, authored text and Git identities. Writes fresh ignored
JSON; --tables also writes authored metadata/catalogue CSVs. Stdlib and existing
owned guard/tests only. No target/database/save/Git mutation or downloads.
Run CPython -B from repository root after stopping read-only native session.
"""
import argparse
import ast
import collections
import csv
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import zipfile
import hashlib
from catalog import ROOT, pin
sys.path.insert(0, str(ROOT / 'save-analysis/scripts'))
from inventory_historical_saves import guard

BASE = ROOT / '.local-work/s1-storage'
DOCS = ROOT / 'docs/experiments/storage'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    ap.add_argument('--tables', action='store_true')
    a = ap.parse_args()
    assert a.run.isalnum()
    guard()
    out = BASE / (a.run + '.json')
    assert not out.exists()
    seed = json.loads((BASE / 'baseline.json').read_text())
    checks, pins = [], {}
    def check(ok, label):
        assert ok, label
        checks.append(label)
    def verify(p):
        now = pin(p['path'])
        check(now['sha256'] == p['sha256'], 'protected identity ' + p['path'])
        pins[now['path']] = now
    def capture(p):
        q = pin(p)
        pins[q['path']] = q
        return q
    check(subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT).decode().strip() == seed['head'], 'HEAD unchanged')
    for p in [seed['index'], *seed['files'], *seed['protected'], *seed['database']]:
        verify(p)
    check({p['path'] for p in seed['database']} == {str(p) for p in Path('D:/ReverseEngineering/Starfield/GhidraProject').rglob('*') if p.is_file()}, 'analysis database file inventory unchanged')
    census = json.loads((BASE / 'census02.json').read_text())
    verify(census['source'])
    verify(census['cache'])
    verify(census['tool'])
    rows = census['rows']
    primary = [r for r in rows if not r['boundary_chest']]
    chests = [r for r in rows if r['boundary_chest']]
    check(len(primary) == 225 and len(chests) == 16, '225 primary + 16 independent chest-list boundary definitions')
    check(all(r['no_in'] == r['no_out'] == 1 for r in chests), 'all boundary defaults block both link directions')
    stores = [r for r in rows if r['editorid'].startswith('OutpostStorage') and 'Cargo' not in r['editorid']]
    check(len(stores) == 12 and collections.Counter(r['carryweight'] for r in stores) == {75.: 4, 150.: 4, 300.: 4}, 'all four dedicated families and three capacities')
    check(all(any(c['product'] == r['formid'] for c in census['construction']) for r in stores), 'each dedicated base has actual construction COBJ')
    for r in stores:
        check(len(r['filter_entries']) == 1 and r['filter_entries'][0]['type'] == 'KYWD', 'dedicated keyword filter ' + r['formid'])
    check(len([r for r in primary if 'Harvester' in r['editorid']]) == 154, '154 extractor definitions retained')
    check(len([r for r in primary if 'Organic' in r['editorid']]) == 6, 'six organic variants')
    samples = []
    for n in ['saved03.json', 'saved04.json', 'saved05.json', 'saved06.json']:
        j = json.loads((BASE / n).read_text())
        verify(j['source'])
        verify(j['tool'])
        verify(j['census'])
        check(j['source_unchanged'], 'original pre/post saved read ' + n)
        samples.append(j)
        for r in j['rows']:
            inv = r.get('inventory', {})
            if inv.get('status') != 'DECODED_EMPTY_STACK_EXTRA_SUBSET':
                continue
            check(r['offset'] < inv['start'] <= inv['end'] <= r['end'], 'inventory bounds ' + n + ' ' + r['identity'])
            check(inv['next_reference_index'] == inv['reference_count'], 'item queue closure ' + n + ' ' + r['identity'])
        capture(BASE / n)
    check(len({j['source']['sha256'] for j in samples}) == 4, 'four distinct original byte identities; equal counts not deduplicated')
    h36 = next(j for j in samples if j['sample'] == 'HIST-0036')
    by = {r['identity']: r for r in h36['rows']}
    check([sum(s['count'] for s in i['stacks']) for i in by['DYNAMIC:ff02c339']['inventory']['rows']] == [41, 3], 'real warehouse two-item counterexample')
    check(by['DYNAMIC:ff01c792']['inventory']['item_count'] == 0, 'explicit empty serialized solid list')
    check(by['DYNAMIC:ff018b69']['inventory']['status'] == 'NO_INVENTORY_CHANGE_BRANCH', 'fuel marker absence label remains narrow')
    check(any(e['type'] == '4c' and any(x['keyword'] == 'starfield.esm:054ba6' and x['target'] == 'DYNAMIC:ff04ba51' for x in e['entries']) for e in by['DYNAMIC:ff018b64']['extra']['extras']), 'actual storage Workshop owner edge')
    check(any(r.get('inventory', {}).get('status') == 'UNSUPPORTED_STACK_EXTRAS' for r in h36['rows']), 'unsupported real stacks retained')
    assemblies = json.loads((BASE / 'assemblies01.json').read_text())
    verify(assemblies['source'])
    verify(assemblies['tool'])
    def base_of(r):
        return next((int.from_bytes(bytes.fromhex(v), 'little') for k, v in r['fields'] if k == 'NAME'), None)
    for family in ['OutpostPI_CargoLink01LandingPad', 'OutpostPI_CargoLink02LandingPad_Fueled']:
        check({0x219171, 0x219173}.issubset({base_of(r) for r in assemblies['children'] if r['packin'] == family}), 'actual basic cargo child pair ' + family)
    for folder in ['native', 'native-menu', 'native-final']:
        check((BASE / folder / 'stop').exists(), 'native session stop requested ' + folder)
    for request in sorted(BASE.glob('native*/*.request')):
        check(request.with_name(request.name + '.done').exists(), 'native completion ' + request.name)
        p = request.with_name(request.name + '.tsv')
        t = p.read_text()
        check('SHA256\t' + seed['protected'][0]['sha256'] in t, 'export executable pin ' + request.name)
        # Some early exploratory address guesses intentionally return no function.
        check('DECOMPILED\tfalse' not in t, 'selected decompiler success ' + request.name)
        capture(p)
    for p in [BASE / 'native-menu/fields.tsv', BASE / 'native-final/menu-fields.tsv', BASE / 'native-final/model-fields.tsv']:
        check('cancelled=false' in p.read_text(), 'bounded field locator complete ' + p.name)
        capture(p)
    capture(ROOT / 'ghidra/scripts/ScopedFieldUses.java')
    regressions = []
    for name in ['test_workshop_inventory.py', 'test_outpost_record_framing.py', 'test_stream_save.py', 'test_extractor_resources.py']:
        r = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'save-analysis/scripts', '-p', name], cwd=ROOT, capture_output=True, text=True)
        regressions.append(dict(command=name, returncode=r.returncode, stdout=r.stdout, stderr=r.stderr))
        check(r.returncode == 0, 'regression ' + name)
        capture(ROOT / 'save-analysis/scripts' / name)
    for p in (ROOT / 'research/s1-storage').glob('*.py'):
        ast.parse(p.read_text(encoding='utf8'))
        capture(p)
    for p in [BASE / 'census02.json', BASE / 'assemblies01.json', BASE / 'native/E2ReadSession.java', ROOT / 'ghidra/scripts/OutpostRecon.java',
              ROOT / '.local-work/recon/e1-arithmetic-10.tsv', ROOT / '.local-work/recon/scripts/OutpostContainerScript.psc',
              ROOT / 'research/p1-power/saved_instances.py', ROOT / 'research/e3-fabricators/catalog.py',
              ROOT / 'save-analysis/scripts/workshop_inventory.py', ROOT / 'save-analysis/scripts/stream_save.py',
              ROOT / 'save-analysis/scripts/outpost_record_framing.py', ROOT / 'save-analysis/scripts/inspect_outpost_definitions.py']:
        capture(p)
    for name in ['extractor_resources.py', 'outpost_membership.py', 'validate_mature_outposts.py', 'inventory_historical_saves.py']:
        capture(ROOT / 'save-analysis/scripts' / name)
    for p in [Path(sys.executable), Path('C:/Users/User/AppData/Local/Programs/Eclipse Adoptium/jdk-21.0.12.8-hotspot/bin/java.exe'),
              Path('D:/tools/ghidra_12.1.2_PUBLIC/Ghidra/application.properties')]:
        capture(p)
    archive = Path('C:/Program Files (x86)/Steam/steamapps/common/Starfield/Tools/ContentResources.zip')
    capture(archive)
    with zipfile.ZipFile(archive) as z:
        names = [n for n in z.namelist() if n.replace('\\', '/').lower().endswith('/outpostcontainerscript.psc')]
        check(len(names) == 1, 'unique installed development script archive entry')
        check(hashlib.sha256(z.read(names[0])).hexdigest() == pin(ROOT / '.local-work/recon/scripts/OutpostContainerScript.psc')['sha256'], 'installed archive script matches consulted local source')
    if a.tables:
        def write_csv(path, headings, data):
            s = io.StringIO(newline='')
            w = csv.writer(s, lineterminator='\n')
            w.writerow(headings)
            w.writerows(data)
            path.write_text(s.getvalue(), encoding='utf8', newline='\n')
        write_csv(DOCS / 'catalogue.csv', ['formid', 'editorid', 'esm_physical_offset', 'capacity_fallback', 'incoming_prohibition', 'outgoing_prohibition', 'filter', 'admitted_keywords', 'scope'],
                  [[r['formid'], r['editorid'], r['offset'], '' if r['boundary_chest'] else r['carryweight'], r['no_in'], r['no_out'], '|'.join(r['filters']), '|'.join(i['editorid'] for i in r['filter_entries']), 'CHEST_LINK_COMPARISON_ONLY' if r['boundary_chest'] else 'PRIMARY_DEFINITION_INCLUDING_EXCEPTIONS'] for r in rows])
        private_labels = {j['source']['path']: 'protected-original:' + j['sample'] for j in samples}
        write_csv(DOCS / 'sources.csv', ['locator', 'bytes', 'sha256', 'eligibility'],
                  [[private_labels.get(p['path'], p['path']), p['bytes'], p['sha256'], 'Raw LOCAL-ONLY; metadata REVIEW-REQUIRED'] for p in pins.values()])
        functions = [
            ('140f84470', 'ordered endpoint pair validator', '001'),
            ('140f7c210', 'current full by capacity versus weight', '001'),
            ('140b70a80', 'ordinary positive capacity insertion fit count', '001'),
            ('140f83f60', 'source capability and outgoing prohibition', '002'),
            ('142068a10', 'ObjectReference AddTransferLink callback', '002'),
            ('140f65870', 'UI link creation command', '002'),
            ('140b24ca0', 'reference base TESContainer component query', '003'),
            ('140b756c0', 'base component lookup wrapper', '003'),
            ('140b69760', 'inventory weight query', '003'),
            ('1421c3bf0', 'UI valid target highlighting', '004'),
            ('1421e7e20', 'UI closest eligible target selection', '004'),
            ('1405da040', 'TESContainer component name identity', '005'),
            ('141589840', 'Workshop action mask source gate', '006'),
            ('1406448b0', 'reference inventory list restoration', '006'),
            ('140641320', 'item identity and stack load', '007'),
            ('140642a00', 'stack extra list and signed quantity load', '008'),
            ('1406447c0', 'inventory item count and row serialization', '009'),
            ('140641180', 'item identity stacks quantity bookkeeping save', '010'),
            ('140156fc0', 'outgoing prohibition default binding', '012'),
            ('140156f80', 'incoming prohibition default binding', '012'),
            ('140126ca0', 'Transfer Container keyword binding', '015'),
            ('140156f40', 'OutpostBuildContainer default binding', '015'),
            ('14173ae90', 'UI filter keyword category classification', '016'),
            ('1416d7a00', 'Workshop relationship Transfer Container selection', '019'),
            ('141ee8d20', 'spatial Transfer Container candidate selection', '019'),
            ('1416d47e0', 'Workshop reverse-link Transfer Container query', '021'),
            ('1416bd210', 'two-reference inventory menu handoff', '024'),
            ('14146d800', 'OpenContainerMenuEventData source identity', '025'),
            ('140a84810', 'CONT ONAM filter loader', '026'),
            ('140a84690', 'CONT filter form fixup', '026'),
            ('141eaf900', 'manual ContainerMenu TransferItem sink', '031'),
            ('141eaf9e0', 'manual item identity and inventory command', '033'),
            ('140b29700', 'reference inventory change serialization gate', '034'),
            ('141eafe00', 'manual per-item transfer admission and dispatch', '036'),
            ('141eaf090', 'manual item and bound callable acceptance', '037'),
            ('141eab810', 'ContainerMenu separate inventory model construction', '039'),
        ]
        for va, alias, n in functions:
            check('FUNCTION\t' + va + '\t' in (BASE / 'native' / (n + '.request.tsv')).read_text(), 'registered function actual entry ' + va)
        write_csv(DOCS / 'functions.csv', ['key', 'static_va', 'rva', 'original_name', 'alias', 'source', 'window', 'basis', 'interface', 'limits'],
                  [[f'S1-{i:03}', '0x' + va, hex(int(va, 16) - 0x140000000), 'FUN_' + va, alias,
                    f'.local-work/s1-storage/native/{n}.request.tsv', 'Named function; native.md narrows claimed paths; instruction caps preserved',
                    'STATIC; proposed STRONG scoped interpretation', 'OBSERVED-INTERNAL', 'No invocation; live values and general safe ABI unqualified']
                   for i, (va, alias, n) in enumerate(functions, 1)])
    for p in DOCS.glob('*'):
        if not p.is_file():
            continue
        b = p.read_bytes()
        t = b.decode('utf8')
        check(not b.startswith(b'\xef\xbb\xbf') and b'\r' not in b, 'UTF8 LF ' + p.name)
        check(all(line.rstrip() == line for line in t.splitlines()), 'whitespace ' + p.name)
        if p.suffix == '.md':
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', t):
                f = target.split('#')[0].strip('<>')
                if f and not re.match('[a-zA-Z]+:', f):
                    check((p.parent / f).exists(), 'link ' + p.name + ' ' + f)
    r = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True)
    check(r.returncode == 0, 'git diff --check')
    verify(seed['index'])
    with out.open('x', encoding='utf8', newline='\n') as f:
        json.dump(dict(checks=checks, pins=list(pins.values()), regressions=regressions,
                       head=seed['head'], scientific_limits='Checks verify framing, coverage and bytes; native semantics still need independent instruction review'), f, indent=2)
        f.write('\n')
    print('PASS', len(checks), 'checks;', len(pins), 'pins;', out)


if __name__ == '__main__':
    main()
