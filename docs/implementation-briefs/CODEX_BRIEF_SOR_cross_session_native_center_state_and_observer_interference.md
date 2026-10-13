# Codex Research Brief — Cross-Session Workshop Center State, Hook Coverage, and Observer Interference

**Project:** `D:\Projects\starfield-outpost-research`  
**Type:** Offline scientific reconstruction and comparative instrumentation audit  
**Authority:** Analysis, read-only evidence processing, original test/diagnostic development, documentation, independent review. **No Starfield launch, injection, deployment, new observer build, save modification, staging, commit, or push.**  
**Starting state:** Latest committed and synced research, including the 0.5.0 and 0.6.0 native observer implementations, sealed live captures and their reports.

## 1. Purpose and central question

Two observations of the same controlled Save25 lineage appear to disagree about native Workshop center Z:

| Outpost | Saved Z and 0.6.0 observed Z | 0.5.0 observed Z |
|---|---:|---:|
| SOR-002 | approximately +18.352507 | approximately +3.643147 |
| SOR-003 | approximately -31.890842 | approximately -9.516418 |

The 0.5.0 terrain-query callback observations were attributed to caller RVA `0xAD0C36`, whereas the 0.6.0 coherent Workshop-center observations were attributed to caller RVA `0xF4A1D4`. These are **reported prior findings**, not an established like-for-like comparison. The central task is to determine whether these are (a) different normal native operations or reference coordinate states, (b) different observation coverage/semantics, (c) observer-induced changes to engine behavior, (d) faulty identity/decoding/association, or (e) some evidenced combination. Do **not** assume that the 0.5.0 discrepancy requires a Z-restoration write, nor that 0.6.0 disproves it.

The **scientific priority** is to characterize the actual native coordinate state and the implications for exact durable outpost positioning, not to defend either observer's interpretation.

## 2. Required evidence inventory and baseline

1. Locate and read the committed source, run cards, scientific reports, acceptance matrices, raw-capture manifests, private receipts and archived static native exports for both versions. Verify version/build identity, installed game version, capture completeness and source provenance. Preserve all originals as read-only; derivative products go under ignored `.local-work/`.
2. Construct a matched event/call-site inventory: every relevant patched native `CALL` or pointer site, original target, wrapper target, observed event kind, entry/exit boundary, thread/context, and whether equivalent native behavior is visible in both versions. Distinguish *not instrumented*, *instrumented but not observed*, *recorded but filtered*, and *missing/ambiguous data*.
3. Establish exact raw field semantics from game instructions, not from similarly named observer fields. Inspect the native `F4AB80` center calculation and the two reported immediate callers. Verify the 0.5.0 and 0.6.0 sampled object pointers, base/reference identities, own-cell/world pointers, `+0xD3` flag, Workshop compensation, query source frame, and their sampling times as evidence permits.
4. Explicitly audit live-game context differences: save identity/hash, loaded modules, gameplay action, build-mode/travel sequence, initial scene, thread/caller paths, and activation/reuse of references. Do not assume that loading the same Save25 produces identical runtime state.

## 3. Competing hypotheses — test, don't pick a favorite

### H1: Different hook coverage or sampling boundaries

Reconstruct whether 0.6.0 instrumented the `0xAD0C36` path from 0.5.0, whether 0.5.0 sampled `0xF4A1D4`, and what their absence/presence can establish. Different caller RVAs must be mapped to actual instruction-level provenance; an event label alone is insufficient.

### H2: Genuine native frame/state differences

Trace parent/cell/world ownership, restoration flags, conversion (`B734C0` → `B73310`), replacement writes (`B4E410` and audited direct writers), reference lifetime, and candidate/Workshop frames. Identify concrete native transitions capable of producing the respective Z values. Check binary32 arithmetic and exact bits; do not fit arbitrary offsets to two data points.

### H3: Observer-induced perturbation

Compare hook byte patches, wrapper ABI, register/flags/FPU preservation, exceptions, concurrency, reentrancy, recursion guards, queue/write-induced timing, admission/retirement and call ordering. Review especially the dramatic instrumentation difference (0.5.0's targeted travel/Workshop observations versus 0.6.0's high-volume general position-writer coverage). Determine whether an implementation defect or timing-sensitive behavioral change is **supported**, merely possible, or contradicted by the traces/tests. Do not claim noninterference simply because disposable tests passed.

### H4: Identity or interpretation mismatch

Re-decode critical original binary blobs independently of the report's existing decoder. Confirm which objects and native frames the center values belong to, whether the sampled reference is the same logical Workshop, whether load remapping/pointer reuse matters, and whether either value represents a different intermediate rather than the same-position field.

### H5: Other evidenced explanation

Follow credible new static/native leads within the authorized scope. Preserve counterexamples and alternative explanations rather than shoehorning findings into H1–H4.

