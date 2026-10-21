# Integrity, damage, operational effects and repair

Reader notation: [vtable versus object offsets](../../audits/publication-readiness-b2/notation.md#native-prose-at-first-use);
[experiment-local export namespaces and lookup](../../audits/publication-readiness-b2/native-export-ids.md).
These guide the existing local address/offset declarations; they do not make
export labels global symbols or raw exports available in a checkout.

[Answer](report.md), [attack lifecycle](attacks.md), [saved contrasts](persistence.md).
Native export numbers below refer to `.local-work/da1-defense/native/`.
Every address is preferred static hexadecimal VA, not a runtime pointer.

## Indicator and definition provider

`14158cf50` binds WorkshopPickRefData **fIntegrity** at model-relative +148.
The PickRef payload starts 48 hex bytes into that model. Its producer `14158a6e0`
(n008) resolves the selected reference, reads Health from singleton
`14049a430()+108`, calls its ActorValueOwner current/effective method +8 and
permanent method +10, then computes **current / permanent** when permanent>0.
The value is stored in the payload's typed value lane +118 (model +160).
Otherwise it sends **-1**. Native does not clamp this ratio.

Installed Health registration `140d96b20` (n032) binds the Health entry at
singleton +108; main ESM AVIF `000002d4` independently identifies Health.
The REFR ActorValueOwner vtable at `144b96a90` is qualified by its destructor
thunk `140b90c6c` subtracting **70 hex**. Its +8/+10/+18 implementations are
`140b6ce20`, `140b6cee0`, `140b6cfa0`: current includes modifier storage;
permanent adds modifier section 0 to base; base checks explicit storage,
definition properties and the definition fallback. These are not three
interchangeable health values. Actor turrets dispatch through actor methods.

REFR base fallback `140b82b40` explicitly recognizes Health at instruction
`140b82c03`. It obtains **BGSDestructibleObject_Component** (registration
`1405bf6d0`), reads its data's u32 **+18 hex**, converts it to float and adds it
to the property-derived base (`140b82c52..140b82c67`). Therefore the ordinary
destructible definition is a positive Health source, even when PRPS has no
explicit Health entry. It is not valid to conclude “no Integrity” from an
absent Health PRPS alone. Explicit bases/modifiers remain possible overrides.

The installed WorkshopMenu member, hash pinned in [evidence](evidence.md),
finishes the chain. ABC **1429**, OutpostItemCard.UpdateItemData, offsets
**819–894**, checks presence of fIntegrity, shows the section when it is greater
than -1, and maps ratio 0..1 to frames **1..framesLoaded** with clamping enabled,
casts to int and calls gotoAndStop. MapLinearlyToRange is ABC **65**, code
bytes 0..74; it performs normalized interpolation and endpoint clamping.
It does not display a numeric hit-point count. The supplied screenshot's full
bar establishes visible fullness only, not exact underlying HP or object history.

## Representative object/Integrity matrix

Values are installed main-game defaults, not a universal winning load order.
For destructible nonactors, **H** denotes Health ratio provider above; **A** is
actor Health. **R** denotes the existing-reference repair operation below,
subject to its broken-state and owner/recipe/NoRepair gates. **BF** denotes
saved AV base/modifier storage; a missing override can derive from definitions.

| Object / exact example | Provider and ordinary maximum | Damage/operational threshold | Repair and saved state | Exceptions and coverage |
|---|---|---|---|---|
| Small Iron extractor CONT 0005ef19 | H; DEST Health **200**, one destruction stage | Partial damage lowers ratio; terminal destruction is a separate state. E1 rejects invalid/destroyed producer before creation | R; BF Health damage and form state; related large extractors positively sampled | Medium/large defaults differ; current output not measured |
| Large He-3 extractor CONT 0020a084 | H; **400** | Same shared producer gate; no proportional production penalty from the Health fraction in this gate | Real ff0202dc has damage -144; ff0202f7 has no serialized Health override in the same save/owner | Definition identity is confirmed in definitions.csv; saved comparison is not an attack or repair transition |
| Solar ACTI 00030238 | H; **200** | Destroyed/invalid gate participates in P1 electrical eligibility; power allocation is recalculated separately | R; BF/form channels | Full Health does not imply sufficient sun-selected power or powered consumers |
| Fueled generator ACTI 002b063a | H; **300** | Same invalid/destroyed boundary; fuel availability and charge are separate P1 conditions | R; BF/form channels | Repair cannot create He-3, fix missing links or guarantee current charge |
| Solid storage CONT 0023aed9 (small), 0023aeda/b (larger) | No DEST/explicit Health in inspected ordinary definitions; default H denominator is not established positive | No ordinary destructible-component Health target established; passive S1/S2 inventory is not a producer | No demonstrated ordinary damage/repair need; saved inventory and links remain separate | An attached/modded destructible component or Health override would be a different input |
| Regular cargo PKIN 002191a0; fueled 0021903f | Assembly; no DEST, both carry WorkshopNoRepairKeyword **001e5dcc** | Do not substitute whole-pad “HP” for child inventories/marker state | Ordinary repair excluded by configured NoRepair; persistence of compartments/pairing is C1–C3 | Operational marker ACTI 002a6c3f and regular incoming CONT 00219173 also have no DEST and carry NoRepair. No assumption every assembly child is identical |
| Turret NPC 002e181c (ballistic 1); 001099a5/001e663d (tier 3 pair) | A; PRPS Health **70 / 115 / 310** respectively | Actor life/Health and P1 power are distinct from nonactor destruction | R includes actor reset/recovery; actual pair has explicit Workshop owners | No DEST in these NPC definitions. Actor Health does not automatically admit it to GetDestructibleOutpostObjects |
| Watchtower PKIN 000dae43 | No DEST/Health on assembly definition; auto-foundation height property **5** | No native defense-score contribution in mapped attack paths | Ordinary structure persistence; no damaged tower witness | Geometry and child properties are separate from a numerical defense modifier |
| Armillary PKIN 001ec78c / mount ACTI 001ec794 | No DEST in these two definitions; positive Armillary resource **1** | Quest eligibility resource, not protective Health | MQ00 aliases/resource reconciliation, not a damage history | Attack probability condition is not a damageability test |
| Fabricator CONT 0022174d, Semimetal Wafer | H; **250** | Shared E3 producer invalid-state gate plus recipe/power/input checks | Real ff072592 retains Health damage -3.6667633 in BF | No conclusion that the damage was caused by attackers |

A category label never replaces the actual saved base join.

## Damage and operational consequences

The explicit script DamageObject route is positively mapped, without invoking
it: `14206b1b0 -> DamageObjectFunctor (144d3f290, execute 142065260) ->
1418be6e0 -> 140b56c50`. The dispatcher distinguishes actors from destructible
references; full generic actor combat mechanics are outside DA1. For nonactors,
`140b56c50` admits the destructible-capability flag24, excludes an already
destroyed ordinary target, obtains its actual destructible component and reaches
`1405c02a0 -> 1405c0530`. Positive damage, valid component/target and non-disabled,
non-deleted state are checked. Optional parent/foundation redirection is explicit
in `140b56c50 -> 140f2fc50 -> 1418be3e0`; it is not silently interpreted as
independent damage to every child of a PackIn.

`1405c0530` reads base and effective Health, calculates remaining Health floored
at zero, evaluates actual destruction stages, and at its exported decompiled
lines **422–426** modifies Health **section 2** by new minus old current Health.
REFR modifier implementation `140b6d4d0` calls `1419ae970`, marks AV change
mask `80000000` and emits AV-change events. Negative Health section 2 is thus a
damage channel, not a reduced definition maximum. `14206b300` DamageValue also
uses modifier section 2, with script-modification and actor-specific checks;
it is not claimed equivalent to every physical hit.

When remaining Health<=0, `1405c0530` calls `1405bfe60`. That routine sets
reference **destroyed bit 23 / 00800000**, marks form change 1 and emits the
destruction event. Independently, SetDestroyed binding at `14208bb50` directly
tail-jumps to `140b73230`, which changes the same bit and event state. That is
the human attack's unload shortcut: it need not produce the same gradual damage
history or Health modifier as ordinary hits. IsDestroyed at `14208baa0` reads
this bit. Deleted bit 20 hex and disabled bit 800 hex are different predicates.

Shared producer `140f7d120` begins with `140f2fd40` and disabled/deleted checks.
Nonactor destroyed state and actor Health/life-state are mapped there;
successful production still requires its separate halt, power and ingredients.
Partial Health loss by itself does not multiply the timer or requested units in
this path. P1's `140669ac0` also consumes `140f2fd40`, excluding invalid
electrical candidates within its existing allocation rules. A failed generator
can affect downstream consumers; no blanket graph deletion follows from damage.
Passive S2 stock movement has no general Health/power predicate in its inventory
and downstream-store logic. Object loss/resolution/explicit cleanup can still
remove access. No claim of universally working disabled/deleted logistics follows.

## Repair, identity and accounting

HUD activation handlers `141463a30` / `141464fd0` route their repair action to
`1421e3f50`; Build-mode wrapper `1421b03c0` reaches the same entry. It requires a
WorkshopItem owner, the native broken/invalid predicate `140f2fd40`, an actual
construction recipe via ExtraDA/base lookup, and absence of the configured
NoRepair keyword. It collects the construction's references with `140f366c0`
(single fallback when no assembly), converts them to current handles and submits
`1421e9b50`. This service resolves each handle, checks repairable Workshop state
`140f3cc90`, and calls `140f36310` on the existing reference.

The complete mapped action and its ordinary service branch perform no ingredient
stock comparison, cost roll or material removal. Old names such as
fWorkshopRepairComponentMult and “Mod Workshop Repair Cost” exist but their
existence is not evidence they affect this Starfield repair operation. The
independent direct ObjectReference.Repair binding tail-jumps to `1418c7030`,
which shares repairable-state checking and main-thread/queued service delivery.
It is not identical to all UI eligibility checks.

`140f36310 -> 1405c42d0` restores negative Health damage through modifier index 2
and the ActorValueOwner restoration method +48, resets eligible destruction
state/scene data, clears destroyed bit via `140b73230(false)`, handles actor
recovery, emits owner/object repair notification and refreshes the selected
construction. There is no Delete/Place replacement pair in this route. Existing
reference identity is retained. This is a scoped native model, not a witnessed
repair transition; partial damage does not by itself establish UI repair eligibility.

L1 category quota counts construction representatives; L2 budget is accounted
on ordinary construction/deconstruction. This repair path neither inserts a new
representative nor runs those ordinary removal/accounting operations. Repair
therefore does not buy a new turret allowance or charge a fresh construction
budget in this mapped route. Destruction alone is not ordinary deconstruction;
actual removal still follows the existing cleanup/accounting path. Exceptional
scripts, altered definitions and universal destruction cleanup remain untested.
