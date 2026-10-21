# Focused B2 rework: native domains and export locators

2026-10-21. [Maintainer's focused brief](../../implementation-briefs/CODEX_BRIEF_SOR_B2_focused_rework_native_notation_and_export_ids.md)
reopens the existing B2 assignment for presentation and navigation. The original
[AC1–AC8](../../implementation-briefs/CODEX_BRIEF_SOR_B2_documentation_quality_technical_presentation_evidence_context.md#9-frozen-assignment-completion-contract--eight-mandatory-criteria)
remain frozen. Prior ACCEPT records identify earlier bytes; they do not accept
this revised snapshot. Publication remains **NOT CLEARED**.

The maintained SD1 paragraph now distinguishes function VAs, item-interface
vtable byte offsets, menu-object fields and SD1-local export selections. A
[tracked export guide](native-export-ids.md) supplies lookup steps and separate
experiment namespaces. [Notation](notation.md#native-prose-at-first-use) states
first-use owner/domain rules. Scientific interpretation, evidence and the three
previous analytical tables are unchanged.

## Concrete before/after and primary support

Before, retained here as a literal defect specimen:

> Fresh `141eaf090` (n010) requires item virtual+130 and the menu+4c8 callable.

After, in [SD1 native contracts](../../experiments/containers-displays/native.md):

> `141eaf090` (SD1 n010) requires the item-interface predicate at vtable byte
> offset `0x130` and the bound callable held at menu object + `0x4C8`.

This is an analytical explanation, not a copied decompiled function. SD1 n010
is an export selection, not the function name. The actual function is the
preferred VA under SD1's pinned retail 1.16.244.0 executable, preferred base
`0x140000000`. Existing source pins identify its local TSV, not a public download.

| Offset / domain | Existing source check; no new reverse engineering |
|---|---|
| `0x130`, item-interface vtable byte offset | SD1 `010.request.tsv:2034–2060`; `141eaf0a5` obtains the item interface, `141eaf0ac` reads its vtable, `141eaf0af` calls the entry at that byte displacement. No concrete item class or vtable slot index is inferred. |
| `0x4C8`, menu-object member holding callable | Same FUNCTION: `141eaf09f` retains menu argument RCX in RBX; `141eaf0b5` reads `[RBX+0x4c8]`. Callable object dispatch is separate. SD1 n039 contains the bound `141eadf60` setup and calls `14146bc10`; n041 contains that helper. |
| `0xD68` / `0xD70`, menu filter and inversion byte | SD1 `042.request.tsv`, FUNCTION `141eae1f0`; `141eae207` retains menu RCX in R15, `141eae357` reads its filter pointer, `141eae3a2` tests its inversion byte. `0xD80` mode uses the same owner at `141eae21d`. |
| `0x2E8` / `0x2F0` / `0x2F8`, crafting-menu fields | SD2 n011/n012 callback `141445660`, instructions `141445669–141445677`, prepares three addresses from the same RCX object for provider `1417f6fa0`. The existing SD2 explanation supplies their bench/combined/source-vector roles. |
| Other expanded virtual offsets | Existing SD1 contracts already name their interfaces and associated function/export; formatting makes byte displacement explicit. For example n031 `140f42fdb` dispatches at `0x538`; n049 `140b79a35` dispatches at `0x740`. No table index or new concrete receiver class is derived. |

Local raw evidence is pinned by unchanged SD1/SD2 sources.csv files. The ignored
`protected-local-sources.json` records ten native-output checks and the original register-generator pin; no native payload
is copied into this package. Existing function/source CSVs, actual review returns,
saves, analysis databases, snippets and primary experiment logs remain untouched.

## Bounded search and occurrence accounting

The reproducible scan uses direct Markdown routes from the current roadmap,
plus named native/mechanism entry points in those subsystem directories:
**134 documents / 768 candidate hits**, skipping fenced bodies. The full corpus
and hashes are in `.local-work/b2-focused/scan.json`; the durable
[candidate register](focused-candidates.csv) records every occurrence, including
deliberately unchanged historical reviews, registry labels and scoped shorthand.
This is not another repository-wide prose or scientific audit.

[Focused corrections](focused-corrections.csv) records **38 explicit edits in
19 explanatory documents**. Most add first-use navigation to the established
notation and namespace guide; a small set expands concrete ambiguous expressions.
No global replacement ran. Unchanged shorthand retains its original domain only
where its source contract supplies that domain; the guide does not invent owners
or cross-experiment label equivalence. Uppercase N register IDs, E1 aNN, S1
sNNN/cNN and S2 nNN retain separate lookup conventions. The four SD1 demonstration
exports resolve from surviving pinned metadata. Other candidate labels are not
all independently remapped to functions; explicit prior-work qualifiers govern.
An unresolvable reference must remain an unresolved local export locator, never
an authoritative symbol. Concrete item class, slot indices, exceptional ABI and
runtime validity remain unqualified.

The [token/number inventory](focused-token-inventory.csv) accounts for each edit's
hex values before/after, explicit `0x` prefixes and case changes. Original n labels,
research IDs and function addresses survive; added version/domain/lookup examples
are attributed. [Focused hashes](focused-documentation-hashes.csv) distinguish
the prior candidate's documentation bytes from this revision. The original B2
baseline and 469-operation ledger are preserved, not overwritten or repinned.

## Full B2 and focused verification

The focused verifier reconstructs all original 469 operations into the preserved
prior B2 candidate, then reconstructs all 38 focused edits into the current 19
documents. It checks numeric-value preservation, source/CSV protection, HEAD/index
and original supplied briefs. Current full structural checks still cover the
entire B2 document surface, not just these 19 files. The previous 37 initial
fixtures, five residual controls, alias control and scientific-table comparisons
remain required. Focused fixtures add literal/clear-domain classifications,
hex-equivalence tests and deliberately corrupted identifier/offset negatives.
These are documentation tests, not native execution or scientific revalidation.

The focused brief was already supplied as an untracked repository file. It is
retained under WORKFLOW's brief convention, included unchanged in the complete
patch, and excluded from task-authored scope alongside the original B2 brief.
Both refreshed patches include all prior authored B2 changes plus this rework;
they do not mislabel a correction-only patch as the full B2 task. Ignored native
payloads, baseline copies, private receipts and scratch trees remain excluded.

Preserved failures: an initial combined read exceeded output limits; it was
followed by focused source reads. A draft notation patch missed a wrapped-line
context and failed atomically; the corrected patch applied. A guessed C2 methods
filename did not exist; the existing function register supplies its local path.
No failed lookup was used to infer a new mapping or native absence.
An initial lookup assertion expected every re-export to have a separate register
row and failed on n039. Reading the preserved metadata generator showed first-
encountered-function deduplication; the revised guide and checked lookup table
explicitly retain the earlier registered export and later cited export separately.
The adapted review exporter initially checked supplied-input bytes before its
in-memory map was initialized, then passed a Path to a byte-hash function.
Both attempts stopped before patch output; failed helper versions are retained
as `package-failed01.py` / `package-failed02.py` locally. Corrected export passed
exact forward/reverse scratch reconstruction and actual-tree reverse checks.

Current actual verification: 37 original fixture controls pass; ten focused
classification/identity fixtures, three hex-equivalence tests, one changed-offset
negative and three identifier-corruption comparisons pass. Four malformed-prose
classification negatives are also rejected. Full structural checking covers
1,094 text files with no UTF-8/BOM/table/fence failures; all 105 deliberately
local-only Markdown link targets exist. This is bounded checking, not rendering
or a proof of universal prose cleanliness. The cumulative review inventory is
103 files: 101 task-authored/edited files plus two unchanged supplied briefs.

## Original criteria on the revised full snapshot — ACCEPT

| Frozen criterion | Independent result, focused review03 | Evidence / reviewed scope |
|---|---|---|
| AC1 authority/input safety | PASS | Original and focused baselines; prior 82 submitted hashes matched before edits; unchanged source pins, ten native-output checks plus the register-generator pin, HEAD/index and both supplied briefs. |
| AC2 historical defect-led audit | PASS | Earlier reviews/37 original fixtures retained; bounded focused corpus and occurrence decisions supplement original scan. |
| AC3 prose/UTF-8/Markdown | PASS | Original 469 plus focused 38 literal edits reconstructed; full structural and focused checks required on revised tree. |
| AC4 precise notation | PASS | Explicit owner/domain convention, source-checked SD1/SD2 fields and vtable offsets, token/number inventory and negative fixtures. |
| AC5 scientific-quality pseudocode | PASS | Three analytical tables and eight-candidate review unchanged; independent reviewer must confirm their full-snapshot preservation. |
| AC6 context/dependencies | PASS | Original sample/context registers unchanged; local export namespace/lookup added without raw evidence publication or cross-experiment conflation. |
| AC7 durable documentation/coverage | PASS | Current report/notation/guide/ledger links; original acceptance history retained and focused scope/unknowns explicit. |
| AC8 independent full-snapshot review/package | PASS | Actual independent ACCEPT on package-review03.json; all original AC1–AC8 pass. Full cumulative patches, primary provenance, numeric/identifier controls and exact reconstruction independently checked; receipt-only limits below. |

## Independent focused review and remediation

The new reviewer inspected the entire revised B2 snapshot and returned **REWORK**
against `package-review02.json`, SHA-256
`5771f1bbfb08dbb0fee0e1f453ae318fa14e73eb7e0601d1bbd5cd4205ca5ef0`.
AC1/AC2/AC4–AC7 passed; AC3/AC8 failed for an introduced nested inline-code
delimiter in the placement chain. This was a real Markdown defect despite the
structural checker passing. It is ledgered and repaired using separate spans;
an exact current-text regression preserves all addresses, `0xA0` and ordering.
The explicit exclusions manifest now names both `.local-work/b2` and
`.local-work/b2-focused`. No primary evidence or scientific meaning changed.
The verbatim response is local `.local-work/b2-focused/independent-review01.md`.
That required re-review is complete: all original criteria PASS in the actual ACCEPT recorded below.

Scientific result: unchanged. Text/package integrity: actual receipts control.
Target survival/instrumentation: NOT APPLICABLE. Authority: documentation only.
Rights/publication: NOT CLEARED; B3/B4 holds remain. No staging, commit or push.


## Actual final independent disposition and delivery

**ACCEPT — all original AC1–AC8 PASS.** The independent reviewer assessed the
**entire cumulative B2 snapshot**, including the repaired inline-code delimiter,
against both briefs. Reviewed package: `.local-work/b2-focused/package-review03.json`,
SHA-256 `6585c073c0df1c4ae1fc4edf015fae6087a7ea8202712bd683c62fe56859eebd`.
The verbatim return is `.local-work/b2-focused/independent-review02.md`.
The earlier REWORK remains above and in its original receipt; it is resolved,
not erased. Prior original-B2 reviews remain historical records.

The reviewer independently checked all 103 submitted hashes, source receipts,
1,589 original and 1,604 focused baseline copies, both correction-ledger replays,
original/focused fixtures and negatives, full structural/relative-link checks,
protected inputs, HEAD/index and both patch directions in memory. All eight
criteria passed; the analytical tables and scientific conclusions are preserved.
Historical operation order and implementer on-disk scratch application remain
receipt-only; this is documentation qualification, not engine/save revalidation,
full Markdown rendering, public reproduction or rights clearance.

Final cumulative delivery is `.local-work/b2-focused/package-final01.json`,
with `status-final01.txt`, inclusion/exclusion, source, identifier, preservation
and structural receipts in the same directory. Diffs are
`.local-work/diffs/b2-notation-final01-complete.diff` and
`.local-work/diffs/b2-notation-final01-task-only.diff`: 103 complete / 101 task
files, including both unchanged supplied briefs only in complete scope.
The exact final package SHA-256 and fresh full-snapshot reviewer decision are
retained in `.local-work/b2-focused/independent-review-final01.md`; this separate
receipt avoids making the reviewed document hash depend on its own manifest.
Changed final bytes require affected re-review; the original frozen criteria
remain intact. Nothing is staged, committed or pushed; publication is NOT CLEARED.
