# Saved fuel sources and decision-input correspondence

[Answer](report.md), [native decisions](native.md),
[C2 endpoint/ship corroboration](../transport/saves.md).
Offsets here are decimal decoded logical-stream offsets, not compressed-file
offsets, native addresses or live handles. `ff` identities are save-era resolved
FormIDs within this sample; token/definition/live identity domains remain distinct.

Protected Save52 is 16,411,136 bytes, SHA-256
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.
Fresh `save01.json` rereads 205,557 framed R3 records and the 246-edge local
resource-transfer envelope at 1,860,043. Payload spans 1,860,051–1,861,639;
SHA-256 `37a4fec9c010c33678d4e15f7de772aa26d0d501a4be0cb61a783a0a0bdc4f36`.
The existing C2 selection is extended only to transitive upstream fuel sources,
giving 944 inspected records. Existing strict readers decode supported extras,
inventories, explicit owner links and producer groups. Unsupported tails stay
unknown; this is neither a complete VM decoder nor an exhaustive cargo census.

## Two independently grounded routes

| Saved role | Schrod II ↔ Feynman V | Carinae III-a ↔ Feynman IX |
|---|---|---|
| Shared fueled ship | `ff01c5b7`, GBFM `219042`, record 2,276,744; Ionic Liquids `00557a` ×7 at inventory 2,277,095 | `ff047b8b`, GBFM `219042`, record 2,436,024; Lithium `00557f` ×3 at inventory 2,436,372 |
| Pad 01 / owner | `ff0217b5` at 3,256,198 / beacon `ff04ff81` | `ff020ce1` at 3,212,896 / beacon `ff02be17` |
| Pad 02 / owner | `ff04fad9` at 5,783,291 / beacon `ff03388f` | `ff02b86b` at 3,732,122 / beacon `ff02a0c0` |
| Both pad definitions | ACTI `219523`; reciprocal LinkActive `255cc8`, both LinkShip `255cc7` resolve to the shared ship | Same independently checked base/relationship pattern |
| Incoming / outgoing 01 | `ff0217c8` / `ff0217bf` | Explicit ship/pad role-key correspondence retained in save01.json |
| Incoming / outgoing 02 | `ff04faec` / `ff04fae3` | Explicit ship/pad role-key correspondence retained in save01.json |
| Saved selected target | Current `255cc3 → ff0217b4`, endpoint 01 landing marker | Current → `ff02b86a`, endpoint 02; explicit destination AV `2457af = 1` |
| Incoming fuel graph at 01 | No incoming edge in the fully parsed serialized envelope for `ff0217b5` | No incoming edge there for `ff020ce1` |
| Incoming fuel graph at 02 | `ff0428f5 → ff04fb23 → ff04fad9` | `ff036b0f → ff050483`, `ff036b11 → ff050483`, `ff050483 → ff02b86b` |

Owner/body names reuse the independently grounded mature beacon table, followed
by freshly reread explicit marker owner and role links. The direction selection
does not prove a physically docked ship or a timestamped departure. Absence of
an incoming serialized edge at pad 01 is scoped to this envelope; it is not
proof of historical inactivity, missing defaults or universal absence of supply.

The Schrod/Feynman route's intermediate gas store `ff04fb23`, CONT `273199`,
has **one He-3** item `00558e`, count bytes at 5,801,989. Its record begins
5,801,887; inventory 5,801,987–5,801,999 closes under the empty-stack-extra subset.
Upstream incoming cargo container `ff0428f5`, CONT `219173`, has **499 Alkanes**
`005576`, count at 5,094,135. The source graph and native IRES→product resolution
therefore demonstrate a physical fuel source and an unrelated ingredient stock;
the 499 Alkanes cannot be counted as He-3. One He-3 cannot pay a five-unit cycle.
It does not establish whether either pad's complete current predicate passed.

For Carinae/Feynman, gas store `ff050483`, CONT `273199`, record 5,873,590,
contains **150 He-3**, count at 5,873,692. Two explicitly connected extractor
references `ff036b0f` and `ff036b11`, base CONT `20a07c`, have **15 He-3 each**,
count offsets 4,567,639 and 4,568,153. Thus this saved transitive subset holds
180 He-3 across three source inventories. The native input graph can draw from
the extractors without first putting those units into the gas store or marker.
Current accessibility/eligibility after load remains separate from these counts.

