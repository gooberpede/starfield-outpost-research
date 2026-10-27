# SPDX-License-Identifier: GPL-3.0-or-later
"""Apply the independently reviewed native first-miss proof to task ledgers.

The native proof is manual/instruction-backed, not inferred from a numeric mask
match. Requires its explicitly supplied exact review-receipt SHA-256. Reads the
candidate ledgers and witness02; preserves their original task-only bytes locally,
updates only these task-authored CSVs, writes a fresh ignored receipt. No frozen
historical result, generator, target, save, archive, analysis DB or Git writes.
Stdlib and owned D5H methods only (SOR-P-0002).
"""
import argparse
import collections
import csv
import json
from pathlib import Path
from audit import ROOT, LOCAL, pin, write


def save_csv(path,rows):
    with path.open('w',encoding='utf8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader();writer.writerows(rows)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--proof',type=Path,required=True)
    parser.add_argument('--proof-sha256',required=True)
    parser.add_argument('--receipt',type=Path,required=True)
    args=parser.parse_args()
    proof=args.proof.resolve();output=args.receipt.resolve()
    assert proof.is_relative_to(LOCAL) and pin(proof)==args.proof_sha256
    assert output.is_relative_to(LOCAL) and not output.exists()
    doc=ROOT/'docs/experiments/resource-query-reachability'
    source=doc/'source-domains.csv';candidate=doc/'counterexamples.csv'
    rows=list(csv.DictReader(source.open(encoding='utf8')))
    examples=list(csv.DictReader(candidate.open(encoding='utf8')))
    assert len(rows)==25 and len(examples)==31
    assert collections.Counter(row['classification'] for row in rows)=={
        'PROVED INVARIANT':19,'UNRESOLVED':6}
    assert all(row['actual_first_miss']=='NOT_PROVED' for row in examples)
    selected=[r for r in rows if r['source_key']=='0:37536:20928:0029d20e']
    assert len(selected)==1
    row=selected[0]
    assert row['pre_projection_masks']==row['modeled_roundtrip_masks']=='0;3'
    vectors=json.loads(row['ordinary_vectors'])
    assert vectors['0']!=vectors['3'] and all(x>0 for m in ('0','3') for x in vectors[m])
    witness_path=LOCAL/'witness02.json';witness=json.loads(witness_path.read_text())
    assert witness['helper_sha256']==pin(ROOT/'research/resource-query-reachability/witness.py')
    assert witness['arithmetic_receipt_sha256']==pin(LOCAL/'native-bytes09.json')
    assert [r['continuation'] for r in witness['rows']]==['L','H']
    for state,expected,root,query,offset in zip(witness['rows'],(0,3),([5,-2],[5,0]),
                                             ([37540,20927],[37540,20929]),([4,-1],[4,1])):
        assert state['root']==root and state['density_queries'][0]['geographic_query']==query
        assert all(result['emitted'][0]==row['source_key']
                   for result in state['first_query_occupancy']['permutation_outcomes'])
        assert all(b['mask']==expected and b['vector']==vectors[str(expected)]
                   for q in state['density_queries'] for b in q['branches'])
        examples.append(dict(case=row['case'],source_key=row['source_key'],
            geographic_pre_projection=';'.join(map(str,query)),
            source_relative_query=';'.join(map(str,offset)),outside_nominal=offset[1]<0,
            raster_mask=expected,ordinary_vector=json.dumps(vectors[str(expected)],separators=(',',':')),
            insertion_attempt=True,actual_slot_occupancy='PROVED_EMITTED_FIRST',
            actual_first_miss='PROVED_STATIC_FEASIBLE',
            verdict=f"Admitted static witness {state['continuation']}; original root A+({root[0]},{root[1]}); qualified proof in feasibility.md; not a historical observation"))
    before=dict(source_sha256=pin(source),candidate_sha256=pin(candidate))
    for path in (source,candidate):
        backup=LOCAL/(path.stem+'.candidate04.csv')
        with backup.open('xb') as stream:stream.write(path.read_bytes())
    row['classification']='PROVED VARIABLE'
    row['first_miss_mask_lower']='0;3'
    row['qualification']+='; initialized fixed main-file CellLoad prefix; healthy started pool; ready component/raster/file inputs; common allocation and owner state'
    row['missing_operands']='Historical first query and actual source-lifetime ordering remain unobserved; qualified prospective mask set is closed'
    row['domain_status']='Two admitted static first-miss continuations; mask lower equals qualified upper {0,3}; not a historical replay'
    for other in rows:
        if other['classification']=='UNRESOLVED':
            other['missing_operands']='Source-specific retained emission slots and first-miss dependency prefix in a coherent initialized frame; qualified owner-component/raster readiness'
    save_csv(source,rows);save_csv(candidate,examples)
    assert candidate.read_bytes().startswith((LOCAL/'counterexamples.candidate04.csv').read_bytes())
    write(output,dict(proof=str(proof.relative_to(ROOT)),proof_sha256=pin(proof),
        witness_sha256=pin(witness_path),helper_sha256=pin(Path(__file__)),before=before,
        source_sha256=pin(source),counterexamples_sha256=pin(candidate),
        classifications=dict(collections.Counter(r['classification'] for r in rows)),
        original_candidate_rows_preserved=31,admitted_static_witnesses=2,
        historical_classifications_changed=False,geometry_rerun=False,
        qualification='Manual native proof application; prospective ordinary domain, not observed historical construction'))
    print('Applied reviewed static proof: 19 invariant, 1 variable, 5 unresolved; 31 candidates plus 2 admitted witnesses')


if __name__=='__main__':main()
