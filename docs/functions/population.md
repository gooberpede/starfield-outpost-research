# Crew, robots and defense

[Subject navigation and ABI limits](README.md) · [RVA index](index.md)

Entries use the pinned `Starfield.exe` 1.16.244.0 image. Internal-only observation. External invocation remains unvalidated.

Follow a mapped path

- [Ordinary crew admission](population.md#rva-0x004074f0)
- [Script assignment bypass](population.md#rva-0x02068d70)
- [Robot recipe quota](population.md#rva-0x00f3b170)
- [Crew production contribution](production.md#rva-0x00f7bd20)
- [Crew power contribution](power.md#rva-0x00f3dd50)

## RVA 0x000e5200

**entry-point metadata initialization** · Level B · preferred VA `0x1400e5200`

Analysis labels recorded in the original sources are `FUN_1400e5200`.

Recorded scope — entry-point metadata initialization

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 100).

- **Inputs** — Constructor context
- **Outputs** — Metadata rows initialized
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — 14590fc18; 1459102f8
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 100) · `N99`
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 95) · Initialize perk context metadata
  Binds entry-point context metadata, including two A1 context descriptors.

## RVA 0x002b5fa0

**function data getter** · Level B · preferred VA `0x1402b5fa0`

Analysis labels recorded in the original sources are `FUN_1402b5fa0`.

Recorded scope — function data getter

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 107).

- **Inputs** — Entry
- **Outputs** — Pointer at entry+18
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — Shared evaluator
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 107) · `N106`
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 103) · Read perk operation data
  Reads entry +0x18.

## RVA 0x00306db0

**Encode a saved reference identity** · Level C · preferred VA `0x140306db0`

Recorded scope — Encode a saved reference identity

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · current assignments](../experiments/crew/current-assignments.md) (line 110)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 24)

## RVA 0x00306e40

**report · entry** · Level C · preferred VA `0x140306e40`

Analysis labels recorded in the original sources are `FUN_140306e40`.

Recorded scope — Original report discusses this roster entry under report.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 64)
- [crew lifecycle · report](../experiments/crew-lifecycle/report.md) (line 13)
  Original report discusses this roster entry under report.
- [crew · functions](../experiments/crew/functions.csv) (line 77)
- [crew · lifecycle](../experiments/crew/lifecycle.md) (line 42)
  Original report discusses this roster entry under Persistence classes.

## RVA 0x004073c0

**Charged slots and the player clamp · entry** · Level C · preferred VA `0x1404073c0`

Analysis labels recorded in the original sources are `FUN_1404073c0`.

Recorded scope — Original report discusses this roster entry under Charged slots and the player clamp.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · capacity](../experiments/crew/capacity.md) (line 9)
- [crew · functions](../experiments/crew/functions.csv) (line 28)

## RVA 0x004074a0

**Clamp destination crew capacity by player command slots** · Level B · preferred VA `0x1404074a0`

Analysis labels recorded in the original sources are `FUN_1404074a0`.

Takes the lesser of effective destination capacity and player command capacity.

It calls destination-capacity helper `0x1404073c0` and applies the player's effective `SpaceshipCrewCommandSlots`, with no outpost exemption in the mapped clamp. The Crew menu worker compares occupied plus candidate cost against the result. This is a capacity input to admission, not a roster count or a remaining global pool. General native declaration and return register are unknown.

Original records

- [crew · capacity](../experiments/crew/capacity.md) (line 7)
- [crew · capacity](../experiments/crew/capacity.md) (line 29)
- [crew · functions](../experiments/crew/functions.csv) (line 29)
- [crew · functions](../experiments/crew/functions.csv) (line 29) · `SOR-FN-0064` · Player-clamped destination capacity

## RVA 0x004074f0

**Check ordinary crew admission** · Level A · preferred VA `0x1404074f0`

Analysis labels recorded in the original sources are `FUN_1404074f0`.

Evaluates destination slots and assignment restrictions before ordinary insertion.

Ordinary insertion uses the player-clamped option, while the Crew picker can ask for raw destination capacity. In ordinary nonnegative cases, outpost capacity is the lesser of effective destination slots and effective player command slots. Admission charges the candidate and existing actor costs. The insertion predicate's unsigned subtraction is distinct from the menu worker's positive sum test, so overcapacity behavior cannot be assumed safe. `CrewReassignDisabled` can block reassignment, and the outpost branch omits the final ship-location restriction. General prototype, return register and anomalous input behavior remain unknown.

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 114).

- **Inputs** — Crew context; actor; flags
- **Outputs** — Conditional admission
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — Slot cost; capacity; ownership
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 114) · `N113` · crew assignment capacity gate
- [crew · capacity](../experiments/crew/capacity.md) (line 29)
  Evaluates destination slots and assignment restrictions before ordinary insertion.
- [crew · functions](../experiments/crew/functions.csv) (line 2) · `SOR-FN-0063` · Assignment predicate
- [crew · lifecycle](../experiments/crew/lifecycle.md) (line 29)
  Evaluates destination slots and assignment restrictions before ordinary insertion.
- [robots · functions](../experiments/robots/functions.csv) (line 6) · normal human admission
- [crew · capacity](../experiments/crew/capacity.md) (line 31)
  Original report discusses this roster entry under Charged slots and the player clamp.
- [crew · capacity](../experiments/crew/capacity.md) (line 122)
  Original report discusses this roster entry under Removal, inaccessibility and overcapacity.
- [crew · lifecycle](../experiments/crew/lifecycle.md) (line 19)
  Original report discusses this roster entry under lifecycle.
- [crew · screen](../experiments/crew/screen.md) (line 45)
  Original report discusses this roster entry under Native population.

## RVA 0x004076b0

**Insert an actor into Workshop crew membership** · Level A · preferred VA `0x1404076b0`

Analysis labels recorded in the original sources are `FUN_1404076b0`.

Transfers crew membership and writes the actor's keyed assignment.

The routine deduplicates the actor handle, applies admission through `0x1404074f0` unless bypassed, resolves the owner and removes membership from a different owner. It appends to destination E2, writes actor CrewAssignment `0x26beac` via `0x140ba0d40`, marks owner change flag `0x80000000` and then notifies. Assignment can precede physical movement or a contributing active perk. The robot's WorkshopItem construction relationship has a separate key. The exact declaration and atomicity across consumers are unknown.

Scoped pseudocode abstraction. It covers the described branch and omits unqualified paths.

```text
Abstraction of the ordinary membership path. Failure, notification and transfer races are omitted.

qualify actor and destination
if not bypassed, apply admission predicate
remove old owner membership when different
append the actor handle to destination E2
write the actor's keyed assignment and mark the owner changed
notify downstream consumers
```

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 113).

- **Inputs** — CrewExtraData; actor; bypass flags
- **Outputs** — Append handle; assignment and notifications
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — Handle equality; 1404074f0; 140408bb0
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 113) · `N112` · unique actor crew insertion
- [crew · current assignments](../experiments/crew/current-assignments.md) (line 109)
  Transfers crew membership and writes the actor's keyed assignment.
- [crew · functions](../experiments/crew/functions.csv) (line 3) · `SOR-FN-0066` · Insert/migrate crew
- [crew · lifecycle](../experiments/crew/lifecycle.md) (line 15)
  Transfers crew membership and writes the actor's keyed assignment.
- [robots · functions](../experiments/robots/functions.csv) (line 4) · shared crew insertion
- [robots · lifecycle](../experiments/robots/lifecycle.md) (line 35)
  Transfers crew membership and writes the actor's keyed assignment.
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 59)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 79)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 12)
  Original report discusses this roster entry under Assignment to a real query.
- [crew lifecycle · report](../experiments/crew-lifecycle/report.md) (line 10)
  Original report discusses this roster entry under report.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 12)
- [crew skills · native](../experiments/crew-skills/native.md) (line 23)
  Original report discusses this roster entry under A1: per-actor producer timing.
- [crew · lifecycle](../experiments/crew/lifecycle.md) (line 19)
  Original report discusses this roster entry under lifecycle.
- [robots · effects](../experiments/robots/effects.md) (line 41)
  Original report discusses this roster entry under effects.

## RVA 0x00407a10

**Remove crew** · Level C · preferred VA `0x140407a10`

Analysis labels recorded in the original sources are `FUN_140407a10`.

Recorded scope — Remove crew

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 4) · `SOR-FN-0067`
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 80)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 12)
  Original report discusses this roster entry under Assignment to a real query.
- [crew lifecycle · report](../experiments/crew-lifecycle/report.md) (line 10)
  Original report discusses this roster entry under report.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 11)

## RVA 0x004088c0

**Sum charged slot costs** · Level C · preferred VA `0x1404088c0`

Analysis labels recorded in the original sources are `FUN_1404088c0`.

Recorded scope — Sum charged slot costs

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 30) · `SOR-FN-0065`

## RVA 0x00408a50

**get/create CrewExtraData** · Level B · preferred VA `0x140408a50`

Analysis labels recorded in the original sources are `FUN_140408a50`.

Recorded scope — get/create CrewExtraData

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 111).

- **Inputs** — Reference; create flag
- **Outputs** — ExtraE2 pointer; optional allocation
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — Reference+c8; CrewExtraData144b0a9d8
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 111) · `N110`
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 49)
- [build catalogue · ui](../experiments/build-catalogue/ui.md) (line 109)
  Original report discusses this roster entry under Footer gaps investigated.
- [crew · functions](../experiments/crew/functions.csv) (line 8)

## RVA 0x00408bb0

**assignment perk notification** · Level B · preferred VA `0x140408bb0`

Analysis labels recorded in the original sources are `FUN_140408bb0`.

Recorded scope — assignment perk notification

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 117).

- **Inputs** — Owner; actor
- **Outputs** — Context-specific crew perk traversal
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — 14040a230
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 117) · `N116`
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 81)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 16)
  Original report discusses this roster entry under Assignment to a real query.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 10)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 19)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 69)
- [crew skills · native](../experiments/crew-skills/native.md) (line 39)
  Original report discusses this roster entry under Type1 abilities: ship Fusion and destination state.
