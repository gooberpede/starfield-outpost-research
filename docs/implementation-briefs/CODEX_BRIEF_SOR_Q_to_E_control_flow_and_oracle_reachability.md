# Codex Research Brief — Native Candidate-Query Control-Flow Reconstruction and Oracle Reachability

**Project:** `D:\Projects\starfield-outpost-research`  
**Mode:** Offline research, deterministic analysis and tests only  
**Starting point:** Current committed/synced repository after SorNativePositionOracle 0.2.0 live attempt 02; **do not restart the investigation from scratch**  
**Authority:** Research and local, non-destructive analytical tooling. No Starfield launch, process access, new injection/hooking, save creation, deployment, staging, commit or push.

## 1. Mission and scientific question

The 0.2.0 live experiment captured **18 complete, naturally executing native candidate-query (Q) calls**, each returning the integer `1`, during the approved N1 Kreet landing interval. The instrumented enumeration (E), callback dispatch, workshop-center and terrain-grid sites recorded **zero events**. The earlier ordinary Save25/Save26 controls did not produce Q events. The event collector and its health checks yielded a defensible scoped capture, though the strict one-second external monitoring requirement failed; do not relabel that operational deviation as a pass.

**Reconstruct the native Q control flow and its downstream relationship to E sufficiently to explain the observations, determine the meaning of return `1` in this context, and identify the shortest defensible route to independent validation of the durable outpost-position algorithm.** Investigate whether E is skipped by a legitimate shortcut, a predicate, an alternative path, or another supported mechanism. Do not equate absence of an E event with proof that no enumeration of any kind occurred.

This is primarily a scientific explanation task, not a request to build new instrumentation. Failure of a hypothesis is an acceptable finished scientific result; unresolved, still-investigable dependencies are not.

## 2. Required starting evidence and preservation

Before analysis, inspect the existing committed documents, source, local evidence references and method contracts, including as applicable:

- `docs/experiments/native-oracle/continuation-020-live-attempt-02.md` and its independent review;
- the 0.2.0 acquisition/reachability design, run card, inspector and Q/E instrument source;
- locally retained original Q event journals, raw descriptor/argument snapshots, hashes, invocation associations, health counters and operator chronology;
- native function and caller analyses already documented for Q, E, C and relevant grid/position paths;
- `docs/experiments/durable-position-resumption.md`, the deterministic position-model sources, 23 frozen predictions and Save25/26/27/28 control provenance;
- `WORKFLOW.md` and the Research Execution and Completion Protocol.

Recover exact paths from the repository; do not infer them from this brief or manufacture missing records. Hash and preserve original evidence before deriving working copies. All raw saves, proprietary binaries, dumps, raw memory and bulky private evidence remain local/ignored. The earlier external software-breakpoint debugger path is **closed** and must not be revived.

## 3. Workstream A — Reconstruct the native decision tree

1. Identify the precise native Q function(s), instrumented CALL boundary/boundaries, callers, return paths and relationship to E. Verify version-specific RVA/VA identities from existing source and native analysis rather than assuming label meanings.
2. Trace the control-flow graph from Q entry through all reachable returns, and through any candidate-resolving, cached-state, terrain-overlay, hierarchy, flag or eligibility dependencies required to interpret these calls. Trace relevant upstream producers and downstream caller branches wherever needed for the explanation.
3. Recover the actual semantics of Q returning `1` (and relevant alternate values) from code and caller behavior. Distinguish a Boolean return from status or sentinel semantics; do not label it “success” or “failure” without proof.
4. Determine whether the instrumented E site is a mandatory consequence of any Q path, an optional nested operation, or a separate path; examine other enumeration/callback call sites where supported by static evidence.
5. Record exact predicates and operand provenance. Where a predicate cannot be evaluated from existing captures, explain which value is missing and why it matters. Do not infer a branch merely from the absence of downstream events.
6. Pursue legitimate offline hypotheses, counterexamples and alternate call paths to completion within this assignment; do not return a list of interesting uninvestigated leads as the result.

Produce a concise, source-addressed native dependency/decision-tree map, with confidence, coverage and known branch distinctions. Use deterministic executable probes or scripts where helpful, and test their arithmetic/decoding independently.

## 4. Workstream B — Reconcile all 18 observed invocations

Create a **per-invocation ledger** grounded in the raw recorded artifacts (not reconstructed expected values). Each entry must include, when available:

- Q invocation ID, thread ID, entry/exit association and event provenance;
- original argument register values and bounded memory/descriptor snapshot references;
- return bytes, integer interpretation, and any observed output mutations;
- relevant candidate identity, flags, terrain/frame/hierarchy state, with exact origin of each interpretation;
- branch predicates evaluable from captured operands and the resulting path, with demonstrated vs inferred vs unknown separated;
- E/C/center/grid event association status, without proximity-only joins;
- limitations or missing data preventing exact path resolution.

