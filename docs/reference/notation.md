# Reading technical notation

2026-10-21. Reader convention under the [evidence standard](../EVIDENCE_STANDARD.md).
Historical declarations remain authoritative for their original domains. These
conventions clarify documentation; they do not revalidate another build.

| Domain | Reading rule and example |
|---|---|
| Build and image | Give executable version, exact source hash and preferred image base together. The principal native reports pin retail 1.16.244.0 and preferred base `0x140000000`; originating historical configurations can remain UNKNOWN. |
| Static VA / RVA | A preferred static VA is an address in that preferred image; RVA = VA minus preferred base. A runtime VA additionally needs the actual loaded module base and capture epoch. Preserve leading zeros in source locators. A bare function label is read under its report's declared domain, never inferred solely from digit length. |
| Native member / virtual method | `reference+0xd3` denotes a byte offset in a native reference. A vtable byte offset is not a slot index. Specify owner, units and representation; do not transfer layouts across builds. |
| Files and records | Physical ESM file offset, compressed save-file offset, decoded logical-stream offset, record-relative offset, decompressed SWF offset and ABC method-byte offset are distinct. Preserve a report's decimal or all-hex declaration. Ranges retain their stated end-exclusive convention. |
| Masks and bits | Write mask `0x10`; its zero-based bit index is 4. Decimal bit index 10 would correspond to mask `0x400`. A historical `bit2` qualified as mask `0x02` means zero-based index 1; never silently reinterpret it as mask `0x04`. Multi-bit masks are not a single bit index. |
| Types and fields | A native status byte, notification type, condition wire index and extra-data tag are separate domains even when their digits match. `ExtraBC`, `Extra4C`, `binary32` and `u32` are valid compact labels. Field names retain their spelling. |
| Identity | FormID identifies a form within its plugin/load-order context; EditorID is its textual editor label; `COBJ` is a record signature. Saved reference tokens and plugin-qualified saved identities need their decoder mapping. A pointer, reference handle or UI key is not a persistent identity. `Save52` is a sample alias, not a FormID or filename grammar. |
| Decimal quantities | State signedness/width when established. A signed internal count copied to unsigned UI storage is not evidence of a clamp. Counts, ranks and prose labels have word boundaries; exact filenames, EditorIDs and hexadecimal values remain intact. |
| Units and frames | State engine elapsed seconds versus calendar/game days, UT versus local display, local XYZ versus terrain-cell indices, and degrees versus radians. Nominal rates, requested cycles, accepted inventory and displayed totals have different consumers and epochs. No unqualified metre conversion or common vertical frame follows from compatible numbers. |
| Hash and version scope | SHA-256 identifies bytes, not semantics. An edited explanation receives a new documentation hash; a historical source/evidence manifest keeps its original hash. Date/review labels describe the snapshot actually reviewed. |

The Build Limit clarification is checked against retained native instructions:
`.local-work/l2-budget/native/025.request.tsv`, static VAs `1421f2b69`
(`0x1f`) and `1421f2b8c` (`0x10`), with the producer/receiver path documented
in [L2 UI](../experiments/build-budget/ui.md). These are local source
locators, not promised downloads. [Corrections](../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b2/corrections.md`) records exact
edits and hash consequences. No historical mask value has been guessed.

## Native prose at first use

Declare executable version, SHA-256 and preferred image base locally or through
a clearly linked document-wide legend. Function labels such as `141eaf090` in
SD1 are preferred hexadecimal VAs on retail 1.16.244.0, preferred base
`0x140000000`, under SD1's exact executable hash. Keep the function identity;
do not silently substitute an RVA or infer a current runtime pointer.

| Current prose expression | Meaning and owner |
|---|---|
| Item-interface method at **vtable byte offset `0x130`** | Offset into the interface's table of pointers, neither executable address nor slot index 130. SD1 reads the item's interface vtable before this indirect call; the concrete item class is not inferred. |
| **Menu object + `0x4C8`** holds a bound callable | Object member containing a pointer to the callable object, not its destination function's VA. The callable is invoked through its own vtable. |
| Filter at **menu object + `0xD68`**, inversion byte at **menu object + `0xD70`** | Two fields in the same menu object, not vtable entries or decoded-save offsets. The SD1 consumer retains this object in R15 before these reads. |
| Record-relative offset or temporary buffer + `0x88` | Needs its own named record/buffer origin. An object member, stack temporary, decoded record and compressed file have different origins even at the same displacement. |

Use explicit `0x` prefixes for new or revised explanatory offset expressions.
State owner/domain on introduction; shorter notation may follow while unambiguous.
In an established native-dispatch contract, retained `virtual+...` denotes a
vtable byte displacement for that receiver/interface; it does not denote an
object data field. Retained `menu+...` denotes a field in the already identified
menu object. A bare `+...` needs an unambiguous local owner and domain; the
notation alone cannot supply an unnamed structure or interface type.
If surviving source does not establish the owner, say **owner unresolved** rather
than inventing a structure. No vtable slot is computed here: index conversion
requires confirmed pointer width, table origin and indexing convention. A 64-bit
executable name alone does not prove those facts.

Source quotes, CSV field encodings, original exports, saved bytes and historical
pins retain literal spelling. The [export-ID guide](native-export-ids.md) separates
local receipt numbers from functions and scientific pins. The [focused rework](../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b2/focused-rework.md`)
records concrete checks, before/after examples and bounded-search limitations.
