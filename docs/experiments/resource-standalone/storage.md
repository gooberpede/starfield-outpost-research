# Measured corpus alternatives and removal ledger

2026-10-24, Australia/Sydney. [Primary selected measurements](measurements-v1.json),
[schema](corpus.md), [validation and preserved failures](validation.md).
These are measured bounded representations, not a proof of a globally smallest
corpus. The recommended normalized payload supports the three supplied tiles,
not every source or location on either planet.

## Representation costs

| Variant | Serialized bytes | zlib level-9 bytes | Principal organization |
|---|---:|---:|---|
| Normalized | 16,792 | 3,125 | Three shared SFPT arrays, 106 SFBK dimensions, four shared generation blocks and body/tile/biome references. |
| Expanded | 25,942 | 4,252 | Per-tile 256-entry resolved anchor/block/dimension arrays replace SFPT/SFBK tables; generation remains on demand. |

Sizes include envelope, digest and final newline. Compression is a measured
alternative encoding; delivered inference reads JSON, not compressed input.
No expected native paths, generated regions, prepacked seed-key grid or prior
request result is present in either corpus. Deduplication collapses eight
selected resource occurrences across three biome projections to four distinct
eight-float blocks. The two unused floats per original block are omitted.
Pattern tables are shared by reference; expanded routes repeat anchor/dimensions
across covered subslots. Both variants generate identical ordered geometry and
availability in the two held-out requests.

The same final builder ran twice: 9.064 and 9.230 seconds, including installed
hash checks, ESM/BA2 reads, EXE constants, planetary selection, validation and
both variants plus code export. Corpus and flat-code bytes are identical across
those runs. Build elapsed time is not embedded in the deterministic payload;
local manifests retain the measured times separately.

| Accounting projection | Normalized bytes | Expanded bytes |
|---|---:|---:|
| Shared fixed tables and envelope, no body rows | 15,951 | 1,230 |
| Feynman body, two supplied tiles | 16,473 | 17,663 |
| Carinae body, one supplied tile | 16,269 | 9,508 |
| Both bodies, three tiles | 16,792 | 25,942 |

These projections retain all shared tables to isolate marginal body cost. The
empty-body projection is accounting only and is invalid for inference. The
single-body projections intentionally retain shared entries unused by that body;
they are not separately minimized single-planet corpora. A one-outpost request
within Feynman's supplied context uses the same body corpus as a batch of local
Feynman requests. Additional queries within existing coverage add zero corpus
bytes; their output geometry is generated, not cached in the corpus.

Under the explicit assumption of reusing exactly these fixed shared tables and
similarly sized body metadata, another Feynman-sized body row would add about
523 normalized bytes or 16,434 expanded bytes. This is a structural estimate,
not a measured third body. New planets can require new patterns, source blocks,
components, masks or branches, so actual growth is coverage-dependent. No
whole-planet storage or performance extrapolation is certified from three tiles.

## Execution measurements

Times below are seconds, medians of two complete in-process predictions/batches,
including corpus validation and geometric area/callback derivation. Every
request generates its whole resolved sources afresh. The one-planet case is
three nearby Feynman footprints, not a whole-planet sweep. The multiple-planets
case is one Feynman and one Carinae footprint.

| Supported case | Requests | Normalized | Expanded | Generated paths per request |
|---|---:|---:|---:|---|
| One outpost | 1 | 0.563 | 0.558 | 103 |
| One planet, bounded local batch | 3 | 1.687 | 1.693 | 103, 103, 103 |
| Multiple planets, bounded batch | 2 | 37.469 | 36.796 | 103, 1326 |

Warm JSON load plus referential validation, 20 repeats, has median about
0.00085–0.00086 seconds normalized and 0.00145–0.00149 seconds expanded.
Separate fresh-interpreter load/validate processes took 0.290 and 0.143 seconds
respectively. These include interpreter/audit initialization; operating-system
file caches and scheduling were uncontrolled, so the fresh-process difference
is not evidence that expanded data intrinsically starts faster. Exact samples
and commands remain local. The small lookup difference does not dominate the
Carinae whole-source competition and rational geometry cost.

Recommend normalized for this bounded capability: it is smaller both serialized
and compressed, retains the upstream lookup model, and has no observed scientific
loss or material prediction-time penalty. Expanded remains a verified alternative
when consumers prefer direct routes. Neither timing sample establishes a general
performance guarantee. No arbitrary corpus-size acceptance threshold was used.

## Removal and redundancy ledger

| Group / experiment | Actual result | What it establishes and does not establish |
|---|---|---|
| Remove constants | UNKNOWN, missing group | Required by declared schema; exact arithmetic needs polynomial operands. Not individual coefficient minimality. |
| Remove six settings | UNKNOWN, missing group | Complete ordinary-setting vector is a schema obligation; individual active branches can avoid some settings. |
| Remove patterns | UNKNOWN in normalized form | Normalized lookup needs its referenced entries; expanded routes legitimately replace the group. |
| Remove source dimensions | UNKNOWN in normalized form | Frame construction cannot proceed; expanded nominal dimensions replace this table. |
| Remove generation blocks | UNKNOWN, missing group | No invented chance/walk defaults. |
| Remove body rows | UNKNOWN, missing group | Body/key/tile/component dependencies remain explicit. |
| Perturb inactive Exotic setting | Changed deterministic output | The installed override is geometrically consequential in the tested Feynman request. |
| Increase a used source dimension by 12 | Changed deterministic output | Source extent/traversal is consequential; original ineffective same-value attempts remain failures. |
| Reverse resource order | Changed ordered geometry output | Order is part of the required representation and prior-resource competition. This comparison alone does not separate reordering from population changes. |
| Change system key | Changed deterministic output | Body/system packing participates in generation seed; owner alone is insufficient. |
| Omit original block tail at +0x20/+0x24 | Synthetic nonempty generation is identical with tails zero versus 123/456; all seven native controls still exact | Qualified generator reads only first eight floats. This does not prove tail irrelevance to unrelated native consumers. |
| Omit zero-chance Everywhere geometric pass | Builder verifies own rarity-6 chance zero; seven controls and variant equality pass | Strict threshold rejects every cell independently. Water admission remains a separate UNKNOWN. |
| Replace full SFTR/BIOM/global definition tables with three tile projections | Same held-out exact controls and supported query behavior | Derivation is sufficient within supplied tile coverage, not globally. |
| Drop source anchors, packed-key maps and generated regions from payload | All are rebuilt from requests, routes/dimensions and body identity | No witness anchor or native answer lookup at inference. |
| Drop SFPT registry, style selection and surface seed | Linked SFTR supplies selected entries | Defensible route-specific redundancy, not a generated-tree result. |
| Project planetary RSCS/RSGD/IRES hierarchy into selected components | Builder recomputes first; predictor uses resulting order/blocks | Computational preparation boundary, not proof those original dependencies are irrelevant upstream. |

Removal failures are validation failures, not proofs that no alternative schema
could derive the group. Perturbations establish consequential outputs for the
chosen tests; symbolic dataflow and cross-representation substitution support
the larger dependency inventory. No individual-byte brute-force minimum claim
is made. Tighter selected-width bounds, compact integer/binary encodings,
dead-table pruning per coverage and removing descriptive identities are possible
future reductions; none is silently described as already measured or validated.
