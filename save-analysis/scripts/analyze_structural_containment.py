"""Bounded structural containment analysis of existing S/L archives.

Reads: prior manifests, verified archived .sfs and prior analysis hashes; originals
for integrity hashing only. Writes: a fresh --run under ignored structural root;
numeric CSV summaries and local JSON. No decoded blob duplication, editor, live
process interaction, dependency download or external parser. CPython stdlib only.
Directory labels are structural aliases, not proven engine schema names.
"""
from pathlib import Path
import argparse
import csv
import datetime as dt
import json
import struct
import sys
import zlib

from analyze_manual_corpus import decode, sha, hits
from probe_manual_candidates import MAIN
from probe_output_link_structure import BASE_LIKE

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / '.local-work/structural-containment'
S = ROOT / '.local-work/manual-S0-S7C'
L = ROOT / '.local-work/output-link-L0-L2C'
BRIEF = ROOT / 'docs/implementation-briefs/CODEX_RESEARCH_BRIEF_outpost_save_structural_containment.md'
REGION_NAMES = ['early_metadata', 'region_R1', 'region_R2', 'region_R3', 'region_R4', 'reference_u32', 'late_region']


def u32(b,p):
    return struct.unpack_from('<I',b,p)[0]


def directory(b):
    """Unique early six-pointer hypothesis with independently closed u32 table."""
    found=[]
    for p in range(160,min(8192,len(b)-100)):
        v=struct.unpack_from('<10I',b,p)
        a,c=v[:2]
        if (1000<a<c<len(b) and a+4+u32(b,a)*4==c
                and 0<v[2]<v[3]<v[4]<v[5]<a
                and all(0<x<100000 for x in v[6:])):
            found.append((p,v))
    if len(found)!=1:
        raise ValueError(f'Directory ambiguous/missing: {found}')
    p,v=found[0]
    bounds=[0,v[2],v[3],v[4],v[5],v[0],v[1],len(b)]
    return dict(offset=p, words=list(v), auxiliary_words=list(struct.unpack_from('<16I',b,p+40)),
                regions={n:[bounds[i],bounds[i+1]] for i,n in enumerate(REGION_NAMES)},
                reference_count=u32(b,v[0]))


def endpoints(b):
    result={}
    for role,base in BASE_LIKE.items():
        found=[]
        for q in hits(b,bytes.fromhex(base)):
            p=q-15
            if p>=0 and b[p]==0x3a and b[p+4:p+8]==bytes.fromhex(MAIN[role])[4:8] and b[p+1:p+4]==b[p+18:p+21]:
                found.append(p)
        if len(found)>1:
            raise ValueError(f'Ambiguous endpoint {role}: {found}')
        if found:
            p=found[0];token=b[p+1:p+4]
            result[role]=dict(offset=p, token=token.hex(), window_length=512, window_sha256=sha(b[p:p+512]),
                base_like=base, base_arithmetic=int(base,16)&0x3fffff,
                full_dynamic_arithmetic=0xff000000|(int.from_bytes(token,'big')&0x3fffff))
    return result


def tail_table(b):
    """Maximal exact-to-EOF sorted FF-prefixed uint32/count pairs, <=64KiB.

    A suffix can falsely close too; require ascending IDs, nonzero counts, FF tag
    and select maximal count. This remains an empirical tail-table hypothesis.
    """
    found=[]
    for p in range(max(0,len(b)-65536),len(b)-3):
        n=u32(b,p)
        if 0<n<=8191 and p+4+8*n==len(b):
            pairs=[struct.unpack_from('<II',b,p+4+8*i) for i in range(n)]
            if all(v>>24==255 and 0<c<100000 for v,c in pairs) and all(pairs[i][0]<pairs[i+1][0] for i in range(n-1)):
                found.append((p,pairs))
    if not found:
        raise ValueError('Missing tail table')
    p,pairs=max(found,key=lambda x:len(x[1]))
    return dict(offset=p,count=len(pairs),entries={v:(p+4+i*8,c) for i,(v,c) in enumerate(pairs)},suffix_candidates=len(found))


def relation(b,ep,d):
    if 'beacon' not in ep:
        return None
    a,z=d['regions']['region_R2'];token=bytes.fromhex(ep['beacon']['token']);found=[]
    for p in hits(b[a:z],bytes.fromhex('79000000')):
        p+=a;n=u32(b,p+4);end=p+8+n
        if n in (5,12,19) and b[p+8:p+12]==b'\x04'+token and b[end:end+8]==bytes.fromhex('7a00000028000000'):
            found.append(dict(offset=p,length=n,payload_offset=p+8,end=end,payload_sha256=sha(b[p+8:end])))
    if len(found)>1:
        raise ValueError(f'Relation envelope ambiguous: {found}')
    return found[0] if found else None


