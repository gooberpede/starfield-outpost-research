# Codex implementation brief — Cargo Evidence Retirement and Archive-Baseline Activation

**Project:** `D:\Projects\starfield-outpost-research\` (`gooberpede/starfield-outpost-research`)  
**Assignment:** SOR — Cargo Evidence Retirement and Archive-Baseline Activation  
**Type:** Bounded engineering implementation and non-destructive qualification, followed by an approval-ready execution card  
**Authority now:** Offline code/documentation changes, inspection of local archives and historical evidence, and disposable synthetic tests only. **No deletion of real historical evidence and no activation of the real preservation baseline.**  
**Integration authority:** Maintainer retains staging, commit, push, policy, live-session and destructive-operation decisions.

## Background and fixed facts

The accepted Cargo archive and cutover investigations establish authenticated locate/verify/restore, two historical consumer reproductions, and a proposed retirement of **all 1,051 archived loose Cargo originals**. Three version-sensitive packager files remain outside the archive and must not be touched. The earlier 37-file deletion proposal is superseded. The latest accepted consumer-cutover work remains the baseline; do not re-open its scientific results or broaden to other research systems.

Verify the following against the **actual** local artifacts, established repo records, and approved provenance; strings below are expected identities, **not** an instruction to trust them without checking:

| Artifact | Expected SHA-256 |
|---|---|
| Cargo compressed archive | `ebda740f0092b93f1dc9f32120db365223f465a6d374ce8e98933e8041eb1da7` |
| Embedded archived-member inventory | `f46605615abca2ff026f46aad6f51162a554c4383e89b79048899e4fb6e39a7a` |
| Current proposed 1,051-file retirement allowlist | `b809a65f25560bec838873bfbb50c1e945a478a627129c24f837ec437b88e75d` |

The current projected recovery from the consumer-cutover report is **13,594,624 bytes net**, counting persistent costs, not observed recovery. It must be recalculated for the final execution card. Earlier Cargo research has **no members in the historical 93,334-pin D5G inventory**; this pilot demonstrates a cutover architecture, not a reduction of that particular historical count. The broader eventual goal remains at least 80% less routine historical-verification work following migration of relevant systems.

Read and obey `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/templates/completion-contract.md`, `docs/reviewers/research-completion-reviewer.md`, and the Stage A, Stage B and Cargo consumer-cutover reports, contracts, primary artifacts and review records. Pin repository HEAD/index and current source/tool versions at start. Resolve actual filenames and APIs from the repository; do not invent local paths or reinterpret prior acceptance.

## Governing objective

Implement and independently qualify the **smallest production-capable, crash-recoverable exact-allowlist retirement executor** and **archive-backed preservation-baseline activation** for Cargo. Prove them on isolated disposable replicas with archived originals absent. Deliver a precise, independently reviewed **real-execution authorization card**; **do not execute it**. Once a future maintainer-approved retirement runs, it must be possible to say that the archive has replaced the loose originals in routine checks, not merely created a second copy.

## Scope and implementation requirements

### A. Resolve identities and authority before implementing

1. Read the current authoritative archive index, embedded member inventory, archive bytes, 1,051-file allowlist, existing resolver, shadow baseline, preparer and retention/hold records. Verify consistency between all identities and the actual file population. Preserve the 3 excluded version-sensitive packager paths.
2. Bind the retirement executor to a **separate, explicit maintainer authorization** naming the exact allowlist hash, archive/index identities, source population, operation and applicable conditions. An approval of this *implementation brief* is **not** such authorization. A dry run or a prior reviewer ACCEPT must never activate destructive mode.
3. Reject changed sources, missing or altered approved manifests, unsupported files, non-Cargo paths, symlinks/reparse escapes, hardlink alias risks, ambiguous sources, archive members outside scope, and unexpected directory contents. Resolve path normalization and Windows identity checks using the existing repository policy; fail closed on ambiguous conditions.

### B. Implement minimal production retirement and recoverability

4. Reuse existing archiver/resolver/retirement-preparer components rather than replacing them. Add only the required deletion execution, verified transaction journal, resumable validation and preservation-baseline handover.
5. Design explicit durable states, e.g. **PREPARED → RETIRING → RETIRED_PENDING_BASELINE → COMMITTED** with **RECOVERY_REQUIRED** for ambiguous failure. Define precise transitions, flushed journal records, idempotent restart and what can or cannot be rolled back after original removal. Neither a partially retired population nor a failed baseline write may be reported as committed.
6. Before each destructive act, revalidate the approved exact path, identity/content hash, archive authenticity, applicable manager/index/allowlist provenance, and operation safety conditions. Delete **only** the exact approved file, never an ancestor directory or wildcard. Avoid cross-drive atomicity assumptions. Validate stale handles, concurrent edits, interruption between validation and deletion, and Windows deletion semantics. Any unqualified race must fail closed; do not silently skip members and declare completion.
7. Build/verify the archive-backed baseline in a crash-recoverable way, with externally established archive/index hashes and exact loose holds. The new routine protection check authenticates archive-level objects without rehashing every member on unrelated offline tasks; the embedded member hashes remain available for targeted restoration and integrity verification. Its real activation occurs **only after** approved retirement and verified transaction completion.
8. Plan for partial failure when only one authoritative local archive remains. Report irrecoverable archive-loss risk explicitly; never promise that a local-only copy protects against drive failure. Do not require unavailable Google Drive or an independent physical backup for this bounded pilot, but do not create or claim one. Keep the three held `package.py` variants outside the deletion allowlist.
9. Retain the existing **40,000,000,000-byte free-space guard on both C: and D:** at applicable sensitive stages. Measure actual free space, journal/workspace needs and real archive/index placement; C: may be used only for bounded temporary work if necessary, never as an unapproved enduring authority or escape from the guard.

### C. Qualification — strictly disposable

10. Use isolated synthetic filesystems/test directories and disposable archival replicas. No test may mutate the 1,051 real Cargo loose originals, the archive, protected saves, original backups, installed EXE/ESMs, analysis projects or past evidence. Qualified reads and identity checks on real originals are permitted.
11. Exercise at least: exact normal retirement; source corruption; archive/index/member-inventory/allowlist tampering; wrong source version; extra/missing source; protected-path or reparse/hardlink escape; concurrent mutation; IO and permission failures; disk guard failure; interrupted journal writes; stop after some deletions; restart/replay; interrupted baseline publication; double activation; bogus external authorization; stale approvals; and attempted cleanup with unknown file types.
12. On disposable copies **after loose-file removal**, reproduce the two formerly qualified Cargo consumer workflows (C1 SWF and C2 PEX) through authenticated restore. Compare complete outputs to frozen baselines and verify integrity and cleanup of temporary restoration leases. Also test verification baseline before, mid-transaction and after commit; it must reject ambiguous/partial states rather than misclassify missing originals as benign.
13. Include a genuine fault/negative case for which restoration or safe commitment is impossible, with a correct blocked/recovery disposition. Don't turn every interrupted run into a purported success. Report full test matrices, evidence and independent reruns/inspection. Keep tests proportionate: no entire 90K-pin rehash unless an evidenced new exposure justifies it.

### D. Reviewed execution card — not executable under current authority

14. Produce a concise maintainer-facing card specifying: exact archive and index paths and hashes; embedded inventory identity; final 1,051-member allowlist hash; three excluded holds; before/after baseline identity; preflight free space; approved action and command (inert until separately authorized); target byte/file count; projected net change including all retained artifacts; independent reviewed rollback/recovery procedure; STOP conditions; expected postflight evidence; and the **specific text of the future approval request**.
15. If the real population or hash changes during this assignment, do not auto-regenerate a different deletion set and call it approved. Explain the discrepancy and prepare a re-reviewed proposal. Neither a convenient shortcut nor a cosmetic 37-file retirement fulfills the purpose.
16. Provide a post-authorization operator sequence as a future plan only: re-pin → confirm approval → preflight → archive authentication → journaled exact deletions → baseline commit → archive/member restoration smoke checks → loose holds and protected-file checks → actual net recovery measurement → durable closure. Do not stage/commit/push or perform the sequence now.

## Frozen acceptance criteria — AC1–AC8

| ID | Mandatory criterion | Required evidence |
|---|---|---|
| **AC1** | Authority and source protection: no real deletion, baseline activation, retail attachment, or unapproved Git writes; protected source identities unchanged. | Before/after HEAD/index/status and scoped protected checks; explicit operation log. |
| **AC2** | Exact identities: source population, archive/index/embedded inventory and 1,051-file allowlist independently authenticated; 3 holds excluded; fail closed on discrepancies. | Identity ledger, hashes and reconciled counts. |
| **AC3** | Production-capable bounded executor: exact-file retirement, durable state machine, idempotent recovery, safe authorization enforcement and non-ambiguous baseline handover. | Source review, state-transition specification and executable disposable demonstration. |
| **AC4** | Safety qualification: destructive and adversarial simulations detect/stop corruption, out-of-scope deletion, stale authorization, races, interruptions and storage failures. | Complete reproducible positive/negative case matrix and receipts. |
| **AC5** | Reproducibility: with all 1,051 originals absent from a disposable replica, archive-backed locate/verify/restore and both historical Cargo workflows still yield qualified frozen results. | Output-equality checks, member authenticity and lease-cleanup records. |
| **AC6** | Correct future verification baseline: archive-level routine validation replaces all 1,051 retired Cargo members; partial-state cases block; actual operations remain unperformed; realistic net-positive cleanup model. | Before/mid/after shadow checks and independently reviewed storage calculations. |
| **AC7** | Durable editorial completion and precise execution card: all added prose and code documentation fully read/screened; unresolved risks and true limits preserved; card sufficient for a separate GO decision. | Full changed-file inventory, source/tool pins, original/failed test histories, editorial screen and card. |
| **AC8** | Independent scientific, engineering, security and editorial review of the substantive **exact snapshot**, with reviewed final delta, verified complete/task-only diffs/manifests and no unstated exclusions. | Independent ACCEPT or explicit REWORK/ESCALATE, exact reviewer receipts and hashes. |

Acceptance is **all mandatory criteria PASS**. Do not change the criterion definition to fit results. A failed test means investigate, fix and rerun within authorized scope; do not ask for another brief merely because an implementation test failed. A genuine safety/authority blocker requires bounded ESCALATE, not an invented PASS. If one of the expected existing hashes proves obsolete or access unavailable, preserve evidence, diagnose and report exact missing authority/input without destructive fallback.

## Deliverables

- Reusable implementation and focused synthetic tests under suitable existing `research/` paths.
- Updated Cargo cutover report, provenance and a new concise retirement-executor qualification report, containing frozen AC matrix and limitations.
- Precise **NOT AUTHORIZED** execution card and approved-scope request text; no real deletion or baseline switch.
- Baseline and retirement state schema, fault matrix, exact member/source identity ledger and postflight checklist.
- Full evidence/provenance hashes, editorial completion record, independently reviewed substantive snapshot and any narrow final-delta acceptance.
- Complete and task-only Git diffs containing all tracked and untracked text, along with file/status manifests, exact SHA-256 and forward/reverse application verification. Preserve clear exclusion reports for ignored raw evidence, save files, archives, scratch and databases. Do not stage, commit, push or publish.
- Report prospective measured-versus-projected disk and pin-check reductions separately; actual recovered bytes must remain **zero from this assignment**, unless unrelated activity is explicitly identified and segregated.

## Explicit non-goals and future decision boundary

No archive-system expansion, no reclassification of original science, no new archive construction beyond disposable tests, no deletion of real Cargo originals, no activation of modified project-wide preservation policy, no cleanup of historical review receipts, no saves or game changes, no cloud upload, no publication/B6 work and no RG2-D5H work.

**After independent ACCEPT:** Return the complete real-execution authorization card for maintainer review. The maintainer may then approve the *exact bounded deletion and baseline transaction* separately. Approval of this brief or acceptance of the diff is **not** an execution GO.
