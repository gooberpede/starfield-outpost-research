# CODEX BRIEF — SOR RG2 D5BS: Native Function Catalogue Generator Modernization

**Task type:** Bounded engineering implementation and documentation, with independent review  
**Project:** `starfield-outpost-research`  
**Roadmap:** Item 6 (after D5BR readiness audit; before item 5B evidence-reader execution and B6)  
**Status on issue:** Authorized scope for Codex execution when invoked by the maintainer; **not** permission to publish, commit, push, tag or expose files externally  
**Native baseline:** `Starfield.exe` retail `1.16.244.0`, executable SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`, preferred image base `0x140000000`  
**Controlling historical source revision:** `6e799a428a765aa196a24d3c1de8ae133260aa08` (verify actual Git availability and exact applicability rather than assuming)

## 1. Purpose and non-negotiable scientific boundary

The accepted D5BD native-function reference contains **2,095 canonical function entries** (18 Level A, 366 Level B, 1,711 Level C), generated into **16 files**. The existing `research/function-catalogue/inventory.py` discovers source material by scanning broad repository directories. After D5BD, new publication and audit documents entered those directories. The later D5BG comparison found that generation against the expanded tree changes **only** `docs/audits/native-function-catalogue-d5bd/coverage.csv` and `locators.csv`; the other 14 generated files, including canonical catalogue, alias, evidence, index and subject outputs, stayed identical in that comparison.

**Goal:** Make the historical D5BD edition reproducible from a pinned, explicitly versioned source set, prevent new documents from silently changing it, and demonstrate a separate new-edition workflow for explicitly admitted current sources. This is generator infrastructure, **not** a new catalogue census or re-adjudication of accepted native functions. A test edition is not automatically scientifically accepted or selected for publication.

Preserve original D5BD results, source attribution, exclusions, ambiguities, negative controls, separate address domains, build scope and external-invocation warnings. Do not replace an unresolved locator with a guessed function entry or convert an instruction site into an entry. The existing scientific confidence and publication access classifications remain unchanged.

## 2. Mandatory reading and scope constraints

Read and substantively apply the relevant complete content of: `AGENTS.md`, `WORKFLOW.md`, `THIRD_PARTY_POLICY.md`, `docs/CHARTER.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md`; the D5BD original brief and accepted audit (`docs/implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BD_Native_Function_Catalogue_and_Developer_Reference.md`, `docs/audits/native-function-catalogue-d5bd/{README.md,closure.md}`); `docs/functions/README.md`; `research/function-catalogue/{inventory.py,verify.py}` and curated sidecars; D5BG handoff's catalogue-reproduction note; D5BR's readiness report and execution plan insofar as they establish the publication boundary; and the publication run card. Follow relevant links to original source/identity proofs needed for the changes. Recover truncated reading before substantive acceptance and record how it informed safeguards; reading chronology itself is not an acceptance test.

**Permitted:** inspect tracked authored source, Git historical blobs/trees and existing local receipts where available; create/edit project-owned Python tests, source manifests, generator tooling, versioned test-edition outputs and directly necessary documentation; execute bounded **text-only, offline** generator and tests in isolated disposable working directories, using approved project-owned source and installed CPython/stdlib; perform Git read operations and disposable checkout/export comparisons; preserve reviewed evidence in ignored local receipts. Verify paths, writes and destructive effects before running commands.

**Prohibited:** run the game, attach a debugger, execute native code or use Ghidra; acquire or decode protected original saves, game binaries, raw exports or third-party assets; alter original research observations or historic reviews; make new scientific function claims; perform network downloads, install dependencies, contact external services, upload evidence, alter Git index/refs, stage, commit, push, tag, release, archive or publish. Do not touch D5BR item-5B reader repairs or D5BJ/D5BM deferred experiments. The presence of a historic commit hash does not authorize a checkout that disrupts the working tree: use a verified disposable tree/export.

**Agents:** Primary Codex agent owns all edits. At most **one active sub-agent at a time** under `AGENTS.md`. One optional **read-only** specialist may audit historical/current source-manifest design and migration risks, then terminate before the fresh independent reviewer begins. A distinct independent reviewer is mandatory for the final exact snapshot. There is no authorization for concurrent specialists or specialist writes.

## 3. Frozen controlling questions

**D5BS-Q1 — Historical reproducibility.** Can the exact original D5BD 16-file output be reproduced byte-for-byte using a verified historical source set, without hidden access to the current source tree or `.local-work/`? A negative must identify precisely which unavailable bytes or provenance prevent this and the smallest lawful remedy; a current-tree approximation is not a PASS.

**D5BS-Q2 — Explicit source and edition identities.** Can every source influencing an edition be selected by an explicit, versioned manifest with defined content/revision identity, deterministic order and failure on missing/mismatched inputs? Historical and new editions must have separate source identities and write boundaries.

**D5BS-Q3 — Safe generator and new-edition operation.** Can the generator consume the selected manifest, leave the stable historical public outputs unchanged, and demonstrate a separately located current-source **technical test edition** without promoting it as accepted science? Changes to later research documents must not silently mutate the historical outputs.

**D5BS-Q4 — Independent regression and documentation.** Can an independent reviewer validate exact old-output identity, deterministic new-output generation, failure and drift controls, links, source provenance, safe effects and the complete delivery snapshot, with no unapproved output or repository effects?

## 4. Design requirements and implementation discretion

### 4.1 Historical edition is immutable by default

Preserve the existing user-facing `docs/functions/` catalogue and D5BD audit paths, and their currently accepted contents, as the historical edition. Existing links must continue to resolve. Do **not** silently overwrite those files simply because newly discovered sources would change their generated audit rows. A deliberate, separate explicit maintenance procedure may be offered only if it cannot silently rewrite the accepted edition and its authorization boundary is documented; default normal verification must be read-only.

Establish actual availability of the source bytes at historical Git revision `6e799a428a765aa196a24d3c1de8ae133260aa08`. If a historical source file differs from today's copy, reconstruct it from that verified historical tree or from an independently pinned, lawful source snapshot; an ordinary path-only manifest against HEAD does not suffice. Record exact source-revision/tree identity and relevant manifest/hash identities. Do not automatically embed an entire historical repository, proprietary bytes or unrelated archive in the current checkout.

### 4.2 Manifests, editions and isolation

Use a simple, auditable project-owned manifest format (JSON, TOML or similar) chosen by Codex. It must explicitly enumerate the source set (and any essential curated sidecars or reference guides), its order or a deterministic ordering rule, a pinned revision/content identity, edition/build identity, output namespace and expected output set. Design for a future different executable build without conflating `(executable SHA-256, module, entry RVA)` identities. Manifest completeness must be auditable and fail closed if selected inputs are missing, unexpected or have wrong bytes; optional diagnostic flags must not quietly weaken this for official reproduction.

Historical output paths stay stable. A current-source test edition must write only under a distinct, clearly labelled **non-public/test** namespace or disposable output directory; it must not overwrite the 16 accepted files. If material current source changes would affect canonical entries, preserve the differences and source/evidence context as unreviewed; do not auto-accept an expanded catalogue.

Preserve all existing source-coordinate and alias semantics, original exclusion accounting and provenance domains. The manifest must not make changed original-line references falsely appear to refer to historical physical lines in the current files. Explain whether source links in a historical edition resolve to a historical revision or to unchanged current text and identify unavoidable limitations.

### 4.3 Drift diagnostics

Provide a bounded, read-only check that reports research/audit source material outside an edition's selected manifest that could change the broad scanner's coverage or warrant future consideration. Reporting is not admission: no newly scanned file can mutate a frozen edition. Avoid claiming this diagnostic proves exhaustive new native-function discovery; broad address matching includes globals, instruction sites and unrelated text. Keep a stable, reviewable output with file identities and the reason each document is outside the manifest. Do not make an ever-growing set of unrelated files a hard failure of historical reproduction; distinguish **manifest-input mismatch** (hard failure) from **unselected-source drift** (informational/auditable).

### 4.4 Compatibility and verification entrypoints

Give the public developer a minimal documented command for exact D5BD reproduction from the correct historical inputs, and a separate explicit command for generating/verifying the test edition. Preserve reasonable existing `research/function-catalogue/verify.py` usage where feasible; if behavior or entrypoints change, document a compatible wrapper or exact migration. `--write` or equivalent must never target the wrong edition by default. No network, proprietary source, installed game or ignored local receipts may be prerequisites for the text-only catalogue build.

## 5. Required proof and controls

The primary agent must retain a baseline snapshot and produce actual receipts for:

1. **Historical exactness:** verify every one of the 16 original generated files byte-for-byte and against original accepted hashes or a verified original tree, including the two D5BG-drifted audit outputs. Report all target paths and hashes, not only catalogue count. Keep accepted current working-tree originals untouched.
2. **Current-tree isolation:** add unrelated relevant-looking authored audit text in a disposable test tree; show historic-generation hash equality and a separate diagnostic for the unselected source. Do not change the original checkout merely to stage the control.
3. **Edition separation:** build the explicitly selected current-source technical edition twice from equivalent clean inputs and compare all output bytes; show its generated paths cannot collide with historical output paths. If today's source scan yields the same 2,095 canonical entries, do not misdescribe that as a new scientific census.
4. **Fail-closed cases:** missing manifest member, altered selected-source bytes, incompatible build/edition identifier, malformed manifest, duplicate source entry and output-path collision. Record which controls fail before any output is modified; verify no partial overwrite or inappropriate fallback.
5. **Semantic regressions:** 2,095 original canonical identities and the A/B/C 18/366/1711 distribution; historical alias collisions (`SOR-FN-0062`–`0064` and other retained checks), excluded interior sites, source namespaces and all 18 subsystem crosswalks. Reuse and extend the existing regression suite, avoiding a new unqualified native interpretation.
6. **Navigation/provenance:** existing public links, generated anchors, source-line referents and build pins remain correct. A future edition may refer to its own admitted sources but cannot inherit historical correspondence just from matching address strings.
7. **Effects and preservation:** verify source copies, untracked documents, HEAD/index and protected originals before/after; isolate outputs/scratch; honor the project's existing dual-drive free-space and retention safeguards where applicable; no stage/commit/push.

If exact historical reproduction is impossible with lawful available source bytes, do not substitute a weaker result and label Q1 COMPLETE. Record the exact blocker and smallest required permission/input; continue the other authorized branches where meaningful, then return an appropriate ESCALATE, rather than silently dropping Q1.

## 6. Required durable deliverables

Place the minimal implementation and tests in the existing `research/function-catalogue/` family and the edition/manifest data in a clearly named, versioned project location. Add concise developer documentation covering purpose, historical and test-edition invocations, source-version provenance, outputs, expected differences, drift interpretation, safety effects, and publication boundaries. Keep a task-specific audit under `docs/audits/` recording:

- Answer-first D5BS-Q1–Q4 results and a PASS/FAIL/NOT TESTED matrix for acceptance criteria.
- The exact historical source set/commit, manifest and 16 output checks; original versus current-source comparison of `coverage.csv` and `locators.csv`.
- Explicit file/output inventories, actual commands and outcomes; changed-input, malformed-input and collision negative controls.
- Any outstanding source/provenance limitations, alternatives, deviations, preserved failures, and precise next action.
- The qualified test-edition outputs as **engineering demonstration only**, clearly not approved for public release.
- Independent reviewer return and final-snapshot assessment, separate scientific / engineering / editorial / publication outcomes.

Avoid indiscriminately expanding the archival surface: generated test outputs may stay in ignored, hash-pinned local receipts if the versioned procedure demonstrates them independently. Do not introduce many redundant generated text files to the release tree without a demonstrated need. Where a new source manifest references historical Git, ensure normal clean-checkout reproduction is feasible with documented access to that Git object or an explicit lawful snapshot; otherwise record the remaining historical dependency rather than claiming standalone success.

## 7. Mandatory acceptance criteria

- **AC01 — Reading and authority:** Complete relevant required reading by substantive acceptance; documented applied understanding; no prohibited operations or unintended side effects.
- **AC02 — Frozen baseline:** Precisely establish the original source revision, full original 16-path/output identity, and the two known current-scan drift files without changing prior findings.
- **AC03 — Exact historical reproduction:** Demonstrate byte-exact 16/16 regeneration using the historical source set, including `coverage.csv` and `locators.csv`, with independently checkable receipts.
- **AC04 — Manifest identity:** Manifest is explicit, deterministic, edition/build-aware and source-byte/revision pinned; missing or mismatched source fails closed.
- **AC05 — Isolation:** New documents and explicit current-source edition cannot alter accepted historical paths or contents; a clean two-run new-edition check passes.
- **AC06 — Drift:** Unselected candidate sources are reported separately without being auto-admitted; false-positive lexical leads are not promoted to functions.
- **AC07 — Regression:** Accepted 2,095 entries, depth distribution, identity domains, alias collisions, exclusions, crosswalks and evidence-source distinctions remain consistent for D5BD.
- **AC08 — Failure safety:** Negative cases for altered/missing/duplicate/malformed inputs, build mismatch and output collision are exercised; no partial or unauthorized writes.
- **AC09 — Reproducible methods:** Portable, accurately documented entrypoints and explicit required tools/inputs, independent of `.local-work/`, original saves, native exports and game runtime.
- **AC10 — Preservation:** Input hashes and source/index/HEAD state preserved; complete tracked/untracked output and exclusion inventories; no user-unapproved Git or external actions.
- **AC11 — Documentation/editorial:** User-facing paths and links remain correct; edition and publication status unambiguous; complete changed-prose manual reading and editorial screen with resolved findings.
- **AC12 — Independent terminal review:** Fresh reviewer assesses the original frozen Q1–Q4 and AC01–12, source bytes, negative controls, exact file inventory and scientific limits; independently verifies complete/task-only patches' forward and reverse reconstruction and final reviewed snapshot. An initial REWORK is corrected and resubmitted **within the same assignment**. A terminal evidenced blocker requires ESCALATE, not an unsupported PASS.

## 8. Execution and completion contract

**Question-level gate:** Q1–Q4 must reach substantive COMPLETE with evidence, or an exact terminal BLOCKED result with barrier, attempted remedies and smallest requested action. A method-level success cannot close an unanswered parent question. Preserve failed attempts and alternative hypotheses in an active investigation ledger opened near the start.

**Continuation:** Diagnose, correct and retest ordinary implementation or validation failures within this assignment; do not request a fresh brief for routine fixes. Hard stops apply to protected-input identity, free-space/safety breaches, unapproved writes, external access or missing essential authority. No arbitrary elapsed-time, evidence-volume or monitoring-cadence cutoff.

**Review:** Independent review receives original brief, original D5BD/D5BG decision and source evidence, active ledger, actual test receipts, proposed changes and counterexamples. Review must challenge whether a hidden current-tree dependency remains and whether a future edition can touch historical output. Confirm optional specialist termination before reviewer start.

**Handoff:** Provide concise summary, exact artifact paths, Q1–Q4 COMPLETE/INCOMPLETE/BLOCKED dispositions, AC01–12 PASS/FAIL/NOT TESTED, known differences, original-current checks, developer commands, review verdict, failed/negative tests, manifest of all authored changes and exclusions, and both task-only/complete unified diffs with SHA-256 and exact forward/reverse verification. The complete patch includes the supplied brief if it is an untracked input; task-only excludes it. Explicitly report HEAD/index and staging status. Do not commit or publish.

**Scope after completion:** This assignment closes roadmap item 6 only if accepted. D5BR item 5B original-save reader qualification, release asset clearance, archival and B6/publication remain separate pending work. Current-source test-edition acceptance is an engineering result, not scientific approval or visibility authorization.
