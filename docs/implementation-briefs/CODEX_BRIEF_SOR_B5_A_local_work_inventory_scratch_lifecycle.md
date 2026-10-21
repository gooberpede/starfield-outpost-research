# Codex implementation brief — SOR B5-A: local-work inventory, scratch lifecycle and reviewed deletion proposal

**Status:** Maintainer-authorized brief for Codex execution; this document is the assignment, not evidence of execution or approval of deletions.  
**Project:** `D:\Projects\starfield-outpost-research`  
**Type:** bounded repository/tooling maintenance, retention audit, and documentation.  
**Release status:** NOT CLEARED. B5-A does not authorize publication or B5-B deletion.

## Objective and source authority

Make the project's local research workspace sustainable: account for major disk consumers, preserve unique and useful scientific evidence (including prospective follow-up work), prevent uncontrolled temporary-file accumulation, and produce a **precise, independently reviewed deletion-candidate manifest** for subsequent maintainer approval. Aim for meaningful, demonstrated reclamation opportunities; **no preset byte target**, and do not accept a trivial proposal that ignores the major consumers without substantiated retention reasons.

Read and apply `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/PERMISSIONS.md`, `docs/audits/publication-readiness-b0/local-work-retention.md`, `docs/audits/publication-readiness-b0/release-gates.md`, `docs/audits/publication-readiness-rr1/external-material.md` and B3/B4-F1 evidence/source manifests. Current governing documents prevail over older plans. Maintain provenance and historical source hashes. Record actual starting Git state and protected identities.

## Non-negotiable retention boundaries

**Never propose deletion of these four directory roots:**

- `.local-work/diffs/`
- `.local-work/scratch/`
- `.local-work/screengrabs/`
- `.local-work/savegames/`

Their **contents** may be audited at file/subtree granularity; neither blanket retention nor blanket deletion follows from residence there. Preserve reviewed patches and useful delivery history in `diffs`; preserve the usable scratch area; preserve original or scientifically useful screenshots; treat `savegames` especially conservatively (maintainer reports about **190 MB**, planning estimate only). An original or unique saved state with no verified recoverable copy **cannot** be proposed for deletion, even if no current tracked document links to it. Do not privilege small savings there over evidence safety. Explain the local-scaffolding expectation and how the directory roots continue to exist after cleanup.

Preserve original captures/WALs, unique failed-run evidence and receipts, original saves/screenshots, B3 exact historical source, B4-F1 approved core/addendum archives and their protected constituent identities, and uniquely significant Ghidra/manual-analysis state **outside the repository**. Installed Ghidra, xEdit, x64dbg, game installations (including executables/ESMs/BA2/INI/libraries) and `D:\ReverseEngineering` are external dependencies and **not cleanup targets**. Don't move them into the project. First-party publication approval for the B4-F1 core/addendum **does not grant deletion authority**.

## Scope and methods

### A. Measure and classify significant storage

Inventory `.local-work/` comprehensively enough to **account for its large contributors**, refreshing the previously reported ~30 GB rather than relying on it. Provide actual bytes, file counts, timestamp and method, top-level and substantial nested consumers; identify duplicates by reliable hashes/identities where warranted. Classify **individual files or defensibly uniform subtrees** as:

1. Unique, irreplaceable or practically costly evidence useful now or for follow-up research — retain.
2. Source/build configurations or historical method versions — retain as authoritative tracked or local copies per B3; do not destroy original source evidence merely because another version exists.
3. Legitimate protected/local-only dependencies and durable receipts — retain.
4. Demonstrably duplicate, reproducible, obsolete or disposable scratch — candidate for deletion **only after** verified dependency and recovery assessment.

Evaluate actual reconstruction cost, external input accessibility and reproducibility, not hypothetical regeneration. Account explicitly for review-application trees, snapshot duplication, built observer/packaging outputs, temporary acquisition artifacts and other large families. Rank opportunities by **safely reclaimable bytes**, giving reasons for retained large consumers. No age-only, extension-only, ignored-status-only or pathname-prefix-only classification. A result proposing merely a handful of empty Temp trees while leaving significant space unexplained is insufficient.

### B. Reference and dependency closure

For every candidate, check references/consumers in tracked Markdown/CSV/code/build files **and relevant untracked manifests, receipts and local helpers**. Distinguish historical provenance references from *operational* prerequisites and links readers must follow. Flag any candidate whose deletion would leave dangling references, break current reproduction directions, orphan protected evidence or destroy the sole original of a historical method. Give exact paths and proposed replacement/correction, and **block deletion** until a replacement is verified or the maintainer expressly approves the documented exception. No silent historical source repinning or deletion of evidence merely because a current report is accepted.

### C. Scratch-creator remediation

Review named RR1 leads first, then other actively maintained creators discovered during the audit:

- `.local-work/position-resumption/package_review.py` and `.local-work/native-oracle/package_review.py` using default Temp `mkdtemp` and associated `sor-position-patch-*` residue (29 empty trees at the *RR1* inspection, not an assertion of current state).
- Historical scripts capable of recreating `D:\tools` outputs.
- Maintained x87/internal-observation qualification package scripts and test helpers using `TemporaryDirectory()` — recognize ordinary automatic cleanup as legitimate, not proof of leakage.
- Current project-owned packagers whose scratch creation or output paths undermine source reproduction.

**Prefer self-cleaning workspaces** (`try/finally`, context management) that clean both normal completion and exceptions. If a process needs resumable state, make it explicit, retained under approved project-local paths with a separately callable safe cleanup/retirement method after the required receipts are preserved. The preferred current review-application scratch is `.local-work/review-patches/`, within the repository's Git-discovery boundary; check current `WORKFLOW.md` rules. Obsolete historical source must retain its original provenance: retire its entrypoint or supply a maintained wrapper/successor rather than silently rewriting frozen source.

