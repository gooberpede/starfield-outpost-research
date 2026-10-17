# S1 capacity, occupied weight and receiving behavior

2026-10-17, Australia/Sydney. SOR-EXP-0042 / SOR-EV-0050 continuation.
[Frozen contract](capacity-contract.md), [native derivation](capacity-native.md),
[saved calculations](capacity-saves.md), [review package](capacity-review.md).
Authored synthesis REVIEW-REQUIRED; native/save payloads LOCAL-ONLY.

| Element | Result |
|---|---|
| Question | For an ordinary outpost container and incoming stack, what permits the item, how much fits and what does the receiving operation actually do? |
| Best-supported answer | Capacity is effective **CarryWeight**, in weight units. Occupied weight is derived from item weights and quantities and cached on the materialized reference inventory. Category admission and weight admission are separate. Local redistribution bounds a positive-weight transfer to whole units that fit. Production uses an already-full predicate before a generic add that retains the requested batch; generic add's excess return is **not a measured rejected quantity**. There is no universal all-or-nothing or partial-fit insertion rule across these callers. |
| Confidence | Proposed STRONG / STATIC + SAVE for ordinary positive-count MISC stacks, nonactor CONT references and finite positive capacity/weight. Exact saved counts and definition rereads are mechanical observations; actual instructions support the stated branch distinctions. Independent assignment disposition is in capacity-review.md. |
| Coverage | Pinned retail 1.16.244.0/main ESM; fresh native exports; four existing distinct historical S1 subsets; nine selected calculations, including dedicated stores, mixed warehouse, empty controls, cargo children and producer buffers. No universal save decoder, winning load-order merge or negative-count/modded-item semantics. |
| Evidence | capacity-native.md addresses/spans, capacity-examples.csv and local calculations03.json with 113 physically reread records; protected pre/post and validation/package receipts. |
| Limits | Saved contents at a definition-fallback boundary are established; actual historical/current effective full state is not measured. Runtime overrides, load-time application and other plugins can change effective capacity. Manual menu's captured item predicate remains S1's bounded unresolved interface. |
| Next step | Critical review and eventual S2 observation of matched source/destination operands and actual deltas; no live action or S2 execution follows here. |

For a particular store, first resolve the item and receiver, distinguish failed
resolution from zero contents, and run the caller's category predicate. Then get
effective capacity C, occupied weight W and the incoming item weight w. For the
supported local redistribution path, positive w and finite ordinary inputs give
free weight F = binary32(C − W). If F < w, that destination is excluded for the
item. Otherwise k = min(request, floor(binary32(F / w))) is passed to the actual
transfer path. Equality admits an exactly fitting unit. A store can therefore be
below its numerical capacity yet accept zero units of a particular heavy item.

For production, the already-full test is W >= C, independently of the candidate
unit's mass. A not-yet-full selected receiver can get an entire requested batch,
crossing C. The generic add path calculates a fit count but does not substitute
it for its mutation count. Saved over-nominal contents are consequently compatible
with the traced mechanism, but do not identify their historical writer or rule
out historical overrides. Never discard stock above C as corrupt solely on that
basis. Current link compatibility also does not prove historical contents were
admitted under current definitions.

## Receiving decisions and observable results

These are static contracts/predictions, not a live transfer experiment. Assume a
valid ordinary inventory and item, available source quantity, positive finite C/w,
and no concurrent mutation. S2 still owns scheduling and routing.

| Condition | Local redistribution | Production-selected receiver | Direct generic add |
|---|---|---|---|
| Enough weight for entire request | Transfer instruction carries the request | Sends requested batch | Mutates request; ordinary excess result 0 |
| Only k units fit, 0 < k < request | Transfer instruction carries k; remaining request may be considered elsewhere, outside this receiving contract | Selection only asks W < C, so may send entire batch | Mutates request; returns request − theoretical fit, not actual leftovers |
| W >= C, positive w | Item-specific admission excludes destination | Already-full predicate excludes it | No universal rejection: valid direct generic add can still mutate request and return the computed excess |
| W < C but free weight < w | Excluded for this item | Can still pass the precheck | Same direct-add distinction |
| Free weight, category mismatch | Excluded by per-item filter before transfer | Connected destination excluded by product filter | No ONAM check in the mapped ordinary generic path; separate callers can impose their own restrictions |
| Unresolvable reference / unsupported save bytes | Unavailable/unknown, not full or empty | No successful receiver established | No stock conclusion |

