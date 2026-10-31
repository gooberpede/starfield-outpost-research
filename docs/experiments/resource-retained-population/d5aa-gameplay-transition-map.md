# D5AA player action and resource-demand map

2026-10-31, Australia/Sydney. [Report](d5aa-report.md),
[source windows](d5aa-sources.csv), [investigation](d5aa-investigation-ledger.md).
All addresses are preferred static VAs for Starfield 1.16.244.0, image base
`0x140000000`, executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Runtime B1 addresses add the RVA to `0x7ff785930000`, never to a source pointer.
Raw exports and disassembly remain local. Function names below are research
aliases unless grounded by the existing RTTI/vtable names.

**Confirmation prepares a pending transition; it does not synchronously select
the resource source.** `0x141a67830` swaps the transition payload into player
storage at `+0xa08`. This is a pending payload slot, not an established FIFO
command queue. Transition processing, world/context preparation, service commands
and worker dependencies are separate stages. The source-map lock selects the
constructing miss only after an eligible request reaches the provider.

## Confirmation and transition ingress

The existing `StarMap::Util::ConfirmFastTravelCallback` vtable at `0x144c943c8`
binds callback slot `+0x08` to `0x1416d3c20`. Its zero response branch accepts;
other response values return without preparing travel. If callback field `+0x10`
is zero it calls `0x141a28cd0` with reference handle `+0x14`; otherwise it calls
`0x1416d48b0` with the other destination identifier. Both prepare a payload
through `0x141a67830`. The Monocle confirmation table at `0x144c84970`, callback
`0x1415f6520`, supplies a separately verified reference-travel ingress. These
are compiled alternatives; B1 does not identify which UI callback executed.

Reference transition `0x141a28cd0` requires the destination handle to resolve,
nonnull TES and clear TES bytes `+0x177/+0x178`. It copies reference position,
orientation and destination membership; an interior parent cell is retained,
whereas the other branch resolves world context through `0x140b4eb40`. It sets
transition reason 5 and swaps the payload into player `+0xa08`.
`0x1416d48b0` prepares a different destination payload; it is not equivalent to
immediately traversing source coordinates.

`0x141a20380` swaps pending player state into local transition storage and resets
the pending slot through `0x141a1ada0`. The outer loading/UI and state predicates
can postpone processing. Direct caller `0x1418842a0` wraps this processor with
main-state progress bytes. Save loading also calls it from `0x141829ec0`; other
explicit producers/callers in the exports remain distinguished. A confirmation
callback return is therefore not a resource-demand timestamp.

The admitted transition calls context processor `0x1417df210` before choosing
the cell/world preparation branch. For exterior destinations,
`0x141a278a0` acquires manager context through `0x14078c940`, obtains/creates
terrain through `0x140bbd270(world,true)`, writes valid focus and calls
`0x14099f2c0` **before** cell resolution and the final call to `0x141a25420`.
That is a positive pre-final-placement demand opportunity, subject to the
service/task gates below. It does not prove that a worker finishes before
visual arrival or loading-screen dismissal.

`0x141a27d80` preserves an important alternative. A null parent relation, or a
parent whose cell flag `+0x48` bit `0x1` is clear, takes `0x141a278a0`.
The interior alternative conditionally drains on a changed cell, acquires context
and calls `0x141a25420`. That body reaches TES cell transition `0x14057abc0`
at `0x141a26536`, `0x141a2666c` or `0x141a2686e` according to its predicates.
Later `0x141a272d0` can update terrain focus through `0x14099f230`.

## Save loading and interior residency

