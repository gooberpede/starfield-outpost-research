# Supported alternatives and falsifiers

2026-10-25, Australia/Sydney. [Report](report.md), [complete source matrix](discrimination.csv),
[resource outcomes](outcomes.csv), [identity context](identity-context.csv).
All numeric outcomes are DERIVED conditional predictions, not native observations.

## What constitutes an alternative

D5 establishes one initial ordinary sample before the resource/cell loops and
its low-nibble admission predicate. It does not establish a unique historical
query. Each source's two candidates are actual installed masks in the retained
conservative source neighbourhood, with representative fine cells in `cases.csv`.
Those cells are raster/context examples, **not independently qualified initial
caller queries**. Query-to-geographic round-trip and source-selection reachability
are still unknown. The candidate set is not claimed exhaustive outside that
neighbourhood. A captured mask outside it falsifies that coverage assumption;
it is useful contrary evidence, not an invalid run or permission to fit the set.

Three query explanations remain distinguishable only if their actual sampled
positions differ: the original first caller query, source anchor and beacon
location. Static instructions support the first. Saved source/beacon coordinates
support the existence of the latter two positions, not that either was the first
caller. If all three produce the same mask, mask equality alone cannot choose a
query explanation; the acquired original query and operand lineage are required.
Later per-cell sampling is already contradicted by the static ordinary dataflow.
No hypothetical continuous query sweep is treated as engine evidence.

## Ordered operands

The admission multiplier is 1 unless mask is 8 or smaller than resource rarity;
then it is the corresponding installed inactive setting. A rarity-6 ordinary
occurrence uses zero in that inactive branch. Exact binary32 setting values are
in `prediction-freeze.json` and `outcomes.csv`; displayed decimals below are
rounded for readability. Multipliers are not chances by themselves: DNAM chance,
random draws and competition remain unchanged in the owned generator.

| Site | Ordered ordinary occurrences | Mask A weights → mask B weights | Interpretation |
|---|---|---|---|
| VI-b | He-3 `0x000057f5` rarity 5; Be `0x000057d8` rarity 1; Al `0x000057d6` rarity 0 | 0: (0.3,0.2,1) → 8: (0.3,0.2,0.3) | Only Al's multiplier distinguishes; ordinary He-3 generates no paths with this DNAM in either run. Special He-3 remains outside this table. |
| VII-b comparison | He-3 rarity 5; Nd `0x000057db` rarity 2; Al rarity 0 | 0: (0.3,0.1,1) → 2: (0.3,1,1) | Nd changes; Al can change through prior-resource competition. No unresolved saved association remains at this site. |
| Second V | IL `0x000057d4` rarity 3; F `0x000057d0` rarity 1; Cu `0x000057cf` rarity 0 | 0: (0.05,0.2,1) → 3: (1,1,1) | Two direct admission contrasts, plus different Cu competition history. |
| VIII-b | Water `0x000083ec` rarity 6; Sb `0x000057d3` rarity 3; Au `0x000057d2` rarity 2; F rarity 1; Cu rarity 0 | 0: (0,0.05,0.1,0.2,1) → 3: (0,1,1,1,1) | Three weight contrasts; zero Water occurrence is not a finite Water vein or atmosphere observation. |

Candidate identities and ordering are invariant across each source's two tested
masks. No mask in this experiment chooses a new candidate family or descriptor.
The source path counts and per-resource positive-area counts in the CSV retain
effects of competition and source-specific seeds. Unknown-area counts are zero
for these 90 resource rows. Zero paths is a scoped conditional output, not a
general resource absence claim.

## Every source and what a capture could refute

The machine-readable matrix has one row per source and both outcomes. It names
the missing query/frame/mask/current-Workshop operands for every row. All 13
sources differ in at least one native multiplier and total path count. Only
three differ inside the relevant footprint; ten are nondiscriminating for
ordinary footprint availability in these two branches. This includes the two
VII-b comparison sources and eight candidate sources. Even the three selected
footprint cases often retain the same resource presence under both masks.

For each row, captured mask A rejects mask B **for that witnessed invocation**;
mask B rejects A. Neither rejects the historical Save52 alternative. Correct
mask with different candidate order, DNAM or multiplier refutes the installed
projection or its current-state applicability before geometry. A matching
multiplier alone does not prove generated path counts. Path predictions become
testable only with complete acquired source/frame/settings and new geometry.
An unbound source, borrowed query, truncated chain or cache-only observation
does not test either initial-mask branch.

Saved extractor presence supplies positive configuration witnesses, and the
screenshot inventory supplies later visual comparisons. Neither has a negative
oracle capable of selecting an initial mask. Water admission, Special and
atmospheric routes remain separately classified and untested here.

## Reproduction and concrete offline prerequisites

Run the installed CPython 3.14.3 interpreter from repository root, without `-O`:

```powershell
$d5aPython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $d5aPython -B research/resource-construction-mask-selection/analyze.py
& $d5aPython -B research/resource-construction-mask-selection/metadata.py
```

These commands created the exclusive retained outputs under
`.local-work/resource-construction-mask-selection/` and authored CSVs. They
refuse overwrite; repeat in a disposable copy with the same pinned local inputs
and fresh output files. Metadata recovery accepts existing byte-identical tables
after a partial failure, never differing bytes. The first metadata attempt used
an incorrect module path for `resource_spatial.py`; correcting it to the actual
owned `save-analysis/scripts/` path recovered the first two already flushed
tables by byte equality. No prediction changed.

The next engineering prerequisite is a pure joined-event reducer with producer
and consumer fixture streams. It must distinguish exact source bytes/frame/key,
selected Workshop bytes, owner, pointer lifetimes and transfer ancestry before
STOP. Test same-body wrong site, same SFBK different anchor, pointer reuse,
cache-only, nested/interleaved providers, stale query, no target consumption,
contradictory masks and rejected durable receipts. Integrate into a real
disposable Windows fixture only after the pure contract passes. This can resolve
engineering feasibility offline; actual natural construction and source epoch
still require separately authorized observation.

If stronger reachability ranking is required, export/read the existing provider
caller ranges `0x1407a1a3c` and `0x1407b526a`, follow their finite query loops
and descriptor transforms, and retain only neighbour examples that both select
the exact source and survive the native geographic/raster conversion. The current
final-raster sampler does not qualify that entire round-trip. No such reachable
query census is claimed here; it is a specific offline method to strengthen the
conditional selection without manufacturing a query from an extractor.
