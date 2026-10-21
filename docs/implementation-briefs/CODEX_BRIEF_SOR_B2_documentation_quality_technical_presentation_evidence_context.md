# Codex implementation brief — B2: Documentation Quality, Technical Presentation and Evidence Context

**Project:** `D:\Projects\starfield-outpost-research`  
**Task:** B2 publication-readiness documentation correction and technical-presentation improvement  
**Status:** Maintainer-approved scope; execute only under repository permissions and workflow  
**Starting authority:** B0 release policy, RR1 publication audit, B1 navigation/roadmap, original scientific reports and independent reviews. Publication remains **NOT CLEARED**.

## 1. Purpose and governing principle

Prepare the authored, tracked research documentation for a coherent public research archive by correcting verified prose/encoding/notation faults, improving explanation of selected technical mechanisms through **original analytical pseudocode or decision tables**, and making historical-save examples intelligible even where their source evidence remains local-only.

**Preserve scientific meaning, provenance and historical evidence.** This is a documentation implementation, not new outpost reverse engineering, source promotion, save decoding, licensing clearance or publication. B1's research roadmap is the reader-facing authority; RR1's findings and B1's pseudocode candidates are initial inputs, not exhaustive defect or improvement lists.

## 2. Mandatory preparation and provenance

1. Read `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `PUBLICATION.md`, the B0 policy/release-gate documents, RR1 report and ledgers, B1 report/pseudocode candidate register, and existing documentation conventions.
2. **Before a fresh general scan**, retrieve the earlier independent reviewer reports and correction records documenting malformed prose, UTF-8/mojibake issues, malformed Markdown, or changed technical notation (including L3, SD1, BM1, and relevant earlier reviews). Extract confirmed failure specimens and reviewer resolutions. Create positive and negative scan fixtures, ensuring valid identifiers such as `Save52`, `kernel32.dll`, `0x140000000`, `+0x88`, EditorIDs and compact record names do not trigger false replacements.
3. Establish a baseline tracked-file inventory and Git state. Record the exact HEAD, index/worktree status, file identities and any source hashes/pins whose historical bytes require protection. Existing scientific reports, source pins, saves, local evidence and user inputs are protected; capture before/after hashes for any authorized tracked documentation edit.
4. Read accepted mechanism explanations before adding pseudocode. Cite authoritative accepted reports and independent review status; distinguish source-proven behaviour from qualification, interpretation and examples.

## 3. Workstream A — prose, encoding and Markdown corrections

Conduct a wide contextual audit of **tracked authored text**, including Markdown, pertinent CSV/TSV and textual documentation. Cover not only RR1 flagged files but other authoritative and historical authored documents. Prioritize active reader-facing material and demonstrated defects.

- Recover omitted spaces such as `Save52contains` or `recordat0x88`, without damaging valid identifiers, file names, hexadecimal forms, code, original logs or quotation evidence.
- Detect and correct confirmed UTF-8 corruption and mojibake, broken Markdown tables, malformed fences, links/anchors and incidental whitespace defects.
- Distinguish a textual error from a historical reproduction of an error; preserve original measurements, source excerpts, raw transcripts and intentionally preserved failure specimens. If an archival passage must remain literal, provide explanatory annotation elsewhere rather than silently changing it.
- Verify repaired technical values against authoritative evidence; never guess replacement bytes, bit indices, masks or offsets from typography alone.
- Maintain an **occurrence-level correction ledger** with file/location, original and corrected reading, classification and rationale, plus explicit retained exceptions.

Do not undertake global regex rewrites or claim universal cleanliness from a zero-match scan. Treat scan matches as review candidates with human/contextual verification.

## 4. Workstream B — consistent technical notation

Create or refine a concise reader-facing convention, aligned with existing `docs/EVIDENCE_STANDARD.md` and provenance conventions, distinguishing:

- executable version and image base; preferred virtual address versus RVA/module-relative address;
- native structure/member offset versus serialized save offset versus compressed/decoded-record offset;
- hexadecimal masks versus bit indices (`0x10` is not bit index 10), fields and signed/unsigned decimal values;
- FormID/EditorID, record signature, persistent saved form/reference identity versus transient pointer/handle;
- units and frames: local units, seconds/game days, terrain indices, angular degrees/radians;
- evidence-hash and historical version scope.

Correct **actual inconsistencies**, including RR1's known mask/bit ambiguities, with exact source checks. Do not force different semantic domains into one notation or retroactively re-pin historical experiments. Include a concise reviewer-checkable identifier/number preservation test.

## 5. Workstream C — selective analytical pseudocode

Start with B1's eight candidate areas and assess the current authoritative explanation before editing. Prefer pseudocode, decision tables or compact diagrams where they materially clarify **algorithms, selection filters, event sequences or state transitions**; do not impose a quota or rewrite prose for appearance alone.

High-value candidates include Workshop ownership/membership, production scheduling and normalized aggregate rate, cargo/fuel timing, construction catalogue visibility/locks/admission, inventory and Stored Resources eligibility/aggregation/shared backing deduplication, and nominal biome enumeration. Select the cases that actually need improvement; record justified exclusions.

For every substantive addition:

1. Mark it clearly as **analytical pseudocode**, not decompiled or verbatim engine source.
2. Ground each branch/operand and important exception in accepted research references; preserve uncertainty and coverage.
3. Compare the pseudocode against its authoritative mechanism report, including relevant edge cases and counterexamples. Produce a scientific-semantic review checklist separate from punctuation checks.
4. Avoid copying full decompiled functions, `.asm`/`.c` game-source files, bulk disassembly or game assets. Short justified technical snippets and original analysis follow the adopted B0 policy, with applicable rights controls.
5. Favor adding clear current reference material or small improvements over rewriting primary experimental history.

The goal is reader comprehension without sacrificing implementation distinctions, such as cached versus realized production, resource source eligibility, unpowered states, virtual backing inventory, snap-behaviour replacement identity, and qualified biome frame assumptions.

## 6. Workstream D — historical evidence context and dangling references

Audit references to unpublished/local-only inputs throughout tracked reader-facing material, including **Save52**, named historical outposts such as **Feynman V** and **Carinae III-c**, numbered save aliases, private screenshots, ignored `.local-work` receipts, absolute machine paths and historical extract outputs.

For each material occurrence distinguish:

- **Self-contained explanatory example:** contextualize the outpost, planet, source save, relevant observed property and supported result, with a link to an accepted report;
- **Evidence-dependent demonstration:** identify precisely what local input a reader needs to independently reproduce it, and what publicly documented derived observations are sufficient to understand it;
- **Unresolved/dangling reference:** identify missing context or an unavailable referenced artifact, without inventing the data;
- **Historical literal provenance:** retain and annotate when alteration would corrupt evidence.

**A mere mention of Save52 or Feynman V does not mandate publishing the mature save.** It does mandate a meaningful explanation and honest statement of evidence availability. If independent replication genuinely requires Save52 or a smaller derived artifact, register this for B4's per-asset decision; do not copy, sanitize, publish, compress or promote saves during B2. Apply the same principle to screenshots and compiled/native evidence.

Provide an **evidence-dependency register** listing affected text, source identities, current access tier, proposed context/links and any B4 follow-up. Fix actual broken tracked relative links within scope; distinguish deliberately local-only paths from broken public documentation links.

## 7. Scope and write authority

**Permitted:** offline repository inspection, relevant archived review receipt reading, qualified read-only checks of installed declarations or local evidence **only to verify documentation references**, contextual edits to authored tracked documentation, new documentation conventions, corrections ledger, pseudocode/evidence-context registers, validation helpers limited to this audit and the review package.

**Not permitted:** game launch; debugger or live instrumentation; new scientific reconstruction; editing or generating saves; moving/promoting source/evidence; deleting any local work; rewriting Git history; manipulating external installed tools; altering GPL/third-party permissions or publication clearance; committing, staging, pushing, tagging, publishing or uploading assets. Leave primary experimental logs/raw outputs verbatim. The approved textual changes must not require reclassifying accepted scientific claims. Escalate material contradictions or required scientific changes as narrow exceptions; continue safe independent corrections.

Only touch existing files demonstrably needed for B2 and new B2 audit/supporting documents. Respect historical exact-hash pins and record revised documentation hashes without altering the historical evidence claimed by those pins.

## 8. Required deliverables

Place the durable B2 package under a suitable `docs/audits/publication-readiness-b2/` directory, with entries in the existing documentation audit/implementation-brief indexes where appropriate:

1. `report.md` — answer-first completion and scope, categories, totals, material unresolved items and B4 handoff.
2. `corrections.md` (or appropriately split machine-readable ledger) — contextual before/after fixes, validated exceptions, baseline defect cases, source/hash implications.
3. `notation.md` or a link to an updated authoritative conventions document — precise domain-aware technical notation.
4. `pseudocode-review.md` — candidate evaluation, selected changes, per-case evidence and semantic correspondence tests, explicit cases not changed.
5. `evidence-dependencies.md` — named local historical examples, context sufficiency, broken/deliberate links, candidates reserved to B4.
6. `review.md` — original criteria, PASS/FAIL/NOT TESTED matrix, verification receipts, failures/corrections, protected input/hash table, independent reviewer disposition and limitations.
7. Verified task-only and complete unified diffs, status/inclusion/exclusion inventories and exact forward/reverse patch reconstruction receipts. No staging/commit/push.

The precise filenames may vary to match repo conventions, but all content and cross-links are mandatory.

## 9. Frozen assignment completion contract — eight mandatory criteria

**Task type:** documentation implementation and contextual audit; no fresh scientific research.

- **AC1 — Authority and input safety.** Demonstrate correct repository baseline, review of controlling policies, immutable primary evidence, and no unauthorized external/save/game/Git operation.
- **AC2 — Historical defect-led audit.** Recover previous independent-review examples; validate positive and negative scan fixtures; examine all in-scope tracked authored text with contextual classification and reproducible coverage receipts.
- **AC3 — Correct prose, UTF-8 and Markdown.** Repair all confirmed in-scope defects discoverable through this bounded audit or explicitly retain justified historical exceptions. Preserve identifiers, quoted evidence, source pins and semantic content; provide occurrence-level ledger and regression checks.
- **AC4 — Precise notation.** Establish applicable notation standard; resolve known genuine bit/mask/address/offset ambiguities against evidence and verify unchanged numeric identities.
- **AC5 — Scientific-quality pseudocode.** Evaluate B1 candidates; implement selected valuable original analytical pseudocode/decision tables and validate their semantics against accepted findings via a distinct substantive review.
- **AC6 — Reader context and dependencies.** Audit local-only/save/named-outpost references including Feynman V, Carinae III-c and Save52; fix context and links where supported; inventory material B4 publication/access decisions without mandating full save publication.
- **AC7 — Durable documentation and coverage.** Deliver accessible reports/registers with current-versus-historical distinctions, unresolved cases, source/version provenance and intact relative links; no new scientific claims or rights decisions.
- **AC8 — Independent critical review and package.** Obtain independent reviewer ACCEPT on the frozen criteria, repair in-scope REWORK findings, report the final pass/fail matrix and separate scientific/integrity/authority/publication statuses, run tracked-link/Markdown/UTF-8/identifier/hash checks and verify exact complete/task-only patches forward and reverse.

**Negative-result closure:** A candidate pattern proven to be a legitimate identifier, intentional literal quote or harmless historical locator is a correctly documented negative finding, not a forced edit. A pseudocode candidate that would add no clarity or cannot be supported by accepted evidence may be explicitly deferred with rationale. No claim of absolute repository-wide absence is required beyond the declared corpus and scan limitations.

**Continuation authority:** Diagnose, correct, recheck and resubmit in-scope failures within existing bounds. A reviewer REWORK returns the same assignment for correction; an independent reviewer cannot accept its own changes. Material science changes, missing permissions or protected-input/hash violations require a narrow evidenced escalation, not silent relaxation.

**Exit / escalation:** Stop affected operations on protected-input mismatch, integrity/tool failure, missing essential evidence, unsafe output/disk state or absent authority. Preserve logs, candidate/exception inventories and resume checkpoint. Follow the repository's existing free-space, identity, worker/STOP and historical-evidence safeguards; do not invent arbitrary time or test caps for healthy offline work.

**Review artifacts:** final matrix, primary evidence pointers, scan fixtures, occurrence ledger, semantic-pseudocode checks, local evidence-dependency register, status/inclusion/exclusion lists, exact diffs and reviewer decision. Publication remains **NOT CLEARED** independently of AC1–AC8 success.

## 10. Suggested implementation sequence

1. Baseline + controlling docs + archived reviewer defect taxonomy.
2. Contextual scan with false-positive tests and targeted corrections; separately inventory identifier ambiguity.
3. Evaluate B1 pseudocode candidates; draft, compare and scientifically review additions.
4. Resolve reader context for named saves/outposts and inventory B4 dependencies.
5. Rerun structural, numerical, UTF-8, link and semantic regressions; independently review.
6. Deliver both patch forms and review package for maintainer critical diff review. **Do not commit or publish.**
