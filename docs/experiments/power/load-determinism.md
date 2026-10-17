# Power restoration and identical-save reloads

2026-10-17. SOR-EXP-0041 / SOR-EV-0049.
[Authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_P1_power_load_reconstruction_determinism.md),
[frozen criteria](load-contract.md), [review](review.md).

| Plain-language question | Best-supported answer |
|---|---|
| What does the game do on load? | **Both restoration and later recalculation are supported.** It restores saved powered bits and electrical links. A load-finalization path emits object-loaded events; the Workshop listener can then recalculate from the notified object. Attach, activation and deferred work can make later changes. Restoration is not proof of the settled result. |
| What chooses load-time roots and order? | The demonstrated load callback uses **each notified reference as root**. One notification list preserves saved order, while cell/reference registration and later jobs provide other inputs. No invariant, final Workshop-wide refresh has been established that supersedes all those writes. Reverse ownership order alone is insufficient to predict a change: an owner refresh unions its per-generator results before applying them. |
| Must identical reloads power the same consumers? | **NOT YET ESTABLISHED.** Neither repeated-load variability nor necessary repeatability is demonstrated. Order-sensitive event allocation and a missing pre-save event root prove neither answer. |
| Can an offline reader predict settled outcomes? | It can decode the inspected historical powered bits and ordered links, and compute a qualified individual pass with explicit current inputs. A validated save-to-**settled-powered-set** predictor is **not yet established**. The missing proof is the complete load/attach/deferred event sequence and its final effective inputs, or proof that its differences cannot matter. Those are not automatically intrinsically random or unavailable from all static analysis. |
| Smallest decisive next test? | Separately authorize repeated fresh-process loads of one unchanged, hash-bound deficient baseline, observing the same identified consumers under stable conditions. Use per-consumer game UI first if it can distinguish state. Record early versus operationally settled readings; no test or observer is executed/built under this brief. |

Confidence: proposed **STRONG / native-static** for the particular loader,
event and identity contracts below; **SAVE** corroboration for historical
snapshots; **OPEN** for identical-reload settled-outcome equivalence. Assignment
completion is separate from that scientific verdict and independent review.
No new live evidence, current power values or safe invocation claim is supplied.

## Pinned evidence and identity correction

Preferred static image base `0x140000000`, retail **1.16.244.0**, executable
SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
The existing main ESM remains SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Functions below use preferred static VAs; subtract the image base for RVA.
For example `1405810b0` is RVA `005810b0`, `1421f0340` is `021f0340`.
The [existing register](../native-availability-map/functions.csv) records both.
Object offsets/masks are hexadecimal; counts and RTTI displacement output are
decimal unless marked otherwise. `LNNN` denotes local
`.local-work/p1-load/native/NNN.request.tsv`; L015-L022 are in `native-r2`.
[Source pins](load-sources.csv) bind raw exports, prior evidence and receipts.

**Correction to prior P1 terminology:** ExtraCB stride-8 entry `+00` is a
**reference FormID**, not a reference-manager handle. `14065c2f0` loads it
from reference `+28`; native GetFormID instructions `14204d600/604` read that
same field. `1405de3b0` looks it up in the form map, then traversal obtains
a reference. Temporary traversal queues and Extra4D instead use validated
manager handles from reference `+24` through `1428ccc40`; the latter checks
index/generation before invoking a callback. Callback `1402cf060` returns the
input handle only if the resolved pointer equals the expected reference.
Pointer-set keys are yet another domain. L011/L013-L015 establish this distinction.
The saved token-to-FormID queue mapping and observed graph identities remain
valid; the earlier runtime-CB "handle" label and proposed CB-specific
FormID-to-handle fixup are superseded. No numeric handle/pointer ordering is
silently substituted for saved identity order.

## A: supported lifecycle, with unknown edges retained

This is a **partial order**, not an invented global execution timeline.
Rows with an unknown interleaving must not be read as a universal sequence.