Ordinary full load clears visited state through complementary native routes:
`0x141815620 → 0x1418278c0 → 0x141827960`, type 3, when the reload setting is
zero; or `0x141824020 → 0x141825e00 → 0x141825ac0 → 0x1407896d0` when it is
nonzero. Both converge through reset handling into the actual ProcGen clear.
The manager loader's false compatibility flag still clears ProcGen. These
positive paths and Save52's version/prefix qualification are in
[D5Z](d5z-report.md#persistence-and-load); saved world descriptors are separate
inputs, not visited entries or proof of demand for every saved world.

The fresh `0x141829ec0` body supplies load reconstruction ingress into
`0x14078af30`, world installation `0x14057fce0`, focus preparation,
`0x141a278a0` and `0x141a25420`, under distinct saved-destination branches.
Starting-world `0x141895460` and fallback `0x141895cc0` also call the actual
cell-transition body. These branches do not require pressing fast travel;
their actual Save52 predicates and caller history were not recorded in B1.

An interior cell does not by itself exclude an exterior-linked context.
`0x140af4c50(cell)` first searches the cell's extra-data list via
`0x14051b2b0`: a present-list flag and entry type `0x81` produce the entry's
`+0x38` value. If absent, only the exterior-cell branch (cell `+0x48` bit `0x1`
clear, world pointer `+0x110` nonnull) uses the mapped world/component fallback.
`0x1417df210` takes this context through `0x140786850`, owner/component comparison,
and descriptor/context initialization. An attached interior value is a concrete
possible path, not evidence that the Lodge supplied that value or Jemison.

There is also an explicit interior-residency terrain path:
`0x1405754c0 → 0x140575020 → 0x14099f280 → 0x14099f2c0`.
Its outer guards require the relevant global manager, TES `+0xe8 == 0` and no
reentrant `0x1461df738` operation. The relevant branch additionally needs a
nonzero mode argument and TES world `+0x188 != 0`. It selects existing terrain
at world `+0xe0`, or follows world `+0x1f0` with flag `+0xf2` bit `0x2` through
`0x140bbd270(parent,false)`, then uses the manager's focus. Creation is disabled
on that getter: an existing valid terrain instance is a prerequisite, not an
outcome guaranteed by interior residency. `0x140b03360` supplies another mapped
terrain focus call during cell/world operations.

Consequently an exterior resource-demand route can be eligible while the player
is interior, if the linked context, existing terrain/focus and downstream
service/Grid prerequisites hold. **Actual Lodge→Jemison resource demand is
UNKNOWN.** The operator account establishes interior residency; no copied
Jemison identity, complete attached-data snapshot or caller trace authenticates
that route in B1. The pre-travel retained prefix contains no provider records.
No bounded claim here asserts that all resource/file loading or all exceptional
scripted interiors have been enumerated.

## Native transition table

| Player-visible milestone | Native operation / predicate | Possible resource effect | Provable ordering and historical limit |
|---|---|---|---|
| Load Save52 | Complementary global-revert/type-3 clear, then saved-destination reconstruction | Empty visited state; reconstruction can later enable demand | Clear precedes its own protected unlock; exact B1 load stages/callers unknown. |
| Remain in Lodge | Interior attached context or existing-world terrain update under the guards above | Conditional exterior-linked demand opportunity | No guaranteed Jemison demand; no witnessed prefix provider admission. |
| Accept travel | Named confirmation callback, zero response, valid destination predicates | Pending transition payload at player `+0xa08` | Publication precedes consumption of that payload; no global worker barrier follows. |
| Process transition | `0x141a20380 → 0x1417df210`, matching owner/component or replacement/reset branches | Establish/replace context, descriptor, landscape/source Grid and service work | Preparation is guarded; identical owner alone does not guarantee retention. |
| Prepare exterior destination | `0x141a278a0 → 0x140bbd270(true)`, focus-valid write, `0x14099f2c0` | Eligible service prewarm and other terrain work | Occurs before this function's final `0x141a25420` call; no maximum completion latency proved. |
| Prepare cells | `0x140bbb170/0x140afb220 → 0x140aed020` | Single-cell original Int2 demand after placement/context preparation | Exterior bit clear, global `0x145f60c10 == 0`, cell `+0x20 & 0x2400 == 0`, and false `0x140ad3410(cell+0x110)` required. |
| Service acquisition | Module slots `+0x48/+0x70 → 0x1407b2370/0x1407b1fe0 → 0x1407b3c50 → 0x1407b4750 → 0x1407b2390` | Focus-derived bounded region demand | Focus valid, manager state/context and enabled handle prerequisites apply; command execution may overlap other preparation. |
| Register work | Coordinate/layer/density DB new-entry gates and file/dependency readiness | Ready density/layer nodes can reach provider | Ready nodes can execute before later roots register; warm keys/aggregate can reuse instead. |
| Select target | `0x1407a1940/0x1407b5160 → 0x14079f860` with actual source Grid | Selected contributor passes BIOM then visited/map gates | Target needs current frame/Grid support and identity; no exact earliest B1 target demand is proved. |
| Arrive / move | Final cell processing, later focus/cell/LOD updates | More requests, retained hits, visited bypass or retirement | No source construction must coincide with visual arrival, Workshop refresh or subsequent movement. |

## Demand, scheduling and state boundaries

The service command requires valid terrain focus before `0x1407b2390` can form
its rectangle. Its ordinary branch additionally needs enabled global
`0x145e903a8`, a false `0x1403473a0` global-state test, successful manager
reader admission, receiver manager `+0x20 == 2`, nonnull `0x14078c4e0` context,
the resolved owner handle's allowed form-type predicate, and nonzero active
terrain focus-valid byte `+0xe0`. A focus setter is insufficient if these fail.
`0x1407b30c0` binds region/discriminator; the acquired handles
flow through `0x1407b3aa0/0x1407b2880`. Context initialization invokes the
registered RuntimeService callbacks; their queued commands may inspect focus
after the setter writes it. Focus alone does not prove command execution.
The default normalized Feynman contract produces `[-16,23]²` bounds, but these
are D5S model operands, not measured B1 settings or its first request.

[D5R](d5r-query-scheduling-map.md) and [D5W](d5w-normal-path-model.md) give the
remaining exact native chain: coordinate acquisition `0x1403625e0`, layer
`0x1407b5a00/0x1407b4bb0`, density `0x1407a1260/0x14076cd40`, ready-node
dispatch `0x1427e56d0 → 0x1427eb6b0`, pool claims `0x1428d3960` and workers
`0x14076c560/0x1407b5160`. Original density query survives to
`0x1407a1940 → 0x14079f860`; layer prepares four density neighbors first.
A populated density aggregate skips the provider entirely. The actual B1
worker registrations/claims were not captured.

This establishes code-supported opportunity before final placement and during
qualified interior residency. It supplies no fixed delay, mandatory first source,
global FIFO, measured visual-arrival fence or actual Lodge/Jemison history.
The [causality figure](d5aa/causality.svg) keeps these domains separate.
