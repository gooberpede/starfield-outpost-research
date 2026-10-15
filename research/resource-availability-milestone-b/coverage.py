# SPDX-License-Identifier: GPL-3.0-or-later
"""Stream every sealed 070 WAL/raw record. Stdlib and owned readers only.
Reads original evidence without edits. Writes exclusive local summary and SQLite
uniqueness index (fixed cache); holds only active invocations, aggregates and six
population runs. No process, game, save or analysis-database effects.
"""
import argparse, collections, hashlib, json, sqlite3, struct, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'runtime/beacon-resource-070'),str(ROOT/'save-analysis/scripts'),str(Path(__file__).parent)]
from inspect_resources import records, field, resource
from resource_availability import ResourceOperand, UIInputs, EXE_SHA256, project_ui_rows
from preserve import disk
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--session',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); args=ap.parse_args()
    disks=disk(); args.out.mkdir(exist_ok=False)
    db=sqlite3.connect(args.out/'unique.sqlite'); db.execute('pragma cache_size=-2048')
    db.execute('create table inputs (key blob primary key, count integer)')
    db.execute('create table positions (key blob primary key, count integer)')
    def unique(table,key): db.execute(f'insert into {table} values (?,1) on conflict(key) do update set count=count+1',(key,))
    pending={}; counts=collections.Counter(); kinds=collections.Counter(); statuses=collections.Counter(); refresh=collections.Counter(); sources=[collections.Counter() for _ in range(3)]; frames=collections.Counter(); params=collections.Counter(); domain=collections.Counter(); run=None; runs=[]; previous=None; ui_sets=collections.Counter(); transitions=[]; max_active=0
    def entry(i): return pending.setdefault(i,dict(pops={},children=[],census=[]))
    def operands(pop):
        if pop is None: return None
        assert pop['status']==0 and len(pop['members'])*8==pop['end']-pop['begin']
        return tuple(ResourceOperand(m['pointer'],m['form_id']) for m in pop['members'])
    for e in records(args.session):
        counts['records']+=1; kinds[e['kind']]+=1; statuses[e['status']]+=1
        v=entry(e['invocation']); max_active=max(max_active,len(pending)); k=e['kind']; phase=e['phase']
        if k==108:
            v['pops'][phase,e['args'][0]]=dict(begin=e['args'][1],end=e['args'][2],status=e['status'],members=[])
        elif k==109:
            pop=v['pops'][phase,e['args'][0]]; assert e['args'][3]==len(pop['members']); pop['members'].append(resource(e)); pop['status']|=e['status']
        elif k==110:
            assert e['args'][3]==len(v['census']) and e['operand']['ok']; v['census'].append(e['operand']['address'])
        elif phase==1:
            assert 'before' not in v; v['before']=e
        else:
            assert phase==2 and 'before' in v and not e['status']; b=v['before']; assert b['kind']==k and b['parent']==e['parent']
            if k==101:
                counts['evaluations']+=1; assert b['ref']['ok'] and b['ref']['length']==24
                indexed=bytes.fromhex(b['ref']['bytes']); x,y,z,frame,dp=struct.unpack('<fffIQ',indexed)
                frames[frame]+=1; domain[str((dp,field(b['operand'],0x28,'<I'),field(b['operand'],0x2e,'<B')))]+=1
                params[str(tuple(b['args'][2:4]))]+=1
                unique('positions',indexed); unique('inputs',indexed+struct.pack('<QQ',*b['args'][2:4]))
                populations=[operands(v['pops'].get((2,i))) for i in range(3)]; assert all(p is not None for p in populations)
                signature=tuple(tuple(m.form_id for m in p) for p in populations)
                for i,p in enumerate(signature): sources[i][str(p)]+=1
                change=previous is not None and signature!=previous; refresh[str((e['result']&255,change))]+=1; previous=signature
                if change or run is None:
                    if run: runs.append(run)
                    run=dict(first_invocation=e['invocation'],first_qpc=b['qpc'],last_qpc=e['qpc'],count=0,populations=signature,first_xyz=[x,y,z])
                run.update(last_invocation=e['invocation'],last_qpc=e['qpc'],last_xyz=[x,y,z]); run['count']+=1
                if e['site']==0x21b42e3: counts['preview_evaluations']+=1
                else: counts['initialization_evaluations']+=1
            elif k==102:
                counts['ui_updates']+=1
                common={c['kind']:c for c in v['children'] if c['kind'] in (103,104)}; assert len(common)==2
                special=operands(v['pops'].get((1,2)))
                selector=field(b['operand'],0,'<Q'); assert selector is not None
                selected=field(b['cell'],0x28,'<I') if selector else None; assert not selector or selected is not None
                first=common[103]['population']; second=common[104]['population']
                predicted=project_ui_rows(UIInputs(EXE_SHA256,args.session.name,str(e['invocation']),first,second,special,True,selected,True))
                rows=sorted((c for c in v['children'] if c['kind']==106),key=lambda c:c['ordinal'])
                assert [r['ordinal'] for r in rows]==list(range(len(v['census'])))
                start,end=field(e['output'],0x38,'<Q'),field(e['output'],0x40,'<Q'); assert end-start==0x170*len(rows)
                actual=[r['resource']['form_id'] for r in rows]
                assert predicted['ui_form_set']==sorted(set(actual))
                assert [r['runtime_form_id'] for r in predicted['ui_rows']]==actual
                counts['ui_exact_order_and_set']+=1; ui_sets[str(actual)]+=1
                if run: run.setdefault('ui_updates',0); run['ui_updates']+=1
                transitions.append(dict(invocation=e['invocation'],qpc=[b['qpc'],e['qpc']],rows=actual,selector=selected))
            if e['parent']:
                parent=entry(e['parent']); child=dict(kind=k)
                if k in (103,104): child['population']=operands(v['pops'].get((1,0 if k==103 else 1)))
                elif k==106: child.update(ordinal=b['command'],resource=resource(b)); assert e['operand']['ok']
                parent['children'].append(child)
            del pending[e['invocation']]
    if run: runs.append(run)
    assert not pending; retired=json.loads((args.session/'retired.json').read_text()); assert retired['failed']==retired['active']==0 and retired['last_durable_sequence']==counts['records']
    db.commit()
    hist={t:dict(db.execute(f'select count, count(*) from {t} group by count')) for t in ('positions','inputs')}
    uniques={t:db.execute(f'select count(*) from {t}').fetchone()[0] for t in hist}; db.close()
    # Independently label phase intervals by operator receipt containment only.
    phases=[]
    for p in sorted(args.session.glob('operator-*.json')):
        m=json.loads(p.read_text()); q=m['receipt_monotonic_ns']//100
        phases.append(dict(phase=m['phase'],labels=m['reported_labels'],marker=p.name,runs=[i for i,r in enumerate(runs) if r['first_qpc']<=q<=r['last_qpc']]))
    out=dict(schema='sor-resource-capture-coverage/1',counts=counts,kinds=kinds,statuses=statuses,unique=uniques,repetition_histogram=hist,
             frames=frames,domains=domain,radius_geometry_bits=params,source_populations=sources,refresh_change=refresh,runs=runs,ui_sets=ui_sets,ui=transitions,phases=phases,
             max_pending_invocations=max_active,missing_native_region_operands=True,region_identity_count=None,spatial_oracle_comparisons=0,
             disk=disks,source_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    with (args.out/'coverage.json').open('x',encoding='utf8') as f: json.dump(out,f,indent=2)
    print(json.dumps(dict(counts=counts,unique=uniques,max_pending=max_active)))
if __name__=='__main__': main()
