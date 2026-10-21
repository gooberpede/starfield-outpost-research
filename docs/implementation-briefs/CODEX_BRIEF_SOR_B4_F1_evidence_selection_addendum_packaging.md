# Codex brief — B4-F1: Evidence selection, addendum, and provisional packaging

**Project:** `D:\Projects\starfield-outpost-research`  
**Task type:** B4 documentation/evidence-selection continuation and bounded local packaging  
**Authority:** Explicit maintainer request for this brief; follow the repository's `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/PUBLICATION.md`, and B0/B4 policy and review records, as amended by the decisions below.  
**Publication status:** NOT CLEARED. **Do not publish, upload, stage, commit, push, change visibility, or create a GitHub release.**

## 1. Question and intended result

Revisit B4's 71-file evidence inventory and 26-row claim/evidence assessment in light of the maintainer's subsequent decisions. Produce a **minimal, scientifically justified core evidence shortlist**, a **separately justified optional evidence addendum**, and clear local-only/excluded dispositions. Prepare **provisional local evidence archives or unchanged stand-alone file packages** for files which pass the authorized selection, provenance, privacy, and preservation checks; verify every member against its protected original. Deliver final proposed membership for **maintainer approval before distribution**.

The archive is supporting evidence for a **research release about Starfield 1.16.244.0**, not a general game-save collection or a software distribution. Historic save-origin versions are distinct from the single investigated executable version.

## 2. Settled decisions — do not relitigate

1. **First-party saves/screenshots are eligible** as research evidence. This is a maintainer policy decision informed by established community practice, **not a representation that Bethesda/ZeniMax granted an express license or that legal risk is eliminated**. Do not hold every first-party item solely for lack of individual written permission. Record applicable notices accurately and keep rights decisions file-specific.
2. **Third-party saves are excluded** unless a separate permission decision is supplied. No donor material is implicitly promoted.
3. **Save contents are immutable.** Do not sanitize, edit, redact, rewrite, resave, or otherwise transform `.sfs` bytes. A file that fails a necessary inspection is excluded or held. Packaging and reversible lossless compression may wrap the unchanged bytes.
4. **Character names are acceptable.** Historical paths including `C:\Users\User` are acceptable provenance, provided they do not make public instructions nonportable and no other genuinely identifying or sensitive detail is exposed.
5. **HIST-0255 is first-party** as a maintainer-accepted provenance determination grounded in its original membership in the authorized local `Saves` inventory. It is **not** Save52. **Save52 = HIST-0267**. Retain exact hash-based identity distinctions.
6. Inclusion is governed by **distinct scientific utility**, for control saves and mature saves alike. The safeguard against bloat is eliminating redundant or low-value evidence, not assuming ZIP materially shrinks already compressed saves.
7. A **core evidence package** and a **separate optional evidence addendum** may be attached as GitHub Release assets, both discoverable from the tracked evidence index. The addendum is curated, not a dump of everything omitted from core. Nonselected material can remain private/local-only.
8. Compression is **optional for small controls and larger saves**; measure compression benefit and choose lossless packaging based on actual benefit and usability. A ZIP archive with little compression may still be reasonable for grouping; unchanged stand-alone files may be more useful for some controls. Preserve original filename and SHA-256 in all cases.
9. Ghidra/projects/databases, installed tools, game installations/EXE/ESM/BA2/INI/libraries, bulk decompiled material, and other protected proprietary inputs remain excluded. Existing analytical reports, bounded original pseudocode and approved source code are separate categories; do not expand B4-F1 into source promotion (B3 completed).
10. **One coordinated release** is intended; assets will be GitHub-hosted and linked from the Git repository when actually released. No fake or premature download URLs. B6 and the maintainer approve exact release assets/history.

## 3. Sources to read first

Before modifying anything, inspect and reconcile the exact current documents, at least:

- `docs/audits/publication-readiness-b4/`: `report.md`, `file-dispositions.csv`, `claim-evidence.md`, `archive-plan.md`, `rights-policy.md`, `review.md`, all relevant manifests and privacy receipts.
- `docs/audits/publication-readiness-b0/`: `report.md`, `scope-and-evidence-policy.md`, `release-gates.md`, `versioned-baselines.md`.
- B3 baseline and provenance documents, B1 proposed claim/build scope, and the current `docs/PUBLICATION.md` and `THIRD_PARTY_NOTICES.md`.
- `docs/experiments/historical-save-inventory/inventory.json`, the original **protected local inventory containing filenames/paths**, and existing exact source/copy hash manifests. Resolve identities by SHA-256, not numeric alias alone.
- The accepted research reports and evidence ledgers cited by each candidate, especially controls Save30–39, older controlled experiments, Save52/HIST-0267, HIST-0255, and visual L3/coordinate witnesses.

