# Codex implementation brief — B3: Source completeness, historical reproducibility and primary baseline

**Project:** `D:\Projects\starfield-outpost-research\`  
**Research baseline:** **Starfield.exe 1.16.244.0 only**  
**Assignment type:** bounded offline source/documentation implementation, provenance reconciliation and verification  
**Publication status:** NOT CLEARED  
**Authority:** This brief authorizes only the bounded B3 work below. No staging, commit, push, publication, game execution, installed-tool modification, evidence deletion or live instrumentation.

## 1. Purpose and governing decisions

Complete B3 of the accepted B0 release-preparation programme. Make the **minimum necessary project-authored method source and build/configuration material** available in the tracked research repository so the selected first-release findings have a truthful, navigable reproduction path. Resolve historical method-source hash discrepancies to their *actual historical identities* or document the exact remaining limitation. Populate the primary game-build baseline manifest using **existing verified provenance**, not a new native research campaign.

**Critical baseline correction:** Every native/definition research finding in this project targets the **same Starfield executable, version `1.16.244.0`**. Some historical first- and third-party **save files were created under older Starfield versions**; this is saved-evidence provenance, **not** a second executable research baseline and does not warrant a multi-build native crosswalk in B3. Record save origin separately where established, without inventing build associations. Future executable-version crosswalks belong to the later update-qualification policy, not this assignment.

Governing material (read before making changes): `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/PROVENANCE.md`, `docs/audits/publication-readiness-rr1/` (particularly `source-and-reproducibility.md`, `source-inventory.csv`, `source-pin-inventory.csv` and findings RR1-021), `docs/audits/publication-readiness-b0/` (`report.md`, `release-gates.md`, `scope-and-evidence-policy.md`, `versioned-baselines.md`, `local-work-retention.md`, `rr1-dispositions.md`), and B1's `docs/audits/publication-readiness-b1/claim-build-matrix.md` and `docs/research-roadmap.md`. Apply current B2 notation and native-export-ID guidance.

The release is a **research archive**, not a generalized tool distribution. Include authored helper source where essential to understanding/reproducing an accepted method; normally exclude generated outputs. Do not promote everything under `.local-work/` merely because it is a `.py`, `.ps1`, `.pas`, project or build file.

## 2. Source and method census: selective, claim-led

Begin with B1's *proposed* claim/build matrix and RR1's exact source leads. Establish a **source-selection manifest** organized by **selected claim → original method → historical version → input dependencies → candidate source and build files → public reproduction route**. Distinguish:

1. Maintained helpers readers could reasonably run from a fresh checkout;
2. Historically significant/unique method implementations, perhaps archived and explicitly unsupported;
3. One-off scripts essential to a specific accepted result;
4. Duplicated snapshots, generated code, disposable scratch and products, which normally stay local;
5. Third-party sources or embedded game data, requiring separate permissions and B4 decisions.

For every selected candidate identify exact originating path, SHA-256, source authorship/provenance, reason it is indispensable, tracked destination, direct internal dependencies, external prerequisites, possible side effects, and availability tier. Show why selected source is minimal and why excluded candidates are not needed for the stated claim. Do not convert every experimental tool into a maintained product.

**Permitted file promotion:** After inventory/provenance and content inspection, copy **selected original project-authored** source, build definitions and non-sensitive configuration into appropriate tracked directories. Preserve originals in place and their hashes. Do not copy private data, game record dumps, binaries, native analysis exports, decompiled game code, installed SFSE/Ghidra dependencies, or protected sample saves. Promote xEdit `.pas` scripts only if project-authored and not already tracked; installed byte-identical copies in `D:\tools\xEdit.4.1.5p\Edit Scripts\` are legitimate tool-installation copies. No operations on external tool installs.

Prefer reusable path parameters or documented local-input placeholders in reader-facing *usage examples*; preserve original historical source bytes where changing them would obscure evidence provenance. If a historical script depends on a hardcoded path, document that limitation rather than silently altering the pinned artifact. New safety/portability wrappers are separate, identified derivatives.

## 3. Reconcile historical method source identity

Address **RR1-021: 26 historical hash-mismatch occurrences at 23 literal source paths**, plus materially related examples exposed while closing selected B3 methods. For each occurrence, investigate bounded credible sources (actual tracked Git history, protected snapshots, independently hashed local copies, applicable original package manifests). Record:

- Historical citation and expected hash, size/version where available;
- Observed candidate(s) and verified hashes;
- `EXACT RECOVERED`, `CHANGED/CURRENT DISTINCT`, `UNAVAILABLE AFTER BOUNDED CHECK`, or an explicitly justified more precise state;
- Which accepted claim/procedure uses it, what remains reproducible, and whether historical evidence integrity is affected;
- Stable tracked source path if selected for promotion, or honest local-only reference and release limitation.

Do **not** silently update an old SHA-256 to a newer script's hash, rewrite historical evidence to match present files, or declare a mismatch resolved simply because the current script runs. Preserve genuine unavailability as a reportable result and escalate only when it prevents a mandatory selected-method reproduction contract, with a specific missing artifact or scope decision.

## 4. Primary version baseline and locator provenance

Create or populate a reader-facing **primary game-build manifest** (choose a durable path and link it from the appropriate B0/B1 indexes). One investigated baseline: `Starfield.exe 1.16.244.0`. Use existing verified SHA-256 pins for EXE and ESM and catalog directly relevant BA2, SWF, Papyrus declarations and other installed data *only when provenance is supported*. For every entry distinguish pinned/existing verification from any independently rechecked material, and avoid inventing data versions or matching builds.

Preserve historical save **creation-version** provenance in a **separate field/table**, including `UNKNOWN` when not reliably established. Saved-state compatibility limits must not be described as native analysis conducted against an older executable.

Map significant existing semantic/function/structure identities to their **1.16.244.0** locators and source evidence, reusing existing registers; do not create a comprehensive new function census, re-identify every native routine or generate a speculative later-version address crosswalk. Historical native addresses and object offsets must remain bound to the original pinned executable. Explicitly distinguish RVA, preferred VA, field/vtable offset and file offset, and version-specific identities from stable research aliases.

Do not run Ghidra, xEdit, game executable, debugger, the game itself or observer programs to fill baseline entries. New installed-input hashing is not mandatory if reliable verified evidence already exists; discrepancies must be documented rather than assumed away.

## 5. Reproduction contracts and bounded qualification

For each **selected** source/method publish a concise usage contract: purpose, claim/review reference, exactly which source version and build files are provided, required external tools/versions or input classes, minimal invocation guidance (with safe placeholders), whether it reads/writes anywhere, output type and local destination, limits, and whether the method is:

- **SOURCE AVAILABLE** (inspectable source, not necessarily runnable);
- **PROCEDURE REPRODUCIBLE** (qualified instructions/dependencies);
- **SYNTHETICALLY QUALIFIED** (safe, isolated test actually passed);
- **HISTORICAL / UNAVAILABLE** (precisely scoped reproduction limitation).

These tiers describe evidence access, not scientific confidence or rights clearance. Avoid claiming that a fresh clone can reproduce a live historical experiment merely because a script is checked in. Any claimed capability must have its own test and identity receipts.

Execute **at least one safe representative fresh-checkout or isolated-clean-tree synthetic reproduction** for a selected, genuinely non-intervening helper, with fixed synthetic/owned inputs, bounded outputs, documented commands, source hashes and expectations. Choose the smallest adequate method. Before running, explicitly enumerate potential writes and dependency risks. No automatic downloads, real save mutation, game/tool execution, debugger attachment, installed-directory writes, or native-observer execution. Where available safe synthetic tooling cannot support this gate, diagnose in scope and provide a narrow evidenced escalation rather than substitute an unqualified PASS.

## 6. Rights, privacy, documentation and publication boundaries

Only source authored by the project and adequately provenance-checked can be promoted under this brief. Inspect promoted source/build/config for embedded secrets, usernames, absolute paths used as implicit live prerequisites, third-party code and proprietary game data. The presence of a license or a public GitHub copy does not establish rights to redistribute unrelated code. Rights/publication approval remains **B4/B6**; privately tracking a candidate is not clearance.

Installed Ghidra, xEdit, x64dbg, Ghidra databases, retail game executables, `Starfield/` INI/libraries/archives/ESMs/BA2s, extracted game content and decompiled `.c`/`.asm` or bulk assembly must remain outside publication candidates. Short authored explanatory pseudocode and bounded cited assembly excerpts in *documentation* follow B0 policy; do not publish decompiler output under a new file extension. Retain legitimate historical machine paths as provenance, but ensure current instructions and tracked links are navigable without private directory layouts.

Do **not** select, compress, publish or copy control/mature saves and screenshots; B4 owns those decisions. Do not delete residual `.local-work` or system-temp folders, fix scratch creators, prune copies, or run blanket `git clean`; B5 owns cleanup.

## 7. Deliverables

Place new durable B3 documentation under `docs/audits/publication-readiness-b3/`, with appropriate updates to navigation indexes and claim/build links. Produce at minimum:

1. `report.md`: answer-first B3 disposition, precise selected scope and remaining reproducibility holds;
2. `source-selection.md` plus machine-readable manifest of selected/promoted/rejected/deferred candidates, paths, hashes, ownership, dependencies and reasons;
3. `historical-source-reconciliation.md`: all 26 RR1-021 occurrences with reproducibility impact and exact identity disposition;
4. `method-reproduction.md`: per-selected-method usage and availability tiers, synthetic-qualification receipt;
5. `baseline-manifest.md` (and structured manifest if useful): **single** investigated `1.16.244.0` executable baseline, pinned inputs, locator/offset domains, separately qualified save origins;
6. `review.md`: frozen AC matrix, source/claim inventories, test/regression/failure ledger, preservation status and independent disposition;
7. Promoted minimal authored source/build files **only where justified and inspected**; link to them via tracked relative paths. Do not silently duplicate existing tracked sources.

For any promoted executable source, place a clear status and safety warning in its entry README. Record originating local hash and new tracked hash. Do not change existing accepted scientific interpretations or confidence and publication classifications. Fix only the currently permitted indexes/necessary reference text; flag wider inconsistencies for B4/B6 rather than expanding the assignment.

## 8. Frozen compact completion contract — AC1–AC8

**AC1 — Scope, baseline and preservation.** Confirm authority, source identity, project state, both-drive/disk guards and protected-input hashes before work. No game/tool installations or protected evidence altered, no live/debugger/deployment work, no Git staging/commit/push.

**AC2 — Claim-led source selection.** Every selected first-release method has an exact minimum-needed source/build/dependency and availability determination; a reasoned manifest distinguishes maintained, archival, redundant, third-party and generated candidates, including a justified no-promotion result where appropriate.

**AC3 — Historical identity closure.** All 26 RR1-021 hash-mismatch occurrences across 23 paths receive exact recovered/distinct/unavailable findings with attempted evidence, affected claims and reproducibility consequences. No historical repinning without positive historical identity.

**AC4 — Source promotion and rights hygiene.** Each promoted file has verified origin, authorship, hash, tracked destination, dependencies, content/security/rights screening and preserved local original. No prohibited proprietary, extracted, decompiled, private or disposable bulk payloads introduced. No automatic promotion by extension/folder.

**AC5 — Reproduction contract and safe qualification.** Each selected method has honest instructions, input/output/side-effect description, external dependency policy and availability tier; at least one representative safe isolated synthetic/fresh-checkout reproduction is evidenced and verified, with no actual installed/game/live intervention.

**AC6 — Single-game-version baseline.** One independently documented and source-pinned `Starfield.exe 1.16.244.0` native research baseline; relevant installed-data provenance and 1.16.244.0 locator domains; older-save creation versions *separately* qualified, not treated as other analyzed executables. Later-version crosswalk implementation explicitly deferred.

**AC7 — Durable source/research navigation.** B3 report, inventories, mismatch decisions, method contracts and baseline manifests are complete and relative-link navigable; accepted findings, historical source pins, B0/B4/B5/B6 boundaries and NOT CLEARED status retained. Findings and source-version availability not overstated.

**AC8 — Verification and independent review.** Run manifest/hash/relative-link/UTF-8/prose/identifier checks; validate selected synthetic case and all affected regressions; obtain independent reviewer assessment against **these original AC1–AC8**, not merely a newly narrowed post-hoc contract. Preserve failures and corrections, independently reconstruct complete and task-only diffs forward/reverse with verified content inventory, report original/current HEAD/index and all protected hashes, and return package plus reviewer `ACCEPT`, `REWORK` or `ESCALATE`. Do not integrate automatically.

**Negative-result closure:** Missing historical source may be recorded as an evidenced scoped limitation; cannot be silently substituted. A reasonable search of credible exact-hash sources can close that acquisition branch. A missing mandatory *selected* reproduction requirement must be corrected in scope or specifically escalated for maintainer scope decision; do not fabricate tests or use hypothetical alternatives as universal blockers.

**Continuation authority:** Diagnose, correct and reverify ordinary in-scope defects without needing a new brief. Freeze mandatory criteria; material changes require maintainer agreement with amendment history. Report genuine authority, integrity, input-access or resource blockers with exact paths, failed checks, preserved checkpoint and narrow next decision. Apply the repo's research execution protocol and healthy-run safeguard; no arbitrary premature stopping.

**Submission:** Summarize selected/promoted and excluded source, mismatch closure, baseline, synthetic reproduction, remaining publication holds and actual independent verdict. Provide complete and task-only verified diffs and manifest. Recommend commit message only; **do not stage, commit, push, distribute or publish**.