- [crew · functions](../experiments/crew/functions.csv) (line 21)
- [crew · lifecycle](../experiments/crew/lifecycle.md) (line 21)
  Original report discusses this roster entry under lifecycle.

## RVA 0x004094b0

**Reverse the destination ability path during assignment removal** · Level C · preferred VA `0x1404094b0`

Analysis labels recorded in the original sources are `FUN_1404094b0`.

Recorded scope — Reverse the destination ability path during assignment removal

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 16)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 72)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 78)
- [crew skills · native](../experiments/crew-skills/native.md) (line 39)
  Original report discusses this roster entry under Type1 abilities: ship Fusion and destination state.

## RVA 0x004095c0

**highest qualifying crew rank dispatcher** · Level B · preferred VA `0x1404095c0`

Analysis labels recorded in the original sources are `FUN_1404095c0`.

Recorded scope — highest qualifying crew rank dispatcher

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 116).

- **Inputs** — Entry point; list; contexts
- **Outputs** — Chosen actor entry evaluation
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — Not called by140f7bd20
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 116) · `N115`
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 2)
- [crew skills · native](../experiments/crew-skills/native.md) (line 45)
  Original report discusses this roster entry under AA: ship capacity, not a CONT CarryWeight aura.
- [crew skills · processes](../experiments/crew-skills/processes.md) (line 14)
  Original report discusses this roster entry under processes.

## RVA 0x00409f80

**Combat and non-effect role metadata · entry** · Level C · preferred VA `0x140409f80`

Analysis labels recorded in the original sources are `FUN_140409f80`.

Recorded scope — Original report discusses this roster entry under Combat and non-effect role metadata.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 5)
- [crew skills · native](../experiments/crew-skills/native.md) (line 53)
  Original report discusses this roster entry under Combat and non-effect role metadata.
- [crew skills · processes](../experiments/crew-skills/processes.md) (line 17)
  Original report discusses this roster entry under processes.

## RVA 0x0040a0d0

**Prune unresolved entries during E2 serialization** · Level C · preferred VA `0x14040a0d0`

Recorded scope — Prune unresolved entries during E2 serialization

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 58)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 45)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 25)

## RVA 0x0040a230

**crew perk traversal** · Level B · preferred VA `0x14040a230`

Analysis labels recorded in the original sources are `FUN_14040a230`.

Recorded scope — crew perk traversal

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 118).

- **Inputs** — Actor; assignment contexts
- **Outputs** — Visits crew-flagged perks
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — 14040a9d0
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 118) · `N117`
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 6)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 17)
- [crew skills · native](../experiments/crew-skills/native.md) (line 39)
  Original report discusses this roster entry under Type1 abilities: ship Fusion and destination state.
- [crew · functions](../experiments/crew/functions.csv) (line 22)
- [crew · lifecycle](../experiments/crew/lifecycle.md) (line 21)
  Original report discusses this roster entry under lifecycle.

## RVA 0x0040a360

**Assignment to a real query · entry** · Level C · preferred VA `0x14040a360`

Analysis labels recorded in the original sources are `FUN_14040a360`.

Recorded scope — Original report discusses this roster entry under Assignment to a real query.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 82)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 16)
  Original report discusses this roster entry under Assignment to a real query.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 39)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 54)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 70)
- [crew skills · native](../experiments/crew-skills/native.md) (line 39)
  Original report discusses this roster entry under Type1 abilities: ship Fusion and destination state.

## RVA 0x0040a840

**Type1 abilities: ship Fusion and destination state · entry** · Level C · preferred VA `0x14040a840`

Analysis labels recorded in the original sources are `FUN_14040a840`.

Recorded scope — Original report discusses this roster entry under Type1 abilities: ship Fusion and destination state.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 8)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 18)
- [crew skills · native](../experiments/crew-skills/native.md) (line 39)
  Original report discusses this roster entry under Type1 abilities: ship Fusion and destination state.

## RVA 0x0040a9d0

**type-one crew effect competition** · Level B · preferred VA `0x14040a9d0`

Analysis labels recorded in the original sources are `FUN_14040a9d0`.

Recorded scope — type-one crew effect competition

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 119).

- **Inputs** — Perk; actor rank; crew contexts
- **Outputs** — Type1 effect admission/suppression
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — Type2 A1 entries excluded from this branch
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 119) · `N118`
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 7)
- [crew skills · native](../experiments/crew-skills/native.md) (line 39)
  Original report discusses this roster entry under Type1 abilities: ship Fusion and destination state.
- [crew · functions](../experiments/crew/functions.csv) (line 23)
- [crew · lifecycle](../experiments/crew/lifecycle.md) (line 21)
  Original report discusses this roster entry under lifecycle.

## RVA 0x005366a0

**Participate in native selected-template restoration** · Level C · preferred VA `0x1405366a0`

Recorded scope — Participate in native selected-template restoration

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 30)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 47)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 51)

## RVA 0x00543370

**Participate in native selected-template restoration** · Level C · preferred VA `0x140543370`

Recorded scope — Participate in native selected-template restoration

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 30)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 46)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 52)

## RVA 0x00547c90

**Dispatch saved linked-reference restoration** · Level C · preferred VA `0x140547c90`

Recorded scope — Dispatch saved linked-reference restoration

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · current assignments](../experiments/crew/current-assignments.md) (line 114)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 31)

## RVA 0x00554bd0

**Load the ExtraData E6 counted representation** · Level C · preferred VA `0x140554bd0`

Analysis labels recorded in the original sources are `FUN_140554bd0`.

Recorded scope — Load the ExtraData E6 counted representation

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · persistence](../experiments/outpost-defense/persistence.md) (line 68)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 5)

## RVA 0x005bf6d0

**Register BGSDestructibleObject_Component** · Level C · preferred VA `0x1405bf6d0`

Analysis labels recorded in the original sources are `FUN_1405bf6d0`.

Recorded scope — Register BGSDestructibleObject_Component

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 33–35)
- [construction variants · functions](../experiments/construction-variants/functions.csv) (line 111)

## RVA 0x005bfe60

**Damage and operational consequences · entry** · Level C · preferred VA `0x1405bfe60`

Analysis labels recorded in the original sources are `FUN_1405bfe60`.

Recorded scope — Original report discusses this roster entry under Damage and operational consequences.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 6)
- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 93)
  Original report discusses this roster entry under Damage and operational consequences.

## RVA 0x005c02a0

**Damage and operational consequences · entry** · Level C · preferred VA `0x1405c02a0`

Analysis labels recorded in the original sources are `FUN_1405c02a0`.

Recorded scope — Original report discusses this roster entry under Damage and operational consequences.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 7)
- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 79)
  Original report discusses this roster entry under Damage and operational consequences.

## RVA 0x005c42d0

**Restore Health damage through modifier index 2** · Level C · preferred VA `0x1405c42d0`

Analysis labels recorded in the original sources are `FUN_1405c42d0`.

Recorded scope — Restore Health damage through modifier index 2

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 131)
- [construction variants · functions](../experiments/construction-variants/functions.csv) (line 54)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 9)

## RVA 0x005d2590

**Load the NPC template parts array** · Level C · preferred VA `0x1405d2590`

Analysis labels recorded in the original sources are `FUN_1405d2590`.

Recorded scope — Load the NPC template parts array

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew skills · population](../experiments/crew-skills/population.md) (line 19)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 76)

## RVA 0x005d2d90

**Resolve enabled NPC template parts** · Level C · preferred VA `0x1405d2d90`

Analysis labels recorded in the original sources are `FUN_1405d2d90`.

Recorded scope — Resolve enabled NPC template parts

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew skills · population](../experiments/crew-skills/population.md) (line 19)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 94)

## RVA 0x005d3ad0

**Resolve enabled NPC template parts** · Level C · preferred VA `0x1405d3ad0`

Analysis labels recorded in the original sources are `FUN_1405d3ad0`.

Recorded scope — Resolve enabled NPC template parts

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew skills · population](../experiments/crew-skills/population.md) (line 19)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 7)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 106)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 112)

## RVA 0x005d4a00

**Selected rank and load reconstruction · entry** · Level C · preferred VA `0x1405d4a00`

Analysis labels recorded in the original sources are `FUN_1405d4a00`.

Recorded scope — Original report discusses this roster entry under Selected rank and load reconstruction.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 8)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 21)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 30)
  Original report discusses this roster entry under Selected rank and load reconstruction.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 101)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 107)

## RVA 0x005d4b20

**generic template selected-source recursion; not alone proof of scripts** · Level C · preferred VA `0x1405d4b20`

Analysis labels recorded in the original sources are `FUN_1405d4b20`.

Recorded scope — generic template selected-source recursion; not alone proof of scripts

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 50)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 16)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 116)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 121)

## RVA 0x005e0230

**installed VMAD loader forwards parser** · Level C · preferred VA `0x1405e0230`

Recorded scope — installed VMAD loader forwards parser

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 48)
- [robots · functions](../experiments/robots/functions.csv) (line 49)

## RVA 0x009e7900

**IRES definition loader** · Level B · preferred VA `0x1409e7900`

Analysis labels recorded in the original sources are `FUN_1409e7900`.

Recorded scope — IRES definition loader

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 101).

- **Inputs** — IRES and file reader
- **Outputs** — Tagged NAM references
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — 1409e8570
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 101) · `N100`
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 53) · Load resource definition fields
  Reads NAM1/NAM2/NAM3 into IRES +0xf8/+0x108/+0x100 as tagged IDs.
- [stored resources · functions](../experiments/stored-resources/functions.csv) (line 27) · `n026` · IRES NNAM GNAM SNAM TINC loader
- [resource retained population · d5ad input provenance](../experiments/resource-retained-population/d5ad-input-provenance.md) (line 33)
  Original report discusses this roster entry under d5ad input provenance.
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 205) · `D5AD-IN037`
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 274) · `D5AD-IN106`
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 388) · `D5AD-DF01-04`

## RVA 0x009e8570

**IRES reference fixup** · Level B · preferred VA `0x1409e8570`

Analysis labels recorded in the original sources are `FUN_1409e8570`.

Recorded scope — IRES reference fixup

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 102).

