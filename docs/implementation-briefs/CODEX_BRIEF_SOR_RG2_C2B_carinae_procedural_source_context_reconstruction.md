# Codex implementation and research brief — RG2-C2B

## Carinae procedural source-context reconstruction

**Project:** `D:\Projects\starfield-outpost-research` (`gooberpede/starfield-outpost-research`)

**Authority:** **Phase A only — offline investigation, analytical implementation, synthetic qualification, documentation and independent review.** No launch of, attachment to, or other live operation against `Starfield.exe`; no live capture, forced regeneration, save modification, staging, commit, push, release or publication. If live evidence proves necessary, return a finished implementation and run card for explicit maintainer approval before Phase B.

**Baseline:** Retail `Starfield.exe` 1.16.244.0; retain the project's existing executable, installed-definition and evidence hash pins. Follow `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/PERMISSIONS.md`, `docs/reviewers/research-completion-reviewer.md`, `docs/templates/completion-contract.md` and the third-party policy. These documents control in case of conflict. Freeze AC1–AC8 below before work.

## Research question and established evidence

Why do the three native resource regions accepted during the **Save52 / Carinae III-a Rc Fe** evaluation fail exact comparison against the existing installed-settings offline geometry, when the Feynman V reconstruction has four exact accepted-region matches?

Relevant accepted Carinae observations from RG2-C2A Phase B/C:

- Positively bound Workshop identifier `91bac704da9b1e34` and spatial transfer; three accepted regions: **Iron** (two-point path), **Alkanes** (singleton), **Rothicite** (two-point path). The observed region/source attribution is **consumption-time**, not a demonstrated generating source or epoch.
- The three accepted regions were associated with consumption-time source **slot 24** and observed source key/wrapper in that evaluation; **none** exactly matches the offline region population for its resource, including comparisons of ordered XY/width. The 895-path installed-settings prediction consists of 259 Iron, 505 Alkanes and 131 Rothicite paths. A frozen 150-unit query assumption does not independently identify source-generation context.
- Independently reported and photographed visible connected deposit counts in this outpost: **two Iron, two Alkanes and one Rothicite**. Only **one Alkanes deposit has an extractor**. These are connected overlay deposits, **not counts of native region paths**; do not assume one path per deposit or infer exact geometry from pixels.
- Feynman V is a strong regression reference: the installed Exotic inactive chance multiplier `0.05`, rather than the executable initializer `0.01`, yields exact native accepted-region matches for IL, Copper, Cobalt and Nickel in the qualified comparison. Do not sacrifice those matches or refit the shared generator to make Carinae work.

Read before implementation: `docs/experiments/resource-carinae/{report.md,phase-b.md,phase-b-review.md,run-card.md}`, `docs/experiments/resource-geometry-mature-context/{prediction-contract.md,report.md}` where present, `docs/experiments/resource-geometry-live-prep/prediction-contract.md`, `docs/experiments/resource-geometry/{native.md,evaluator.md}`, `docs/experiments/resource-installed-settings/`, `docs/experiments/resource-region-ancestry/`, `docs/experiments/resource-selection-operands/`, `docs/experiments/resource-generation-ancestry/`, `docs/experiments/native-availability-map/`, plus their source ledgers and existing local primary receipts. Use actual repository paths where naming has evolved, recording any substitutions. Check the prior `starfield-resource-research` project only for narrowly relevant, attributable first-party material, without extending the scope into general ProcGen research.

## Required work — Phase A

### A. Freeze identities, comparators and competing hypotheses

1. Verify the exact native Carinae evidence and source pins without rewriting original receipts or frozen predictions. Record the different domains: saved beacon/Workshop identifiers; runtime reference/pointer; source slot; wrapper; manager owner/key; geographic source anchor; selected biome/RSGD; and epoch. A matching slot number is not a unique generating identity.
2. Establish an explicit, falsifiable comparison matrix for: (a) wrong source or source-frame association; (b) wrong manager owner or spatial packed keys; (c) effective BIOM/RSGD/family/mask or settings difference; (d) selected-source/region cache history; (e) a genuine shared generator implementation defect. Identify which existing evidence already excludes or supports each, without assuming all three resources share a generation epoch.
3. Keep native and offline geometry comparisons exact (original ordered binary32 points, widths and bounds), with a separate, clearly labelled spatial-consumer comparison. No free alignment or seed search to force a match.

