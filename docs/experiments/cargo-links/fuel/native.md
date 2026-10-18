# Fuel acquisition, charge and withdrawal

[Answer](report.md), [stage model](stages.md), [save correspondence](saves.md).
All native addresses here are preferred static VAs at image base `0x140000000`;
RVA is VA minus that base. Object/interface offsets are hexadecimal. These are
OBSERVED-INTERNAL operations, not validated integration points. No runtime
module base, object pointer or live field was sampled.

## Identity and local evidence

Fresh preflight pins retail EXE 1.16.244.0, SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
and main ESM SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
The installed Misc BA2 and ContentResources ZIP were hashed, then all five C2
PEX members and their five development sources were freshly read and matched.
PEX decoding closes each member; development comments are not consumption proof.
`f001`–`f003` below mean `.local-work/c3-fuel/native/NNN.request.tsv`.
[Function locators](functions.csv) retain exact export lines and bounds;
[source pins](sources.csv) bind receipts, inputs, helpers and reused baselines.

| Installed record | Positive connection / operand | Physical ESM offset, decimal |
|---|---|---|
| ACTI `219523`, OutpostCargoLinkMarker_Fueled | Resource AV `21e6fe` = 1; fueled keyword `216f84`; VMAD RequiresFuel true and ship `219042` | 3,645,320 |
| IRES `21e6ff`, OutpostCargoLinkInterSystem | NAM1 resource AV `21e6fe`; NAM2 recipe `214c92`; NAM3 interval GLOB `217854` | 1,301,643,316 |
| COBJ `214c92` | FVPA ingredient IRES `0057f5` quantity 5; CNAM null product | 1,300,539,019 |
| IRES `0057f5` and COBJ `05ed88` | Ingredient resource resolves to He-3 product MISC `00558e`; no ship-fuel item guessed from a name | See definitions01.json and prior E1 definition mapping |
| GLOB `217854` | FLTV bytes `8fc2f53c`, approximately .03 hours; binary32 multiplication by 3600 gives 108 seconds | See definitions01.json |

The ordinary ACTI `2a6c3f` lacks this resource recipe; its marker and ship use
RequiresFuel false. Supply missions use additional script configuration; they
are not silently treated as ordinary player endpoints.

## Actual causal chain

1. Registration `140f7dfa0` (f003) connects the positive resource AV to the
   Workshop's IRES group. Base quantity is rounded upward into row +0c;
   ordinary sampled pads have iteration quantity 1. The shared scheduler
   `140f7ef20 → 140f7f1e0` handles elapsed production, separately from ship timers.
2. `140f7d030` (f001) recognizes fueled generators or the configured fueled
   cargo-link default object. Existing E1's constructor/default binding is
   DFOB `03e829 → KYWD 216f84`; it is not an inferred EditorID test.
3. Current-reason evaluator `140f7d120` checks activation/invalid-state, halt,
   applicable power and other ordinary reasons. At `140f7d4b9..4e1`, for a pad
   outside builder/extractor/generator categories, mode 0 with charge 2 bypasses
   the input cap. Otherwise `140f7f6f0(..., null, 1)` must yield a cycle, or
   reason 7 results. Ship Papyrus native `14206ab30` (f003) passes mode 0 and
   returns reason == 0. Condition wrappers `140c59ab0/140c01fe0` corroborate it.
4. At due production, `140f7f1e0` explicitly passes mode 1 at `140f7f3b0..3b5`.
   This forces the ingredient recheck even for a charged pad. With reason 0,
   it calls `140f7d6a0` with the due count at `140f7f3c9..3d3`.
5. `140f7d6a0` (f001) recognizes the pad through `140f7d030`, calls input cap
   `140f7f6f0` with an output vector, and iterates prepared source-removal rows.
   Each row is source handle +00, quantity +04 and ingredient pointer +08,
   stride 10. The IRES ingredient is resolved to its product before invoking
   the source reference's virtual +458. This is a concrete inventory-withdrawal
   request, independently of the admission-only null-vector call.
6. The recipe's null product leaves no receiving output container. This does
   **not** bypass the pad's fuel removal. No fuel item is first added to the
   logical marker. Normal successful removal consumes `5 × accepted cycles`;
   partial availability caps cycles by `floor(available / 5)`. Actual removal
   failure/concurrent inventory changes remain outside this static ordinary
   accounting claim.