- **Inputs** — IRES tagged references
- **Outputs** — Resolved AV global and recipe
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — IRES+f8; +100; +108
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 102) · `N101`
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 54) · Fix up resource definition links
  Resolves tagged IRES fields and writes the resource backpointer at AV +0x148.
- [resource retained population · d5ad input provenance](../experiments/resource-retained-population/d5ad-input-provenance.md) (line 47)
  Original report discusses this roster entry under Definition loading and postlink readiness.
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 250) · `D5AD-IN082`

## RVA 0x00a02160

**load JNAM at COBJ+178** · Level C · preferred VA `0x140a02160`

Analysis labels recorded in the original sources are `FUN_140a02160`.

Recorded scope — load JNAM at COBJ+178

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 14)
- [build catalogue · catalogue](../experiments/build-catalogue/catalogue.md) (line 22)
  Original report discusses this roster entry under Definition to category map.
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 42)
- [limits · functions](../experiments/limits/functions.csv) (line 52)
- [limits · native](../experiments/limits/native.md) (line 25)
  Original report discusses this roster entry under Recipe limit, displayed count and accepted construction.
- [robots · limits](../experiments/robots/limits.md) (line 16)
  Original report discusses this roster entry under limits.
- [shared outpost storage · functions](../experiments/shared-outpost-storage/functions.csv) (line 36)
- [shared outpost storage · prerequisites](../experiments/shared-outpost-storage/prerequisites.md) (line 34)
  Original report discusses this roster entry under Definition to menu and accepted build.

## RVA 0x00acc660

**Read a component of the Actor native suffix** · Level C · preferred VA `0x140acc660`

Analysis labels recorded in the original sources are `FUN_140acc660`.

Recorded scope — Read a component of the Actor native suffix

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew skills · lifecycle](../experiments/crew-skills/lifecycle.md) (line 45)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 56)

## RVA 0x00b56c50

**Damage and operational consequences · entry** · Level C · preferred VA `0x140b56c50`

Analysis labels recorded in the original sources are `FUN_140b56c50`.

Recorded scope — Original report discusses this roster entry under Damage and operational consequences.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 12)
- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 81)
  Original report discusses this roster entry under Damage and operational consequences.

## RVA 0x00b64fc0

**general item insertion** · Level B · preferred VA `0x140b64fc0`

Analysis labels recorded in the original sources are `FUN_140b64fc0`.

Recorded scope — general item insertion

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 109).

- **Inputs** — Destination; item; reason; count
- **Outputs** — Inventory mutation request/results
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — 140f7d6a0 caller; 140b70a80
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 109) · `N108`
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 160) · Insert ordinary produced item
  Native insertion receives product, reason 9 and selected integer count at the documented caller.
- [storage · functions](../experiments/storage/functions.csv) (line 39) · `S1C-002` · generic add retains request and returns theoretical excess
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 149)
- [storage · capacity native](../experiments/storage/capacity-native.md) (line 108)
  Original report discusses this roster entry under Fit computation does not enforce all generic additions.
- [storage · capacity native](../experiments/storage/capacity-native.md) (line 121)
  Original report discusses this roster entry under Fit computation does not enforce all generic additions.
- [storage · capacity native](../experiments/storage/capacity-native.md) (line 151)
  Original report discusses this roster entry under Local output-link redistribution admission and execution.
- [storage · native](../experiments/storage/native.md) (line 45)
  Original report discusses this roster entry under Owner, weight and capacity.

## RVA 0x00b6cee0

**Read the permanent reference actor value** · Level C · preferred VA `0x140b6cee0`

Analysis labels recorded in the original sources are `FUN_140b6cee0`.

Recorded scope — The scoped Health route distinguishes this reference vtable method at byte displacement +0x10 from current and base value paths. It adds modifier section zero to base.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 26)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 15)

## RVA 0x00b6d4d0

**Damage and operational consequences · entry** · Level C · preferred VA `0x140b6d4d0`

Analysis labels recorded in the original sources are `FUN_140b6d4d0`.

Recorded scope — Original report discusses this roster entry under Damage and operational consequences.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 17)
- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 87)
  Original report discusses this roster entry under Damage and operational consequences.

## RVA 0x00be3fb0

**Condition callback for the base actor value** · Level C · preferred VA `0x140be3fb0`

Analysis labels recorded in the original sources are `FUN_140be3fb0`.

Recorded scope — Condition callback for the base actor value

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew skills · native](../experiments/crew-skills/native.md) (line 33)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 123)

## RVA 0x00be51a0

**Apply the native GetDead condition predicate** · Level C · preferred VA `0x140be51a0`

Recorded scope — Apply the native GetDead condition predicate

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 44)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 28)

## RVA 0x00c49960

**HasKeyword condition callback** · Level B · preferred VA `0x140c49960`

Analysis labels recorded in the original sources are `FUN_140c49960`.

Recorded scope — HasKeyword condition callback

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 108).

- **Inputs** — Native condition context
- **Outputs** — Qualified condition result
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — Registration 1230
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 108) · `N107`
- [construction variants · functions](../experiments/construction-variants/functions.csv) (line 117)
- [inorganic extractors · production modifiers](../experiments/inorganic-extractors/production-modifiers.md) (line 31)
  Original report discusses this roster entry under production modifiers.
- [terran armada outpost recon · native](../experiments/terran-armada-outpost-recon/native.md) (line 67)
  Original report discusses this roster entry under Exact quest-request condition and invocation.

## RVA 0x00c93cf0

**conditional entry-point evaluator** · Level B · preferred VA `0x140c93cf0`

Analysis labels recorded in the original sources are `FUN_140c93cf0`.

Recorded scope — conditional entry-point evaluator

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 97).

- **Inputs** — Entry-point number; actor; argument array
- **Outputs** — Conditional operation calls
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — 141935370; 140c94430
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 97) · `N96`
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 85) · Evaluate active perk entries
  Checks active entry-point rows and dispatches qualifying operations.
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 88)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 20)
  Original report discusses this roster entry under Assignment to a real query.
- [crew lifecycle · report](../experiments/crew-lifecycle/report.md) (line 9)
  Original report discusses this roster entry under report.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 9)
- [crew skills · native](../experiments/crew-skills/native.md) (line 17)
  Original report discusses this roster entry under Possession, display and effect registration are different.
- [crew skills · native](../experiments/crew-skills/native.md) (line 23)
  Original report discusses this roster entry under A1: per-actor producer timing.

## RVA 0x00c94060

**variadic entry-point dispatch** · Level B · preferred VA `0x140c94060`

Analysis labels recorded in the original sources are `FUN_140c94060`.

Recorded scope — variadic entry-point dispatch

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 96).

- **Inputs** — Actor and argument pointers
- **Outputs** — Calls shared evaluator
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — 140c93cf0
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 96) · `N95`
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 85) · Dispatch entry-point perk evaluation
  Builds variadic argument array for the perk evaluator.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 71)
- [crew skills · native](../experiments/crew-skills/native.md) (line 23)
  Original report discusses this roster entry under A1: per-actor producer timing.

## RVA 0x00c94430

**single-float multiply operation** · Level B · preferred VA `0x140c94430`

Analysis labels recorded in the original sources are `FUN_140c94430`.

Recorded scope — single-float multiply operation

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 99).

- **Inputs** — Float result pointer; OneValue factor
- **Outputs** — Binary32 result multiplied in place
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — 1458d30b0 index3
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 99) · `N98`
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 104) · Multiply perk result scalar
  Operation 3 checks float type, updates the result and invokes bookkeeping.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 24)
- [crew skills · native](../experiments/crew-skills/native.md) (line 25)
  Original report discusses this roster entry under A1: per-actor producer timing.

## RVA 0x00c954b0

**OneValue four-byte field loader** · Level B · preferred VA `0x140c954b0`

Analysis labels recorded in the original sources are `FUN_140c954b0`.

Recorded scope — OneValue four-byte field loader

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 110).

- **Inputs** — OneValue data object; file reader current field
- **Outputs** — Four bytes read into data+18 if field size4
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — OneValue vtable144bd0498 +28; 140ca13b0 EPFD dispatch
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 110) · `N109`
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 100) · Load OneValue operand
  Validated four-byte EPFD field supplies the operation's scalar.

## RVA 0x00c9fda0

**operation index getter** · Level B · preferred VA `0x140c9fda0`

Analysis labels recorded in the original sources are `FUN_140c9fda0`.

Recorded scope — operation index getter

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 106).

- **Inputs** — Entry
- **Outputs** — Byte at entry+11
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — Shared evaluator
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 106) · `N105`
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 102) · Read perk operation index
  Reads entry +0x11 to select the operation.

## RVA 0x00ca0540

**PERK entry type allocation** · Level B · preferred VA `0x140ca0540`

Analysis labels recorded in the original sources are `FUN_140ca0540`.

Recorded scope — PERK entry type allocation

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 104).

- **Inputs** — Entry type
- **Outputs** — Allocated entry
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — Type2 BGSEntryPointPerkEntry
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 104) · `N103`
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 98) · Construct type-2 perk entry
  Creates the entry consumed by the type-2 loader.

## RVA 0x00ca13b0

**entry-point data loader** · Level B · preferred VA `0x140ca13b0`

Analysis labels recorded in the original sources are `FUN_140ca13b0`.

Recorded scope — entry-point data loader

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 105).

- **Inputs** — Entry; owner; reader
- **Outputs** — DATA EPFT EPFD condition fields
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — Entry+10; +18
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 105) · `N104`
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 98) · Load entry-point perk data
  Loads DATA bytes and handles the EPFT=1 OneValue allocation branch.

## RVA 0x00ca1a20

**active entry-point registration** · Level B · preferred VA `0x140ca1a20`

Analysis labels recorded in the original sources are `FUN_140ca1a20`.

Recorded scope — active entry-point registration

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 127).

- **Inputs** — Entry; actor
- **Outputs** — Sorted active bucket insertion
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — Actor+228/+8/+480; 140ca4be0
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 127) · `N126`
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 84)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 26)
  Original report discusses this roster entry under Selected rank and load reconstruction.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 21)
- [crew skills · native](../experiments/crew-skills/native.md) (line 15)
  Original report discusses this roster entry under Possession, display and effect registration are different.

## RVA 0x00ca1bd0

