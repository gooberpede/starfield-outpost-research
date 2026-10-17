# Saved item inventories and object joins

[Report](report.md), [native wire contract](native.md),
[reader](../../../research/s1-storage/saved.py). All offsets below are decimal
**decoded logical save-stream offsets**, not compressed-file offsets or native VAs.
Dynamic identities are save-era resolved FormIDs; no runtime handle is substituted.

Final receipts in ignored `.local-work/s1-storage/` use four distinct originals:

| Sample / final receipt | Original SHA-256 | Candidate rows; decoded / no inventory branch / stack gap / leading gap |
|---|---|---|
| HIST-0036 / saved05.json | 7e6642f49774c9827fe5230f8cdccdff6b00e4af8738dac11018b56e7ffeca37 | 382; 279 / 86 / 10 / 7 |
| mature-Save52 / saved06.json | 6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8 | See final receipt; same candidate/status counts as H36 |
| HIST-0077 / saved03.json | 3830eb374f086bece85ca3e92ff2d13a3d5aa811193f0c2e583c4564000551bc | 254; 180 / 57 / 8 / 9 |
| HIST-0083 / saved04.json | babba0dd0e1822d7afebea5ddee4461392070c25423daa494910fee831f07caa | See final receipt; same candidate/status counts as H36 |

These are observational historical samples, not controlled successive saves or
independent gameplay trials. Matching counts do not establish identical originals.
Originals are hashed before and after; strict header/decompression/R3 framing and
both-drive 40 GB guards are retained. Temporary decoded scratch is cleaned.
All original/private paths, full queues and raw data remain local.

The candidate census selects bases; `reference_prefix` independently resolves each
supported inline base from the actual reference queue. Counted extras then locate
inventory without searching for plausible item bytes. Explicit Extra4C
`WorkshopItemKeyword` edges supply owner joins; definitions do not prove ownership.
Supported base/owner/quantity findings are a positive subset, not a complete
enumeration of all construction roots or every load representation.

## Object-level evidence

H36 examples below have native-backed inventory rows with empty stack extras.
The native row grammar supports signed counts; values below are observed positive
counts, not inferred capacities. Base form identity is from the actual reference
prefix, product identity from the item queue at the serialization cursor.

| Class | Reference / base | Record / inventory start | Saved contents |
|---|---|---|---|
| Solid small | ff018b64 / 23aed9 | 2982305 / 2982405 | MISC 00557f x150 |
| Gas small | ff018b66 / 273199 | 2982758 / 2982858 | MISC 00557c x150 |
| Liquid small | ff018b61 / 2c5913 | 2981471 / 2981571 | MISC 0057df x94 |
| Warehouse small | ff01a9f3 / 29b453 | 3076595 / 3076695 | MISC 202f5a x1 |
| Mixed warehouse | ff02c339 / 29b453 | 3870343 / 3870446 | MISC 246b77 x41 and 246b73 x3 |
| Atmospheric water | ff01a4fb / 06ac92 | 3034154 / 3034279 | Water MISC 005591 x20 |
| Greenhouse | ff01a5c5 / 2965f7 | 3058481 / 3058629 | MISC 0055ba x15 |
| Fabricator | ff0382cf / 3a8619 | 4658488 / 4658628 | Product MISC 203eb2 x4 |
| Cargo outgoing | ff018b73 / 219171 | 2984588 / 2984703 | MISC 0057df x375 |
| Empty cargo incoming | ff01ac54 / 219173 | 3114381 / 3114500 | Explicit compact item count zero |
| Empty solid store | ff01c792 / 23aed9 | 3184787 / 3184884 | Explicit compact item count zero |
| Fueled pad marker | ff018b69 / 219523 | record 2983622 | No inventory-change branch; **not** an empty inventory proof |

H77 independently joins Iron extractor ff0294fd / base 05ef19 at record 3339175,
inventory 3339286, to Iron MISC 00556e x17. This corroborates the own-reference
output-buffer model beyond the mature H36 snapshot. It is not a production rate.

For H36 ff018b64, Extra4C at 2982400 has keyword `starfield.esm:054ba6`, target
`DYNAMIC:ff04ba51`, mode 0. Native-backed inventory begins at 2982405, with one
item, one empty-extra stack and count 150; item row ends at 2982417. The reference
queue is exhausted there; 269 later body bytes belong to other unparsed channels.
The scoped decoder does not call the whole REFR body closed.

H36's mixed warehouse has two distinct item references and two signed quantities.
That is direct evidence against a one-resource/one-form-per-warehouse model.
Save52 incoming cargo ff01ca38 at record 3073299 contains He-3 00558e x351 and
005579 x152. Arrival/return mechanism is deliberately not inferred from contents.

## Gaps and negative controls

Ten H36 candidates stop at nonempty stack extra lists (for example large gas
ff014675). Seven stop before inventory at unsupported reference extras. They
remain positive base associations with **unknown contents**, never empty.
Omitted inventory flags likewise do not prove empty because defaults and other
representations are not decoded here. Explicit zero-count records above are the
appropriate empty serialized-list comparison.

No Transfer Container or decorative chest base is identified in this selected
inline-base subset. This does not establish that those objects are absent from
the save, the playthrough or the wider corpus. Their native serialization route
is identified, but an actual object-level save join remains unresolved. The same
husbandry instance gap as E2 remains. No disabled-plus-stock witness was found in
the inspected subset; no disable transition is claimed. Native save restoration
is documented; current loaded restoration has not been measured.

Capacity-relevant ExtraBF fields are retained by section and mask. H36's small
solid example has explicit AV 22a2b6 = 1 but no CarryWeight override in its decoded
BF sections. Thus its capacity value 75 is definition-derived, whereas its item
count and owner are explicit saved facts. Do not multiply unrelated saved floats
into capacity or treat every queued reference as an item.
