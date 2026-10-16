# Native inorganic availability output contract

2026-10-16, Australia/Sydney. SOR-EXP-0034 / SOR-EV-0042 continuation,
using SOR-EV-0043's completed 0.7.0 capture. **CONDITIONALLY COMPLETE** for
the bounded native research endpoint; [assessment](completion-assessment.md)
and [review and checks](output-review.md) control acceptance.

The engine evaluates a naturally selected area into three cached resource-pointer
populations. The UI consumes their then-current contents and constructs the
displayed inorganic list. The storage, native callers and identity association
are mapped; a universal safe external read/copy or invocation API is unqualified.
This reference explains where identities are accessible in ordinary execution.

| Dimension | Scoped statement |
|---|---|
| Answer | Three operation-owned cached pointer arrays supply a UI-local union plus selected water append and typed rows. |
| Confidence | PROVEN for pinned instruction stores/locations and sampled captured identity values; proposed STRONG for bounded semantic/ownership interpretation. STATIC and OBSERVED below label evidence basis, not confidence. |
| Coverage | One pinned executable; static preview/Workshop/output/lifecycle paths; observed 0.7.0 Kreet preview and 346 UI folds. |
| Completeness | CONDITIONALLY COMPLETE reference endpoint; neither whole-engine writer coverage nor universal coherent copying/freshness is established. |
| Evidence | Existing function/source registers, exact windows and capture boundaries cited below; verification and review in output-review.md. |
| Limits / next step | General lifetime lease, established runtime equality, spatial equivalence and independent invocation remain unqualified; retain this stopping point for maintainer review. |

## Build, evidence and navigation

Applicable only to retail **Starfield 1.16.244.0**, SOR-ENV-0001, executable SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Preferred static image base is `0x140000000`; RVA = static VA minus that base.
All instruction windows below are **static VAs**; table entry points are **RVAs**.
Field offsets are hexadecimal and relative to the named object. Runtime VAs need
the actual loaded base. No addresses or layouts transfer to another build.

[functions.csv](functions.csv) is the single function inventory. N01–N07,
N11–N16 and N27–N34 map calculation and consumption; N67–N70 extend it with
operation-state construction, teardown and range reset. Names `FUN_…` are
analysis-generated; descriptive names are analyst aliases, OBSERVED-INTERNAL.
The register's `exe_sha256` field pins the build; this document supplies its
version. [sources.csv](sources.csv) pins every registered native export.

