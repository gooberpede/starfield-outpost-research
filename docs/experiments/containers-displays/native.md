# Native contracts and compiled-script correspondence

[Answer](report.md), [saved witnesses](saves.md), [methods](methods.md).
Every native address is a hexadecimal **preferred static VA**, image base
`0x140000000`; subtract that base for RVA. Retail executable version is
1.16.244.0 under the exact hash below. Object offsets are hexadecimal.
None is a runtime pointer, file offset or safe callable ABI.

Fresh EXE SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
main ESM `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
`nNNN` denotes a numbered **SD1-local export request/output**, not a function
name or global identifier. The [export-ID guide and SD1 lookup](../../reference/native-export-ids.md#sd1-lookup-example)
links each function address to its tracked register and exact local output/pin.
Raw `.local-work/sd1-containers/native/NNN.request.tsv` outputs are LOCAL-ONLY;
one output may contain several FUNCTION sections. Identical numbers in another
experiment have a different namespace.

Reading convention: an explicit vtable byte offset selects a pointer in the
referenced interface's vtable; an object/member offset selects data in the named
object. Neither is an executable address or a vtable slot index. Existing shorter
hexadecimal expressions below retain their locally stated owner; see the
[prose notation convention](../../reference/notation.md#native-prose-at-first-use).
Read-only Ghidra exports identify the imported hash/base in every file.
RTTI names are existing analysis state; semantic names below are analyst labels,
OBSERVED-INTERNAL. Instructions govern when decompiler pointer/float types err.

## Recognition, definitions and ordinary admission

`140431a00` (n003) registers BGSDisplayCase. `1400183b0` (n008) installs
form-component factories and binds its component ID `1461dd764`.
`141303ce0` (n008) queries it using generic component lookup `1405ddbd0`.
`1412fe780` (n013) tests the reference, then its base at reference+98.
It does not infer display behavior merely from CONT or a keyword/name.
`1413026e0` (n003) registers loaded DisplayCaseComponent and its unloaded
counterpart, IDs `1461eea88/1461eea8c`, with attach/detach creation policy.

Form-component vtable `144b0cd00`, loader at vtable byte offset `0x40` -> `140431b50` (n011/012):
DCSD is a sequence of 16-byte little-endian rows, **include form, exclude form,
snap-node index, maximum item count**. The loader expands each to a runtime
30-byte-hex rule. Versions below 140 hex decrement the saved node index;
cross-version index equality must not be presumed. DCED holds counted u32
exclusion-group indices per rule. Empty, absent and populated filters differ.
The authored CSV preserves every inspected DCSD tuple; raw DCED remains local.

`1404321f0` (n006) selects the first usable rule whose occupied-reference count
plus one is <= its maximum. Nonempty include/exclude FLSTs test exact forms and
the item visitor `140640c90`; it also rejects when a mutually excluded group is
occupied. It writes the selected **rule array index** through the output pointer.
The rule's node index is a separate field. Zero configured rules uses
`uDefaultMaxDisplaySlotItemLimit`, initialized to **30** by `140018340` (n003).
That fallback is not the normal 1-item limit in populated DCSD rules.

Ordinary menu TransferItem follows the accepted S1 sink -> `141eaf9e0` ->
`141eb7950` -> `141eafe00`. Fresh `141eaf090` (SD1 n010) requires the item-interface predicate at **vtable
byte offset `0x130`** and the bound callable held at **menu object + `0x4C8`**.
The latter is a member holding the callable object, not its code address.
Fresh `141eadb50` (SD1 n039) assigns the bound
`141eadf60` predicate through `14146bc10` (n041), closing the earlier S1
assignment boundary for this setup path. A null callable throws.
`141eafe00` also enforces take/give mode and actor capacity before `141eb01a0`.

Fresh `141eb01a0` (n010) positively closes **display-specific** preflight:
on the store direction, `1412fe780` recognizes the target; unless carousel
predicate `141300fc0` applies, `1412fea50` simulates slot reservations on a copy
of the component lists, repeatedly invokes `1404321f0`, and bounds the requested
quantity. Zero compatible slots selects the explicit cannot-store feedback.
BOOK type 31 can reuse an existing matching displayed reference and aggregate its
quantity; this is not unrestricted one-reference-per-physical-unit behavior.
This slot gate is independent of the general captured callable.

`141eadf60` (n041) -> `141eae1f0` (n042) applies item/quest eligibility,
mode-specific pickpocket/quest restrictions, target-specific gates and the actual
menu filter held at **menu object + `0xD68`**, with the inversion byte at
**menu object + `0xD70`**. FLST filters iterate alternatives;
`141ee7440` handles a single form/category. Thus the mannequin script's supplied
filter has a native consumer; compatible appearance alone does not admit an item.
The completed ancestry supersedes the interim captured-callable uncertainty.

Weight reuses [S1 capacity](../storage/capacity-native.md): `140b70a80` applies
positive-capacity positive-weight fit; nonpositive C bypasses that clamp.
The menu substitutes the fit amount; generic add can retain the original request.
Chest default 10/40/150 is a weight contribution, not a slot count. Actors call
`14190bee0` (n025): effective CarryWeight plus entry-point 10 adjustment through
`140c94060`. Mannequin -85 PRPS alone is not the final capacity; its complete
actor default calculation and current overrides are not established here.

## Inventory instance to displayed reference

Actual generic row insertion `140643360` (n028) repeatedly calls `1412ff580`
and removes each represented quantity using `1406425a0`. This is a mutation
path, not just a theoretical matching helper.

`1412ff580` (n007) -> `1412ffae0` (n005) obtains the reference/base display
component and current slot lists. The latter selects a compatible rule and
matches its node index against actual snap-template node records, requiring the
node flag bit 2 and choosing the qualifying priority. `1412ff2d0` (n028) composes
fixture rotation/position/scale with node-local transform for the new item.
Failed template/node/slot lookup does not establish successful mounting.

The creation payload uses the actual inventory item form. It may reuse a
selected existing reference; otherwise `1405a0520` creates one. `140504b40`
(n029) copies a **whitelist** from the selected nonnull instance ExtraDataList:
it includes 1F ownership, 22 count, 33 modifications, 96 instance/name data and
other supported instance channels. It is not a bitwise clone of all reference
state. The first selected nonnull stack extras supply that creation context;
different modified instances must not be collapsed into base-form identity.
The separate source-removal operation bounds actual quantity and splits stacks.

In the new-reference branch (payload+48 is null), an explicitly owned fixture
overwrites the copied item's ownership through `14050ced0`. Instructions
`1413001a6` copy selected extras; `1413001b5..1bd` test fixture ownership;
`1413001cb` skips allocation if extras already exist, jumping to `141300236`,
which still reads fixture ownership and calls the setter at `141300252`
(n005, independently checked in n034). Thus the null-list condition guards
allocation, not ownership assignment. The reused-reference branch is distinct.
Modification retention does not imply ownership retention or a measured
stolen-to-clean UI transition; other permitted extras can survive while ownership
changes. No claim covers every possible modded/quest extra.

New display reference registration sets fixture ExtraDroppedItemList via
`140515ee0` and item ExtraItemDropper via `140515090`, then appends its handle to
the chosen rule's component list with `141304dd0`. `140f34be0` handles Workshop
attachment relationships. Native reference count `14050b150` (n030) reads
Extra22 or defaults to one. BOOK reuse adds existing and incoming quantities.
Count/instance extras, item-reference identity and rule position are different facts.

## Ownership and player action

Workshop placement uses `140f3cf40/1421dd600` (n016/023), setting the
WorkshopItem relationship. Extra4C is not ExtraOwnership.
Fixture/item setter `14050ced0` (n010) creates ExtraOwnership type 1F, stores
either a form pointer at extra+18 or actor reference identity at +20, and its
byte at +24. `14050aad0`, `140ba4eb0` and `14050aa30` (n010/014) read the
different reference/actor/faction lanes; zero/null does not encode one universal
player/faction rule.

`140ba5700` (n010) is the actual ownership/access predicate used by actor
OpenInventory `141fc8c70` (n004). It tests explicit Extra1F, actor/base equality,
cell ownership fallback and faction rank/permission branches; Workshop owner
handle equality is not substituted for those decisions. Force-open changes menu
access, not every item's lawful owner.

`141eb01a0` distinguishes store direction 0 and take direction 1. Its taking
branch chooses owner/crime mode, calls `141a45dc0`, and in the applicable
mode uses `140640eb0` to write ownership across selected stack extras;
special currency and quest cases are separate. `140640030` reads actual stack
ownership. The transfer callback `140b67380` (n030) copies extras and has
reason-dependent ownership changes: reasons 1/19-hex can set source ownership;
reason 2 removes Extra1F; reason 5 has its own no-owner fallback. The caller's
reason and direction must therefore accompany any conservation/ownership claim.
No general stolen-item laundering claim is justified by putting an item in a
Workshop fixture, and saved ownership bytes alone do not prove UI theft color.
Fresh request ancestry closes that gap: reference-interface vtable byte offset `0x458` at
`144b95fb8+458 = 144b96410` resolves `140b66680` (n037/039), then
`140b67a30` (n041), `140b7c560/140b89690` (n043), row visitors
`140b89fd0/140b8a8c0 -> 140b8f540` (n044/050), and `140b67100` (n051).
The latter calls `140b7c100/140b7bd20` (n048), which actually invoke
`140b67380` with each selected instance and split quantity. Their callback
context retains the original request; reason is request+20, destination+28.

| Mode at menu object + `0xD80` | Store/take transfer reason | Scoped ownership effect |
|---|---|---|
| 2 | 5 | Callback's guarded no-owner fallback can assign Player NPC; existing ownership is not simply erased |
| 1 | 1 | Source-owner handling applies; taking also has explicit selected-stack owner/crime processing before transfer |
| Other (including ordinary mode 0) | 4 | Callback copies instance extras without its reason 1/2/5 ownership-set/remove branches; currency and display conversion remain separate transformations |

`141eadb50` takes mode from event byte+20 (n039). Actor OpenInventory
`141fc8c70` constructs that event (n004): ordinary allowed/forced access reaches
mode 0, denied access can select 1, and its separate activation route selects 2.
Do not conflate this byte with take/store direction. Ordinary mode 0 deposit and
retrieval therefore preserve copied item ownership **in this transfer callback**;
new display-reference creation can subsequently overwrite it as established
above. Display retrieval's actual `140b67100` branch resolves the mounted item
and dispatches actor pickup or `140b4c620`, preserving its count and instance
context; `141a44770` (n016/053) removes the dropper/slot relation. No ordinary
player theft/UI or deliberately stolen-item transition was measured.

## Mannequin script, equipment and restoration

Installed MannequinScript PEX SHA-256
`8cb3b6e22d053222ae8d2efdc9f128adc84dca4c85ea36739ed064a549588a74`
is fully parsed in scripts01.json; independent development PSC hash
`c0aa7f323e7c4630f50def1ff43c6eeaa7f1d96010332f11322da52bed753d37`.
OnLoad disables head tracking, restrains and makes unconscious, and blocks default
activation. OnActivate requires the player and allowPlayerActivation before
calling OpenInventory(true, DisplayFilter_Mannequins, true). The third argument
means include-only-from-filter, **not automatic equip** (installed Actor.psc
declaration). Filter FLST280901 includes equipment-type keywords. Script part 9
inheritance reaches the female/male mannequin template; the R1 inherited-script
binding contract applies separately from cosmetic/perk parts.

ContainerMenu_ToggleEquip source `141eb6060` -> sink vtable `144d07df0`, handler
`141eb1640` -> immediate/queued `141eb1730` (n019/020/023). It resolves the
selected inventory identity and actual actor target, then calls `1419a3330`
(n027/028) and refreshes equipment/3D through `1419d0690`. Its manager uses
actual equipment slots and selected instance data, not native display snap lists.
This is the causal difference between storing an outfit and equipping it.
The saved equipment channel is concrete: `140641180` (n039) writes inventory
row+20 (u32) and+24 (byte), and `140641320` restores them. `1419a9040`
(n039) tests low 3 bits of that same row+20 and resolves corresponding slots;
`1419aa500` (n040) unequips and clears the low nibble. Actual equip processing
`1419a47d0 -> 1418f53e0` (n036/042) looks up the exact form/instance row and
checks the corresponding bit via `14196cdc0 -> 1418f56d0` (n050/054).
The live manager collection at actor+228, manager state+270/+278 is separate
from serialized inventory rows and holds form/instance/slot state.

Initialization `140b6ee30` (n053, reference-interface vtable byte offset `0x900` in the inspected table)
calls `140b7d5b0` (n055). It iterates loaded rows, tests low 3 equipment bits,
dispatches armor to `140b79750`, weapons to `140b79970`, and reconstructs actor
equipment through vtable byte offset `0x740` of the actor interface and `1419b4d10` after resolving instance/slot.
This supplies a restoration consumer for the saved bits; it is not the earlier
`1406416f0` extra-normalization helper, which runs before reading those bits.
H256/H257 now positively corroborate three modified equipped rows each
([saved witnesses](saves.md)). Full actor-tail decoding and rendered reload
remain unproven; native equipment restoration does not prove scene success.

TestDisplayCaseScript PEX is parsed independently; it merely logs item events.
NativeTerminal:DisplayCaseScript manages linked locks/terminal conditions, and
CWAHDisplayTrackScript creates/deletes a music effect. None supplies the ordinary
native item mounting algorithm just because its name contains Display.

## Save/load and lifecycle

### New construction suppresses default stock

The empty-construction result is an explicit native operation, not an inference
from a base name ending EMPTY. The constructible pistol case CONT246226 has
COCT=1 and CNTO item 21972a, quantity 1; heavy case CONT188d28 has COCT=1 and
CNTO item 219727, quantity 1
(census01.json physical records, same installed hash). Those defaults can populate
world instances, but do not describe the ordinary construction preview's final
inventory.

`1421dcb10` (full n073) updates the construction preview through `1421d9230`,
obtains the selected preview wrapper's representative handle through its vtable byte offset `0x40`,
resolves that actual reference, then applies the decisive branches:

- A nonactor with positive `140b693b0` inventory count is passed to
  `140b61610(source, null, reason0, capacityClamp0)` at **1421dd301**.
  It removes ExtraDroppedItemList37 and requests display-component reset
  `141305190` after clearing stock.
- An actor recognized by `140f38600` (the mapped `bIsMannequin` predicate) uses
  the same null-destination clear at **1421dd2d7**, then sets actor+37c bit 1000.
  General actor equipment/default-outfit behavior is a competing branch and is
  not silently generalized to mannequin construction.

The analogous clearing blocks appear in the assembly preview `1421cbf40` and
the helper `1421cbc20` (n073). The ordinary accepted placement remains
`1421b10b0` -> `1421de3f0` -> wrapper vtable byte offset `0xA0` ->
`140f60f60` -> `1421dd600`
([L1](../limits/native.md), fresh n070). It commits the representative reference;
this is distinct from moving an existing fixture through `1421b1450`.

Null destination has concrete different semantics from scrap's player recipient:
`140b61610` (n053) rejects unavailable sources, then its reason 0/null branch
calls **140644210** (n074). That destroys existing stack extras, clears the row
array through `1406450e0` (n075) and invalidates cached inventory weight. It
retains the source inventory object rather than transferring items to the player
or adding loot. `140b24af0` (n075) initializes only when source+a0 is null;
an allocated empty inventory is therefore distinct from uninitialized base stock.
The generic inventory writer/reader retains that state separately from a world
case's installed CNTO defaults. No ordinary construction loot reward follows
from reusing a loot-case base.

This is a strong static answer for the inspected ordinary preview/commit path:
stock is explicitly suppressed, and engine-recognized mannequins are explicitly
emptied. Resolver failures, exceptional creation interfaces, active overrides and
later scripted insertions retain their separate conditions. No live empty-build
or repeated-reload measurement was performed. Earlier drafts omitted this
competing default-stock branch; independent review required the correction.

The inventory writer/reader is reused from S1: `1406447c0/1406448b0` with item
rows `140641180/140641320`, stack extras and signed counts. Display component
serialization is an independent type 6 channel. `141822570` calls
`141303d30` for unloaded components and `141303fa0` for loaded components
(n009/014). The latter writes owner identity/index and `1412fd300`: byte flag,
u16 number of rule groups, then u16 count and serialized item-reference
identities for each group. These are saved FormRefs, not saved handles.

Loader `1412fe810` -> `1412fd450` (n018/019), and component callbacks
`141302bb0/141302bc0` (n015), corroborate the grammar. `1418234e0` (n015)
resolves each component owner and calls `1412fd650`, which resolves saved item
identities to new handles and queues fixture/item post-load work
`1413049e0 -> 1412fd980`. The latter restores dropper/Workshop attachment
relationships under actual reference/template preconditions. `141855570 ->
1412fdfb0` reconciles qualified inventories after load. Attach/detach has separate
loaded/unloaded representations and deferred work; successful deserialization
alone is not proof of completed scene construction.

Removal of a displayed reference from slot lists is `141304f40` (n005),
independent of generic inventory mutation. Workshop scrap
`140f34650 -> 140f404f0 -> 140f3a6e0` (n016/029) removes roots/children and
queues `140f42ec0` (n031), which calls the reference-interface method at vtable byte offset `0x538` before deletion.
That vtable byte offset `0x538` resolves to `140b3e1e0`, a 3D replacement/detachment operation
(n032/033), not an inventory-content transfer. It is incorrect to infer item
return from that operation or the final Delete alone.
The decisive ordinary Workshop caller is **`1421de660`** (n052; full n057).
For each resolved removed reference, it invokes the removal chain and then
checks positive inventory count through `140b693b0` **or** native display
recognition. Nonactors enter its content transfer block; actors require the
additional `140f38600` predicate. The block selects an eligible recipient through
the player context, calls `140b61610(source, recipient, reason0, capacityClamp1)`
unless that recipient is the excluded player-reference alias, then calls
`140b61610(source, player, reason0, capacityClamp0)`. A nonempty localized
Contents transferred to the player string is shown only on its ordinary
non-silent path. This is positive scoped transfer evidence, not a conclusion
from final reference deletion. Other reference-removal callers need not use it.

Bulk `140b61610` (n053) rejects source==destination and unsupported sources;
the optional positive-capacity branch limits quantity by item weight. It builds
instance/quantity requests with the original reason/destination and invokes
the source-reference interface at vtable byte offset `0x458`. For native displays it first calls `1417324f0` (n055):
walk fixture ExtraDroppedItemList, resolve each item and `141732620` (n057)
copies qualifying item extras/count back into the source inventory before
removing the displayed representation. Missing handles and flags 820 cause
qualified skips. `140b65df0` handles reconciliation/cleanup. This explains how
separately mounted items can enter the same bulk-content route. Ordinary
inventory capacity does not cap the final explicit unclamped player transfer.
No universal guarantee covers invalid handles, quest restrictions, generic Delete,
exceptional actor removal or every external caller; no conservation trial ran.

The actor exception has a positive semantic binding: **the same predicate
`140f38600` produces ContainerMenu's `bIsMannequin` value**. `141440d30`
(n066) resolves the actor and sets event payload+13 from that predicate;
`141441b10 -> 141441f70 -> 1414410f0` (n067–069) carries it into property
array+20/value+23. `141441730` (n016/067) registers `bIsMannequin` at
provider+29/value+2c, after the nine-word provider header; the property order
and value offsets match. The pointer adjustment is independently pinned from
the original EXE in accessor01.json: model+38 uses vtable 144c56760, virtual+58
at 144c567b8 -> **14038a050**, whose complete getter is LEA RAX,[RCX+28]; RET.
Thus model+38+28 = model+60 = provider+48, exactly nine eight-byte words into
the provider beginning at model+18. Native instruction addresses and PE file
offsets are separately recorded; the getter was manually decoded from its
complete five-byte body, not inferred from the surrounding structure name.
This closes the actor class meaning without guessing
from Workshop membership. Internally the predicate still requires actor+4b0
bit 200 and its global keyword lookup at 145f0c620. The specific resolved keyword
and every possible overridden/generated actor are not independently qualified.
Thus ordinary **engine-recognized mannequins** enter the content-transfer block;
other actor references can skip it. A recipe/script name alone supplies no
unconditional promise that an arbitrary runtime actor passes that predicate.

Movement reuses L1/L3's `1421b1450` mapping rebuild; no item duplication or
measured preservation is inferred merely from the owner's unchanged identity.
Selected chest/display definitions lack DEST; DA1's destroyed-bit/Health/repair
contract applies only to qualifying targets. No independent physical destruction
or repair inventory mutation is established for the passive examples.

## Preserved failed routes

The first definition dependency pass treated arbitrary FNAM as an array and
failed a size assertion; recipe-only decoding corrected it. The initial native
string scan reached its 1500-string cap; n002 reran a focused uncancelled scan.
Several guessed interior function addresses returned NO_FUNCTION_AT, retained as
failed locators, never absence evidence. Ordinary exports cap instructions at 600
and decompilation at 50000 characters; full:14051ea30 in n026 repairs the
truncated extra writer for later cases. No claim uses an unexported capped span.
The first component attempt omitted CTName and failed bounds; its corrected
reader then hit a nonempty pending-dialogue section. Native `140d4ae40` (n018)
qualified that section's id/u16-index/u32 layout, allowing exact full-unit closure.
Earlier failure and unsupported item extras remain in the local receipts.

Independent preliminary review rejected the author's ownership-fallback reading.
The failed interpretation confused the allocation guard with the subsequent
setter guard. The instruction-level correction above supersedes it; the earlier
review and exact counterexample are retained in review.md.
The final actor investigation also tried a literal EXE pointer locator for
145f0c620 (binding01.json, no absolute-pointer occurrence) and an uncancelled
bounded offset-4b0 instruction census (n060); neither establishes the keyword's value.
The named UI consumer supplied the stronger semantic connection above. n049's
broad WorkshopMenu symbol query hit 256; it is reconnaissance, not exhaustive
evidence. Selected full exports and later instruction windows repair consequential
truncation; remaining caps and failed interior locators are not absence evidence.
