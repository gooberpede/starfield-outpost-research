# Physical freight transfer, saturation and origin incoming

[Answer](report.md), [journey](cycle.md), [S1 receiving](../../storage/capacity-native.md),
[S2 local redistribution](../../local-output-links/native.md).
Native locators are preferred static VAs, base0x140000000. `nNN` is local
`.local-work/c2-transport/native/NNN.request.tsv`. PEX offsets below are member-relative.

## Shipment operation and native admission

The shipped quest's TransferCargo has89 instructions (body10001..10925 in
`sq_outpostcargolinkscript.pex`). Ordinary unload at 10325 passes
RemoveAllItems(incoming,false,true); ordinary load at 10743 passes
RemoveAllItems(ship,false,true). The last argument is capacity respect, verified
against native registration `142092b00` and implementation `14207dd70` (n02/n03).
That wrapper supplies remove reason18 hex and the respect-capacity byte to
`140b61610` (n05/n14). This is a different planner from S2's local floor-fit mover
and from generic production insertion. No source comment alone supplies the rule.

`140b61610` first obtains recipient effective capacity. For an ordinary CONT it
uses CarryWeight through AV virtual+8; a spaceship base (type41 with its ship
flag) uses `14211b700`; actor capacity has its own branch. With positive C,
free F=C-W<=0 returns **before any source removal**, even for zero-weight items.
With room it gathers eligible source item descriptors under the source inventory
lock, then releases that lock before executing removals. Missing materialized
inventory enumerates base-container entries through `140b87b40`; it is not
treated as empty.

`140b61ca0` builds24-byte planned rows: value/mass priority float+0, quantity+4,
source item descriptor+8 and item bookkeeping+10hex. Admitted forms pass item
virtual+130. Player-specific quest/object exclusions are separate branches;
ordinary bays/ships do not become resource manifests. Local outgoing ONAM
filtering and the set of stock actually present remain separate from this
generic transfer call. Mission SpecificCargo/SpecificCargoMax instead selects
RemoveItemByComponent, and is excluded from the ordinary all-stock rule.

If source weight exceeds free weight, `140b81410` sorts by descending value/mass;
small-vector comparator `140b87cc0` confirms the direction (n07/n09). Zero mass
uses FLT_MAX as priority. Equal-priority ordering is not qualified as stable,
fair or user-controllable. For each retained row with ordinary positive mass w:

```
fit = floor_binary32((F - planned_weight_so_far) / w)
if fit != 0: q = min(q_available, fit)
if planned_weight_so_far + q*w > F: erase this planned row
else: keep it and advance planned_weight_so_far
```

VROUNDSS immediate1 floors; integer conversion truncates that result. Equality
fits; there is no epsilon, throughput-per-second rate or reservation shared with
another simultaneous transfer. Only retained/bounded descriptors execute.
If C<=0, this routine leaves its initial free-weight budget at 0; it does **not**
inherit the generic add helper's nonpositive-capacity bypass. Positive-weight
stock is then rejected by its budget loop; zero-weight rows are a distinct case.
Corrupt/negative/extreme/NaN quantities or mass are outside the qualified model.

Execution sets requested count at descriptor+1c, destination+28 and invokes
source virtual+458 (call at `140b61b20`, n07 window; n14 full function).
The ordinary source/receiver chain is the independently established S1
`140b66680 → 140b67a30 → 140b89690 → 140b8f540 → 140b67100`, stack subtraction
`140b7c100/140b7bd20`, then `140b67380 → recipient virtual+4d0 → 140b4ef90 →
140b4cbc0 → 140b64fc0`. The **actual removed count**, bounded by source stock,
is handed to the receiver. Nonselected stock remains in source; there is no
ordinary copy-and-later-delete operation, full-hold purge, or compulsory move
to an origin outbox. The engine updates/invalidate occupied-weight caches through
the existing inventory mutation family.

This is a staged plan/removal/addition, not a global two-inventory transaction.
The source lock does not reserve every target against concurrent changes.
Exceptional receiver capability/lookup failures, unsupported item classes and
engine interruption have no proven universal rollback. A missing incoming
reference must not be interpreted as a successfully blocked capacity receiver:
the script does not explicitly guard None before RemoveAllItems. Ordinary valid
endpoint conservation does not qualify the null-recipient disposition.

## Load/unload ordering and repeated attempts

Unloading makes **one** capacity-respecting ship→incoming attempt, then calls
incoming.MoveContainerContentToUnfilledContainers, then checks fuel readiness
and sends the unload custom event. If the bay starts full but could subsequently
flush downstream, that call can free it **after** the failed unload; there is
no second immediate normal unload in this invocation. Retained freight can
therefore return even when downstream space becomes available just afterwards.
Fuel-retry timer2 does repeat the whole arrival/unload method without a voyage.

Loading first requests outgoing redistribution; inside its loop it requests
that wrapper again, samples total outgoing count, attempts transfer and compares
count afterwards. No count change ends loading; partial reduction causes another
iteration. The S2 script-native wrapper can request upstream sources' downstream
redistribution, explaining refilling without reversing the local edge direction.
All eligible stock need not be physically in the outgoing bay at the first
sample. Continuous concurrent replenishment and Papyrus budget scheduling are
not an instantaneous atomic load or an unconditional finite-load guarantee.
Ordinary production may interleave; the script contains no fixed stack quota.

Mixed items compete for one free-weight budget, with value/mass priority when
constrained. Example, hypothetical finite operands: F=5, item X mass2 q=4,
item Y mass1 q=4, X selected first →2X then1Y; if Y priority is higher →4Y
and no X. A fit calculation is a prediction only with current item/provider,
stock, ordering and capacity operands. No historical priority or current effective
capacity is inferred from a saved empty bay.

## Returned-cargo discrimination

The same ship hold is unloaded at **both ends**. There is no ordinary item-origin
test in this path. A refused item stays aboard, competes with opposite exports
for capacity and is offered to the original endpoint's incoming bay next time.
This is a positive code-derived mechanism for the user's anomaly, STRONG STATIC;
the [worked journey](cycle.md#worked-partially-blocked-round-trip) shows exact
decrement/increment accounting and full/one-way variants.

Concrete alternative writers: a real opposite-end outgoing shipment, explicit
player/script inventory insertion, or an external mod/mission writer. Ordinary
incoming children prohibit **incoming local output links** (S1); thus S2 does
not ordinarily send the origin outbox backwards into that incoming bay. Incoming
can redistribute **outward** to its storage graph. Direct production likewise
cannot be assumed to target a prohibited ordinary incoming local destination.
An exceptional/changed graph or external writer requires its own positive path.
Mixed saved inventory alone is evidence of stock, not which writer ran.

Useful controls already present: principal ship/bays explicitly empty; other
ordinary/inter-system holds stocked; exactly matching per-end role keys; actual
partial planner and no-stock timer branches. Incident-specific disambiguation
requires uniquely sourced item/count and matched load/refusal/return epochs.
No live capture or observer is proposed as a prerequisite to accepting the
ordinary returned-freight mechanism.