**active entry-point removal** · Level B · preferred VA `0x140ca1bd0`

Analysis labels recorded in the original sources are `FUN_140ca1bd0`.

Recorded scope — active entry-point removal

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 128).

- **Inputs** — Entry; actor
- **Outputs** — Exact entry-pointer removal
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — Actor+228/+8/+480
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 128) · `N127`
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 85)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 26)
  Original report discusses this roster entry under Selected rank and load reconstruction.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 22)
- [crew skills · native](../experiments/crew-skills/native.md) (line 15)
  Original report discusses this roster entry under Possession, display and effect registration are different.

## RVA 0x00ca2490

**PERK entry loader** · Level B · preferred VA `0x140ca2490`

Analysis labels recorded in the original sources are `FUN_140ca2490`.

Recorded scope — PERK entry loader

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 103).

- **Inputs** — PERK and reader
- **Outputs** — Entries with ranks and priority
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — 140ca0540; 140ca13b0
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 103) · `N102`
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 97) · Load PERK entries
  Creates type-2 entries through the documented constructor.

## RVA 0x00ca3910

**remove old and install selected perk rank** · Level B · preferred VA `0x140ca3910`

Analysis labels recorded in the original sources are `FUN_140ca3910`.

Recorded scope — remove old and install selected perk rank

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 126).

- **Inputs** — Perk; actor; old/new ranks
- **Outputs** — Entry+8+1 equality dispatch
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — Virtual+70 remove; +68 register
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 126) · `N125`
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 83)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 26)
  Original report discusses this roster entry under Selected rank and load reconstruction.
- [crew lifecycle · report](../experiments/crew-lifecycle/report.md) (line 10)
  Original report discusses this roster entry under report.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 20)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 32)
- [crew skills · native](../experiments/crew-skills/native.md) (line 14)
  Original report discusses this roster entry under Possession, display and effect registration are different.

## RVA 0x00ca4be0

**sorted active entry insertion** · Level B · preferred VA `0x140ca4be0`

Analysis labels recorded in the original sources are `FUN_140ca4be0`.

Recorded scope — sorted active entry insertion

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 129).

- **Inputs** — Bucket; entry; comparator
- **Outputs** — Inserted entry
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — 140ca3670 priority/rank comparator
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 129) · `N128`

## RVA 0x00cd77d0

**part-specific NPC copy; bit 3 selected grants** · Level C · preferred VA `0x140cd77d0`

Analysis labels recorded in the original sources are `FUN_140cd77d0`.

Recorded scope — part-specific NPC copy; bit 3 selected grants

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 44)
- [robots · functions](../experiments/robots/functions.csv) (line 45)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 9)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 22)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 30)
  Original report discusses this roster entry under Selected rank and load reconstruction.
- [crew lifecycle · persistence](../experiments/crew-lifecycle/persistence.md) (line 13)
  Original report discusses this roster entry under Search coverage and why these witnesses qualify.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 114)
- [crew skills · population](../experiments/crew-skills/population.md) (line 19)
  Original report discusses this roster entry under Template inheritance, rather than a union of ancestor perks.

## RVA 0x00cdf140

**Participate in effective NPC template assembly** · Level C · preferred VA `0x140cdf140`

Recorded scope — Participate in effective NPC template assembly

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 30)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 50)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 56)

## RVA 0x00cdfde0

**Participate in effective NPC template assembly** · Level C · preferred VA `0x140cdfde0`

Recorded scope — Participate in effective NPC template assembly

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 30)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 49)

## RVA 0x00f2fc50

**Dispatch the reference damage route** · Level C · preferred VA `0x140f2fc50`

Analysis labels recorded in the original sources are `FUN_140f2fc50`.

Recorded scope — Dispatch the reference damage route

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 81)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 23)

## RVA 0x00f34650

**removal through cleanup** · Level C · preferred VA `0x140f34650`

Analysis labels recorded in the original sources are `FUN_140f34650`.

Recorded scope — removal through cleanup

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 10)
- [robots · functions](../experiments/robots/functions.csv) (line 11)
- [robots · functions](../experiments/robots/functions.csv) (line 12)
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 80)
- [containers displays · native](../experiments/containers-displays/native.md) (line 292)
  Original report discusses this roster entry under New construction suppresses default stock.
- [robots · limits](../experiments/robots/limits.md) (line 71)
  Original report discusses this roster entry under Why the set is per outpost and how it changes.

## RVA 0x00f36310

**Restore existing-reference Health and destruction state** · Level C · preferred VA `0x140f36310`

Analysis labels recorded in the original sources are `FUN_140f36310`.

Recorded scope — Restore existing-reference Health and destruction state

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 121)
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 217)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 25)
- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 131)
  Original report discusses this roster entry under Repair, identity and accounting.

## RVA 0x00f386a0

**Native population · entry** · Level C · preferred VA `0x140f386a0`

Analysis labels recorded in the original sources are `FUN_140f386a0`.

Recorded scope — Original report discusses this roster entry under Native population.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 97)
- [crew · screen](../experiments/crew/screen.md) (line 45)
  Original report discusses this roster entry under Native population.
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 27)
- [spatial placement · functions](../experiments/spatial-placement/functions.csv) (line 10)

## RVA 0x00f3b080

**construction base to COBJ lookup** · Level C · preferred VA `0x140f3b080`

Analysis labels recorded in the original sources are `FUN_140f3b080`.

Recorded scope — construction base to COBJ lookup

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 19)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 76)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 153)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 163)
- [limits · functions](../experiments/limits/functions.csv) (line 53)
- [limits · native](../experiments/limits/native.md) (line 32)
  Original report discusses this roster entry under Recipe limit, displayed count and accepted construction.

## RVA 0x00f3b170

**count matching recipe limit global in selected-context item set** · Level C · preferred VA `0x140f3b170`

Recorded scope — count matching recipe limit global in selected-context item set

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 15)
- [robots · functions](../experiments/robots/functions.csv) (line 17)
- [limits · functions](../experiments/limits/functions.csv) (line 2)

## RVA 0x00f3cf40

**WorkshopItem owner relationship** · Level C · preferred VA `0x140f3cf40`

Analysis labels recorded in the original sources are `FUN_140f3cf40`.

Recorded scope — WorkshopItem owner relationship

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 9)
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 82)
- [docs · function register](../function-register.md) (line 226) · `SOR-FN-0058`
  Original group scope — Saved owner or membership reconstruction path

## RVA 0x00f404f0

**remove wrappers through 1421c6b90** · Level C · preferred VA `0x140f404f0`

Analysis labels recorded in the original sources are `FUN_140f404f0`.

Recorded scope — remove wrappers through 1421c6b90

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 13)
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 81)
- [containers displays · native](../experiments/containers-displays/native.md) (line 292)
  Original report discusses this roster entry under New construction suppresses default stock.
- [robots · limits](../experiments/robots/limits.md) (line 71)
  Original report discusses this roster entry under Why the set is per outpost and how it changes.

## RVA 0x00f5f2d0

**registry callback exclusion predicate** · Level C · preferred VA `0x140f5f2d0`

Recorded scope — registry callback exclusion predicate

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 37)
- [robots · functions](../experiments/robots/functions.csv) (line 39)
- [docs · function register](../function-register.md) (line 226) · `SOR-FN-0059`
  Original group scope — Constructed item reconstruction path

## RVA 0x00f60f60

**SingleWorkshopItem virtual method at +A0 placement** · Level C · preferred VA `0x140f60f60`

Analysis labels recorded in the original sources are `FUN_140f60f60`.

Recorded scope — SingleWorkshopItem virtual method at +A0 placement

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 40)
- [construction variants · functions](../experiments/construction-variants/functions.csv) (line 61)
- [construction variants · functions](../experiments/construction-variants/functions.csv) (line 114)
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 224)
- [containers displays · native](../experiments/containers-displays/native.md) (line 250)
  Original report discusses this roster entry under New construction suppresses default stock.
- [limits · functions](../experiments/limits/functions.csv) (line 63)
- [limits · native](../experiments/limits/native.md) (line 60)
  Original report discusses this roster entry under Selected-outpost scope and updates.
- [robots · limits](../experiments/robots/limits.md) (line 65)
  Original report discusses this roster entry under Why the set is per outpost and how it changes.

## RVA 0x012b5c60

**additional perk rank record update** · Level B · preferred VA `0x1412b5c60`

Analysis labels recorded in the original sources are `FUN_1412b5c60`.

Recorded scope — additional perk rank record update

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 123).

- **Inputs** — Actor additional records; perk; requested rank
- **Outputs** — One bounded rank value per perk
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — Zero request increments current rank
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 123) · `N122`
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 26)
- [crew skills · native](../experiments/crew-skills/native.md) (line 14)
  Original report discusses this roster entry under Possession, display and effect registration are different.

## RVA 0x012b60a0

**Write additional selected actor perk ranks** · Level C · preferred VA `0x1412b60a0`

Analysis labels recorded in the original sources are `FUN_1412b60a0`.

Recorded scope — Write additional selected actor perk ranks

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · persistence](../experiments/crew-lifecycle/persistence.md) (line 40)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 55)

## RVA 0x012b62f0

**Selected rank and load reconstruction · entry** · Level C · preferred VA `0x1412b62f0`

Recorded scope — Original report discusses this roster entry under Selected rank and load reconstruction.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 43)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 32)
  Original report discusses this roster entry under Selected rank and load reconstruction.

## RVA 0x012b6eb0

**Read the actor owned-perk rank list** · Level C · preferred VA `0x1412b6eb0`

Analysis labels recorded in the original sources are `FUN_1412b6eb0`.

Recorded scope — Read the actor owned-perk rank list

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · persistence](../experiments/crew-lifecycle/persistence.md) (line 40–42)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 86)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 28)

## RVA 0x012b7020

**Read the other actor perk-state representation** · Level C · preferred VA `0x1412b7020`

Analysis labels recorded in the original sources are `FUN_1412b7020`.

Recorded scope — Read the other actor perk-state representation

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew skills · lifecycle](../experiments/crew-skills/lifecycle.md) (line 21)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 29)

## RVA 0x0130caa0