Only repair **project-owned current** scripts within the approved bounds; do not alter tool installations, archived historical bytes, installed scripts, game inputs or protected original evidence. Perform **safe, isolated synthetic** normal/exception tests for corrected live entrypoints, checking no unexplained external residue and ensuring essential receipts survive. Do not run scripts against game process, Ghidra, xEdit, original saves, native analysis databases or any installed target. If synthetic execution would violate safety/authority, record the precise blockage and do authorized static work; don't fabricate a PASS.

### D. Exact deletion proposal, not deletion

Produce a machine-readable manifest with for each proposed file or *enumerated* subtree: original absolute resolved path, relative owner root, file/dir nature, count, measured bytes, hashes and identity as appropriate, source/creator, duplication or regeneration proof, reference audit, unique/protected descendants, risk and future research value, estimated recoverable bytes, disposition and required maintainer approval. Include current free-space checks on affected volumes (preserve existing 40,000,000,000-byte C:/D: guards where applicable), symlink/reparse/junction/out-of-root defenses, identity recheck plan and recovery/stop conditions.

Treat each candidate as **PROPOSED, NOT AUTHORIZED**. No deletion, moving, overwriting, cleanup of Temp, `git clean -xfd`, broad globs, history manipulation, Git garbage collection or tree pruning in B5-A. Any future B5-B action must be limited to specifically approved paths, freshly rechecked against the manifest, with before/after preservation receipts and actual reclaimed space.

## Required deliverables

Create coherent, linked reports under `docs/audits/publication-readiness-b5/` (choose clear filenames and register them in the report):

- Answer-first housekeeping report: measured storage distribution, leading retention/reclamation classes, meaningful savings opportunity and exact limits.
- Size/retention ledger with top storage consumers, scientifically useful follow-up evidence, duplicates and unrecoverable/practically expensive classes.
- Exact deletion-candidate manifest (CSV or JSON with stable IDs) plus separately stated **HOLD** inventory. If no large safe opportunities exist, document positive evidence accounting for the large consumers.
- Tracked-and-local reference impact register, especially dangling links/locators and operational prerequisites.
- Scratch-creator inventory and remediation/retirement notes, with test results for current repaired wrappers.
- B5-B proposed execution/safety plan restricted to reviewed manifest IDs and requiring a **new, explicit maintainer deletion approval**.
- Review/verification records, protected-input/HEAD/index checks, changed-file and included/excluded inventories, verified complete/task-only patches and a concise commit recommendation.

Do not silently modify foundational publication/permission policy, accepted scientific conclusions or historical reports. Any ordinary documentation additions should have working portable tracked links. Preserve the approved B4-F1 evidence package hashes and source identity throughout.

## Compact frozen completion contract — AC1–AC8

**Task type:** tooling housekeeping / evidence classification / read-only deletion planning with limited current-script maintenance.

**Mandatory acceptance:**

1. **AC1 — Scope and protection:** Complete current-policy/permission review, inventory start state and preserve all protected originals, four designated roots, evidence assets, HEAD and index.
2. **AC2 — Meaningful storage accounting:** Refresh actual `.local-work` measurements; explain major byte contributors, substantial retained portions and realistic ranked reclaimable opportunities without an invented deletion quota.
3. **AC3 — Retention/recoverability:** Verify individual/subtree classification; protect unique, practically costly and follow-up-useful evidence; handle `savegames` conservatively; distinguish duplicates from unique historical versions.
4. **AC4 — Reference closure:** Audit tracked and relevant ignored references; identify and block candidates that would cause dangling links, orphan evidence or invalid reproduction until a documented disposition is approved.
5. **AC5 — Scratch lifecycles:** Account for RR1 external Temp/`D:\tools` and current packagers; repair or retire eligible active creators; qualify normal and failure cleanup with safe synthetic tests or document evidenced authority blockers.
6. **AC6 — Exact B5-B proposal:** Machine-readable path/identity/bytes/reference/duplicate/retention manifest, reparse protections, guards and new approval gate; zero unauthorized deletion.
7. **AC7 — Durable reporting:** Answer-first documented rationale and relevant source/provenance links, preserve failures and limitations, no scientific or historical rewrites, no unsupported savings or safety assertions.
8. **AC8 — Independent review/delivery:** Independent reviewer against original AC1–AC8 and actual inputs, correct in-scope defects under same task, final ACCEPT or evidenced escalation; PASS/FAIL/NOT TESTED matrix; exact verified complete/task-only patches, protection/status receipts and no staging/commit/push.

**Optional:** Extra synthetic regression cases, improved future housekeeping ergonomics or more refined space accounting beyond material contributors, if bounded and safe.

**Negative closure:** A small deletion proposal is acceptable **only with demonstrated accounting** that explains large retained material and why reclamation would endanger unique evidence or future research. A scan that simply fails to find references is not sufficient evidence of disposability.

**Continuation authority:** Diagnose, repair, recheck and resubmit in-scope failures without requesting another brief. Review does not authorize deletion. Freeze the criteria; material changes require maintainer approval and recorded amendment.

**Exit/escalation:** Stop affected operations on missing permission, unexpectedly changing protected bytes/paths, unsafe reparse points, failed disk guards, inaccessible indispensable data or evidence of unintended mutation. Preserve logs/checkpoints; describe the exact blocked step. Do not silently reduce safeguards or invent an arbitrary duration/volume cutoff for a healthy run.

**Review outcome dimensions:** Scientific evidence/reproducibility effects; script repair/test qualification; protected state; authority compliance; independent verdict. Maintain the B0/B3/B4 publication distinctions. **Publication remains NOT CLEARED.**