Reconcile all 18 Q pairs with journal/hash/counter evidence and phase chronology. Inspect meaningful variation in the 18 distinct descriptors rather than treating them as identical because they share return value `1`. Include an explicit negative-control comparison with the Save25/26 phases that produced no Q events, within what was actually recorded. Account for the failed strict one-second external monitoring criterion separately from native capture integrity.

## 5. Workstream C — Scientific synthesis and next acquisition decision

Explain the best-supported Q→E relationship and return semantics at the narrowest defensible claim scope. Assess whether the current native candidate-query path is on the critical path to the **full outpost-position oracle** or merely a related terrain/candidate operation. Do not promote static execution plausibility to live execution proof.

Finish with a **ranked, decision-ready acquisition assessment** answering: *What is the shortest source-supported route from existing evidence to independently comparing native positioning calculations with the frozen offline model?* Propose only concrete, justified options. For any potential new observation, specify the exact required input/output or branch value, why the existing records cannot supply it, the source-supported trigger, and the minimum useful change. Include controlled-save or new-landing options if they would distinguish hypotheses, with practical operator prerequisites; **proposal only**, no new saves or live actions under this brief. Steam/NVIDIA overlays are normal baseline components, not automatic exclusions in such proposals.

If full explanation is not possible offline, document a reproducible **evidence-closure argument**: precise unresolved predicate(s), available/missing operands, exhausted authorized static/offline routes, competing explanations and the smallest discriminating observation. “Requires more research” alone is not a completed outcome.

## 6. Execution and completion contract

Apply the committed Research Execution and Completion Protocol. The primary implementer owns static tracing, raw-evidence decoding, hypothesis tests, corrections and regression tests. In-scope failures and missing interpretations trigger **continued work under this assignment**, not a new brief. Do not silently weaken the goals or the acceptance criteria.

Permitted final outcomes:

- **COMPLETE — RESOLVED:** A source-grounded Q/E decision explanation, supported return semantics, per-call reconciliation and ranked next oracle route, with claims distinguished from unobserved behavior.
- **COMPLETE — EVIDENCE GAP / ESCALATE:** Exhaustive in-scope investigation establishes exactly which indispensable native operands/execution observations cannot be recovered offline; includes a discriminating minimal acquisition proposal and reviewer-accepted closure. This is not full native equivalence and is not permission to run a test.

A partially traced CFG, speculative meaning of `1`, unevaluated readily available operands, or a proposed hook without explaining the existing 18 calls is **INCOMPLETE — REWORK**, not an acceptable final package. A genuine safety/permission barrier may require ESCALATE; do not conceal it.

### Agents

Maximum **two concurrently active sub-agents**, excluding the primary: one independent completion reviewer and at most one specialist researcher. Prefer assigning the specialist independent native Q/caller CFG reconstruction while the implementer analyses captured events; integrate both lines and resolve disagreements. The reviewer must examine source, original contract, raw-evidence references, tests and coverage—not only the implementer's summary—and issue **ACCEPT / REWORK / ESCALATE**. REWORK returns to the primary within this same assignment. Record actual reviewer challenges and corrections, including challenges where existing evidence was sufficient. Do not claim an agent was used unless it actually ran.

## 7. Required deliverables

1. A durable research report under `docs/experiments/` detailing the Q/E CFG, native address/source evidence, return semantics, hypotheses, counterexamples, coverage and limitations.
2. The complete 18-invocation evidence ledger in a reviewable, deterministic format, plus any parsers/probes and regression tests needed to reproduce it from retained raw records.
3. A decision-ready acquisition assessment with ranked concrete next steps and clearly identified authorization needs.
4. An acceptance matrix mapping every criterion to **PASS / FAIL / NOT TESTED**, primary evidence locations, independent reviewer findings, and final outcome classification.
5. `-task-only.diff` and `-complete.diff` in `.local-work/diffs/`, using the existing naming/status/manifests/inclusion-exclusion/patch-validation convention. If the tree starts clean, record that fact; otherwise preserve and identify pre-existing changes. Never stage solely to build a diff.
6. Reproducibility, link, whitespace, source-to-output, test, evidence-integrity and protected-input verification receipts. Respect the minimum **40,000,000,000 available bytes on both C: and D:** for substantial evidence processing.

Preserve exact binary32/native bit patterns and frozen predictions. No changing prior evidence or test expectations to force agreement. Explicitly separate native observation, native static-code deduction, controlled-save inference, offline prediction and speculation.

## 8. Prohibitions and handoff

**No Starfield launch, process attach/read/injection, SFSE plugin implementation or modification, Vortex deployment, runtime hook changes, new controlled saves, console commands, external-debugger work, staging, commit or push.** A future runtime experiment requires a new explicit authorization. Ordinary static examination of already available Starfield game binaries and offline artifact analysis are within scope.

Return a compact summary of demonstrated results, the final review verdict, actionable next acquisition decision, and the report/diff paths. If a narrow live evidence gap is established, state it precisely and request the necessary authorization; never imply native-equivalence validation was achieved without independent native output comparison.
