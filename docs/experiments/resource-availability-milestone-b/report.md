# Inorganic availability milestone B — executable native predicates

2026-10-15, Australia/Sydney. SOR-EXP-0034 / SOR-EV-0042 continuation;
uses independently captured SOR-EXP-0035 / SOR-EV-0043. Authored interpretation
REVIEW-REQUIRED; raw/native/save evidence LOCAL-ONLY.
[Original authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_inorganic_resource_availability_milestone_B.md).

| Element | Scoped result |
|---|---|
| Question | How does the Available Resources panel decide ordinary inorganic presence at an unplaced prospective beacon? |
| Answer | Generated resource regions undergo an XY broadphase, count-specific acceptance and consecutive tapered-strip predicates. Accepted IRES pointers feed a deduplicated spatial population. Atmosphere contributes a second population; the biome population contributes only entries matching the selected water identity. Native UI folds the first two by pointer, then appends selected biome entries. |
| Confidence | STATIC reconstruction and synthetic qualification of the spatial algorithm; CROSS-VALIDATED final fold over all 346 recorded UI updates. No independent spatial-input/native-output equivalence is claimed. |
| Coverage | Retail 1.16.244.0, pinned executable; full 611,926-record 0.7.0 capture, 35,574 evaluations, 11,128 distinct indexed argument tuples. Native region point/count/width and enumeration operands are not recorded by 0.7.0. |
| Completeness | Outcome B, completed evidence-bounded reconstruction independently ACCEPTED; maintainer critical review remains pending. Outcome A remains NOT TESTED: argument positions and final populations alone cannot validate reconstructed region membership. Arbitrary site generation is not supplied. |
| Evidence | [Specification](specification.md), [native/provenance ledger](native-provenance.md), [validation](validation.md), [review/package](review.md). |
| Next step | [Decision/acquisition assessment](acquisition.md): a linked callback-input/result acquisition is required for independent spatial validation unless an equivalent archived operand source is recovered. No live action is authorized. |

The result is useful to engine researchers independently of any save importer:
the executable now evaluates supplied region geometry rather than merely merging
the game's finalized spatial set. Its `UNKNOWN` state preserves incomplete
enumeration, missing points, frame qualification and numeric-domain limits.
See the versioned [contract](specification.md) and synthetic input/output there.

The capture's 35,574 evaluations contain **11,128** distinct 24-byte indexed
position descriptors; including radius/height bits gives the same count. Only
56 descriptors repeat, with the most frequent occurring 13,836 times; 11,072
occur once. These are evaluation arguments, **not 11,128 reconstructed native
region geometries or independent games**. All use frame index 0 and one indexed
domain; radius is 150.0 and the separate height operand is 13.94818115234375.
The runtime pointer is session-local and is retained only in private receipts.

All 346 captured UI callbacks agree with the existing evaluator in both row order
and identity set using independently observed common-consumer operands, selected
biome inputs, constructor identities and final ordinal census. There are 339
three-row and seven two-row updates. This validates the final fold, not a spatial
prediction: no candidate region identity or full point sequence was acquired by
the ten hooks. An installed definition, region's IRES, or final population cannot
substitute for those operands. The native-ledger investigation follows their
actual generation and index dependencies instead of calling them generically
unknown terrain.

Fresh save replay reproduces all 29 prior audit objects and decoded hashes,
including all 63 mature extractor/resource/owner joins among 848 supported roots.
Construction/removal controls retain empty producer registries at beacon-only
and extractor-removed stages. That registry supplies positive historical producer
evidence; it cannot establish absent availability or rebuild the region cache.
This does not prove whole-save absence of every upstream generation parameter.

The original 0.7.0 observations, prior partial evaluator, frozen position
predictions and historical findings remain preserved. No game execution,
instrumentation change, deployment, save write, shared session-tool change,
staging, commit, push or external disclosure belongs to this assignment.
