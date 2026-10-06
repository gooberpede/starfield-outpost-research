# Initial reconnaissance review package

2026-10-06; SOR-EXP-0001. Agent self-check, **not independent critical review or integration approval**. Governing [brief](../implementation-briefs/CODEX_RESEARCH_BRIEF_initial_outpost_system_reconnaissance.md); [report](../experiments/initial-outpost-system-reconnaissance.md); [evidence index](../experiments/evidence/initial-reconnaissance/README.md).

## Actual checks and limits

- Installed/pinned Starfield and CK size/SHA-256 equality verified; Ghidra imported hashes match. Version resources and preferred PE bases read directly. No live compatibility test.
- All 37 pre-existing Ghidra project/database files rehashed after eight successful bounded read-only/no-analysis exports: zero changed path/size/hash records. Read-only flags were supplemented by actual hash comparison. Ordinary tool caches/settings/logs were written to private workspace. Initial batch launcher attempts failed on Java preference permissions; direct JVM launch with documented installed settings succeeded. No analysis-state edits performed.
- Starfield.esm SHA-256 before/after both xEdit runs matches `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`. Source copies and the archive retain original byte hashes; no saves were accessed.
- Corrected xEdit discovery helper and focused helper executed by the user; original syntax error and repair recorded. Output metadata/counts inspected, 1,743 discovery records and 15 focused details. First-pass detail cap acknowledged; focused pass has no cap flags. Actual helper deployment hashes match repository source. No second ESM decoder, arbitrary malformed-input suite or other xEdit-version compatibility test.
- Ghidra helper compiled and ran. Eight exports comprise broad/interface scans for each executable, two retail function/callback passes, CK registration functions and retail membership follow-up. Final helper supports targeted references and missing-function instructions without creating functions. Export limits explicit; one larger callback instruction section is capped. Decompilation success is not semantic proof.
- Independent PE header/section mapping and four 24-byte reads checked callback instructions and three registration LEA targets. Raw bytes/offset mappings are local in pe-checks.json; not a universal structure-layout validation.
- Source claims reviewed against exact local script lines; ESM attachments prevent incorrectly assigning OutpostContainerScript to ordinary storage. Public reports stay SOURCE-REPORTED. No runtime/save semantic finding, native serializer identification or validated hook claim.
- Final Markdown target/encoding checks, diff whitespace, status, tracked-file boundary and complete review export results are appended after execution below.

## Rights and operation review

Materially used sources are SOR-S-0101–0112, credited at point of use and in CREDITS.md. Only original helpers and factual notes added. No third-party implementation copied/adapted, no dependencies installed, no mod files downloaded, no fork/PR/issues/comments/contact or uploads. Local Bethesda script extraction was explicitly authorized inspection and remains ignored/local. No licence grant was treated as incorporation permission. Raw outputs are LOCAL-ONLY; authored notes/index REVIEW-REQUIRED.

No game/CK UI launch, debugger attach, instrumentation deployment, plugin/save editing, live experiment, staging/commit/push/tag/remote/visibility change. Two original xEdit scripts were copied into Edit Scripts at user request and remain there; no cleanup or deployment into the game. Existing unrelated files were left alone. Licence text unchanged. Crash-tolerant policy still requires separate bounded live authorization, save protection, flushed evidence and corruption stops.

## Review contents and open limits

Tracked-document changes: AGENTS.md, CREDITS.md, README.md, THIRD_PARTY_NOTICES.md; docs/DECISIONS.md, EVIDENCE_STANDARD.md, PERMISSIONS.md, PROVENANCE.md, README.md, RESEARCH_STATE.md, SOURCES.md, function-register.md, hypotheses.md, known-facts.md, state-register.md, subsystems/README.md; ghidra/scripts/README.md.

New files: this audit, focused experiment report, evidence-index README, initial subsystem map, Ghidra Java reader/PowerShell launcher, xEdit README/two Pascal readers. The user-supplied brief was already untracked on entry and is included unchanged in the review package.

Open: complete ESM dependency graph/PKIN children, robot attachments, PEX equivalence, native key identity/layout, ownership authority, production scheduler, power propagation, serializer and save restoration semantics, loaded/unloaded behavior and precise live profile. Baseline is sufficient for this static pass, not authorization or complete readiness for a probe. First-publication scope/rights review still required. Recommendation is SOR-EXP-0002's minimal membership/no-action/reload case, not immediate deployment.

The local review package contains a combined Git patch including untracked files plus exact status and changed-file inventory. It excludes raw local evidence and uses Git-generated patch bytes; nothing was staged. Suggested commit after critical review: `docs(research): map initial outpost system`. Optional separate policy commit: `docs(policy): define bounded crash-tolerant captures`.

## Final repository checks

Checked all 27 changed/new files, including the unchanged supplied brief: UTF-8 decoding and local Markdown link targets passed; authored files use LF without BOM. Four pre-existing links to absent `docs/GIT_SETUP.md` were corrected or explicitly marked historical, preserving their provenance. External source URLs were consulted during research; this local link check does not prove their future availability.

`git diff --check` passed for tracked changes; separate new-file checks passed for authored additions. The unchanged supplied brief has four existing two-space Markdown hard breaks (lines 3–6) flagged as trailing whitespace; these are preserved and are the only new-file whitespace exception. Independent callback/registration operand checks passed; both installed xEdit helpers match repository bytes. The index is empty, LICENSE unchanged, and sampled private artifacts are ignored. Tracked/proposed file-extension inventory contains no proprietary binaries, script sources, saves or databases. Exact status and combined tracked/untracked patch are in `.local-work/reviews/initial-reconnaissance-status.txt` and `.local-work/reviews/initial-reconnaissance.diff`; the changed-file inventory accompanies them. These checks establish repository hygiene and the stated static anchors, not runtime semantics or independent critical approval.
