# Allocation order and switch persistence

2026-10-17. SOR-EXP-0041 / SOR-EV-0049. [Frozen contract](followup-contract.md),
[original report](report.md), [review](review.md), [availability](availability.md).
Completion and confidence are separate: the bounded offline derivation is
STATIC; saved bytes corroborate representation, not a running allocation.
Maintainer review and publication gates remain in force.
Independent review02 **ACCEPTED** the bounded task as **COMPLETE**;
[review.md](review.md#focused-allocation-orderswitch-follow-up) records exact
snapshot, executed versus receipt-inspected checks and corrective history.

**A is conditionally reconstructable.** Ordered saved adjacency is real input,
but it does not identify the triggering root, current generator eligibility,
setting, handle-resolution failures or current activation/animation state.
The native sequence is specified below. **B has a positive persistence contract:**
open-state difference is encoded in REFR change mask `0x800000`; ExtraAction
is reconstructed, rather than an independently saved Extra0D Boolean. Current
getter results also depend on pending work and animation. **C:** one available
He-3 satisfies the ordinary one-cycle ingredient comparison; charge and other
operating gates remain independent.

## Evidence notation and corrections

All function identities below are preferred static **VAs**, hexadecimal, for
retail **1.16.244.0**, image base `0x140000000`, executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
For example allocator VA `0x14066b100` is RVA `0x0066b100`.
The [single function register](../native-availability-map/functions.csv) supplies
VA/RVA pairs and prerequisites. Object offsets, words and masks are hexadecimal.
`oNNN` denotes `.local-work/p1-order/native/NNN.request.tsv`, except `o012`
in `native-r2`; `pNNN` retains the original P1 path. Raw exports remain local;
[follow-up pins](followup-sources.csv) bind them and the saved receipts.

Preserved correction to P1: its phrase "queue preserves discovery order" did
not establish FIFO behavior. Actual front insertion and pending-entry rotation
give the different contract below. Its allocator "discovery vector" starts
with **eligible generators**, not every node visited by generation collection.
The preliminary "animation/script" wording is narrowed to the demonstrated
pending map, animation variables and named interface query. No authoritative
Papyrus property or independent Extra0D saved payload was established.

## A: roots, generation seeds and assessment

An allocation invocation receives a reference root; no fixed global priority
list or construction timestamp is consulted. `14066bfc0` invokes it on the
first connection endpoint and, conditionally, its owner/beacon; removal/split
paths `14066c4f0`, `14066ccd0`, `14066d890`, `14066e9b0`, `14066d4b0`
and `14066fa50` select affected references/components (p007–p010 and o001
caller references). `140f35090` invokes it on its changed-reference operand
(o001). These are event-dependent roots, not save record iteration order.

Owner refresh `14066d4b0` obtains roots through `1406728e0` (o002): it walks
Extra `4D` reverse linked-reference entries in increasing array position,
stride `10`, filters keyword `145f0b3d8` and positive nominal generator
predicate `1406697f0`, and appends resolved references. It invokes the allocator
for those roots into a shared result set, applying old/new differences after
collection. Each invocation has its own supply/demand accumulation. The reverse
list is runtime ownership indexing; the inspected serialized `4C` forward
ownership link does not certify the rebuilt reverse-list order.

`140671f70` first traverses the generation component and appends unique eligible
generators to the seed vector. It sums `140669880` contributions; excluded
generators are separately recorded. Both traversal modes enumerate onward
after the generation classification callback, including across an ordinary
non-generating switch. Allocation-node gating is a later, different step.

With default-true `bWorkshopPowerNonRecursiveTraversal` (`145e8c1a8`),
`140675c50` removes the **front** pending handle and appends its visited identity.
`1406779e0` enumerates ExtraCB entries in increasing array position, resolving
direct targets or spline endpoints. `140677c50` first rejects visited identities.
If the target is already pending it rotates `[begin, found, found+1)` to move
that target to the **front**, before a new edge-gate evaluation. Otherwise it
tests `140669c60` and pushes the handle to the **front** with `1406797c0`.
Thus the last newly admitted neighbor is normally processed next. This is a
deque worklist with front promotion, not breadth-first FIFO traversal.

Decisive instruction proof (o004/o005): `1406797c0` decrements front index
`+18`, writes the handle there and increments count `+20`; `140675c50` reads
front and increments it on removal. At `140677e41..140677e7d`, the rotation
arguments are begin index RBX, found index R14 and found+1 R8; `140679890`
implements three range reversals. The decompiler loses some iterator fields;
the instruction operands establish these indices. Pending duplicate promotion
must not be simplified to "ignore duplicate" on cyclic graphs.

With the setting false, `140676350` calls classification `14066bcb0`, marks
visited, then `140678f60` / `1406791d0` recursively follow admitted neighbors
in forward CB order (p011/p020/p026/p027). The callback returns 1 even after
an excluded generator. Recursive forward traversal and the front worklist can
collect generators in different orders. Equal reachable sets do not prove
equal seed order or equal binary32 supply summation order.

`14066b100` then walks the generator seed vector at increasing index, appending
eligible neighbors at the end through `1406722f0`. This second stage is an
expanding multi-source vector, independent of the setting's worklist direction.
Visited pointer-set membership prevents repeated assessment; pointer ordering
does not rank consumers. Excluded/invalid/open-switch nodes are marked visited
without demand assessment or ordinary expansion. The receiver/simple-terminal
category branch can also stop expansion. On expanding nodes, the partition
restriction rejects direct word-1 edges when required; spline crossings have
their separate admitted route. Rejected consumer demand still expands when
its category permits; shortage alone is not a traversal cutoff.

If no generator seed exists and `142116840(root,1)` returns a cell-context
reference, the allocator adds the original root and, for its qualifying
receiver/simple-consumer branch, its Workshop-linked owner. This path uses
cell-context fallback supply initialized in the allocator before generation
collection; it is not a blanket rule
to add every changed consumer. `142116840` examines parent-cell `+b0`, cell
flags and child subtype, then resolves a handle via `140922b30` (o002).
The exact category-specific cell-context result is an explicit runtime input,
not a claimed universal outpost supply source. Assessment runs only with
positive computed supply. Each assessed power-applicable node adds reference
base PowerRequired, virtual `+18`, to cumulative binary32 demand. Threshold
and rejection arithmetic remain the original P1 result.

Array mutation matters. `14065c2f0` appends unique `(FormID,word)` entries;
`14065bfc0` removes matching endpoints by moving the following tail forward
(o001), preserving survivors' relative order. Saver `14051ea30` case CB writes
count, remapped reference identities and connection words in array order.
Loader `14065be30` restores entries in that order (o012). Pure identity remapping
does not numerically sort entries, but missing handles, later insertion/removal,
owner reverse-list rebuilding and topology recomputation can change the usable
walk. There is no demonstrated guarantee of the same future root or assessment
sequence after load/rebuild.

## Actual saved order examples and bounded replay

Owned [followup.py](../../../research/p1-power/followup.py) freshly decodes and
fully reframes R3 in HIST-0036 and HIST-0077, checks every selected locator,
prefix, change flags and ordered extra against the original P1 receipt, and
rehashes each original before/after. Receipt
`.local-work/p1-order/saved/inspection02.json` covers 311 and 234 candidates.
It records one complete actual eight-node, seven-edge reciprocal word-3 tree
per sample. The fixture has two solar-dome generators, two receiver lamps,
two levers and two consumers; it is not a fabricated electrical network.

HIST-0036 root `ff04fd2e` yields generator seeds `[ff04fd2e, ff04fd30]`.
Conditional assessment identities are
`ff04fd2e, ff04fd30, ff04fd2a, ff04fd27, ff01a9f5, ff04fd26,
ff01a9f1, ff04fd23`. The corresponding HIST-0077 identities are
`ff049065, ff049067, ff049061, ff04905e, ff01a477, ff04905d,
ff01a473, ff04905a`. All are saved DYNAMIC identities, not runtime handles.
Choosing the other generator as root reverses the two seeds; each fixture
therefore has two distinct assessment sequences over its four root/mode runs.
Modes differ in generation visitation here, but not the generator order for a
fixed root; do not claim these two-generator trees prove general equivalence.

Assumptions are explicit: all saved targets resolve in unchanged order,
positive eligible generators, matching connector/receiver predicates, positive
total supply and otherwise valid nodes. The fixture makes no demand/supply
calculation. Its conditional open-switch variant skips the chosen lever and
cuts off its leaf consumer while retaining generation gathered earlier.
An additional four-node synthetic cycle checks pending promotion: after
root a queues [d,c,b], processing d promotes b ahead of c, giving a,d,b,c.
Ignoring pending duplicates instead gives a,d,c,b. Forward recursion gives
a,b,d,c; it is labelled a control-flow counterexample, not saved proof.
Replay validates our implementation against specified sequences and invariants;
it does not measure a historical or newly loaded native invocation.

## B: switch getter, transitions and persistence

`1405cdc70` (p019, RVA `005cdc70`) is an **open-state** getter on supported
base types `1e/24/25/27/2f/3e`: 0 unsupported/unknown, 1 open, 2 opening,
3 closed, 4 closing. The Open/Close bindings in `1400391d0/140039200`
and setter paths ground these names (o004). For switch-keyword category
`140a74420`, electrical gate `140669ac0` excludes **state 1**, or the matching
reference override supplied by the recomputation event. Do not replace this
with a test for saved powered bit `40`, or treat opening/closing as state 1.

Getter precedence is exact:

1. `1418c2a60` checks the locked pending map `145f43de0`, keyed by current
   reference pointer. A pending desired open/close returns 2/4 immediately.
2. Otherwise ExtraAction type `0D`, byte `+20`, mask `04` supplies fallback:
   set → 1, clear or absent → 3. Writers' RTTI is `ExtraAction::vftable` (o003).
3. If both animation variables `Open` and `Close` exist, their `+68 == 1`
   values override with 2 or 4; otherwise their inactive state retains fallback.
4. When that pair is unavailable, reference interface `+60`, virtual `+98`,
   queries `OpenCloseFormState` (`140030f50`) with fallback and clamps 0..4.
   This is a named interface override, not evidence of an authoritative saved
   Papyrus property. No particular VM instance was substituted for this query.

`1405cd370` (o001) and completion setter `1405ccd00` (o010/o012) choose
`140b47420(ref,4)` or `140b475b0(ref,4)`. These set/clear ExtraAction mask 04,
allocate/remove the default extra as necessary and maintain REFR change mask
`800000` relative to the reference's default state, subject to the shown
cell/template exclusions. The animated route queues desired state with
`1418c2af0`; immediate/snap variants write directly. `1405cd7a0` dispatches
Open/Close animation/actions; completion updates the settled bit. Pending
entries are counted and retired by `1418bcfb0` (o010). Power recomputation
may receive the same-reference override before settled state; this is temporal
state that a saved powered word cannot describe. Natural activation contains
the same bit writers and queue insertion at `140af796a..140af7bbd` (o009).

There are **two distinct change masks**. `140b29470` (o007) returns default
state from ExtraAction mask 08 XOR current change-record mask `400000`.
Definition REFR loader `140b230a0` recognizes `ONAM` (`4d414e4f`) and sets
mask 08 at `140b24307` (o006). Save restoration `140b29990` invokes
`14050ffe0` to toggle mask 08 when saved `400000` is present (o006/o008).
The default-open mechanism is separate from current open difference `800000`.

Reference saver `140b29700` (o008) has no separate `800000` body payload;
the REFR change flags carry the difference. Generic extra saver `14051ea30`
has no serialized ExtraAction case. Post-load reconstruction `140b2bc70`
uses default helper XOR saved `800000`, writes/clears ExtraAction mask 04 and
restores animation/action state. Instructions `140b2bfbd..140b2c097` (o009)
establish that XOR and writer branches despite this large function's erroneous
decompiler switch recovery. Existing transition animation can defer its settled
branch; `140b3cbc0` reaches `1405cd370` for load/reset initialization (o006).
Thus recoverable persisted intent and current getter result are distinct.

The saved levers are grounded by dynamic REFR base `001b1862`, ACTI
OutpostPoweredLever02, ESM byte 3,474,375, keyword `001690a4`; ordinary COBJ
`0025240a` directly creates that base. Base `001b1863` is also classified, but
no sampled instance is claimed for it. All 86/62 sampled levers have saved
`400000` clear; `800000` is set on 8/12. HIST-0036 `ff01a9f5`, record
[3,077,048, 3,078,102), has change flags `9280030f`, ExtraFlags `800` and
the bit difference set. HIST-0077 `ff01a477` is its separately resolved example.
The receipt retains their precise locations and bytes through the owned reader.

For an ordinary dynamically created lever with original default closed and no
overriding pending/animation/interface state, set `800000` reconstructs open
(electrically excluded state 1); clear reconstructs closed. This is a
**conditional static interpretation of actual saved flags**, not independently
observed toggle ground truth. We have not measured these switches' displayed
On/Off poses or proven every construction/script initialization preserves that
default. A saved `40` bit says whether that switch was powered at capture; the
allocator computes downstream power separately. Their observed correlation is
not proof of either activation cause or shortage.

The minimum discriminating follow-up is a separately authorized paired save
of the same identified lever, settled before/after one toggle, no topology or
inventory changes, recording displayed state and loaded conditions. Compare
its REFR identity/base, `800000`/`400000`, extra/animation component and `40`
independently. A third reload-and-save snapshot tests reconstruction stability.
For actual assessment order, a separately authorized bounded natural call
capture needs root/event, setting, resolved ordered CB entries, seed vector,
skip/partition predicates and assessment sequence at a common epoch. Until
then the offline fixture's explicit parameters are the achievable contract.
Neither experiment was performed or implemented here.

## C: bounded fuel threshold

The installed recipe remains `002b0639`: He-3 `000057f5` ×1, fueled generator
`002b063a`, nominal interval 36 engine-elapsed seconds. `140f7f6f0` (p100/o012)
compares total available ingredient count with required count using **unsigned
less-than** rejection, then floors available/required and caps requested cycles.
For ordinary requested cycles = 1 and sole required input = 1, available = 1
passes and yields cap 1; no additional reserve is imposed along this checked
path. `140f881c0` collects the existing eligible input references; this is not
an assertion that one unit in any arbitrary container is available.
`140f7d6a0` issues the accepted ingredient removal; it does not require a
non-null item product. No full inventory/network simulation was added.

Charge state remains independent: `140f7f1e0` uses effective
WorkshopProduceUntilNextCycle, `Uncharged` 1 / `Charged` 2. An accepted reason-0
cycle can consume inputs, restore generation, refresh and set Charged; a
Charged reason-7 transition suppresses generation and sets Uncharged. Timer
readiness/modifiers, validity, halt, current power applicability and activation
can prevent immediate output. Exactly one available unit answers the ordinary
ingredient threshold; it guarantees neither immediate nor continuous generation.

## Load-determinism clarification

The [load investigation](load-determinism.md) identifies actual load-event roots
and narrows two earlier dependencies: CB stores FormIDs, whereas temporary
queues/Extra4D use manager handles; owner refresh unions its per-generator
results, so merely permuting its fixed root list does not change that union.
Neither the earlier missing pre-save last root nor these fixtures establish
variation across identical-save reloads. Historical claims are refined with
new native evidence; repeated-load settled equivalence remains OPEN.