**Deduplicate available crew registration** · Level C · preferred VA `0x14130caa0`

Analysis labels recorded in the original sources are `FUN_14130caa0`.

Recorded scope — Deduplicate available crew registration

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · report](../experiments/crew/report.md) (line 68)
- [crew · functions](../experiments/crew/functions.csv) (line 64)
- [crew · functions](../experiments/crew/functions.csv) (line 70)

## RVA 0x0130cd20

**Remove old crew assignments before insertion** · Level C · preferred VA `0x14130cd20`

Analysis labels recorded in the original sources are `FUN_14130cd20`.

Recorded scope — Remove old crew assignments before insertion

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · report](../experiments/crew/report.md) (line 70)
- [crew · functions](../experiments/crew/functions.csv) (line 68)

## RVA 0x0130ce90

**Serialize the unassigned registry** · Level C · preferred VA `0x14130ce90`

Analysis labels recorded in the original sources are `FUN_14130ce90`.

Recorded scope — Serialize the unassigned registry

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · current assignments](../experiments/crew/current-assignments.md) (line 116)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 2)
- [crew · functions](../experiments/crew/functions.csv) (line 105)

## RVA 0x0130d540

**Persistence classes · entry** · Level C · preferred VA `0x14130d540`

Analysis labels recorded in the original sources are `FUN_14130d540`.

Recorded scope — Original report discusses this roster entry under Persistence classes.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · current functions](../experiments/crew/current-functions.csv) (line 29)
- [crew · functions](../experiments/crew/functions.csv) (line 119)
- [crew · lifecycle](../experiments/crew/lifecycle.md) (line 44)
  Original report discusses this roster entry under Persistence classes.

## RVA 0x0130d650

**Persistence classes · entry** · Level C · preferred VA `0x14130d650`

Analysis labels recorded in the original sources are `FUN_14130d650`.

Recorded scope — Original report discusses this roster entry under Persistence classes.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · current functions](../experiments/crew/current-functions.csv) (line 6)
- [crew · functions](../experiments/crew/functions.csv) (line 106)
- [crew · lifecycle](../experiments/crew/lifecycle.md) (line 44)
  Original report discusses this roster entry under Persistence classes.

## RVA 0x0130fba0

**Enumerate ship management components for registry serialization** · Level C · preferred VA `0x14130fba0`

Analysis labels recorded in the original sources are `FUN_14130fba0`.

Recorded scope — Enumerate ship management components for registry serialization

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · current assignments](../experiments/crew/current-assignments.md) (line 116–118)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 4)
- [crew · functions](../experiments/crew/functions.csv) (line 115)

## RVA 0x0130feb0

**Entry points and actual source lists · entry** · Level C · preferred VA `0x14130feb0`

Analysis labels recorded in the original sources are `FUN_14130feb0`.

Recorded scope — Original report discusses this roster entry under Entry points and actual source lists.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 71)
- [shared outpost storage · consumers](../experiments/shared-outpost-storage/consumers.md) (line 51)
  Original report discusses this roster entry under Entry points and actual source lists.
- [shared outpost storage · functions](../experiments/shared-outpost-storage/functions.csv) (line 62)

## RVA 0x0144e220

**Find or update an existing Crew row** · Level C · preferred VA `0x14144e220`

Analysis labels recorded in the original sources are `FUN_14144e220`.

Recorded scope — Find or update an existing Crew row

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · screen](../experiments/crew/screen.md) (line 37)
- [crew · functions](../experiments/crew/functions.csv) (line 92)

## RVA 0x0144e3d0

**Installed movie and UI actions · entry** · Level C · preferred VA `0x14144e3d0`

Analysis labels recorded in the original sources are `FUN_14144e3d0`.

Recorded scope — Original report discusses this roster entry under Installed movie and UI actions.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 107)
- [crew · screen](../experiments/crew/screen.md) (line 91)
  Original report discusses this roster entry under Installed movie and UI actions.

## RVA 0x0144f510

**Insert a Crew row in sorted order** · Level C · preferred VA `0x14144f510`

Analysis labels recorded in the original sources are `FUN_14144f510`.

Recorded scope — Insert a Crew row in sorted order

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · screen](../experiments/crew/screen.md) (line 37)
- [crew · functions](../experiments/crew/functions.csv) (line 108)

## RVA 0x0153cfe0

**Merge unassigned and destination lists** · Level C · preferred VA `0x14153cfe0`

Analysis labels recorded in the original sources are `FUN_14153cfe0`.

Recorded scope — Merge unassigned and destination lists

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 44) · `SOR-FN-0069`
- [crew · screen](../experiments/crew/screen.md) (line 21)
  Original report discusses this roster entry under Native population.

## RVA 0x0153d170

**Native population · entry** · Level C · preferred VA `0x14153d170`

Analysis labels recorded in the original sources are `FUN_14153d170`.

Recorded scope — Original report discusses this roster entry under Native population.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 45)
- [crew · screen](../experiments/crew/screen.md) (line 29)
  Original report discusses this roster entry under Native population.

## RVA 0x0153d900

**Row fields and skills · entry** · Level C · preferred VA `0x14153d900`

Analysis labels recorded in the original sources are `FUN_14153d900`.

Recorded scope — Original report discusses this roster entry under Row fields and skills.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 48)
- [crew · screen](../experiments/crew/screen.md) (line 58)
  Original report discusses this roster entry under Row fields and skills.

## RVA 0x0153dc70

**Fill actor row and crew perks** · Level C · preferred VA `0x14153dc70`

Analysis labels recorded in the original sources are `FUN_14153dc70`.

Recorded scope — Fill actor row and crew perks

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 49) · `SOR-FN-0070`

## RVA 0x0153e290

**Inspect possessed perks for screen display admission** · Level C · preferred VA `0x14153e290`

Analysis labels recorded in the original sources are `FUN_14153e290`.

Recorded scope — Inspect possessed perks for screen display admission

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew skills · native](../experiments/crew-skills/native.md) (line 12)
- [crew · functions](../experiments/crew/functions.csv) (line 50)

## RVA 0x0153e4f0

**Fill an assigned or unassigned Crew row** · Level C · preferred VA `0x14153e4f0`

Analysis labels recorded in the original sources are `FUN_14153e4f0`.

Recorded scope — Fill an assigned or unassigned Crew row

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · current assignments](../experiments/crew/current-assignments.md) (line 119–121)
- [crew · functions](../experiments/crew/functions.csv) (line 10)
- [crew · functions](../experiments/crew/functions.csv) (line 39)

## RVA 0x0153eb90

**Populate Crew provider** · Level C · preferred VA `0x14153eb90`

Analysis labels recorded in the original sources are `FUN_14153eb90`.

Recorded scope — Populate Crew provider

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 51) · `SOR-FN-0068`
- [crew · screen](../experiments/crew/screen.md) (line 19)
  Original report discusses this roster entry under Native population.

## RVA 0x0153f4d0

**Populate the crew assignment picker** · Level C · preferred VA `0x14153f4d0`

Analysis labels recorded in the original sources are `FUN_14153f4d0`.

Recorded scope — Populate the crew assignment picker

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · screen](../experiments/crew/screen.md) (line 43)
- [crew · functions](../experiments/crew/functions.csv) (line 55)

## RVA 0x0153f6d0

**Native population · entry** · Level C · preferred VA `0x14153f6d0`

Analysis labels recorded in the original sources are `FUN_14153f6d0`.

Recorded scope — Original report discusses this roster entry under Native population.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 12)
- [crew · screen](../experiments/crew/screen.md) (line 44)
  Original report discusses this roster entry under Native population.

## RVA 0x0153f7d0

**Native population · entry** · Level C · preferred VA `0x14153f7d0`

Analysis labels recorded in the original sources are `FUN_14153f7d0`.

Recorded scope — Original report discusses this roster entry under Native population.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 13)
- [crew · screen](../experiments/crew/screen.md) (line 45)
  Original report discusses this roster entry under Native population.

## RVA 0x0158a6e0

**Produce the selected reference integrity indicator** · Level C · preferred VA `0x14158a6e0`

Analysis labels recorded in the original sources are `FUN_14158a6e0`.

Recorded scope — Produce the selected reference integrity indicator

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 15)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 50)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 33)

## RVA 0x01625260

**Final menu capacity check/assignment** · Level C · preferred VA `0x141625260`

Analysis labels recorded in the original sources are `FUN_141625260`.

Recorded scope — Final menu capacity check/assignment

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 6) · `SOR-FN-0071`
- [crew · lifecycle](../experiments/crew/lifecycle.md) (line 18)
  Original report discusses this roster entry under lifecycle.

## RVA 0x018236c0

**Direct serialization edges recovered (exports 36–40) · entry** · Level C · preferred VA `0x1418236c0`

Recorded scope — Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40).

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · current functions](../experiments/crew/current-functions.csv) (line 59)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 62)
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 123)
  Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40).
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 121)

## RVA 0x01825820

**Direct serialization edges recovered (exports 36–40) · entry** · Level C · preferred VA `0x141825820`

Recorded scope — Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40).

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · current functions](../experiments/crew/current-functions.csv) (line 60)
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 120)
  Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40).
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 123)
- [static exhaustion · trace notes](../experiments/static-exhaustion/trace-notes.md) (line 187)
  Original report discusses this roster entry under Fifth trace round.

## RVA 0x018698d0

**Direct serialization edges recovered (exports 36–40) · entry** · Level C · preferred VA `0x1418698d0`

Recorded scope — Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40).

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · current functions](../experiments/crew/current-functions.csv) (line 57)
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 120)
  Original report discusses this roster entry under Direct serialization edges recovered (exports 36–40).
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 144)

## RVA 0x0186b940

**Independent registry boundary and positive unassigned input · entry** · Level C · preferred VA `0x14186b940`

Recorded scope — Original report discusses this roster entry under Independent registry boundary and positive unassigned input.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · current assignments](../experiments/crew/current-assignments.md) (line 183)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 63)
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 136)
  Original report discusses this roster entry under Typed restoration and packed origin (exports 42–49).
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 145)
- [static exhaustion · trace notes](../experiments/static-exhaustion/trace-notes.md) (line 228)
  Original report discusses this roster entry under Sixth trace round: typed load paths and active key.

