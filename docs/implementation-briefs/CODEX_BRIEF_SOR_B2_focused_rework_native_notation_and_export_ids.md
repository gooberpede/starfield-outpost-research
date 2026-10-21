# Codex focused rework brief — B2 native notation and local export IDs

**Project:** `D:\Projects\starfield-outpost-research`  
**Assignment:** Focused REWORK of the existing B2 documentation-quality assignment, **not** a new research phase  
**Input:** The maintained, not-yet-committed B2 final submission (`b2-documentation-final01-complete.diff` and task-only companion), B2 original brief and frozen AC1–AC8, prior independent ACCEPT and its evidence, and this maintainer-requested focused correction.  
**Authority:** Offline, limited documentation edits and validation only. **No staging, commit, push, publication, deletion or scientific reclassification.**

## 1. Reason for rework

The maintainer's critical review of B2 uncovered a documentation-readability defect not adequately resolved by the B2 notation guide. An otherwise valid native explanation in `docs/experiments/containers-displays/native.md` reads in part:

> Fresh `141eaf090` (n010) requires item virtual+130 and the menu+4c8 callable. Fresh `141eadb50` (n039) assigns the bound `141eadf60` predicate through `14146bc10` (n041) ...

An experienced reverse engineer new to this repository cannot reliably determine, without consulting unstated conventions, which values are **virtual-table byte offsets**, which are **object-member byte offsets**, which numbers are **preferred virtual addresses**, and what `(n010)`, `(n039)` and `(n041)` identify. The underlying scientific result is not being challenged. This is a **contextual presentation and evidence-navigation defect**.

The goals are to (a) improve first-use clarity and contextual consistency throughout *current authoritative explanatory prose* and (b) give local native-export identifiers a discoverable, accurately scoped definition and correspondence. Retain all accepted B2 scientific/pseudocode conclusions and the original AC1–AC8 contract. Do **not** use this rework as an opportunity to reopen a repository-wide prose or scientific investigation.

## 2. Verify provenance before editing

1. Read `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, the original B2 brief, `docs/audits/publication-readiness-b2/notation.md`, `report.md`, `review.md`, correction ledger, and the actual independent-review receipts. Read the SD1 explanation, native export/function registers and relevant methods/evidence documents to determine the *actual* meaning and scope of `n###` before defining it. **Do not infer a universal identifier meaning from the lettering.**
2. Capture HEAD/index/worktree status and hashes for affected tracked documentation. The B2 edits are **uncommitted**; work from the actual B2 candidate state, preserve the previous full change inventory and verify both patch scopes after correction. Do not overwrite or misattribute the B2 baseline.
3. Check the reviewer history and protection rules already adopted by B2. A previous ACCEPT is evidence of prior review, **not acceptance of the newly modified snapshot**.

## 3. Limited implementation requirements

### A. Define offset and address domains with reader-friendly first use

Extend B2's authoritative notation guidance with concrete examples and a short convention for prose:

- **Native addresses:** Identify preferred virtual addresses and their pinned executable/build/image-base context at first use or through a clearly linked document-wide legend. Preserve original function identities; do not silently convert VAs to RVAs.
- **Vtable offsets:** Say `vtable byte offset 0x130` (and, only if verified, the relevant table/object type) rather than ambiguous `virtual+130`. Explain that this is a byte offset into a table of pointers, **not** an executable address and **not** a vtable slot index. Never infer the virtual slot from the byte offset without confirming pointer width and indexing conventions.
- **Native object fields:** Prefer `menu object + 0x4C8`, `item object + 0x...`, etc., when the owner is established. Distinguish a member holding a callable from the callable's destination address.
- **Other domains:** Keep save offsets, decoded/compressed record offsets, bit positions, masks and temporary buffer offsets distinct. Require the owning structure/domain to be stated at first introduction; shorter notation may follow **only while unambiguous**.
- Use explicit `0x` prefixes for **new or revised expository offset expressions**. Preserve literal archival extracts, quoted tool output, fixed identifiers, stored data tables and historical pins. Do not impose a universal formatting rewrite on native-address registers or existing experiment artifacts.

### B. Define native-analysis export IDs and their local scope

Establish what `n010`, `n039`, `n041`, and analogous `n###` labels denote in the actual SD1 native-analysis workflow. Identify their scope (e.g., experiment-specific export batch or selection, if supported), their correspondence to functions/receipts, and whether the underlying export is **tracked** or **LOCAL-ONLY**.

- Add a concise local legend **and/or** direct link from the current SD1 explanation to a durable, tracked register explaining the ID namespace and lookup procedure.
- Check other *current, reader-facing native explanations* for unexplained `n###` references or equivalent experiment-local locator conventions. Apply focused corrections where meaning and provenance can be verified. Do **not** assert that two identical labels from different experiments identify the same native function.
- Where a local export identifier cannot be resolved from surviving evidence, mark it explicitly as an **unresolved local export locator**; do not invent a mapping, relabel it as an authoritative symbol, or demand publication of proprietary/decompiled exports.
- Preserve and distinguish **scientific source pin**, **function address**, and **experiment-local native export ID**. A public reader must be able to understand a claim from tracked explanations even when raw export contents remain private.

### C. Focused contextual edits, not indiscriminate normalization

