# SPDX-License-Identifier: GPL-3.0-or-later
"""Offline reproducibility, negative controls and queue sensitivity for D5AA.

Reads fresh authenticated derivatives and owned chronology code; writes only a
fresh .local-work destination, including altered disposable derivative copies.
Never changes primary evidence. Stdlib only, no native/observer/target effects.
Queue replay uses admitted QPC samples, serial producers and ideal periodic drains;
it is not a loss reconstruction, concurrency qualification or deployment test.
"""
from contextlib import redirect_stdout
import csv
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import sys

ROOT=Path(__file__).resolve().parents[2]

def main(source,out):
    source,out=Path(source).resolve(),Path(out).resolve()
    assert source.is_relative_to(ROOT/'.local-work')
    assert out.is_relative_to(ROOT/'.local-work') and not out.exists();out.mkdir()
    spec=importlib.util.spec_from_file_location('owned_d5aa',Path(__file__).with_name('d5aa_chronology.py'))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    with redirect_stdout(io.StringIO()):
        m.derive(source,out/'repeat-a');m.derive(source,out/'repeat-b')
    hashes=lambda p:{f.name:m.sha(f) for f in p.iterdir()}
    assert hashes(out/'repeat-a')==hashes(out/'repeat-b')
    controls={}
    for label,file,mutate in (
        ('wrong-path-clock','paths.jsonl',lambda v:v['evidence'][0].update(ticks=1)),
        ('wrong-target-epoch','conditional-target.csv',lambda v:v.update(epoch='1'))):
        trial=out/label;trial.mkdir()
        for name in ('analysis.json','paths.jsonl','conditional-target.csv','checkpoints.json'):shutil.copyfile(source/name,trial/name)
        path=trial/file
        if file.endswith('jsonl'):
            values=[json.loads(line) for line in path.read_text(encoding='utf8').splitlines()];mutate(values[0])
            path.write_text(''.join(json.dumps(v)+'\n' for v in values),encoding='utf8',newline='\n')
        else:
            values=list(csv.DictReader(path.open(encoding='utf8')));mutate(values[0]);m.write_csv(path,values)
        try:
            with redirect_stdout(io.StringIO()):m.derive(trial,out/(label+'-result'))
        except AssertionError:controls[label]='REJECTED'
        else:raise AssertionError('Altered raw-reference control accepted')
    try:m.derive(source,out/'repeat-a')
    except FileExistsError:controls['existing-output']='REJECTED'
    else:raise AssertionError('Output overwrite allowed')
    events=list(csv.DictReader((out/'repeat-a/events.csv').open(encoding='utf8')))
    partials=list(csv.DictReader((out/'repeat-a/partial-chains.csv').open(encoding='utf8')))
    assert sum(int(p['later_pointer_compatible_bypass_count'])>0 for p in partials)==23
    negative=next(p for p in partials if p['lookup_sequence']=='1227')
    assert negative['later_pointer_compatible_bypass_count']=='0' and negative['epoch']=='207'
    anchor=events[1226]
    future=[e for e in events[1227:] if e['kind']=='visited' and e['branch_a']=='1' and e['source_alias']==anchor['source_alias'] and e['proc_alias']==anchor['proc_alias'] and e['status']=='0' and e['hazards']=='0']
    assert future[0]['sequence']=='3907' and future[0]['observer_epoch']=='4974'
    assert not any(e['observer_epoch']=='207' for e in future)
    ticks=sorted(int(e['qpc_ticks']) for e in events);rows=[]
    for capacity in (1024,8192,32768):
        for gap in (0,20,100,500,1206.5674):
            period=round(gap*10000);deadline=ticks[0]+period;used=peak=refused=0
            for tick in ticks:
                if not period or tick>=deadline:
                    used=0
                    if period:deadline+=((tick-deadline)//period+1)*period
                if used==capacity:refused+=1
                else:used+=1;peak=max(peak,used)
            rows.append(dict(capacity=capacity,gap_ms=gap,cell_payload_bytes=320*capacity,peak=peak,refused_admitted_inputs=refused,coverage='SERIAL ADMITTED INPUTS ONLY; dropped attempts and producer races absent'))
    m.write_csv(out/'capacity-sensitivity.csv',rows)
    result=dict(reproducible_bytes=True,negative_controls=controls,epoch_counterexample=dict(lookup=1227,epoch=207,same_epoch_bypasses=0,first_later_pointer_bypass=3907,later_epoch=4974,positive_rows=23,audited_rows=24),events=len(events),capacity_cases=len(rows),limit='No new observer build, native queue concurrency or retail validation.',outputs=hashes(out/'repeat-a'))
    (out/'checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main(*sys.argv[1:])