## RVA 0x018be3e0

**Handle the inspected damage path call** · Level C · preferred VA `0x1418be3e0`

Analysis labels recorded in the original sources are `FUN_1418be3e0`.

Recorded scope — Handle the inspected damage path call

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 81)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 35)

## RVA 0x018be6e0

**Dispatch actor versus destructible reference handling** · Level C · preferred VA `0x1418be6e0`

Analysis labels recorded in the original sources are `FUN_1418be6e0`.

Recorded scope — Dispatch actor versus destructible reference handling

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 75)
- [transport · transit functions](../experiments/cargo-links/transport/transit-functions.csv) (line 148)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 36)

## RVA 0x018c3600

**Type1 abilities: ship Fusion and destination state · entry** · Level C · preferred VA `0x1418c3600`

Analysis labels recorded in the original sources are `FUN_1418c3600`.

Recorded scope — Original report discusses this roster entry under Type1 abilities: ship Fusion and destination state.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 75)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 81)
- [crew skills · native](../experiments/crew-skills/native.md) (line 39)
  Original report discusses this roster entry under Type1 abilities: ship Fusion and destination state.

## RVA 0x018c4f00

**dispatch or queue perk rank transition** · Level B · preferred VA `0x1418c4f00`

Analysis labels recorded in the original sources are `FUN_1418c4f00`.

Recorded scope — dispatch or queue perk rank transition

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 124).

- **Inputs** — Actor; perk; old/new ranks
- **Outputs** — Immediate or queued change
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — 1418c50a0; 1418ccbd0
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 124) · `N123`
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 38)
- [crew skills · native](../experiments/crew-skills/native.md) (line 14)
  Original report discusses this roster entry under Possession, display and effect registration are different.

## RVA 0x018c50a0

**resolved actor rank transition** · Level B · preferred VA `0x1418c50a0`

Analysis labels recorded in the original sources are `FUN_1418c50a0`.

Recorded scope — resolved actor rank transition

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 125).

- **Inputs** — Change record
- **Outputs** — Qualified actor apply/remove
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — 140ca3910
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 125) · `N124`
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 61)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 26)
  Original report discusses this roster entry under Selected rank and load reconstruction.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 31)
- [crew skills · native](../experiments/crew-skills/native.md) (line 14)
  Original report discusses this roster entry under Possession, display and effect registration are different.

## RVA 0x018ccbd0

**Selected rank and load reconstruction · entry** · Level C · preferred VA `0x1418ccbd0`

Recorded scope — Original report discusses this roster entry under Selected rank and load reconstruction.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 5)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 10)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 26)
  Original report discusses this roster entry under Selected rank and load reconstruction.

## RVA 0x018d8ea0

**Entry-storage loss and return · entry** · Level C · preferred VA `0x1418d8ea0`

Recorded scope — Original report discusses this roster entry under Entry-storage loss and return.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 74)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 38)
  Original report discusses this roster entry under Entry-storage loss and return.

## RVA 0x018e17d0

**Entry-storage loss and return · entry** · Level C · preferred VA `0x1418e17d0`

Recorded scope — Original report discusses this roster entry under Entry-storage loss and return.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 39)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 36)
  Original report discusses this roster entry under Entry-storage loss and return.

## RVA 0x018e2540

**Entry-storage loss and return · entry** · Level C · preferred VA `0x1418e2540`

Recorded scope — Original report discusses this roster entry under Entry-storage loss and return.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 40)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 36)
  Original report discusses this roster entry under Entry-storage loss and return.

## RVA 0x018e4540

**Life state, absence and replacement · entry** · Level C · preferred VA `0x1418e4540`

Recorded scope — Original report discusses this roster entry under Life state, absence and replacement.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 13)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 44)
  Original report discusses this roster entry under Life state, absence and replacement.

## RVA 0x01916b30

**Write the Actor private owned-perk channel** · Level C · preferred VA `0x141916b30`

Analysis labels recorded in the original sources are `FUN_141916b30`.

Recorded scope — Write the Actor private owned-perk channel

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · persistence](../experiments/crew-lifecycle/persistence.md) (line 40)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 46)

## RVA 0x01917e40

**Read additional selected actor perk ranks** · Level C · preferred VA `0x141917e40`

Analysis labels recorded in the original sources are `FUN_141917e40`.

Recorded scope — Read additional selected actor perk ranks

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · persistence](../experiments/crew-lifecycle/persistence.md) (line 40)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 87)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 30)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 37)

## RVA 0x019198a0

**Actor finalization and perk-bucket reset** · Level C · preferred VA `0x1419198a0`

Recorded scope — Actor finalization and perk-bucket reset

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 28)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 25)
- [crew lifecycle · report](../experiments/crew-lifecycle/report.md) (line 13)
  Original report discusses this roster entry under report.

## RVA 0x01935370

**active actor entry-point copy** · Level B · preferred VA `0x141935370`

Analysis labels recorded in the original sources are `FUN_141935370`.

Recorded scope — active actor entry-point copy

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 98).

- **Inputs** — Actor; entry point; output list
- **Outputs** — Copied active entry pointers
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Static export only; native routine may allocate lock mutate and notify
- **Mapped edges** — Actor+228 ->+8 ->+480
- **Limits** — No current runtime values; active participant/rank and downstream semantics bounded in production-uncertainties.md
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 98) · `N97`
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 20) · Copy active actor perk entries
- [inorganic extractors · production native](../experiments/inorganic-extractors/production-native.md) (line 88) · Copy active perk entry array
  Provides the actor's active entry-point rows to the evaluator.
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 12)

## RVA 0x01936490

**Entry-storage loss and return · entry** · Level C · preferred VA `0x141936490`

Recorded scope — Original report discusses this roster entry under Entry-storage loss and return.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 42)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 36)
  Original report discusses this roster entry under Entry-storage loss and return.

## RVA 0x01948250

**Entry-storage loss and return · entry** · Level C · preferred VA `0x141948250`

Recorded scope — Original report discusses this roster entry under Entry-storage loss and return.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 75)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 38)
  Original report discusses this roster entry under Entry-storage loss and return.

## RVA 0x01954810

**actor perk rank update** · Level B · preferred VA `0x141954810`

Analysis labels recorded in the original sources are `FUN_141954810`.

Recorded scope — actor perk rank update

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 121).

- **Inputs** — Actor; perk; requested rank
- **Outputs** — Stored rank and change event
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — 1412b5c60; 1418c4f00
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 121) · `N120`
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 61)
- [crew skills · native](../experiments/crew-skills/native.md) (line 14)
  Original report discusses this roster entry under Possession, display and effect registration are different.

## RVA 0x01955080

**actor effective perk rank lookup** · Level B · preferred VA `0x141955080`

Analysis labels recorded in the original sources are `FUN_141955080`.

Recorded scope — actor effective perk rank lookup

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 122).

- **Inputs** — Actor; perk
- **Outputs** — Base NPC first then additional record
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — Actor+98/+250; actor+360
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 122) · `N121`
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 4)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 30)
  Original report discusses this roster entry under Selected rank and load reconstruction.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 25)
- [shared outpost storage · functions](../experiments/shared-outpost-storage/functions.csv) (line 41)
- [shared outpost storage · prerequisites](../experiments/shared-outpost-storage/prerequisites.md) (line 56)
  Original report discusses this roster entry under Definition to menu and accepted build.

## RVA 0x01955350

**Read the active actor perk bucket** · Level C · preferred VA `0x141955350`

Recorded scope — Read the active actor perk bucket

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 20)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 66)

## RVA 0x01955400

**Replay base and added actor perk ranks** · Level C · preferred VA `0x141955400`

Recorded scope — Replay base and added actor perk ranks

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 20)
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 65)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 28)
  Original report discusses this roster entry under Selected rank and load reconstruction.
- [crew lifecycle · report](../experiments/crew-lifecycle/report.md) (line 13)
  Original report discusses this roster entry under report.

## RVA 0x01955f80

**Selected rank and load reconstruction · entry** · Level C · preferred VA `0x141955f80`

Recorded scope — Original report discusses this roster entry under Selected rank and load reconstruction.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 11)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 32)
  Original report discusses this roster entry under Selected rank and load reconstruction.

## RVA 0x019776f0

**Deployment allowance and ordinary beacon operation · entry** · Level C · preferred VA `0x1419776f0`

Analysis labels recorded in the original sources are `FUN_1419776f0`.

Recorded scope — Original report discusses this roster entry under Deployment allowance and ordinary beacon operation.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 57)
- [limits · functions](../experiments/limits/functions.csv) (line 20)
- [limits · native](../experiments/limits/native.md) (line 141)
  Original report discusses this roster entry under Deployment allowance and ordinary beacon operation.
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 64)
- [locations outpost · functions](../experiments/locations-outpost/functions.csv) (line 105)

## RVA 0x019ae970

**Apply a reference actor-value modifier** · Level C · preferred VA `0x1419ae970`

Recorded scope — Apply a reference actor-value modifier

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 87)

## RVA 0x019ce030

**Process an admitted defense target** · Level C · preferred VA `0x1419ce030`

Analysis labels recorded in the original sources are `FUN_1419ce030`.

Recorded scope — Process an admitted defense target

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · attacks](../experiments/outpost-defense/attacks.md) (line 64–66)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 40)

## RVA 0x019f7b80

**Selected rank and load reconstruction · entry** · Level C · preferred VA `0x1419f7b80`

Recorded scope — Original report discusses this roster entry under Selected rank and load reconstruction.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 71)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 28)
  Original report discusses this roster entry under Selected rank and load reconstruction.
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 36)
  Original report discusses this roster entry under Entry-storage loss and return.

## RVA 0x019f8f40

**Entry-storage loss and return · destructor** · Level C · preferred VA `0x1419f8f40`

Recorded scope — Original report discusses this roster entry under Entry-storage loss and return.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 48)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 36)
  Original report discusses this roster entry under Entry-storage loss and return.

## RVA 0x01a154d0

**Read a companion Actor suffix field** · Level C · preferred VA `0x141a154d0`

Analysis labels recorded in the original sources are `FUN_141a154d0`.

