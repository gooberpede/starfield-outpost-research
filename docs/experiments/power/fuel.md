# Generator contribution, fuel and temporal dynamics

[Definition catalogue](definitions.md), [saved corroboration](saved.md).
This is STATIC native analysis, proposed STRONG within the inspected paths,
OBSERVED-INTERNAL and REVIEW-REQUIRED. No native function was invoked.
All native addresses are preferred static VAs for retail 1.16.244.0,
SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
image base `140000000`; RVA = VA minus that base. Object offsets are hexadecimal.
`pNNN` denotes local `.local-work/p1-power/native/NNN.request.tsv`.
Full exports, game-derived fields and raw saves remain local.

The [bounded follow-up threshold check](followup.md#c-bounded-fuel-threshold)
confirms unsigned available < required rejection: exactly one eligible He-3
unit satisfies one ordinary requested cycle, with no extra reserve along that
path. Timer readiness, charge, halt, validity and activation remain independent;
one unit does not guarantee immediate or continuous output.

## Current generator contribution

`140669880` (RVA `669880`, p007) reads the generator's PowerGenerated base
through reference +70 virtual +18, and its three modifier slots through
virtual +40 with selectors 2, 1 and 0. It adds them in that order. If this
preliminary sum is positive, `140f3dd50` modifies the **base**, after which
the original three modifier values are added again; the result is clamped
to at least zero. It does not multiply total generation by a planet factor.
This helper's returned contribution is distinct from Workshop aggregation,
network reachability and the individual powered bit.

`140f3dd50` (RVA `f3dd50`, p010) applies only to positive PowerGenerated base
input with a distinct linked Workshop and ExtraE2. It walks that Workshop's
assigned actor handles at ExtraE2 +18/+20, resolves each, excludes the actor
virtual +868 condition, requires positive AV singleton +108 and dispatches
perk entry `db` to each eligible actor, passing the same in/out float and
generator context. Failed actor handles can be replaced by a sentinel.
This path dispatches the assigned actors; it contains no extra player dispatch.
The prior [crew selection and rank semantics](../inorganic-extractors/stacking-native.md)
remain applicable to the shared perk dispatcher, rather than assuming every
actor's advertised skill participates.

The complete 502-record main-ESM PERK inventory has one entry-`db` owner:
Crew_Outpost_AneutronicFusion `0020d24f`, physical ESM byte `1290039702`.
Its three entries have DATA `db0202`, scalar payloads 1, 2 and 3 and
PowerGenerated condition operands with thresholds 6 and 12. Local receipts
`power-perks01.json` and `power-perks-recheck01.json` retain the census and
an exact field-by-field reread of this record from the installed ESM, with
unchanged source hash before/after. These are entry payloads and condition
bytes, not evidence that a particular saved or loaded crew actor supplies them.
The shared dispatcher `140c93cf0` indexes operation handlers at
`1458d30b0 + operation * 18`; p107 binds operation 2 to `140c94350`.
Its decisive p108 instructions at `140c943ad..140c943b9` add the entry's
scalar to the pointed-to float. Thus qualifying entries add 1, 2 or 3 power,
with binary32 addition; they do not multiply output by those numbers.
Entry-table label bytes at `144bcf670` decode to Mod Power Generated.
For an illustrative qualifying +3 entry, base 20 and zero AV modifiers give
23. With modifier slot 2 = -20, the preliminary total is zero, the crew
dispatch is bypassed and the contribution remains zero: a crew bonus does
not bypass this fueled-generator suppression branch. These are native
arithmetic examples, not measured loaded generator outputs.

## Fueled generator prerequisites and consumption

Installed ACTI OutpostPowerFueledGenerator01 `002b063a` has base generation
20 and resource AV ResourceInorgPower01 `002b063b` = 1. IRES ResPower01
`002b0638` selects COBJ `002b0639`, whose ingredient is He-3 IRES `000057f5`
times 1 and whose product is null. Its interval GLOB `002b0637` is .01f hours.
`140f7bd20` (RVA `f7bd20`, p100) multiplies that binary32 value by 3600f,
giving exactly 36 seconds before timer modifiers and the positive effective
interval multiplier. The generator is not a recipe producing twenty power
items every 36 seconds: base generation and scheduled fuel use are separate.

`140f7cb70` (RVA `f7cb70`, p100) tests the OutpostIsFueledGenerator default
object, bound to keyword `0003e82a`. Current operating evaluator
`140f7d120` calls input cap `140f7f6f0` for this category with one requested
cycle; zero available cycles gives reason 7. This is distinct from power
failure reason 5 and halt reason 9. No physical connection alone proves fuel.

`140f7f6f0` (RVA `f7f6f0`, p100) obtains the positive selected resource's
recipe ingredients and traverses transitive incoming **resource-transfer**
sources through `140f881c0`. For each required ingredient it counts available
units and caps requested cycles by floor(available / required). With a
nonnull output vector it prepares consumption rows: source handle +00,
units +04 and ingredient pointer +08, stride 10. This is the local input
graph already mapped for [fabricators](../fabricators/native.md#connections-and-upstream-input-contract),
not the electrical wire graph. No general storage accounting is attempted.

`140f7d6a0` (RVA `f7d6a0`, p100) calls that cap for fueled generators and
removes the prepared ingredients through each source's virtual +458 before
the ordinary output-insertion branch. A null product does **not** skip this
fuel branch: only Builders require a nonnull output destination to continue;
the fueled-generator branch consumes inputs, then skips null-destination
insertion. IRES ingredients resolve to their recipe product for removal.
For this definition, one accepted requested cycle therefore requests removal
of one He-3 item. A source-removal request is not an independently measured
inventory delta; concurrency and removal failure are not sampled here.

## Fuel charge and generation changes

The shared scheduler `140f7f1e0` (RVA `f7f1e0`, p101) reads effective
WorkshopProduceUntilNextCycle, AV singleton +3d0. Its enum names are
0 NoResourcesNeeded, 1 Uncharged and 2 Charged, established by the constructor
in prior `e1-stacking-08.tsv` and p102's pointer window at `1459141f8`.
At each due production check it evaluates the current reason and handles
fueled generators specially:

| Prior charge / current reason | Native consequence |
|---|---|
| Uncharged / reason 0 | Calls the fuel-consumption path; restores PowerGenerated through virtual +48 using its base rating, refreshes the graph and sets Charged |
| Charged / reason 7 | Adds negative base generation to modifier slot 2 through virtual +38, refreshes the graph and sets Uncharged |
| Other nonzero reasons | No universal fuel-specific zero-generation or charge transition is established by these two branches; retain the separate halt/disabled/network contracts |

Decisive instruction spans are `140f7f3b0..140f7f44e`,
`140f7f4eb..140f7f508` and `140f7f597..140f7f61e`. Virtual +48
`140b6d720` (p103) restores against the existing negative modifier through
the modifier setter; it does not increase the generator's base rating.
Virtual +50 uses `14038a200` (p106), a seven-byte tailcall to virtual +20,
which is the known ExtraBF base-value setter. Thus the charge writes are
actual AV mutations, not merely anonymous notifications. This setter marks
the reference's persisted AV channel; a restored value still needs current
reevaluation after load.

`14066f880` (p101) can queue to the engine thread; its worker `14066fa50`
(p105) recomputes connected powered membership and applies differences.
Fuel transition timing is governed by the shared due-cycle scheduler rather
than an asserted instantaneous inventory-change detector. The
[existing clock/catch-up contract](../inorganic-extractors/arithmetic-clocks.md)
therefore applies: elapsed at least a positive interval uses trunc(elapsed /
interval), whereas the smaller-elapsed branch subtracts the countdown and
can dispatch one cycle, resetting both countdown and interval afterward.
Saved charge, timer and registry values are historical state, not current
fuel-stock or electrical-authority measurements.

## Answer to the temporal-dynamics question

The inspected ordinary contribution path uses the selected definition's
base rating, current AV modifiers and eligible crew entry `db`. It has no
illumination, local-hour, day/night, weather or wind-event operand or test.
The solar/wind ratings in the [definition catalogue](definitions.md) belong
to distinct ACTI variants selected by planet-keyword conditions; temperature
and pressure select ratings, rather than supplying changing solar irradiance
or wind velocity to this calculation. **Within these mapped ordinary native
paths, solar and wind contribution does not oscillate with day/night or
weather.** Fuel charge, switch/network state, condition and applicable AV/crew
changes remain consequential independent inputs.

This is a positive static dataflow result. It is not a new runtime observation
and does not cover arbitrary plugin scripts or deliberate external AV writes.
Those ordinary coverage boundaries do not justify replacing the mapped
answer with an unspecified weather hypothesis. No new live test is needed to
show what this output helper actually reads. A claim about an additional
modded writer would first need a concrete source or trace identifying that
writer and its conditions.
