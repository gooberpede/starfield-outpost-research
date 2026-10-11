# Codex Research Brief — SorEventOracle 0.1.3 Early Startup Failure (`0xC0000409`)

**Project:** `D:\Projects\starfield-outpost-research`  
**Mode:** Offline diagnosis and disposable-process qualification ONLY  
**Status:** Implementation/research assignment; **no Starfield launch or attachment authorized**  
**Reference incident:** `center-smoke-20261011-022037-UTC`, 11 October 2026; SOR-EXP-0026 / SOR-D-0046

## 1. Objective and decision boundary

Determine, with the strongest obtainable direct evidence, why the approved external debugger **SorEventOracle 0.1.3** terminated almost immediately with **`0xC0000409`**, before emitting READY or creating its session evidence directory, during the first authorized two-site center-only Starfield smoke attempt. Establish whether the fault originates in the executable, launch environment, tool prerequisites, argument handling, startup/runtime initialization, or another identifiable cause.

**Do not infer a cause merely from the NTSTATUS name.** `0xC0000409` may represent a fail-fast condition and does not alone prove a buffer overflow, a debugger attach, an installed breakpoint, or a Starfield defect. Investigate until the actual failing boundary/subcode/instruction or an equivalently persuasive causal chain is established, or document specific irreducible limits and next discriminating tests.

The expected output is a decision-quality diagnosis and, **only if supported by evidence**, a narrowly scoped fix and disposable requalification. Do not treat “unable to reproduce” or the first uncertain static lead as completion.

## 2. Verified starting evidence and scope

Read the durable documents and actual local receipts before changing code:

- `docs/experiments/event-latency/center-smoke-20261011-result.md` — failure chronology and interpretation.
- `docs/experiments/event-latency/center-only-live-run-card.md` — reviewed launch/preflight procedure.
- `docs/experiments/event-latency/procedure-review.md` — operational checker and qualified assumptions.
- `docs/experiments/event-latency/review.md` and qualification materials — 0.1.3 latency improvement and six disposable controls.
- `docs/experiments/event-instrumentation/review.md` and earlier 0.1.2 qualification — comparison baseline.
- `.local-work/event-oracle-operations/center-smoke-20261011-022037-UTC/` — original private authorization, preflight, process postflight, launch/exit receipts, stdout/stderr and offline-after records. **Keep these artifacts immutable**; do not fabricate a WAL or READY event.
- Approved versioned package: `.local-work/event-latency/review-01/SorEventOracle-0.1.3.zip`; approved executable identified in the run card. Hash both against pinned values rather than rebuilding over them.

The reported first attempt: target preflight passed; Starfield PID 17100 and exact binary/site guards established; external adapter PID 8556 launched at 2026-10-11T02:23:04.1284781Z and exited at 02:23:04.4462634Z with signed `-1073740791` / `0xC0000409`; stdout/stderr empty; no session root/READY/WAL. Subsequent independent postflight on the *same surviving target* confirmed original 32-byte windows and no debugger; game later exited normally and protected saves, reference inputs, game, adapter and ZIP passed post-sync integrity. **Attachment was not confirmed.** No native event or latency was captured.

These are established observations, not a root-cause determination. The evidence-root creation is described as preceding `DebugActiveProcess`; check this precisely in the exact compiled source and executable, including initialization that executes before `main`/argument parsing. Distinguish absent directory because code never reached creation from cleanup, path mismatch, process termination during creation, or reporting/visibility error.

## 3. Workstream A — Reconstruct exact executable startup and failure

1. Inventory the **exact** approved 0.1.3 binary: hash, PE architecture/subsystem, entry point, dependencies/imports, CRT/runtime model, exception/security features, relevant linker switches and versioned source-to-binary provenance. Distinguish static source inspection from verified compiled behavior. Preserve the approved binary unchanged.
2. Trace from process initialization and CRT/static constructors through argument handling, `--reviewed-retail`/PID parsing, path construction, evidence-directory/WAL initialization, target/process validation, and any possible call to `DebugActiveProcess`. Identify the earliest visible durable side effect and failure routes preceding it.
3. Enumerate program paths that can produce fail-fast/`0xC0000409`: explicit fast-fail, stack-cookie or CFG failure, invalid-parameter/runtime abort, unhandled exception transformed by runtime, startup initialization defects, and any platform-dependent equivalent. Differentiate plausible hypotheses from demonstrated behavior; examine PE/disassembly and relevant runtime state where necessary.
4. Investigate Windows Error Reporting and event diagnostics **read-only**: targeted Application/System event entries, WER reports, LocalDumps if already present, crash metadata, fault module/address, exception parameters and fast-fail subcode when recoverable. The original bounded Application-log search found no matching 1000/1001 at the queried time; do not conclude no WER artifact exists. Record timestamp/timezone conversions and negative searches.
5. Review the actual PowerShell `Start-Process` invocation, working directory, hidden window, redirection, command-line quoting, environment, user token/permissions, inherited handles and filesystem paths. Test concrete launch hypotheses rather than assuming hidden mode or redirection caused the failure. Avoid altering system-wide security settings.
6. Explicitly characterize whether any debugger attach, patch, target-process open, or evidence-file operation could have happened *before* the observed termination. Mark unknowns when trace data cannot prove ordering.

