# C2C: Carinae's retained surface pattern explains the missing source

2026-10-23, Australia/Sydney. [Invoked brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_C2C_source_enumeration_carinae_reconciliation.md`).
Offline research only. Authored synthesis is REVIEW-REQUIRED; primary native,
save, definition and full generated-geometry artifacts remain LOCAL-ONLY.
B6 and publication remain on hold.

| Element | Supported result |
|---|---|
| Question | Why did the frozen Carinae source population omit a consumed source, and can that source reproduce the accepted geometry? |
| Answer | The copied source retains coarse SFPT `0x00212e16`; the frozen ordinary initialization selected `0x00212e19` at the same coarse cell. Applying the retained pattern to the unchanged halo independently discovers source `0:21396:15636:002493cf`, local anchor (-12, -12). Whole-source installed-input generation matches all three captured native regions exactly. |
| Confidence | PROVEN for copied field decoding, the finite pattern-selection discrepancy, enumeration arithmetic and exact geometry comparisons. The general rule uses retained native pattern witnesses where available. A fully offline reconstruction of the native pattern-selection state remains OPEN. |
| Coverage | One Carinae consumption-time pattern witness, five resolved sources under that pattern, 79 paths in the observed source and 978 in the five resolved sources. Feynman's six frozen sources and four accepted paths remain independent controls. Neither site has a complete native source or region census. |
| Evidence | [Native ledger](native.md), [versioned inventories](inventories.md), [selected results](results-v1.json), [controls](controls-v1.json), [source pins](sources.csv), [verification](verification.md), [review](review.md). |
| Limits | Forty-eight Carinae halo cells fail the existing anchor resolver under the retained pattern; native fallback and contributing-source behavior are not fully reconstructed there. Historical effective BIOM/RSGD/DNAM/order/mask and generation epoch are not directly observed. |
| Next step | Trace the surface-pattern registry and initialization state if a wholly offline selected-pattern predictor is required. This result does not require another live capture; no launch, attachment or collector extension was performed or authorized. |

## Scientific classification

**PARTIALLY DISCRIMINATED, with exact observed-source geometry correspondence.**
The omission is localized to a demonstrably different upstream selected surface
pattern, rather than a missing search-halo cell. A general witness-driven rule
discovers the source without using its observed local anchor. This is a bounded
enumeration correction for available pattern witnesses, not proof that the
unwitnessed native selection sequence can be reproduced from installed files.
The observed-source diagnostic independently establishes exact correspondence
for all three accepted regions using one coherent, unfitted source request.

The brief's stronger general enumeration result is therefore qualified: the
source inclusion rule is supported, but the pattern-selector's historical
operand transition remains unqualified. Do not describe the candidate envelope
as the native selected map or treat source-key/pointer equality as epoch proof.
No universal enumeration proof is needed for the finite positive result.

## The omitted-source mechanism

The retained source constructor fields provide more information than its local
anchor alone. All three C2B accepted stops retain identical 0x70-byte source
prefixes. Source `+0x44` contains SFPT `0x00212e16`, `+0x48` contains flags 8,
`+0x4c/+0x50` contain subindices (7, 7), and `+0x54` contains SFBK
`0x002493cf`. These are constructor-retained selectors, not newly observed
producer execution. [Exact constructor mapping and caveats](native.md) distinguish
their identity domains.

The frozen requests all used SFPT `0x00212e19`. Their halo was geographic fine
cells [21392, 21407] by [15632, 15648], inclusive. The independently derived
observed anchor (21396, 15636) lies inside it. With the frozen pattern,
`source_at` follows a backlink to (21384, 15636), SFBK `0x0006ce55`; with the
retained pattern it resolves (21396, 15636), SFBK `0x002493cf`. Changing the
query radius or adding more samples at that same cell cannot repair a different
selected SFPT. The descriptor (21408, 15648), owner 386266, padding and spatial
transform need no adjustment to reproduce the accepted geometries.

The implemented rule replaces coarse-pattern inputs only when an independent
constructor-retained witness identifies that coarse cell and pattern. It then
traverses every original halo cell, resolves anchor/backlink semantics with the
existing helper and deduplicates source identities. The routine accepts no local
source anchor, target geometry, resource label or expected count. All five
resolved sources are retained, including sources outside the query center.
Unresolved cells are recorded, not treated as empty or dropped from coverage.

Separately, an installed style-compatible pattern envelope yields 23 Carinae
source candidates and 33 Feynman pattern/source combinations representing 26
source IDs. This envelope is computed before reading the observed anchor or
pattern. It discovers the Carinae source as a candidate, but it does not choose
which compatible SFPT the game selected. Feynman's after inventory retains its
six conditional frozen sources because there is no equivalent native pattern
witness for them in the cited controls. Four exact regions cannot certify that
inventory's completeness.

Here the pattern and BIOM definition envelope covers the pinned installed main
`Starfield.esm` and its derived maps. It is not an audit of SFPT overrides or
additional style candidates in every installed plugin.

## Whole-source result and independent constraints

The installed map assigns BIOM `0x001160d9`. The existing installed selection
resolves family root Iron `0x000057c7`, RSGD `0x0018ce04`, and selected DNAM
SHA-256 `fd99c23e35f6b3c0b2abefbfb224920c0cea7787dae4a4e8c71dee6b29e83111`.
The complete order is Rothicite, Alkanes, Iron with mask 4 and active weights 1.
The five resolved footprints plus conservative four-cell margins have uniform
mask 4. Source-family, mask and DNAM remain installed derivations rather than
historical native operand captures. The complete frozen Carinae requests agree
on resource order, blocks and owner; no resource receives separate tuning.

For nominal dimensions (10, 10), padding (2, 2), raw dimensions (14, 14), local
anchor (-12, -12) and descriptor (21408, 15648), the unchanged native transform
gives generator origin (-1400, -1400), clip center (-900, -900), clip half
(700, 700), and half-open X/Y cell ranges [1, 13). Every packed cell key is
rebuilt from that complete frame. The unchanged generator executes complete
resource/cell traversal and competition, producing 8 Rothicite, 49 Alkanes and
22 Iron paths. No path omission, translation, seed search or tolerance is used.

| Captured resource | C2A capture | Exact ordered XYZ/width and native-bound matches | Generated cell |
|---|---|---|---|
| Iron `Starfield.esm:0x000057c7` | 1280 | 1 | (4, 5) |
| Alkanes `Starfield.esm:0x000057c9` | 1301 | 1 | (5, 6) |
| Rothicite `Starfield.esm:0x00005df1` | 1270 | 1 | (6, 7) |

The fixed captured query is XYZ (-813.3619384765625, -729.5208740234375,
68.7126693725586), radius 150 and upper height 168.71267700195312, all in the
captured consumer frame. Evaluating every generated path yields four Iron, two
Alkanes and one Rothicite positive paths. All seven come from the observed
source even when all five resolved sources are generated. Acceptance
short-circuits native traversal; a single exact accepted path per resource
therefore cannot establish how many additional native regions would pass.

The maintainer's independent visible connected-deposit counts are Iron 2,
Alkanes 2 and Rothicite 1; one Alkanes deposit has an extractor. Four generated
Iron paths are not four visible components. No connected-component geometry or
path-to-extractor join is established by this task, and none of those counts
was used to choose parameters. Saved hardware identity and effective generation
history remain separate questions.

## Controls, limits and disposition

Fresh C1H replay regenerates all 895 frozen Carinae and 156 frozen Feynman paths
before installed resolution. Feynman's installed population retains 156 paths,
four exact accepted matches and three exact C1G chance comparisons. The two
Fluorine-to-Ionic-Liquids replacements remain unchanged. Carinae's old 895 paths
and their negative comparisons remain historical; the 79-path diagnostic and
978-path resolved subset are separate outputs, not replacements of that freeze.

Concrete mechanisms eliminated for the three captured matches include a
necessary descriptor translation, owner change, width/seed fitting, per-resource
retuning and a simple failure to sample the observed geographic anchor. The
remaining selected-pattern dependency is precise: native initialization reads
the effective surface map, ordered style-compatible SFPT candidates and surface
seed/PRNG stream, whereas the frozen reconstruction used installed map bytes,
definition-file candidate order and the default surface seed. Existing receipts
retain the resulting source pattern but not that historical selector invocation.
They cannot distinguish which of those inputs differed. Registry order is a
candidate explanation, not an established cause. Nor does this task establish
whether the observed source was created in the captured session.

Further native acquisition is not required to support these scoped results.
If future work needs a fully predictive selector, first inspect its registration
and map-input path offline. Only a demonstrated residual acquisition gap should
produce a separately qualified collector extension and approval-ready live card.
This delivery proposes no live experiment and consumes no live authority.

Scientific outcome: positive finite pattern/source discrimination and exact
geometry correspondence, with incomplete selection/census coverage. Engineering:
owned offline analytical additions, unchanged shared generator and controls.
Target survival, restoration and cleanup: not applicable; no target operated.
Authority: protected inputs preserved and no staging, commit, push, publication,
third-party incorporation or external disclosure. Independent disposition and
exact delivery identity are recorded separately in [review.md](review.md).
