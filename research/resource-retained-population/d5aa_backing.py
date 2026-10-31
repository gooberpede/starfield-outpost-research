# SPDX-License-Identifier: GPL-3.0-or-later
"""Create a fresh sanitized review subset and original graph backing tables.

Reads a complete D5AA chronology directory; writes only a fresh local or D5AA
documentation directory. No original raw evidence, native, save, observer,
database or Git effects. CPython stdlib only. Selection is explicit and retains
451 records; full 19,780-row ledger remains local. Graph labels are authored.
"""
from pathlib import Path
import csv,json,shutil
R=Path(__file__).resolve().parents[2]
import sys
S,D=(Path(arg).resolve() for arg in sys.argv[1:])
assert S.is_relative_to(R/'.local-work')
assert D.is_relative_to(R/'.local-work') or D==R/'docs/experiments/resource-retained-population/d5aa'

D.mkdir(exist_ok=False)
def load(name):return list(csv.DictReader((S/name).open(encoding='utf8')))
def write(name,rows):
    with (D/name).open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
for name in ('paths.csv','partial-chains.csv','conditional.csv','checkpoints.csv','summary.json'):shutil.copyfile(S/name,D/name)
events=load('events.csv');byseq={int(e['sequence']):e for e in events}
chosen={1,2,3,4,110,111,115,116,117,1235,1236,19780}
for p in load('paths.csv'):chosen.update(int(v) for v in p['event_sequences'].split(';'))
for p in load('conditional.csv'):chosen.update(int(p[k]) for k in ('selection_sequence','visited_sequence'))
for p in load('partial-chains.csv'):chosen.update(int(p[k]) for k in ('first_later_bypass','last_later_bypass') if p[k])
write('events.csv',[byseq[s] for s in sorted(chosen)])
points=[(1,'READY'),(3,'First empty reset certificate'),(110,'Last pre-travel prefix event'),(116,'Second empty reset certificate'),(215,'First copied non-target map miss'),(1236,'Admission at first sampled loss boundary'),(3297,'First conditional target selection'),(10445,'Last conditional target selection'),(19780,'Last retained admission')]
write('chronology-points.csv',[dict(sequence=s,label=label,second=byseq[s]['relative_seconds'],qpc=byseq[s]['qpc_ticks'],basis='CONDITIONAL' if 'conditional' in label else 'OBSERVED') for s,label in points])
def e(a,b,basis,q):return {'from':a,'to':b,'basis':basis,'qualification':q}
g=dict(windows=[dict(label='Main-menu checkpoint',start=53.0658791,end=57.4424402),dict(label='Loaded / not-travelled checkpoint',start=159.6000001,end=165.1588306),dict(label='First-arrival checkpoint',start=245.0536603,end=249.9573088)],causality=[
e('Full load','ProcGen clear','PROVEN STATIC','Complementary revert/type-3 reset routes; B1 callers and exact stage are unknown.'),
e('Lodge interior','Linked context / existing terrain','CONDITIONAL','Interior attached context or TES interior update; actual Lodge/Jemison binding is unknown.'),
e('Accepted travel confirmation','Pending player payload +0xa08','PROVEN STATIC','Named callback; zero response, valid destination, guards; payload swap is not a FIFO queue.'),
e('Transition processor','Context / owner / descriptor setup','PROVEN STATIC','141a20380 → 1417df210; branch-specific resets and initialization.'),
e('Exterior preparation','Valid focus / source Grid / service command','PROVEN STATIC','141a278a0 prepares terrain before final placement; execution still needs valid prerequisites.'),
e('Eligible service or cell demand','Ready layer / density task','CONDITIONAL','Region, key, file and dependency guards; other tasks can execute while registration continues.'),
e('Worker provider request','Selected source / visited / map decision','OBSERVED','Nineteen non-target sampler paths; 24 copied map decisions; no copied target identity.'),
e('Target first processing','Append / later target bypass','UNKNOWN','Historical query, mask, positive bypass identity and direct append success are missing.'),
e('Final placement / visual arrival','Later movement / consumer refresh','CONDITIONAL','Native preparation can precede final placement; no B1 visual-arrival or Workshop ordering fence.')],state=[
e('Construction or qualifying reset','Unvisited / empty map','PROVEN STATIC','Two B1 reset certificates are observed; they do not establish an uninterrupted target history.'),
e('Original query selects source','Shared visited comparison','PROVEN STATIC','Source token +0x68 compared under ProcGen +0x40; source identity must remain valid.'),
e('Visited token matches','Bypass before map lookup','OBSERVED','5,675 valid bypass outcomes; 119 conditional target-compatible pairs lack copied identity.'),
e('Unvisited; release shared lock','Acquire exclusive; map hit','OBSERVED','Five copied non-target hits; concurrent checks can pass before an earlier append.'),
e('Exclusive map miss','Insert holder / generation / ordinary sampler','OBSERVED','Nineteen non-target sampler paths; generation success and complete geometry are separate.'),
e('Generation returns','Reserve visited slot','PROVEN STATIC','No geometry-success test; failure sentinel 0xffffffff skips token store.'),
e('Reservation succeeds','Token store','PROVEN STATIC','Successful reserve writes the token; B1 occurrence is not observed.'),
e('B1 append occurrence','Authenticated later source bypass','UNKNOWN','Successful append was not instrumented; pointer-compatible later bypasses are conditional joins.'),
e('Reservation fails','No token write','PROVEN STATIC','Existing map holder may remain; map reuse is independent of visited membership.'),
e('Source retirement','Map erasure; visited retained','PROVEN STATIC','No B1 retirement witness; pointer equality cannot establish lifetime continuity.'),
e('Broad reset / destruction','Clear map and visited / end lifetime','PROVEN STATIC','Observer epochs include loss and other fences; they are not native visited epochs.')])
(D/'graph-data.json').write_text(json.dumps(g,indent=2)+'\n',encoding='utf8',newline='\n')
write('transitions.csv',[dict(id=f'AA-T{i+1:02}',**row) for i,row in enumerate(g['causality'])])
write('state-edges.csv',[dict(id=f'AA-S{i+1:02}',**row) for i,row in enumerate(g['state'])])
print('selected events',len(chosen))