Recorded scope — Read a companion Actor suffix field

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew skills · lifecycle](../experiments/crew-skills/lifecycle.md) (line 45)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 60)

## RVA 0x01a4b590

**Selected rank and load reconstruction · wrapper** · Level C · preferred VA `0x141a4b590`

Recorded scope — Original report discusses this roster entry under Selected rank and load reconstruction.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 76)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 28)
  Original report discusses this roster entry under Selected rank and load reconstruction.

## RVA 0x01b30b30

**Combat and non-effect role metadata · entry** · Level C · preferred VA `0x141b30b30`

Analysis labels recorded in the original sources are `FUN_141b30b30`.

Recorded scope — Original report discusses this roster entry under Combat and non-effect role metadata.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 63)
- [crew skills · native](../experiments/crew-skills/native.md) (line 53)
  Original report discusses this roster entry under Combat and non-effect role metadata.
- [crew skills · processes](../experiments/crew-skills/processes.md) (line 17)
  Original report discusses this roster entry under processes.

## RVA 0x01f76dd0

**NPC script bit 9/slot 9 source selection and original-handle binding** · Level C · preferred VA `0x141f76dd0`

Recorded scope — NPC script bit 9/slot 9 source selection and original-handle binding

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 51)
- [robots · lifecycle](../experiments/robots/lifecycle.md) (line 20)
  Original report discusses this roster entry under lifecycle.

## RVA 0x01fb5de0

**NPC form callback invokes inherited script binding** · Level C · preferred VA `0x141fb5de0`

Recorded scope — NPC form callback invokes inherited script binding

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 54)
- [robots · lifecycle](../experiments/robots/lifecycle.md) (line 20)
  Original report discusses this roster entry under lifecycle.

## RVA 0x01fc48e0

**Actor AddPerk callback** · Level B · preferred VA `0x141fc48e0`

Analysis labels recorded in the original sources are `FUN_141fc48e0`.

Recorded scope — Actor AddPerk callback

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 120).

- **Inputs** — Actor; perk; notify
- **Outputs** — Rank change request
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — 141954810
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 120) · `N119`

## RVA 0x01fc7f50

**Handle the IsBleedingOut native callback** · Level C · preferred VA `0x141fc7f50`

Recorded scope — Handle the IsBleedingOut native callback

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 44)

## RVA 0x01fc7fb0

**Return the script-facing actor death predicate** · Level C · preferred VA `0x141fc7fb0`

Recorded scope — Return the script-facing actor death predicate

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 44)

## RVA 0x01fd1470

**Handle the IsUnconscious native callback** · Level C · preferred VA `0x141fd1470`

Recorded scope — Handle the IsUnconscious native callback

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 44)

## RVA 0x02008540

**Add an unassigned actor to availability** · Level B · preferred VA `0x142008540`

Analysis labels recorded in the original sources are `FUN_142008540`.

Admits a nonnull actor without current assignment to the available roster.

The crew report maps this routine to available actor registration and describes the null and currently-assigned rejection conditions. It is separate from transfer into a destination E2. Its historic crew-table ID `SOR-FN-0062` collides with the Workshop region callback's register ID. The native declaration, return and all add/remove symmetry remain unknown.

Original records

- [crew · functions](../experiments/crew/functions.csv) (line 66)
- [crew · functions](../experiments/crew/functions.csv) (line 66) · `SOR-FN-0062` · Add available unassigned actor
- [crew · report](../experiments/crew/report.md) (line 67)

## RVA 0x0200f5a0

**Continue available and assigned crew bookkeeping** · Level C · preferred VA `0x14200f5a0`

Analysis labels recorded in the original sources are `FUN_14200f5a0`.

Recorded scope — Continue available and assigned crew bookkeeping

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew · report](../experiments/crew/report.md) (line 70)
- [crew · functions](../experiments/crew/functions.csv) (line 67)

## RVA 0x02065260

**Execute the damage object functor** · Level C · preferred VA `0x142065260`

Analysis labels recorded in the original sources are `FUN_142065260`.

Recorded scope — Execute the damage object functor

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 74)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 44)

## RVA 0x02068d70

**Bridge script AssignCrew with admission bypass** · Level B · preferred VA `0x142068d70`

Analysis labels recorded in the original sources are `FUN_142068d70`.

Obtains the owner's E2 and calls shared membership insertion with its bypass option.

This script bridge is exercised by the mapped robot placement path. It creates or obtains the owner's E2, then calls `0x1404076b0` with bypass. The documented void return cannot establish ordinary UI admission. Construction owner and crew membership remain separate, and membership alone does not confer active A1 or DB entries. Full ABI details remain unknown.

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 112).

- **Inputs** — Reference; actor
- **Outputs** — Calls crew insertion
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — 140408a50; 1404076b0
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 112) · `N111` · AssignCrew native script callback
- [crew · capacity](../experiments/crew/capacity.md) (line 43)
  Obtains the owner's E2 and calls shared membership insertion with its bypass option.
- [robots · effects](../experiments/robots/effects.md) (line 39)
  Obtains the owner's E2 and calls shared membership insertion with its bypass option.
- [robots · functions](../experiments/robots/functions.csv) (line 5) · AssignCrew capacity bypass bridge
- [robots · lifecycle](../experiments/robots/lifecycle.md) (line 35)
  Obtains the owner's E2 and calls shared membership insertion with its bypass option.
- [crew · functions](../experiments/crew/functions.csv) (line 75)
- [crew · functions](../experiments/crew/functions.csv) (line 99)
- [robots · effects](../experiments/robots/effects.md) (line 41)
  Original report discusses this roster entry under effects.

## RVA 0x0206b1b0

**Dispatch the damage-object operation** · Level C · preferred VA `0x14206b1b0`

Analysis labels recorded in the original sources are `FUN_14206b1b0`.

Recorded scope — Dispatch the damage-object operation

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 74)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 45)

## RVA 0x0206f3b0

**GetAllCrewMembers callback** · Level B · preferred VA `0x14206f3b0`

Analysis labels recorded in the original sources are `FUN_14206f3b0`.

Recorded scope — GetAllCrewMembers callback

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 115).

- **Inputs** — Owner reference
- **Outputs** — Resolved E2 actor array
- **Conditions** — Pinned build; valid native context; no invocation authority
- **Effects** — Export only; native execution may lock allocate mutate or notify
- **Mapped edges** — 1417eb150
- **Limits** — Normal traced selection/completion paths; runtime actuals and full startup/template/override closure not tested
- **Source assessment** — STATIC instructions/decompilation; scoped interpretation REVIEW-REQUIRED

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 115) · `N114`

## RVA 0x020c02b0

**Ordinary causal trace · entry** · Level C · preferred VA `0x1420c02b0`

Analysis labels recorded in the original sources are `FUN_1420c02b0`.

Recorded scope — Original report discusses this roster entry under Ordinary causal trace.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · attacks](../experiments/outpost-defense/attacks.md) (line 65)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 48)

## RVA 0x021159b0

**AA: ship capacity, not a CONT CarryWeight aura · entry** · Level C · preferred VA `0x1421159b0`

Analysis labels recorded in the original sources are `FUN_1421159b0`.

Recorded scope — Original report discusses this roster entry under AA: ship capacity, not a CONT CarryWeight aura.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 33)
- [crew skills · native](../experiments/crew-skills/native.md) (line 47)
  Original report discusses this roster entry under AA: ship capacity, not a CONT CarryWeight aura.

## RVA 0x0212d230

**Resolve the ship-associated actor** · Level C · preferred VA `0x14212d230`

Analysis labels recorded in the original sources are `FUN_14212d230`.

Recorded scope — Resolve the ship-associated actor

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [crew skills · native](../experiments/crew-skills/native.md) (line 47)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 45)

## RVA 0x021b03c0

**Build-mode repair wrapper** · Level C · preferred VA `0x1421b03c0`

Analysis labels recorded in the original sources are `FUN_1421b03c0`.

Recorded scope — Build-mode repair wrapper

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 115)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 49)

## RVA 0x021b10b0

**successful construction inserts item** · Level C · preferred VA `0x1421b10b0`

Analysis labels recorded in the original sources are `FUN_1421b10b0`.

Recorded scope — successful construction inserts item

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 29)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 94)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 152)
- [limits · functions](../experiments/limits/functions.csv) (line 58)
- [limits · native](../experiments/limits/native.md) (line 59)
  Original report discusses this roster entry under Selected-outpost scope and updates.
- [robots · limits](../experiments/robots/limits.md) (line 64)
  Original report discusses this roster entry under Why the set is per outpost and how it changes.

## RVA 0x021b2360

**normal build requires candidate status 2** · Level C · preferred VA `0x1421b2360`

Analysis labels recorded in the original sources are `FUN_1421b2360`.

Recorded scope — normal build requires candidate status 2

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 42)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 92)
- [build budget · report](../experiments/build-budget/report.md) (line 53)
  Original report discusses this roster entry under Causal path.
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 135)
- [limits · functions](../experiments/limits/functions.csv) (line 5)

## RVA 0x021b2e20

**normal attempt requires status 2** · Level C · preferred VA `0x1421b2e20`

Analysis labels recorded in the original sources are `FUN_1421b2e20`.

Recorded scope — normal attempt requires status 2

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 43)
- [robots · functions](../experiments/robots/functions.csv) (line 47)
- [workshop origin · native map](../experiments/workshop-origin/native-map.csv) (line 4) · `SOR-FN-0041` · reset
  create-enabled accessor then zero compensation
- [build budget · functions](../experiments/build-budget/functions.csv) (line 93)
- [build budget · report](../experiments/build-budget/report.md) (line 53)
  Original report discusses this roster entry under Causal path.
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 136)
- [limits · functions](../experiments/limits/functions.csv) (line 6)
- [spatial placement · functions](../experiments/spatial-placement/functions.csv) (line 107)
- [spatial placement · persistence](../experiments/spatial-placement/persistence.md) (line 17)
  Original report discusses this roster entry under persistence.
- [docs · function register](../function-register.md) (line 121) · `SOR-FN-0041`
  Original group scope — Accumulating endpoint-subtraction writer, callers and separate reset; endpoint labels inferred

## RVA 0x021b6be0

