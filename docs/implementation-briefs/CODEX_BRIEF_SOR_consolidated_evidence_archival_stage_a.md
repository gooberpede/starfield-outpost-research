# Codex Research Brief — SOR Consolidated Evidence Archival and Storage Recovery, Stage A

**Status:** Proposed implementation/research brief; authorized work is **Stage A only**.  
**Project:** `D:\Projects\starfield-outpost-research\` (`gooberpede/starfield-outpost-research`).  
**Purpose:** Discover the true research-area boundaries and disk costs of the existing `.local-work/` evidence estate, then design and qualify a **non-destructive** consolidated archival system. Do not select final archive boundaries, migrate real evidence, delete originals, activate a new verification policy, or upload to a cloud service in this assignment.

## Background and frozen constraints

The maintainer reports approximately **45 GB and 230,000 files** under `.local-work/`, with approximately **90 GB free on D:**. Prior research reported 93,334 pinned historical entries and repeated large before/after audits. The previous preservation-optimization assignment ended **REWORK (AC4 failed)**. Its conditional NTFS-journal fast path did not provide fresh verification of unread content and must not be presented as equivalent to full content hashing. Preserve that historical verdict; do not amend the old contract or silently reuse its failed solution.

The maintainer's new design decision is **one consolidated evidence archive per outpost research system**, spanning any number of experiments and briefs. Evidence with overlapping relevance is physically stored in **one** archive and referenced from other systems through a central index. **Maximum 30 archives**, preferably substantially fewer; no archives per experiment and no clutter of thousands of sidecar manifests. Do not assume the archive candidates named in previous discussions are definitive: inventory the research areas first so the maintainer can combine or split them.

Off-device backup options are limited. **10 GB compressed total** is a *planning target* for a possible Google Drive backup, not a verified entitlement, hard scientific selection threshold, or permission to upload. Measure whether a defensible essential-evidence set can fit, without deleting unique original observations or relabeling evidence as disposable to achieve the target. No off-device backup is currently confirmed.

The migration must ultimately include deletion of eligible loose copies **after independently approved, verified cutover**, because storage and file counts need to decrease. **Stage A does not authorize such deletion.** The future migration will require a separate reviewed authorization describing the exact batch and paths, recoverability, space guards, and rollback. The current 40,000,000,000-byte free-space guards for both C: and D: remain in force wherever applicable; do not defeat or silently reinterpret them.

## Governing project instructions

Read `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md`, `docs/reviewers/research-completion-reviewer.md`, relevant permissions/publication/provenance policies and the prior preservation-optimization report/review **before** implementing. Follow actual current repository state, not the names or assumed locations in this brief. Keep original scientific controls, installed files, protected saves/backups, analysis databases and historic receipts intact. Do not stage, commit, push, publish, disclose, synchronize to Google Drive, or run/attach to Starfield.

## Frozen research question and completion contract

**Task type:** Offline inventory, design and isolated engineering prototype (not real migration).  
**Research question:** How can we consolidate historical research evidence into a small number of research-system archives, retain trustworthy member-level provenance and restoration, and materially reduce routine verification overhead and `.local-work/` storage/file counts after an approved future migration?  
**Required outcome:** An independently reviewed discovery report, complete research-area and dependency inventory, proposed archive alternatives, measured compression and verification prototypes, quantified cleanup projections, and an approval-ready *non-executed* migration plan.  
**Negative result:** If the essential evidence cannot plausibly fit in 10 GB or important current tools cannot resolve archived inputs, preserve those limitations and propose defensible alternatives. The brief does not require an invented compression ratio or unsafe deletion plan.

### AC1 — Authority, identity and protected baseline

Document branch/HEAD/index/untracked baseline, tool versions and pinned scientific references. Verify relevant inputs against prior expected hashes before analysis. Use read-only inventory paths and isolated disposable output for prototypes; no writes to protected original evidence. Record current disk free space and the free-space guard checks. Do not initiate a full 93,334-entry double-rehash merely as a default task ritual; justify any broad hash audit by specific risks or unresolved identity requirements, and explicitly distinguish metadata inventory from payload read/hash verification. Preserve failed attempts and corrections.

### AC2 — Exhaustive research-area discovery and classification

Produce a **human-reviewable research-area list first**, sorted both thematically and by descending current bytes/file counts. It must cover the entire `.local-work/` namespace without treating every experiment folder as its own research system. Each row should include proposed research system, experiment IDs, directories, evidence roles (unique primary capture, derived/cached, working, diagnostics, critical/protected, unknown), count, logical bytes, relevant allocated-size estimate where available, active/historical status, original pins, ownership uncertainties and candidate disposition. Maintain explicit UNKNOWN rather than guessing from names. Distinguish 93,334 historical pin entries from the entire ~230K-file working tree, and explain overlap, omissions and growth. Show the top space/file-count contributors and unclassified remainder; the total must reconcile to measured inventory.

### AC3 — Candidate groupings and ownership/dependency graph

Propose at least two **research-system** grouping schemes with rationale, under a **hard ceiling of 30 archives** and a preference for fewer. Provide a legible proposed archive roster, each archive's intended research areas, likely member types, total bytes/files, anticipated access frequency and dependencies. Assign every eligible file one physical archive owner (or a reason it remains loose/excluded/unknown). Cross-system references must resolve through one central index, not duplicate payloads. Identify significant shared evidence, absolute-path consumers, scripts, reports, verifier dependencies and whether each would need direct archive access, controlled extraction, locator adaptation or loose retention. Record a candidate split/merge decision list explicitly for maintainer review; **no final archive mapping is approved by this analysis**.

### AC4 — Defensible retention tiers and backup feasibility

Produce independent **complete archival** and **essential archival** estimates. For proposed exclusions or retirements, distinguish independently reproducible products, replaceable temporary diagnostics, duplicative copies and truly irreplaceable primary observations; supply concrete reproduction/source evidence and confidence. A filename or age is not proof of disposability. Preserve original file/member hashes, provenance and original paths. Analyze the possibility of total essential compressed archives at or below **10 GB**, indicating the compression ratios required, actual tested ratios, unknown data, optional prioritization if larger, and expected backup exposure without any confirmed off-device copy. Neither 10 GB nor 30 archives is an excuse to discard unique primary evidence.

### AC5 — Measured non-destructive compression and verification prototype

Implement a minimal reusable candidate archival format/prototype **against disposable copies or synthetic test trees only**. Prefer `tar.zst` if available, but verify installed tool availability and compare at least one practical alternative or configuration on representative actual **read-only source samples** replicated to disposable storage. No new dependency installations without explicit project authority. Preserve canonical original relative paths; prevent path traversal, symlink/reparse-point escape, duplicate names, case collisions, truncated members, archive bombs or unsafe extraction. Use **one logical master index** (e.g. a JSON or SQLite index; justify choice); member inventories may be embedded in archives but must not yield per-experiment sidecar clutter. Record archive SHA-256, member SHA-256, sizes, original locations, grouping/version, and verifiable restore instructions. Use lossless extraction and byte-equality validation on disposable members, including injected corruption, missing/extra/substituted member, manifest substitution, interrupted packaging and failed restore. Distinguish full archive-byte hashing from validating its included members; an archive hash is only meaningful after initial authenticated member-to-original comparison.

### AC6 — Actual resource and performance accounting

Measure or bound (with disclosed methodology) the **archive creation**, compression ratio, restoration, enumeration counts, bytes read/hashed, elapsed time, peak temporary disk and expected net recovery. Use several representative research-area samples, not only highly compressible text or a tiny synthetic set; include native binary/log/receipt mixes. Quantify complete vs essential outcomes, projected `.local-work/` residual loose-file count and D: free-space change after future staged cleanup, with assumptions and uncertainty bands. Discuss duplicated originals during transactional migration and how to remain above free-space guards. Analyze routine historical archive verification vs loose evidence: fewer file handles alone is not equivalent to fewer bytes read. Keep the earlier **≥80% reduction in redundant routine historical-verification work** as the *eventual migration objective*, not a Stage A claim of achieved savings. Identify measurement/reporting metrics and comparable baseline for future validation. If baseline elapsed time remains unavailable, label it UNKNOWN; do not invent it.

### AC7 — Non-executed migration and cleanup design, editorial completion

Produce a concrete but **NOT AUTHORIZED** Stage B proposal with migration by approved research system; exact candidate manifests for first pilot where feasible; preflight hash/member audit; archive creation and verification; disposable restoration; independent backup/risk decision; locator compatibility tests; explicit maintainer approval boundary for deleting exact loose files; safe postflight verification, rollback and error handling; progress accounting for reclaimed disk and removed files; and behavior if any check fails. Deletion is a required part of any **future approved** successful migration batch, not optional indefinite deferral, but this task performs **zero real deletions**. Protect originals and project policies, no automatic rewriting of consumers, no production activation. Run changed-text screens and **manually read all authored prose, comments, schemas and navigation changes**; record exceptions and repairs.

### AC8 — Independent research, engineering, security and editorial review; verified package

Arrange a genuinely independent read-only reviewer against **this frozen original brief**, primary measurements, source provenance, all acceptance criteria and exact tree/diff. Require explicit PASS/FAIL/NOT TESTED for AC1–AC8; evaluate resource/retention claims, archive format safety, threat model, benchmark methodology, false savings, backup risk, failure injection and editorial quality. The reviewer must challenge unsafe exclusion, projected 10 GB claims, understated storage costs and premature deletion authority. REWORK for missing mandatory tests; ESCALATE for genuine safety, permission or resource blockers, rather than silently relaxing criteria. Record substantive acceptance and a separate final delta review where applicable. Deliver complete/task-only patches including untracked authored files, inclusion/exclusion inventories, exact hashes and forward/reverse applicability, with no Git staging/commit/push. If this is not fully complete, report unfinished criteria honestly.

## Suggested durable output structure

Use existing repository conventions. One reasonable placement (adapt to current repo naming) is `docs/experiments/evidence-archive-discovery/` with:

- `report.md`: concise findings, decisions needed, coverage and uncertainty.
- `research-areas.csv`: every research area with file counts/bytes and evidence role summary.
- `directory-inventory.csv` or an equivalent complete aggregate reconciler (avoid dumping huge personal/absolute path lists into tracked files).
- `archive-options.csv`: grouped candidate archives, merge/split choices and estimates.
- `dependencies.csv`: cross-system and absolute-path consumers.
- `retention.csv`: disposition and justification by evidence class or significant path grouping, exceptions/UNKNOWN.
- `benchmarks.md` and limited reproducible isolated prototype code/tests.
- `stage-b-plan.md`: reviewable future migration, deletion gate, restore and rollback.
- `review.md`, `sources.csv` and contract/verification records.

Detailed raw inventories, private absolute paths, sample captures, benchmark raw results, archive prototypes and scratch outputs remain ignored under `.local-work/` and are **not** placed in Git or published. The proposed central index schema may be tracked as authored design, but do not emit real production manifests or distribute raw evidence.

## Important decision gates and reporting format

At completion, present the maintainer a compact **research-area roster and candidate archive roster** suitable for eyeballing and editing. Explicitly call out the largest areas, proposed combinations/splits, candidate outliers and any irreducible unknown. Report whether **10 GB essential compressed** appears achievable; if not, give measured reasons and sensible priorities instead of trimming originals to meet the goal. State expected improvement in file counts and net storage with realistic confidence. Provide one concrete next approval request: **approve or amend archive boundaries and retention policy**. Do not request authority to delete until a reviewed exact-path Stage B batch and recovery terms are presented and separately approved.

### Prohibited shortcuts

Do not create one archive per brief; do not create hundreds of manifest sidecars; do not treat `.local-work/` as wholly disposable; do not classify unknown originals as regenerable; do not hash huge historical populations repeatedly for cosmetic reassurance; do not rely solely on filesystem journal changes as equivalent to direct byte verification; do not claim an archive digest proves member identity without validated intake; do not hide benchmark I/O in setup; do not upload to Google Drive or create cloud connections; do not assume off-device backup exists; do not modify protected saves, installed data, raw native evidence or analysis databases; do not run the game; do not delete or move genuine evidence during Stage A; do not activate new archival/verification workflow, relax policies, stage, commit, push or publish.

**Frozen completion principle:** Stage A succeeds by providing a measured, safe, comprehensible decision basis and proven *disposable* restoration mechanics. Material disk recovery and the ≥80% routine-verification reduction are Stage B acceptance goals after approved real consolidation, **not accomplishments to claim before migration**. The historical failed preservation-optimization result stays REWORK.
