# Analytical decision tables for selected mechanisms

2026-10-21. These are **original analytical decision tables**, not decompiled
or verbatim engine source. Each table is a reading aid for the linked accepted
research, within its build and coverage. It introduces no new scientific claim,
callable API, simulation, safe integration point or live observation.

## Existing producer clocks and changed crew factors

Use the pinned native domain and row layout in [E1 clocks](../../experiments/inorganic-extractors/arithmetic-clocks.md#countdown-catch-up-and-reset)
and [production operands](../../experiments/inorganic-extractors/arithmetic-production.md).
[E1 review](../../experiments/inorganic-extractors/arithmetic-review.md) and
[CR3 review](../../experiments/crew-lifecycle/review.md) govern their respective
scientific snapshots; this table receives its own B2 semantic review.

| Stage / condition | Analytical action | Boundary preserved |
|---|---|---|
| Elapsed is at least the old positive interval | Derive due cycles by the mapped binary32 division, truncation and integer conversion using that interval. | Do not subtract old remaining first or adopt a newly assigned crew factor retroactively. |
| Otherwise | Subtract elapsed from old remaining; positive remaining stays pending, nonpositive makes one cycle due. | The ordinary countdown branch differs from the large-elapsed branch. |
| Due work and resolved producer | Retain the effective interval multiplier; loop registration-time integer iterations; recheck reason in mode 1 and call creation only for reason zero. | Iterations are not current effective resource quantity or recipe NNAM. Halt, input, power and other gates remain applicable. |
| After the due branch | Resolve base and recompute timer or nominal fallback; apply retained multiplier and reset both remaining and interval. | New crew factors affect the reset. Overshoot is not preserved as a continuous clock; a reason failure does not preserve automatic due debt. |
| Handle fails | Mark sentinel and retain the described integer due/iteration bookkeeping. | No universal replay of that bookkeeping is established. |
| Creation requested | Follow the distinct destination, recipe, capacity and insertion paths. | Requested quantity is not accepted quantity; special early object and leveled-product branches remain outside an ordinary-item shortcut. |

The authoritative examples remain discriminating: interval 36, remaining 5,
elapsed 10 yields one due cycle before reset; elapsed 50 also yields one through
the large-elapsed branch. This is not a measurement of inventory growth.
[BM2 nominal production](../../experiments/build-catalogue/production.md) separately
folds current effective rate terms in native order with binary32 rounding and
cached eligibility, excludes fueled generators and does not predict realized
throughput or current power state.

## Eligible inventories and Stored Resources rows

[SD2 shared backing](../../experiments/shared-outpost-storage/shared-inventory.md),
[consumer matrix](../../experiments/shared-outpost-storage/consumers.md),
[SD3 provider](../../experiments/stored-resources/provider.md) and
[aggregation](../../experiments/stored-resources/aggregation.md) control these
branches. Their [SD2](../../experiments/shared-outpost-storage/review.md) and
[SD3](../../experiments/stored-resources/review.md) reviews preserve the static
scope and actual rework, including default-entry preparation.

| Question / stage | Analytical decision | Exception / coverage |
|---|---|---|
| Is this a construction/Stored Resources member source? | Resolve a member of the relevant Workshop, require TESContainer capability and nonzero effective OutpostBuildContainer. | A saved owner edge alone is insufficient. Craft/research have their own provider context; do not sweep every remote fixture. |
| Ordinary or recognized shared fixture? | Keep ordinary reference, or substitute the present player-held backing at `player+1008`; deduplicate source references by pointer. | Absent backing adds no shared source. Several fixtures do not multiply backing stock. Fixture position/membership remain separate. |
| Initialized inventory exists? | Visit initialized stacks. Otherwise use the base-container/default-entry path. | Do not add default stock again to initialized inventory. Default count zero prepares argument 1; initialized zero stacks do not receive that substitution. Generic realization of default/leveled entries remains qualified. |
| Does an item map to a resource? | The mapped item visitor admits MISC with exactly one associated component whose form is IRES; normalize an IRES input through its physical item first. | Multiple/missing/non-IRES associations do not become generic crafting decomposition. Mounted displays are not independently swept. |
| How is quantity grouped? | Sum mapped stack counts, then accumulate by associated IRES FormID. | No weight, component-amount, interval or capacity multiplication; no invented positive-count filter or saturation. Abnormal signed/overflow/rendering cases remain untested. |
| What reaches the screen? | Build name-ordered resource/count arrays, copy into queued UI data and repaint the selected entry. | Collection, delivery and repaint have different epochs. Selection alone does not recount inventory; source locks do not prove a global atomic snapshot. |

Spending craft ingredients and displaying Stored Resources are different
consumers. Neither table nor a positive distant fixture proves arbitrary
unloaded reference residency, exact backing quantities after load, current
availability to craft or universal conservation on deletion.

## Catalogue choice and placed component replacement

[BM2 catalogue](../../experiments/build-catalogue/catalogue.md),
[eligibility](../../experiments/build-catalogue/eligibility.md) and
[BM1 manual/automatic](../../experiments/construction-variants/manual-and-automatic.md)
describe different operations. [BM2 review](../../experiments/build-catalogue/review.md)
and [BM1 review](../../experiments/construction-variants/review.md) control status.

| Operation | Analytical route | Identity / limit |
|---|---|---|
| Discover a prospective catalogue choice | First-FNAM roots lead to categories and recipe/list children; conditions and specialized availability gates determine candidates. | Physical definition census is not an actual menu population. |
| Retain an unmet unlock | Ordinary failed recipe can survive the restricted perk/research retry as unearned. | Quest/location failure is not generally rescued; visible locked is different from absent. |
| Attempt construction | Preview evaluates ingredient/prerequisite/quota/budget/placement state; ordinary commit requires accepted frame status 2. | No universal total ordering across unrelated calls or atomic low-level recheck is asserted. |
| CHANGE on a placed hab component | Eligible grouped STBH entries drive the documented candidate/transition/executor path; PKIN replacement generates children linked to stable anchors. | Do not equate a component's generated reference with its stable anchor or prospective recipe. Not every target is a primitive base swap. |
| Automatic connection behavior | The mapped ungrouped STBH rules follow connection/disconnection context. | This is separate from manual grouped cycling, foundation/stair actions, material swaps, animation or damage. |

Saved replacement edges are positive correspondence, not paired CHANGE action
or rendered reload proof. No independent-side selector or blanket furnishing,
wiring or decal persistence guarantee is supplied by these mechanisms.
