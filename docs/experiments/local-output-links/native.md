# Native contracts, direction and dispatch

Reader notation: [vtable versus object offsets](../../reference/notation.md#native-prose-at-first-use);
[experiment-local export namespaces and lookup](../../reference/native-export-ids.md).
These guide the existing local address/offset declarations; they do not make
export labels global symbols or raw exports available in a checkout.

[Report](report.md), [function register](functions.csv), [lifecycle](lifecycle.md).
All VAs are preferred **static VAs**, base `0x140000000`; RVA = VA minus base.
Object offsets and strides here are hexadecimal. Build 1.16.244.0;
executable SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
main ESM `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Fresh baseline also pins stopped database and source originals. `nNN` denotes
`.local-work/recon/s2-links-NN.tsv`, through n13. Existing S1 `cNN` retains its
[capacity-source provenance](../storage/capacity-sources.csv).
Aliases are analyst names, OBSERVED-INTERNAL, no validated callable ABI.

## Directed identity and traversal

Fresh `140f81200` (n05/n11) and `140f81a90` (n11) corroborate E1's add/remove
contract: map `145916580`, lock `1459165d0`, destination handle -> incoming source
handle set. `140f80af0` (n11) scans occupied destination hash slots and finds the
source in their nested sets. There is no output-port keyword or item identity
stored as this edge. WorkshopItem Extra4C key `054ba6`, electrical ExtraCB,
cargo pairing and local movement are distinct channels.

`140f82c30` (n02) copies the cached handle vector at map `1459165d8`, lock
`145916618`, or calls `140f82820`. The latter seeds the vector with **self**, then
walks outgoing destinations from each appended node, suppressing handles already
in the vector. Appended destinations must resolve, have TESContainer capability,
and fail harvester (`140f7c9f0`), builder (`140f7cab0`) and fueled-input
(`140f7d030`) classifications. It appends/expands eligible stores, not arbitrary
producer/fuel nodes. This yields a finite visited traversal even if a graph
contains cycles; no item circulates hop by hop just because the traversal repeats
its loop. Invalid handles are marked sentinel in the local vector.

Fresh `140f84470` (n09/n10/n12) corroborates S1 pair policy. Topology helper
`140f843e0` calls `140f894c0` (n04/n11), whose incoming traversal deduplicates
resolved references and can stop on the queried target. Pair branches select
the traversal orientation and return reason `26` on its positive result.
This is a construction/topology gate, not proof that every conceivable cycle
is impossible. Cycle termination is independently supported by visited handles
in the actual forward traversal. Persisted hash slot order is not a stable
user creation-order list, and load reconstructs hashes/handles anew.

## Existing-stock planning and mutation

`140f84d70` (n01) gets that forward vector, locks source inventory +a0/+a8,
and visits materialized item rows (stride28) with `140f84fc0`. A missing materialized
inventory takes `140f8ccf0` (n06), which walks the base TESContainer rows into the
same visitor. Null inventory is not assumed empty. All descriptors are prepared
before the source lock is released and execution begins.

The item visitor (n01, n09 windows `140f85580..140f856bb`) copies candidate handles
for each item, obtains provider-aware mass, and filters through `140f89d00` /
`140f84c40`. Missing, already excluded, ONAM-incompatible or insufficient-one-unit
space references are excluded. It scans the retained vector **backwards**, skips
source/self and bounds a descriptor to min(remaining stack quantity, floor(F/w))
for ordinary finite positive w, F = binary32(C-W). Descriptor stride **40 hex =
64 decimal bytes**, requested quantity +1c, reason4 +20, receiver pointer +28.
Nonpositive-weight handling takes the separate whole-remaining branch after
filter admission. This is not a qualified contract for corrupt/extreme floats.

After planning, `140f84ede` invokes source virtual+458 for each descriptor.
Accepted [S1 mutation trace](../storage/capacity-native.md#local-output-link-redistribution-admission-and-execution)
grounds `140b66680 -> 140b67a30 -> 140b89690 -> 140b8f540 -> 140b67100`,
then source stack subtraction (`140b7c100`/`140b7bd20`), `140b67380` and
destination virtual+4d0 (`140b4ef90 -> 140b4cbc0 -> 140b64fc0`). Source shortage
bounds the actual removed quantity; that removed count is sent to destination.
The receiving TESContainer gate precedes ordinary add. This is a staged mutation
chain, not a transaction with rollback on every exception/capability failure.
No concurrent inventory race, exceptional loss or failure recovery is certified.
Virtual+488 is event emission, not the mutation result. Visitor return1 is continue.

Important counterexample: the cross-item exclusion set is updated when
`binary32(k*w + (C-W)) >= C` (`140f8567e..140f856ac`, n09 instructions).
This is the actual comparison, not `W+k*w >= C`. No weight reservation updates W
between planning different source item rows. Hence whole-call capacity safety
cannot be inferred from the per-item floor. [Worked traces](traces.md) show both
ordinary partial fit and a mixed-item overplanning prediction. S1's scoped
per-item result is preserved; this adds its missing batch context.

## Production delivery and input withdrawal

`140f7d510` (n03) starts with the producer if it is not already full, then scans
the same vector backwards. It selects the first resolved nonself ordinary
container passing `140f7d0b0`, ONAM item compatibility and W<C. If none qualifies,
it returns the producer fallback or null. This is a **single** receiver; it does
not distribute the production batch over all remaining capacities.

`140f7d6a0` (n03) gets this receiver before builder ingredient removal. E2/E3's
`140f7f6f0` caps cycles by available recipe inputs and builds upstream removal
rows via `140f881c0` (n11/n12). Sources' virtual+458 remove ingredients before
output insertion. Ordinary product creation uses `140b64fc0` at `140f7df8f`;
its original requested count can cross nominal capacity under S1's verified
mutation semantics. Leveled output/special early objects retain E1 exceptions.
Reason/event counts are not independent inventory-delta measurements.

An extractor with a full own buffer may pass production eligibility when a
reachable store is not full; `140f7d120` (n06/n10) checks the forward vector.
The final receiver selector still applies item compatibility. Empty compatible
space, cached eligibility and an actual successful production are distinct.
Fabricators/organics use the same receiver selection; missing input or no
receiver returns without a completed product. No automatic bulk flush of all
old source stock is implied by creating a new batch downstream.

## Actual movement triggers and scheduler boundary

The complete existing xrefs to `140f84d70` in n01/n09 list three code callers:

| Trigger | Positive path | Meaning |
|---|---|---|
| Qualified link add | `140f85760`, call `140f858ae` (n05/n11/n13) | Successful validation AND insertion AND destination acceptance by `140f7d0b0` gate movement. Seed source handle, collect additional upstream container sources via `140f8a020`, then redistribute each resolved selected source. |
| Script-facing operation | `142077ac0`, call `142077b58` (n02) | MoveContainerContentToUnfilledContainers binding; walks incoming sources (`140f881c0`), or falls back to self if empty, then calls ordinary mover for each selected source |
| Native command wrapper | `140c1f400`, call `140c1f44e` (n02) | Requires TESContainer capability and dispatches mover; not a periodic tick |

The link-add collector `140f8a020` (n13) looks up the current node's incoming set
in the destination-keyed map, resolves each source, and deduplicates discovered
references using a visited tree. It appends each newly reached source handle to
its traversal queue; only sources with a TESContainer component are appended to
the caller's movement vector. Noncontainer upstream nodes can therefore be
traversed without becoming a stock-movement invocation themselves. Starting from
the newly linked source, it collects upstream sources, not arbitrary downstream
receivers. The caller's seed plus this finite vector can invoke redistribution
more than once during one successful qualified link-add call. Each invocation
uses its own forward candidate vector and descriptors; it still moves downstream.
The destination gate means that adding a link to a builder/fuel consumer does
not automatically take this stock-flush branch. Existing recipe input access
remains separately supported. No inventory delta or timing was observed live.

The installed-source `OutpostContainerScript.psc` (prior S1 pin
`0342cf3ee0045b943a3870f6ac0a6c969255c9cd234e4289d655230cbfade3d5`)
uses player-origin add/remove and busy-state ContainerMenu close to request the
script operation. OnLoad registers menu/inventory events and OnUnload unregisters;
busy state suppresses those item callbacks. This is SOURCE-REPORTED development
source, not new PEX equivalence or measured event timing. It explains upstream
refilling requests without reversing transfer direction.

TESContainerChangedEvent -> `140f7e530` is **not** another stock-movement caller:
it checks the manager's full-reason set and C!=0/W<=C, clears the reason/entry.
`140f83120` / `140f83450` update eligibility and notifications, not stock.
Load's queued `140f87f00 -> 140f8b570 -> 140f82160` rebuilds forward caches and
signals event `145916620`; it does not redistribute inventories. These actual
dispatch paths support an event-driven ordinary mover, distinct from producer
elapsed scheduling. Existing xrefs bound this claim; untyped indirect engine/
compiled script call discovery is not universally exhaustive.

There is no fixed items-per-second contract here. Each explicit movement call
visits its source rows and finite destination vector, preparing multiple
descriptors; the script wrapper may process multiple upstream sources in one
invocation. The mover does not recursively invoke itself for each receiver.
Visited graph traversal and decreasing row/receiver loops bound ordinary work;
no fixed arbitrary stack quota was found in these paths. Long-run rates depend
on producer timing, input stocks, current eligibility, capacity, caller events
and runtime ordering. No fair-share, round-robin or continuous-time throughput
guarantee follows.
