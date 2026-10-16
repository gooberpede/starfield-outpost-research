# Codex Research and Qualification Brief

## SOR — Experiment A: x87 State Preservation Across Internal Exception Observation

**Assignment type:** Narrow offline engineering qualification and scientific decision.

**Repository:** `starfield-outpost-research` (use repository-local paths and current `WORKFLOW.md` conventions).

**Authority:** This brief authorizes disposable Windows fixture analysis, narrowly scoped test implementation, documentation, and one evidence-motivated preservation correction **only**. It does **not** authorize launching Starfield, attaching to or instrumenting a retail process, creating or modifying an SFSE observer/DLL or Vortex package, deploying anything, altering the frozen spatial evaluator, staging, committing, or pushing.

### 1. Background and decision to resolve

The prior Experiment A internal-observation qualification reported a **scoped synthetic PASS** for its exception-based breakpoint and continuation mechanism, but **full x87 environment preservation failed**. The test reported **1,110 instances of lost high x87 instruction-pointer bits**. That limitation must not be dismissed on the grounds that the mapped geometry presently appears to use SSE/AVX; equally, do not assume that a field observed through a Windows exception context necessarily represents a loss of architectural processor state. The previous qualification, its failing fixtures, independent review, and preserved receipts form the baseline. Do not rewrite history or replace the baseline with the new results.

**Primary question:** Can the existing exception-based internal-observation mechanism preserve the required x87 state through a trap, handler and resumption, including its documented adversarial operating conditions?

The only acceptable scientific outcome is a defensible **PASS** or **NO-GO** for this mechanism, with diagnostic uncertainty recorded explicitly. A result that cannot establish preservation is **not a PASS** and does not authorize progressing to retail instrumentation.

### 2. Three comparable execution conditions

Prepare equivalent, repeatable x87 preconditions and operations for:

1. **Uninstrumented control:** No exception-based observation; record baseline before and after the comparable instruction sequence.
2. **Minimal exception handler:** Only the smallest necessary exception handling and continuation, avoiding unrelated instrumentation work.
3. **Adversarial handler:** The prior synthetic mechanism with the tested observation, continuation, and lifecycle conditions.

Keep initial state, instruction sequence, execution path, data and expected outputs equivalent wherever technically possible. Document unavoidable differences. Distinguish the architectural x87 state from the representations exposed by `CONTEXT`, extended state/XSTATE, save instructions, or instrumentation itself. The act of inspecting x87 state may modify or report it differently; qualify the measurement rather than assuming it is passive. Retain raw binary evidence or unambiguous hexadecimal field representations and compare exact relevant fields, not merely numerical operation results.

### 3. Locate the first divergence

Obtain qualified state observations at **three boundaries**:

- Immediately **before the trap** (or equivalent control-point in the uninstrumented case).
- At **exception-handler entry**, before the handler's own preservation or instrumentation work insofar as the API and measurement mechanism permit.
- **After continuation**, at a controlled comparable instruction boundary.

Track as independently as practicable: x87 control word; status word and condition flags; tag state; x87 register stack values and top-of-stack interpretation; x87 last-instruction pointer and last-data pointer and their full relevant width/selector representation; and any associated state needed to establish exact continuation semantics. Record the mechanism used to obtain each observation and its limitations.

For each discrepancy, classify whether it first appears **before handler entry**, **inside handler manipulation**, or **on continuation**. If the available measurements cannot localize the loss, record that as uncertainty rather than selecting a convenient cause. Include a clear analysis of whether missing instruction-pointer high bits are lost from actual architectural state, are absent only from a Windows context representation, or remain recoverable from independently qualified data.

### 4. Exactly one targeted correction, conditionally

Only if the baseline investigation identifies a specific mechanism of loss **and** demonstrates where the original required information remains recoverable, implement **one narrowly targeted correction** and rerun the three-way comparison and all relevant regressions. Describe the hypothesis, modification and anticipated exact field-level difference before implementing it.

Do not try a sequence of speculative preservation fixes; do not weaken the required-state definition after seeing the results; do not quietly substitute inferred state for captured state. If the state is irretrievably unavailable at handler entry and there is no independently justified recovery path, return **NO-GO** for this exception route. If no correction is warranted or evidence cannot support one, report that explicitly.