`uiNN` means `.local-work/recon/resource-availability-ui-NN.tsv`.
Those exact-hashed, local-only exports contain instructions and decompilation,
not public header declarations. [Dataflow](dataflow.md),
[region lifecycle](region-lifecycle.md) and
[spatial predicate ledger](../resource-availability-milestone-b/native-provenance.md)
retain upstream detail. This account synthesizes those project findings and
Bethesda executable evidence; source lineage is recorded in
[SOURCES](../../SOURCES.md#native-output-contracts--provenance-extension).
STATIC means instruction/decompilation-backed; OBSERVED means existing captured
execution; inference is labelled explicitly. Neither label grants integration.

## Computation and result representations

| Boundary / register key | Entry RVA | Result and decisive source |
|---|---|---|
| Loaded-area updater N01 | `0x021e07d0` | Mutates initialized state in RCX using indexed area RDX, radius XMM2, upper scalar XMM3; AL indicates refresh. ui15 `1421e07fd..0808`, `1421e0f04`; not a returned set object. |
| Spatial admission N07 | `0x021e0f50` | Resolves IRES (native type `0x9f`), accepts any qualifying region and inserts its pointer in a temporary pointer-keyed set. ui16 `1421e100a..1154` and full branch decompilation; ui15 `1421e0aa5..0bf4` enumerates the set into a vector. |
| Atmosphere N11/N12 | `0x0076bd20` / `0x0076b950` | Resolves effective ATMO and copies its resource list into second population. ui15 `1421e0c61..0d65`, ui16 complete helper bodies. |
| Biome N14 | `0x0078ee90` | Translated/scaled/floored XY selects BIOM; its RNAM RSGDs contribute resource pointers in descriptor order to third population. ui15 `1421e0e44..0eff`. |
| UI consumer N31 | `0x01578500` | Reads the three shared ranges, forms a local identity list, then builds typed rows. ui08 `1415785af..8643`, `1415787da..8803`; ui09 union body. |
| Other consumer N34 | `0x021f68f0` | Separate selected-harvester resource gate reads populations; does not produce whole-area availability or prove placement fit. ui10 `1421f6b3a..6b5c` and full function. |

The spatial population deduplicates exact IRES pointers across qualifying regions
and sources. It is materialized in temporary hash-slot traversal order, with no
supported alphabetical, FormID, rarity or durable order guarantee. Atmosphere is
a copied definition list; biome appends descriptor entries without a demonstrated
deduplication pass. These latter populations are lists even when their sampled
members happen to be distinct. Membership in the raw biome list does not mean
membership in the displayed inorganic list.

The UI's two calls to N32 (`0x021f8120`) at `1415785c9` and `1415785e8`
deduplicate exact pointer values in first-occurrence order: spatial first,
atmosphere second. Then `1415785ed..8641` compares third-list member FormID
against the selected water resource at static `145efb1f0` and appends matches
separately. This special append is not covered by the common deduplication.
Allocation failure paths preclude an unconditional complete-list guarantee.
The 0.7.0 session exercised no selected special-water append.

## Storage and identity domains

Let O be the operation context and S = O+`0x520`. Each population is a
24-byte vector header of 64-bit begin/end/capacity pointers; each member is an
8-byte resource pointer. End is exclusive; member count is `(end-begin)/8`.
This layout follows updater writes, reset stores and teardown allocation sizes,
and is corroborated by 0.7.0 population captures. It is not the UI's local fold
layout (u32 count+0, capacity+4, data+10 in ui09 N32).

| Population | Header relative to S | Header relative to O | Shared static VA begin/end/capacity |
|---|---|---|---|
| Spatial | `+0/+8/+10` | `+520/+528/+530` | `145f5d800 / 145f5d808 / 145f5d810` |
| Atmosphere | `+18/+20/+28` | `+538/+540/+548` | `145f5d818 / 145f5d820 / 145f5d828` |
| Raw biome | `+30/+38/+40` | `+550/+558/+560` | `145f5d830 / 145f5d838 / 145f5d840` |

The mapped shared context is static `145f5d2e0`; ui08 loads the absolute ranges
above. This association is documented in the
[original native ledger](../resource-availability/native.md#cache-lifecycle-and-persistence-classification).
S also holds cached indexed XYZ at +48, index +54, retained domain/reference +58,
and last ATMO/BIOM FormIDs +60/+64 (ui15). A raw pointer, runtime FormID,
plugin-qualified definition identity, localized name and saved identifier remain
distinct. Resource header +28 is FormID, +2e is native form type; row text is not
an identifier. Header-to-definition resolution in the 0.7.0 installed plugin
context supports Iron `Starfield.esm:0057c7`, Alkanes `0057c9`, Helium-3 `0057f5`.
These are not universal load-order-independent runtime IDs.

The final typed row vector is model+90/+98/+a0, stride `0x170`, with searched
byte model+e8. N33 and growth constructor `0x0157fde0` receive actual resource
operands at the UI caller. Growth can relocate earlier rows. A completed row
ordinal associates that operand with its row; retaining an earlier row address
does not. See [070 native boundaries](../continuous-beacon-preview/native.md).

## Refresh, ownership and bounded identity-copy contract

STATIC: N67 initializes operation storage; N68 passes O+520 to N69 teardown
(`ui17:1421ae2fb..e302`). N69 frees the three backing allocations, zeros their
headers and releases S+58 (`ui25:1421ae59d..e633`). It does not individually
retain/release each resource member in this body. Thus the vector owns its
pointer-array storage, not demonstrated ownership of each IRES definition.
Definition lifetime is a separate engine condition; no general lifetime lease
for a borrowed IRES pointer is established by these helpers.

STATIC: spatial refresh enumerates a temporary set into allocated pointer
storage, installs it via helper `1412ed2a0` at `1421e0bf4`, then cleans temporary
storage. That helper's full allocation-transfer semantics are not independently
reconstructed here. ATMO uses it at `1421e0d2f`; changed BIOM resets end then
appends, potentially growing storage (`1421e0e75..0ee3`). N70 and the separate transition/reset routine `0x021b6a10`
reset all three ends to begins (ui15 `1421b6b50..6b73`,
`1421d06f6..0719`). A header or array address is not an immutable snapshot.

Spatial refresh depends on domain and translated XY displacement, not simply
every call. Radius/upper are not separately compared by this local guard.
Missing or unchanged ATMO/BIOM resolution retains the previous corresponding
population; it does not certify empty resources. AL tracks refresh work, not
set inequality. Caller resets can also invalidate ranges. Exact all-context
freshness, full writer census and a global epoch remain unestablished.

| Observation point | What is available | Lifetime/synchronization qualification |
|---|---|---|
| After a natural updater return | All three currently stored populations, including retained values; descriptor and scalar operands at that invocation | OBSERVED by 070. Header/member walks are non-atomic; completed reads and overlap diagnostics qualify sampled records only. Not a universal coherent snapshot or fresh-area certificate. |
| Actual UI union/selected-append calls | RDX/R8 first/second ranges, each actual selected water operand; local fold after assembly | OBSERVED consumed operands and final row associations for 346 callbacks. Each borrowed range/element must remain readable for that use. No asynchronous borrowed-pointer retention follows. |
| UI return | Completed typed row census with constructor-associated resource identities | OBSERVED for 346 events. Full event population is available within captured coverage, not proof of all resident natural resources or an arbitrary earlier producer's output. |

For an **independently owned identity result**, already copied numeric FormIDs
and their recorded plugin/build context do not depend on the source array after
copying. That is a property of the copied value, not proof that every source read
is safe. A copied IRES pointer still depends on native definition lifetime.
The existing capture copied member pointers and `0x30`-byte resource headers
synchronously at the observed boundaries into owned evidence; it did not defer
dereferencing a borrowed population to a worker. Its `forms`, `populations` and
row-census methods are in `runtime/beacon-resource-070/capture.h` (pinned in
[verification](output-review.md)). No extractor implementation is supplied.

The exact general safe-copy contract remains bounded: live operation/definition
objects, a valid range, no conflicting replacement/reset/destruction during the
walk, successful reads/allocation and correct identity context are required.
No native lease spanning those reads, all-writer exclusion, arbitrary thread
permission or supported callback registration is proven. The updater's shared
ProcGen+40 lock protects mapped region traversal; it is not shown to guard the
three output vectors against every operation writer. The UI model lock at
`14157853e` likewise does not prove exclusion against all producer/reset paths.
Observed nested CALL execution establishes synchronous ancestry only there;
the queued command carries neither descriptor nor population snapshot.
Header rereads/zero reported overlaps cannot exclude in-place ABA.

This small identity result does not require retaining generated region-point
geometry. [Experiment A's geometry ownership NO-GO](../spatial-equivalence-feasibility/geometry-lifetime/report.md)
concerns a different complete-operand capture contract. It supplies neither a
barrier to understanding these output locations nor proof of output-copy safety.

## Observations, coverage and stopping boundary

[070 scientific report](../continuous-beacon-preview/live-scientific-report.md):
35,573 preview evaluations plus one initialization, 611,926 verified records;
346/346 consumed-input folds match independently associated final native rows.
Iron / Iron+Alkanes spatial changes plus atmospheric Helium-3 agree with the
operator's A/B/C displayed lists. Raw biome Iron+Lead is not displayed wholesale.
These counts describe one Kreet session and repeated sets, not 346 independent
geometries. Direct rendering times and unique evaluation→queue→UI ancestry are
unresolved. This task verifies static pins and regression receipts afresh; the
full capture census is inherited, not newly repeated.

STATIC adds the established descriptor path, source-map retrieval, refresh and
teardown rules. [Path assessment](output-paths.md) scopes established association.
Native spatial equivalence, general source readiness, remote contexts,
persistence authority, arbitrary invocation and retail integration safety remain
NOT TESTED/UNKNOWN as appropriate. 0.8.0 remains unadopted and NO-GO; synthetic
and x87 qualifications remain historical engineering results. No new live work
is needed to close this limited technical-reference endpoint.
