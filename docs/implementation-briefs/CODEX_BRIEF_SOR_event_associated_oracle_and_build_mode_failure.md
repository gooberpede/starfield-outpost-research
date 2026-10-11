# Codex Research Brief — Event-Associated Position Oracle and Build-Mode Failure Investigation

**Project:** `D:\Projects\starfield-outpost-research`  
**Status:** new offline investigation and acquisition-design brief; **no live Starfield run, deployment, commit or push authorized**.

## 1. Objective and evidentiary baseline

Continue SOR-EXP-0022 after the reviewed Phase 1 observer 0.1.1 run. That run preserved 16 captures and found native workshop-center values sometimes matching the frozen SOR-002/SOR-003 predictions exactly, but the shared four-float result did not consistently refresh on site changes, and its radius remained zero. These are observations, **not** proof that the saved-position model is wrong, that the game used an invalid radius, or that the game has a boundary bug.

**Primary objective:** identify and prepare an acquisition method for **event-associated, independently engine-produced outpost-position outputs**. Recover the actual producer, caller/input identity, ownership/lifetime, execution conditions, frame selection and output values. Choose the best evidence-producing native oracle for validating the reconstructed durable outpost center and, ideally, the native terrain-grid position algorithm. Event-associated means a captured value is tied to a particular invocation and workshop/reference, not merely a stale shared buffer read afterward.

**Secondary objective:** investigate the observed zero radius and the intermittent build-mode *spinning/loading placement reticle* as falsifiable hypotheses. Establish whether they are connected, are unrelated, or remain distinguishable only by additional targeted evidence. Do not assume either a vanilla game bug or an observer defect at the outset. A solution to the intermittent UI bug is **not a prerequisite** for finishing primary oracle design.

Keep established outcomes separate:
- Saved beacon XYZ plus `ExtraWorkshop +0x60` compensation reconstructs the unchanged durable workshop center in Save25/Save26.
- The native four-float output has sometimes matched that result bit-for-bit, but Phase 1 demonstrated retained/stale states and radius zero; no qualified always-current oracle has been demonstrated.
- Native planetary-grid algorithm equivalence is still unvalidated. Exact continuous geographic longitude/latitude remains deferred rather than a new objective.

## 2. Research inputs and first actions

