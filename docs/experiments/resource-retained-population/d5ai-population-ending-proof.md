# D5AI baseline population ending proof

## Bounded offline experiment contract

Question: after a complete native baseline positively witnesses a holder and
all its resource collections, which observed native endings or mutations can
distinguish retained external storage from final release after map removal?
This is separate from whether the ordinary query currently exposes that data.

Allowed actions are reading retained native exports and existing owned methods,
exporting named dependency functions only from the independently reverified
disposable Ghidra copy in read-only/no-analysis mode, and executing pinned
original instruction slices on explicitly owned disposable host allocations.
Inputs are the pinned 1.16.244.0 PE, existing local source receipts and owned
fixture objects. Outputs are this source-indexed proof, authored methods and
fresh ignored receipts. No game process, save, original analysis project,
deployment, network or installed file is changed.

Risks are host mapping conflict, incorrect fixture ABI/object invariants and
host faults. STOP on pin, disk floor, mapping, callback, assertion or unexpected
fault; preserve failed receipts and allow the disposable host to exit. Both
drives retain the standing 40,000,000,000-byte free floor. Owned buffers remain
allocated by the fixture even when a recording-free callback observes a native
release. Cleanup is process exit; no game cleanup is needed. These native
controls do not claim retail occurrence, thread scheduling or a native lease
on an object after the observed reader interval.

## Receiver correction

`0x1407aa8a0` clears the **outer ProcGen pointer map**, with receiver
ProcGen+0x10. Final holder references call `0x1407aab10` at
`0x1407aa8ec`, passing holder+0x10. Therefore the proposed interpretation of
`aa8a0` as a holder resource-map clear is incorrect.

`0x1407aab10` is the holder's resource-map teardown, receiver holder+0x10;
its final collection release calls `0x1407ac260` at `0x1407aab66`, passing
collection+0x08. When region backing is nonnull, `ac260` frees constituent
point allocations, then the region array, and zeros the vector state before
returning. Valid empty/null vectors already have no nested backing to free.
Baseline holder
and collection addresses must remain distinct witness types.

## Ending coverage at the ordinary typed graph

The [ending sources](d5ai-population-ending-sources.csv) bind full bodies and
their exact local SHA256/line ranges. Existing `audit03.json` authenticates
the data-reference dispositions: the only non-code references to `aab10` and
`ac260` are their `.pdata` runtime-function entries. No unexplained callback
table reference is counted as a direct-only caller proof.

All ten existing direct calls to `aab10` pass the just-decremented holder+0x10:

| Caller / final-reference sites | Receiver and ordering |
| --- | --- |
| Provider `14079f860`: `14079fe6d`, `14079ff82` | Atomic old-reference count equal to 1; teardown, then sentinel and 0x40 outer free. |
| Outer map collision/move `1407ab510`: `1407ab62a` | Final reference of displaced holder; teardown precedes 0x40 free. |
| Outer map rehash `1407abaf0`: `1407abc3a` | Same typed final-reference cleanup. Moving a still-owned pointer is separate. |
| Outer erase `140975030`: `1409750f7`, `140975142` | Final reference of removed/displaced holder; both erase branches covered. |
| Slot cleanup `1407ab6a0`: `1407ab6d7` | Final holder reference; slot nulling does not itself mean collection destruction. |
| Outer map clear `1407aa8a0`: `1407aa8ec` | Final holder reference per occupied slot. |
| Retained holder consumer `1407a5790`: `1407a59cc` | Atomic old reference minus 1 is zero; +0x10 teardown precedes outer free. |
| Holder reference cleanup `1407a9690`: `1407a96be` | Atomic old reference equal to 1; +0x10 teardown precedes outer free. |

All eleven existing direct calls to `ac260` similarly pass collection+0x08
after an atomic old reference count equal to 1: point consumer `1407b0145`;
builder temporaries `14079acc5`, `14079ad0a`; holder teardown `1407aab66`;
reference replacement `1407aac1a`; resource-map collision `1407ab849`;
resource-map rehash `1407abe27`; resource sampling `1407af3f0`; consumers
`1407a5711`, `1407a60d5`; reference cleanup `1407a98de`. Each calls the
geometry teardown before setting the outer reference sentinel and freeing the
0x18 collection. These are positive typed argument and control-flow traces,
not matches to a global allocation size or offset.

The caller can fail or be interrupted after the teardown returns and before
its outer free. Therefore journal events attest **holder resource-map ending**
or **collection geometry ending**, not physical outer-object deallocation.
An entry event occurs before the first mutation/free and irrevocably ends the
baseline content identity. Exit confirms that this body returned; missing exit
leaves an interrupted interval, never evidence that old content survived.

