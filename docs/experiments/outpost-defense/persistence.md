# Saved damage, healthy contrasts and turret ownership

[Native meaning](integrity.md), [source pins](sources.csv), [review](review.md).
All record/value positions below are **decimal decoded-save stream offsets**;
they are not original compressed-file offsets or native addresses. Dynamic
saved IDs identify this snapshot, not a stable live reference across sessions.

## Purpose-selected corpus and controls

HIST-0255 was selected because prior CR1–CR3/R1/L1 work positively identified
constructed actors, assigned crew and mature owned equipment. HIST-0036 and
HIST-0077 independently offer developed production/storage/cargo topologies;
HIST-0267 (mature Save52) supplies the existing root/accounting corpus. Selection
therefore seeks damage and actual membership, rather than treating one favorite
save as a universal sample. These are observational snapshots, not a chronological
controlled experiment or four independent playthroughs.

Fresh protected-original reads found **110 / 128 / 100 / 128** selected
destructible-definition/turret candidates respectively (HIST-0255/0036/0077/0267).
The second HIST-0255 pass also includes its 17 beacon candidates (**127** rows)
and uses the newly mapped ExtraE6 grammar for the turret links. Source hashes
agree before/after each decode; temporary scratch is cleaned by decoded_save.
The reader retains unsupported prefixes/extras rather than interpreting them as
empty state. Counts are detector coverage, not an exhaustive outpost inventory.

Five positively parsed HIST-0255 devices have **Health modifier section 2**:

| Saved reference | Base / object | Record start | Damage-value offset | Saved damage | Explicit Workshop owner |
|---|---|---:|---:|---:|---|
| ff01d232 | 0020a090, large atmospheric Water extractor | 5117540 | 5117638 | -12 | ff087168 |
| ff0202dc | 0020a084, large He-3 extractor | 5198249 | 5198341 | -144 | ff047885 |
| ff0202e6 | 0020a084, large He-3 extractor | 5199206 | 5199298 | -40.5 | ff047885 |
| ff062023 | 0020a052, large Antimony extractor | 7833283 | 7833379 | -380 | ff062012 |
| ff072592 | 0022174d, Semimetal Wafer fabricator | 8499326 | 8499440 | -3.6667633056640625 | ff062012 |

Each owner join is a counted Extra4C **WorkshopItem keyword 00054ba6**, mode0,
targeting an actual beacon-base record, not a coordinate/queue-adjacency guess.
Their counted extras close. They have saved nonactor capability bit 24 and
destroyed bit 23 clear. None is labelled destroyed or attack-damaged merely
because damage is present.

The strong same-object-class control is **ff0202f7**, record **5207446**:
the same 0020a084 base, same owner ff047885, closed ExtraBF sections, no
serialized Health base or modifier override. Additional same-owner large He-3
controls ff020309/031a/0325/0334 agree. Under the pinned current definition and
no additional loaded override, max400 plus damage-144 predicts **256/400=.64**;
the -40.5 example predicts **359.5/400=.89875**; the no-override control predicts
**400/400=1**. These are explicit **PREDICTIONS of default reconstruction**, not
photographed historical bar values or observed loaded Health. Untracked DLC/mod
overrides and current process state cannot be recovered from that arithmetic.

The other three scans detected no positive Health damage/destroyed witness in
their supported selected rows. That is a bounded negative control, not evidence
that Integrity cannot persist. No repair-positive transition or attack-history
record was recovered. The healthy control might never have been damaged; absence
of a damage modifier is not proof of repair.

## L1 historical turret owner gap: closed for the pair

Both original L1 actors remain at their original framed record offsets:

| Actor / base | Record | ExtraE6 interval | First explicit4C interval | Workshop owner |
|---|---:|---|---|---|
| ff038e6c / ballistic3 001099a5 | 12263961 | 12265255–12265265 | 12265265–12265269 | ff087168, mode0, key00054ba6 |
| ff038e6d / laser3 001e663d | 12265672 | 12266963–12266973 | 12266973–12266977 | ff087168, mode0, key00054ba6 |

