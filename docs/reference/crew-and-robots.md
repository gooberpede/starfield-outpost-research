# Crew and robots technical reference

[Reader guide](../guides/crew-and-robots.md) ·
[Claim and evidence map](../audits/remaining-guides-d5bc/claims.md) ·
[Build and source pins](../experiments/robots/report.md#evidence-and-material-gaps)

The native and definition paths below use retail 1.16.244.0 and the pinned
main ESM. Native locators are preferred static VAs at image base
`0x140000000`. Subtract that base for an RVA. Saved dynamic IDs, base
FormIDs and current handles refer to different identity domains.

## Admission, ownership and roster

| Decision | Owner, writer and reader | Boundary |
| --- | --- | --- |
| Human capacity | Station placement/removal adds/subtracts effective slots on the beacon. Menu worker `0x141625260` compares occupied plus candidate cost with the lesser of effective beacon slots and player command slots. It sums nonnegative truncated costs on resolved members, with a raw-count fallback when the default is absent. | Per-destination ceiling. Station construction has a shared threshold of 3, ordinarily 6 with player Management rank 3. Sampled assemblies have two stamped contributions of one slot. [Capacity](../experiments/crew/capacity.md) |
| Robot quota | Eight recipes share JNAM global `0x001d9f5e`. Selected Workshop's item set is reconstructed from reverse WorkshopItem edges and updated on construction/removal. `0x140f3b170` resolves each representative and counts matching recipe-global pointers. | Configured threshold 3 becomes 6 via installed PlayerSkills stage 702 with increment 3. Admission compares against the current floored nonnegative threshold. The count can retain a dead or noncontributing robot. [Limit model](../experiments/robots/limits.md) |
| Ordinary robot placement | Each recipe directly creates an NPC representative. OutpostActorScript's direct or selected script-part-9 binding calls AssignCrew through `0x142068d70`, bypassing ordinary menu capacity. It configures zero slot cost and disables ordinary reassignment. | WorkshopItem key `0x00054ba6` records placement ownership. CrewAssignment `0x0026beac` records actor assignment independently. [Robot lifecycle](../experiments/robots/lifecycle.md) |
| Destination membership | `0x1404076b0` removes prior ordinary assignment, deduplicates and appends the actor handle in destination ExtraE2, and sets the actor Extra4C relationship. `0x140407a10` removes membership/link and processes applicable ability removal. | Travel and queued effects have separate writers. The Locations Crew consumer reads list length. [Assignment](../experiments/crew-lifecycle/native.md#assignment-to-a-real-query) · [Locations](locations-ui.md) |

## Ordinary direct robot catalogue

Each row represents a unique NPC base in the installed category. The original
[catalogue](../experiments/robots/catalogue.csv) gives its recipe and physical
ESM locators. R1 expands CR2's five positive process-grant cases and preserves
their effect findings. Script inheritance in slot 9 supplies no perk inheritance
through slot 3.

| Robot | NPC base FormID | Selected ordinary contribution |
| --- | --- | --- |
| Garden | `0x0004297c` | A1 duration ×0.91, qualifying organic |
| Sanitation | `0x000bd67e` | A1 duration ×0.91, qualifying solid/liquid/gas and nonorganic/nonmanufactured |
| Model A01 | `0x001f416e` | Engineering rank 1, A1 ×0.91 on manufacturing |
| Model A02 | `0x001d9250` | Management rank 1, A1 ×0.95 across the five ordinary families |
| Model A03 | `0x001d924e` | Outpost Fusion rank 1, DB +1/+2/+3 for base generation below 6, 6 to below 12, or 12 and above |
| Security minibot | `0x0004297d` | No direct process perk or enabled perk-part inheritance |
| Model S01 | `0x001d8ee5` | Same bounded negative |
| Model A04 | `0x00337eab` | Same bounded negative |

These are installed definitions and mapped target tests. Combat and overrides
are outside the catalogue result. [Perk and inheritance evidence](../experiments/robots/effects.md) ·
[R1 independent review](../experiments/robots/review.md)

## From rank to a consumer

- **Possession and dispatch.** A crew flag can put a possessed perk on the
  roster. Rank changes replace old entries. A1 `0x140f7bd20` and DB
  `0x140f3dd50` resolve the owner's E2 members, reject the specific native
  life-state predicate and require effective Health above zero. The dispatcher
  needs active process bucket storage, the appropriate assignment environment
  and passing rank and target conditions. Process teardown can free those
  buckets while ownership and assignment survive. Unconsciousness and disabled
  state alone do not reproduce the mapped life-state test.
  [Native gate and counterexamples](../experiments/crew-lifecycle/native.md#life-state-absence-and-replacement)
- **Timing.** A1 operation 3 multiplies duration per eligible actor, then
  evaluates player entries. Ordinary human crew Management `0x0021b8c3` has
  rank factors 0.95/0.91/0.87. Crew Engineering `0x0021b8c8` has
  manufacturing factors 0.91/0.83/0.77. Ordinary entries fail the inter-system
  fuel marker's resource-family conditions. `0x140f7f1e0` determines due work
  from the old row interval and remaining time, then resets both from current
  modifiers. Inputs, current reason and receiving still govern output.
  [CR2 processes](../experiments/crew-skills/processes.md) ·
  [CR3 clocks](../experiments/crew-lifecycle/native.md#production-clocks-and-remote-scheduling)
- **Power.** DB operation 2 adds per eligible actor per generator and uses
  the base band. A nonpositive preliminary base-plus-modifiers result can
  bypass DB. Outpost Fusion `0x0020d24f` is distinct from ship Fusion
  `0x00222f83`, a type 1 destination ability. Power evaluation has its own
  update and fuel/allocation gates. [DB examples](../experiments/robots/effects.md) ·
  [Power reference](power.md)

## Saved participants and reconstructed entries

Owner ExtraE2 serializes actor identities that the reader attempts to resolve
into handles. Actor Extra4C supplies assignment context. Generated actor
template part 3 supplies qualified base ranks, while explicit added ranks have
their own saved channel. Actor finalization `0x1419198a0` clears existing
buckets where present and reaches `0x141955400` through virtual dispatch to
replay base and additional selected ranks. Appropriate process storage and
successful registration are still required. An unresolved saved member may
produce an invalid sentinel, distinct from a retained live handle that fails
one query and can resolve later.
[Saved inputs](../experiments/crew-lifecycle/persistence.md#saved-inputs-to-transient-consumers) ·
[Native replay](../experiments/crew-lifecycle/native.md#selected-rank-and-load-reconstruction)

HIST-0255 supplies eight reciprocal robot joins across four mixed owners.
Model A03 actor `0xff07258a` resolves on the saved assignment and WorkshopItem
edges to `0xff062012`. R1 qualifies CR3's earlier unsupported Extra9C cases,
without decoding every later actor extra. CR3's selected generic Security
witness owns a Pistols grant and supplies no A1 timing entry from that skill.
These examples establish saved inputs and challenge roster-based inference.
Historical post-load bucket residency and actual output were unobserved.
[Robot witnesses](../experiments/robots/persistence.md#positive-witnesses) ·
[Crew examples](../experiments/crew-lifecycle/examples.md) ·
[CR3 review](../experiments/crew-lifecycle/review.md)

**PUBLICATION DEPENDENCY — EVIDENCE ACCESS PENDING.** The tracked catalogue,
reports and calculations can be inspected. The protected saved joins and
original compiled/native witnesses remain separate access dependencies.
