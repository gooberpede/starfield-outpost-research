# D4E algorithm and local corpus revision

2026-10-25, Australia/Sydney. Versioned extension of the
[D1 algorithm](../resource-standalone/algorithm.md),
[D3 selection](../resource-save52-d3/operands.md) and
[D4C SFPT installation correction](../resource-owner-root/source-layout.md).
Earlier specifications and frozen outputs remain historical. [Native rules](native.md).

## Preparation

Run the pinned installed-main planetary selection before thinning dependencies.
Preserve its PNDT order, shuffle/selection draws, family cache, capacity guards,
guarded fallback, Special and descriptor qualifications. For each selected BIOM,
derive root and descendant slots 0–3 from its assigned family, Special in slot 4,
and first BIOM-local rarity-6 resource in slot 5. A PNDT effective-RSGD Everywhere
list must not substitute for that last scan. Preserve zeros and repeated
identities. The native producer's raw inputs are record references, rarity bytes,
selection inputs and descriptor data; runtime slots are initialized derivatives.

Sort components by the unsigned BIOM-derived creation key on the supported route.
Start with empty map and staging array. Visit every component, including zero
roots. Append each nonzero slot in offset order without deduplication. For a
nonzero root, exchange the entire staging array with that root's map array;
the displaced old array becomes the next staging array. Discard final staging
at cleanup. The existing general evaluator also models refused appends explicitly;
the predictive successful-storage case does not simulate heap allocation.

For a selected root, insert its resolved IRES first, then the root-map array in
order. Preserve duplicate occurrences and sort descending by rarity. Lists of
up to 32 resolved pointers use the native stable insertion path: only strictly
greater rarity shifts an earlier entry. Equal-rarity identities retain encounter
order, including duplicate occurrences. Larger lists with different identities
tied in rarity remain unsupported.
Use the root-selected DNAM rarity block for every ordinary candidate. Keep the
later Special pass separate. Rarity-6 ordinary candidates take zero weight on
the native inactive branch; they are still real candidate occurrences and must
not be removed because they generate no finite points.

The component projection needs explicit admission qualification: selected Special
alone does not prove a slot-4 write. `qualification.py` requires shared occupancy
below eight, accepted Special occurrence and a selected effective-RSGD descriptor.
It also requires equality between the native first-per-BIOM Everywhere identity
set and the owned model's prepass set. A mismatch rejects corpus construction
instead of implying general equivalence. All 16 represented bodies and three
Special assignments pass these checks. The original component freeze is preserved;
these checks qualify its projection without changing its values.

## Portable representation and boundaries

The new schema is `sor-d4e-corpus/1`, using the existing SHA-256 envelope and
request shape. `predictor_d4e.py` adapts the owned D3 inference module: admit
rarity 6, preserve its occurrences and supply its inactive zero weight. All
geometry, source enumeration, SFPT transpose, seed arithmetic and spatial
predicates retain their existing implementations. The inherited generated-region
provenance string still names the D3 geometry layer; the schema and preparation
receipt identify the new D4E selection version.

Inference receives derived ordered `resources` rows and referenced generation
blocks. New resource occurrences use the existing `id`, `rarity`, `block` fields;
no captured slot word, runtime pointer, answer list or native geometry is retained.
The local preparation ledger retains all component/map provenance separately.
Raw component slots and the full planetary selection dependencies need not be
added to the portable inference payload because preparation has already consumed
them. There is no new inference field. The new schema tag is one byte longer.

The build starts from the source-corrected D4C dependency corpus and recomputes
all requested bodies' component/map candidates from the independent D4E freeze.
The D3 descriptor resolver is reused conservatively. One represented BIOM
projection retains unsupported descriptor qualifications; no ambiguity is resolved
by matching geometry. The underlying owned selection adapter still assumes
empty atmospheric occupancy and its existing effective-RSGD/shared-state model.
D4E does not claim those assumptions cover every native initialization context.
The new BIOM-local slot scan is source-backed; broad root assignments remain
conditional and tested only where native controls exist.

| Canonical local payload | Prior corrected D4C | D4E | Increment |
|---|---:|---:|---:|
| Save52 normalized payload | 220292 bytes | 221130 bytes | 838 bytes |
| Feynman/Carinae control payload | 16724 bytes | 16834 bytes | 110 bytes |

The canonical payload comparison holds JSON formatting fixed and excludes the
envelope. The Save52 D4E normalized file is 221219 bytes; expanded is 1620493
bytes. Preparation receipts account for changed candidate rows, block references,
new rarity blocks and unused-block removal. Save52's field deltas are 784 bytes
for body candidate data, 53 for blocks and one for the schema; controls are
56, 53 and one respectively. These are measured local costs,
not a new compression/performance study or a publication corpus. Earlier pretty
JSON sizes must not be compared as if the formatting savings were algorithmic.

At runtime inference is isolated with the existing owned Python audit boundary:
only supplied corpus, request, flat code and interpreter standard library are
allowed; eight deliberate forbidden-read probes must fail. This is not an OS
sandbox. Validation persists predictions and hashes before native comparison.
Save52 associations remain a separate post-prediction diagnostic table beside
their frozen D3 classifications; saved equipment never becomes an absence census.
