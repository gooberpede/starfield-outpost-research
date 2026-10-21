# Saved/runtime correspondence and real local edges

[Report](report.md), [finite rereader](../../../research/s2-links/saved_examples.py).
Offsets are decimal decoded logical save-stream offsets, never compressed-file
offsets or native VAs. `ff...` below abbreviates save-era `DYNAMIC:ff...` identity;
base/item/resource identifiers explicitly name the main ESM domain.

HIST-0036 original SHA-256:
`7e6642f49774c9827fe5230f8cdccdff6b00e4af8738dac11018b56e7ffeca37`.
Decoded SHA-256:
`6f47ac5a129fecef2a6323994478372a85ee975a1a582343de379c47a9bf2184`.
Fresh `.local-work/s2-links/saved01.json` redecodes this protected original,
reproduces all 246 edges in the unique qualified envelope at 1913537, and rereads
18 fixed endpoint records through separate reference prefix/counted extras and
inventory grammar. Nine selected edges have matching explicit Workshop owner
joins. Producer rows are independently joined through beacon ExtraBC, not guessed
from a container's display name or item count. All selected inventories equal
the accepted S1 originals' receipts. No historical transition is inferred.

| Actual saved edge/source -> destination | Bases, main ESM | Inventory snapshots / support |
|---|---|---|
| ff02a281 and ff030376 -> ff02a29b -> ff02a2c7 | Europium harvesters -> small solid -> cargo outgoing | Both producer buffers, store and outgoing child have explicit zero item counts. This is a real merge and chain, not absence of production or a measured transfer. Common owner ff02a13e. |
| ff05632f -> ff018b62 | Chlorosilanes harvester -> small liquid | MISC00557e x10 at source, x125 at destination; separately decoded counts, common owner ff04ba51. Fullness cannot be inferred from stock count alone. |
| ff0288d7 -> ff031075 | Medium He-3 harvester20a07c -> small gas273199 | He-3 MISC00558e x15 and x150; common owner ff01bc4d. Producer row3154079 joins IRES0057f5 and same source/base. |
| ff01aa14 -> ff01aa4d | Cargo incoming219173 -> small liquid2c5913 | Caesium MISC0057df x374 and x93; common owner in receipt. Near-full target under S1 fallback mass .8/C75; no attribution to shipment or reverse flow. |
| ff0514e1 and ff050aae -> ff038416 | Two small solid stores -> Zero Wire fabricator | First source Copper MISC005576 x125; second explicit empty; fabricator explicit empty. These are ingredient-source relationships, not evidence the builder physically stores all inputs. |
| ff028cfd -> ff028cbd | Small liquid -> greenhouse2965f7 | Water005591 x150 upstream; organic product0055a6 x8 at facility; owner ff028c1c and registered IRES077826 at 3612143. No measured consumption. |

Additional selected witnesses preserve S1's full/over-nominal cases: ff018b64
Lithium00557f x150, definition-fallback C75/W75; ff02c339 mixed warehouse246b77
x41 and246b73 x3, C75/W85.79999542236328; ff0382cf fabricator3a8619 contains
203eb2 x4. They are selected inventory/producer joins, not newly claimed link
transitions. Exact record/inventory offsets and signed stack quantities remain
in saved01 and [S1's table](../storage/capacity-examples.csv).

| Mechanism/object state | Persisted representation | Native reader/writer and loaded use | Authority/limitation |
|---|---|---|---|
| Local directed edges | Destination reference followed by counted incoming source references in global transfer envelope | `140f7e6f0` / `140f7ea10` rebuild destination-keyed handle sets | PERSISTED identity, RECONSTRUCTED handles; saved enumeration order is not durable routing priority |
| Workshop association | Extra4C key054ba6 -> explicit Workshop reference | `140517d60` owner lookup; saved_examples rereads owners independently of graph | Separate from link ownership and electrical membership; selected positive joins only |
| Storage/cargo/producer contents | REFR mask08000020 inventory tail, item identity, compact stack count, per-stack extras and signed quantity | `1406447c0/1406448b0`, `140641180/140641320`, `140642a00` | PERSISTED stock; nonempty stack extras unsupported here, unknown rather than empty; original snapshot not current settled stock |
| Capacity, filters, mass | Main-ESM PRPS/ONAM/MISC DATA plus saved AV providers where present | Effective getter+70, `140b69760`, `140f84020` | DEFINITION-DERIVED/MIXED, effective runtime overrides can differ; weight cache TRANSIENT |
| Extractor/builder selected production | Resource-keyed ExtraBC rows; independent ExtraBF selection/preset channel | `140f50660 -> 140f515a0` writes; `140f50880` restores; current reason/AV rechecked | Saved handle/base identities remapped, not pointer identity; E1-E3 recipes/arithmetic retained |
| Producer pending/countdown | Wire body i32 pending, i32 iterations, u8 cached eligibility, f32 remaining, f32 interval (17 bytes) after reference/base; runtime row1c uses +08/+0c/+18/+10/+14 | Fresh n11 writer/loader; `140f7f1e0` and `140f8c580` | PERSISTED bookkeeping; pending is neither inventory nor guaranteed eventual debt; wire order differs from runtime offset order |
| Registered Workshops | Global saver writes registered references separately from graph; loader remaps them | `140f7ee40`, `140f83020`, `140f7ef20`, global save/load | PERSISTED selection, reconstructed current-handle set; missing whole Workshop skips timer updates |
| Ordered reachable candidate vector | Derived forward-cache vectors keyed by source handle | `140f82820/140f82c30`; queued `140f82160` rebuild | RECONSTRUCTED; no matching stable vector serialization in the inspected global writer |
| Ordinary transfer descriptors | Per-call vector of source item requests and receiver pointers | `140f84fc0`, execution `140f84d70` | TRANSIENT; not written by the mapped graph or inventory savers; save snapshots do not describe a partially executed transfer call |
| Full-reason set / rebuild command | Runtime manager set and queued cache command | `140f7f1e0`, ContainerChanged sink, `140f87f00` | Runtime bookkeeping/rebuild; not a saved conveyor work queue in these serializers |

Native row saver writes the eligibility byte **before** the two timer floats;
it is not a memcpy of runtime fields. Fresh save examples can contain cached
eligibility false while retaining stock and registration. Do not relabel that
byte as an enabled flag or infer inactivity from an empty own buffer.

H36 uses the accepted supported header/inline-base/empty-stack-extra subset.
HIST-0077/0083 and mature Save52 remain independently pinned S1 examples; this
task does not pretend to freshly decode all their inventories. Unsupported
representations, Transfer Container/husbandry saved-instance gaps and current
loaded restoration remain explicitly unknown. A save describes stock, graph and
qualified production timing fields, not the invocation chronology needed to
reproduce all outstanding local effects or predict universal settled inventories.