## Mutation and backing-allocation coverage

The ordinary writer chain is the previously closed
`14079f860 → 14079b520 → 14079c470 → 14079a330 → 1407ac2f0`.
The provider constructs into a newly inserted holder on a protected miss;
the hit branch retains the existing holder and does not call generation.
Existing `d5ai-source-lifecycle-map.md` and OWN-01–09 supply those operands.
The first complete consumer baseline is after that synchronous writer interval
under the ProcGen reader; same-thread exclusive recursion is refused.

`1407ac2f0` appends to collection+0x08 and owns the region-vector reserve
operation `1407ac32a`. It may move/free old region backing during construction.
Its sole ordinary direct caller is `14079aced`. The sole direct point-copy
caller is `1407ac39d → 1407ac0d0`; it copies into that new region's +0x18
point vector. Point reserve at `1407ac18a` and append at `1407ac207` may
replace point backing during construction, while shrink `1407ac156` changes
the destination's represented count. These are within the same construction
operation, not independently retained point aliases.

Resource slot pointer replacement and resource-map rehash/collision move
collection references; surviving nested region/point allocations are not
rewritten. Final displaced references still pass through `ac260`, as above.
The extra ending callers consume geometry into independent outputs: for
example `1407a59f0` reads collection/region/point operands into stack vectors
and calls `140974bc0` with independent output; `1407af1a0` builds stack
sampling operands before its retained collection release. Their writes do not
target the borrowed baseline region/point buffers.

Thus no post-publication nested realloc/clear writer remains in the examined
ordinary receiver graph outside the ending boundary. This uses typed native
immutability, not continued readability or equal pointer values. It is not a
global heap or arbitrary computed-call census. A defensive mutation journal
can additionally observe `ac2f0` with collection=RCX−8 and resource insertion
`aa9b0` with holder=RCX−0x10; a matching baseline mutation must invalidate
unchanged-content continuity rather than being called a physical free.

## Baseline-to-query predicates

Start only from a positively qualified complete baseline containing the actual
holder, every resource collection and complete nested content. Record no later
borrowed dereference of those old objects. Maintain an exact versioned journal
from that baseline through the completed query, with loss/fault/sequence and
active-interval accounting independent of the core source epoch.

* Holder-map continuity: no matching holder resource-map entry event.
* Per-collection geometry continuity: no matching collection geometry entry
  event, and no matching content mutation. This is prior region/point-storage
  continuity under the native immutability premise, not an observed refcount.
* All prior constituent geometry: every baseline collection satisfies that
  predicate. A proper subset is PARTIAL; it cannot stand for the whole old
  population. Holder ending can coexist with all prior collections retained
  by external references.
* Empty collection: its empty vector/content lifetime was witnessed, but no
  nested allocation is inferred merely from its existence. Allocated spare
  region backing remains an allocation even with zero represented regions;
  the actual baseline pointer/capacity distinguishes that case. A baseline with zero collections has no
  constituent geometry to prove externally owned; do not infer external-owner
  survival from a vacuous all-collections check.

Any relevant beginning event invalidates the old identity even if the same
address is subsequently reused with equal bytes. No allocation-birth hook is
needed to retain an already positive baseline identity when every ending is
covered; absence of a baseline, lost history, unmatched intervals, failed bridge
installation or an unobserved start refuses the continuity conclusion. A
complete current query establishes present exposure independently. An empty
current map may coexist with all old constituent storage surviving elsewhere.

## Native controls and limits

`d5ai_population_ending_native.py` executes original map erase, slot release,
reference replacement, point scan, holder teardown and collection teardown on
owned fixture buffers. Two owned entry probes call copied original teardown
bodies with explicit direct-call relocation; the bodies have no RIP-relative
data operands. They record typed begin/end, while recording-free callbacks
retain all actual fixture backing. This is not the production hook bridge.

Final-source `ending-native02.json` and `ending-native03.json` repeat seven
native release/storage controls plus one explicitly labeled owned admission
oracle: external holder survival then final release; external collection
survival then final release; partial constituent survival; empty collection
ending; same-address reinitialization after a real native ending; and
lost/unmatched-history refusal. The last refusal is an owned admission check,
not a native transport workload. Original native control 01 is retained.
These validate the receiver/end distinction and adverse objects; exact final
production journal transport, bridges, overlap ordering and reducer remain
independent qualification obligations.
