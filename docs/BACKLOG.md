# Separately scoped research backlog

## Cargo Link Time-Skip Reconciliation

2026-10-18. Separate **future modding application**, informed by
[C3 fuel/time research](experiments/cargo-links/fuel/report.md) and
[worked discontinuity cases](experiments/cargo-links/fuel/time.md). Elapsed
production and direct local delivery can advance during wait/sleep while cargo
timer stages are one-shot and are not replayed once for each missed voyage.
Possible consequences are outgoing freight and net He-3 buildup, remote
manufacturing starvation and storage saturation, conditional on supply,
consumption, capacities, timing and otherwise functioning routes. These are
source-derived predictions, not verified universal gameplay outcomes.

Future scoping could reconcile missed voyage stages or perform bounded abstract
freight transfers during skips. It must account for temporal order, available
stock, outbound and reverse freight, independent periodic fuel-production
accounting and each stage's readiness timing, effective capacities, partial unloading,
returned cargo, pauses, broken routes and item conservation. Reproducing ordinary
transport rules and intentionally changing balance are different design choices.
**No mod, plugin, hook or save modification is authorized.** The existing native
cargo-link UI enhancement remains a separate backlog application.

### C2/C3 boundary correction

The older C2 freight / C3 remote-fuel entry below is retained as historical
planning. [C2](experiments/cargo-links/transport/report.md) and its
[transit continuation](experiments/cargo-links/transport/transit.md) now explain
ordinary returned freight, remote transport, movement and recovery. C3 adds
He-3 accounting, endpoint readiness and their elapsed-time interfaces; remote
transport generally is no longer deferred to C3. C1/S1/S2 accepted scopes are
preserved. No new execution follows from this prospective clarification.

## Future modding application: native cargo-link management UI

