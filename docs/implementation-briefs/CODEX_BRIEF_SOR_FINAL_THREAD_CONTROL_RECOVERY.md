# Codex implementation brief — Final attempt to qualify SorEventOracle thread control

**Project:** `D:\Projects\starfield-outpost-research`  
**Disposition:** One final, offline-only engineering attempt. **Do not return an unfinished or partially qualified implementation as a successful deliverable.**  
**Baseline:** Retain the original 0.1.2/0.1.3 packages, failed October 11 live-attempt artifacts, and diagnostic 0.1.4 candidate unchanged. The 0.1.4 startup diagnostic correction is accepted in principle, but **0.1.4 is NOT_LIVE_QUALIFIED**. No staged or committed work; user wishes to wait until a live result, if one becomes justified.

## 1. Mandate and decision rule

This is the **last authorized attempt** to make the external event-associated debugger sufficiently correct and reproducible to justify *considering* another Starfield center-only smoke test. Do the actual investigation, implementation and verification within this assignment. Do not stop at a fault taxonomy, a plan, a promising hypothesis, a single passing rerun, or a partial test matrix and ask for permission to continue.

There are exactly two permissible final outcomes:

**A — COMPLETE / READY FOR REVIEW (not authorized for live use):** Both retained runtime counterexamples have been explained to the extent required to engineer demonstrably correct handling; the fixes are implemented; the **exact delivered binary** passes the entire established six-control disposable suite, the nineteen startup controls, twelve health assertions, eleven WAL/inspector tests and focused deterministic/stress/failure-path qualifications. Every control must have complete test results and independent restoration/detachment verification where applicable. Return a version-pinned candidate, source/binary hashes, complete evidence, critical residual limitations, and a recommendation whether a separately approved two-site live diagnostic is technically justified.

**B — COMPLETE / ABANDON EXTERNAL DEBUGGER:** After substantive, bounded work, if either unsafe state cannot be resolved or independently qualified, terminate the engineering line explicitly. Deliver a **completed failure analysis**, retained negative evidence, exact unresolved mechanism(s), why live use is unjustified, and a short decommission/alternative-research recommendation that does not require another debugger engineering iteration. Do not call this a partially successful candidate; do not recommend an exploratory Starfield attachment. The goal is a definitive engineering decision, not guaranteed success.

A misleading all-green report, omitted case, retest until lucky, assertion weakening, or treating a subsequent pass as erasure of a prior failure is unacceptable. **Do not ask for another follow-up implementation brief.** If a necessary solution would require unsafe or unjustified architectural changes, choose outcome B.

## 2. Exact unresolved defects and evidence to preserve

Use the committed and uncommitted repository's durable reports and the original local raw receipts. At minimum:

- `docs/experiments/event-latency/startup-failfast-investigation.md`
- `docs/experiments/event-latency/startup-014-qualification.md`
- `docs/experiments/event-latency/startup-review.md`
- `docs/experiments/event-latency/center-smoke-20261011-result.md`
- Original 0.1.2 six passing disposable controls and approved 0.1.3 and failed 0.1.4 artifacts.

**Counterexample R1 (delivered 0.1.4 `startup-candidate-014-03`):** The **grid-guard-failure** qualification returned `suspend_live_thread:5 stage=event_loop attached=0` in a center event after the deliberately bad grid preimage was disabled; the fixture ultimately completed but independent restoration/detachment was not established by that case's wrapper. `GetLastError=5` alone does not establish exactly which thread API failed or why. Instrument and correlate precise HANDLE/access, TID, return values, pre/post-liveness, suspension ownership and actual Windows errors. Determine and correct the defect, or decisively classify it as unsafe/unresolved.

**Counterexample R2 (`startup-candidate-014-02/full`):** A second breakpoint exception arrived while original-instruction replay was pending. The adapter marked `restored:true` / `RETIRED` before fixture completion. Exception address and numeric fixture exits were not captured. The later 0.1.4-03 full PASS does not negate this. Record exact exception code/address, site ownership, thread, pending-replay state, trap-flag state and source of each trap, then correctly handle native/foreign/queued events or terminate safely with independently verified teardown. Do **not** suppress or misattribute foreign exceptions.

The delivered 0.1.4-02 and -03 have identical runtime `.text` hashes, so neither counterexample can be dismissed as unrelated to the current implementation. Keep the proved startup double-fault fix. Do not reconstruct unknowable original Starfield initiating errors from guesses.

## 3. Investigation and implementation expectations

Work from executable behavior and primary API results, not just inferred control flow. Extend disposable fixtures and debugger telemetry **as needed** so both failure mechanisms can be deliberately driven and inspected. In particular:

