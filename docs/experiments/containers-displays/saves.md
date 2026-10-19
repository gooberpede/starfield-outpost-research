# Saved fixture, item and display joins

[Answer](report.md), [native contracts](native.md), [methods](methods.md).
Offsets below are decimal **decoded logical save-stream offsets**, not original
compressed offsets or native VAs. Dynamic identities are save-local resolved
FormIDs; component id_word is a storage ID whose low 24 bits resolve through
that save's form table/plugin namespace. It is not a runtime handle.

## Positive native-display witness

HIST-0021 original SHA-256 is recorded in [sources.csv](sources.csv) and the local
saved-HIST-0021.json/components-HIST-0021.json receipts. The actual protected
original is hashed before/after strict decoding. The type 6 envelope, CTName and
all 43 ordered component sections close exactly after the pending-dialogue
extension described in native.md. This proves framing, separately from semantics.

| Relation | Saved observation / exact support |
|---|---|
| Helmet fixture | DYNAMIC:ff05bb90, base Starfield.esm:363cc8, Outpost_Display_HelmetStand01, REFR record 5861284 |
| Slot relation | Component table1412fe810-Nested row 1579789, index 0, flag 1, one group containing item ff05bb92 |
| Specific item | REFR5861468, ff05bb92 -> ARMO026bf0, Spacesuit_Miner_Helmet_Deimos; same saved parent ff020801 |
| Instance data | Seven counted reference extras close 5861601..5861629; Extra33 holds ten exact modification form identities/flags; component envelope contains 28 separately preserved bytes |
| Item ownership | Extra1F stores NPC Player form 000007 in its first lane and no reference owner in the second; retained as item ownership, not a boolean stolen classifier |
| Backlink | Extra36 identifies fixture ff05bb90; Extra4C contains an additional fixture link. These agree with the independently parsed slot table |
| Fixture membership | Extra4C at 5861368 contains WorkshopItem054ba6 -> ff029ca0; another keyed edge 1c5edd -> ff0436d1 is separately retained |
| Fixture ownership | Extra1F at 5861372 has null form lane and reference lane player000014, byte 0. This differs from both Workshop target and item's NPC owner lane |
| Saved presentation inputs | Fixture XYZ 2.5121391, 9.8284836,.0883081; helmet XYZ 2.5121391, 9.8284836,.5883081. Numeric difference alone is not mounting proof; the independent component/backlink joins supply the relation |
| Inventory counterexample | The fixture's serialized inventory count is zero, while its component points positively to the helmet reference. Empty inventory therefore does not mean empty display |

The second independent relation in the same original is backpack wall stand
ff05bb91, base 363cc6, record 5861376. Its component row 1579804 group 0 points to
ff05bb93, record 5861629, ARMO026bef Spacesuit_Miner_Backpack_Deimos. The item
also has ten Extra33 modification entries, Player NPC ownership and fixture
Extra36 backlink; all seven reference extras close. The fixtures share Workshop
ff029ca0 while the second non-Workshop keyed target differs. No proximity-only
association or historical action ordering is used.

The supported persistence chain is **specific fixture -> saved rule group ->
specific item reference -> installed equipment base plus instance extras ->
native saved-ID resolution/handle reconstruction and attachment work**. Actual
rendered representation after loading these originals is NOT TESTED. This is
stronger than an inventory-only join, without claiming a screenshot or reload.

## World case/rack comparisons and quantity

HIST-0036 original SHA-256
`7e6642f49774c9827fe5230f8cdccdff6b00e4af8738dac11018b56e7ffeca37`;
HIST-0255 has its own original pin in sources.csv. Each full component unit closes.
Four populated static fixtures occur in both, with save-specific generated items.
These are separate observational snapshots, not a controlled transition pair.

In H36, static reference 14bd2a at 2719300 has component row 1476795 with two
occupied groups -> ff19c369 and ff19c36a. Physical installed REFR14bd2a's NAME
is CONT246226, the same pistol-case base reached by ordinary construction.
Static reference 14bd2b at 2719686 maps to heavy CONT188d28; row 1476816 has four
groups, two occupied. Static 3a9073 and 3a90a8 each have four groups with actual
item identities retained in components-HIST-0036.json. Exact installed defaults
are comparison evidence, not proof of historical winning definitions/ownership.

H36 ff19c364 (weapon base 02d7f4) has fifteen Extra33 modifications and a closed
extra list after the 2C/22 extension. The ammo references have explicit Extra22
counts, whereas the helmet/backpack instances use the native default count 1
when no Extra22 is serialized. This separates a visible reference from its
quantity. Some weapon variants stop at ExtraEB and remain partially decoded;
their full bodies, reference queues and modification identities are preserved
locally, with no invented legendary/charge/condition interpretation.

H255 comparisons include weapons with ten, sixteen and twenty-six decoded
modification entries. A count of modifications is not a count of legendary
effects; the exact OMOD semantics require their own per-entry joins. This
assignment does not import enchantment/condition fields from another game.

## Corpus search, controls and limits

