# SPDX-License-Identifier: GPL-3.0-or-later
"""Check D5Z source identities, scoped artifacts and reproducible graphs.

Reads the source ledger, native exports, original task receipts and authored
artifacts. Writes one fresh ignored JSON receipt. Stdlib only; no native code,
game, save decoder, analysis-database, network or Git mutation. These checks
verify identity/consistency and exact graph regeneration, not source semantics.
"""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT/'docs/experiments/resource-retained-population'

def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()

def check_links(path):
    text=path.read_text(encoding='utf8')
    targets=re.findall(r'\[[^\]]*\]\(([^)]+)\)',text) if path.suffix=='.md' else re.findall(r'href="([^"]+)"',text)
    checked=[]
    for target in targets:
        if re.match(r'[A-Za-z]+:',target):continue
        relative,_,anchor=target.partition('#')
        dest=(path.parent/relative).resolve() if relative else path
        assert dest.exists(),(path,target)
        if anchor and dest.suffix=='.md':
            headings=re.findall(r'^#+ (.+)$',dest.read_text(encoding='utf8'),re.M)
            slugs=[re.sub(r'[^\w\- ]','',s.lower()).replace(' ','-') for s in headings]
            assert anchor in slugs,(path,target,slugs)
        checked.append(target)
    return checked

def main():
    out=Path(sys.argv[1]).resolve()
    assert out.is_relative_to(ROOT/'.local-work') and not out.exists()
    with (DOC/'d5z-sources.csv').open(encoding='utf8',newline='') as stream:
        rows=list(csv.DictReader(stream))
    assert len({r['id'] for r in rows})==len(rows)
    verified={}
    for row in rows:
        path=Path(row['path'])
        if not path.is_absolute():path=ROOT/path
        assert path.stat().st_size==int(row['bytes']),row['id']
        if str(path) not in verified:verified[str(path)]=sha(path)
        assert verified[str(path)]==row['sha256'],row['id']
        if row['line_start']:
            lines=path.read_text(encoding='utf8').splitlines()
            start,end=int(row['line_start']),int(row['line_end'])
            assert 1<=start<=end<=len(lines),row['id']
            if row['static_va']:
                assert lines[start-1].startswith('FUNCTION\t'+row['static_va'][2:]+'\t'),row['id']
    with (DOC/'d5z/checklist-audit.csv').open(encoding='utf8',newline='') as stream:
        audit=list(csv.DictReader(stream))
    checklist=(DOC/'resource-generation-gameplay-checklist.md').read_text(encoding='utf8')
    items=re.findall(r'^- \[([x ])\] (.+)$',checklist,re.M)
    assert len(items)==len(audit)==31
    for (tick,text),row in zip(items,audit):
        assert tick==row['durable_tick'] and text==row['durable_operation']
        assert row['original_tick']=='x' or tick==' '
        assert 'Native ' in text and 'Specific B1 event observed:' in text
    with (DOC/'d5z-state-access.csv').open(encoding='utf8',newline='') as stream:
        accesses=list(csv.DictReader(stream))
    assert len(accesses)==10 and all(None not in row and None not in row.values() for row in accesses)
    graph_path=DOC/'d5z/graph-data.json'
    graph_data=json.loads(graph_path.read_text())
    spec=importlib.util.spec_from_file_location('owned_d5z_figures',Path(__file__).with_name('d5z_figures.py'))
    figures=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(figures)
    graph_hashes={}
    for graph in graph_data['graphs']:
        path=DOC/'d5z'/graph['file']
        assert path.read_text(encoding='utf8')==figures.render(graph)
        ET.fromstring(path.read_bytes())
        nodes={n['id'] for n in graph['nodes']}
        assert len(nodes)==len(graph['nodes'])
        assert all(e['source'] in nodes and e['target'] in nodes for e in graph['edges'])
        graph_hashes[graph['file']]=sha(path)
    b1=json.loads((ROOT/'.local-work/d5z/b1-02/b1.json').read_text())
    assert b1['records']==19780 and b1['pretravel_records']==110
    assert len(b1['matched_certificates'])==2 and b1['reader_qualified_chains']==0
    assert b1['conditional_target_bypasses']==119 and b1['target_copied_records']==0
    save=json.loads((ROOT/'.local-work/d5z/save-04/save-prefix.json').read_text())
    assert save['independent_descriptor_span_match'] and len(save['world_descriptors'])==88
    assert save['prefix_logical_offset']==4085 and save['world_descriptor_end']==5421
    assert save['remaining_unit3_bytes']==892
    assert save['header_structure_version']['value']==27
    assert save['native_buffer_version']['value']==153 and save['native_buffer_version']['at_least_0x3e']
    control=json.loads((ROOT/'.local-work/d5z/append-01/control.json').read_text())
    assert control['passed'] and len(control['cases'])==6 and not control['game_process']
    # Exact arithmetic consequences, not a simulated allocator or memory bound.
    arithmetic=dict(element_bytes=8,control_bytes=16,last_doubling_capacity_before_byte_wrap=268435456,
                    bytes_at_that_capacity=8*268435456,next_capacity=536870912,
                    wrapped_next_bytes=(8*536870912)&0xffffffff)
    assert arithmetic['wrapped_next_bytes']==0
    authored=sorted(set(DOC.glob('d5z*.md'))|set((DOC/'d5z').glob('*'))|{DOC/'resource-generation-gameplay-checklist.md'})
    links={}
    for path in authored:
        if path.suffix not in ('.md','.json','.svg','.csv'):continue
        raw=path.read_bytes()
        assert not raw.startswith(b'\xef\xbb\xbf') and b'\r' not in raw,path
        assert all(line.rstrip()==line for line in raw.decode('utf8').splitlines()),path
        if path.suffix in ('.md','.svg'):links[str(path.relative_to(ROOT))]=check_links(path)
    result=dict(schema='sor-d5z-checks/1',source_rows=len(rows),verified_sources=verified,
                checklist_items=len(items),reproducible_graphs=graph_hashes,links=links,
                arithmetic=arithmetic,b1_sha256=sha(ROOT/'.local-work/d5z/b1-02/b1.json'),
                save_sha256=sha(ROOT/'.local-work/d5z/save-04/save-prefix.json'),
                limit='Identity, framing, consistency, arithmetic and regeneration checks do not independently prove native semantics.')
    out.parent.mkdir(parents=True,exist_ok=True)
    with out.open('x',encoding='utf8',newline='\n') as stream:
        stream.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(sources=len(rows),checklist_items=len(items),figures=len(graph_hashes),passed=True)))

if __name__=='__main__':
    main()