| Stage | Established native path and state | Order/authority boundary |
|---|---|---|
| Saved reference data | REFR change flags and generic extras enter `140b29990` → `140521620`; Extra9C invokes `140545e40` (L001/L002/L014, existing `active-outpost-static-30.tsv`) | Four-byte modern flags are masked with `7ffffffd`, which retains powered `40`. No blanket power reset occurs in this loader. Omitted extras are not assigned an invented historical zero. |
| Restored adjacency | ExtraCB `14065be30` reads count, queued/remapped FormIDs and words in saved array order (prior o012); Extra4C `140547c90` → `140562ef0` restores ordered keyword/target entries (L002) | Per-record restoration is deterministic for fixed remapping inputs. It does not prescribe the eventual event root or scheduler. |
| Ownership reconstruction | Reference post-load `140b2bc70` calls `140526bb0` at `140b2bcca`; saved change `100` causes restored forward4C entries to resolve targets and append reverse4D through `140518750` (L002, existing population native21-23) | Reverse4D is not independently saved: eligibility-table entry is zero and generic loader has no 4D case. It preserves insertion order, not a save-wide canonical sort. |
| Other association/attach paths | `1405a0520` → `1405afea0`; `140afb220` → `140b0fd40`; initialization `140b19a60` → `140afe0d0`; `1405315c0` → `140540a90` → `1405407b0` can insert directly or queue `140543c80` | These are concrete forward-derived rebuild routes. Exact cross-reference order across all relevant load/attach jobs is not established by an insertion lock. |
| Explicit load finalization | `141827380`, diagnosed `FinishLoadGlobalData`, case `0A`, calls `1405810b0` (L015-L017). It processes loaded cells/reference visitors and an ordered restored handle list, conditionally emitting loaded=true events via source `140b9a340` | A positive load-reachable notification path, not a claim that every selected saved outpost member is loaded or notified exactly once. |
| First applicable allocator call | Workshop's TESObjectLoadedEvent handler `1421f0340` resolves the event **FormID**, checks disabled/global suppression and resolved Workshop ownership; on loaded=true it calls `14066f880(reference,null)` → direct/queued `14066fa50` → `14066b100` (L001/L003-L005) | Root is the notified object, not an inferred historical last root or necessarily a generator. If ownership is declared but unresolved, it invokes `14187bb60` and returns; this is a reference cleanup/retirement path, not demonstrated ownership recovery (L020/L021). The actual first successful call for each real saved network remains unobserved. |
| Deferred result application | `14066fa50` compares collected old/new powered sets, then `14066abc0` writes mask `40` for old-only/new-only members and emits further updates (prior p008; L001 call census) | Recalculation is a set-difference update, not necessarily an unconditional rewrite of every saved flag. A reference may retain its restored bit if no applicable differing update reaches it. |
| Later state changes | Cell attach `140b02630`/`140b11780` and reference move/3D paths can emit further object-loaded notifications. TESOpenCloseEvent sinks and AV changes can queue other allocations (L006/L008/L010/L012/L015-L017) | Reaching the game/UI is not proof that all relevant references, animations and jobs have settled. No final universal last-writer barrier has been proved. |
| Settled result | Last effective update for a consumer after the applicable load, attach and deferred work, while topology/inputs remain fixed | **Unknown final edge:** the preserved static paths do not establish one exhaustive, canonical terminal refresh or show that all admissible sequences converge. Operational observation boundary is defined below. |

The load route is bound beyond an analyst-assigned label. Existing RTTI in
`native-r2/rtti01.tsv`, read without database changes by the owned bounded
`PowerLoadRtti.java`, identifies Workshop listener vtable `144d4b710` as
TESObjectREFRGameEventListener, subobject displacement 72, whose base at that
displacement is `BSTEventSink<TESObjectLoadedEvent>`. Constructor `1421ad860`
stores that vtable at `145f5dae8`; `1421ad290` registers it with source getter
`140b9a340`. The dispatch slot is `144d4b718` → `1421f0340`.
The same RTTI identifies the separate PowerUtils sink `144b32be8` as
`BSTEventSink<TESOpenCloseEvent>`, not a universal load-completion observer.
`141883440` registers that sink with the open/close source (L010).

