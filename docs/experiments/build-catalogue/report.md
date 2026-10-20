# BM2: Build Mode catalogue, selection and nominal production

2026-10-20, Australia/Sydney. SOR-EXP-0061 / SOR-EV-0069.
[Authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_BM2_build_catalogue_selection_production_aggregation.md),
[frozen plan](plan.md), [review](review.md).
Authored interpretation REVIEW-REQUIRED; game-derived primary payloads LOCAL-ONLY.

| Element | Answer |
|---|---|
| Question | How do installed construction definitions become grouped, visible, selected and admitted, and how are different producer rates combined? |
| Best-supported answer | Ordinary discovery scans loaded construction recipes and admits recipes whose **first FNAM menu keyword** belongs to the configured category list. Recipes can target individual forms or recursive form lists/recipes; a recipe flag preserves a list as one grid entry with selectable variants. Conditions can omit choices or retain specific unmet perk/research requirements as visible locks. Selection produces a preview and item card; construction still requires the separate admission status. Production adds each included producer's independently normalized nominal rate in binary32. |
| Confidence | Proposed STRONG / STATIC for the bounded installed routes; physical bytes, method spans and numerical reproduction are mechanically checked. Independent disposition is recorded in review.md; no live measurement is claimed. |
| Coverage | Fresh retail 1.16.244.0 EXE/main ESM and four installed interface assets; 3,009 physical COBJ records, 15 configured outpost category positions and 204 physically discovery-qualified root recipes before contextual gates. FNAM/CNAM traversal reaches 545 COBJ records. SD2's add-on supplies the multi-perk extension control. Prior saved evidence is reused selectively, without a new save census or a winning-load-order merger. |
| Evidence | [Catalogue](catalogue.md), [eligibility](eligibility.md), [UI](ui.md), [production](production.md), [extension/persistence boundaries](extensibility.md); exact [definitions](definitions.csv), [categories](categories.csv), [functions](functions.csv) and [sources](sources.csv). |
| Limits | Physical qualification is not an actual menu snapshot. Current player progression, effective overrides, runtime cache epochs, practical 1,000/2,000-entry performance, rendering and delivered production remain unmeasured. No numerical supported-capacity ceiling is inferred from the census or counter width. |
| Next step | Critical review of the original AC1–AC8 and exact patch package. Optional live refresh/performance/realization questions require a separate decision; none is needed to use the bounded static architecture. |

## Practical answers

Furniture choices are already supported by ordinary definitions. Chair recipe
`00296338` targets ordered FLST `00296339`, containing 35 physical entries,
including direct furniture and child recipes. The native/compiled path turns
eligible leaves into `aObjectVariants` inside one preview icon. Cycling chooses
a prospective construction form; it does not replace an already placed chair.
Beds and tables use the same list mechanism. BM1's placed-wall CHANGE instead
selects grouped Snap Behavior rules and applies replacement/add/remove actions.

A new definition needs the actual discovery relationships. BNAM alone, a familiar
name, an existing model or a recipe count does not put it into the grid. The first
FNAM menu keyword, category-list membership, grouping flag, target form/list,
conditions and suitable assets all matter. The installed add-on's Shared Outpost
Storage is positive evidence that additional plugin recipes can use the ordinary
route. Arbitrary custom plugin behavior and effective override winners have not
been tested.

The inspected ordinary catalogue containers grow dynamically. Neither the native
population/selection routes nor the compiled grid loop imposes a detected fixed
1,000- or 2,000-item menu limit. Allocation failure, finite counters, recursion,
asset availability and UI performance remain real bounds. This is a scoped
absence of a small fixed cap, **not unlimited capacity** or a stress-test result.

Definition locks, material shortage and placement rejection are different states.
Research/perk failure can remain visible; quest/global/context failure ordinarily
does not survive the provider's restricted retry. A visible or selectable entry
can still fail ingredient, quota, budget, territory, support or collision checks.
No universal construction API or safe integration ABI is qualified.

The footer is a cache display. Its production statistic is a sum of item rates,
even across different output products, rather than a synchronized batch schedule
or inventory-growth measurement. A mixed four-producer calculation is reproduced
from installed definitions in production.md. Cargo counts qualifying active
cargo endpoints in the selected Workshop membership, not ships or a universe-wide
route count; Crew uses the assignment-list count, not station capacity.

No earlier scientific status is overwritten. The old Build Mode audit's untraced
wall-CHANGE language predates BM1; the [BM1 report](../construction-variants/report.md)
controls that now-resolved mechanism. The separate Locations field-coverage pass,
actual throughput and historical screenshot diagnosis remain outside BM2.
