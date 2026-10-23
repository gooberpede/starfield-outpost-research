# Codex implementation brief — RG2-C2A
## Carinae III-a native Iron-region observation: Phase A implementation and qualification

**Project:** `D:\Projects\starfield-outpost-research\` (`gooberpede/starfield-outpost-research`)  
**Authority:** Phase A only — offline analysis, adapter implementation, synthetic execution and approval-ready run card. **No Starfield launch, attachment, live instrumentation, new live saves, or Phase B/C execution is authorized.**  
**State:** Maintainer-approved scope; acceptance criteria AC1–AC8 frozen before implementation.  
**Scientific priority:** Resolve the Carinae III-a Iron mismatch without fitting assumptions or disturbing the established Feynman V correspondence.  
**Publication:** B6 remains on hold.

## 1. Context and evidence to inherit

Read `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md`, and `docs/reviewers/research-completion-reviewer.md` before implementation. Honor their source, preservation, delivery, independent-review and finalization rules. Do not treat this brief as permission to change frozen criteria, modify source games/saves, stage or commit.

Reuse, rather than repeat, the established scientific and engineering work in:

- `docs/experiments/resource-geometry/` (RG1 native generator and evaluator), `docs/experiments/resource-geometry-live-prep/` (case identities and frozen baselines), `docs/experiments/resource-geometry-mature-context/` (mature context and F1 reconciliation);
- `docs/experiments/resource-generation-ancestry/` (C1F), `docs/experiments/resource-selection-operands/` (C1G), and `docs/experiments/resource-installed-settings/` (C1H settings-resolved replay);
- `docs/experiments/resource-geometry-observation/`, `docs/experiments/resource-region-ancestry/` (C1E collector and observed regions), `docs/experiments/resource-oracle-retail/` (C1D identity/save preflight), and associated original `research/` code;
- prior save, source-selection, biome, region-lifetime and disappearing-deposit research, only insofar as it resolves a concrete dependency.

Pinned installed game: `Starfield.exe` **1.16.244.0**, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. Existing installed-definition pins and source ledgers control their own identities; verify rather than guessing. Preserve all existing RG1/RG2 frozen predictions, C1E/C1G live receipts and independent native-path matches.

**Cases:** Primary is Save52 / HIST-0267, **Carinae III-a Rc Fe**, with saved Iron extractor and Workshop positively joined using existing identity evidence. Within the same evaluation, Alkanes and Rothicite are controls where available. **Feynman V Cu Co Ni IL** remains an offline regression control, not a second mandatory live site. Feynman VIII-b stability/bug reproduction and the other Feynman V site are out of scope.

C1H's Carinae replay currently yields **895 paths** (Iron 259, Alkanes 505, Rothicite 131), unchanged by installed inactive-setting correction. It predicts no Iron region intersecting nominal territory despite the existing saved Iron extractor and gameplay evidence. Treat those as different evidentiary domains, not proof that native generation is wrong. The outpost is a single-biome site, but don't equate beacon biome with the selected source's effective BIOM/RSGD without observation.

## 2. Objective and work plan

Implement and synthetically qualify a **Carinae-specific extension** of the already functioning external native region collector. Prefer reuse of C1E's region-ancestry and C1D's Workshop-bound spatial-transfer methods. The planned, separately authorized Phase B should capture the **actual native Iron region accepted by the Carinae outpost area query**, with source identity and query parameters; collect Alkanes/Rothicite controls as naturally available.

1. **Offline case and ancestry preparation.** Verify original Save52 SHA, Workshop identifier, beacon/extractor tokens and definitions against established primary evidence. Map the qualified saved identities to the specific runtime join that the collector must witness. Do not manufacture a runtime FormID/handle mapping from saved tokens or identify by resource name alone. Record the exact predicted Carinae region populations, the saved Iron extractor position and query assumptions, and the versioned installed-settings baseline to be compared later.
2. **Trace the natural observation path.** Confirm guarded retail sites, register and object layouts for area updater, accepted/rejected region callbacks, source-wrapper/slot identity and spatial transfer. Reuse C1E where exact native semantics carry over; any change requires source-backed rationale and guards. Identify a natural Carinae trigger through ordinary Save52 travel/build-mode actions and an independent Workshop identity check. No forced source/cache regeneration.
3. **Implement collector extension.** Capture actual reference/Workshop identity, exact area XY/radius/upper, spatial source slot and wrapper, IRES identity, complete native region bound, point count and ordered XYZ/width bits, accepted/rejected decision and exact spatial-transfer membership. Preserve the distinction between observed accepted region, callback's final return, shared cached list and catalogue outcome. A pre-install transfer is not a completed cache install. Track thread/invocation ancestry, source-slot scope, and lost/truncated/invalid samples. Don't infer the generation epoch from a consumer pointer or digest.
4. **Qualify synthetically.** Run the real Windows debugger against controlled source-shaped fixtures exercising at least: positively bound Carinae-like Workshop/Iron region; Alkanes/Rothicite control; wrong Workshop and wrong cell; accepted singleton and multipoint paths; skipped or short-circuited regions; nested/threaded invocations; invalid pointers/counts; source-slot reuse; partial read; loss accounting; durable ACK before controlled exit; crash before/after receipt; no-hit/retained-cache result. Verify no source-specific IDs are silently hardcoded into a generic decoder. Retain prior regression coverage from C1C/C1D/C1E/C1G where relevant.
5. **Prospective comparison contract.** Implement or prepare a nonfitting comparator that checks native point and bound bit patterns against the immutable installed-settings prediction, with separate results for source/frame identity, geometry equality, region-intersection/classification, and coverage. A positive single region does not establish a complete region census; do not treat missing events as absence. Preserve Feynman exact matches as a hard regression gate for any shared code or algorithm changes. **No changes to the shared generator or to frozen predictions are authorized simply to fit Carinae.**
6. **Approval-ready run card.** Prepare one finite Phase B session and its Phase C offline interpretation, but do not perform either. Include exact build/source pins, commands, identity/guard checks, user actions from Steam launch through Save52 and Carinae, expected observations, positive/negative controls, finite stop conditions, event-budget and loss handling, no-hit contingency, diagnostics, controlled exit and postflight audit. Any retry or change of target requires a reviewed card and fresh authorization.

## 3. Operational authority and save integrity

**Authorized now:** Existing-repo read-only research and evidence review, original analysis/code changes within the approved scope, local build, synthetic/disposable target execution, independent reviewer work, and preparation of a run card. Original inputs, existing local receipts, installed game files and saved games remain read-only during Phase A.

**Not authorized now:** Starfield launch or attachment, native retail pilot, forced generation/cache invalidation, creation or modification of gameplay saves, altering installed definitions/settings, code injection into Starfield, publication, staging, commit or push. Return Phase A to the maintainer for approval before any Phase B retail operation, even if independent review says ACCEPT. A successful synthetic qualification is **not** live authorization.

For the future live run card, use the established standard: hash and verify live saves against independent protected backups **before** game launch; verify an actual recoverable backup and rehearsal of scratch restoration; account for autosaves and cloud-sync paths; record file additions/changes/deletions and hashes **after** exit; preserve changed files for diagnosis; restore from verified backup only under the approved recovery procedure, then rehash. Some risk to backed-up live saves is acceptable; risking the sole recoverable copy is not. Post-capture game instability or controlled process termination is acceptable after externally verified durable evidence. Evidence integrity and correct site association are mandatory.

## 4. Scientific decision table for a future capture

- **Observed native Iron region, geometry absent/different offline:** Trace selected source/frame, BIOM/RSGD, mask, effective settings and then generation inputs; no arbitrary fitting.
- **Native Iron geometry matches but offline area consumer misses:** Investigate actual query operands, native spatial predicate and association rather than changing the generator.
- **Native Iron and expected context differ:** Localize earliest source-selection/context discrepancy and verify independently before adopting a correction.
- **No observed generation but valid accepted cached region:** Preserve useful consumer evidence; historical generator inputs/epoch remain UNKNOWN.
- **No qualifying Iron event or unbound Workshop:** Preserve as no-hit/identity failure, not native absence; apply the bounded contingency and propose a specific mitigation.

## 5. Frozen acceptance criteria

- **AC1 — Authority, baseline and preservation:** Exact project/target/version/source pins; no retail execution; verified protected save/evidence/prediction and HEAD/index integrity; clear scope and permissions.
- **AC2 — Carinae identity and ancestry:** Precise Save52 Carinae Workshop/extractor/source binding plan, without extrapolating saved tokens to native handles.
- **AC3 — Implemented native geometry collector:** Working guarded Carinae observation extension capturing native regions, query coordinates and source membership with explicit status and loss semantics; not merely a design report.
- **AC4 — Synthetic qualification:** Executed real debugger/fixture trials for positive, negative, threading, identity, partial/corrupt and durable-exit cases; inherited regressions checked.
- **AC5 — Comparison discipline:** Immutable installed-settings baseline and Feynman regressions preserved; reproducible exact, nonfitting region comparator and explicit scientific coverage limits.
- **AC6 — Approval-ready retail procedure:** A fully specified one-session Carinae Iron Phase B card, with Alkanes/Rothicite controls, preflight, stop criteria, no-hit mitigation, postflight and Phase C comparison. **No Phase B/C execution.**
- **AC7 — Reproducibility and durable records:** Original code and research documents, source/receipt lineage, commands, tests, failures and uncertainties; exclusions for protected raw data/binaries; editorial finalization performed.
- **AC8 — Independent critical review and exact delivery:** Independent reviewer audits AC1–AC7, scientific and engineering claims, genuine test results, actual final changed text and patch coverage; deliver complete and task-only exact diffs plus manifests/hash checks, with no staging/commit/push.

All eight criteria are mandatory; passing other criteria cannot compensate for a failure. An unresolved scientific cause is permitted during Phase A; an unimplemented instrument or missing executable-in-principle live card is not.

## 6. Mandatory editorial finalization and independent review

Apply the now-durable `docs/EDITORIAL_STANDARD.md` to **every changed prose file**, including tables, captions, index entries, final summary and review artifacts. Run `research/editorial/screen.py` (or its current repository-authoritative equivalent) and relevant regression fixtures; document exact commands, findings and dispositions. Read the complete changed prose manually. Check run-together words/numbers, encoding/Markdown problems, ambiguous offset/VA/RVA/FormID/saved-token/source-index notation, and inadvertent strengthening of scientific claims. Use conventional `0x` notation; avoid redundant `(decimal)` labels or unnecessary conversions. False positives require reasoned disposition, not blind rewriting.

The independent reviewer must explicitly sign off on the **exact final changed-text snapshot**, including an editorial/notation check in addition to the technical AC matrix. Material defects require REWORK. Any later changes require an appropriate independent delta review before producing the final package. Preserve historical failures and earlier reviews; do not silently rewrite evidence or prior research conclusions.

## 7. Delivery and stopping rule

Return an independently reviewed Phase A package comprising the collector/code, synthetic results, report and evidence ledgers, **approval-ready Phase B run card**, prospective Phase C comparison contract, explicit risks/unknowns, complete/task-only verified diffs and manifest with exclusions. Provide exact target/build hashes and commands, no unsupported game execution claims, and separate scientific versus engineering dispositions. The final answer should prominently state **`PHASE B NOT EXECUTED — MAINTAINER APPROVAL REQUIRED`**.

Do not stop at another feasibility-only memo. If a specific engineering route fails, document the tested failure and an actionable, bounded mitigation or alternative within the approval boundary. If the scope must materially change, escalate rather than silently extend authority.