Generic reference restoration and these notifications have separately verified
entry points. No assertion is made that the single generic post-load method
contains every subclass, registration or service completion. Its recovered
large switch has known decompiler problems; positive call/operand evidence is
used, not absence claims based on truncated listings.

## B: exact order provenance and what it does not prove

### Saved load-notification list versus the whole load

`140580d20`, called by global loader `141825e00`, reads the trailing saved list
count and each entry through `1402cee60` into `145e87090/145e87098` in increasing
array order. `1402cee60` restores a saved identity to a current reference handle;
`1405810b0` walks that list forward and conditionally sends its reference FormID
with loaded=true. This supplies a concrete **saved-order-derived part** of load
recalculation, not unexplained randomness. This global-list grammar was inspected
natively; it was not newly decoded from the selected historical saves.

The same finish method also visits current loaded cells/references. Generic cell
enumerator `140b1e190` walks a cell's pointer array backward under its lock,
with category/residency filters. Cell attach callback `140b11780` receives an
array index and calls `140b02630`; that method conditionally emits loaded=true
through `140b97ac0` when `140b40660` admits the reference. Move/3D state routes
`140b48ca0`, `140b40430`, `1418dba40` can emit the same event (L010/L012/L015-L017).
The named positive load route therefore does not establish save-wide order from
ExtraCB alone, or an invariant final root after every attach.

### Reverse ownership, electrical order and addresses

`140518750` locks the target's extra list, deduplicates `(source handle,keyword)`
and appends a stride-`10` entry. `140526bb0` enumerates each source's forward4C
in array order; across sources the order depends on their reconstruction calls.
`1405407b0` demonstrates both direct and service-command insertion. A serialized
critical section orders completed inserts; it does not prove independent reloads
will present the same sources in that order. Conversely, the presence of queued
insertion alone does not demonstrate that its relative order varies on the final
load path or that such variation changes consumers.

**Scoped invariance:** `14066d4b0` collects all eligible owner generator roots,
invokes `14066b100` into one shared new-result set for each, and applies differences
only after collection (prior p007, L018). For an unchanged set of roots and fixed
graph/effective inputs, merely permuting that root loop leaves its **union**
unchanged. Each per-root seed order may still affect that root's contribution.
This corrects any implication that Extra4D array order by itself proves a
different powered set from this owner-refresh function. It does not prove this
refresh is a mandatory final load pass, or that later object-local passes cannot
supersede its result. Direct caller evidence points to `140f7c060` and its
Workshop events, not a demonstrated unconditional last load callback.

Within an individual allocation, the [prior order derivation](followup.md)
still applies: generation uses deque front insertion/promotion or forward
recursion according to the current setting; eligible generators seed a separate
expanding vector; consumers accrue demand in that vector's order. CB entries
preserve FormID/word order, but failed resolution/category/activation gates can
change the usable traversal. Manager handles index/generation-check a current
reference. Pointer sets implement identity membership/result union, not an
explicit pointer-address consumer-priority sort. Different allocator addresses
or handle numbers alone therefore do not prove a different assessment sequence.

`14066f880`, `1418c7270` and `1418c7550` can execute immediately on the designated
thread or create engine service commands on other threads. Workers resolve the
then-current references and state, rather than reading an atomic historical save
snapshot. `1421efb30` reacts to PowerGenerated changes; `1421f01f0` and
`1421eff10` route reference/open-close state changes through these workers.
Initialization of switch animations uses the previously mapped load/default
mechanism, so settled switch state and own powered state remain distinct.
Fuel/AV/activation changes are possible later writers, not evidence that this
particular baseline has changing generation. No scheduler variation or outcome
variation was measured here.

### Real saved examples and coverage

The unchanged prior receipts retain actual HIST-0036 and HIST-0077 eight-node
trees, exact identities and Extra9C locators. HIST-0036 `ff01a9f1` and lever
`ff01a9f5` have historical flags `800` (powered `40` clear); HIST-0077 has its
separately resolved counterparts. Those observations establish neither a
shortage nor what a later load will write. Existing fixtures parameterize roots
and predicates; they are not repeated identical-save loads.

