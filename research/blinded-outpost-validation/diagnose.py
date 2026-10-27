# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only D5K diagnostics; adapted from owned D5H remaining_inputs.py.

Does not repair or replace the strict historical postflight, active baseline or
namespace policy. Reads the authenticated active archive/index, original pin
rosters, remaining loose inputs and existing active-save policy. Writes one new
ignored receipt. No restoration, deletion, game, DB, Git or policy mutation.
Uses maintainer-owned archive/save helpers under SOR-P-0002; stdlib only.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from audit import ROOT, LOCAL, pin, write


def main():
    output = Path(sys.argv[1]).resolve()
    assert output.is_relative_to(LOCAL) and not output.exists()
    assert min(shutil.disk_usage(d).free for d in ('C:/', 'D:/')) >= 40000000000
    sys.path.insert(0, str(ROOT / 'research/resources-evidence-consolidation'))
    from cutover import trusted_configuration, transaction, e
    config = trusted_configuration()
    selection = e.authenticate(ROOT / 'docs/experiments/resources-evidence-consolidation/active-baseline.json', config['selection_sha256'])
    assert selection == config['selection']
    tx = transaction(config)
    assert pin(tx.folder / 'baseline.json') == selection['baseline_sha256']
    assert pin(tx.folder / 'journal.jsonl') == selection['journal_sha256']
    norm = lambda p: os.path.normcase(os.path.normpath(str(p)))
    with tx.store.authenticated() as (entry, archive, members):
        archived = {norm(ROOT / r['path']):r['sha256'] for r in entry['rows']}
    roster = ROOT / '.local-work/resources-evidence-consolidation/historical-pins.json'
    assert pin(roster) == 'a243c67c0e451aac21cbb5fcb671c9e94ad2b3806406d0fdec1b2626f153ab9b'
    old = json.loads(roster.read_text())['pins']
    removed = {norm(ROOT / f'.local-work/continuous-beacon-preview/builds/qualification-{i:02}/SorNativePositionOracle-0.7.0.zip') for i in range(3,7)}
    missing, bad, loose, substitutions = [], [], 0, 0
    for name, expected in old.items():
        key = norm(name)
        if key in archived:
            actual = archived[key];substitutions += 1
        elif Path(name).is_file():
            actual = pin(name);loose += 1
        else:
            missing.append(name);actual = None
        if actual != expected and key not in removed:
            bad.append(dict(path=name,expected=expected,actual=actual))
    assert not bad and all(norm(p) in removed for p in missing)
    sys.path.insert(0,str(ROOT/'research/resource-carinae-source-context'))
    from save_policy import load_policy, classify, compare, snapshot, partition
    policy=load_policy(); live=Path('C:/Users/User/Documents/My Games/Starfield/Saves')
    manifest=ROOT/'.local-work/resource-carinae-source-context/protected-before.json'
    rows=json.loads(manifest.read_text());expected_live={}; failures=[]; transients=[]
    for row in rows:
        p=Path(row['path']); key=norm(p)
        if p.parent==live:
            kind=classify(p.name,policy)
            if row['sha256'] is not None:expected_live[p.name]=dict(bytes=0,sha256=row['sha256'])
            if kind['protection']=='TRANSIENT':transients.append(str(p));continue
            assert kind['protection']!='UNCLASSIFIED'
        actual=archived[key] if key in archived else pin(p) if p.is_file() else None
        if actual!=row['sha256']:failures.append(dict(path=str(p),expected=row['sha256'],actual=actual))
    current=snapshot(live,policy)
    for name in expected_live:expected_live[name]['bytes']=current.get(name,{}).get('bytes',0)
    delta=compare(expected_live,current,policy)
    assert not failures and delta['ok']
    before=json.loads((LOCAL/'start.json').read_text())
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==before['head']
    assert pin(ROOT/'.git/index')==before['index_sha256']
    assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT)
    write(output,dict(strict_historical_postflight='FAIL; not replaced by these diagnostics',
        acknowledged_external_removals=sorted(removed),missing_historical_rows=missing,
        historical_rows=len(old),archived_matches=substitutions,remaining_loose_hashes=loose,
        unacknowledged_historical_differences=bad,protected_policy_rows=len(rows),
        protected_policy_differences=failures,live_comparison=delta,
        live_classification=partition(current,policy),excluded_live_transients=transients,
        selection_sha256=config['selection_sha256'],archive_sha256=tx.store.archive_sha,
        index_sha256=tx.store.index_sha,baseline_sha256=selection['baseline_sha256'],
        journal_sha256=selection['journal_sha256'],head=before['head'],index_sha256_git=before['index_sha256'],
        free={d:shutil.disk_usage(d).free for d in ('C:/','D:/')}))
    print('Remaining-input diagnostics complete; strict historical postflight remains FAIL',len(old),substitutions,loose,len(missing),len(rows))


if __name__ == '__main__':
    main()