The locator inventory is the frozen historical scan-01 inventory, not Save52
alone. The current pass attempts every original still accessible at its recorded
canonical path; source hashes must match before analysis. `corpus-selection.json`
records eligible/missing labels; individual saved-HIST files retain typed footer
count closure, prefix gaps, source pins and inventory statuses. Failures are
retained in corpus-failures01.json, including older header-build contexts rejected
by plugin_tables. They are capability failures, not no-item findings.

Initial purpose-selected samples were HIST-0036/0077/0083/0255/0267; HIST-0021
then supplied the positive helmet/backpack mechanism. The subsequent broader
survey is summarized in corpus.csv. Detected roots are inline-base positives,
not complete/default Workshop populations. An inherited/generated NPC whose
initial base cannot join the known 26 mannequin definitions is outside that
detector. Static world references can need installed/default base lookup rather
than inline base, as the component comparisons demonstrate.

Explicit empty control: H36 ff025aa2/Outpost_Display_WeaponRack02 at 3520880
has compact inventory item count 0 and queue closure. Its ordinary WorkshopItem
target is ff025a78. H255 ff03f008/WeaponRack01 and ff03f5ab/multi-slate display
also have explicit count 0 and WorkshopItem -> ff078293. The broad scan also
finds no-inventory-change records; those are **not verified empty inventories**.
The repeated dynamic pistol-case candidate with NO_EXTRA_DISPATCH is not an
inventory decode or a proved ordinary constructed fixture.

The completed survey covers **278 locator entries: 255 accessible originals,
147 accepted by the qualified header/prefix reader, 108 rejected for unsupported
header/build, and 23 missing at their recorded paths**. All 255 attempted
originals receive final preservation checks independently of successful decoding.
The census CSV records successful candidates and errors per label; repeated
historical snapshots are not independent gameplay trials.

The completed pass overturns the initial interim no-mannequin/no-chest result:
HIST-0256 and HIST-0257 contain both mechanisms. `stock-joins01.json` initially
stopped on extras86/1A. Native n026 qualifies these as one/two queued identities;
`stock-joins02.json` then closes all three mannequin inventory rows. Equipment
rows each have one instance and row state 1 (low equipment bit set), preserving
Extra33 modifications and Extra96 instance data. H256 mannequin ff04f2d6 and
H257 ff05c66c use installed Outpost_Mannequin_Female01; their actor tails and
remaining queues are expressly outside this row subset, not a full actor parse.
Exact item/offset/modification evidence is in the following table and local
receipts. Native row writers/readers independently preserve these state bits.

| Sample / actor | Item identity | Inventory evidence |
|---|---|---|
| H256 ff04f2d6 | Starfield.esm:227ca3, Varuun suit | Row 16021620..16021643; one instance, state 1, extras86/33/96, ten modifications |
| H256 ff04f2d6 | Starfield.esm:16d3d0, Varuun backpack | Row 16021643..16021666; one instance, state 1, extras33/96, eleven modifications |
| H256 ff04f2d6 | Starfield.esm:16d3d1, Varuun helmet | Row 16021666..16021689; one instance, state 1, extras86/33/96, ten modifications |
| H257 ff05c66c | Same three installed item identities | Independently parsed rows at 18879240 onward, same state 1; no action sequence inferred |

Ordinary ammo-box positives H256 ff0324b7 and H257 ff039508 each contain
Starfield.esm:2bae3f quantity 18 and 00e8ec quantity 57. Their inventory row and
reference queues close (decoded ranges 7405634..7405657 and 8586843..8586866).
The parser's inherited status name DECODED_EMPTY_STACK_EXTRA_SUBSET means
**empty stack-extra lists**, not empty inventory; item_count is 2. Wall safes
have 22 item rows declared but stop at extra9B after two decoded rows; cooler
NO_INVENTORY_CHANGE_BRANCH is not verified empty. These controls preserve
counterexamples to interpreting a status name or missing change data as emptiness.

Native/script support remains positive independently. Generic case/rack native
restoration is shared with the real positive stand chain; actual rendered reload,
mannequin actor-tail closure and measured scrap-content conservation remain
unobserved. Native ordinary scrap transfer is now positively traced separately.

## Smallest proposed controlled acquisition

**Proposal only; no execution authority.** Use an immutable copy of an approved
current-build source and a new separately approved run card. Protect and hash
originals; keep C:/D: guards, finite action scope, evidence flush, STOP and cleanup.
No new observer or debugger is required merely to obtain ordinary saves/screenshots.

1. At one identified outpost construct one chest, one rack/case and one mannequin;
   save an empty control with matched fixture identities.
2. Deposit one distinctly modified owned weapon and one legitimately retained
   stolen item with recorded metadata, plus one compatible outfit. Equip the
   outfit using the mannequin's explicit equip action; record which item mounts.
3. Save, reload that controlled copy and record rendered/equipped state before
   further action. Compare fixture inventory, slot lists, item refs and actor
   equipment/ownership channels rather than counts alone.
4. Retrieve one item, then move and scrap separate populated controls, each with
   a save and no-action companion; record player inventory/item deltas. Keep
   physical destruction/repair as a separate optional case only if the chosen
   definition actually supports it.

This would resolve named ordinary-action/visual conservation gaps; it is not
needed to re-prove the static display serialization grammar. No active playthrough
save may be overwritten or edited.