The bounded nominal screen reuses all six P1 graph receipts. The four complete
word-3 forests cover 17/15/17/14 components respectively; **none has nominal
base demand exceeding nominal base generation**. The word-1 subsets have external beacon edges or incomplete adjacency coverage.
In particular HIST-0193 `ff0253b2` and `ff0253b3` are isolated, boundary-zero
rows with apparent deficits, but their Extra views stop at unsupported type
`04` before CB. Their absent decoded CB is a coverage gap, not proof of an
unconnected closed component. The reproducible screen records these separately. This screen cannot certify actual surplus: current contribution,
switching and other gates were not measured. It does establish why this corpus
does not supply a verified deficient, stable, repeated-load experiment simply
by relabelling its saved off bits. No additional save decoding or power
calculator was undertaken.

## C: competing models and discriminators

| Model | Evidence tested | Disposition and precise falsifier |
|---|---|---|
| H1 deterministic recomputation | Ordered saved list/CB restoration and fixed-input traversal; load-reachable per-object callback | Compatible, **not established globally**. Needs exhaustive stable terminal roots/inputs or proven convergence. A matched settled outcome difference from one unchanged baseline falsifies necessary repeatability within those controlled conditions. |
| H2 deterministic restoration | Modern Extra9C restoration retains 40; no reset in that loader; later native allocations exist | Restoration is established as an intermediate. Universal "saved bits are always final" is unsupported. A witnessed post-load applicable bit change falsifies that strict model; identical final bits alone do not distinguish restoration from recomputation to the same set. |
| H3 order differs but outcome unchanged | Owner-refresh union is invariant under root-list permutation for fixed per-root results; no deficit in sampled nominal closed forests | **Supported for that algebraic subcase**, not all load/event sequences or deficient graphs. A demonstrated varying final consumer assessment with material threshold impact and no superseding convergence defeats its broader version. |
| H4 reload outcomes genuinely vary | Event-dependent roots, conditional resolution and queued paths are real; no coherent repeated-load final-state observations | **NOT ESTABLISHED.** A reachable varying final schedule plus material consumer impact, or controlled differing settled observations, is required. Failure to prove H1/H2 is not affirmative H4 evidence. |

Static evidence distinguishes restoration from the claim of a universal final
saved-bit authority, and identifies actual load-triggered recalculation. It does
not discriminate necessary deterministic settled outcomes from genuine reload
variation. The missing observation is the same identified consumers' settled
powered set across controlled independent loads, with stable supply/topology/
activation and coverage of later transitions. Static completion/order proof
could also close that gap; no impossibility of such proof is claimed.

## Saved versus runtime availability

| Input/result | Available now | Remaining requirement |
|---|---|---|
| Historical powered set | Decoded Extra9C 40 on positively identified saved records | Missing extras/unsupported records remain unknown; no current-state promotion |
| Topology/ownership/order | Saved CB FormID-word arrays and 4C keyword-target entries; native restored global list grammar | Matching definitions/defaults, dynamic remapping, all relevant members and global list contents for the particular baseline |
| One initialized pass | Native deterministic calculation for specified graph/root/setting/gates/effective AVs | Values at the invocation epoch; stable reference lifetimes/resolution; not an implemented production predictor |
| Settled powered set | **Not yet determined by a validated offline method** | Exhaustive effective load/attach/deferred sequence and convergence, or controlled current observations |
| Candidate runtime dependency | Current pending jobs/animation/reference residency are runtime state | Whether every relevant state is uniquely derivable from saved/definition/load context remains unproven; do not call it inherent nondeterminism |

Smallest sufficient candidate input contract: complete electrical/owner/default
relationships and historical flags; matched winning definitions and settings;
effective generation/demand and settled switch/validity gates; and either the
effective terminal event/root sequence or proof that all relevant sequences have
the same result. The first two are chiefly saved/definition data; the last two
currently need initialized-state evidence. Elapsed/fuel/crew context must be
held stable rather than silently replaced by base ratings or Workshop HUD totals.

## Minimal proposed validation, unperformed

