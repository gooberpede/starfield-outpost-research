# Codex implementation brief — Repository-wide documentation spacing repair

**Project:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)  
**Mode:** Documentation maintenance only; **one primary Codex agent, no sub-agents of any kind (including no reviewer agent)**.  
**Authorization:** Offline repository inspection, documentation corrections, validation and review-package preparation. **No staging, commits, pushes, Starfield access, save modifications, native instrumentation or deployment.**

## Purpose and context

Research documents contain widespread missing whitespace between ordinary prose and numerals. Examples include:

- `The supported Save52 inventory increases from657 to848 physical roots` → `The supported Save52 inventory increases from 657 to 848 physical roots`.
- `The191 additions are51STAT,89FURN and51PKIN` → normal readable prose with spaces between quantities and record-type identifiers, while retaining the exact numbers and record types.

The goal is to repair these defects consistently **without changing factual claims, evidence interpretation, scientific statuses or technical identities**. This is a standalone cleanup. Do not undertake the inorganic-resource availability investigation in this assignment.

## Scope and preservation

1. Survey authored Markdown documentation throughout the repository, including `docs/`, root documentation and applicable documentation templates. Include headings, paragraphs, tables, captions, blockquotes and prose inside Markdown documents. Investigate any other **authored textual documentation** demonstrably affected, but identify its format before editing.
2. Correct missing spaces where normal English typography requires them, especially around counts, dates, versions when used as prose, units, and record-type labels. Adjust nearby punctuation only where necessary for readability, while preserving meaning.
3. **Do not blindly insert whitespace at letter/digit boundaries.** Legitimate tokens that must remain unchanged include `Save52`, `ExtraFlags9C`, `ExtraWorkshop`, `FormID`, `Starfield.exe`, `0x140F4AB80`, `+0xD3`, `ff01b58f`, `FURN`, `STAT`, `PKIN`, identifiers, file paths, URLs, command-line options, JSON keys, code snippets, source names, version numbers and native offsets. Check context for ambiguous cases.
4. Protect code fences, inline code, shell commands, JSON/XML literals, source excerpts, patch fragments, serialized examples, machine-readable fixtures, quoted primary-source material, link destinations/anchors and source identifiers. Do not alter them merely for typographic consistency. If a broken sentence is inside a literal or quotation, document it rather than silently rewriting primary evidence.
5. Do not edit raw or sealed research evidence, saves, binaries, logs, private `.local-work` receipts, Ghidra databases or historical original tool outputs. Historical **authored interpretation** can be corrected typographically while preserving its exact substance and historical verdicts.
6. Research source and test code must remain untouched unless a **demonstrated documentation generator or template bug** is responsible. If such a cause exists, fix only the text-emission defect and add a narrowly scoped regression test; do not change scientific computation.
7. Do not change scholarly attribution, permission records, experiment classifications, scientific figures, acceptance matrices, confidence levels, filenames, evidence IDs or numerical values.

## Work plan

### A. Discover and classify

- Start from a clean understanding of the current Git working tree and the committed project baseline. Respect pre-existing uncommitted changes if any; do not revert or mix unrelated work.
- Inspect a broad inventory of Markdown files and identify the recurring defect patterns. Use detection scripts where useful, but distinguish candidate matches from confirmed defects; false positives are expected in technical documentation.
- Check whether a generator, template, formatting pipeline or copying/encoding step is responsible. Report either a demonstrated cause or `cause not established`, rather than speculating.
- Retain a concise audit ledger of affected paths and representative examples, including ambiguous tokens deliberately excluded.

### B. Repair carefully

- Apply targeted edits with context-aware verification. An automated transformation may help propose changes, but **every class of transformation requires human-readable before/after inspection** and checks against protected technical strings.
- Keep changes focused on malformed word/number boundaries and obvious associated typographic spacing. Do not reformat entire documents, change section structure or rewrite technical explanations.
- Preserve counts and numerical values exactly; correct their separation from surrounding words and punctuation, not their substance.
- If a candidate is ambiguous, do not guess. Preserve it and record why it was excluded; investigate enough surrounding context to resolve avoidable ambiguities.
- Continue until the full in-scope documentation corpus has been scanned and the confirmed defects repaired. Do not stop after fixing the illustrative examples.

### C. Validate and package

- Independently rerun the full detection pass and examine remaining candidate matches, classifying them as legitimate notation, protected literal material or unresolved ambiguity. There should be no **known** unfixed ordinary-prose examples within scope.
- Check Markdown links, reference paths, whitespace errors, Unicode preservation and document encoding. Verify the technical-value/identifier inventory and text-level semantic preservation wherever possible.
- Run relevant documentation checks, and any affected generator regression test. Do not run unnecessary expensive native/code tests for documentation-only edits; explain if a specific check is inapplicable.
- Preserve and report unrelated pre-existing changes. Generate `-task-only.diff` and `-complete.diff` beneath `.local-work/diffs/`, including newly authored text files, as required by `WORKFLOW.md`; provide `git status --short`, changed-file and exclusion manifests, patch applicability/reversibility checks and supporting receipts.
- **Do not spawn a reviewer or specialist agent.** The maintainer and ChatGPT will critically review the submitted diff after Codex finishes.
- Do not stage, commit or push. Do not include local generated diagnostics or raw project data in the commit-ready patch unless a small authored report or regression test is necessary.

## Completion contract

Return **COMPLETE — PASS** only when the entire authorized authored-documentation scope has been surveyed, all confirmed spacing defects have been corrected, protected technical material has been checked, and the review package is ready. In-scope formatting defects and failing validations are for Codex to resolve **within this assignment**, not to return as a follow-up request.

If a genuine authority, integrity or external-access blocker prevents completion, report precisely what blocked progress and which work remains; do not relabel an incomplete cleanup as a scoped success. No arbitrary time, file-count or volume quotas; retain the established disk-space and input-preservation safeguards.

## Handoff

Provide a compact summary with:

- Total authored files scanned and files changed (distinguished).
- Representative corrected strings and legitimate technical tokens deliberately preserved.
- Whether a common generating cause was verified and, if so, its precise fix.
- Check results and remaining explicitly classified ambiguities.
- Exact paths to complete and task-only diffs, status/manifest, and any brief supporting audit report.
- Suggested commit subject only; **no commit or push**.

**Do not start the next inorganic-resource availability task.**
