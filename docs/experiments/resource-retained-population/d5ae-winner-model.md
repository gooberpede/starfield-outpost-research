# D5AE winner model and B2 reconstruction

**The selector is a protected constructing miss, conditioned on actual source
eligibility and readiness.** [Causality](d5ae-scheduler-causality.md),
[readiness](d5ae-eligibility-readiness-map.md), [sources](d5ae-sources.csv).
All native VAs use image base `0x140000000`, build 1.16.244.0.

## Selection contract

Inputs are current owner/descriptor/Grid/source allocation and token, map and
visited state, effective definitions/raster/PCM preparation, pending request
keys, dependency/node state, service/pool queues, workers and their progress.
For a stable live source and successful holder/map allocation:

```text
Form requests only where ingress/context/focus/region predicates admit them.
Reuse warm handles; activate new tasks only when their readiness predicates hold.
Dispatch/claim according to actual pool and worker state; validate discriminator.
Reuse a populated aggregate, otherwise select actual Grid contributors.
For each eligible source:
    take shared ProcGen protection; test source token; release shared protection
    if visited: bypass this construction path
    take exclusive ProcGen protection
    look up the full source pointer in this owner's map
    if hit: retain existing holder; skip generator and visited append
    if miss:
        allocate/insert holder
        convert original request using effective manager descriptor
        invoke generator, including metadata/raster/definition guards
        attempt visited reserve; store token only if reserve succeeds
    release exclusive protection
```

There is no second visited test after exclusive acquisition. A request which
passed before another stores can therefore hit the map even after visitation.
Insertion and generation return do not certify nonempty geometry. Source tokens,
pointer map keys and geographic identities are different domains.

The firstness supported here is the first constructing miss within defined
owner/source state. A request can be first to register, claim, select or test
visited and still lose. A prepopulated map, aggregate or visited token can mean
there is no construction winner for the new demand at all.

## Actual B2 pair

These are independently redecoded retained fields, not simulated times. Native
QPC frequency is 10,000,000 ticks per second. Admission sequence does not itself
give a total causal clock; all listed QPC comparisons are checked directly.

| Sequence | Invocation/query | Native QPC | Supported event |
|---:|---|---:|---|
| 8004 | 3837, `[4,-1]` | 3761445485639 | Provider entry, thread 42984. |
| 8006 | 3837/3838 | 3761445485668 | Target unvisited. |
| 8018 | 3844, `[5,0]` | 3761445496317 | Provider entry, thread 44268. |
| 8020 | 3844/3845 | 3761445496360 | Same target unvisited. |
| 8091 | 3844/3845 | 3761445560087 | Protected miss: result/capacity 64/64. |
| 8094 | 3844/3845 | 3761445560191 | Direct ordinary sample `0x3`. |
| 8104 | 3844/3845 | 3761445576022 | Generator return. |
| 8105 | 3844/3845 | 3761445576037 | Reserve index 21, count 21 to 22, capacity 32. |
| 8106 | 3844/3845 | 3761445576040 | Matching token stored at base plus 21 eight-byte slots. |
| 8339 | 3837/3838 | 3761445739159 | Protected map hit, slot 18/capacity 64. |

Both share the ProcGen owner and geographic-source allocation 932, identity `0:37536:20928:0029d20e`,
epoch 207 and the same full runtime pointer key. Birth/publication 2074/2075
precede both. No intervening retirement/replacement or reset is observed.
The full operands and frame offsets stay local in `controls03/controls.json`
and `.local-work/d5ac/d5ae-reconstruction01/target.json`.

The native exclusive interval spans lookup `0x14079fccb`, insertion
`0x14079fdf9`, generator `0x14079ff18`, reserve/store `0x14079ff3e/ff60`
and unlock `0x14079ffa5`. Thus 3844's required insertion and construction
precede 3837's hit. Neither OS scheduling instants nor lock-wait durations were
captured. Check-to-lookup elapsed time cannot be relabelled lock-wait time.
This explanation identifies the actual deciding operation and result without
inventing a cause for the OS's worker progress.

## Independent counterexamples and failure boundaries

The [D5S native continuations](d5s-query-winner-model.md) share one ordinary
initialization prefix yet construct from `(10,11)`/mask 3 or `(-2,-2)`/mask 0.
Earlier dequeues do not select the target, and other source tokens do not
collide in that controlled contract. The new replay reproduces the original
queue controls, generation discriminator and retirement series. The D5W
incremental replay also gives owner `(-2,-2)` at batch 875, rejecting a permanent
owner-to-mask-3 mapping.

Grid clear/retirement can erase a holder while retaining visited; broad ProcGen
reset clears both. A newly allocated pointer with an equal token need not be
eligible. A different owner has separate stores. Genuine same-source reuse
requires continued allocation/owner identity, not pointer equality after free.
Failed visited reserve allows later map reuse without a token. A normally
returned unsuccessful generator still reaches the append attempt. Holder
allocation failure is **not** modelled as safe recovery: the provider's
null-holder branch can proceed toward `RBX+0x08` without a positive guard.
Inner geometry allocation failure and successful/nonempty output are separate.

D5S also demonstrates a detached-density source-lifetime gap during movement.
The selection-to-dereference interval can outlive source retirement despite
Grid retention. The model requires valid source lifetime and does not assign
a well-defined winner to invalid dereferences or fabricate a retail crash rate.

The model is falsified by an ordinary same-owner map hit without a prior holder,
generation on a protected hit, a second visited recheck before map lookup on
this exact path, or a required source-coordinate priority/barrier invalidating
the paired native continuations. Identity drift, omitted mutators and different
builds require revalidation rather than silent transfer of this contract.