### 5. Mandatory regression coverage

Reuse and extend the existing disposable fixture and decoder where practical. Include the established adversarial checks relevant to this mechanism:

- Nested exceptions and nested or interrupted observation sequences.
- Concurrent threads, handler re-entry and correlation isolation.
- Cooperative STOP, retirement and quiescence with in-flight events.
- Both native-decision continuation classes (ACCEPT and REJECT fixture paths).
- Previously passing GP-register, flags, SSE/AVX, MXCSR, control-flow and evidence-correspondence checks; do not regress earlier qualified guarantees.
- Malformed/incomplete evidence treatment, where the existing decoder contract applies.

The test suite should record failures as failures. Do not skip troublesome cases silently, infer a PASS from a process surviving, or establish success merely through mathematical output equivalence while required environment fields differ.

### 6. Decision gate

**PASS:** The required x87 environment is shown to survive the trap/handler/continuation accurately within explicitly defined fixture conditions, using reliable measurements, with nesting/concurrency/STOP and previously qualified controls still passing. Show field-level comparison evidence and precise coverage limits. This is **only** an offline mechanism qualification; retail safety and native spatial equivalence remain NOT TESTED.

**NO-GO:** Required state is lost, cannot be recovered by the one authorized evidence-based correction, or its preservation cannot be demonstrated to the demanded contract. Explain the earliest evidenced failure boundary, what can and cannot be inferred, and why this mechanism should not advance to retail use.

If uncertainty prevents proving irrecoverable loss, document the outcome as **indeterminate evidence / operational NO-GO**, not as a successful qualification or a mandate for open-ended additional experiments.

Do **not** condition acceptance of this task on obtaining PASS; an independently reviewed NO-GO is a complete result.

### 7. Explicit scope exclusions

Do not expand into resource-region geometry ownership, new native operand boundaries, different hooking approaches, retail process exception-chain compatibility, live resource-preview experiments, remote resource querying, or general AI-assisted decompilation. Do not implement an alternate breakpoint mechanism as a fallback. A NO-GO may recommend reconsidering the observation mechanism in a future separately approved assignment, but no such development is authorized here.

Protect all existing saves, native exports, Ghidra projects, historic captures, existing observer binaries/packages and frozen evaluator sources. Use disposable output paths for tests. Do not run Starfield or modify deployed game files.

### 8. Review, reporting and deliverables

Follow `WORKFLOW.md` and the established research execution/completion protocol. Have an **independent reviewer** examine experimental controls, reliability of x87 measurements, correction eligibility (if used), preserved regressions, and the PASS/NO-GO inference. A reviewer must be empowered to return REWORK on methodological defects and to accept a properly justified NO-GO. Do not allow unlimited iterative speculative experiments under the cover of review.

Deliver:

1. A concise technical report explaining the measurement methods, three-way results, first-divergence localization, full-width pointer findings, and any targeted correction.
2. Reproducible disposable fixture/test code and explicit offline commands.
3. A field-by-field before/handler/after comparison table with traceable evidence references and stated measurement uncertainty.
4. A regression and preservation ledger, with relevant receipts, SHA-256 checksums and an exact account of which protected inputs were checked.
5. A **PASS or NO-GO** conclusion with independent review record and a clear statement of what remains **NOT TESTED**.
6. Task-only and complete diffs under `.local-work/diffs/`, including newly created text files; package/output inventory and hashes, with private raw evidence and binary blobs excluded from shared diffs as usual.
7. A proposed Conventional Commit subject only; **do not** stage, commit or push.

**Prose-quality gate:** Review all newly written or edited documentation for fused words, missing spaces around versions/hex addresses/counts, damaged Markdown and inconsistent terminology. The independent reviewer must inspect authored prose, not only code/test outputs.

### 9. Final handoff format

Summarize: decision; first loss boundary; whether correction was attempted (and why); exactly which x87 fields are proven preserved or unproven; regression results; preservation scope; files changed; independent review outcome; and whether any follow-on work is actually justified. **Do not imply a PASS here authorizes any live observer.**
