# Clearing, restoration and reappearance

[Answer](report.md), [native](native.md), [saved comparisons](saves.md).
Native addresses use the pinned static VA domain in functions.csv.

| State | Persistence class | Evidence / scope |
|---|---|---|
| Constructed root, explicit owner edge, initial local XYZ | PERSISTED | Six-save direct root/membership/position reads, derived roots.csv |
| Radius 150 | DEFINITION-DERIVED for ordinary beacon | ACTI `002c60e9`, PRPS entry for AV `00063fc5`; no explicit radius BF override decoded on these beacons |
| Drawn clipped border | RECONSTRUCTED in inspected ordinary route | 140f49440→48a60→47de0/48480; selected location/grid inputs required |
| Candidate collision result, physics hit shape and error | TRANSIENT | preview validator/collector; rejected preview need not be a saved reference |
| Preview clearing sets, fading scene nodes | TRANSIENT | clearing sets at `frame + 0x1a8`, functions 140f2ffb0/3a640/412c0; restored as candidate membership changes |
| Confirmed reference bulldozed state | PERSISTED, scene application reconstructed | mask `0x04` at reference offset `0xd3`; change mask `0x01000000`; native commitment/load and actual six-save channel observations |
| Particular pictured rock's persisted flag and identity | UNCLASSIFIED | no exact photograph/reference join |
| Historical returned rock's cause | OPEN | no before/after travel or reload incident in these six saves |

`1421b2e20` admits success status `0x02`, creates the item, then calls
`140f30820`, passing the clearing state at `frame + 0x1a8`. For selected resolved
references that are not already bulldozed, that function hides/removes scene
participation, sets mask `0x04` in the reference byte at offset `0xd3`, and calls
the virtual method at vtable offset `0xb8` with change mask `0x01000000`.
It also handles certain
special base types separately. `141803ba0` names this exact mask
CHANGE_REFR_WORKSHOP_BULLDOZED. This differs from the saved form flags for
disabled (mask `0x00000800`) and deleted (mask `0x20`).
Saved change flags and saved form flags are distinct domains.

The post-load/reference restoration path `140b2d0c0` examines change-state bit 24
(mask `0x01000000`). It restores mask `0x04` at reference offset `0xd3`, or calls
`140f30380` when an earlier bulldozed reference is no longer marked.
`140f30380` clears the runtime bit and removes the saved change through the
virtual method at vtable offset `0xc0`, passing mask `0x01000000` and restoring scene/registration
as appropriate. The transient frame clearing reconciliation in `140f412c0`
restores visibility without being equivalent to that permanent-state removal.
Ordinary move/delete reevaluation also has a permanent restoration route:
`1421d69b0→1421ea3a0` collects nearby already-bulldozed references;
`1421d6ad0` revisits potentially overlapping construction items; the selected
restore set is processed by `1421d6fd0→140f30380`. Calls from ordinary move
`1421b1450` and delete `1421de660` are independently in n023/n018 xrefs.
These are intended restoration operations, not proof of a travel bug.

In the physical saves, REFR rows carrying mask `0x01000000` number 0/1/4 and
0/1/12 across the two sequences. Most have conditional case 7, no inline base/XYZ
and a one-byte body containing `00`. That body is not a
false bulldozed Boolean: the positive channel is in the change mask. It is not
safe to assign a mesh or object class from the remaining parent/self queues.
Save36 also has two rows with additional state bits; their full raw framed
records are retained. A mask/channel count is neither an object-category census
nor a photograph identity proof.

The save sequences are construction checkpoints, not no-action controls or
travel/reload tests. Across Save31→33, 1,179 records appear, 1,147 disappear and 5,438
retained IDs change body/queues/flags; therefore a whole-save diff cannot isolate
one rock intervention. Save35→36 has 21 new and 1,715 changed retained IDs.
These controls support positive membership/state observations and ordinary
construction correspondence; they cannot establish historical reappearance.

## Minimal consequential discriminator, proposal only

Under a separately approved live brief, identify one eligible rock reference
and candidate, capture its pivot/bounds, clearing-set membership, bulldozed flag
at reference offset `0xd3`, and
change-state identity before preview, after confirmation, after save/reload and
after one cell reentry. Preserve source saves and flush observations. If the
same saved reference retains change-state bit 24 and the runtime bulldozed flag
at reference offset `0xd3` but returns visibly/collidably, investigate
scene application; if it loses the bit, trace restoration; if identity changes,
investigate generated-reference resolution. If only preview was confirmed
visually and no permanent flag was set, restoration may be ordinary behavior.
No observer, save request, gameplay or new capture was commissioned here.
