# Native contribution lifecycle and recovery

Reader notation: [vtable versus object offsets](../../audits/publication-readiness-b2/notation.md#native-prose-at-first-use);
[experiment-local export namespaces and lookup](../../audits/publication-readiness-b2/native-export-ids.md).
These guide the existing local address/offset declarations; they do not make
export labels global symbols or raw exports available in a checkout.

[Answer](report.md), [function locators](functions.csv), [source pins](sources.csv). `nNNN` is `.local-work/cr3-lifecycle/native/NNN.request.tsv`. All addresses are hexadecimal preferred static VAs for EXE1.16.244.0/SHA in the report; object offsets are hexadecimal. Aliases describe observed internals, not supported integration points. No native routine was invoked.

## Assignment to a real query

`1404076b0` (n022; CR1/CR2 original exports) checks/deduplicates the actor handle, removes its previous owner with `140407a10`, appends it to destination ExtraE2 and sets CrewAssignment through `140ba0d40`. Ordinary transfer removes old membership before later queries. `140407a10` removes duplicate matching handles recursively, conditionally removes type1 effects, clears the link and emits downstream notifications. Normal insertion does not promise coherent visibility across the entire transition to concurrent consumers; malformed/restored arrays do not inherit the ordinary deduplication proof.

CR1's installed compiled `SQ_CrewScript`/`OutpostBeaconScript` separate those operations from travel. Loaded actor/beacon paths can retain a pending CrewGoingToOutposts member; neither-loaded paths MoveTo with the locked-in companion exception. Beacon OnUnload rereads current assignment before moving pending actors. No native timing entry waits for that alias to report arrival. Recruitment/grants, available roster, current assignment and physical location are distinct.

Assignment refresh `140408bb0 → 14040a230 → 14040a9d0` (n022 and CR2 n001/n002) inspects crew-flagged selected-rank entries. Its ability branch requires **type1**, destination environment and competition checks; location context and queued effect work can postpone this branch. Removal `14040a360 → 1404094b0` reverses the destination ability path. CR2's A1/DB entries are **type2** and use the dispatcher instead. The ability branch supplies neither a universal strongest-only rule nor the activation clock for production timing.

`140f7ef20` gets each registered, resolved Workshop/ExtraBC and its E2. `140f7bd20` (n001) resolves each E2 handle through `1428ccc40`, calls actor virtual868 with false, reads effective Health and invokes `140c94060(A1, actor, producer-base-context, duration*)` only when the state predicate is false and Health>0. It evaluates the player afterward. It neither changes failed actor slots nor waits for actor arrival. DB `140f3dd50` (n022; CR2 n002) has the corresponding per-actor gate for generator power, without extra player dispatch.

`140c93cf0` (CR2 n001; fresh bucket probes n004/n017/n022) requires an actor identity and entry-point bounds, then virtualBA8. Main Actor vtable `144cb9248` has BA8=`141955350`, BB0=`141955400` (n022 data window). `141955350` requires actor+228, that process object's +8, bucket array +480 and a nonempty selected bucket under lock+478. `141935370` copies the active entries. The dispatcher builds condition context and applies environment/rank/condition-qualified operations. For ordinary outpost crew category2, CrewAssignment must resolve to the outpost environment; absence or ship context suppresses the entry. CR2's caveat about the first bucket entry selecting environment still applies to hypothetical mixed-category modded buckets.

Thus the ordinary model is **assignment plus current actor state plus active entries**, not a distance check and not identity alone. The actor's +228/+8 process storage is not its 3D pointer. Positive remote operation means the registered/resolvable Workshop and producer can reach a qualifying crew query without 3D/arrival tests; it does not mean every fully unloaded actor retains those buckets.

## Selected rank and load reconstruction

Normal rank mutation uses `141954810 → 1412b5c60 → 1418c4f00`. The service runs directly or queues `1418ccbd0`; `1418c50a0` resolves the actor and rejects deleted/invalid-state/form-identity cases before `140ca3910`. The latter removes entries matching old rank through virtual70 and registers selected new rank through virtual68. Entry vtable `144bd2870` maps these to `140ca1bd0/140ca1a20`. The registration routine allocates per-entry-point storage only when process+8 exists, then inserts type2 entries. Rank ownership is not itself bucket availability. Per-entry locking does not make a whole rank transition atomic.

**The actual actor finalization path is now traced:** `1419198a0` (n007, focused instructions n021 at 14191aa26..46) clears existing buckets via `1419f7b80` when storage exists, then calls Actor virtualBB0, resolved to `141955400`. That routine (n017) walks the effective base NPC's perk/rank array (+250 count/+258 data), sending old 0/new selected rank through `1418c4f00` with registration mode 4; it separately snapshots the actor's additional ranked list under +36c and replays those entries after unlocking. This is positive native reconstruction, not an assertion that saved wire pointers become active entries. The caller wrapper `141a4b590` (n022) reaches `1419198a0`; its vtable reference is Actor+E8, alongside the established Actor load reader. Complete global startup interleaving remains unqualified.

Base selected-rank lookup `141955080` (n001) searches base NPC rank rows first, then actor additional rows. Generic Extra2B's selected template part3 and the native NPC template copier `140cd77d0` therefore matter. `1405d4a00` builds a new NPC from the saved source/selected part context and invokes the part copier; the spell/perk override explicitly tests bit3 and copies rank rows, not an arbitrary ancestor union. CR1's `140cdfde0/1405366a0/140543370` and nested NPC `140cdf140` establish the saved branch; CR2 n020/n024 and fresh n002/n006 qualify part-specific reconstruction. See [actual instances](persistence.md).

The actor finalization sequence also calls `1412b62f0` to prune null entries from its three restored perk-state lists (n011); it is not the active-entry registration loop. Likewise `141955f80` marks other state and refreshes AVs; it is not an all-perks restoration oracle. These inspected alternatives remain distinct from the positively identified BB0 replay.

## Entry-storage loss and return

Process transitions `1418e17d0` (sets level 3) and `1418e2540` (sets level 2) explicitly destroy/free process+8 and set it null (n011), including its bucket owner. Destructor `1419f8f40` calls `1419f7b80`; the latter frees all 255 bucket arrays and nulls +480 under the process lock (n012/n018). `141936490` can destroy the full process and null actor+228. These paths establish a real indirect contribution-loss condition even though A1 does not inspect graphics. They do not establish that every remote assigned actor takes these transitions.

Conversely, setup/replacement paths `1418d8ea0` and `141948250` clear/replay nonplayer entries through BB0 after their own applicable state/setup checks (n021). The former skips this replay on the true dead predicate; the latter's relevant branch also checks it. Actor finalization has the explicit clear→replay order above. Recovery requires suitable process storage and successful registration; a later 3D setup path is a concrete re-registration opportunity, not proof that 3D was the timer's direct operand. No unconditional timer-side lazy bucket rebuild was found: the actual bucket test simply returns false when storage is absent.

This is sufficient to explain how a retained assignment/perk can temporarily supply no modifier, and how normal setup/load can restore it. Which transition an actual remote crew actor takes, and any crew-specific process-retention guarantee, remain UNKNOWN. That gap affects a blanket promise about all remote crew, not the traced per-query contract.

## Life state, absence and replacement

Main Actor virtual868 is `1418e4540` (n004/n005). It reads actor+F8 masked by1E0000. The timer/DB pass false and exclude **20000,40000,A0000,E0000**. Script IsDead's callback141fc7fb0 and GetDead condition callback140be51a0 pass true, which excludes20000,40000,A0000 but **does not includeE0000** (n008/n009/n010). Do not equate timer admission with merely asking script IsDead. IsUnconscious callback141fd1470 tests60000; that state alone is not excluded by virtual868(false). IsBleedingOut callback141fc7f50 recognizes100000/E0000 and a process byte, with its own return distinction. Script-state names are grounded by installed native registration strings/callbacks, not guessed from an enum number.

| State | Actual next-query result | Recovery/remaining limit |
|---|---|---|
| Assigned, en route, valid active entries and positive Health | No arrival test; passing entry can contribute | Travel can lag logical membership; not a measured historical en-route bonus. |
| 3D absent, handle resolves, active bucket survives | Same query as with 3D | No distance/graphics test. Process teardown is a different state. |
| Process/bucket absent | No passing A1/DB entry despite assigned identity and possessed skill | Applicable setup/load replay with recreated storage; resolution alone does not restore entries. |
| Dead/excluded life state, or Health<=0 | Actor skipped before its entry query | State/Health recovery can restore eligibility if assignment/entries survive; scripts may separately remove/deallocate the actor. |
| Unconscious60000 with positive Health | Not automatically excluded by this particular life-state test | Other predicates/conditions/storage can still block; no blanket claim about every incapacitation mode. |
| Bleeding-out/downed | E0000 is excluded on false;100000 alone is not | Distinct script bleeding-out/process conditions; actual current state must be known. |
| Disabled bit alone | No direct IsDisabled/800 test in these actor folds | Disability can affect process lifetime/resolution elsewhere. No universal disabled-contribution claim or alleged bug. |
| Actor handle fails this A1/DB lookup, E2 slot retained | Omit actor now; original slot is not invalidated by A1's local lookup | Next resolution of the same still-valid handle can contribute automatically, subject to all gates. |
| Handle index/generation stale | Resolver rejects it; never substitute another actor occupying that index | New-generation/replacement handle requires list reconstruction/reassignment; a new actor's matching base is insufficient. |
| E2 loader fails actor lookup | Stores invalid sentinel through140306e40 | Future query cannot rediscover the saved identity from that sentinel alone; explicit restoration/reinsertion required, not a guaranteed retry. |
| E2 pruned by serialization14040a0d0 or another mutating consumer | Failed member removed from that list | A1's nonmutating lookup does not undo pruning. CR1 writer passes the E2 list itself; UI local/other slot invalidation has separate scope. |
| Assignment removed or transferred | Old E2 no longer dispatches actor; category2 also needs matching environment | Reassignment reinserts normally. Cached producer interval can retain the old rate until due reset. |
| Destination unregistered or its Workshop/producer fails resolution | Scheduler skips Workshop or producer branch | No crew effect can create missing scheduled work. S2's pending/sentinel recovery limits still apply. |
| Generic unassigned then unloaded | CR1 compiled cleanup clears availability/holding references and disables/deletes actor | Named retention differs. A deleted generic's replacement is a new identity, not automatic recovery. |

Handle resolver `1428ccc40` validates masked index, nonnull table entry and generation before callback (S2 n004). It does not load missing references or check actor 3D. The A1 loop, E2 load reader and serializer have different mutation behavior; confusing them creates a false universal automatic-recovery claim. Normal dedup/removal handles ordinary repeated assignment; deliberately malformed/restored duplicates and disagreements remain outside the settled-transition proof.

## Production clocks and remote scheduling

`140f7f1e0` (n001) decides due cycles using old interval/remaining, then performs current reason/creation work, then obtains the current A1 timer and resets both floats at row+10/+14. Crew changes do not themselves rescale this row in the ordinary insertion/removal code. Failed production reasons can still consume the due opportunity/reset; actual creation remains separate. New row/re-registration and UI-rate caches have independent writers; this is not an exhaustive claim about every possible timer reset.

The same registered/resolvable scheduler receives frame, wait/sleep and travel elapsed under [E1](../inorganic-extractors/arithmetic-clocks.md) and [S2](../local-output-links/lifecycle.md). Crew queries use current state at reset, not a reconstructed history of each actor during skipped time. Remote presence does not override reason, power, input, receiver, registration or process-entry prerequisites. Save/load restores identities and row scalars, then rebuilds applicable runtime state; neither elapsed catch-up nor actual production is proved by a successful identity remap or finalization routine alone.