7. The scheduler's charge update uses AV singleton +3d0,
   WorkshopProduceUntilNextCycle. Enum table `1459141f8` names 0 NoResourcesNeeded,
   1 Uncharged, 2 Charged. Reason 0 with prior 1 writes 2 via producer +70 virtual
   +50; reason 7 with prior 2 writes 1. Fuel-generator power suppression is a
   separate branch: pads do not inherit a generator's PowerGenerated mutation.
   f002's `14038a200` identifies the +50 implementation as the base-AV setter
   tailcall, supporting persistence through the existing ExtraBF channel.

The charge's numeric identity is positively bound. Existing complete constructor
export `.local-work/recon/e1-stacking-08.tsv`, lines 3808–3810, creates named
WorkshopProduceUntilNextCycle with index `7c` and stores it at singleton +3d0.
Fresh f004 `140d96680` calls form-ID setter `1405e18a0` with index +700 decimal;
f005 confirms that setter writes the form identity. Thus `7c + 2bc = 338`,
matching the saved ExtraBF AV `000338`. The fresh large constructor's capped/
incomplete export is not substituted for the earlier complete named binding.

## Which stock is accessible

`140f881c0` (f002) seeds the consumer handle, looks up its incoming adjacency in
the resource-transfer map, resolves each source and walks further upstream with
a visited set. The output contains those incoming references, not a proximity
search and not the endpoint/ship pairing graph. Ingredient cap `140f7f6f0` then
counts eligible units across this transitive set and distributes removal rows
over their actual inventories. Four units in one store plus one in another can
satisfy five; four total cannot satisfy one requested cycle. It does not remove
a fractional recipe merely because some stock exists.

Consequently direct-linked He-3 extractors and transitive gas stores qualify;
a linked cargo incoming child can supply fuel received through another route.
Physically adjacent storage, player inventory, ship hold and cargo bays have no
automatic special source status. A bay's He-3 qualifies only if its reference
is reachable through this ingredient graph and ordinary item eligibility.
S1's marker has no established TESContainer component; S2's link creation can
admit a fuel-consumer edge without its ordinary container flush. The visible
fuel endpoint is therefore not evidence of a separately stocked fuel tank.

## Rate, lifecycle and modifiers

Fuel use is producer-driven, even while a ship is away or waiting for fuel.
Both unhalted pads can independently consume their local recipe supply. Linking
clears OutpostProductionHalted on both markers; unlinking/marker initialization
adds it on fueled pads. Fresh PEX confirms these writes. A charged pad halted
or otherwise ineligible does not bypass those earlier failure reasons.

The base interval is `binary32(.03f × 3600f) = 108`. `140f7bd20` folds eligible
assigned actors then the player through perk entry A1; scheduler reset multiplies
by positive effective HarvesterRateMult, substituting 1 when that effective
value is not positive. The existing E1 arithmetic/stacking contracts apply.
The main-ESM A1 review retains category-conditioned outpost perks and unconditional
Constellation's Guide `208e92` .95 entries as candidates; the sampled 102.6-second
row interval is compatible with `binary32(108 × .95f)`, but does not identify
the historical actor/rank that supplied it. Relevant known category conditions
must actually match the producer context. Skill descriptions do not establish
a fuel discount. OutpostManagement cargo-capacity entry AA belongs to C2's
hold-capacity arithmetic, not this five-unit recipe.

There is no LY distance, ship grav-jump cost, current ship hold, freight weight
or departure counter operand in these recipe/cap/removal/scheduler bodies.
The complete shipped TransferCargo, CargoLinkCanProduce, arrival, load, leave
and retry bodies make no direct fuel removal call. f002's direct caller census
finds `140f7d6a0` called by the producer scheduler and `140f8c580`; f003 resolves
the latter as existing load-event pending-production replay, rather than a
voyage debit. That bounded positive review supports periodic consumption;
it does not exclude external mods or claim all engine calls were recovered.

At a successful due update, cap/removal can accept multiple elapsed cycles;
with 12 available units and three requested cycles, it withdraws 10 and leaves
2. An initial one-cycle shortage rejects the call and leaves four unchanged.
No stock-change event in the ship/quest wakes timer 2 immediately. Input changes
affect subsequent current-reason queries and producer updates. No fuel debt per
failed ship poll or per missed voyage is recorded by these paths.
