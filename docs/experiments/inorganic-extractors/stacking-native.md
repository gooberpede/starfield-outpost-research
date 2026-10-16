# Native selection and registration contract

Bethesda retail 1.16.244.0, executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Every address is hexadecimal static VA, image base `140000000`; subtract that
base for RVA. None is a current runtime address or file offset. Existing
[timer arithmetic](production-native.md) and [central register](../native-availability-map/functions.csv)
remain the shared reference. New local exports are
`.local-work/recon/e1-stacking-NN.tsv`, pinned in [sources](stacking-sources.csv).
Ghidra reads existing state with readOnly/noanalysis; no native code is invoked.

## Actor list: ownership, insertion and consumption

Export 07, `140408a50`: get ExtraE2 from reference+`c8`; optionally allocate
30 bytes, set vtable `144b0a9d8` (**CrewExtraData**), type byte +12=E2,
zero count/capacity/data at +18/+1c/+20 and record owning FormID at +28.
This is distinct from ExtraFollower type 1B, ruled out by constructors
`14051c5d0`/`14051c800` in export 04. Earlier “ExtraCrew” symbol absence was a
name mismatch, not absence of a crew structure.

ObjectReference.AssignCrew registration in export 05 binds `142068d70`.
Export 06 shows that callback gets/creates CrewExtraData and calls
`1404076b0`. Export 08's full insertion function:

1. Resolves the actor's handle and scans existing +20 uint32 handles. A matching
   handle returns immediately. A different actor with the same perk is not a match.
2. Depending on its bypass argument, checks capacity/assignment predicates via
   `1404074f0` (export 12). Ordinary menu assignment in `141625260` (09) also
   qualifies capacity before insertion. The script callback uses the bypass;
   this does not mean that every assignment route ignores capacity.
3. Resolves the owner recorded at +28, removes the actor from a different owner's
   E2 list through `140407a10`, appends one four-byte handle, sets the assignment
   relationship through `140ba0d40`, then notifies crew/perk consumers.

`140407cb0` (10) migrates selected handle groups through the same insertion
function. Save restoration has a distinct `1404089e0` reader (12), reached by
existing `140521620` case E2 in owned `workshop-origin-09.tsv`; it must not be
silently equated with the normal insertion invariant. Malformed/exceptional
restored lists and startup reconstruction are outside the proven uniqueness claim.

GetAllCrewMembers registration `14209ff50` (04) binds `14206f3b0` (05), which
reads this same E2 list and resolves actors via `1417eb150` (08). Separately,
the established scheduler `140f7ef20` passes owner E2 to `140f7bd20`. That timer
walks the actual handles, resolves each actor, skips virtual +868 true and
requires positive Health. Health binding is now explicit: `14049a430` (07)
returns registry `1461de020`; initializer `140d96b20` (08), instructions
`140d971f6`–`140d97209`, registers string “Health” at `144c0c0b0` and stores its
AV pointer at registry+108. The virtual predicate's broader meaning remains
unnamed here. The timer calls `140c94060(A1, actor, context, interval*)` for
each eligible actor, then for the player. No running maximum is updated in that
loop; the positive Health threshold stays zero.

## Highest-rank alternative and assignment side effects

`1404095c0` (03) really does select a qualifying highest entry rank across a crew
list, then evaluates the chosen actor's entries. Wrappers `140409f10`,
`140409f60`, `140409f80` (06) reach it. This is a real alternative path, not a
fictional rule, but `140f7bd20` directly uses the ordinary per-actor dispatcher.
Do not transfer this selector's rule to production timers or generalize timer
stacking to every crew bonus.

Insertion also reaches `140408bb0` (09) → `14040a230` (10) → `14040a9d0` (11).
These inspect crew-flagged perks (perk+63 mask 8). The competing-crew suppression
branch in `14040a9d0` requires entry virtual +20 to return **type 1**, along with
matching rank and environment. The traced A1 entries are **type 2**. Helper
`14040a840` (13) compares competing ranks within that type-1 path. This provides
a concrete boundary for the otherwise plausible objection that assignment
silently applies a universal strongest-only rule. It does not implement such a
rule for the type-2 timer entries inspected here.

The ordinary dispatcher also checks crew environment: `140c93cf0` (prior
production export 02) examines parent perk+63 mask 8 and +62 category, resolves
the actor's assignment relationship and requires the matching environment.
Inspected outpost crew and robot timer perks have root DATA category 2/flag 8.
Merely owning a crew perk away from an appropriate assignment is insufficient.

## Active perk entries and rank transitions

Actor.AddPerk binding `141fcc740` (05) → `141fc48e0` (07) → `141954810` (08).
`141955080` (09) looks up base-NPC perk rank first, then the actor's additional
perk records under the actor+36c lock. `1412b5c60` (09) stores one rank per perk
record, bounds it by the perk's rank-vector length and increments a zero-request
from the current rank. It does not create one independent actor bonus per rank.

`141954810` sends old/new ranks through `1418c4f00` (09). This either dispatches
directly or queues `1418ccbd0`; both reach `1418c50a0` (10), which resolves and
qualifies the actor, then calls `140ca3910` (11). This last function walks the
perk's rank objects, stride 68, and their entries:

- `entry+8 + 1 == old rank`: virtual +70 unregisters the entry;
- `entry+8 + 1 == new rank`: virtual +68 registers the entry.

For BGSEntryPointPerkEntry, vtable `144bd2870` +68=`140ca1a20` (03) and
+70=`140ca1bd0` (12). Registration allocates 255 entry-point buckets, stride 10,
at actor+228 → +8 → +480 under lock +478, and inserts type-2 entries in the
bucket selected by entry+10. Removal searches for that exact entry pointer and
erases it. `140ca4be0` (04) inserts using comparator `140ca3670` (instruction
window in 05): priority +9 ascending, rank +8 descending when priority ties.
Equality in the comparator is not an instruction to discard different perks.

Existing `141935370` copies the resulting active bucket; `140c93cf0` checks
context/predicates and calls operation 3 (`140c94430`) once per qualifying entry.
Each operation multiplies the current binary32 interval. Different perks can
contribute; old ranks are explicitly removed during normal transitions.
`141954f20` (12) handles cache/state follow-up, with `141958550` (13) updating
other actor state; it does not contain an all-prior-ranks registration loop.
Export 13's `1413da8f0` is a separate power-upgrade caller of the same transition
routine, not an actor-startup oracle. Full startup/load hook closure is not claimed.

Rank replacement here describes a settled normal transition. Per-entry bucket
locking does not establish a coherent snapshot across the entire remove/add
sequence. No claim is made that a concurrent consumer can never see an
intermediate state during a rank change.

No native call, hook, current actor state, save restore or gameplay measurement
was performed. These routines mutate state when the game invokes them; their
description is OBSERVED-INTERNAL, not a safe integration API.