2026-10-18, documentation only under [C2](experiments/cargo-links/transport/report.md).
Extend [C1's inventory/direct-neighbor queries](experiments/cargo-links/configuration-ui/report.md)
using [S2 local output-link traversal](experiments/local-output-links/native.md).
For **Outgoing Resources**, trace upstream through intermediate storage to
configured extractors, greenhouses, husbandry and fabricators, deriving their
products/recipes even when every intermediate inventory and the outgoing bay
is empty. Show configured potential, current eligibility/operation and physical
stock separately. For **Build Resources Needed**, trace downstream through
storage to ultimate fabricator/fueled consumers; distinguish possible recipe
inputs, local supply and actual unmet/import demand. Reachability alone does
not imply exclusive import need or a producer's intended destination.

Account for branches, cycles, mixed stock and ambiguous producer/consumer intent;
do not duplicate quantities along multiple reachable paths or infer an exclusive
manifest. Consider read-only remote graph/stock/eligibility diagnostics alongside
the existing **Remote outpost diagnostics feasibility** entry below. C2's shared
hold, returned freight and asynchronous sampling make stock provenance and
freshness explicit requirements. This preserves the user's application idea;
it authorizes no plugin design, implementation, hook, UI patch, package or new
source project. A separately agreed implementation brief is required.

Current C2/C3 boundary: remote/unloaded **transport**, saturation and interruption
are investigated in C2; detailed inter-system He-3 acquisition, rate,
replenishment, fuel transport and persistence remain C3. This supersedes the
earlier C1 follow-on allocation of remote transport to C3 below; it does not
reclassify C1 evidence or authorize C3.

## C1 result and S2/cargo follow-on boundary - 2026-10-18

[C1](experiments/cargo-links/configuration-ui/report.md) explains configuration/UI
and Save52. [S2](experiments/local-output-links/report.md) preserves downstream
stock redistribution/direct production. These backlog entries grant no live,
implementation or C2/C3 execution authority. User topics in the C1 brief refine
this existing boundary; earlier S1/S2 findings remain unchanged.

| Deferred topic | Bounded question / provenance |
|---|---|
| Storage-container side indicator | Percentage and green/yellow/red thresholds, refresh, effective occupied weight/capacity and clipping/>100% after overcapacity production. Save52 screenshot is a user reference, not live instrumentation. S1 capacity supplies underlying arithmetic, not the display contract. |
| Remote outpost diagnostics feasibility | From elsewhere (for example Lodge), query membership, individual production eligibility, power, inventory/capacity, local-link graph and pending work. Separate snapshots from trends; unresolved reference is not stopped/empty. |
| Remote reference/producer lifecycle | Do ordinary distant/unloaded states cause failed resolution/sentinel/pending bookkeeping and later identity reconciliation/delivery/catch-up, versus deletion/exceptional cases? S2's matched lifecycle test remains proposed only; actual residency and universal debt replay are unknown. |
| Local stock re-redistribution | Which triggers, if any, flush old upstream stock when a destination regains space, beyond established link-add and explicit/script triggers? Mixed-item local plans lack aggregate reservation; no periodic conveyor is inferred. |
| C2 freight / C3 remote fuel | Preserve user-reported outgoing-to-incoming spillover and **undelivered freight returning from a blocked destination** as an OPEN hypothesis. C2 covers departures, loading/unloading/round trips, stranded/returned cargo; C3 remote saturation/unloaded simulation/recovery and inter-system He-3. Full local storage or C1 empty panels prove none of these causes. |

## Storage follow-on boundary - 2026-10-17

[S1 reference](experiments/storage/report.md) supplies storage/endpoint semantics;
S2 now supplies separately scoped movement. The deferred chest/display phase
retains general contents/persistence, Shared Outpost Storage cross-outpost access
and workbench sourcing, and which inventories (including shared storage) feed
LOCATIONS **Stored Resources**, with its refresh triggers. The supplied Schrod II
Ad image remains a question prompt, not evidence of aggregation provenance.
C1's Cargo Link resource panels are different providers. No follow-on experiment
or implementation authority follows.

## Save29 allocation authority - bounded closure, 2026-10-17

[Offline result](experiments/power/save29-authority.md): **C / STRONG** for ordinary
Save29 loading. The known load-event allocator independently selects #1 from the
actual ordered four-reference graph, without a favourable-root assumption.
Retain accepted reload PASS and save-writer NO-GO; defer general save-to-settled
power prediction. Do not automatically build a temporal observer or reopen save
writing. A concrete contradictory native/observed path, decisive independent
evidence or material application need can justify a separately scoped decision.
[Independent review/package](experiments/power/save29-authority-review.md) governs
assignment acceptance; no integration, live or publication authority follows.

## Local native availability dependencies — 2026-10-15

[Neutral native mapping](experiments/native-availability-map/report.md) identifies internal loaded-region retrieval and upstream preview/Workshop descriptor construction. [Scientific discriminators](experiments/native-availability-map/uncertainty.md) retain complete same-evaluation region/point/translation/cache operands and established-context equality as unresolved evidence needs. No observer implementation or live authority is requested by this offline result. Deferred position/geography/Hab questions remain separate.

## Inorganic availability milestone B continuation — 2026-10-15

[Result](experiments/resource-availability-milestone-b/report.md) and [acquisition assessment](experiments/resource-availability-milestone-b/acquisition.md) retain the spatial-equivalence dependency: complete loaded source/resource/region/point operands and independent decisions, actual frame translation and linked final populations. The executable is conditional on qualified inputs; 346 final UI folds agree, while spatial equivalence is NOT TESTED. Arbitrary-site generation additionally needs selected component/descriptor/ordering/terrain inputs. A separate approved acquisition brief is required; no live execution or deferred-topic reopening follows.

## Frozen position questions — DEFERRED, 2026-10-14

Verified under the [inorganic availability brief](implementation-briefs/CODEX_BRIEF_SOR_inorganic_resource_availability_runtime_serialization.md).
These questions remain separate from resource availability; none is reopened here.
The brief explicitly broadens the earlier feature-only reopening recommendation:
a concrete application need, independently discriminating evidence, **or** a
pre-public-release research review can initiate a new scoped decision. An actual
experiment still needs its own approved inputs/actions and falsifiable controls.
There is no promise to resolve these before release.

| Status / question | Preserved evidence and reopening discriminator |
|---|---|
| DEFERRED — historical 0.5.0 versus 0.6.0 native XYZ/Z state | [Cross-session report](experiments/cross-session-center/report.md), [caller audit](experiments/workshop-caller-semantics/report.md), [disposition](position-model/disposition.md). Own frame flag/parent, activation epoch and transformation remain unresolved. Reopen with matched identity/lifetime/caller/epoch and independently measured frame operands, or an application/release review requiring that evidence. |
| DEFERRED — complete saved-to-live vertical restoration and terrain/procgen dependencies | [Z restoration](experiments/workshop-z-restoration/report.md), [write history](experiments/position-write-history/report.md), [050 frame follow-up](experiments/ship-relocation-050/z-frame-followup.md). Reopen for a height-sensitive application or independently discriminating load/writer/consumer evidence, or pre-public-release review. |
| DEFERRED — exact continuous subcell longitude/latitude | [Position specification](position-model/specification.md), [application disposition](position-model/disposition.md). Qualified anchors/discrete positions do not establish continuous beacon geography. Reopen for concrete geographic precision need, independent native geographic reference/held-out seam evidence, or release review. |
| DEFERRED — native-equivalence branches and historical position exceptions | [Consolidated review](position-model/review.md), [capabilities](position-model/capabilities.md), [generic marker/fallback](experiments/fallback-grid-provenance.md). Preserve existing-reference, source-world/marker-to-Workshop and unmatched historical frame boundaries. Reopen with a concrete linkage need, independently discriminating branch/identity evidence, or release review. |

## Removed-outpost four-wall Hab control — DEFERRED, separate question

[Population acquisition assessment](experiments/workshop-population/acquisition.md)
and [original acceptance](experiments/workshop-population/acceptance.md) preserve
the two retained four-wall Hab assemblies. Exact world/location/historical-beacon
context does not establish original player construction or authoritative Workshop
ownership. A small future protected-copy construction/deletion/outpost-removal
and no-action-save control could test whether similar remnants persist; it cannot
recover the past ownership of those exact saved identities. Reopen only by a
separate controlled-save brief or independently discriminating same-cohort
historical evidence. No save creation, game launch or observer work is authorized
by this backlog, and this control is not part of inorganic resource research.

## Position consolidation disposition — 2026-10-13

[Disposition and falsifiable reopen criteria](position-model/disposition.md) defer historical runtime XYZ/Z, continuous exact geography and generic landing-marker provenance until a concrete feature needs them. Prioritize separately briefed authoritative structure membership, then deposits/active production, power and cargo semantics. No execution or integration is authorized by this backlog.

## Read-only save-menu identification extractor

2026-10-14: the [explicit support brief](implementation-briefs/CODEX_BRIEF_SOR_save_menu_identification_utility.md) is implemented for review in the [utility/report](experiments/save-menu-identification.md). Practical identification is qualified for five controlled menu entries, with original timestamp provenance/collisions/unknowns and a model-based separate mature Save52 label. Universal menu parity is outside scope. The earlier unimplemented status below is preserved history; no additional menu reverse-engineering phase is proposed.

Recorded 2026-10-12 under the Q030 procedure brief; **not implemented or investigated**.
Future separate brief should map research IDs to visible character name, manual/auto/
exit-save type, in-game location text, level, visible date/time and playtime, detect
collisions and support character-filtered menus. User examples Cao Tran and Atilla
Kiraly are examples, not newly verified labels for the controlled Save27/28 input.
Until qualified, use pinned filenames/hashes plus explicit unique-row/operator
confirmation, preserving unknown labels rather than decoding assumptions.

## Workshop membership follow-through — 2026-10-14

[SOR-EXP-0032 dependency map](experiments/workshop-membership/dependencies.md) advances explicit saved owner/root reconstruction. Separate briefs are still needed for alternate 80/default/inherited population restoration, independent loaded native item census, production readiness/integration, container/display contents and category/filter views. Empty fixtures remain instances when supported; stored/displayed item rows must not be promoted without independent construction evidence. Power, deposits/operating state, cargo/output links and rates remain separate. This note authorizes no execution or implementation.

Workshop population: [EXP0033 boundary and original criteria](experiments/workshop-population/acceptance.md) govern any later loaded-census or controlled historical acquisition. Container/display contents, category labels and functional cargo/power links remain separate decisions/briefs. No production importer or live execution follows from the supported 848-root research export.

## S1 capacity follow-up and S2 boundary — 2026-10-17

[Capacity report](experiments/storage/capacity-report.md) supplies conditional real
saved boundary calculations and distinguishes item-specific local partial fit
from production/direct generic batch addition. No new live evidence is required
merely to use the bounded ordinary model. S2 must correlate actual operand state,
planned quantities and source/destination deltas before interpreting backpressure;
routing/retries/cargo scheduling remain separately briefed. Current effective
capacity is unmeasured; no observer, live, importer or writer authority follows.

## Cargo Link Fuel-Efficiency Correction (in-game mod)

2026-10-18, documentation-only future application under [CR1](experiments/crew/plan.md).
[C3](experiments/cargo-links/fuel/report.md) establishes five He-3 per accepted
periodic fuel-production cycle and a 108-base-scheduler-second interval, separate
from freight trips and endpoint readiness. Investigate whether eligible
production-speed/interval modifiers accelerate that consumption without increasing
freight trips; identify the actual crew/player perks and their eligibility before
attributing an effect. Consider decoupling those clocks or per-voyage fuel economics
only in a later scoped design. Balancing is unimplemented; no perk applicability,
mod, hook, live test or save change is authorized. Keep this separate from the
existing cargo-link UI enhancement and Time-Skip Reconciliation applications.

## Starfield Save-to-Network Importer (Outpost Network web-app feature)

2026-10-18, documentation-only future application under [CR1](experiments/crew/plan.md).
Reconstruct saved outpost identity/site, production configurations, cargo pads and
pairings, and defensible inferred outbound products into a draft Outpost Network.
Preserve uncertainty, player-entered planning intent and existing UUIDs on reimport.
This is a web-app feature proposal, not an in-game mod. Outstanding completeness
problems include selected biomes/site resources, actual skill ranks, exceptional
constructed-object membership, identity matching and arbitrary/modded saves.
[CR1 saved crew gaps](experiments/crew/saves.md) and earlier Workshop/site/cargo
coverage remain explicit. Do not build an importer or promise full JSON parity;
implementation requires its own later decision and brief.
