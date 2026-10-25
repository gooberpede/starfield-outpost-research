# Codex implementation brief — SOR Consolidated Evidence Archival, Stage B Pilot

**Status:** Issued for implementation and qualification; **real loose-file deletion is NOT AUTHORIZED by this brief**.

**Research system:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research`)

**Pilot scope:** Cargo Transport and Fuel, the Stage A candidate of approximately 1,054 eligible non-save files / 34.6 MB uncompressed (figures to verify against actual inventories before acting).

## Objective and frozen contract

Implement and qualify a crash-recoverable, research-system–level archival and restoration workflow, then produce an exact, independently reviewed pilot deletion proposal. The intended Stage B end state is one verified local archive replacing the approved loose non-save members, with actual measured disk/file recovery. **This assignment ends at a decision gate before real deletion**; the implementer may not call the work a completed storage-recovery migration until a separately authorized cleanup has actually occurred. No invented recovery figures.

The owner has accepted the *residual risk* of a single verified local archive potentially being the only retained copy of eligible non-save evidence. This is not permission to erase originals before archive verification, compatibility assessment, independent review, and approval of the exact deletion allowlist. Saves, protected backups, raw save streams, installed game material, native analysis projects and unresolved live working data are excluded from this pilot.

### Governing requirements

Read and obey `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/templates/completion-contract.md`, `docs/reviewers/research-completion-reviewer.md`, and the completed Stage A report and review at `docs/experiments/evidence-archive-discovery/`. Preserve the earlier failed preservation-optimization AC4 disposition; do not reclassify it. Stage A's proposed nine system archives are provisionally accepted, with a bounded inspection of whether `workshop-inventory` merits a separate archive under the overall **30-archive hard ceiling**. Do not create an archive per experiment/brief or many sidecar manifests. Maintain one authenticated central index; member inventories may live inside the archive. Track one owner archive per item and explicit cross-system references.

## Authority and storage policy

**Authorized now:** read-only inventory and provenance work; source hashing; design and code changes to archival tooling; disposable synthetic fault-injection; bounded creation/verification of the *actual pilot archive* without deleting or changing any original loose source; disposable full restoration; independently reviewed deletion manifest and approval-ready continuation/run card. No Starfield launch or debugger attachment, no game installation/save/config modifications, no staging/commit/push, no publication/upload to Google Drive.

**NOT authorized now:** deletion, moving/renaming, truncation, compression-in-place, repacking or modification of any actual pre-existing research file; bulk migrations or unreviewed archive cutovers. The final real deletion needs a separate explicit maintainer approval referring to the final exact manifest hash. If only a separate dry-run can safely be completed, make that boundary explicit.

Free-space context reported by owner: approximately 90 GB on D: and 85 GB on C:, unverified and subject to change. C: is a 500 GB OS SSD under installation/OS pressure. **Prefer D: for the small pilot. Use C: only as bounded temporary staging when required**, never as the default archive home or backup. Independently check caller-available capacity on both drives immediately before each disk-intensive operation and preserve the existing **40,000,000,000-byte minimum free-space guard on C: and D:**. Estimate worst-case concurrent source/archive/staging/restoration/temp usage and abort safely if the guard could be crossed. Identify and remove only *task-created, verified temporary artifacts* during cleanup; never treat older scratch as automatically disposable. Record actual drive free space before and after each step. No migration plan may rely on consuming C:'s headroom long-term. No Google Drive upload in this brief; 10 GB is only a prospective complete-corpus backup planning target. Report total-corpus archive sizing uncertainty until measured. Do not require an external copy for this bounded single-local-copy pilot, but state the remaining drive-failure/corruption risk unambiguously.

## Workstream A — Freeze an exact pilot inventory

1. Reconcile Stage A `Cargo Transport and Fuel` proposed inventory with the actual working tree, historical pins and exact member origins. Produce immutable membership snapshot listing source relative path, size, expected and newly verified SHA-256, provenance, owner research system, and retention/active-consumer status. No silent scope expansion to non-cargo evidence.
2. Resolve the **three version-sensitive packager paths** identified by Stage A: identify the exact authoritative versions and referencing consumers, or mark them ineligible for deletion and retain loose. Do not arbitrarily select the newest or overwrite history.
3. Review active absolute-path references and consumers; classify direct archive access, controlled temporary extraction, code adjustment, or retained-loose exception. Verify that old research remains discoverable and reproducible. Keep archival metadata navigable from durable docs without publishing local-only raw evidence.
4. Perform the bounded `workshop-inventory` grouping assessment for later archives, documenting recommendation and rationale, without migrating or reclassifying that data in this pilot.

## Workstream B — Implement transactional archive mechanics

Use the Stage A prototype as a starting point, not as proof of crash-durability. Prefer a single `Cargo Transport and Fuel` research-system archive, e.g. `.tar.zst`, under a stable archives directory. Exact paths/names are subject to the project's existing rules. Central authenticated index records archive identity, logical owner, archive SHA-256, member manifest digest, original-path mappings, status, exclusions and recovery instructions. Do not duplicate members into multiple system archives; support explicit index references for overlaps.

Implement or demonstrate:

- Deterministic safe packaging, full source-hash match, path canonicalization, exclusion of reparse/path-traversal/alternate-stream hazards, handling or explicit exclusion of hardlinks; no import of arbitrary executable metadata on restore.
- Durable temporary build, flushed writes, archive verification, final atomic publication where supported, and recoverable journal/checkpoint distinguishing PREPARED, VERIFIED, RESTORED-TESTED, AWAITING-APPROVAL, RETIRING and COMPLETED states. A crash must never convert an incomplete archive into an authoritative copy.
- Complete member verification against historical expected hashes, independent scratch extraction and restored-content hash equality, plus index/archive identity verification against an independently stored expected digest.
- Fail-closed missing/corrupt archive, index tampering, nonmatching source, changed source since freeze, insufficient disk, interrupted archive creation/cleanup, path alias, and resume/retry handling. No unattended deletion.
- Exact allowlist executor **implemented but not exercised on real originals**, requiring explicit approved manifest identity, rechecking each source's expected hash and archive/index integrity immediately before any removal, and stopping safely upon mismatch. A system must not claim logical migration complete until deletion and postflight succeed. Provide a deterministic dry-run and a rollback/recovery plan. Avoid promising full transactional atomicity across thousands of filesystem deletions; document partial-completion recovery.
- Separate reporting of archive-format authenticity, local single-copy residual risks, and incident/periodic audit provisions. Do not silently replace per-task scientific-input verification with unverified journal assumptions.

## Workstream C — Test and measure

Use disposable Windows/local fixtures to exercise restore equivalence, original-file deletion simulation, partial deletions, crash recovery, invalid indexes/manifests, malicious paths, altered bytes without recorded journal changes, missing inputs, incorrect version selection, pointer/alias and hardlink cases, disk-guard failure, and rollback. Never inject faults into authentic protected inputs.

Where safe under the live drive guards, construct and verify the **real pilot archive without source deletion** and perform a complete disposable restoration. Report exact file count, original logical/allocated bytes, compressed archive and index bytes, total temporary peak allocation, SHA-256, creation/verification/restore wall-clock timings, and projected versus **actual** freed space (zero or negative until approved cleanup). Distinguish synthetic proof from real-file success.

For broader planning, report nine-archive grouping and potential identity/lifecycle split, projected system totals, empirical pilot compression, estimated complete versus essential archive totals with uncertainty, 10 GB off-device-backup feasibility and archive count ≤30. No invented extrapolated savings. Retain the ≥80% routine historical-verification reduction as a **future migration acceptance objective**, not a false Stage B pilot achievement; measure comparable per-task reads, hashes, enumerations, bytes and time where possible.

## Stage B deletion decision package (mandatory)

Return a concise approval-ready plan containing:

- Exact pilot archive and index locations; archive SHA-256, member inventory hash, version-sensitive exclusions and independent restoration proof.
- A stable manifest of **every exact source path eligible for deletion**, its preexisting SHA-256, count and expected recoverable allocated bytes; separate retain-loose list, including all protected saves and dependencies.
- Proof active consumers work through the archive or are explicitly blocked from deletion, plus local C:/D: capacity and 40 GB guard checks.
- Explicit residual one-copy risk, abort/partial-retirement/rollback instructions, and the command/operation proposed **only after** the maintainer authorizes this manifest.
- Subsequent systems' migration order selected by storage relief, cross-system dependencies and risk; no advance permission for their deletion.

## Frozen acceptance criteria (AC1–AC8)

| ID | Mandatory acceptance standard |
|---|---|
| **AC1 — Authority and preservation** | No preexisting actual evidence changes/deletions, no game/target actions, no Git integration; saved material excluded and critical guards honored. |
| **AC2 — Research-system boundaries** | Nine-group proposal accounted for, bounded workshop-inventory split decision, ≤30 archives, single owner per original, no experiment-per-archive sprawl. |
| **AC3 — Archive authenticity** | Actual eligible pilot members and expected historical hashes reconciled; archive/central-index fully authenticated; three version-sensitive paths resolved or explicitly retained. |
| **AC4 — Independent recoverability** | Verified full disposable restore of real pilot archive, exact byte/hash equality, controlled extraction and compatibility with dependent research. |
| **AC5 — Engineering safety** | Crash/partial/restart, malicious/corrupt input, path/alias, changed byte, disk guard, index tamper and fail-closed conditions exercised; deletion executor remains unexercised on real evidence. |
| **AC6 — Cleanup readiness (NOT cleanup completion)** | Exact independently reviewed allowlist + hashes + pre-delete guards + rollback/continuation card, with clear separate permission gate; prospective recovery quantified, actual recovery not overstated. |
| **AC7 — Measurement and durable records** | Actual compression/temp/free-space/verification measurements; central manifest and report; failures retained; full editorial manual pass; source/provenance and local-only boundaries explicit. |
| **AC8 — Independent acceptance and delivery** | Separate scientific/engineering/security/editorial reviewer ACCEPT on final substantive snapshot and closure delta; verifiable complete/task-only patches, status/exclusions/hashes. |

Do **not** redefine AC6 as requiring real deletion within this unapproved assignment. The *overall* Stage B storage-recovery objective remains unfinished until a later approved cleanup actually frees space. If an essential prerequisite fails, continue in-scope repair or report precise REWORK/ESCALATE; do not call a non-destructive prototype a completed migration.

## Workflow and final return

Freeze baseline HEAD/index/status, brief preexisting-change status, member admission rules and criteria before work. Maintain actual log timestamps and measured costs. Implementer owns failed-test remediation and relevant retests. Independent reviewer must inspect the original contract, primary receipts, restored files/hashes, real tree and actual patches; acceptance cannot be self-issued. Follow `docs/RESEARCH_EXECUTION_PROTOCOL.md` and `WORKFLOW.md` for manual editorial pass, verified complete/task-only diff including new untracked authored files, source-code/historical evidence exclusions and separate final delta review if needed. Do not stage/commit/push or delete real source evidence.

Final response must state AC1–AC8 PASS/FAIL/NOT TESTED, actual vs projected storage recovery, exact archive/member/hash and deletion manifest identifiers, the independently reviewed disposition, and the one explicit user decision needed to authorize retirement of the verified pilot loose files. If real-archive construction would jeopardize the disk guard or retention safety, stop that operation and return the evidenced block rather than expanding to C: without bounded capacity proof.