A return value of 1 from the redistribution item visitor means the visitor can
continue, not that one item moved or that the entire stack was accepted. The
wrapper performs concrete transfer descriptors, then refreshes inventory-related
presentation. Source availability/actual removal can still bound realized movement.
The menu path uses the fit count as its subsequent requested quantity (and has
separate predicates); forced/script calls must be classified by their actual
entry point rather than assumed to inherit ONAM or the menu policy.

## Runtime/save correspondence and S2 handoff

| Class / condition | Native owner and effective inputs | Admission / mutation | Saved fields and reconstruction | Potential divergence after load |
|---|---|---|---|---|
| Dedicated Solid/Liquid/Gas/Warehouse | CONT reference +a0 inventory; +70 effective CarryWeight interface; base 75/150/300 plus actual providers | ONAM item/keyword gate; local floor-fit descriptors; production/direct add distinguished above | REFR inventory-change mask 08000020; queued item identity, stack extras and signed quantity; ExtraBF AV sections; pinned base properties and item DATA | Winning definitions, reapplied modifiers/overrides and lifecycle transfers; loaded C/W unmeasured |
| Cargo incoming/outgoing child | Each child owns its own CONT inventory; ordinary template capacity 300 | Same receiver arithmetic, outgoing filter versus incoming null filter; local direction gates separate | Same inventory grammar, independent child/reference identities; actual saved empty/full-fallback examples | Cargo arrival/departure timing and restoration are S2, not inferred here |
| Producer buffer | Own CONT inventory; capacity depends on base (e.g. water atmosphere 10, small Iron 10) | Production precheck W >= C, then batch add; incoming link prohibition distinct | Product quantities and separate producer configuration persist; own buffer examples support same weight calculation | Production timing, active inputs and effective values after load |
| Empty serialized list | Same owner; positive decoded zero count | Compatible candidate may fit by F/w; category still applies | Explicit item count zero is persisted evidence for that list | Default contents/other change representations must be considered before an engine-wide emptiness claim |
| Unsupported/omitted inventory branch | Owner association may still be positive | No capacity/acceptance verdict | Unknown, never zero; omitted changes do not prove empty | Cannot distinguish without the missing representation |

Contents/counts and explicit AV overrides/modifiers are PERSISTED. Base capacity,
base item mass and filters are DEFINITION-DERIVED. Effective C is MIXED; cached W,
resolved references and calculated full/fit results are RECONSTRUCTED/TRANSIENT
in these paths. The mapped inventory serializer writes neither cached W nor a
dedicated full bit. This is not an assertion that no other subsystem ever stores
a capacity-related status. Producer reason/cached eligibility and presentation
state are separate consumers, not saved inventory authority.

For a qualified save-time reconstruction, decode all selected reference extras
and stack extras, resolve actual definitions and explicit AV provider state, then
state the remaining load-time assumptions. All nine examples have closed decoded
reference extras, empty stack extras, no ExtraE1 and no decoded CarryWeight BF
entry. That supports the stated ordinary fallback reconstruction, without
substituting zero for an unknown runtime modifier.

S2's minimum matched observation is: resolved source and destination identities;
operation/caller; requested item/quantity and source quantity; item predicate and
ONAM result; effective C and its relevant providers; W/cache validity; per-item w
and any instance provider; planned transfer count; actual source/destination
deltas; readiness/resolution result and loaded/time state. These distinguish
numerically full, insufficient room for one unit, partial acceptance, category
rejection, transient unavailability, explicit empty stock, missing reference and
undecodable evidence. A UI label or generic excess return alone cannot do so.

No gameplay, current live inventory measurement, writer, new save, installation,
network, staging, commit, push or publication occurred. Accepted S1 history remains
intact. General chests/displays, Shared Outpost Storage, Stored Resources
aggregation, cargo scheduling, routing, retries and production timing remain out
of this assignment.