## Producer and state joins

Every selected pad is explicitly registered under resource IRES `21e6ff` with
its own beacon owner. The serialized row payload is `i32 pending`, `i32 iteration
quantity`, `u8 cached eligibility`, `f32 remaining`, `f32 interval`; it is 17
bytes after the queued reference/base identities. Runtime row stride is 1c and
its field order differs. This distinction prevents a cached eligibility byte
from being misread as countdown or fuel charge.

| Pad | Owner / row offset | Pending / iterations / cached eligibility | Remaining / interval |
|---|---|---|---|
| `ff0217b5` | `ff04ff81` / 5,811,894 | 0 / 1 / 0 | 30.271221160888672 / 102.5999984741211 |
| `ff04fad9` | `ff03388f` / 4,440,860 | 0 / 1 / 1 | Same sampled pair |
| `ff020ce1` | `ff02be17` / 3,760,441 | 0 / 1 / 0 | Same sampled pair |
| `ff02b86b` | `ff02a0c0` / 3,616,939 | 0 / 1 / 0 | Same sampled pair |

Both supply extractors also join resource `0057f5` under beacon `ff02a0c0`,
producer rows at 3,616,977 and 3,616,994. These positive instance joins corroborate
definition, registry and stock roles. The pad interval is compatible with a .95
modifier on 108; it does not prove its historical modifier source. Cached
eligibility 0 coexisting with 180 units is retained, not rewritten as a failed
fuel model. The updater and stock snapshot need not share an evaluation epoch.

The marker inventories have `NO_INVENTORY_CHANGE_BRANCH`; this is not a decoded
empty physical tank. ExtraBF positively records AV `000338 = 1` at 5,783,442
on `ff04fad9` and `000338 = 2` at 3,732,273 on `ff02b86b`. The other two pads
have no explicit `000338` override in their closed ExtraBF subsets. The
[constructor/helper binding](native.md#actual-causal-chain) identifies `000338`
as WorkshopProduceUntilNextCycle: the first saved value is uncharged, the second
charged. Their omission at the other pads does not establish a zero value;
the installed ACTI explicitly supplies uncharged base value 1 under ordinary
restoration, with effective modifiers/restoration still separate inputs. These qualified
saved charges are historical rather than present-time authority.

| Native decision input | Persisted correspondence | Coverage / unsupported portion |
|---|---|---|
| Source inventories and He-3 recipe product | Explicit item identities/count offsets above; native inventory save/load reused from S1/C2 | Positive supported stack subset, not all polymorphic extra-node cases |
| Incoming ingredient graph | Full scoped envelope and explicit source/destination identities | Runtime handle map/cache is reconstructed; no post-load current reachability sampled |
| Endpoint, children and shared ship | Both marker owner/peer/ship links and ship endpoint/bay/landing keys | Three-dimensional residency and actual travel completion unobserved |
| Resource choice and producer countdown | Four resource-group/owner/base joins plus two source extractors | Saved cached eligibility/countdown differs from current reason and restored effective interval |
| Fuel charge and current reasons | Native charge getter/setter and numeric AV binding plus saved explicit AV rows above | Historical uncharged/charged instances are joined; active halt/charge/power/effective getters not evaluated live |
| RequiresFuel, cached waits and initializer guard | Installed mutable ship script/default definitions and C2 VM persistence route | Specific Save52 VM object/property join unqualified; no fabricated default-restored value |
| Pending freight timer and script identity | C2 native remaining-time/ID/handle/pause serializer and loader | Particular Save52 timer ID, bound VM object, overdue state and event queue not decoded |
| Hold and direction | Qualified stocked ships and explicit selected target | No origin manifest, chronological voyage, consumed-fuel delta or exact physical phase inferred |

The missing instance VM/timer and exact historical charge epochs do not block
the ordinary native fuel explanation. Recovering them would require a broader
VM/save join, but could not reconstruct an unrecorded historical withdrawal
sequence from these snapshots alone. No generic extractor or live experiment
is proportionate merely to turn those incidental historical unknowns into counts.