Correct the quoted SD1 paragraph and nearby ambiguous explanatory usages. Run a **bounded, recorded search** for analogous `virtual+...`, `menu+...`, `at+...`, `(n###)` and similar constructions in current authoritative/native-mechanism documents; contextually fix demonstrably unclear first-use examples. The search is an inventory of candidates, not a command to globally replace strings.

Prioritize the active roadmap-linked technical narratives. Leave primary experiment logs, unaltered source snippets, original saved bytes, historical quotes, CSV field definitions, native export payloads and exact historical evidence intact. If a historical document cannot safely be edited, put a local legend or cross-reference in its maintained explanatory entry point.

Record each changed document and the semantic owner/domain verification used. If you discover an ambiguity whose resolution requires **new substantive reverse engineering**, report a narrow unresolved documentation item instead of expanding authority.

## 4. Verification and independent review

1. Provide a concise before/after example for the SD1 paragraph, supported by existing source pins. Explicitly verify `0x130`, `0x4C8`, `0xD68`, `0xD70` and any other corrected offsets against available records **when assigning their owners**; if an owner cannot be confirmed, use a qualified rather than invented expansion.
2. Add positive/negative notation test cases: `Save52`, `kernel32.dll`, `0x140000000`, FormIDs, `n010` in a literal receipt, `+0x88`, legitimate unqualified source quote, and clear vtable/object-offset prose. The tests must distinguish formatting from identifier corruption.
3. Validate all modified Markdown links/anchors, UTF-8 integrity, tables, code fences, address/offset literals and research IDs. Supply an exact before/after token/number inventory or equivalent targeted preservation check, accounting explicitly for added `0x` prefixes and capitalized formatting without changing numeric values.
4. **Independently review the *entire revised B2 final snapshot*** against the **original frozen AC1–AC8**, with focused adversarial attention on notation clarity, identifier scope, and preservation of previous B2 improvements. The reviewer must inspect actual changes and primary provenance, must not simply rely on the earlier ACCEPT, and must not accept its own edits. Use the repository's reviewer procedure/manual independent fallback as applicable. Record ACCEPT, REWORK or ESCALATE with criterion-by-criterion evidence; remediate REWORK under this same assignment.
5. Re-run relevant full B2 document/structural, prose, UTF-8, link and preservation checks **plus** the focused new tests. Report the exact tests actually run, not invented totals. Preserve failed attempts and remediation.
6. Rebuild **both** `complete` and `task-only` unified diffs for the new final working tree, including all prior B2 changes plus the focused rework in the correct scope. Generate status, inclusion/exclusion and hash manifests; verify exact forward and reverse application/reconstruction independently as required by WORKFLOW. Ensure the complete patch includes the supplied unchanged original B2 brief only if it is actually part of the current working-tree delta. Do not accidentally include this external rework instruction as a repository change unless the project's brief-retention convention and worktree scope explicitly call for it.

## 5. Deliverables and response contract

- Updated B2 notation guide and precisely scoped explanatory documents, with tracked internal pointers to local export-ID meaning.
- A **focused rework ledger** listing candidate hits, changed and intentionally untouched occurrences, before/after expressions, verified domains and evidence references. Incorporate into B2's durable review/report record without erasing the prior reviewer/correction history.
- Refreshed full-snapshot AC1–AC8 matrix and **new independent reviewer verdict**, with exact reviewed revision/manifest identity.
- New verified **complete** and **task-only** diffs; exact forward/reverse reconstruction receipts; updated package manifest and status/inclusion/exclusion listing; protected-input/HEAD/index checks.
- A concise completion summary stating what changed, where notation remains deliberately local or uncertain, what was independently reviewed, and confirming that nothing was staged, committed or pushed.

## 6. Frozen completion contract and boundaries

**Task type:** Documentation REWORK and independent qualification of the existing B2 implementation.

**Question:** Can a technically experienced first-time reader distinguish native function addresses, vtable offsets, object fields and experiment-local export references, without changing the underlying evidence or scientific interpretation?

**Scope:** Targeted edits to current authored documentation/notation and B2 audit receipts; read-only inspection of existing native source pins and local review/export metadata. No game launch, process attachment, new native research, save editing, external scratch deletion/migration, source/evidence promotion, license/policy changes, publication, staging, commit, push or Git history rewrite.

**Mandatory acceptance:** Original B2 AC1–AC8 remain frozen and must all PASS on the revised final snapshot. Additionally the maintainer's focused readability defect must be resolved with traceable examples and appropriately scoped local identifiers; this clarification does not replace or waive any original criterion. Independent acceptance and exact verified patch delivery are mandatory.

**Negative-result closure:** Where existing evidence cannot establish an offset owner or local ID correspondence, preserve the valid literal and disclose the exact limitation; no universal or invented mapping is required. An unresolved item cannot be silently styled as known.

**Continuation authority:** Diagnose/fix/retest in-scope defects and resubmit to independent reviewer under this same task, preserving failures and frozen requirements.

**Escalation:** Stop affected actions for missing permission, protected-input mismatch, genuinely inaccessible essential evidence or demonstrably necessary new reverse engineering. Supply the exact blocker and evidence; continue independent authorized corrections.

**Review artifacts:** Original/final acceptance matrix; before/after ledger; primary references; focused and full validation; protected status/hashes; exact package manifest; both patch types; independent verdict. **Publication remains NOT CLEARED.**