Intervals are half-open. Native writer `14051ea30 case E6` writes a **u32 count**
followed by **count*(u32,byte)**. Loader `140521620 case E6 -> 140554bd0`
independently reads exactly that wire shape into padded 8-byte native entries.
It consumes **no queued reference identity**. Both actual records have count 1,
word2/byte1: ten bytes including the tag. The next counted extra is therefore
4C at the positions above; this is not skipping an opaque byte window.

The inherited Actor header and prior extras84/9C are parsed first. Native
4C save/load and key meaning are the existing Workshop/CR1/R1 contracts. The
second mode1 key `001c5edd` has separate targets ff01d169/ff01d15c; those are not
substituted for the mode0 Workshop owner. Fresh owner ff087168 is actual beacon
base 002c60e9 at record **9306058**, disabled/deleted clear. Its closed saved CB
member list independently contains both turret identities. CB corroborates
membership, not a current powered allocation or the entire construction list.

Thus L1's specific explicit-owner join gap is now **STRONG SAVE/STATIC closed**.
Full actor-extra parsing after the first4C, exhaustive turret count at that owner,
actual loaded power/AI and post-load coherence remain unclaimed. The original
L1 failure and report are retained; this is a new qualified continuation.

## State/restoration matrix

| State | Persistence class / producer | Reader/consumer and limit |
|---|---|---|
| Definition maximum and destruction stages | DEFINITION-DERIVED, DEST/component plus property defaults | Health base fallback 140b82b40; explicit AV overrides can supersede defaults |
| Health damage and explicit bases | PERSISTED when serialized, ExtraBF | 14051ea30 case BF ->1419aec20; loader 140521620 case BF ->1419aeff0; current/permanent/modifier methods use separate sections |
| Destroyed reference flag | PERSISTED change channel; different from negative Health damage | Writer-side SetDestroyed/terminal damage marks form change 1; common form loader 1405dfa40 merges saved reference mask d12960, including00800000. A flag's restoration is not an observed settled reload |
| Disabled/deleted | Separate form bits, not synonyms for zero Integrity | Existing prefix reader exposes800/20; production checks these independently |
| Owner and electrical/local links | PERSISTED saved identities, RECONSTRUCTED handles/maps | Counted4C/CB and prior Workshop/P1/S2 contracts; no attack cause follows from an edge |
| Attack timestamps | Script writes planet-location AVs | General AV persistence machinery exists; exact timestamp payloads in selected planet locations were not decoded here |
| Running attack, IsAttackStarted, aliases and timers | Script/quest VM state, not an authoritative field on every device | Compiled scripts identify writers/readers. Historical VM serialization/resumption was not reconstructed or live-tested |
| UI ratio/target list/current native pointers | RECONSTRUCTED/TRANSIENT | Recompute from resolved current values, membership and flags; no screenshot-to-save epoch join |

## Remaining gaps and prospective discriminator

1. **Damage cause:** the five snapshots do not identify the responsible actor,
   event, weapon, self-damage or script. A matched attack event/action history is
   needed to attribute them; guessing from their damage magnitudes is invalid.
2. **Travel ordering:** the exact order of human AttackTarget unload and
   different-planet cleanup determines whether the shortcut runs during a
   particular departure. The compiled rules are positive; the historical order
   remains OPEN.
3. **Reload/effective state:** defaults, saved damage and ownership are mapped;
   actual historical overrides, VM timer continuation, current quest aliases and
   settled loaded Health/operation were not measured. A live dependency is not
   silently added to accept the scoped static model.
4. **Repair transition:** no protected paired before/after repair saves or
   screenshot/reference join exists in this selected corpus. Native identity
   retention and Health restoration are supported independently; no SAVE repair
   transition is claimed.

If travel ordering becomes consequential, the smallest prospective test uses a
separate protected-save copy with a **positively identified already-started human
attack**, an owned destructible device and living attacker, plus a no-departure
control. Record device reference/Health/IsDestroyed and attack-started/alive
state before departure and after target unload/different-planet cleanup, then
compare an ordinary local retreat and different-planet departure. Discriminating
outcomes are direct destroyed-state changes before cleanup versus cleanup first
with no shortcut. User gameplay and any observer must be separately authorized;
the current offline brief permits neither. No game or save modification occurred.
