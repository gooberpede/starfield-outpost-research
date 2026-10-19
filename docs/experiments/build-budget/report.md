# L2: what the outpost Build Limit measures

**Build Limit is an accumulated construction charge.** The mapped ordinary
Starfield path uses one scalar budget, with a default allowance of **2,500**.
Its fast cost function starts with a base charge of **1** and uses form types,
properties and optional fixed surcharges. The installed main ESM sets all four
actor/container/light/navmesh surcharge settings to **0**. A simple eligible
object therefore ordinarily costs **1**; an assembly can cost several units
because its eligible constituent references are summed. One construction root
does not necessarily cost one unit.

**The engine does not recount rendered triangles to make this decision.** It
resolves the selected construction's references and effective forms, calculates
their charges, and stores the candidate total in the build context. Repeated
admission checks read that cached total and the outpost's current actor value.
The mapped ordinary gate accepts `usage + candidateCost <= allowance`.
Successful new construction adds the charge; ordinary deletion subtracts the
then-calculated item charge, with a floor of zero.

**The thin footer bar displays cached `usage / allowance`.** Its compiled menu
handler selects `round(100 * ratio)` on a 100-frame movie clip. A rounded full
bar can precede the exact cap, and the separately queued display refresh can lag
an accounting change. The native admission comparison remains unrounded.

2026-10-19, Australia/Sydney. SOR-EXP-0052 / SOR-EV-0060.
[Frozen brief](../../implementation-briefs/CODEX_BRIEF_SOR_L2_outpost_build_budget_native_accounting.md),
[plan](plan.md), [native chain](native.md), [UI](ui.md),
[saved controls/contrasts](saves.md), [verification and review](review.md),
[function locators](functions.csv), [source pins](sources.csv).
Proposed **STRONG / STATIC** ordinary mechanism with **SAVE** corroboration;
exact sampled bytes are PROVEN within their inputs. Authored interpretation is
REVIEW-REQUIRED; game/save/native/movie payloads remain LOCAL-ONLY. Assignment
completion and independent acceptance are separate from confidence.

| Question | Strongest supported answer | Coverage and material limit |
|---|---|---|
| What consumes the meter? | Eligible references in the construction item's single or assembled representation, at scalar form/property costs | Native ordinary wrappers; Kreet additions/removal agree. Raw saved REFR count, physical root count and rendered draw count are different quantities. |
| How is cost fast? | Form/property lookups, bounded member sum and a candidate-context cache at +78 | No model triangle traversal, GPU visibility query or renderer statistics in these inspected cost producers. No claim of a universal renderer-independent engine. |
| What enforces the cap? | Preview status +620, status reason 1e, then accepted-action state +193 == 2 before placement | Native ordinary build UI. No independent atomic budget recheck inside every low-level/script creation function is claimed. |
| What is persisted? | Current usage is an ordinary AV base value in ExtraBF; definitions/settings supply costs and allowance; UI ratio is reconstructed | All 15 beacon-positive Kreet samples explicitly retain AV 00000399. No new load or current-state measurement. |
| Hab versus outside? | Same eligible effective form and properties follow the same cost calculation; room membership/visibility is not an operand | Native same-input contrast, rather than a controlled furnishing trial. Hab assembly constituents and collision helpers are distinct from furnishings placed inside. |
| Constructed robots? | Direct constructed actors use the single-item cost route independently of R1's 3/6 category gate | R1's eight actual owned robots corroborate representation. Default scalar charge predicts 1; historical per-robot budget deltas were not captured. |
| Already over limit? | Ordinary further positive-cost building is refused; the mapped load/rebuild path restores existing state without an excess-budget deletion loop | Scoped STATIC retention rule. Exceptional scripts, corruption or a mod's cleanup are outside this guarantee. |

## Causal path

| Stage | Concrete producer/consumer | Result |
|---|---|---|
| Recipe and selected item | COBJ output -> existing single/PackIn Workshop wrapper | R1/L1/Workshop root model reused, without merging numerical quotas into budget |
| Resolve cost operands | Single `140f64b00`; assembly `140f6e260` -> `140f4c770` -> `140f4c7f0` | Effective-form charge, with reference exclusions; sum for eligible assembly members |
| Cache candidate | `140f33180`, instruction `140f33506` | binary32 charge stored at context+78; refreshed by selection/rebuild paths |
| Admission | `1421dcb10`, `1421dcc0f..1421dcc80` | Compare current usage plus cached charge with effective/fallback allowance |
| Rejection/action | `140f3f9a0` -> reason 1e; `1421b2360/1421b2e20` | Ordinary action needs accepted state; localized exceeded-budget message |
| Account | `1421de3f0 -> 140f4c980`; delete `1421de660 -> 140f4ca70` | Persisted usage base-value update; emit budget statistic refresh |
| Refresh | `1421f2cb0 -> 140f4cb70` | Compute usage/allowance into ExtraWorkshop+90 |
| Publish | `140f34590 -> 14143f690 -> 14143fdc0 -> 14143f8a0` | Snapshot summary, queue copy, populate named fBuildLimit |
| Render | WorkshopMenu FooterContainer.OnStatusDataUpdate, method 621 | Rounded frame selection on BuildLimitMeter_mc |

The attached screenshot identifies the requested footer location and selected
Iron extractor. It supplies no numeric budget reading or matched saved epoch.
Its needed-power 10 is not a budget operand. [UI provenance](ui.md) pins the
actual installed asset independently of that visual identification.

## Scope, counterexamples and next step

The saved sequence is **7 -> 8 -> 10 -> 9**, with unchanged adjacent controls,
linking, rename and solar movement. Beacon-only already costs 7 despite being
one root; the extractor and solar add only 2 despite several saved references.
This directly challenges both a flat construction-root counter and a flat
all-REFR counter. The native model explains why neither is the budget.

Candidate cost, accumulated usage and live rendering expense remain separate.
Changing a definition's costs after building need not retroactively rebalance
the stored usage; deletion can then subtract a different cost. A stale summary,
changed maximum or rounded frame likewise permits disagreement between bar
appearance and new-candidate admission. These are native-supported conditional
predictions, not reproduced exploits or measured runtime incidents.

The bounded ordinary explanatory model needs no new live acquisition. A future
exact historical HUD reconstruction would specifically need the effective
allowance, overrides, selected candidate and refresh epoch of that screenshot;
the screenshot alone cannot recover them. Arbitrary mod/script entry points,
hot changes, malformed state and retail integration are unvalidated. L1 stays
accepted and closed. L3 retains territory/POI clipping, dynamic collision,
procedural scenery suppression and reappearing rocks; turret ownership and
operation remain reserved for their later phase.

## Investigative provenance

A small Fallout 4 lead lookup preceded native tracing. gibbed's
[command inventory](https://mod.gib.me/fallout4/functions.html), entries 751/752,
supplied GetBudgetCounts/WorkshopBudget and draw/triangle terminology as search
leads (SOR-S-0152). Search snippets also surfaced community Workshop script/AV
names; no external script implementation was copied, executed or adopted.
Starfield's retained similarly named AV registrations were inspected, but the
actual scalar cost/admission/UI chain above was independently established here.
The earlier game's semantics are not inputs to the explanatory formula.
Consultation/research credit does not supply code or redistribution permission.