Treat existing B4 recommendations as starting proposals, **not frozen selections**. Confirm the actual 71-member inventory (50 previously held, 13 proposed exclusions, eight local-only). If more candidate evidence is found through claim closure, add it to a separately identified reviewed appendix without silently altering original B4 inventory counts.

## 4. Workstream A — claim-led minimum selection

For every candidate, determine and document:

- Stable B4 ID, `HIST-`/`SaveNN` aliases, **actual original filename**, exact source evidence and SHA-256; distinguish same-file aliases from different saves.
- First-party/third-party provenance, supported privacy inspection depth, actual restrictions, and whether remaining hold is **specific** rather than generic absent written permission.
- Supported research claim(s), control/counterexample role, whether its bytes are needed for exact replication, and whether a smaller first-party witness/synthetic procedure/published explanation already covers it.
- The **marginal evidentiary value** of inclusion relative to the provisional core set. Avoid choosing duplicate snapshots by count, date or size alone.
- Proposed disposition: `CORE`, `ADDENDUM`, `LOCAL-ONLY`, `EXCLUDE`, or `SPECIFIC HOLD`; concise reason and any outstanding maintainer choice. Distinguish `PROPOSED` from `MAINTAINER APPROVED` and `PUBLICATION CLEARED`.

Explicitly assess whether Save52/HIST-0267 and HIST-0255 each supply noninterchangeable evidence. Do not replace one with the other. For control sequences, reason about whether their full causal sequence is necessary and avoid selecting just a result save where the baseline/intervention matters.

Produce a **coverage/redundancy matrix**: per accepted release claim, what core file(s) support it, whether addendum evidence adds a separate witness, what is locally withheld, and what reproducibility remains possible without binaries. No arbitrary numeric file cap.

## 5. Workstream B — provenance, privacy and exact filenames

Retrieve original save filenames by their **verified hashes** from the protected local historical inventory, without editing or re-decoding saves merely to obtain names. If original filename retrieval is impossible, document exact lookup attempt, evidence scope and unresolved identity; do not invent names. Use exact filenames as archive member names where safe and unambiguous, with a deterministic safe prefix or explicit collision resolution only when needed. Manifest should retain both original name and any archive member path.

Re-use B4 privacy results where valid; perform only targeted additional read-only inspection for shortlisted items with genuinely insufficient coverage. Do not claim exhaustive forensic privacy clearance from header or text search. Character names and the workstation profile `User` are not automatically grounds for exclusion.

Review screenshots for incidental identifying content and relevant scientific context; distinguish witnessed UI/surface state from an asserted exact saved reference join. No screenshot edits or re-encoding absent separate approval; originals should normally be retained byte-for-byte.

## 6. Workstream C — provisional packaging

First finish the selection and actual applicable inspection gates. Then build **local-only provisional** `CORE` and `ADDENDUM` archives and/or stand-alone candidates. If a particular member cannot lawfully/safely be packaged under actual authority, keep it in `SPECIFIC HOLD`, explain the precise obstacle, and package the remaining independently cleared candidates where permitted. Do not describe package preparation as maintainer's final public-file approval.

- No writes to original saves/screenshots, their source directories, installed game/tools, or protected evidence archives. Work exclusively in a bounded `.local-work/b4-f1/` scratch/output root (or an existing compliant project-local root), with disk free-space protections and output inventory/guards per project rules.
- Losslessly measure both ordinary ZIP/DEFLATE and stored/no-compression options on a **representative selection** (or all proposed members where efficient). Report original/archive size, savings percentage and packaging convenience; choose based on observed results rather than a fixed presumption that mature saves compress well.
- Use deterministic member paths and safe archive names; prevent path traversal and unintended duplication. Where archives are made, record codec/tool/version/options and archive SHA-256/size.
- Record each member's B4 identifier, stable research alias, **original filename**, archive path, source size/hash, producer, experiment/claim, identity/provenance/inspection decision and exact selection status.
- Verify extracted files byte-for-byte against immutable originals (size and SHA-256, preferably direct byte comparison) using a separate scratch extraction destination. Archive integrity is not a live save-load test.
- Archives must remain ignored/local and **must not** be added to Git, uploaded, linked as existing releases, or described as publication-approved.
- If the complete set cannot be packaged, identify exactly which members were left out and why. Never claim successful extraction verification of an archive that was not built.

## 7. Workstream D — documentation and later-gate integration

Add/update bounded durable B4-F1 documents under `docs/audits/publication-readiness-b4/` (or a clear subdirectory) so a reader sees the **proposed** member inventory and supporting decisions. Keep actual private filenames/paths and sensitive identifiers in local manifests if necessary; public-facing manifests can use research aliases plus hashes pending final review. A future release evidence index should show the intended GitHub Release grouping and relative references to claim documents; label URLs **PENDING RELEASE** until actual GitHub assets exist.