### B. Recover source ancestry offline as far as the evidence permits

1. Trace the observed source slot 24 → wrapper/source key → manager/source-map and cached region objects using existing raw receipts, static native paths and source records. State precisely where that path ceases to identify a **generating** source.
2. Reconstruct the geographic source anchor/frame and the translation to the Carinae outpost frame from independently established native transformations. Test whether **one evidence-supported frame/source correction** accounts for Iron, Alkanes and Rothicite jointly. If only candidate transformations can be established, label them and do not promote them to facts.
3. Trace the effective generating BIOM, RSGD/DNAM, resource masks and ordering, owner key, source dimensions/padding, settings and potential predecessor competition. Distinguish installed values, derived static inputs, observed runtime operands and missing historical inputs. Verify which are invariant across the three observed resources.
4. Perform a bounded exact replay of independently justified candidates with the **unchanged** geometry algorithm and installed-settings resolution. Record the first differing input/decision where it can be established. No parameter fitting, arbitrary offsets, brute-force seeds or undocumented fallback to another biome.
5. Preserve and freshly run the Feynman four-region checks and relevant chance-stage regressions whenever shared code is touched. Preserve Carinae's existing 895-path baseline; any new prediction is a separately named and provenance-labelled version. The connected overlay count 2/2/1 is an independent qualitative constraint, not a fitting objective or proof of region census completeness.

### C. Engineer the narrow missing observation if offline reconstruction is insufficient

1. Identify the **smallest exact runtime operand(s)** preventing a decisive source join or replay. Prefer a targeted extension of the existing qualified external debugger controller over a fresh architecture. Candidate receipt fields include source-map lookup and wrapper lineage, native anchor/origin, actual BIOM/RSGD and resource mask, generator owner/packed key, producer invocation/epoch, and link from constructed regions to consumed region identity.
2. Implement the scoped adapter and synthetic test fixtures where it can be done offline. Qualify real debugger handling against disposable synthetic targets, not Starfield. Tests must cover wrong Workshop/source, source-slot reuse, stale or different producer epoch, bad/partial copy, multi-thread/nested events, short-circuit, event loss, and durable external ACK; do not invent coherency from a pointer, digest or timestamp alone.
3. If a natural producer event might not occur after Save52 is loaded, specify an actionable **no-hit fallback**, such as a different independently meaningful natural evaluation or a consumption-time source-identity capture. Do not force invalidation or manipulate source generation under this authority. Explain what each alternative can establish without pretending it proves historical ancestry.
4. Produce an **approval-ready, finite Phase B run card**: one explicit scientific discriminator; exact target/identity and breakpoint guards; launch/load/action/stop sequence; receipt contents, coherence checks and analysis; bounded attempts and reasons for stopping; proven save/back-up hash preflight, cloud/write-path checks, postflight and verified restoration method; disposable process risk; evidence flushing before stop. The card is **proposed only**. It must not grant itself execution authority.
5. If offline evidence resolves the discrepancy, an unnecessary live capture should not be implemented or proposed merely to satisfy a process step. Explain why live work is unnecessary and provide the reproducible exact replay.

### D. Durable records and scientific disposition

Create a cohesive experiment directory such as `docs/experiments/resource-carinae-source-context/` (follow established naming practices), with report, native/source provenance ledger, comparison matrix, reproducible offline outputs and tests, a run card **if required**, and review. Link from the experiment index and appropriate research-state navigation. Preserve old frozen records and scientific history. Distinguish **EXACT MATCH**, **CONDITIONAL MATCH**, **MISMATCH**, **UNKNOWN**, **NOT TESTED** and **INCOMPLETE**; separate research validity, engineering readiness and live approval. A null/missing region is not an observed empty population.

