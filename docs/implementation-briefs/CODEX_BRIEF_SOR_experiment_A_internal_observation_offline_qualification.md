# Codex implementation brief — SOR Experiment A: Offline Qualification of Internal Spatial-Decision Observation

**Status:** Implementation brief for a finite, disposable **offline engineering qualification**.  
**Repository:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research`).  
**Predecessor:** Committed Experiment A feasibility assessment in `docs/experiments/spatial-equivalence-feasibility/`, decision **REVISE**.  
**Authorization boundary:** This brief authorizes *offline test-harness and qualification work only*. It does **not** authorize an SFSE observer, Starfield launch, live hooks, game/save modification, Vortex package, deployment, staging, commit or push.

## 1. Research rationale and decision

Our Milestone B evaluator reproduces reconstructed resource-region spatial predicates, but **native spatial equivalence remains NOT TESTED**. The accepted feasibility assessment identified region-entry, resolved-operand, ACCEPT and REJECT instruction boundaries in the pinned `Starfield.exe` 1.16.244.0, along with a crucial mismatch between the existing observer mechanism (guarded CALL replacements) and the required observations (internal control-flow edges).

The prospective experiment has value **only if** it can yield independently captured, complete native input/decision pairs for offline comparison. The objective of this task is to establish whether the required internal observation method can be engineered with credible state-preservation and evidence-integrity guarantees *before* building a retail observer. Do not confuse successful synthetic qualification with proof of live safety or of spatial equivalence.

**Decision to deliver:** **PASS / REVISE / FAIL (NO-GO)**, supported by explicit criteria and an independent review. A failure or defensible NO-GO is an acceptable completed result. Prior investment in 0.8.0 or other observers must not bias the result.

## 2. Authoritative research inputs

Read the committed feasibility report and linked evidence *before* designing the harness, especially:

- `docs/experiments/spatial-equivalence-feasibility/report.md`
- `docs/experiments/spatial-equivalence-feasibility/boundary.md`
- `docs/experiments/spatial-equivalence-feasibility/coverage.md`
- `docs/experiments/spatial-equivalence-feasibility/value-risk.md`
- `docs/experiments/spatial-equivalence-feasibility/review.md`
- Existing Milestone B `resource_spatial.py`, tests, native function register, and provenance/index references.
- `WORKFLOW.md` and current observer/test conventions; reuse qualified, project-owned utilities where fit, but **do not modify the unapproved 0.8.0 candidate**.

**Grounding:** Verify exact native byte/instruction contracts and register provenance against the committed pinned exports. Do not assume a proposed RVA is a function entry or an independently patchable point. Preliminary boundaries (all RVAs for the pinned build): region entry `0x021E1060`; resolved query `0x021E1119`; branch paths `0x021E1140–0x021E1154`, `0x021E145C–0x021E1460`, `0x021E16D4–0x021E1714`; actual REJECT `0x021E174E`, ACCEPT `0x021E1772`. Use the committed boundary assessment for precise semantics; correct discrepancies explicitly rather than silently substituting addresses.

## 3. In-scope work: three finite offline qualification gates

### Gate G1 — Native execution-state preservation and continuations

Determine whether a plausible internal instrumentation mechanism can observe both terminal spatial-decision edges and return execution to the *correct original continuation*, without changing observable computation.

- Identify instruction boundaries, displaced instruction semantics, patch/trampoline constraints, register and flag liveness, stack layout/alignment, and the relevant Windows x64 ABI obligations.
- Test preservation of general-purpose registers, condition flags, volatile/nonvolatile SIMD/vector state and floating-point environment where the native path uses them; include representative state that naïve instrumentation would corrupt.
- Test both ACCEPT and REJECT paths and relevant branching/continuation cases. Confirm that an observation callback cannot implicitly alter a native branch condition or return value.
- Exercise concurrent entry/reentry, nested observations, unexpected interruption and cooperative retirement as appropriate to the mechanism. Clearly identify properties not provable from a synthetic fixture.
- Keep experiments confined to disposable test functions and synthetic executable memory under the test process; **never patch `Starfield.exe`**.

**G1 passes only if** concrete reproducible tests establish faithful continuation/state for the tested instruction classes and decision paths, with remaining retail assumptions stated. A conceptual design alone is not a pass.

### Gate G2 — Complete geometry capture and owned-evidence integrity

Qualify a bounded mechanism for capturing **complete**, variable-length native geometric operands before their lifetime expires:

- Query's indexed position, frame/domain context, horizontal radius, upper scalar, actual coordinate translations and any per-use resolved values needed by the frozen evaluator.
- Region identity/center/radius, point count, ordered points and widths **without truncation or synthetic reconstruction**.
- Pair each native verdict with its corresponding region-entry data and query ancestry (thread/invocation/sequence and cache/source identifiers where required), rather than heuristically joining timestamps.
- Handle point-count zero/one/multiple; large-but-valid arrays; pointer/read failure; object mutation during copying; record/queue capacity; STOP during capture; mismatched or missing terminal verdict; nested/concurrent evaluations.
- Distinguish **complete valid record**, **explicitly incomplete/invalid record**, and **not evaluated**. Never emit a partial geometry object as a valid comparison case, silently truncate, or turn a missing decision into REJECT.
- Prefer no blocking waits, allocations or file I/O in a native hot-path callback; compare viable options with measured cost. Do not impose an arbitrary scientific event count, run-time or session-length quota. Capacity overflow is a reported instrumentation failure, not silent loss.

**G2 passes only if** fixture-produced records can be independently decoded and checked byte/element-for-element against their original inputs across positive and negative cases, including concurrent tests and failure injection.

### Gate G3 — Operand/decision provenance and independent replay viability

Show that the proposed observation can reliably capture the operands **actually consumed** by a native decision:

- Account for repeated query-coordinate resolution inside one region evaluation. Establish stability with evidence or capture the distinct values at relevant use points; don't assume a single initial position is sufficient.
- Separate region acceptance/rejection from the source-traversal callback's return status. A callback return is **not** a native Boolean spatial verdict.
- Demonstrate representative broadphase, zero/one/multi-point, containment, vertex and edge-distance cases where the synthetic fixture can faithfully model the instruction-level branch/operand requirements. Do not claim fixture coverage automatically implies such cases will occur naturally in Starfield.
- Run the **existing frozen reconstructed evaluator** against fully owned synthetic input/decision fixtures as a plumbing check; a replay agreement on synthetic inputs is **not** independent native validation.
- Document exactly what real observation would need to capture, what the fixture demonstrates, and what remains unresolved until actual native cases are acquired.

**G3 passes only if** every qualified verdict is unambiguously attributable to a complete operand record, or is explicitly rejected from the comparison corpus with an actionable diagnostic.

## 4. Strict boundaries

- **No retail observer implementation or Vortex ZIP.** No changes to SFSE plugin hooks, no prelive run card, no in-game capture or new deployment.
- **No controlled invocation** of Starfield functions, in or out of process. This is an offline synthetic qualification, not an attempt to invoke the native resource updater.
- **No new resource-generation research**, remote-query feasibility work, Workshop lifecycle experiment, disappearing-deposit investigation, or implementation of replacement native spatial logic.
- No modification to the existing 0.8.0 DLL/package/source. Treat it as a rejected, unadopted candidate.
- Preserve protected files, executable exports, Ghidra projects, reference saves and historical evidence. Only disposable fixture material may be generated; document its creation and deletion policy. Avoid proprietary native code/bytes in public deliverables and diffs.
- Keep technical terminology neutral and scientific; no mod-oriented gap analysis.

## 5. Execution plan and stopping rules

1. **Scope inventory:** Identify already available helpers, native pinned evidence, harness constraints and the smallest plausible observation approach. Explicitly compare candidate mechanisms and choose only what is needed to test the critical feasibility question.
2. **Static safety/contract analysis:** Record exact observed instruction classes, boundary register/flag assumptions and expected decision continuations.
3. **Implement disposable qualification fixtures:** Build the smallest runnable harness for G1–G3. Use project conventions; don't create a generic instrumentation framework.
4. **Run tests and fault injection:** Preserve commands, results, failures and timings. If a gate fails, investigate bounded fixes directly relevant to that gate, but do not silently expand scope or repeatedly reinvent a different hook mechanism.
5. **Independent reviewer:** Require an independent critical review of scientific value, state/ABI fidelity, geometry completeness, provenance, negative tests, and the honesty of the proposed PASS/REVISE/FAIL classification. Primary agent performs any authorized corrections and reruns affected checks. At most two active sub-agents concurrently (reviewer plus optional narrowly scoped specialist).
6. **Decision:** Recommend **PASS** only if G1–G3 all pass as synthetic qualifications and a concrete future retail capture still offers material scientific value. **REVISE** only if there is one narrow, named solvable blocker with a proportionate next step. Otherwise **FAIL/NO-GO**. Do not convert a failed gate into PASS by weakening the acceptance criteria.

**Hard stop:** If no bounded, testable internal-observation method can preserve the native execution state and complete evidence, terminate the task with documented FAIL/NO-GO; do **not** proceed to live-observer construction.

## 6. Deliverables and review package

Place durable research outputs near the committed Experiment A feasibility materials, with clearly named paths chosen to avoid overwriting prior evidence:

1. **Qualification report:** What was tested, mechanisms considered, qualified instruction/operand classes, exact G1–G3 criteria, pass/fail table, measured costs, unproved assumptions, and final PASS/REVISE/FAIL recommendation.
2. **Technical evidence:** Native boundary references, minimal test-harness source, fixture definitions, failure injection results, machine-readable completeness/provenance record definitions, and runnable replay instructions.
3. **Scientific decision note:** What this qualification does *not* establish (especially native equivalence), whether a next observer could settle a consequential question, and what exact next authorization would be needed. Include a defensible NO-GO if warranted.
4. **Independent review:** Reviewer objections, primary-agent response, reruns, residual risks and acceptance or rejection of the decision.
5. **Provenance:** Pinned tool/source identities, executable version, test commands, test results, changed-path inventory, protected-input verification scope and limits. Preserve a full audit trail without modifying historical evidence.
6. **Two diffs:** `.local-work/diffs/<descriptive>-task-only.diff` and `...-complete.diff`, including newly added untracked textual source/documents in the complete diff. Provide SHA-256s for output files and evidence manifests; exclude binary dumps, raw protected files and executable artifacts from user-facing diffs.
7. **Suggested Conventional Commit subject** only after review; do **not** stage, commit or push.

### Documentation quality gate

Audit every added/edited Markdown or prose file for malformed fusion of tokens—e.g., missing spaces around version numbers, addresses, identifiers, counts, punctuation or embedded code—and for broken relative links. Correct problems in the task changes before seeking independent acceptance. Do not initiate a repository-wide prose rewrite absent a separate finding and approval.

## 7. Acceptance standard

The task is **complete** when it returns reproducible offline qualifications (or a clearly evidenced technical failure), independent review, a non-inflated scientific decision and the preservation/review package. It is **not** complete merely because fixture tests pass, and a PASS here is **not** authorization for a live observer. If later authorized, a separate retail implementation and pre-live scientific-value review will still be required.
