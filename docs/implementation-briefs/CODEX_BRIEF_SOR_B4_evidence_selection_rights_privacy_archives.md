# Codex implementation brief — B4: Evidence selection, rights, privacy, and supplementary archives

**Project:** `D:\Projects\starfield-outpost-research\`  
**Assignment:** B4, following accepted/committed B0–B3 and RR1  
**Type:** bounded publication-preparation research, documentation, reviewed policy integration, and **local provisional** evidence packaging  
**Status:** maintainer-authorized scope; **not authority to publish, upload, change visibility, stage, commit, push, rewrite saves, or delete files**.

## 1. Goal and governing decisions

Prepare an exact, reviewable recommendation for the evidence and other third-party-sensitive material that could accompany **one coordinated GitHub research-archive release** of Starfield Outpost Systems Research. Explain claim-by-claim which materials are essential, useful or archival, what can be made intelligible without releasing private originals, and what can be offered as supplementary evidence. Incorporate necessary narrowly scoped publication-policy corrections into a reviewable patch; never claim the repository is cleared for publication.

Read and respect `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/PERMISSIONS.md`, `PUBLICATION.md`, `LICENSING.md`, `THIRD_PARTY_POLICY.md`, `THIRD_PARTY_NOTICES.md`, B0 `docs/audits/publication-readiness-b0/{report.md,scope-and-evidence-policy.md,release-gates.md,versioned-baselines.md}`, RR1 evidence/licensing/findings registers, the B1 claim/build matrix, and B3 source/baseline manifests. Treat the **actual current tracked revision** as the authority; document conflicts. Inspect the relevant accepted report/review pairs and their evidence ledgers. Do not mistake earlier audit *proposals* for publication permissions.

The maintainer has decided:

- The intended release is a **research archive**, not a generalized software product, and should be **one coordinated public repository/tag/release**, not staged public exposure. The research's investigated game executable is **Starfield 1.16.244.0**; save creation versions may differ.
- Original authored research/source is intended to use **GPL-3.0-or-later**; no blanket license claim over underlying Bethesda/third-party content. Publication clearance requires specific review.
- Research explanations, compact original pseudocode and bounded illustrative assembly are legitimate candidates; **do not publish decompiled `.c`/`.asm` source, bulk native dumps/disassembly, Ghidra databases, installed tools, game EXE/ESM/BA2, game-install INIs/libraries or extracted assets**. Review any embedded excerpts by actual content, not suffix alone.
- Project-authored helper source/build definitions (including project-authored xEdit scripts) may be tracked where justified; B3 dealt with source promotion. **Do not use B4 to promote further ignored source or distribute built observers.**
- First-party control saves, selective mature first-party saves, and first-party screenshots are **publication candidates**, not automatically cleared. Character names are acceptable. Inspect for identifying account/platform/user/path data and other concrete disclosure concerns, without inventing an extraordinary save-publication prohibition. Third-party donor saves remain excluded without affirmative permission.
- **Save-file bytes must never be sanitized, redacted, rewritten, patched, or otherwise transformed** for publication. If necessary and acceptable, select the exact unedited source file; otherwise exclude/hold it. Lossless archive compression is allowed and changes only the enclosing archive. Compression is optional for roughly 2 MB control saves and strongly preferred for roughly 16 MB mature saves. Preserve original names and full SHA-256.
- GitHub **Release assets** are the preferred home for downloadable supplemental archives; the Git repository should contain a durable evidence index, with no fabricated live asset links and no unrelated file-hosting dependency. Packaging stays local until separately authorized publication.
- No unapproved Git-history rewrite, private-data disclosure, source-game redistribution, evidence original modification, `.local-work` deletion, or external scratch cleanup.

## 2. Workstreams

### B4-A — Claim-to-evidence selection

Use the current B1 release claim/build matrix, research roadmap, RC1, and accepted report/review evidence ledgers. For each **proposed release claim** classify whether independently checking it needs: (a) publicly documented reasoning/source and lawful user-installed game inputs, (b) selected original saved/captured evidence, or (c) unavailable local-only/third-party evidence. Identify the minimum meaningful public evidence and precisely what remains nonreproducible if omitted.

Make a decision-ready ledger of **essential / useful / archival** candidates; don't demand the original save whenever an authored explanation or reproducible method suffices. Conversely do not claim an untracked Save52 reference is independently replayable without its bytes. Review major controls including Save30–36 (POI/clutter), Save37–39 (Kreet coordinates), earlier controlled series, and first-party mature Save52/HIST-0255 and other genuine unique witnesses as candidates, **not predetermined inclusions**. Ground names, exact file identities, ownership and availability in records; avoid assumed equivalence between Save52 and any HIST alias without documentary support. Explain external-name examples (e.g. Feynman V / Carinae) and B2 evidence-context decisions.

### B4-B — File-level publication suitability and privacy

For each shortlisted actual file, record path or local-only locator, immutable source identity (size and SHA-256), producer/ownership status, research purpose, creation/game-version metadata when supported, explicit first/third-party status, known dependencies, privacy inspection scope, rights assessment/status, and disposition (`PROPOSE INCLUDE`, `PROPOSE EXCLUDE`, `HOLD FOR MAINTAINER`, `LOCAL-ONLY`). Avoid copying identifying contents verbatim into public audit prose. Character names alone are not grounds for rejection. Inspect actual candidate bytes/metadata only through approved read-only parsers or file reads; never load/modify a save in the game. For screenshots, inspect pixel overlays and metadata and pair with exact ledger hashes; a screenshot does not automatically prove a same-time save join.

Clearly separate **technical/privacy pass**, **rights assessment**, **maintainer selection approval** and **actual publication authorization**. The first does not imply the latter three. If legal status cannot responsibly be determined from available evidence, label a precise decision/uncertainty and hold that candidate; don't give categorical legal clearance or fabricate restrictions.

Review project-authored explanations, code, bounded native snippets, credits/notices, relevant Git-history paths and intended release references for third-party material, privacy, authorship and licensing boundaries. Reuse RR1 history scanning with stated limits, rather than pretend that the present tree is the whole future publication surface. No Git-history edits.

### B4-C — Policy integration and licensing/credit proposals

B0 identifies a conflict between the existing blanket raw-save exclusion and the maintainer's **conditional, individually approved first-party original-save evidence** policy. Prepare a **narrowly worded reviewed amendment** to `PUBLICATION.md`/other directly relevant policy documents where permitted by actual governing authority: allow only selected unchanged first-party save evidence after file-specific privacy/rights/maintainer approval; retain bans on donor originals without permission and all game/install/decompilation exclusions. If an authority or permission requires separate approval **before editing even policy text**, deliver a proposed patch/document instead and explicitly escalate that boundary. A policy-text amendment is not a file-specific clearance, upload authorization or public release.

Confirm original GPL-3.0-or-later scope, author/contributor attribution, exact third-party notices and limited SFSE permissions, without generalizing from the three sibling public repositories. Identify unresolved rights decisions in the approval ledger and keep `PUBLICATION` status **NOT CLEARED**. Do not reproduce full third-party license files without a specific reason.

### B4-D — Provisional archive design and optional local construction

Propose GitHub-hosted supplementary archive groupings based on evidence purpose, e.g. controlled saved experiments, selected mature witness saves and screenshots; keep the expected Git clone lightweight. Choose and document a lossless format, member names, expected extracted size, source hash, archive compression/version and privacy/rights status. Include claim/report/experiment links for each member. Avoid duplicate inclusion of the same bytes across archives unless justified.

**Only package locally candidates whose specific review has passed and whose local provisional packaging is authorized by this brief.** Packaging is not release clearance. Where a material rights/permission decision is still pending, maintain a proposed manifest without copying the file into a distributable candidate archive. Under no circumstance transform save contents: verify each extracted `.sfs` is byte-identical to the protected original. Prefer archives under an ignored `.local-work/b4/` review area, with disk/free-space checks and no generated output elsewhere. Preserve source originals immutable. If any needed archive member fails identity/permissions/space checks, halt only that packaging action, retain the evidence and mark it `HOLD`.

For actual provisional archives provide: archive SHA-256, format/codec and producing tool version, byte length, *complete* member inventory (names, uncompressed lengths and SHA-256), protected-original comparisons, independent extraction/reconstruction checks, and no credentials/path leaks. Small uncompressed controls may be proposed as individual assets where sensible. No fabricated GitHub Release URLs; document stable **future link templates** distinctly from operational URLs. Build a tracked proposed evidence index with provisional status, not broken Markdown links to nonexistent assets.

### B4-E — Reproducibility consequences and deferred decisions

Produce a concrete inclusion/exclusion and claim-impact matrix. Explain how a reader gets the corresponding lawful game inputs themselves and what limitations apply when local-only inputs are absent. State which archives cannot be built or published until specific maintainer/rights decisions. Do not insist that every experimental capture or mature playthrough must be public to preserve the author's scientific conclusion. Forward unresolved source completeness to B3 follow-up if truly new, runtime/tool cleanup to B5 and final exact-contents/history/archive verification to B6; do not undertake those batches.

## 3. Deliverables (suggested locations)

Create a bounded B4 report area under `docs/audits/publication-readiness-b4/` including:

- `report.md`: answer-first summary, chosen/proposed distribution model, holds, rights/status and next decisions;
- `claim-evidence.md` or CSV: each selected proposed claim, key evidence, alternatives and reproducibility consequence;
- `file-dispositions.csv`: **actual** candidate identity/hash, authorship/rights/privacy/necessity, inclusion proposal or hold, reviewer and cited input;
- `rights-policy.md`: exact publication/third-party/privacy/attribution analysis and any narrowly scoped policy text change;
- `archive-plan.md` plus member manifests: uncompressed versus compressed packaging, provisional members, codec, hashes and future repository-link route;
- `review.md`: frozen AC matrix, failures and remediation, actual independent verdict, package/patch receipts.

Use the repo's existing naming and ledger conventions when they are more suitable. Link new docs from relevant release-readiness indexes with **relative tracked links**. Keep local file inventories, candidate archives and other non-public details in ignored local review storage unless explicitly approved for tracking. Any externally identifying data should be represented safely in tracked ledgers.

## 4. Frozen compact completion contract

- **Task type:** publication-preparation engineering, evidence audit, policy documentation and selective local archive qualification.
- **Question/deliverable:** Decide and document exactly which source-supported evidence is suitable and useful for proposed publication, preserve originals, propose/construct valid local supplementary packages, and make necessary narrow policy integration reviewable.
- **Scope:** Read-only inspection of nominated local/tracked evidence and relevant Git history; documented/authorized policy and audit file edits; optional guarded local compression of **cleared-for-provisional-packaging** original candidates. No game, Ghidra process, live experiment, save modification, source promotion, external upload, deletion, staged Git changes, publication or history rewrite. Preserve protected inputs and both-drive 40,000,000,000-byte free-space guard where applicable; obey established worker and STOP safeguards.
- **Mandatory acceptance criteria (freeze before execution):**
  - **AC1 — Authority and identity:** Read applicable governing sources and current B0/B1/B3/RR1 artifacts; establish exact starting tree, protected originals, integrity and permitted operations; document excluded actions.
  - **AC2 — Claim-led completeness:** Produce a reviewed claim-to-evidence matrix for the proposed research baseline, with essential/useful/archival distinctions, local-only dependencies and no unexplained mandatory Save52 inclusion.
  - **AC3 — Evidence identity and privacy:** Give a file-specific, provenance- and hash-backed disposition for all selected candidate classes, including first-party controlled/mature saves, screenshots and excluded third-party originals; preserve character-name policy and immutable-save rule.
  - **AC4 — Rights, licensing, policies:** Precisely assess original/third-party materials, bounded analysis excerpts, Git history and attribution; reconcile the raw-save policy tension via authorized narrow documentation change or explicitly prepared approval-ready amendment; retain NOT CLEARED.
  - **AC5 — Supplementary package contract:** Provide working archive/member manifest specification and verified **actual local archives for all approved-to-package candidates** (or reasoned exact holds); prove byte-exact save extraction; distinguish future URL templates from active links.
  - **AC6 — Reproducibility/access consequences:** Every inclusion/exclusion explains its impact on independent inspection and lawful reconstruction; track missing local-only originals, source and selected release dependencies without invented guarantees.
  - **AC7 — Documentation quality and preservation:** Current report, CSV/registers, new index links, original scientific findings and source/version pins unchanged; all edits readable, correctly encoded and free of ungrounded publication claims.
  - **AC8 — Independent critical review and packaging:** Obtain a fresh independent reviewer verdict on this exact B4 snapshot against AC1–AC8, remediate REWORK within the assignment, preserve failures, verify required hashes, integrity, link/UTF-8/format checks and exact forward/reverse reconstruction of **complete** and **task-only** diffs. Return status/inclusion/exclusion manifest, criterion matrix, reviewer decision and protected-input checks; nothing staged, committed or pushed.
- **Optional improvements:** Attractive organization of archive groups; nonessential screenshots; expanded cross-repository style comparisons. Never substitute optional output for failed mandatory criteria.
- **Negative-result closure:** Scoped justified exclusion or HOLD counts as completed research for a candidate when the specific evidence, alternatives, legal/technical limits and consequences are documented; lack of evidence is not affirmative redistribution permission. An unapproved item must never be packaged as cleared.
- **Continuation authority:** Diagnose/fix in-scope validation and reviewer defects, revise ledgers/archives, retest and resubmit under the same assignment; no new brief for routine REWORK. Mandatory criteria cannot be changed without maintainer approval.
- **Exit/escalation:** Stop affected activity if protected hashes change, file identity cannot be established, available free space falls below guard, an essential source is inaccessible after reasonable search, publication permission is unknown for a proposed packaging action, or the operation exceeds authority. Preserve exact observations, attempted routes, checkpoint and narrow request. Continue unrelated authorized work. No arbitrary healthy-run cutoff without a justified authorized exception.
- **Review artifacts:** Primary evidence/file ledger, accept/hold/exclude status, separate scientific/technical/rights/authority outcomes, actual failures/regressions, complete/task-only patch inventories and SHA-256, exact applicability and reverse reconstruction, independent reviewer receipt and final disposition.

## 5. Final Codex return

Summarize: (i) the candidate evidence actually examined, selected/held/excluded, (ii) file/privacy/rights concerns needing the maintainer's decision, (iii) the policy-amendment status, (iv) local archives actually built and verified versus only proposed, (v) changed tracked files and ignored local artifacts, (vi) AC1–AC8 and independent review status, and (vii) full accessible paths for verified complete/task-only diffs. Propose a concise commit message. **Do not stage, commit, push, create a GitHub release, upload an archive or mark publication CLEARED.**