## Frozen acceptance criteria — AC1–AC8

**AC1 — Authority, integrity and provenance.** Verify pinned executable/definition identities and protected save/raw-evidence/frozen-model hashes; do not modify protected materials. No retail execution or save operations. Preserve HEAD/index and supply a concrete source/evidence ledger.

**AC2 — Identity and source-ancestry map.** Produce an auditable chain from the positively bound Carinae evaluation and consumed regions toward the native source wrapper, geographic frame and generating owner, with every join typed as observed, derived, candidate or unknown.

**AC3 — Joint-context discrimination.** Test whether an independently supported common source/frame/selection difference can explain **all three** observed resource mismatches. Explicitly address generation-versus-consumption identity and epoch, competing hypotheses and the earliest demonstrable divergence. Do not infer source identity or causality from shared slot 24 alone.

**AC4 — Exact, unfitted replay and regressions.** Re-run qualified Carinae comparisons and Feynman exact controls using the unchanged algorithm/installed settings; allow only individually evidenced counterfactuals. Preserve frozen predictions and report exact and incomplete coverage honestly. Include visible deposit counts as observational constraints without equating them to path counts.

**AC5 — Constructive acquisition outcome.** Either establish a supported offline explanation, **or** deliver a materially narrowed missing-observation contract and a working, synthetically qualified collector extension (where feasible), with actionable fallback for nonexecuting producer hooks. An unmitigated all-NO-GO or another generic feasibility report fails.

**AC6 — Complete, approval-ready live card where needed.** Specific identities, guards, preflight/backups, bounded natural action sequence, durable receipts, stop criteria, no-hit handling, postflight/restore and analytic discriminator are present. **Phase B remains unauthorized** pending separate maintainer review/approval.

**AC7 — Reproducible records and editorial finalization.** Provide tests, commands, input/output hashes and source pins, preserve intermediate failures and scope limits, update durable navigation. Apply `docs/EDITORIAL_STANDARD.md`: automated checker plus manual pass over **all changed authored prose** (including tables, captions, code explanations and navigation); address fused words/numbers, broken formatting/encoding, ambiguous hex/decimal, VA/RVA/offset/handle domains and scientific qualifiers. Conventional `0x` notation suffices; no gratuitous decimal labels or conversions.

**AC8 — Independent review and verified delivery.** Independent critic reviews original AC1–AC8, substantive scientific/engineering evidence and **exact finalized changed text**; REWORK on material deficiencies. Correct findings, rerun affected tests/editorial checks and obtain scoped delta review of post-acceptance edits. Supply complete/task-only patches, exact hashes/manifests, forward/reverse applicability evidence and a PASS/FAIL/NOT TESTED matrix. No staging, commit, push or release.

## Completion contract and return format

Follow `docs/templates/completion-contract.md` and `docs/RESEARCH_EXECUTION_PROTOCOL.md`, including the project's current independent reviewer invocation, preservation standards and mandatory completion. Include: concise best-supported scientific finding first; exact input/observation table with uncertainty; earliest discriminating stage or blocker; changed file manifest; test and editorial-screening results; final independent review and scope; full/task-only diff paths and SHA-256; explicit Phase B authorization status; recommended commit message. Evidence or review acceptance is **not** permission to execute the live run.

**Scientific stopping rule:** Do not pursue broad ProcGen reconstruction, arbitrary parameter search, or indefinite observer safety debate. Exhaust the bounded existing source-context evidence, establish the earliest responsible missing operand, and, only if needed, build the smallest qualifying acquisition. More screenshots or repeated menu confirmation do not satisfy the objective.

**Publication:** B6 remains ON HOLD. No third-party source, proprietary binary, protected save, raw debugger capture or other local-only artifact is to be copied into a public deliverable.