## 4. Execution and concrete deliverables

- **Cross-session comparison ledger:** Record-level provenance for key observations, including exact source file/hash, offsets or event IDs, caller/return-site identity, raw binary32 XYZ and flags, reference identity qualifiers, confidence and unresolved associations. Include compact tables for both Workshops; do not materialize arbitrary massive evidence sets in tracked documentation.
- **Call-site coverage matrix:** Include both observer versions' *patched native site*, *event emission*, *downstream consumer*, and *gaps*, with explicit decisions on whether an apples-to-apples comparison exists.
- **Independent decoder/verification tests:** Reproduce the critical Z values from raw bytes; exercise incorrect field offsets, pointer reuse, identity-domain confusion, missing ancestry, conflicting frame flags and cross-thread journal ordering. Reuse existing tooling if trustworthy; add original focused tooling if needed.
- **Native dependency map:** Identify where each coordinate frame is created, translated, restored, queried or consumed; separate actual observations, static proof and conjecture.
- **Scientific report:** Adjudicate each hypothesis using evidence-based categories such as supported, excluded for the scoped cases, unresolved, and untestable from current corpus. Explain the significance for the validated XY/grid algorithm and for full XYZ equivalence.
- **Decision-ready acquisition assessment:** If essential evidence remains missing, identify the *smallest* discriminating native observations and a realistic natural trigger, with clear costs and instrumentation effects. Rank alternatives and assess whether further live instrumentation is justified. **Do not build or launch an observer under this brief.**
- **Durable research record and review package:** Update experiment indexes, source/provenance ledgers and decision records where appropriate. Produce `.local-work/diffs/<task>-task-only.diff` and `-complete.diff` inclusive of untracked text, status/inclusion/exclusion manifests, reproducible checks, and a succinct final acceptance matrix.

## 5. Scientific completion contract

The task is **not complete** when Codex merely finds that the two values differ or recommends a new observer. It must fully audit relevant code paths and existing capture provenance, implement/execute reproducible offline comparisons, challenge competing interpretations, and deliver one of:

**A — Resolved comparison:** A defensible explanation of the differing values, supported by native evidence and exact reproducible comparisons; clearly delimit any still-untested broader equivalence.

**B — Complete evidence-bound result:** Demonstrate which hypotheses the available evidence distinguishes and exactly which remaining operands, identity joins, lifetime events or equivalent-boundary observations cannot be reconstructed offline. Include an independently challenged minimal acquisition recommendation; do not relabel an unexhausted static lead as a terminal limitation.

Negative and counterexample findings are welcome. In-scope failures, ambiguous results, unexpected evidence and failed tests require correction/investigation **within this assignment**. A reviewer REWORK verdict triggers continuing work, not a new user brief. Escalate only an actual authority/safety boundary.

## 6. Agent roles and independent review

Maximum **two concurrently active sub-agents**, excluding primary Codex. Use an independent reviewer, and deploy one specialist where worthwhile. Suggested split: specialist independently audits the 0.5.0/0.6.0 native hook and caller coverage or observer interference; primary investigates raw scientific identity/frame evidence and reconciles findings. Preserve disagreements until resolved by primary evidence. Record **distinct specialist contributions** (novel findings, corrected assumptions, tested counterexamples, uncertainty reduction) rather than routinely reassessing the already-established value of the reviewer. The reviewer must see the original brief, primary data references, source, tests and final diff; its ACCEPT/REWORK/ESCALATE and corrections must be durable.

## 7. Permissions, protection and operational policy

- **Strictly offline:** no game launch, process attach, runtime memory, SFSE deployment, native hook changes or external debugger revival. No edits to protected saves, frozen predictions, sealed WALs, game assets, source archives or original baselines.
- Reuse project-owned tools with provenance; third-party code use must satisfy the project's permission and attribution rules. External sources may inform hypotheses but cannot substitute for pinned-game native evidence.
- Maintain the **40,000,000,000-byte free-space guard on C: and D:** for substantial evidence processing. No arbitrary wall-clock or output-volume stop conditions. Only genuine integrity, safety or authority failures justify cessation; partial scientific observations remain evidence.
- Do not stage, commit, push or publish. Keep raw proprietary, save, binary and private capture artifacts ignored/local.
- Preserve prior negative findings, observed disagreements and source snapshots unchanged; report corrections as new documented analyses rather than rewriting historical captures.

## 8. Handoff format

Return a concise conclusion **first**, followed by paths to the scientific report, cross-session ledger, independent reviewer decision, test/qualification receipts, complete and task-only review diffs, and explicit remaining unknowns. State exact scientific scope and do not claim full XYZ equivalence without independent evidence. No live work is implicitly authorized by review acceptance.