Use one deliberately deficient outpost with equivalent identifiable demand
consumers, fixed wiring, closed settled switches and stable non-fueled generation.
Confirm effective available supply is below total demand under the observed
conditions. Preparation/construction and baseline save creation need a separate
approved card. Preserve the original baseline and SHA-256; each trial loads the
same unchanged bytes and matching plugin/settings/build context. Historical
off flags in this corpus are not a substitute for that admission condition.

Start with three independent fresh-process loads as a practical initial
comparison, recording the same consumer identities/locations. Make no build,
wire, switch, inventory or crew changes. Capture each consumer's actual powered
indicator using ordinary UI **only if it distinguishes the per-consumer bit**;
animation, realized output or aggregate supply/demand alone is not a valid proxy.
Record totals, connectivity, switch state, residency and elapsed observations.

An operational settled boundary requires all identified devices resident,
no visible pending load or switch transition, stable supply/demand/conditions,
and the same per-consumer set over three complete observation sweeps separated
by recorded engine-elapsed intervals (for example 10 seconds). Record an early
sweep too. If the set continues to change, retain those transitions and continue
until stable, operator stop or an actual safety/engineering failure; do not label the first stable frame a
native queue-drain proof. Revisit the set after the comparison sweep to detect
late changes. The card must distinguish UI access time, engine-elapsed time and
the measured operational criterion from a proven internal quiescence barrier.

If UI cannot identify power per consumer reliably, first assess an existing
qualified read-only getter facility for exact identities. If none meets that
criterion, propose separately reviewed narrow observation of the existing
IsPowered getter and relevant event epochs; any new injection/hook/breakpoint
instrumentation requires its own scientific/safety authority and may affect
execution. No instrument implementation or debugger branch follows here.

Two controlled differing settled sets falsify necessary same-outcome behavior
for that baseline and conditions; first exclude changing fuel/crew/residency/
switches and observation error. Three identical sets provide bounded repeatability
evidence, not a universal determinism proof and not proof of H1 rather than H2/H3.
Early differences that converge do not show different settled outcomes. A second
configuration is warranted only if the first cannot discriminate, such as every
consumer staying off or all admissible orders choosing the same set. No such
test, game load, observer build, save modification or new live authority occurred.

## Additional load branches and tooling record

The first cell-finish visitor `1405893c0` calls `140b5c350`. That method
tests reference flags and `140b58cf0`, then directly or through worker
`140b90250` invokes `140b979c0`, which dispatches a reference-bearing event
through a different source, `140b9a110` (L020-L022). This is retained as
another deferred notification edge, not silently equated to the FormID-based
TESObjectLoadedEvent source `140b9a340`. Its downstream contribution is not
qualified as a universal terminal power refresh. The positive Workshop
object-loaded allocation path above does not depend on that equivalence.

The unresolved-owner branch is consequential: `14187bb60` resolves a current
handle, calls `14187b5a0`, then conditionally `14187d800`. The first helper
performs relationship cleanup, emits an event, sets reference `+2c` mask `800`
and calls reference-manager operation `1428cce50` (whose exact semantics are
not qualified here); subsequent cleanup can be queued. This is
cleanup/retirement behavior, not evidence that a missing owner is repaired
before allocation. No such behavior was executed here.

The frozen local contract said "Existing owned Ghidra export tooling only."
One narrow deviation occurred: a new original `PowerLoadRtti.java` bounded
reader was executed read-only/noanalysis to export existing RTTI, rather than
using only the existing reader. It reads the specified vtable/COL/type/base
records (at most 64 bases and 1024 bytes per name), writes only ignored local
TSV, and does not modify symbols, types, comments, analysis or game state.
The broader authorized brief permits offline native investigation and owned
readers; nevertheless this narrower contract deviation is retained for
maintainer review, not retrospectively erased. All protected database files
are compared after shutdown. This supplies no authority for new live tooling.

## Assignment disposition

**COMPLETE** as a bounded offline investigation: the independent reviewer
accepted the exact review02 package against the original criteria. The
[review record](review.md) retains its actual return, integrity/regression
limits, narrow tooling exception and final disposition-only delta check.
Scientific settled-outcome equivalence remains **NOT YET ESTABLISHED**;
no live test, integration, publication, commit or push is implied.
