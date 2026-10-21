# One backing inventory, multiple access fixtures

Reader notation: [vtable versus object offsets](../../audits/publication-readiness-b2/notation.md#native-prose-at-first-use);
[experiment-local export namespaces and lookup](../../audits/publication-readiness-b2/native-export-ids.md).
These guide the existing local address/offset declarations; they do not make
export labels global symbols or raw exports available in a checkout.

[Answer](report.md), [prerequisites](prerequisites.md), [consumers](consumers.md),
[saved correspondence](saves.md), [methods](methods.md).

**STRONG / STATIC:** the recognized containers are access fixtures for one
player-held backing reference, **player+1008**. The mapped consumers substitute
that reference; they do not copy remote container stacks into one another.
Multiple eligible fixtures do not multiply the backing inventory. This conclusion
comes from the consumer and save/load paths below, not the word Shared.

## Recognition and residence

Installed CONT `SFBGS00D.esm:02af77` bears keyword `04d338` from the same add-on,
`WorkshopStashContainerKeyword`. Installed DFOB `04d339`,
WorkshopStashContainerKeyword_DO, targets it. `1401596b0` (n006) initializes the
named default object at `145f0c790`; its resolved target at +48 is `145f0c7d8`.
`140b64da0` (n012) checks the resolved target is KYWD and tests that keyword
through the reference's keyword interface. This is capability recognition, not
an exact-base-name comparison or an attached-script registration.

The physical definition has base CarryWeight 5000, OutpostBuildContainer 1 and
both local output-link prohibitions 1. Its inspected fields contain no VMAD or
BGSDisplayCase. Definitions01/context01 physically qualify these observations.
There is no dedicated script in the inspected add-on archive selection; lack of
a script-name hit alone is not the mechanism proof.

Container menu preparation `1414681d0` (n016/n017) recognizes the physical
fixture, takes player+1008, copies its effective capacity/name context to that
backing reference when needed, and substitutes the menu's inventory target.
`1414805e0` performs the matching handle substitution. Ordinary ContainerMenu
operations consequently act on the backing inventory for that recognized path.
The fixture's placed position and Workshop relationship remain its own.

`1405a3cc0` (full n021, exact n022 window `1405a5d10`) creates a backing reference
only when player+1008 is null, assigns the shared generic base through virtual
+7b8, calls `1405df510/140b24da0` and retains it on the player. This is distinct
from player+1000, another internal inventory serialized immediately before it.
Its complete purpose is not inferred from adjacency. Crafting separately
creates/clears/rebuilds a temporary aggregation reference through `1417f6fa0`
(n007); that argument-owned scratch reference is not identified with +1000.

## Membership and lifecycle

Ordinary construction/move/removal uses the accepted [SD1](../containers-displays/native.md)
and [L1](../limits/native.md) WorkshopItem relationship and selected representative
set. Fresh positive [save joins](saves.md) connect the actual special base to
ordinary beacon owners. Registration is not a new global list of all shared
containers: the mapped ingredient walkers follow **the current bench/outpost's
Workshop membership**, recognize eligible containers and substitute the one
backing reference, deduplicating it by pointer.

`1417fe930` (n011) and construction counterpart `141368cf0` (n013) require a
resolvable member reference with TESContainer capability and effective
OutpostBuildContainer != 0. They then either add that ordinary reference or,
for the special keyword, add player+1008 if present. A saved relationship alone
does not prove it was resolvable during a historical operation. Neither mapped
callback adds an explicit perk, power, cargo-link, planet/system, distance,
Health, disabled-bit or loaded-3D test. Event delivery, reference resolution and
effective overrides remain separate conditions. This is scoped branch evidence,
not a universal claim that disabled/destroyed fixtures remain usable.

The recipe quota ordinarily prevents a second same-quota representative at one
outpost; different outposts have independent quotas. If multiple eligible
fixtures reach the same enumeration, deduplication inserts the backing reference
once. No extra stack copy follows. Direct access through a fixture at another
outpost reaches the same backing reference. Crafting at a bench without an
eligible local source does not enumerate all remote fixtures just because they
exist. [Consumer predicates](consumers.md) distinguish these cases.

Ordinary scrap's content-transfer logic is reused from SD1. It operates on the
removed physical reference; the normal shared-menu substitution and the
ingredient callbacks are separate operations. No inspected ordinary local
removal writer clears player+1008. Moving/rebuilding a fixture does not allocate
another backing inventory in the inspected creation path. Actual last-fixture
scrap, malformed state, direct script deletion and destruction transitions remain
unobserved; do not promise conservation for every deletion caller. The backing
reference has player lifecycle reset/retirement paths (`141a1eac0`, n021/n022),
which must not be confused with removal of one Workshop object.

## Save/load authority and remote meaning

Player writer **`141a46940`**, exact instruction `141a4857a` (n021/n022),
serializes player+1000 inventory followed by **player+1008 inventory**, through
`140b2dbd0 -> 1406447c0`. It writes inventory rows, **not a saved raw pointer or
one physical container's FormID**. Loader `141a48f50`, exact `141a4a9bd` (n023),
reads the second list only for buffer version >= `92` hex, through
`140b2dcc0 -> 1406448b0`. Older versions cannot silently inherit that layout.
The backing object is recreated separately; item identities and per-stack data
are restored through the ordinary inventory loader. Reset `141a4bf80` calls
the corresponding virtual reset on both references (n023 `141a4c9da`).

Inventory rows/stack extras are PERSISTED inside player data; backing pointers,
source arrays, handles and the per-bench combined inventory are RECONSTRUCTED or
TRANSIENT. Fixture identity/membership are independently persisted. Current
post-load authority, callback completion and actual depletion remain unmeasured.

The mapped remote behavior is **shared access to the same reference**. It does
not read every remote cell, transport items between fixtures, require freight
scheduling or synchronize independent stocks. A remote fixture's 3D is not an
operand of this substitution. The relevant local fixture and backing reference
must still be discoverable/resolvable. Actual runtime residency is NOT TESTED.
