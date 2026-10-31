# SPDX-License-Identifier: GPL-3.0-or-later
"""Derive sanitized B1 event and individual path ledgers, offline only.

Reads original B1 bytes with the unchanged owned decoder and a fresh authenticated
D5Y result. Writes only a fresh destination under .local-work or the D5AA figure
directory. No saves, native execution, database, observer or Git changes.
Uses CPython stdlib. Run d5y_forensics.py first; all raw fields remain local.
"""
import csv
import hashlib
import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
SESSION=ROOT/'.local-work/d5x/live/session-ceb439b14ddc4db8b734526a124f1e879b64cd457774a87a6a67852fd4489894'
TARGET='0:37536:20928:0029d20e'

def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def write_csv(p,rows):
    with p.open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)

def derive(source,out):
    source,out=Path(source).resolve(),Path(out).resolve()
    assert source.is_relative_to(ROOT/'.local-work')
    assert out.is_relative_to(ROOT/'.local-work') or out.is_relative_to(ROOT/'docs/experiments/resource-retained-population/d5aa')
    a=json.loads((source/'analysis.json').read_text(encoding='utf8'))
    raw=SESSION/'events.bin';assert sha(raw)==a['raw_sha256']=='cd4762095a422fb537844546e923fff667e894a63b082b0205f3107786f49a5c'
    path=ROOT/'runtime/construction-winner/read_capture.py'
    spec=importlib.util.spec_from_file_location('d5aa_owned_decoder',path);reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
    data=raw.read_bytes();events=[reader.decode(data[p+16:p+328]) for p in range(0,len(data),328)]
    assert len(events)==19780==a['authenticated_records']
    out.mkdir(parents=True,exist_ok=False)
    frequency=a['qpc_frequency'];t0=a['t0'];loss=a['terminal']['first_loss_sampled_admission']
    aliases={};groups=defaultdict(list)
    # These labels preserve equality only. They never assert allocation lifetime.
    def alias(p):
        if not p:return ''
        if p not in aliases:aliases[p]='P'+str(len(aliases)+1)
        return aliases[p]
    copies={e['sequence']:reader.source_key(e) for e in events if any(bytes.fromhex(e['source_bytes']))}
    rows=[]
    for e in events:
        seq=e['sequence'];sec=(e['ticks']-t0)/frequency
        if e['invocation'] and e['selection']:groups[e['invocation'],e['selection']].append(e)
        phase='BEFORE_PRETRAVEL_REQUEST' if sec<159.6000001 else 'PRETRAVEL_CHECK_WINDOW' if sec<=165.1588306 else 'BETWEEN_PRETRAVEL_ACK_AND_ARRIVAL_REQUEST' if sec<245.0536603 else 'ARRIVAL_CHECK_WINDOW'
        rows.append(dict(sequence=seq,raw_frame_offset=(seq-1)*328,kind=reader.KINDS[e['kind']],qpc_ticks=e['ticks'],relative_seconds=f'{sec:.7f}',clock='QPC/10000000;t0=2619875036404',thread=e['thread'],invocation=e['invocation'],parent=e['parent'],selection=e['selection'],observer_epoch=e['epoch'],proc_alias=alias(e['proc']),source_alias=alias(e['source']),copied_source_key=copies.get(seq,''),request_x=e['request'][0],request_y=e['request'][1],status=e['status'],hazards=e['hazards'],branch_a=e['a'] if e['kind'] in (3,4,7,10,11) else '',phase_interval=phase,loss_exposure='AFTER_FIRST_SAMPLED_LOSS' if seq>=loss else 'BEFORE_FIRST_SAMPLED_LOSS',confidence='OBSERVED_PAYLOAD',order_rule='admission sequence; QPC sample; no global engine total order',unresolved='source lifetime; append success; gameplay transition instant'))
    write_csv(out/'events.csv',rows)
    paths=[]
    for line in (source/'paths.jsonl').read_text(encoding='utf8').splitlines():
        p=json.loads(line)
        if p['outcome'] not in ('CORRELATED_ORDINARY_PATH_NO_COLD_REQUIREMENT','EXPECTED_MAP_HIT'):continue
        for ref in p['evidence']:
            original=events[ref['sequence']-1]
            assert all(original[k]==ref[k] for k in ('sequence','kind','ticks'))
        g=groups[p['invocation'],p['selection']];lookup=next(e for e in g if e['kind']==4)
        sample=next((e for e in g if e['kind']==7),None)
        keys={copies[e['sequence']] for e in g if e['sequence'] in copies}
        assert len(keys)==1 and TARGET not in keys
        paths.append(dict(invocation=p['invocation'],selection=p['selection'],source_key=next(iter(keys)),source_alias=alias(lookup['source']),epoch=lookup['epoch'],decision_epoch=lookup['d'],thread=lookup['thread'],lookup_sequence=lookup['sequence'],lookup_qpc=lookup['ticks'],lookup_second=f"{(lookup['ticks']-t0)/frequency:.7f}",map_decision='MISS' if lookup['a']==lookup['b'] else 'HIT',request_x=p['request'][0],request_y=p['request'][1],sample_sequence=sample['sequence'] if sample else '',mask=sample['a'] if sample else '',event_sequences=';'.join(str(e['sequence']) for e in g),thread_local_ticks_monotone=all(x['ticks']<=y['ticks'] for x,y in zip(g,g[1:])),successful_append='NOT_INSTRUMENTED',complete_first_to_bypass='NOT_AUTHENTICATED',loss_exposure=lookup['sequence']>=loss))
    assert len(paths)==24 and Counter(p['map_decision'] for p in paths)=={'MISS':19,'HIT':5}
    paths.sort(key=lambda p:p['lookup_sequence'])
    partial=[]
    for p in paths:
        start=events[p['lookup_sequence']-1]
        later=[e for e in events if e['sequence']>start['sequence'] and e['kind']==3 and e['a']==1 and e['source']==start['source'] and e['proc']==start['proc'] and e['epoch']==start['epoch'] and not e['status'] and not e['hazards']]
        partial.append(dict(lookup_sequence=start['sequence'],source_key=p['source_key'],epoch=start['epoch'],later_pointer_compatible_bypass_count=len(later),first_later_bypass=later[0]['sequence'] if later else '',last_later_bypass=later[-1]['sequence'] if later else '',correlation='CONDITIONAL pointer equality within observer epoch; not allocation lifetime or copied bypass identity',append_success='UNKNOWN; not instrumented'))
    write_csv(out/'paths.csv',paths);write_csv(out/'partial-chains.csv',partial)
    conditional=list(csv.DictReader((source/'conditional-target.csv').open(encoding='utf8')))
    assert len(conditional)==119 and all(x['bypass']=='True' for x in conditional)
    for x in conditional:
        selected,visited=(events[int(x[k])-1] for k in ('selection_sequence','visited_sequence'))
        assert selected['kind']==2 and visited['kind']==3 and visited['a']==1
        assert selected['invocation']==visited['invocation'] and selected['selection']==visited['selection']
        assert selected['epoch']==visited['epoch']==int(x['epoch'])
    # Retain only correlation operands, with no pointer or copied native buffer.
    write_csv(out/'conditional.csv',[{k:v for k,v in x.items() if k not in ('source','pointer')} for x in conditional])
    checkpoints=json.loads((source/'checkpoints.json').read_text(encoding='utf8'));write_csv(out/'checkpoints.csv',checkpoints)
    summary=dict(schema='sor-d5aa/1',raw_sha256=sha(raw),reader_sha256=sha(path),analysis_sha256=sha(source/'analysis.json'),records=len(rows),map_decisions=len(paths),ordinary_paths=19,conditional_bypasses=119,first_loss_sampled_admission=loss,drops=a['terminal']['drops'],qpc_admission_inversions=a['qpc_admission_inversions'],pretravel_kinds=dict(Counter(reader.KINDS[e['kind']] for e in events[:110])),copied_target_records=sum(k==TARGET for k in copies.values()),append_success_witnesses=0,complete_source_chains=0,clock_note='Absolute QPC values are observed; UTC event instants are not captured. Checkpoint UTC/QPC pairs permit approximate calibration only.',raw_reference='session/events.bin; offsets are original raw-file byte offsets',loss_note='First sampled loss admission is a counter boundary, not the exact lost event time.')
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf8',newline='\n')
    assert sha(raw)==a['raw_sha256']
    print(json.dumps(summary,indent=2))

if __name__=='__main__':derive(*sys.argv[1:])
