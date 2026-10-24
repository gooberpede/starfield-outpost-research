# Codex implementation brief — RG2-D4: Native Resource-Selection Context Acquisition

**Project:** `D:\Projects\starfield-outpost-research\` / `gooberpede/starfield-outpost-research`  
**Authority:** Phase A only — offline investigation, implementation, and synthetic qualification. **No Starfield launch, retail attach, live sampling, save creation, or installation changes under this brief.**  
**Status:** Proposed assignment; freeze AC1–AC8 upon invocation.  
**Priority:** Scientific discrimination and reproducibility, not performance, publication, or Outpost Tracker integration.

## 1. Purpose and governing evidence

RG2-D2 and RG2-D3 tested the standalone geometry predictor across Save52. D3 increased independently corroborated ordinary resource/extractor associations from 16 to 25, leaving **one potential false negative (Archimedes III Tungsten)** and **nine indeterminate ordinary resource associations**: seven attributed to first construction-query resource-mask uncertainty and two to alternate-component descriptor precedence. Seven native region controls from Feynman V and Carinae III-a remain exact.

The maintainer's new Archimedes III gameplay screenshots independently show **one visible contiguous Tungsten deposit**, **several separated Chlorine deposits**, and **both terrestrial Water and atmospheric Water Vapor extractors**. Visible deposits are not necessarily single generated paths. Terrestrial and atmospheric Water are different admission mechanisms and must not enter the finite-vein score. Existing installed extractor associations are historical positive witnesses, not complete inventory truth.

The currently qualified offline Archimedes context selects a Chlorine resource family through modeled `BIOM 0x0028acd1` / `RSGD 0x0037c66c`, omitting Tungsten. This may be a different effective biome/component selection, source-context/initialization difference, or historical cache state; do not assume a particular cause. Prior D1/D2/D3 predictions and native raw evidence are immutable controls.

**Central question:** What effective native biome, component/descriptor, resource-family and construction-query mask does Starfield select for the source that supplies the Archimedes Tungsten vein, and how can those operands be captured with correct ancestry? Also design reusable operand acquisition for the remaining Feynman mask and descriptor-order cases.

Start with the repository's current authoritative evidence, especially:

- `docs/experiments/resource-save52/` and `docs/experiments/resource-save52-d3/` (frozen roster, discrepancy classifications, prospective acquisition card, if present);
- `docs/experiments/resource-standalone/` (algorithm, corpus schema, predictor, seven controls);
- `docs/experiments/resource-selection-operands/`, `docs/experiments/resource-carinae-source-context/` and `docs/experiments/resource-region-ancestry/` (working collector and verified native chains);
- prior native source maps and acquisition contracts (`docs/experiments/native-availability-map/`, `docs/experiments/resource-geometry/`);
- `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/PERMISSIONS.md`, `docs/templates/completion-contract.md` and the independent-reviewer procedure.

Use actual filenames discovered in the repository where these references differ. Do not invent source locations or claim a historical callback association that the evidence does not show. Native claims are pinned to `Starfield.exe` **1.16.244.0**, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.

## 2. Mandatory scientific design

### Track A — Archimedes III Tungsten versus Chlorine

1. Trace the **actual native producer/selection path** for source BIOM choice, component choice, effective RSGD/DNAM, selected resource family and descendants, source identity/frame/owner, and ordinary mask/weight/order. For each operand identify the producer, native instruction/call boundary, register/member location and lifetime, provenance and evidence level. Avoid conflating saved biome, surface-cell BIOM, source BIOM and generating component.
2. Identify **which selection decision first disagrees with the frozen Archimedes prediction**, if determinable offline. Observe enough upstream causes to distinguish a different BIOM/component, a different family, nonuniform initial mask, cached historical source or generation-vs-consumption mismatch. Never classify the existence of an extractor or a resource UI label as generator provenance.
3. Provide a correct identity chain from Save52 Workshop and body through runtime reference, selected source, generator invocation and eventual accepted region/transfer **where evidenced**. If cross-epoch joining cannot be qualified, mark it UNKNOWN rather than correlate by pointer, resource label, proximity or timestamp alone.
4. Preserve Chlorine as the positive control, and preserve the screenshots as first-party observations, with no claim of exact polygon coordinates or native path count.

### Track B — Reusable Feynman selection operands

1. Capture the **initial construction-query position and its sampled mask**, distinguishing it from later per-cell, outpost-area or extractor-position queries; document spatial input units and coordinate domains.
2. Support the effective component/descriptor ordering decision for the unresolved Feynman III Uranium-family cases, including candidates and their precedence, rather than just reading one final RSGD pointer.
3. Design a single reusable collector schema with case-specific expected values, not several hard-coded site-specific breakpoint variants. These cases are **future acquisition targets**, not live visits authorized here.

### Track C — Replay and falsification contract

Before any prospective retail pilot, specify exact outputs from each capture and how to compare them against the frozen D2/D3 assumption: native selected identity, source/BIOM/component/mask/descriptor, chosen family and resource ordering, whether the event is generation or consumption, and separately witnessed region ancestry. Include opposing possible observations and their interpretation. If observed effective inputs permit replay, the subsequent offline comparison must use unchanged native-equivalent geometry logic, version corrections and rerun all seven exact region controls. No arbitrary seed, biome, source, weight, or geometry fitting to the known Tungsten outcome.

## 3. Working instrumentation — Phase A

Reuse/extend the already qualified C1G/C2B/C2A Windows debugging controller and receipt transport wherever possible. The deliverable must be **working code**, not merely native-location suggestions.

- Implement guarded observation of the requisite selection decisions and their effective operands; establish runtime relocation, instruction guards and native layout provenance. Avoid treating analyst names as exported engine APIs.
- Associate events across native call nesting, threads, source identities and operation contexts to the extent actually witnessed. Event missingness, alias uncertainty, retained cache state, source reuse and mismatched ancestry must be explicit.
- Use synthetic Windows targets exercising source/BIOM selection, alternate components, first-query nonuniform masks, multiple threads/nesting, bad pointers/counts, incorrect Workshop/source association, and partial captures. Require cross-process acquisition from target-owned memory (not fixture-provided answers) where the architecture calls for it.
- Use bounded checked reads, durable externally acknowledged receipts, verified framing/hash/readback and explicit LOSS/INVALID status; no false negative resource conclusions from missing events.
- Preserve immutable failed tests and diagnostic receipts. A tool that only replays the known offline source inputs without observing their native-selection provenance does not meet this brief.
- If a selected breakpoint architecture proves concretely infeasible, provide an independently tested or testably mitigated alternative; a blanket no-go without actionable mitigation fails.

A synthetic qualification demonstrates controller behaviour **only**. It does not establish historic Save52 source selection or grant live-test authority.

## 4. Phase B Archimedes run card — prepare, do not execute

Produce an actionable, approval-ready run card for **one initial Archimedes III session**, with Tungsten primary and Chlorine control. Include:

- exact target/game/plugin/build/configuration identity; observer build hashes, source instructions/register guards and tested decoder revision;
- Save52/body/outpost identity evidence, required movement/actions, natural source-generation or resource evaluation trigger, and evidence needed to claim a bound sample;
- realistic **no-hit/cache-hit** contingency: no callback hit is not resource absence. No forced regeneration/cache invalidation without distinct authority;
- first useful stop and evidence criteria, maximum prospective attempt envelope, no autonomous retries, explicit GO/NO-GO gates, loss/abort handling, evidence preservation and controlled target termination;
- **preflight and postflight** of protected saves and recoverable independent backups using the approved revised classification: named research, manual and quicksaves protected; confidently classified *active* exitsaves/autosaves are diagnostic-only; ambiguous files fail closed; historical backups remain protected. Steam Cloud/sync verification and scratch restoration rehearsal; actual restoration only under approved recovery procedure;
- distinction between session survival (expendable) and independent evidence durability (mandatory). Game instability or post-capture controlled crash can be acceptable after a complete verified receipt;
- exact offline comparison procedure and a prospective independent-review/interpretation route.

**Return the run card and engineering evidence to the maintainer for separate approval.** Neither Codex nor a reviewer may treat Phase A acceptance as approval to launch Starfield, attach to its process or take new saves.

## 5. Frozen acceptance criteria (AC1–AC8)

| Criterion | Mandatory evidence |
|---|---|
| **AC1 — Authority and preservation** | No retail execution; pinned inputs, protected saves, previous receipts and frozen predictions unchanged; clearly scoped read/write operations. |
| **AC2 — Native selection lineage** | Source-backed producer/call-site/operand contracts for effective BIOM, component, family, construction mask, settings and source frame, with unobserved links explicitly separated. |
| **AC3 — Working collector qualification** | Functional extension and independent synthetic Windows debugger tests of actual memory acquisition, threading, partial/error cases and durable receipt transport. |
| **AC4 — Identity and coherence** | Evidence-based attribution to source/workshop/operation where qualified; no invented epoch joins, retained-state claims or source-id equivalence. |
| **AC5 — Scientific discrimination** | For Archimedes and the Feynman dependency classes, map candidate native outcomes to competing explanations and replay tests; do not merely reconfirm visible resource membership. |
| **AC6 — Phase B readiness** | Complete, guarded Archimedes run card including natural/no-hit behaviour, fresh save/backups/sync gates, evidence stopping and explicit separate live approval. |
| **AC7 — Durable reproducibility and editorial finalization** | Source pins, versioned implementation, commands, synthetic results, preserved failures, reporting and a manual+automated final editorial pass per `docs/EDITORIAL_STANDARD.md`. |
| **AC8 — Independent final review and delivery** | Independent critical reviewer verifies AC1–AC7, scientific vs engineering scope, exact final changed text, source/evidence preservation, editorial quality, and complete/task-only diffs with forward/reverse and hashes; ACCEPT/REWORK/ESCALATE unambiguously recorded. |

No mandatory criterion is waived because another passes. A discovery that renders an instrumentation target unnecessary can replace it only with independently verified upstream evidence that genuinely discriminates the specified cases; document and review any in-scope substitution. Leave unsupported branches explicitly unresolved rather than manufacturing a complete solution.

## 6. Finalization, packaging and reporting

- Apply the repository's standing workflow and original frozen completion contract; do not rewrite historical ACs or previous scientific decisions.
- Deliver a concise report with: observed/derived/unknown matrix; Archimedes hypothesis discriminators; remaining Feynman collection plan; controller and synthetic tests; Phase B card; actionable next step; exact provenance and coverage limits.
- Run the editorial screener on the **entire changed authored text**, manually read new/modified prose, clarify domains (FormID vs saved token vs runtime handle, static VA vs runtime address vs member offset; percentages vs multipliers; source anchor vs world position) without redundant conversions; fix fused words/numbers and encoding problems. Independent reviewer must read the final delivered snapshot. Any later change requires scoped delta review.
- Include only permitted original research/source/code in tracked diffs. Keep proprietary binaries, extracted corpus payloads, raw native captures, raw saves, private debugging receipts, locally built binaries and scratch artefacts under ignored local storage. Builder/predictor research code may remain tracked under existing policy; no publication decision is implied.
- Supply exact source hashes, commands and test counts, protected before/after receipts, all changed/new-file inventory, exclusions, verified **complete and task-only** patches with SHA-256, and independent verdict/acceptance matrix. No staging, commits, pushes, live tests, release, cleanup, or B6 activity.

**Expected handoff:** Phase A code and synthetic verification + reviewed Phase B card, followed by maintainer approval decision. Do not execute Phase B in the same assignment.
