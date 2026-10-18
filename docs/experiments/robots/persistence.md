# Real saved robots and ordinary reconstruction

[Report](report.md), [instances](instances.csv), [corpus](corpus.csv),
[nonrobot controls](controls.csv), [CR3 selected humans](../crew-lifecycle/witnesses.csv).
Historical observations are not controlled chronology; repeated snapshots are
not counted as independent actors. No save was modified or loaded.

## Metadata-first selection and extension

The frozen inventory contains 278 protected metadata identities. The initial
selection revisits all 106 CR1-supported mature saves, preserving 97 earlier
build rejects as NOT TESTED. It finds eight robot actors in HIST-0255. Since
every corresponding E2 also has humans, the extension selects the remaining 32
current-build mature inputs within the existing 64 MiB decoder boundary.
Thirty-one are readable; HIST-0167's frozen source is absent, has no listed
existing archive and remains unavailable. All 137 readable originals were freshly
hashed before/after decoding and again in verification. Other 43 inventory rows
remain outside this mature/current-build stratum, not assumed robot-free.

The extension finds no additional robot identities. This is a bounded supported
representation search, not universal absence across every Actor/default branch.
Actor-prefix gaps, unsupported extras and missing fields remain in the local
per-save receipts. `corpus.csv` records selection separately from successful
reading; the missing receipt is `.local-work/r1-robots/HIST-0167.json`.

## Positive witnesses

All below are HIST-0255, protected original SHA256
`635c07a4914c3313bbf12f031523f707183e4757324ce070f361bec0edfe10b4`.
Actor records use actual footer form type `4B` and supported buffer 153, not a guessed
type from a version byte. Initial created-reference base joins and first explicit
keyed 4C are independently decoded. Every WorkshopItem `054ba6` and CrewAssignment
`26beac` pair has the same unique ordinary beacon owner; that beacon independently
contains the actor in its ExtraE2. Locations below are decimal decoded offsets.

| Actor / base | Actor record / first 4C | Owner / owner record | Independently established human comparison |
|---|---|---|---|
| ff021b88 / Garden (`04297c`) |11648190 /11649574 |ff038542 /6343629 | Generic actor `ff084217` selects Management part 3, same E2 |
| ff021b89 / Model A04 (`337eab`) |11650147 /11651550 |ff038542 /6343629 | Same Management human; robot has no ordinary process grant |
| ff02aa28 / Model A04 (`337eab`) |11906800 /11908179 |ff062012 /7830902 | Generic actor `ff044fcb`, retained CR3 selected specialist evidence |
| ff02aa29 / Model S01 (`1d8ee5`) |11908734 /11910120 |ff062012 /7830902 | Same human; no ordinary process grant |
| ff07258a / Model A03 (`1d924e`) |13805747 /13807229 |ff062012 /7830902 | Same mixed owner; conditional definition-backed outpost Fusion rank 1 |
| ff038e6e / Model A04 (`337eab`) |12267384 /12268793 |ff087168 /9306058 | DLC actor sfbgs050.esm:08eca5, explicit reciprocal assignment; detailed DLC perks excluded |
| ff040479 / Garden (`04297c`) |12449445 /12450820 |ff087168 /9306058 | Same mixed owner; second distinct Garden actor |
| ff068d59 / Model S01 (`1d8ee5`) |13613691 /13615062 |ff047885 /6918321 | Lin/Heller plus generic Security actor `ff084219`, explicit/selected ranks in CR2–CR3 |

These are eight distinct saved actor IDs within one pinned sample, not eight
independent playthroughs. Their direct NPC construction recipes explain a single
actor representative rather than a hidden PackIn actor pairing. Constructed
identity versus effective selected NPC remains explicit: Model A03 has leading
Extra2B; its selected template mask has part 3 clear, so its direct power grant is
not replaced by another template's Engineering. The nested NPC zero-change and
selected parts remain in the local link trace. Other robot part 3 flags are checked
against current definitions; historical override parity is not assumed.

## Saved/runtime correspondence

| State | Evidence and persistence class | What it does not establish |
|---|---|---|
| Constructed actor and base | Actual typed created-Actor initial prefix; PERSISTED saved identity/base | A runtime pointer/handle or actual current location |
| WorkshopItem and CrewAssignment | Explicit actor 4C pairs plus independent beacon E2; PERSISTED identities / RECONSTRUCTED handles | Historical Health, active registration, arrival or output |
| Selected template parts | Extra2B supported prefix and nested NPC; PERSISTED choices / DEFINITION-DERIVED effective base | Union of ancestor perks; an unparsed later NPC tail is not absent state |
| Robot process ranks | Direct installed rank 1 definitions, qualified template bit 3; DEFINITION-DERIVED and restored base replay | Missing additional saved rank block does not mean rank 0; extra external grants remain UNKNOWN |
| Added ranks | Shared actor ranked-list writer/loader from CR2 | No explicit robot-added rank list is promoted from an opaque tail |
| CrewSlotCost / reassignment / essential settings | Shipped placement PEX plus configured VMAD and defaults; MIXED script-applied actor state | These actors' historical effective AVs are not decoded by reading an opaque actor extra `15` tail |
| Count threshold | Installed GLOB value 3 and compiled quest increment; saved GLOB changes are a separate channel | Actual historical player rank or current effective threshold without decoding that sample's global changes |
| Current construction count | Owner reverse edges → selected-context item set → recipe-global equality; RECONSTRUCTED/TRANSIENT | A dedicated serialized robot scalar, all unresolved/default constructions or active contributor count |
| Active A1/DB entries | Actor finalization clears/replays selected base/additional ranks; RECONSTRUCTED | Saved raw entry pointers or a universal remote-retention guarantee |
| Output/timing/power state | Existing producer/power save channels and current consumers; MIXED | Which actor caused a saved scalar or whether that scalar remains authoritative after load |

The beacon ExtraBC object list is not a complete constructed-object registry.
The initial exploratory boolean checking those lists was false for these robots;
it is retained locally as a rejected membership oracle. Positive WorkshopItem,
reciprocal E2/4C and native reconstruction, rather than that failed list heuristic,
support ownership. No missing decoded field is promoted into absent robot state.

## Falsifiers and smallest future discriminator

A contradictory unique WorkshopItem owner or mismatched same-sample E2 would
falsify a proposed reciprocal join. A selected part 3 override or historical
definition removing the direct perk would falsify its conditional rank. A native
ordinary admission path accepting count>=threshold without the documented bypass
would challenge the count model. An actual generator query without required
actor entries/Health, or a new direct arrival predicate, would challenge the
shared participation contract.

For the missing robot-only saved category, the smallest future control is two
protected copies of one ordinary outpost with no assigned humans: A with no
robot; B after constructing one Model A03 (or one Garden on a matching producer),
with ordinary no-action companion saves if testing causal byte changes. Record
construction identity, owner reverse edges, E2/4C and count/threshold. That would
discriminate robot-only registration without confounding human assignment; it
would still not measure runtime contribution. A later invocation-matched
Health/process/entry snapshot and actual generator/production observation would
test operation. **Neither gameplay/save acquisition nor instrumentation is
authorized by this proposal.**
