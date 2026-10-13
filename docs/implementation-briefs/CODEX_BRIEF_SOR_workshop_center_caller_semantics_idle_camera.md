# Codex Research Brief — Workshop Center Caller Semantics, Idle-Camera Hypothesis and Coordinate-State Invariants

**Project:** `D:\Projects\starfield-outpost-research`  
**Task:** Offline native research and evidence reconciliation  
**Starting point:** Committed and synced cross-session center analysis (0.5.0 and 0.6.0)  
**Authority:** Offline/read-only analysis and authored analysis tools/docs only. No Starfield launch, game process access, SFSE build/deployment, debugger attachment, save modification, staging, commit or push.

## 1. Purpose and scientific question

Determine what the observed Workshop-center callers **actually do**, which native reference coordinate state each observes, and whether the contrasting 0.5.0/0.6.0 values reflect distinct coordinate frames, reference lifecycle stages, observational selection, timing interference, or another evidenced mechanism.

Test the user's hypothesis that the automatic idle/free-camera mode could explain the high-frequency observations, **without assuming that high frequency implies camera activity**. Preserve the gameplay constraint that outposts, terrain geometry, rocks, trees and resource locations appear stable across visits: distinguish deterministic physical placement from its potentially frame-dependent numerical representation.

Do not presume there is one globally immutable native XYZ, but do not invoke coordinate-frame conversion without tracing an actual contract, producer, transformation or consumer either.

## 2. Baseline facts and research discipline

Start by reading the repository's current `WORKFLOW.md`, completion protocol, prior briefs, frozen predictions, research reports, and source/evidence inventories. In particular, locate the sealed 0.5.0 and 0.6.0 raw captures and their independent decoding tools. **Do not rely solely on previous report summaries.** Establish and hash-pin the actual inputs and identify version-specific observation schemas.

Previously reported observations to verify from primary evidence:

- 0.5.0: forty Workshop grid observations associated with `AD0C36` during the new-landing/return sequence; sampled native Workshop center Z approximately `+3.643147` (SOR-002) and `-9.516418` (SOR-003), contrasting with serialized Z approximately `+18.352507` and `-31.890842`.
- 0.6.0: saved XYZ, sampled reference XYZ and ordinary Workshop-center XYZ agree in coherent samples; approximately 16,824 center calls attributed to `F4A1D4` and two to `F498F1`; no observed `AD0C36` despite hook coverage; distinct Save25 local-travel sequence.
- Different own-cell availability and incomplete 0.5.0 `+0xD3` coverage; previous work has *not* proven the cross-session transformation or causal observer effect.
- Position model contains **23 frozen predictions**, which must not be rewritten or silently recalibrated.

Treat all those as claims to independently confirm, correct or qualify. Do not confuse native RVA with live VA; own-cell/world with query-source world; saved identity with runtime pointer; apparent source-value Z with terrain elevation; journal append order with cross-thread execution order.

## 3. Workstream A — native caller and consumer semantics (mandatory)

Reconstruct the native caller and relevant call-site dependencies for:

- `F4A1D4` and `F498F1` (the dominant 0.6.0 center-call sites);
- `AD0C36` (the 0.5.0 terrain-query Workshop callback);
- shared Workshop-center helper `F4AB80` and the immediate consumers of its XYZ/radius results.

For each, establish as far as source permits: enclosing native function and callers, arguments/eligibility, invocation cadence, whether output is used for Workshop boundary/proximity, terrain-query inclusion, visibility, presentation/camera handling, or another purpose, and the coordinate/frame assumptions evident in the consumer. Follow real dependency leads rather than stopping at the first unresolved indirect call. Record native disassembly spans and source provenance in a durable ledger. Assign confidence separately to proven path, inferred purpose and unobserved runtime activation.

Explicitly test whether a consumer expects serialized/local reference XYZ, transformed/activated-cell XYZ, or another frame, and whether the native APIs encode the required frame identity. If native code does not establish a contract, mark it unresolved; do not substitute an architectural story.

## 4. Workstream B — raw event chronology and idle/free-camera hypothesis (mandatory)

Re-decode both sessions independently enough to reproduce caller counts, center operands/results, identity fields, compensation and relevant frame indicators. Analyze:

- per-caller event intervals and frequency distributions, bursts, gaps and changes over time;
- thread identities and nested/queued ancestry where captured;
- documented operator-action timestamps, loading, travel, idle intervals and STOP/retirement;
- whether the frequent 0.6.0 calls plausibly form a regular update loop;
- whether documented periods of inactivity correlate with caller changes;
- whether static caller ancestry reaches idle camera, visibility, scene update, Workshop proximity or another actual subsystem.

**Idle-camera verdict categories:** supported connection / contradicted within observed scope / not distinguishable. Do not conclude that the camera activated if its activation was not recorded. Avoid claims that a camera caused XYZ mutation without a native dataflow linking camera operation to reference writes.