Reconcile B4 rights/policy status to the maintainer's post-B4 decisions **without claiming unrestricted Bethesda rights or automatic clearance**. Prepare any narrow policy integration required, review its exact wording, and preserve the existing third-party restrictions. Do not alter original scientific classifications, original source pins, or historical reviewer findings.

Document what B6 must verify on actual assets, including manifest consistency, member provenance, hashes, Git links/release URLs, downloadability, and unchanged tracked tree/reachable history review.

## 8. Authority and safety

**Allowed:** read-only inspection and hashing of existing research sources/evidence; bounded privacy and provenance checks; authored documentation and manifests; copying vetted bytes solely into ignored local candidate packaging; safe compression/extraction comparisons using local scratch; proportionate tests and independent review.

**Prohibited:** save editing/sanitization, moving/deleting protected or other local files, gameplay/game launch, Ghidra or debugger target operations, installed-tool or game-file mutation, source promotion unrelated to B4-F1, external contact, third-party save disclosure, Git staging/commit/push, GitHub upload/release creation, public distribution, visibility/license grant expansion, and making final maintainer selections by implication.

Keep all original files unchanged; hash protected starting inputs and check unchanged at end. Inspect tracked working-tree/HEAD/index and preserve concurrent work. Apply existing C:/D: free-space guards (40,000,000,000 bytes where relevant) before meaningful writes, and refuse package construction if identity, safety or space checks fail. No blanket `.local-work` cleanup. Avoid arbitrary test-volume/time cutoffs absent specific risk.

## 9. Frozen completion contract (AC1–AC8)

**AC1 — Authority and input protection.** Original B4/B0 policy, permitted roots, current Git tree and protected source/evidence identities inspected. All inputs, HEAD and index remain unchanged; no unauthorized game/external/Git operation.

**AC2 — Full inventory reconciliation.** All 71 prior B4 rows retain exact original ID and are reclassified under the maintainer's decisions; first-party evidence isn't automatically held for absent written permission; third-party materials remain excluded. Added candidates, if any, are clearly distinct.

**AC3 — Exact identity and provenance.** Every proposed CORE/ADDENDUM save has verified SHA-256, original filename/alias and source provenance, with HIST-0255 first-party and Save52=HIST-0267 distinctions; unresolved filename identity is an explicit limitation, not fabricated resolution.

**AC4 — Scientific selection and coverage.** A claim-to-evidence/redundancy matrix justifies each core and addendum item and each important omission, including contrasting controls and unique mature witnesses. No minimum save count, automatic whole-corpus inclusion or compression-first rationale.

**AC5 — Privacy, rights and policy status.** Targeted actual file reviews and a narrowly consistent policy record; no modified saves and no claim of blanket legal permission. The exact selection and any specific holds remain visible; user approval/publication clearance not invented.

**AC6 — Provisional packaging and verification.** Package all candidates eligible under the actual local-assembly gates, or document member-specific genuine holds and build the safe subset. Record compression measurements, concrete archive/member manifests, archive hashes and byte-exact extraction receipts for every built asset. No phantom archive PASS.

**AC7 — Durable release-facing documentation.** A readable candidate index, original-file/alias map, proposed release/addendum structure, clear PENDING asset labels, and B6 handoff. Link/prose/notational integrity and historical scientific/policy preservation checked.

**AC8 — Independent critical review and verified delivery.** A genuinely independent reviewer examines the **frozen original criteria** and primary selection/privacy/packaging evidence; returns ACCEPT/REWORK/ESCALATE with all-criteria PASS/FAIL/NOT TESTED matrix, correction history and separate scientific/authority dimensions. Deliver status/inclusion/exclusion inventories, exact complete and task-only diffs (including all added text/manifests), verified forward/reverse byte reconstruction, checks and proposed commit message. Reviewer acceptance is not maintainer publication approval.

Negative/partial scientific evidence may be reported within stated scope; **a failed mandatory packaging or safety verification cannot be called PASS**. Correct in-scope problems and requalify under the same assignment. If a necessary user-only approval or inaccessible essential original blocks only certain members, preserve the actual blocked identity and proceed with independent authorized work. Escalation must be narrow and evidenced.

## 10. Required return

Return a short summary with: CORE/ADDENDUM/LOCAL-ONLY/EXCLUDE/SPECIFIC HOLD counts and precise rationales; original historical-save filename reconciliation (including HIST-0255); measured compression savings; actual local package paths and hashes **only where built**; archive member/extraction verification; unresolved user decisions; all eight criteria; independent decision; protected-input and HEAD/index status; complete/task-only patch paths; suggested commit message. No commit or publication.
