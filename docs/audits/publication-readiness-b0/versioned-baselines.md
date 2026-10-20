# B0 versioned research baselines and incremental requalification

2026-10-21. Prospective policy/schema only: no new-build investigation, executable
scan/import, native relocation, populated crosswalk or regression execution.
Research-release identity and game-build identity are independent. Older tagged
snapshots, source addresses, bit/record offsets, failed hypotheses and source pins
remain historically intact.

## Reuse existing provenance

[PROVENANCE](../../PROVENANCE.md) and experiment source CSVs already bind source
identity. [Function register](../../function-register.md) links stable SOR-FN
records and subsystem-local keys; reuse these rather than assigning new IDs to
every incidental function. For example the
[native availability register](../../experiments/native-availability-map/functions.csv)
has local N keys linked through the central register, while
[build-budget functions](../../experiments/build-budget/functions.csv) explicitly
carry static VA/RVA/domain/source hashes. These are existing locator records,
not a universal cross-version identity map. [LO1 sources](../../experiments/locations-outpost/sources.csv)
pin EXE, ESM and relevant BA2/other inputs separately.

Those existing records report predominantly retail `1.16.244.0`, EXE SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
and ESM SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
B0 checked the written pins for consistency, not installed bytes or a new build.
The primary accepted release manifest remains deferred and requires B3/B6
verification against governing pin evidence. A save header version is not proof
of its originating executable hash. Never assign all historical experiments to
the headline build; unknown provenance stays UNKNOWN.

## Prospective minimal records

| Record | Minimum fields and validation |
|---|---|
| Research release | Independent release ID/tag (TBD), candidate commit/tree and public refs/history boundary, date, scope approval, baseline references, source/evidence index, reviewer and maintainer action decisions. Do not use game version as the research-release ID implicitly. |
| Game/input baseline | Baseline ID, exact EXE filename/product version/build/SHA-256/bytes, source pin/receipt and acquisition date; preferred image base; material ESM/load-order, BA2/member/interface, Papyrus/script, configuration/tool pins and their applicability. Hashes identify proprietary inputs without publishing them. Missing pins are explicit. |
| Per-finding applicability | Existing finding/experiment key and claim/report/review; tested/inferred/unknown coverage; each applicable baseline/sample; exact source/evidence refs; old-build exceptions, confidence, publication class and completeness independently; update status and limits. |
| Significant semantic identity | Existing SOR-FN/SOR-ST or scoped register key first, stable role/contract and owning subsystem, aliases and origin. Add a durable identity only for a significant function/structure/definition/interface needing maintenance, not every address. |
| Version-specific locator | Semantic identity, baseline/hash, existing register row, module/domain and preferred base if static VA; RVA or explicitly domain-labelled object/record/stream offset; FormID plus plugin/load-order namespace where relevant; source pin/range/hash and semantic coverage/evidence. Runtime VA needs session/module base; never conflate saved IDs, handles, pointers and FormIDs. |
| Update qualification | Old/new baseline IDs, changed-input inventory, affected findings and dependencies, locator relationships/evidence, proportional checks/results/failures, four per-finding outcomes, reviewer snapshot/decision and release recommendation. |

For functions that split/merge, a relation may be one-to-many or many-to-one with
role partitions and evidence; removed functions have no fabricated successor.
Track changed ownership/data paths and structure fields independently. A stable
address may change behavior; a moved address may preserve it. Signature or locator
match alone is neither semantic equivalence nor behavioral revalidation.

Illustrative row only, deliberately invented placeholders, **not authoritative**:

| Semantic identity | Old baseline locator | Proposed later relationship | Evidence/status |
|---|---|---|---|
| EXAMPLE-only recipe eligibility role | EXAMPLE-A; static VA UNKNOWN, RVA UNKNOWN, image base UNKNOWN | EXAMPLE-B splits into two role partitions; both locators UNKNOWN | No recovered function or new address; UNRESOLVED until source pins and role/consumer comparison establish both partitions. |

No real SOR ID or new-build address is allocated by this example. Historical
registers remain authoritative for their own pinned versions; a future small
crosswalk references their rows rather than duplicating or overwriting them.

## Proportionate future workflow and release threshold

Under a later approved update brief, inventory/hash changed EXE, definitions,
scripts, compiled UI and relevant configuration first. Compare exposed interfaces
and dependency changes. Relocate only significant locators needed for selected
findings, then inspect native call/data paths and targeted original regression
witnesses where those changes matter. Split/merge/removal is a legitimate result.
Unchanged definition bytes do not prove every runtime consumer unchanged. Live
checks still require their own experiment authority; version maintenance grants
none. Preserve failures and exact source revisions.

| Per-finding outcome | Required interpretation |
|---|---|
| REVALIDATED | Specified checks support the stated behavior on the named new baseline within explicit coverage; evidence and independent review linked. |
| CHANGED | Evidence demonstrates a material contract/representation/behavior difference; state effect, new scope and old/new witnesses. |
| CARRIED FORWARD — NOT REVALIDATED | Retained historical knowledge or reasoned expectation, explicitly untested on the new build; no compatibility guarantee. |
| UNRESOLVED | Missing/conflicting evidence or locator/behavior uncertainty; identify exact gap and impact. |

These statuses are independent of scientific confidence and rights eligibility.
Reviewer checks primary comparisons, source identities, claimed behavior versus
locator-only evidence, coverage, negative results and the exact candidate snapshot.
A game update prompts assessment, not an automatic release. Publish a subsequent
tagged research snapshot only after an independently reviewed update-qualification
record and maintainer approval of its explicit validated/changed/carried-forward
coverage and unresolved limits. Required claims must be supported or their scope
revised explicitly. No arbitrary percentage of revalidated functions determines
release readiness. Preserve prior releases; this archive promises scoped research,
not version-independent software compatibility.
