# CODEX IMPLEMENTATION / AUDIT BRIEF — SOR RG2 D5AB-C2
## Existing-Evidence Closure Audit for D5AB Observer Remediation

**Status:** Proposed for maintainer-issued execution. **Task type:** bounded offline research/evidence audit and documentation; **not** an implementation, new native-analysis, or live authorization.

**Parent:** D5AB observer remediation and B2 readiness, **INCOMPLETE / REWORK**; D5R first-construction science **OPEN**. C1 was a separately completed continuation assessment, not a change to D5AB acceptance. Retain all twelve original D5AB acceptance criteria and five controlling questions unchanged. Read the original D5AB and C1 briefs, C1 assessment/matrix/decision/review, D5AB bounded handoff, D5S adverse lifetime evidence, D5X/D5Y/D5AA reports, `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, and `docs/templates/completion-contract.md` before asserting closure.

### Controlling questions (frozen for C2)

- **C2-Q1 — Existing-evidence coverage:** For each C1 evidence candidate in **G1/G2, L1/L2, S1, T1, R1**, what can the *original retained primary artifacts* positively prove or disprove? Satisfy by citing exact available exported native records, source versions/lines, tests, receipts and counterexamples, with evidentiary boundaries. A report summary or prior reviewer verdict alone is not the primary evidence.
- **C2-Q2 — Remaining obligations:** For every unresolved material ownership, writer, source-lifetime, transport, store or reducer question, what exact missing edge/value/test prevents a specified original D5AB claim? Satisfy by an edge-by-edge and requirement-by-requirement disposition; no generic “further analysis required.”
- **C2-Q3 — Smallest justified continuation:** Which original D5AB requirements can be credited from existing evidence, which cannot, and what is the smallest technically credible subsequent action for each genuine gap? Include alternatives with scope, evidence value, risks and prerequisite authority. C2 completion means completing this audit, **not** declaring D5AB/B2 ready.

### Scope and permissions

**Authorized:** Read already committed or retained repository sources; existing Ghidra/native exports, manifests, receipt records, logs, fixed test outputs and previous analyses; perform offline consistency computations and read-only cross-checks that do not execute/rebuild instrumentation or generate fresh executable disassembly; create/update C2 audit notes, evidence indexes, decision matrix and review documents. Use permitted existing local inputs; record missing/inaccessible files and do not invent them. Retain original files and historical verdicts intact. Do not stage, commit, push or publish.

**Not authorized in C2:** New Starfield.exe/CreationKit.exe disassembly or function export; new native instrumentation research involving fresh binary inspection; changing observer/assembly/reducer/controller source; builds or execution of native qualification binaries; deploying plugins; starting or controlling Starfield; new SFSE/observer live capture; protected-save mutation; running a new B2 experiment. These limits are **the agreed purpose of an existing-evidence audit**, not anticipatory cybersecurity restrictions on future briefs. Read-only examination of *existing* native exports is explicitly permitted. If an existing evidence file is genuinely insufficient, identify the exact acquisition proposal for separate approval.

**Cybersecurity interruptions:** Prior D5AB guardrail blocks are unresolved and are suspected false positives; do not assert a proven cause or create a project-wide presumption of prohibited research. Do **not** preemptively weaken, euphemize, quietly redefine, or refuse otherwise authorized work out of fear of a possible block; do **not** make special workflow changes solely to avoid a hypothetical block. If an actual block occurs, record its exact available message, attempted operation, timestamp/context and impact as accurately as possible. Respect that particular enforced refusal; do not circumvent it, disguise the same blocked action or repeatedly retry to defeat it. Continue independently authorized work where possible, without automatically abandoning C2; escalate only if an indispensable task remains genuinely blocked. Ordinary project safety/permission gates remain in force.

### Required method and deliverables

**1. Source/provenance inventory (G1/G2).** Pin the actual committed D5AB checkpoint, current repository revision and source versions; reconcile `d5ab-sources.csv`, initial/build receipts, native-export identifiers, schema, `observer.h`, `bridges.asm`, transport, reducer and fixtures. Resolve or explicitly retain the C1-noted S002 `observer.h` earlier-hash discrepancy. Identify missing local/primary evidence separately from known files. Do not silently rebase historical hashes or repair the record.

**2. Lifetime and safe identity (L1/L2, highest priority).** Using *only retained exports and sources*, enumerate existing evidence for source creation, content-derived identity writes, deduplication, publication, lookup, retirement, destruction and all known alternate writer/free routes. Evaluate the D5S detached-density/shift-38 counterexample rather than assuming Grid retention protects selected source pointers. Examine safe read boundaries, synchronization, lifetime after unlock, unpublished nonnull returns, pointer reuse/ABA, stable token versus source key, owner/context/epoch resets and missed invalidation. For each edge, state observer witness/fence, primary citation, coverage and competing route. A missing counterexample is not a lifetime proof; no pointer/token/key equivalence without separately justified identity and continuity.

**3. Visited insertion (S1).** Trace the existing `reserve_hook`/`stored_capture` and assembly bridge evidence to the native reserve return, `0xffffffff` sentinel, actual executed token-store boundary, failed/exception outcomes and source/epoch correlation. Identify what is native, what is modeled, and which version each control tested. Do not equate a reserve attempt with successful insertion.

**4. Transport and recorder (T1).** Audit existing queue-capacity tests, loss counters/uncertainty, producer concurrency, worker diagnostics, flush/wake delays and shutdown/fault evidence. Reconcile claimed capacities and test geometry with actual source/receipt versions. Clearly distinguish fixture-zero-loss evidence from a retail guarantee, and exclude any missing B1 arrivals from modeled arrivals. Do not silently close controller integration or worker-exit detection on the basis of standalone Python thread checks.

**5. Reducer and final-source correspondence (R1).** Establish the exact native-build reducer snapshot versus later semantic-test reducer versions noted in C1, and map every existing test to the code it truly exercised. Challenge damaged/truncated evidence, missing append/store, identity collisions, reset/loss fences, cross-thread ordering and old-before-arming selection; inspect actual negative-control evidence. Identify required *new* integrated controls as future actions without running them under C2.

**6. D5AB mapping and alternatives.** Reconcile the audit against **all five original D5AB controlling questions and twelve criteria**, even when C2 focuses on G1/G2, L1/L2, S1, T1, R1. Never relabel a partial source/test as a passed original criterion. Provide targeted next-work packages (ordinary offline tests/integration; genuinely necessary native edge acquisition; deployment/live only under separate authority). State which can proceed independently and which depend on a lifetime proof.

### Required artifacts

Create under `docs/experiments/resource-retained-population/`:

- `d5ab-c2-audit.md` — concise evidence-first findings and contradictions, with a section for each workstream.
- `d5ab-c2-evidence-matrix.md` — **one row per material edge/claim** with C1 reference, exact primary source/receipt, verified/claimed access, finding, `PROVEN` / `DISPROVEN` / `UNRESOLVED`, limitation, next discriminating action, and original D5AB mapping.
- `d5ab-c2-decision.md` — account of all original five questions/twelve criteria, C2 controlling-question outcomes, minimal continuation packages and permissions.
- `d5ab-c2-investigation-ledger.md` — active hypotheses, attempts, missing evidence, contradictions, unresolved alternative paths and checkpoint references; start this early, update while working.
- `d5ab-c2-review.md` — independent substantive completeness review, counterarguments, final disposition and exact final-snapshot provenance.

A compact source-lifetime graph may be included **only if** it improves the precise edge ledger; do not use a diagram as evidence. Do not rewrite the gameplay checklist without a directly proven change; if one is justified, preserve its 31 original items and evidence distinctions.

### Mandatory acceptance criteria (frozen)

- **C2-AC01:** Exactly pin original D5AB/C1 authority, commit/source snapshots, evidence access and C2 no-execution boundary. No unauthorized source, binary, plugin, game, save, git-publication or external operation.
- **C2-AC02:** Inspect every relevant C1-named G1/G2, L1/L2, S1, T1, R1 primary-evidence candidate or record a specific inaccessible/missing artifact and its consequence. Resolve source-hash/version discrepancies only with evidence.
- **C2-AC03:** Produce a native/observer ownership and lifetime edge census, with detached-density, alternate frees/writers, pointer reuse, publication/retirement and synchronization challenges; never call it safe from absence of a counterexample.
- **C2-AC04:** Audit visited successful-store, transport and worker-health claims, reducer/final-source version consistency and negative controls; distinguish static, fixture, receipt and retail evidence.
- **C2-AC05:** Complete a row-by-row original D5AB five-question/twelve-criterion matrix and an actionable ledger of exact unresolved obligations, alternatives, smallest next action and required separate authority; retain D5AB **INCOMPLETE** unless its original standard has independently been met (C2 itself cannot authorize such a change).
- **C2-AC06:** Independent reviewer challenges the **original C2 questions and original D5AB criteria**, omitted evidence candidates, adverse paths, unwarranted closure and permission compliance. Deliver final reports, acceptance matrix, local test/read-only checks, complete and task-only diffs as applicable, source-preservation receipts and exact final-snapshot editorial review consistent with `WORKFLOW.md` and `EDITORIAL_STANDARD.md`.

### Completion and escalation contract

C2-Q1/Q2/Q3 are **COMPLETE** only when every scoped material claim is classified with actual evidence or a sufficiently justified missing-evidence determination and the downstream original criterion/next action are explicit. A **DISPROVEN** safety claim is a valid audit result; an unresolved critical edge cannot be elevated to proven. If material accessible evidence remains unexamined or the next action is vague, status is **INCOMPLETE / REWORK**, not ACCEPT. Genuine **BLOCKED / ESCALATE** requires the protocol's specific terminal proof: exact indispensable artifact/authority, attempts, viable alternatives considered, barrier class, smallest required permission and resume point. A narrow C2 acceptance is **not** a native observer qualification, B2 readiness approval, or closure of D5R.

No new live run or B2 authorization is implicit. Preserve original evidence, record failures and stop only unauthorized/unsafe or actually refused actions while continuing independent permitted work. Reviewer verdicts must distinguish C2 scientific sufficiency, evidence integrity, engineering readiness, editorial quality and D5AB parent status.

### Delivery

Provide the five documents, concise operator-facing summary, frozen question/criterion matrix, all negative findings, local reproducibility pointers, and verified `d5ab-c2-task-only.diff` and `d5ab-c2-complete.diff` (or complete only if clean baseline) under `.local-work/diffs/`. Do not stage or commit. Recommend next work *only* after the independent exact-snapshot review and preservation checks. Report cybersecurity blocks as observations, not inferred causes or justification to change accepted research objectives.