**reset clears item caches** · Level C · preferred VA `0x1421b6be0`

Recorded scope — reset clears item caches

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 25)

## RVA 0x021ba8a0

**exit clears selected item set** · Level C · preferred VA `0x1421ba8a0`

Recorded scope — exit clears selected item set

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 24)

## RVA 0x021c6890

**item set insertion and secondary maps** · Level C · preferred VA `0x1421c6890`

Recorded scope — item set insertion and secondary maps

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 34)
- [robots · functions](../experiments/robots/functions.csv) (line 38)
- [limits · functions](../experiments/limits/functions.csv) (line 61)
- [limits · functions](../experiments/limits/functions.csv) (line 62)
- [robots · limits](../experiments/robots/limits.md) (line 67)
  Original report discusses this roster entry under Why the set is per outpost and how it changes.

## RVA 0x021c6b90

**item and reference map removal** · Level C · preferred VA `0x1421c6b90`

Recorded scope — item and reference map removal

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 26)
- [limits · functions](../experiments/limits/functions.csv) (line 55)
- [limits · native](../experiments/limits/native.md) (line 61)
  Original report discusses this roster entry under Selected-outpost scope and updates.

## RVA 0x021c6d00

**rebuild member mappings** · Level C · preferred VA `0x1421c6d00`

Recorded scope — rebuild member mappings

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 30)
- [robots · functions](../experiments/robots/functions.csv) (line 35)

## RVA 0x021c6e30

**remove member mappings** · Level C · preferred VA `0x1421c6e30`

Recorded scope — remove member mappings

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 31)
- [robots · functions](../experiments/robots/functions.csv) (line 36)

## RVA 0x021c6f90

**selected-owner reverse 4D WorkshopItem registry rebuild** · Level C · preferred VA `0x1421c6f90`

Recorded scope — selected-owner reverse 4D WorkshopItem registry rebuild

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 23)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 37)
- [build budget · native](../experiments/build-budget/native.md) (line 148)
  Original report discusses this roster entry under Mutations, movement and restored state.
- [limits · functions](../experiments/limits/functions.csv) (line 8)
- [limits · native](../experiments/limits/native.md) (line 51)
  Original report discusses this roster entry under Selected-outpost scope and updates.
- [robots · limits](../experiments/robots/limits.md) (line 56)
  Original report discusses this roster entry under Why the set is per outpost and how it changes.

## RVA 0x021c71b0

**resolve/deduplicate/qualify construction representatives** · Level C · preferred VA `0x1421c71b0`

Recorded scope — resolve/deduplicate/qualify construction representatives

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 27)
- [robots · functions](../experiments/robots/functions.csv) (line 32)
- [robots · functions](../experiments/robots/functions.csv) (line 46)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 61)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 82)
- [build budget · native](../experiments/build-budget/native.md) (line 148)
  Original report discusses this roster entry under Mutations, movement and restored state.
- [limits · functions](../experiments/limits/functions.csv) (line 56)
- [limits · functions](../experiments/limits/functions.csv) (line 59)
- [limits · functions](../experiments/limits/functions.csv) (line 64)
- [limits · native](../experiments/limits/native.md) (line 54)
  Original report discusses this roster entry under Selected-outpost scope and updates.
- [robots · limits](../experiments/robots/limits.md) (line 59)
  Original report discusses this roster entry under Why the set is per outpost and how it changes.
- [docs · function register](../function-register.md) (line 226) · `SOR-FN-0059`
  Original group scope — Constructed item reconstruction path

## RVA 0x021c77b0

**erase item-set entry** · Level C · preferred VA `0x1421c77b0`

Recorded scope — erase item-set entry

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 28)
- [limits · functions](../experiments/limits/functions.csv) (line 57)
- [limits · native](../experiments/limits/native.md) (line 61)
  Original report discusses this roster entry under Selected-outpost scope and updates.

## RVA 0x021c7990

**set insertion helper** · Level C · preferred VA `0x1421c7990`

Recorded scope — set insertion helper

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 41)

## RVA 0x021dcb10

**count>=nonnegative floor(global+48) at frame offset 61F** · Level C · preferred VA `0x1421dcb10`

Analysis labels recorded in the original sources are `FUN_1421dcb10`.

Recorded scope — count>=nonnegative floor(global+48) at frame offset 61F

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 16)
- [robots · functions](../experiments/robots/functions.csv) (line 18)
- [robots · functions](../experiments/robots/functions.csv) (line 20)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 21)
- [build budget · native](../experiments/build-budget/native.md) (line 93)
  Original report discusses this roster entry under Allowance, admission and action.
- [build budget · report](../experiments/build-budget/report.md) (line 52)
  Original report discusses this roster entry under Causal path.
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 133)
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 233)
- [containers displays · native](../experiments/containers-displays/native.md) (line 234)
  Original report discusses this roster entry under New construction suppresses default stock.
- [limits · functions](../experiments/limits/functions.csv) (line 3)
- [limits · native](../experiments/limits/native.md) (line 35)
  Original report discusses this roster entry under Recipe limit, displayed count and accepted construction.
- [shared outpost storage · functions](../experiments/shared-outpost-storage/functions.csv) (line 6)
- [shared outpost storage · prerequisites](../experiments/shared-outpost-storage/prerequisites.md) (line 53)
  Original report discusses this roster entry under Definition to menu and accepted build.
- [shared outpost storage · prerequisites](../experiments/shared-outpost-storage/prerequisites.md) (line 62)
  Original report discusses this roster entry under Definition to menu and accepted build.
- [spatial placement · functions](../experiments/spatial-placement/functions.csv) (line 6)

## RVA 0x021dd600

**placement owner/actor/slot/event path** · Level C · preferred VA `0x1421dd600`

Analysis labels recorded in the original sources are `FUN_1421dd600`.

Recorded scope — placement owner/actor/slot/event path

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 2)
- [construction variants · functions](../experiments/construction-variants/functions.csv) (line 81)
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 83)
- [containers displays · native](../experiments/containers-displays/native.md) (line 250)
  Original report discusses this roster entry under New construction suppresses default stock.
- [crew · functions](../experiments/crew/functions.csv) (line 83)
- [limits · functions](../experiments/limits/functions.csv) (line 50)
- [limits · native](../experiments/limits/native.md) (line 60)
  Original report discusses this roster entry under Selected-outpost scope and updates.
- [robots · limits](../experiments/robots/limits.md) (line 66)
  Original report discusses this roster entry under Why the set is per outpost and how it changes.
- [docs · function register](../function-register.md) (line 226) · `SOR-FN-0058`
  Original group scope — Saved owner or membership reconstruction path

## RVA 0x021de3f0

**invoke item virtual method at +A0 then placement notifications** · Level C · preferred VA `0x1421de3f0`

Analysis labels recorded in the original sources are `FUN_1421de3f0`.

Recorded scope — invoke item virtual method at +A0 then placement notifications

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 33)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 19)
- [build budget · report](../experiments/build-budget/report.md) (line 54)
  Original report discusses this roster entry under Causal path.
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 227)
- [containers displays · native](../experiments/containers-displays/native.md) (line 249)
  Original report discusses this roster entry under New construction suppresses default stock.
- [limits · functions](../experiments/limits/functions.csv) (line 60)
- [limits · native](../experiments/limits/native.md) (line 59)
  Original report discusses this roster entry under Selected-outpost scope and updates.
- [robots · limits](../experiments/robots/limits.md) (line 64)
  Original report discusses this roster entry under Why the set is per outpost and how it changes.
- [shared outpost storage · functions](../experiments/shared-outpost-storage/functions.csv) (line 71)

## RVA 0x021de660

**deconstruction path** · Level C · preferred VA `0x1421de660`

Analysis labels recorded in the original sources are `FUN_1421de660`.

Recorded scope — deconstruction path

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 3)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 20)
- [build budget · native](../experiments/build-budget/native.md) (line 129)
  Original report discusses this roster entry under Mutations, movement and restored state.
- [build budget · report](../experiments/build-budget/report.md) (line 54)
  Original report discusses this roster entry under Causal path.
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 195)
- [containers displays · native](../experiments/containers-displays/native.md) (line 297)
  Original report discusses this roster entry under New construction suppresses default stock.
- [crew · functions](../experiments/crew/functions.csv) (line 82)
- [limits · functions](../experiments/limits/functions.csv) (line 51)
- [limits · native](../experiments/limits/native.md) (line 61)
  Original report discusses this roster entry under Selected-outpost scope and updates.
- [robots · limits](../experiments/robots/limits.md) (line 71)
  Original report discusses this roster entry under Why the set is per outpost and how it changes.
- [docs · function register](../function-register.md) (line 226) · `SOR-FN-0058`
  Original group scope — Saved owner or membership reconstruction path

## RVA 0x021e3f50

**Ordinary outpost repair service** · Level C · preferred VA `0x1421e3f50`

Analysis labels recorded in the original sources are `FUN_1421e3f50`.

Recorded scope — Ordinary outpost repair service

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 115)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 50)
- [shared outpost storage · consumers](../experiments/shared-outpost-storage/consumers.md) (line 151)
  Original report discusses this roster entry under Other consumers.
- [shared outpost storage · functions](../experiments/shared-outpost-storage/functions.csv) (line 7)

## RVA 0x021e9b50

**Repair service continuation** · Level C · preferred VA `0x1421e9b50`

Analysis labels recorded in the original sources are `FUN_1421e9b50`.

Recorded scope — Repair service continuation

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [outpost defense · integrity](../experiments/outpost-defense/integrity.md) (line 120)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 51)

## RVA 0x027fcc10

**snapshot handle-keyed script list** · Level C · preferred VA `0x1427fcc10`

Recorded scope — snapshot handle-keyed script list

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 52)

## RVA 0x027fd870

**install handle-keyed script list; shared VMAD setter** · Level C · preferred VA `0x1427fd870`

Recorded scope — install handle-keyed script list; shared VMAD setter

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 53)

## RVA 0x027ff160

**VMAD parser feeds script-list setter** · Level C · preferred VA `0x1427ff160`

Recorded scope — VMAD parser feeds script-list setter

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [robots · functions](../experiments/robots/functions.csv) (line 55)