Read the latest committed project evidence and source before making assumptions, including `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, current research state, the SOR-EXP-0022 oracle contracts/frozen predictions, the Phase 1 results and live-session ledger, the workshop-origin native-consumer reports, and the latest static-exhaustion dependency ledger. Locate and reuse exact existing native function/register entries, addresses and pinned input identities; do **not** invent replacement RVAs from this brief.

The existing offline evidence includes Save25 (before beacon relocation), Save26 (after), prior nine-snapshot observer 0.1.0 evidence, Phase 1 sixteen-snapshot observer 0.1.1 evidence, and installed 1.16.244.0 executable/ESM/Ghidra analysis environment. Work from their established local/frozen manifests. Source saves and capture artifacts remain immutable.

Consult maintainer-authored `gooberpede/starfield-reference-handles` instrumentation as useful, with exact provenance. Maintainer-owned reuse requires provenance but no renewed authorial permission or self-credit. Material embedded from unrelated third parties remains subject to its own rights.

## 3. Primary track A — establish the workshop-center output contract

Trace the concrete typed four-float center/radius result **back to its producer and forward to the actual consumer**. Determine as far as statically possible:

1. Who owns and allocates the output storage? Is it a global, static, per-manager, per-workshop, short-lived scratch object or result cache? How is its lifetime/invalidation managed?
2. Which precise functions write **center XYZ**, **radius** and adjacent state/validity flags? Identify full writes, partial writes, zeroing and conditional skip paths. Do not equate a read site with the producer.
3. Which callers invoke those writers; what inputs identify the selected workshop, beacon/reference, world, cell, effective radius and coordinate frame?
4. Which callers/consumers actually use the calculated center for borders, bounds, placement, terrain coverage or other operations? Does the four-float memory location directly govern placement decisions, or is it only an intermediate output?
5. Examine the user's hypothesis of an **unmoved-beacon fast path**: with zero relocation compensation, could a consumer use the beacon's position directly without refreshing the shared result, while the nonzero-compensation path writes a calculated center? Test this hypothesis against static branches **and** both observed SOR-002 outcomes: the output sometimes remained SOR-003, but later did refresh correctly to SOR-002.
6. Distinguish a retained valid-but-unused result, an invalidated output with stale XYZ, keyed cache behavior, a read of an incorrect/reused pointer, and a genuine missed update affecting gameplay. Identify what evidence distinguishes these cases.

Produce a typed producer/consumer map, with relevant functions/RVAs, data-structure offsets, conditional branches and invocation triggers. Preserve contradictory paths rather than selecting a convenient explanation. A plausible buffer label alone is not an oracle contract.

## 4. Primary track B — evaluate the terrain-grid oracle

In parallel, revisit the existing native terrain-grid/activated-overlay selection oracle proposed during SOR-EXP-0022. Compare its **expected information gain and acquisition risk** with the workshop-center producer:

- Does it yield selected source world/cell/activated frame, translated durable center, integer grid indices, residual position or native post-quantization hierarchy on a single invocation?
- Where is it invoked under ordinary play/build mode/terrain queries, and which event reliably triggers it?
- Is there a practical association from each invocation to SOR-002/SOR-003 and to Save25/Save26?
- Can one small event-associated capture collect both center and grid results, or are separate collection mechanisms required?
- Would passive SFSE instrumentation, a narrow hook, hardware/software debugger tracing or another read-only observer be the most defensible approach? Base the choice on prior project experience, including the hardware-breakpoint `STATUS_SINGLE_STEP` failures during native-save tracing and the successful broad passive observer sessions. **Those save-path failures are not a blanket prohibition on debugger use.**

Prefer an event-associated trace of native-produced values over a second passive reading of the same retained global result. Do not select a fragile breakpoint mechanism without explaining why it beats alternatives. If a candidate path is not naturally invoked, distinguish that from an error in the offline reproducer.

## 5. Secondary track — spinning placement reticle and zero radius

The operator reports an intermittent Starfield outpost-build issue: placement preview/reticle indefinitely displays a spinning loading/waiting indicator and new objects cannot be placed; exiting and re-entering build mode may recover. This is gameplay testimony, **not** a captured occurrence in the Phase 1 session. In that session the observed four-float output radius remained zero even during user-reported functional build-mode entry. Therefore zero **in that buffer** is not by itself sufficient evidence of zero **effective placement radius** or of the bug.

Investigate with bounded but meaningful latitude:

- Trace preview initialization, asynchronous readiness, validation and placement gating; distinguish *pending/uninitialized* from *explicit out-of-bounds rejection*.
- Trace the actual effective boundary/radius source (including ordinary beacon `OutpostBuildAreaRadius` 150 native units and any fallback) and whether the four-float radius/validity fields participate.
- Determine whether zero radius is a sentinel/invalidated result, a real effective bound in some state, or simply a scratch-output convention.
- Look for conditions that can leave a loading preview unresolved and whether the user-visible workaround (exit/re-enter) resets relevant state.
- If evidence suggests a concrete engine bug or a shared root cause with stale-center behavior, describe the exact executable path and testable prediction. Otherwise record the two issues as distinct.

This research can follow promising relevant call chains without arbitrary function-count/time caps, but avoid turning the main task into a general catalogue of outpost defects. Preserve potential leads for later work.

### Prior art and permissions

Review **Starfield Engine Fixes — SFSE**, by LarannKiar, at https://www.nexusmods.com/starfield/mods/10457, including accessible changelogs and technical descriptions. Publicly visible version 21.2 (October 2026) documents a fix for its own optional Traversal Stutter beta feature interfering with floating placement-preview appearance, and older versions introduced optional build-placement/rotation features; **these do not by themselves prove a fix for the vanilla spinning-reticle bug**. Also examine credible reports of the issue, including https://steamcommunity.com/app/1716740/discussions/0/3824173836668691935/ and other relevant firsthand evidence. Distinguish original author reports, mod-specific regressions, vanilla observations, community speculation and your own independently verified native findings.

Follow `THIRD_PARTY_POLICY.md`, `docs/SOURCES.md`, `docs/PROVENANCE.md` and existing permission records. Document author, URL, version/date, access status and exact claim used. Do not assume third-party source/code-reuse permission; do not incorporate binaries, unpublished code or third-party implementation without the required permission decision. Source inspection/attribution does not amount to engine validation. If a page is inaccessible, record that limitation rather than inventing contents or repeatedly wasting time on blocked access.

## 6. Required oracle selection and acquisition proposal

Return a **ranked, concrete acquisition design** for the next live experiment, justified by native source evidence and observed Phase 1 behavior. For each viable candidate specify:

- function and exact pinned-build address/RVA; inputs, outputs and typed ownership;
- trigger condition and how to tell a fresh invocation occurred;
- how workshop/reference identity is associated independently of numerical center equality;
- coordinate-frame qualification and expected native results;
- instrumentation mechanism, execution/thread context and crash/detach exposure;
- expected raw evidence (entry/return, register/stack or typed payload, timestamps, TID, caller, associated reference, validity and radius);
- implementation steps and disposable/offline qualifications needed;
- what the candidate can independently validate, and what it **cannot** validate.

**Do not conflate the workshop-center oracle with planetary-grid equivalence.** Prefer a combined capture when feasible, but do not introduce fragile instrumentation simply to combine unrelated events.

Frozen comparisons from the existing SOR-EXP-0022 validation protocol must not be rewritten after inspecting oracle outputs. For same-frame binary32 center predictions require the precommitted exact-byte criterion; for grid/frame operations define comparison precision and inputs **before** live measurement. Conditional/stale/unassociated values are not a pass and are not evidence that the offline algorithm is wrong.

## 7. Autonomy, continuation and stop rules

You are authorized to conduct extensive **offline** static analysis with installed Ghidra, PE/native analysis, xEdit/ESM inspection, saved captures, numerical experiments, original scripts/tests and read-only local evidence. Extend research scripts where helpful; investigate indirect calls, relevant type constructors, state transitions, alternatives and counterexamples. Pursue fruitful detours rather than stopping at the first partial interpretation.

Maintain an auditable dependency/lead ledger. For each primary unresolved producer/consumer path, end with **RESOLVED**, **DISPROVED/IRRELEVANT**, or **SPECIFICALLY BLOCKED** and supporting evidence. “Strong partial”, complexity, or an unexplored plausible call path are not terminal reasons to stop. Do not demand proof of the absence of every possible function in Starfield.exe; demonstrate exhaustion of the investigated expanding dependency graph and specify any genuinely runtime-only dependency.

Do not launch Starfield, alter the Vortex deployment, build or deploy a new live plugin, attach a live debugger, inject hooks, change saves, or begin a new gameplay experiment under this brief. The prior observer 0.1.1 is currently undeployed. Any proposed instrumentation implementation or live run is subject to a subsequent reviewed authorization. **This brief authorizes research and an acquisition design, not live execution.**

For future instrumentation recommendations preserve the established policy: favor evidence-rich capture without arbitrary small count/time/volume quotas, keep the **40,000,000,000-byte free-space guard on relevant C: and D:**, continue through isolated unreadable/unknown scientific observations, and stop only for genuine instrumentation-integrity/machine-safety failures. Scientific completeness and observer health are separate outcomes. Preserve input hashes, file provenance and ignored scratch artifacts.

## 8. Deliverables and success criteria

Create a durable report and supporting research records consistent with current project conventions. Return:

1. **Answer first:** best-supported diagnosis of stale center/zero radius and confidence/coverage.
2. Native four-float buffer allocation/ownership, writer, clear/invalidation and consumer contract, including the unmoved-beacon fast-path hypothesis and its counterexamples.
3. Comparison of center-output versus terrain-grid oracle information gain and acquisition reliability.
4. Build-mode placement-preview state-machine findings and falsifiable assessment of zero-radius causation versus unrelated initialization failure.
5. Reviewed prior-art claims and provenance, distinguishing Engine Fixes optional-feature regressions from vanilla symptoms.
6. A **ranked event-associated oracle acquisition design**, with addresses, inputs, triggers, identity/frame/freshness evidence and exact comparison protocol.
7. Dependency ledger and concrete unresolved static/runtime joins.
8. Any proposed changes to the standing findings/state registers (no unsupported promotion).
9. Files changed, scripts/tests and results, input integrity checks, `git diff --check`, link checks and `git status --short`.
10. Complete task-only and cumulative review diffs, if generated; no staging, commit or push.

**Research success** means a credible, event-associated oracle contract and implementable acquisition plan supported by traced native paths, plus an evidence-based disposition of the zero-radius/build-mode bug hypotheses. A meaningful secondary bug result is valuable but must not block completion of the primary positioning-oracle work. If a native operation cannot currently be instrumented or uniquely qualified, identify the exact mechanism and most discriminating next observation—not merely another generalized recommendation to “run a debugger.”

Suggested later commit subject (only after critical review):

```text
research: map event-associated position oracles and build-mode state
```
