# SD3: what Locations Stored Resources reports

2026-10-19, Australia/Sydney. SOR-EXP-0057 / SOR-EV-0065.
[Frozen plan](plan.md), [provider](provider.md), [membership](membership.md),
[aggregation/refresh](aggregation.md), [icons](icons.md), [saves](saves.md),
[methods/source pins](methods.md), [acceptance and review](review.md).

**Best-supported answer:** Locations reports a snapshot of resource-unit counts
from eligible inventories belonging to each registered, resolvable Workshop.
The selected row displays that outpost's already collected arrays. The collector
requires container capability and effective `OutpostBuildContainer != 0`, and
substitutes the single shared backing inventory for recognized shared fixtures.
It converts physical inventory items into their associated resource definitions,
merges by resource FormID, and orders the presented resources by resource name.
It does not independently add player pockets, ship cargo or every remote chest.

| Question | Strongest supported answer / confidence | Coverage and meaningful limit |
|---|---|---|
| Which outpost? | Registered handle -> qualified beacon/ExtraWorkshop -> OutpostStaticData entry -> selected EntryObject; STRONG STATIC | Actual native/compiled binding; active player ownership and exceptional registry reconstruction retain earlier limitations |
| Which inventories? | Workshop reverse membership, container/effective AV gate, shared substitution and deduplication; STRONG STATIC | 306 physical definition rereads plus 44 saved-case definition rereads; effective overrides and historical loaded resolution unobserved |
| What quantity? | Sum of item-instance stack units, grouped by associated resource identity; STRONG STATIC + sampled SAVE | No mass or production-rate arithmetic; no new generic zero/negative clamp; saved exceptional stack extras remain unsupported |
| Which icons? | IRES symbol/color or GNAM-named OrganicIcons clip; STRONG STATIC | Exact Iron, Adhesive, Amino Acids and Adaptive Frame joins; actual display and unsupported-class exceptions not executed |
| When current? | Collected on Locations state entry, transferred asynchronously, then repainted from provider arrays; STRONG STATIC for mapped path | No inventory-event subscription/recount in the mapped state; current timing, racing mutations and external re-entry behavior unmeasured |
| Saved support? | 27 item rows at three positively joined HIST-0036 beacons, including incoming/outgoing and mixed resource classes; STRONG scoped SAVE | 278 canonical locators, 255 originals, 147 supported, 108 unsupported, 23 missing; no screenshot/save pairing or exhaustive outpost total |

The useful distinction is between **shared eligibility** and **different outputs**.
SD2's construction walker uses the same eligible-member callback, but adds ship
and player sources and plans spending. SD3 walks each outpost independently,
only collects its member sources, and filters/maps their items for reporting.
Industrial consumers instead follow directed graph and recipe/transport rules.
Physical inventory existence does not make all three consumers equivalent.

Installed EXE SHA-256 freshly equals
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
the pinned retail 1.16.244.0 image. Main ESM SHA-256 freshly equals
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
This is installed static analysis, not a measured current load order or historical
runtime baseline. [Sources](sources.csv) bind inputs, readers and primary receipts.

Scientific confidence, completeness, independent acceptance and publication are
separate. This is a bounded ordinary mechanism, not a complete active-player
outpost detector, safe callable API, simulator or importer. No new RUNTIME result
is claimed. Proprietary/save/movie evidence remains LOCAL-ONLY; authored synthesis
is REVIEW-REQUIRED. [Review](review.md) controls assignment disposition.
