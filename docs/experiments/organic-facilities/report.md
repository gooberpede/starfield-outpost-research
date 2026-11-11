# E2 organic production facility native reference

2026-10-16, Australia/Sydney. SOR-EXP-0039 / SOR-EV-0047.
[Authorized brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_E2_organic_facility_native_mapping.md`),
[frozen contract](contract.md), [review package](review.md).

| Element | Answer |
|---|---|
| Research question | How are greenhouse/husbandry facilities identified, given product choices, configured, supplied and scheduled? |
| Best-supported answer | **CONDITIONALLY COMPLETE** native reference, independently accepted with maintainer review pending: six facility definitions connect to planet-scoped domesticable species/resource choices, recipe-keyed UI with knowledge gating, resource-AV configuration, shared persisted producer rows, transitive incoming input checks/consumption and shared scheduling. Product changes can reset registration and prune incompatible links within the documented bounds. |
| Confidence | PROVEN scoped definition/byte equality and saved replay; proposed STRONG / STATIC native interpretation; screenshot and Savannah/desert observation remain user-reported gameplay evidence. No new RUNTIME acquisition. |
| Coverage | Pinned retail 1.16.244.0 and installed main ESM; six producer CONTs/six PKIN constructions, 90 property-linked resource recipes, 3,851 CSV recipe-pattern checks, six saved greenhouse producers and their local Water paths. |
| Evidence | [Definitions/catalogues](definitions.md), [native selection/input/state map](native.md), [local links](links.md), [E1 reuse and modifier matrix](reuse.md), [pins](sources.csv), local receipts identified in review.md. |
| Limitations | Actual loaded knowledge/AV/actor/input state and realized output are unobserved. Actual eligible scan operands, universal cache completeness/freshness, mod overrides and general safe invocation remain unqualified. Saved husbandry instances are not demonstrated by the inspected subset. |
| Next step | Maintainer review of the bounded map. A new live experiment is not automatically warranted by the remaining current-state limits; use the scientific-value assessment below. |

Greenhouse and husbandry menus share the recipe/UI interface but obtain resources
through different species paths. Flora maps species-associated MISC components
to a canonical resource. Fauna uses resource actor values from the species/template
context and retains its fauna-specific IRES/recipe. Both use planetary species
records and domesticability; the inspected consumer does not filter the list by
the greenhouse's current local biome or currently spawned creatures. That gives
a concrete native explanation compatible with the Savannah-to-Sandy-Desert lead,
without generalizing it into every cache state or every planet/mod configuration.

The input rules are definition-backed within the full 90-row facility-property
set: Water ×1 for flora; Water ×1 plus Fiber ×2 or Nutrient ×2 for fauna. A diet
label is not the native selection key. The selected IRES/AV and COBJ preserve
the deciding resource/recipe lineage. Multiple species can contribute the same
IRES, deduplicated with knowledge flags combined; the UI communicates recipe
FormIDs, and apply resolves them back to resource AV and producer.

Visible does not mean selectable: the installed SWF enables selection only when
the row is known and not already built, displays a scanning requirement when
unknown and can require confirmation for link changes. Input availability governs
production independently of menu knowledge. Native input checking uses locally
reachable sources, caps requested cycles and records consumption before ordinary
output insertion. A reachable producer path is not sufficient stock or throughput.

The supplied screenshot shows Analgesic selected in the build list, Solvent
marked CURRENTLY BUILT, and Water in the requirement panel. Codos location comes
from the user's context, not an independently visible planet identifier. The
right panel's clipped count is not evidence of a recipe quantity. This task
does not use the screenshot to certify list completeness, exact scan progression
or measured output. The separate definition and native checks supply those
scoped contracts.

## Completion assessment and discriminating observations

The endpoint is a documented native reference, not a live facility dump. Native
function/state boundaries answer how another researcher can identify the facility,
its candidate/current product, recipe requirements, directed local edges, current
reason and production machinery. Remaining unqualified **values** are disclosed
instead of being treated as missing architecture. Independent review tested
that distinction against every original criterion and accepted the corrected
bounded reference; disposition and preserved rework are in review.md.

| Remaining question | Smallest natural discriminating observation | Scientific value |
|---|---|---|
| Does a particular row become selectable at a particular scan/skill transition? | Same planet/species key at the documented knowledge lookup and UI row before/after the relevant ordinary discovery action; compare stored category membership, bPlayerKnowledge and actual button | REVISE: same-species eligible keyword list, actual scan counts and source controls would need a separate bounded design; no observer implementation or live recommendation here |
| Are current producer and input states sufficient for a chosen due cycle? | One linked reason/input-cap/consumption/insertion sequence with exact producer/resource, requested/capped count and before/after destination delta | REVISE if a later consequential realization question requires it; current native architecture is already mapped |
| Do all current planet candidates agree with a reconstructed table? | Bound planet-cache lifecycle and all selected species/resource operands at the mapped selector; compare an independently generated set | REVISE: cache population/completeness is a distinct coverage qualification; CSV agreement alone cannot answer it |
| Should E2 repeat menu/scheduler behavior live simply to establish reachability? | Existing static contract plus user screenshot already supports a useful endpoint | NO-GO for a redundant broad live repeat without a more consequential discrimination |

These observations confer no execution authority. No additional offline table,
inventory count or full storage/cargo simulation is demanded to use the mapped
contracts. Conversely, no tool, safe callable API, production guarantee, complete
player census or live restoration validation is claimed. Authored interpretation
remains REVIEW-REQUIRED; raw evidence remains LOCAL-ONLY. No staging, commit,
push, publication, game launch, instrumentation or save/configuration change.