## 4. Workstream B — Reproduce safely and isolate cause

Use controlled **disposable executables/processes** and independent scratch directories; **do not launch, resume or attach to `Starfield.exe`**. Begin with the **byte-identical approved 0.1.3 executable**, matching the run card's launch shape where feasible, before testing any modified builds.

- Establish controls for missing/invalid arguments, valid disposable PID, non-running PID, permission failures, output-directory conditions, varied working directory, redirected and unredirected streams, hidden/ordinary launch and expected/bad file hashes as applicable. Do not conflate intentionally rejected inputs with crashes.
- Reproduce or falsify candidate startup-failure explanations with controlled experiments, preserving exact command, environment, hashes, target identity, exit code, stdout/stderr, WER metadata and filesystem side effects.
- When useful, capture an external crash dump or attach a diagnostic debugger **to the disposable adapter process only**, with controlled observation and documented provenance. Prefer fault address, call stack, exception parameters/subcode, and instruction-level evidence to conjecture.
- Do not spoof or bypass reviewed-retail integrity guards to force an attachment. Existing qualification fixtures may be extended *safely* for startup-path testing, but retain original baselines.
- Distinguish **cannot reproduce with disposable PID** from **proven Starfield-specific trigger**: the latter is not established without additional evidence, and a new Starfield attempt is not authorized here.

If a defect is isolated, deliver a minimal corrective patch **without modifying the pinned 0.1.3 archive or executable**. Assign a new candidate version (normally 0.1.4), document changed control/data flow and any impact on the WAL/entry-exit instrument, and explicitly check that the repair does not weaken native-site guards or evidence integrity.

## 5. Qualification and non-negotiable constraints

If any implementation changes are made, rerun the established **six disposable controls**, relevant **12 health assertions** and **11 WAL/inspector tests**, plus new startup regression(s) reproducing the defect or discriminating the diagnosed failure. Add fault-injection/negative-path tests where justified. If no fix is justified, provide the exact reproducible evidence and a ranked investigation plan rather than an unqualified modified binary.

Preserve:

- Pinning of binary/version/source, original native instruction guards, two independent oracle modes and previously qualified 0.1.2/0.1.3 baselines.
- Per-invocation entry/exit association, exception handling, owned single-step and thread-suspension safety, patch restoration, and explicit partial-evidence semantics.
- Durable WAL and recovery semantics, immutable originals, evidence hashes and separate scientific/instrument/target-survival conclusions.
- Both-drive free-space hard guard: **40,000,000,000 caller-available bytes minimum on C: and D:**; fail safely on failed queries. No arbitrary short scientific caps; continue through ordinary optional-field failures when instrumentation integrity survives.
- No changes to saves, Steam/Vortex configuration, SFSE observer 0.1.1, game binaries or repository reference databases.
- No live game launch/attachment, no Starfield process memory access, no unsolicited second smoke, no deployment, staging, commit or push. No system-wide debugger/security configuration change without separate approval.

Do not restart the deferred spinning-reticle investigation or expand into terrain-grid science; both are outside this startup-failure assignment.

## 6. Deliverables and review gate

1. **Root-cause investigation report** under `docs/experiments/event-latency/`: establish timeline, evidence inventory, demonstrated and excluded causes, exact executable/source boundary, repro results, uncertainty and whether attachment was reached. Keep incident facts separate from interpretations.
2. **Startup dependency/fault-path map**: entry point → key initialization stages → first durable side effect → debugger attach, showing static evidence, instrumented evidence and missing proofs distinctly.
3. **Reproduction and qualification artifacts**, including command lines, fixture source and receipts, crash/WER metadata where available, hashes and baseline comparison. Keep private dumps, raw evidence, proprietary files and local paths under ignored `.local-work/`.
4. **If warranted**, new versioned executable/package, surgical patch, added regression tests, full requalification and a changed risk assessment. If no confirmed correction, say so; do not silently promote the original tool to live-ready.
5. **Recommendation for next review decision**: fix approved for consideration, more offline investigation needed, or proposal for a *separately authorized* minimal live diagnostic. Do not schedule or perform such a diagnostic in this task.
6. **Review package** following `WORKFLOW.md`: place diffs in `.local-work/diffs/`, flag `-complete.diff` (all uncommitted tracked and untracked text) and `-task-only.diff` (this work), provide `git status --short`, file/omission manifest, integrity/patch checks and summary. Account for the already uncommitted event-oracle implementation, latency update, run card and failed-attempt record. Do not stage files just to generate diffs. Return review links and candidate hashes, if any.

**Acceptance standard:** We should be able to say precisely what the failed attempt proves, what it does *not* prove, why 0.1.3 died (or which concrete evidence is still missing), and why the next proposed action is proportionate. **No live-run authorization is implied by completion of this brief.**