def string_pool(b,d,ep):
    pointer_field=d['regions']['region_R1'][0]+4
    start=u32(b,pointer_field)
    if not d['regions']['late_region'][0]<=start<len(b)-2:
        raise ValueError('String pool pointer outside late region')
    count=int.from_bytes(b[start:start+2],'little');p=start+2;entries=[];name=None
    if not 0<count<10000:raise ValueError('Unsupported string count')
    for i in range(count):
        if p+2>len(b):raise ValueError('String length bounds')
        n=int.from_bytes(b[p:p+2],'little');end=p+2+n
        if end>len(b):raise ValueError('String body bounds')
        entries.append((p,b[p+2:end]));p=end
    matches=[i for i,(_,t) in enumerate(entries) if t in [b'Kreet Outpost 1',b'SOR-001']]
    if len(matches)>1:raise ValueError('Ambiguous name entry')
    if matches:
        i=matches[0];q,t=entries[i]
        if i+2>=count or entries[i+1][1]!=b'OBJ_Outpost_Beacon_Deploy' or entries[i+2][1]!=b'OBJ_Outpost_Beacon_On_LP':
            raise ValueError('Name-neighbor invariant failed')
        pattern=struct.pack('<3H',i,i+1,i+2)
        e=ep['beacon'];off=e['offset'];matched=hits(b[off:off+512],pattern)
        if len(matched)!=1:raise ValueError('Beacon string-index triple ambiguous/missing')
        name=dict(offset=q,text_offset=q+2,length=2+len(t),text=t.decode(),pool_index=i,
                  beacon_index_relative_offset=matched[0],index_triple_global_hits=hits(b,pattern))
    return dict(pointer_field=pointer_field,start=start,end=p,count=count,span=p-start),name


def unequal(a,b):
    common=min(len(a),len(b))
    changed=sum(x!=y for x,y in zip(a,b))+abs(len(a)-len(b))
    return dict(before_size=len(a),after_size=len(b),delta=len(b)-len(a),
                positional_unequal_bytes=changed,density=changed/max(len(a),len(b),1),aligned_common_length=common)


def write_csv(path,rows):
    with path.open('x',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)