1. **Thread enumeration/suspension:** Audit access rights, `OpenThread`/`SuspendThread`/`ResumeThread` and lifetime races, how `ERROR_ACCESS_DENIED` can arise, observed vs expected suspend counts, thread creation and exit during replay, rights inherited by debug event thread handles, and cleanup after partial suspension. Capture the actual failing API and return value immediately, before another API overwrites `GetLastError`. Never resume suspension increments not owned by the adapter.
2. **Breakpoints and single-step:** Audit all-stop debug-event semantics, pending replay ownership, breakpoint address normalization (including reported RIP), independent thread traps, TF ownership, hardware/software/foreign events, rearm ordering and disarming with multiple threads. Do not treat every breakpoint as instrument-owned or every unexpected event as proof of safe retirement. Exercise nested, overlapping and concurrent calls and exceptions.
3. **Teardown:** Specify and test how original code bytes are restored, owned TF/suspension changes undone, `ContinueDebugEvent` applied with appropriate disposition, and `DebugActiveProcessStop` completed. Avoid a report of clean retirement unless independent process-side/code and debugger checks support it. Track separately: scientific evidence, instrumentation integrity, restoration, detachment, fixture workload completion, and target survival.
4. **Diagnostics and evidence:** Retain crash/exception-address/control-state traces from **the actual fixture run** that exercises each risk. Preserve original WAL and raw evidence, including incomplete tails. Log primary errors before fallible telemetry, without reintroducing 0.1.3's double-fault. Do not weaken durability, WAL hashes, protected input checks or the 40,000,000,000-byte free-space guard on both C: and D:.
5. **Engineering judgment:** A narrow fix is preferred, but the necessary change can be substantial if justified, fully tested and contained. If Windows debugger attachment architecture cannot satisfy safe replay/retirement in this project, state that clearly and select outcome B rather than escalating indefinitely.

No arbitrary tiny event/time/volume caps to manufacture a pass. Test orchestration may use bounded diagnostic timeouts and repeat schedules; document those separately from acquisition constraints. Preserve every meaningful failure and its environment. Avoid race-dependent success criteria as sole evidence; use injected/synchronized adversarial controls wherever possible.

## 4. Required qualification gate

For outcome A, deliver **one frozen, reproducible candidate** (version after 0.1.4; do not overwrite or relabel baselines) and verify the exact package bytes after building. The final matrix must include:

- Established six disposable controls: full, center-only, invalid-grid guard, zero-hit, active retirement, genuine writer failure; **6/6 pass** on exact delivered executable.
- Startup regression controls **19/19**, health assertions **12/12**, WAL/inspector tests **11/11**.
- Specific reproducible adversarial controls for R1 and R2, including independent postflight of target code bytes and absence of debugger where target survives, and explicit treatment of target exit.
- Multi-thread race/stress and exceptional-shutdown cases that exercise repair/rearm/retirement states, not just ordinary sequential calls. Record executions, failures, exit codes, latency, input hashes and fixture completion separately.
- No unidentified early retirement, partial replay leakage, unowned TF/suspension changes, missed restoration check or silently discarded bad result. An isolated unrepeatable failure **still blocks A** until its causal and safety implications are resolved; test quantity alone cannot waive it.
- Adverse outcomes checked with negative assertions (the fixture should not see modified semantics) and recorded in a complete case matrix, including previous failed pilots.

If complete independent restoration/detachment verification genuinely cannot be performed for a particular scenario, explicitly explain why and what equivalent strong evidence exists; do not mark the requirement passed by assertion alone. If the gap matters to live safety, choose B.

## 5. Work boundaries

**Offline/disposable only.** No Starfield launch, attach, process open, memory read/write, script injection, Vortex deployment, SFSE changes, save/config/data changes, system security changes or production process debugging. No live test authorization is implied even by outcome A. Do not touch protected Save25/26 or original archive contents beyond read-only integrity verification. Keep raw WAL/dumps, proprietary binaries, local paths identifying machine configuration and bulky evidence in ignored local work; document hashes/provenance. Reuse maintainer-owned tooling with source/revision provenance; do not incorporate third-party implementation without separately established rights.

No staging, commit, push, or external disclosure. Keep the previously agreed review gate. Do not restart the build-mode spinner investigation, terrain-grid live deployment or unrelated work.

## 6. Review and delivery standards

Implement the standing `WORKFLOW.md` diff convention:

- `.local-work/diffs/<task>-task-only.diff` — only this assignment's changes.
- `.local-work/diffs/<task>-complete.diff` — all uncommitted changes since HEAD, including untracked authored text. If no pre-existing changes, still identify the complete coverage.
- `git status --short`, inclusion/exclusion manifest (including non-text/binary artifacts), exact source/binary/package hashes, patch validity, file inventory and independent checks. Do not stage to make the diffs.

Write a concise answer-first durable report under `docs/experiments/event-latency/` with: A or B at the top, causal findings for **both** counterexamples, exact patches, reproducible controls, all qualification results including negatives, incident preservation, remaining risks, and explicit next step. Include a machine-readable result matrix and a versioned candidate ZIP **only if A**; if B, provide a frozen archive of diagnosis/evidence references without packaging a misleading live candidate. Don't overwrite any reviewed baseline.

**Before returning:** actually complete the chosen outcome and run the full relevant checks. If a test fails, continue investigation within this task or deliver B. Do not finish with “5/6,” “needs more work,” “recommend next diagnostic sprint,” a provisional hook candidate, or a request for another authorization. In the final summary clearly state either **READY FOR CRITICAL REVIEW, NOT LIVE-AUTHORIZED** or **ABANDON EXTERNAL DEBUGGER PATH**.

## 7. Decision after the return

Outcome A invites critical review of the candidate and *possibly* a separately authorized, two-site center-only run card, never automatic live use. Outcome B ends this external-debugger approach and retains previous scientific/offline findings as durable evidence. Alternative positioning-oracle routes can be considered as a separate research direction later, without extending this final debugger attempt.