Provide a reproducible chronology/frequency artifact (CSV or JSON plus a concise reader-friendly table), recording timebase, clock normalization assumptions and capture gaps. Distinguish observed timestamps from operator recollections.

## 5. Workstream C — coordinate-state invariants and observer effects (mandatory)

Compare like-for-like raw snapshots and code paths; identify what comparison is and is not possible because of different gameplay triggers, observation boundaries, reference lifetime and frame coverage. Audit:

- native reference XYZ provenance and the effect of `+0xD3` where established;
- reference own-cell/world versus query-source hierarchy; reference-load, conversion and restoration dependencies;
- Workshop relocation compensation versus reference coordinates;
- differences in 0.5.0 and 0.6.0 CALL/vtable patch coverage, wrappers, ABI preservation and snapshot timing;
- possible sampling bias, scheduling perturbation and semantic instrumentation interference, separately, requiring evidence for causal assertions.

Determine whether any recovered native transform could map the two sets of XYZ while preserving the outposts' physical relationships to stable terrain. If recovered operands are insufficient, furnish precise missing dependencies/observations, not a fitted arbitrary offset. Reconcile all native values against immutable saved-control data without altering frozen expectations.

## 6. Specialist and independent review

The primary Codex agent owns raw-capture chronology, integration, deterministic checks and final scientific result. **Use the specialist sub-agent for an independent static caller/coordinate-contract and idle-camera dependency audit**, with separate source references and counterexamples; the specialist should not simply paraphrase the primary agent. In the final package include a concise, evidence-based assessment of what the specialist discovered, disproved, corrected or materially accelerated.

The independent reviewer examines the original acceptance contract, actual raw evidence/decoders, native source spans, chronology tests, attribution of claims and completion status. It returns **ACCEPT / REWORK / ESCALATE**, and any REWORK must be addressed in the *same assignment*. The reviewer is established practice; do not devote routine prose to re-evaluating its general usefulness. **At most two concurrently active sub-agents** (reviewer plus one specialist), excluding primary Codex.

## 7. Deliverables and acceptance contract

Deliver, in durable repository documents and reproducible offline tools where useful:

1. **Scientific report** that answers the central question and treats alternative hypotheses fairly.
2. **Native caller/dependency ledger**, mapping each observed call site to sources, consumers and coordinate/frame assumptions.
3. **Cross-session chronology and frequency analysis**, including testable assessment of idle-camera hypothesis and its evidentiary limits.
4. **Matched-state and observer-interference comparison**, with explicit alternative hypotheses, counterexamples and unresolved joins.
5. **Decision-ready next-acquisition assessment**: smallest specific missing native observations, which natural trigger would supply them, and whether further live capture would materially improve durable-position validation. Do not automatically commission an observer.
6. **Tests and acceptance matrix**, protected-input checks, specialist contribution record, reviewer verdict and provenance updates.
7. **Review diffs** in `.local-work/diffs/`, clearly tagged `-complete.diff` and `-task-only.diff`, including untracked new text, plus changed-file manifest, status and patch verification.

Two scientifically legitimate completed outcomes:

- **A — Supported explanation:** Actual native path/state evidence establishes why the captured caller contexts differ and what their XYZ values represent. Include a deterministic transformation only when supported and independently checked.
- **B — Completed evidence-bound result:** Exhaust the authorized source/capture dependencies sufficiently to distinguish what is known, rule out or qualify hypotheses, and identify exact missing observations and their discriminating value. A generic “requires another live test” is not completion.

Do not invent elapsed-time, evidence-volume or monitoring quotas. Retain minimum **40,000,000,000 caller-available bytes** on *both* C: and D: for substantial local processing, preservation of protected saves and all frozen inputs, and genuine machine-integrity stop conditions. In-scope test failures or difficult native dependencies are work to resolve, not final handoffs. A real authority/safety blocker must be specifically evidenced.

## 8. Explicit boundaries

- **Offline only:** no Starfield launch/load/attach, no live process reads/writes, no plugin implementation/deployment, no new saves or console actions.
- **External debugger approach remains closed.** Do not reopen it.
- Preserve all sealed capture files, previous report verdicts, 23 frozen predictions and protected save/ESM inputs; original raw material stays local, ignored and out of review patches.
- Public source consultation, if useful, obeys project permissions, source revision, attribution and third-party reuse requirements. Do not copy third-party implementation without permission.
- No staging, committing or pushing.
- Finish scientific analysis and independent review before final handoff; mere postflight/packaging is not the research result.

**Expected handoff:** A conclusive offline, evidence-grounded understanding of the observed caller frequencies and the limits of coordinate-state equivalence, or a fully investigated and independently accepted evidence boundary with a precise next scientific decision.