def verify(s):
    for field in ['source_before','copy']:
        x=s[field];p=Path(x['path'])
        if field=='copy' and not p.resolve().is_relative_to((ROOT/'.local-work/savegames').resolve()):
            raise ValueError('Archive outside authorized root')
        if sha(p.read_bytes())!=x['sha256'] or p.stat().st_size!=x['size']:
            raise ValueError(f'Integrity failure {s["label"]}/{field}')
    return dict(label=s['label'],sha256=s['copy']['sha256'],original_mtime_ns=Path(s['source_before']['path']).stat().st_mtime_ns)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);args=ap.parse_args()
    if not args.run or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in args.run):
        raise ValueError('Simple fresh run name required')
    out=BASE/args.run;out.mkdir(exist_ok=False,parents=True)
    groups=[(S,[f'S{i}{c}' for i in range(8) for c in ['', 'C']]),(L,['L0','L0C','L1','L1C','L2','L2C'])]
    specs=[];data={};records=[];growth=[];chunks=[];anchors=[];maps=[];preservation=[]
    manifest_hashes={}
    for root,labels in groups:
        manifest=json.loads((root/'manifest.json').read_text(encoding='utf-8'));manifest_hashes[str(root.relative_to(ROOT))]=sha((root/'manifest.json').read_bytes())
        old=json.loads((root/'analysis-01/analysis.json').read_text(encoding='utf-8'))
        for label in labels:
            s=next(x for x in manifest['samples'] if x['label']==label);specs.append(s);preservation.append(verify(s))
            physical=Path(s['copy']['path']).read_bytes();raw,cs=decode(physical)
            prior=next(x for x in old['samples'] if x['label']==label)
            if sha(raw)!=prior['decoded_sha256']:
                raise ValueError('Decoded hash differs from existing derivative')
            d=directory(raw);ep=endpoints(raw);rel=relation(raw,ep,d);pool,name=string_pool(raw,d,ep);tail=tail_table(raw)
            rec=dict(label=label,sample_id=s['sample_id'],source_sha256=sha(physical),decoded_sha256=sha(raw),file_size=len(physical),decoded_size=len(raw),directory=d,endpoints=ep,relation=rel,name=name,string_pool=pool,tail={k:v for k,v in tail.items() if k!='entries'},chunks=cs)
            data[label]=(raw,physical,rec);records.append(rec)
            for region,(a,z) in d['regions'].items():growth.append(dict(label=label,region=region,start=a,end=z,size=z-a))
            growth.append(dict(label=label,region='string_pool',start=pool['start'],end=pool['end'],size=pool['span']))
            growth.append(dict(label=label,region='tail_pair_candidate',start=tail['offset'],end=len(raw),size=len(raw)-tail['offset']))
            for ch in cs:chunks.append(dict(label=label,**{k:ch[k] for k in ['index','file_offset','compressed_size','decoded_offset','decoded_size','decoded_sha256']}))
            candidates=[(role,e['offset'],512,e['token']) for role,e in ep.items()]
            if rel:candidates.append(('output_relationship',rel['offset'],8+rel['length'],ep['beacon']['token']))
            if name:candidates.append(('outpost_name',name['offset'],name['length'],''))
            for role,p,n,token in candidates:
                region=next(k for k,(a,z) in d['regions'].items() if a<=p<z)
                first,last=p//262144,(p+n-1)//262144
                anchors.append(dict(label=label,anchor=role,logical_offset=p,extent=n,extent_kind='analysis_window_not_record' if role in ep else 'observed_length_field',region=region,chunk_first=first,chunk_last=last,compressed_stream_start=cs[first]['file_offset'],compressed_stream_end=cs[first]['file_offset']+cs[first]['compressed_size'],compressed_stream_size=cs[first]['compressed_size'],decoded_chunk_size=cs[first]['decoded_size'],exact_physical_anchor_offset='UNRESOLVED_WITHIN_COMPRESSED_STREAM',token=token))
            for role,e in ep.items():
                v=e['full_dynamic_arithmetic'];entry=tail['entries'].get(v)
                maps.append(dict(label=label,role=role,token=e['token'],dynamic_arithmetic=f'{v:08X}',tail_match=bool(entry),tail_offset=entry[0] if entry else '',associated_u32=entry[1] if entry else '',full_u32_hits=len(hits(raw,struct.pack('<I',v))),base_like=e['base_like'],base_arithmetic=f'{e["base_arithmetic"]:08X}'))
                if not entry:print('NEGATIVE tail mapping',label,role,hex(v),tail['count'])
    actions={('S0C','S1'):'beacon',('S1C','S2'):'storage',('S2C','S3'):'extractor_solar',('S3C','S4'):'link',('S4C','S5'):'rename',('S5C','S6'):'solar_move',('S6C','S7'):'delete',('L0C','L1'):'unlink',('L1C','L2'):'relink'}
    pairs=[]
    for _,labels in groups:
        pairs+=list(zip(labels,labels[1:]))
    density=[];window_changes=[]
    for a,b in pairs:
        ra,pa,sa=data[a];rb,pb,sb=data[b]
        kind='RELOAD_RESERIALIZATION' if a=='L0' else actions.get((a,b),'CONTROL')
        for region in REGION_NAMES:
            x,z=sa['directory']['regions'][region];y,w=sb['directory']['regions'][region]
            density.append(dict(before=a,after=b,operation=kind,domain='logical_directory_region',unit=region,**unequal(ra[x:z],rb[y:w])))
        for i in range(max(len(sa['chunks']),len(sb['chunks']))):
            ca=sa['chunks'][i];cb=sb['chunks'][i]
            density.append(dict(before=a,after=b,operation=kind,domain='decoded_chunk_positional',unit=i,**unequal(ra[ca['decoded_offset']:ca['decoded_offset']+ca['decoded_size']],rb[cb['decoded_offset']:cb['decoded_offset']+cb['decoded_size']])))
            density.append(dict(before=a,after=b,operation=kind,domain='compressed_stream_positional',unit=i,**unequal(pa[ca['file_offset']:ca['file_offset']+ca['compressed_size']],pb[cb['file_offset']:cb['file_offset']+cb['compressed_size']])))
        for role in ['beacon','storage','extractor','solar','relationship','name']:
            def segment(raw,rec):
                if role in rec['endpoints']:
                    p=rec['endpoints'][role]['offset'];return raw[p:p+512]
                if role not in ['relationship','name']:return b''
                c=rec['relation' if role=='relationship' else role]
                if not c:return b''
                return raw[c['payload_offset']:c['end']] if role=='relationship' else raw[c['offset']:c['offset']+c['length']]
            x=segment(ra,sa);y=segment(rb,sb)
            window_changes.append(dict(before=a,after=b,operation=kind,candidate=role,**unequal(x,y)))
    final=[verify(s) for s in specs]
    if preservation!=final:raise ValueError('Input changed during analysis')
    if manifest_hashes!={str(root.relative_to(ROOT)):sha((root/'manifest.json').read_bytes()) for root,_ in groups}:raise ValueError('Manifest changed')
    write_csv(out/'growth.csv',growth);write_csv(out/'chunks.csv',chunks);write_csv(out/'anchors.csv',anchors);write_csv(out/'token-mapping.csv',maps);write_csv(out/'density.csv',density);write_csv(out/'candidate-changes.csv',window_changes)
    result=dict(created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),script_sha256=sha(Path(__file__).read_bytes()),brief_sha256=sha(BRIEF.read_bytes()),decoder_sha256=sha((Path(__file__).parent/'analyze_manual_corpus.py').read_bytes()),python=sys.version,python_executable_sha256=sha(Path(sys.executable).read_bytes()),zlib_runtime=zlib.ZLIB_RUNTIME_VERSION,manifest_hashes=manifest_hashes,samples=records,preservation_before=preservation,preservation_after=final,metric='positional mismatches plus unmatched tail; descriptive, inflated by shifting/reordering, not semantic changed bytes')
    with (out/'analysis.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
    print('Verified labels',len(records),'unique saves',len(set(x['source_sha256'] for x in records)),'chunks',sum(len(r['chunks']) for r in records),'tail matches',sum(m['tail_match'] for m in maps))
    for r in records:print(r['label'],r['directory']['offset'],[v[1]-v[0] for v in r['directory']['regions'].values()],r['tail']['count'])
    print('Saved',out)

if __name__=='__main__':main()
