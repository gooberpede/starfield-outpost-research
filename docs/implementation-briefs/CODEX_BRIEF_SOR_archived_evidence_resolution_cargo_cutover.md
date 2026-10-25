# Codex implementation brief — SOR: Archived Evidence Resolution, Verification Cutover and Cargo Retirement Preparation

**Authority:** Maintainer-approved scope, 26 October 2026 (Australia/Sydney). **Execution:** offline implementation and non-destructive qualification only. **Live Starfield operations:** prohibited. **Real evidence deletion:** NOT AUTHORIZED. **Integration:** no staging, commit, push, publication or automatic activation of project-wide policy changes.

## 1. Background and binding intent

The `starfield-outpost-research` project (`D:\Projects\starfield-outpost-research\`) holds large quantities of local-only historical evidence. Earlier audits reported roughly 93,334 routine historical input pins and Stage A found about 245,000 paths / 45 GiB under `.local-work/`. Repeatedly hashing loose historical evidence is the **primary problem**. Avoiding duplicate archive-plus-loose storage, protecting the 40 GB available-space floor on **both C: and D:**, and reclaiming disk space are essential accompanying goals.

Stage A proposed a small number of research-system archives (nine provisionally, no more than thirty), rather than one archive per experiment. Stage B constructed and verified a real **Cargo Transport and Fuel** archive comprising **1,051 members** (~34.58 MB source payload, ~4.66 MB compressed). Three version-sensitive packager files remained excluded. The technically accepted Stage B proposed retiring only **37 members** (~0.75 MB), while retaining **1,017** loose archived files because of broad historical path dependencies; with archive and index overhead, that proposal has **negative net storage recovery** (~−4.83 MB). **That deletion proposal is not approved and must not be executed.** Existing archive/member/index hashes, source pins and detailed caveats are authoritative in `docs/experiments/evidence-archive-stage-b/{report.md,continuation.md}` and local delivery receipts; do not substitute the approximate values above for actual pinned identities.

The objective of this continuation is to **make historical evidence accessible from its authenticated archive, cut over routine verification from individual retired members to the archive object, and produce a significantly larger, exact, independently reviewed retirement proposal**. The goal is not a generic virtual filesystem or another archive-only prototype. Preservation of source content, provenance and reproducibility remains mandatory.

Read the current `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md`, `docs/reviewers/research-completion-reviewer.md`, Stage A and Stage B documents/code, and relevant permissions/provenance policies before implementation. Treat their stricter protections as binding except for **proposed** policy changes explicitly left inactive here. Independently pin the actual current Git HEAD, branch, index, active archive identities and scientific inputs; do not assume earlier HEAD or receipts still describe the current tree.

## 2. Frozen completion contract

**Task type:** Engineering implementation and evidence-method qualification, with an auditable scientific/provenance assessment of historical dependencies.

**Mandatory deliverable:** A minimal, tested archive-backed evidence locator/verifier/restorer; a defensible Cargo consumer cutover; an independently checked replacement routine-verification model; and a signed-off *proposal*, not execution, for retiring at least 95% of the 1,051 archived loose member files with net-positive projected persistent storage recovery.

**Scope:** Cargo Transport and Fuel pilot and a reusable narrow interface applicable to later research systems. Historical working directories and active consumers are in scope for *inspection and scoped adaptation*, not wholesale refactoring. A short scale assessment for larger proposed groups is permitted. Avoid revisiting full archive taxonomy, save serialization, the Starfield runtime or D5H. Keep the previously failed preservation-optimization AC4 result intact.

**Continuation:** Diagnose and fix in-scope implementation/test failures, retain failed trials, and rerun qualification; do not stop at the first obstacle or relax the numerical goal. If a material safety or scientific blocker cannot be resolved under offline authority, report the exact blocker and return REWORK/ESCALATE, never an invented PASS.

**Exit:** All AC1–AC8 pass and exact reviewed artifacts are delivered, **or** an independently assessed failure/escalation with preserved reproducible evidence. A small retirement proposal does not satisfy AC6.

## 3. Investigation and implementation work

### A. Resolve the 1,017-file dependency objection at file and consumer level

Inventory each of the 1,051 archived members and account for the 1,017 previously retained files, 37 previously proposed retirements and three excluded packager files; eliminate double counts and show exact statuses. Classify apparent dependencies by **actual role**: active maintained utility requiring direct paths; reproducible closed experiment; historical report/log referencing a former path; genuine fixed-path consumer; ambiguous/unresolved; or actively written/current data. For active consumers, locate the specific read paths and qualify actual use, not mere grep frequency. Explain why each remaining loose retention is unavoidable, if any. Historical links and citations remain preserved as provenance; they do not by themselves require permanent loose copies. Do not delete or rewrite originals to make dependency scans pass.

### B. Implement a deliberately minimal archive-access layer

Provide a documented CLI and small Python entrypoint, reusing or extending the Stage A/B archive format and authoritative index, with three operations:

1. **Locate:** Original path → current loose source or archive ID/member, with explicit ambiguity and missing-member errors. Original relative-path identity and archive ownership must remain exact; no guessed fallback paths.
2. **Verify:** Authenticate archive bytes against an **externally expected/pinned** SHA-256 and authenticate embedded member inventory. Reject index substitutions, wrong archive version, duplicate/colliding member paths, unexpected symlinks/reparse paths and malicious traversal. Never treat untrusted manifest data as independent authority for its own hash.
3. **Restore:** Select a member, member set or complete experiment into a controlled disposable directory preserving original relative paths. Validate selected member bytes against their original pinned hashes, refuse unsafe paths and overwrites, record identities, and provide explicit lease/cleanup semantics. Fail closed on incomplete verification. A restored working copy must not automatically become a new permanent historical pin.

Do not build a filesystem driver, transparent on-demand file provider or general virtualization framework. Closed historical scripts may be run after deliberate restoration rather than mass-rewritten. Where truly active tools require direct files, adapt only the smallest supported points to call the resolver or a restoration entrypoint. Verify consumers with meaningful operation-specific tests, not just syntax and string replacement.

### C. Archive-level verification and baseline cutover

Define and implement a **versioned, explicit migration of the routine preservation baseline** for the retired Cargo members. Historical member SHA-256s remain available in the authenticated archive inventory; routinely unrelated offline assignments check the approved archive object/central index once per required verification boundary, **not each of its 1,051 retired members**. When research actually consumes a member, authenticate the archive and verify restored/used member content against its pinned hash. Preserve stronger original-save, backup, installed-content and relevant high-risk live-run checks. Never claim that hashing only an archive prevents undetected later disk corruption of unrelated archives; distinguish routine verification, scientific-input verification, and periodic/incident deep validation. New policy is a **proposal** unless the maintainer separately approves activation; implement demonstrable dry-run / shadow mode without mutating the current mandatory baseline.

Prevent double counting (archive + its constituent historical loose files) and silent omission during baseline replacement. Demonstrate pre/post row/object accounting and precise archive identity. Include detection of missing, swapped, corrupt, truncated archive, wrong baseline, altered index, orphaned member, changed loose source and invalid journal/recovery states. Preserve the previous full baseline and provide deterministic rollback to it if cutover has not yet retired originals. Explain post-retirement restoration and audit procedures without pretending deleted loose files are independently available.

### D. Safe retirement preparation, not execution

Generate a deterministic allowlist for **at least 999 of 1,051 archived member originals** (≥95%; rounding up), with exact original normalized path, pre-retirement SHA-256, size, owning archive/member/index IDs, present file identity where necessary, dependency disposition, and an explicit exclusion/hold register. The three separately excluded packager files must remain outside the retirement scope. Do not add unrelated evidence, saves, active scratch or working trees to increase a percentage.

Independent review must verify the exact deletion allowlist against physical sources, authenticated archival membership, and the proposed consumer cutover. The Stage B deletion manifest for 37 files is **not** standing authority; issue a new reviewed manifest with its own hash and immutable reviewed snapshot. An eventual retirement executor must refuse changed allowlists, changed source bytes, unverified archives, missing recovery receipts, unsafe source paths, unexpected hardlinks/reparse targets, unsupported filesystem states and unqualified free-space measurements. It must record each deletion durably with restart/resume/reconciliation semantics, but **must not remove any actual evidence in this assignment**.

Prove **net-positive projected physical storage recovery**, not only logical bytes and not a gross deletion figure. Include the archive, central index, persistent verification metadata, journal/control files and any lasting replica; separate temporary scratch and repeated audit costs. Report expected before/after loose historical object count, routine historical check count, file reads, bytes hashed, elapsed time and disk allocation. Avoid extrapolating from synthetic benchmarks as though they were actual production recovery.

### E. Qualification and storage safeguards

Execute synthetic adversarial fault-injection solely in disposable directories: modification, deletion, substitution, corrupted archive, alternate manifest, interrupted archive/restore/retirement preparation, stale source, source path collision, hardlink/reparse edge, journal ambiguity, insufficient free space and power-loss-like restart. Demonstrate archive restoration and representative former Cargo consumers; include at least one full historical workflow where viable. Preserve exact expected/observed outcomes and counterexamples.

Check both C: and D: free space and maintain the project's 40,000,000,000-byte available-space floor; C: is eligible only for temporary scratch if necessary and safe. D: is authoritative archive storage. No Google Drive upload. Do not create a second permanent full replica by default. No saves, installed game content, protected original archives, or game process may be modified. Storage measurements and actual live state may differ from historical reports—measure current reality.

A credible scale note should explain how Cargo's resolver/baseline strategy applies to the roughly 243K eligible historical members and potential ~9 research-system archives without per-experiment archives, per-experiment sidecar clutter or mass script rewrites; it is not authorization for another archive migration.

## 4. Frozen acceptance criteria (AC1–AC8)

**AC1 — Authority, integrity and protection (mandatory).** Pinned baseline, branch, index, protected files and current Cargo archive/index verified; no retail process, save/game/installed-content edits, original evidence deletion, staging, commit, push, publication or policy activation. Actual scope and exclusions recorded.

**AC2 — Fine-grained dependency accounting (mandatory).** All 1,051 archive members, earlier 1,017 retained/37 proposed, and three nonarchived packager holds reconciled. Active consumers distinguished from historical references. Every remaining proposed loose hold has a specific justified dependency; no blanket directory retention.

**AC3 — Minimal authenticated evidence access (mandatory).** Locate/verify/restore interface implemented, versioned and tested, with original-path continuity, pinned hash authority, safe extraction and controlled ephemeral cleanup. No unnecessary general filesystem abstraction.

**AC4 — Consumer reproducibility (mandatory).** Representative closed workflows and all genuinely active Cargo consumers used to justify deletion cutover work after archive restoration or scoped code adaptation. Failure and dependency gaps must be disclosed; syntax-only qualification does not pass.

**AC5 — Routine preservation baseline replacement (mandatory).** Versioned shadow-mode cutover proves the new archive-level baseline eliminates **100% of routine per-member verification for retired Cargo files in unrelated offline research**, without discarding individual member hashes or weakening task-specific scientific-input checks. Demonstrate no double counting/omission, robust detection of corrupted archives/indices, and rollback. Activation reserved for separate approval. Wider programme objective ≥80% reduction in routine historical verification remains future migration goal, not a claim achieved by Cargo alone.

**AC6 — Material, safe retirement proposal (mandatory).** New exact independently reviewed allowlist covers **≥999 of 1,051 Cargo archive members**, excludes unarchived protected/held files, is reproducible and safety-gated, and projects **net-positive** recovery after permanent archive/index/control costs. If impossible safely, **AC6 FAIL/REWORK or narrow ESCALATE**; no target reduction or silent redefinition. Actual deletion prohibited.

**AC7 — Durability and editorial completion (mandatory).** Source/receipt IDs, measured workload, synthetic tests, reproducible commands, negative results, dependency matrix, revised policy proposal, recovery/rollback run card, exact manifest, reviewer-ready documentation and full editorial screening/manual reading under `docs/EDITORIAL_STANDARD.md`.

**AC8 — Independent scientific, engineering, security and editorial review (mandatory).** Independent reviewer examines original contract, actual code and primary proof, fault injections, active-consumer tests, baseline cutover, cost arithmetic and deletion allowlist; issues per-AC PASS/FAIL/NOT TESTED with evidence and ACCEPT/REWORK/ESCALATE. Include separately independently reviewed substantive and final closure delta where applicable. Verified complete and task-only diffs, hashes, status, manifests and exclusions, including all untracked authored files.

No averaging across ACs: seven passes and an AC6 failure is REWORK, not successful completion. Reviewer acceptance is not maintainer authorization to delete, activate policy or publish.

## 5. Required deliverables and return format

Place concise durable reports and tests under an appropriately named `docs/experiments/` area, with implementation under a coherent project-owned research/utility area; update documentation navigation and provenance precisely, without overwriting historical reports. Deliver:

- Executive report: current Cargo archive/source identity, scientific and operational distinctions, actual dependency census, proposed disposition, projected net space and routine-check savings.
- Full machine-readable per-member dependency/retirement ledger and short human-readable held-file exceptions; keep massive raw data local-only if current publication/evidence rules require.
- Minimal resolver CLI/library, versioned authenticated index/baseline adapter in shadow mode, tests and instructions.
- Representative consumer reproduction receipts, historical input hash evidence, synthetic fault-injection matrix and full recovery/rollback procedure.
- **New exact deletion allowlist and immutable hash**, prepared solely for a separate maintainer decision. Explicitly say `DELETION NOT AUTHORIZED`.
- Proposed future preservation-rule text with no automatic activation; clear retained/retired distinction and periodic full archive audit policy.
- Original frozen AC1–AC8 matrix, failure history and independently signed review/disposition; complete/task-only diff with exact membership, hashes and applicable protected exclusions.

Do **not** suggest a completed-success commit message unless all mandatory criteria pass. Do not ask the maintainer to approve deletion until independent review accepts the exact allowlist and the user can inspect the projected recovery. If results demonstrate safe limitations rather than the required proposal, preserve them and return a precise unfinished/REWORK assessment.

## 6. Explicit decision boundary

**Authorized now:** Offline inspection, implementation, synthetic tests, real-archive read/verify and disposable restoration; production retirement/baseline migration *dry run*; independently reviewed precise deletion proposal.

**Not authorized:** Deleting/renaming/moving real historical originals; activating replacement project-wide verification policy; migrating another research system; changing archive groupings; touching protected saves, raw save streams or game definitions; using C: for permanent archive storage; uploading to Google Drive; Starfield launch/debugger attachment; Git staging/commit/push; B6/publication.

The next maintainer decision is whether to approve the **exact independently reviewed Cargo retirement allowlist and routine-verification cutover**. This assignment must make that decision meaningful and quantify the benefit. Its purpose is to replace repeated pin-by-pin historical checks with a small authenticated archival estate, without sacrificing access to the original evidence or consuming more disk indefinitely.
