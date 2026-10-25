# SPDX-License-Identifier: GPL-3.0-or-later
"""Read pinned local results; write compact new summary and source ledgers.

Uses stdlib, existing Git and owned methods. No target or source-evidence writes.
Local summary receipt names are exclusive. Task-authored aggregate CSVs are
refreshed from the selected frozen run04; private paths stay in ignored receipts.
"""
import csv
import hashlib
import json
from pathlib import Path
import statistics
import subprocess

ROOT = Path(__file__).resolve().parents[2]
LOCAL = ROOT / '.local-work/preservation-verification'
DOC = ROOT / 'docs/experiments/preservation-verification-optimization'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write(path,value):
    with path.open('x',encoding='utf8',newline='\n') as f:
        json.dump(value,f,indent=2)
        f.write('\n')


def main():
    rel = 'docs/experiments/resource-predictability-contrast/sources.csv'
    data = (ROOT / rel).read_bytes()
    assert digest(data) == digest(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT))
    # Hash the exact bytes consumed, then parse the in-memory identity-bound input.
    write(LOCAL / 'supplement-input04.json',dict(path=rel,sha256=digest(data),basis='Exact HEAD bytes; intake prior to parsing'))
    cited = list(csv.DictReader(data.decode('utf8').splitlines()))
    pins = json.loads((LOCAL / 'input-pins.json').read_text())
    ledger = []
    for path,sha in sorted(pins.items()):
        p = Path(path)
        ledger.append(dict(source=p.relative_to(ROOT).as_posix(),sha256=sha,
            role='Owned primary policy/method/receipt; no payload copied',rights='SOR-P-0002; project-authored material'))
    ledger.append(dict(source=rel,sha256=digest(data),role='D5G cited-input coverage cross-check',rights='SOR-P-0002'))
    files = list((LOCAL / 'run04').glob('*.json')) + [LOCAL / 'reconstruction.json']
    for path in files:
        raw = path.read_bytes()
        ledger.append(dict(source=path.relative_to(ROOT).as_posix(),sha256=digest(raw),
                           role='Fresh synthetic qualification or reconstruction receipt',rights='Original task output; LOCAL-ONLY receipt'))
    for name in ('journal.py','prototype.py','qualify.py','reconstruct.py','summarize.py','additional.py'):
        path = ROOT / 'research/preservation-verification' / name
        ledger.append(dict(source=path.relative_to(ROOT).as_posix(),sha256=digest(path.read_bytes()),
                           role='Original task method',rights='GPL-3.0-or-later'))
    with (DOC / 'sources.csv').open('w',encoding='utf8',newline='') as f:
        writer = csv.DictWriter(f,fieldnames=['source','sha256','role','rights'],lineterminator='\n')
        writer.writeheader()
        writer.writerows(ledger)
    for name in ('measurements.csv','tests.csv'):
        (DOC / name).write_bytes((LOCAL / 'run04' / name).read_bytes())
    m=json.loads((LOCAL / 'run04/measurements.json').read_text())
    output = {}
    for mode in ('legacy','full','journal-conditional'):
        rows=[r for r in m if r['workload']=='W1' and r['mode']==mode]
        output[mode] = dict(counts=rows[0]['counts'],
            historical_wall_median=statistics.median(r['historical_wall_seconds'] for r in rows),
            wall_median=statistics.median(r['wall_seconds'] for r in rows),
            wall_min=min(r['wall_seconds'] for r in rows),wall_max=max(r['wall_seconds'] for r in rows),
            cpu_median=statistics.median(r['cpu_seconds'] for r in rows),
            control_bytes_hashed=rows[0]['control_bytes_hashed'],
            journal_bytes_min=min(r['journal_bytes'] for r in rows),journal_bytes_max=max(r['journal_bytes'] for r in rows))
    baseline=output['legacy']
    for mode in ('full','journal-conditional'):
        result=output[mode]
        result['historical_reduction_percent']={k:100*(1-result['counts']['historical'][k]/v)
            for k,v in baseline['counts']['historical'].items() if v}
        result['historical_reduction_percent']['wall_seconds']=100*(1-result['historical_wall_median']/baseline['historical_wall_median'])
        result['total_wall_reduction_percent']=100*(1-result['wall_median']/baseline['wall_median'])
    output['W2']={arm:statistics.median(r['wall_seconds'] for r in m if r['workload']=='W2' and r['arm']==arm)
                  for arm in ('baseline','replacement')}
    setup=json.loads((LOCAL / 'run04/setup.json').read_text())
    output['setup']=setup
    output['amortized_conditional_seconds_per_task']={str(n):setup['wall_seconds']/n+output['journal-conditional']['wall_median'] for n in (1,5,10,100)}
    output['task_intake_sources']=len(pins)
    output['D5G_cited_sources']=len(cited)
    output['AC4']='FAIL: equal readable-byte detection not retained by conditional mode; full mode below threshold'
    write(LOCAL / 'cost-summary04.json',output)
    # Bind the exporter to the actual initial status shown in the first tool
    # transcript. start.json was captured later, after three new task scripts.
    start=json.loads((LOCAL / 'start.json').read_text())
    if not (LOCAL / 'export-baseline.json').exists():
        write(LOCAL / 'export-baseline.json',dict(head=start['head'],index_sha256=start['index_sha256'],
        status='?? docs/implementation-briefs/CODEX_BRIEF_SOR_preservation_audit_optimization.md\n',
        basis='Initial git status tool output before edits; HEAD/index captured later in start.json. No Git writes occurred.'))
    print(json.dumps(output,indent=2))


if __name__ == '__main__':
    main()
