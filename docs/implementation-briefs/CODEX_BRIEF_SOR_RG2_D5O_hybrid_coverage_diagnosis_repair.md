# Codex implementation brief — RG2-D5O
## Hybrid observer hardware-coverage diagnosis, repair and requalification

**Project:** `D:\Projects\starfield-outpost-research\` (`gooberpede/starfield-outpost-research`)

**Type:** Phase A native debugging / engineering investigation, implementation and disposable Windows qualification. **Phase B retail Starfield execution is NOT AUTHORIZED.**

**Authority:** This brief is the maintainer-approved continuation after the failed D5N Phase B acquisition. Its purpose is to finish diagnosing and repairing the existing hybrid observer rather than move to another partially implemented acquisition architecture. The original first-construction / retained-population scientific question remains unchanged. Refer to `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/SAVE_PROTECTION.md`, and the original research completion/reviewer templates. Freeze AC1–AC8 below at start; only the maintainer may authorize material changes.

### Evidence and inherited facts

Read first:

- `docs/experiments/resource-retained-population/d5n-phase-b.md` and its authorization, source ledger, and independent review.
- `docs/experiments/resource-retained-population/d5n-report.md`, `d5n-contract.md`, `d5n-review.md` and `run-card-d5n-v1.md`.
- `docs/experiments/resource-retained-population/d5m-phase-b-postmortem.md`, `phase-b-postmortem.md`, and existing D5L/D5M acquisition contracts.
- `research/resource-retained-population/` — accepted D5N hybrid adapter, controller, native sources, transport, reducer and Windows fixtures.

The D5N Phase B session authenticated its main-menu ARM/READY barrier with thirteen software breakpoints and hardware DR0 at Grid-clear RVA `0x9829b0`, read back on 91 admitted thread lifetimes. During operator-reported Save52 loading the **first delivered owned software trap** was Reset at RVA `0x79de92`, TID `22364`, lifetime `17`, debug event `261`. After fencing 85 peers, the observer failed the combined predicate

```cpp
GetThreadContext(peer.handle, &v) && hardware_context(v, GridClearVA)
```

with journal text `continuous hardware coverage win32=0`. The journal does **not** identify the failing peer, distinguish API failure from successful context read with a bad register predicate, or contain actual debug-register values. `last_error=0` does not establish that `GetThreadContext` succeeded. The controller then recorded GAP/STOP and terminated the game, without any scientific sample. All recorded continuations succeeded. This is a **coverage-qualification failure**, not demonstrated evidence of lost DR0 coverage, nor evidence concerning the resource source. Do not conflate it with D5L/D5M's earlier software-Grid-clear breakpoint exceptions or infer a shared cause. Protected original inputs and prior captures remain authoritative.

The hybrid is **NO-GO for retail reuse until this assignment is independently accepted and a later Phase B card receives separate maintainer GO**.

### Research question and target

Identify the actual correctness defect, if any, in the D5N hardware-coverage test and related thread/context lifecycle handling; repair it while preserving *continuous, accurately qualified* Grid-clear lifetime coverage and the complete construction → copied retained region → subsequent same-lifetime reuse evidence contract. Produce a reviewed, demonstrably safer hybrid build and a specific proposed run card for the **same** ordinary second Feynman V/Save52 experiment, not a new source or scientific question.

The selected source remains `0:37536:20928:0029d20e` (body `0x0005e0de`); the earlier D5N target and gameplay plan are unchanged unless a concrete newly discovered blocker is documented and escalated. Do not rebuild the resource predictor, change frozen geometry, change resource mask classifications, or begin a new architectural programme.

### Workstream A — Establish the failing state, not merely improve logging

1. Audit the exact D5N coverage predicate, its callers, the peer list, `CONTEXT` setup, thread-handle provenance and suspension ordering. Establish when `GetThreadContext` is legal and meaningful for the particular event/peer thread, including running/stopped/exiting states, thread creation, exit, handle reuse, ownership and lifetime.
2. Re-examine existing D5N protected diagnostic evidence. State exactly what can and cannot be recovered retrospectively. If the recorded data lack the decisive operands, do **not** invent the failure type; design new durable diagnostics.
3. Split the combined expression into individually reported, checked operations. At the immediate point of API return, record its success/failure and `GetLastError` *only when meaningful*, without another intervening API call. On success record actual `ContextFlags`, DR0–DR3, DR6, DR7 and relevant flags plus the expected values and specific failed subpredicate. Bind all diagnostics to PID, TID, verified thread creation identity/lifetime, handle ownership, suspend state, current debug event/site and ordered sequence number.
4. Establish how threads that genuinely exited, are in an authorized transitional state, or are no longer in the admitted coverage set should be handled, using independently supported Windows semantics. **Never treat a live relevant thread with missing DR0 coverage as harmless.** Avoid changing the predicate to “pass if API fails,” skipping unspecified peers or weakening lifetime coverage.
5. Identify and investigate plausible concrete causes: missing/wrong `CONTEXT_DEBUG_REGISTERS` flags, stale or already exited peer handle, suspend/exit race, incorrect DR7/GD assumptions, DR0 being modified or consumed, interference between software trap/TF/RF states and hardware readback, or incorrect expected-thread membership. Treat these as hypotheses until tested. Use authoritative Windows debugger API contracts where material.

### Workstream B — Correct and qualify

Implement the smallest justified correction(s). A legitimate result may be a corrected coverage check, corrected thread-set lifecycle, reliable re-arm/readback operation, or evidence-backed change in when context may be read. Maintain original native site identity and thirteen software probes plus hardware Grid-clear unless a demonstrated defect necessitates a bounded, reviewed equivalent. No removing Grid-clear or replacing same-lifetime fencing with pointer equality. Do not weaken the observer merely to keep Starfield alive.

Qualification must use real disposable Windows debuggees, not Starfield. Include tests that **actually exercise** the previously failing boundary after a Reset-site software trap with many suspended peers; distinguish (a) successful context with correct registers, (b) successful context with individually faulty DR0/DR7/GD values, and (c) failed context reads with properly captured Windows errors. Test early and concurrent thread exits, thread creation and destruction during peer suspension, TID/handle reuse, mixed hardware/software traps, queued exceptions during rearm, actual lost coverage, foreign debug register occupancy, and controlled termination. Confirm a correctly qualified construction/copy/retention/hit chain is still captured in synthetic targets and that misleading joining across source/manager replacement fails closed.

Tests must assert the diagnostic records' actual fields and error classification, not merely count events or inspect an expected string. Include a high-traffic repeated-reset/Grid-clear test that genuinely reaches the decision path, and an injected API failure/relevant-DR0-loss test demonstrating a durable and *correct* stop. Demonstrate retained SRO1/ACK integrity and durable control evidence before continuation where required. Do not infer retail reliability merely from 100% synthetic pass rate.

If an architectural or environmental limit makes the required coverage impossible, retain the demonstrated counterexample and produce a concrete **NO-GO** with alternatives and missing capability. Do not report a repaired/qualified observer on the strength of diagnostics alone or relax AC4/AC5. Investigate viable in-scope corrections before escalating; do not bounce into an SFSE, native-code reconstruction or different debugger programme without a maintainer decision.

### Workstream C — Phase B readiness (proposal only)

If Phase A passes, prepare a revised `run-card-d5o-v1.md` (or appropriately named durable card) that retains the natural first-construction opportunity: same ordinary-user unelevated account/session; new process at main menu; verified pre-load ARM/READY barrier; protected Save52; ordinary travel to the second Feynman V outpost; no forced regeneration, cache manipulation, alternate target, or automatic retry.

Pin the newly qualified binary/source/fixture hashes and exact observation sites. Describe *what evidence is expected* and differentiate: (1) completed construction, (2) completed retention without later map hit, (3) same-lifetime reuse, (4) cache/visited observation only, (5) no hit under qualified coverage, (6) failed/unknown coverage. An observation is not “first ever” merely because it is the first captured. State correct treatment of contradictory masks and geometry without fitting predictions.

Preserve the 40,000,000,000-byte free-space guard on both C: and D:, exact installed EXE/ESM/PlanetData identities, protected saves and backups, approved Cloud state and the current `remotecache.vdf`-as-diagnostic policy. Existing known historical discrepancies remain historical; no automatic baseline repair. A crash or intentional termination **after complete, independently authenticated decisive evidence is durably retained is acceptable**, subject to protection/postflight; clean Starfield shutdown is not an acceptance condition. A pre-evidence crash or missing coverage is an incomplete acquisition. No arbitrary healthy-session duration or sample quota. Do not authorize an actual live launch or attachment in this assignment.

### Working-material policy and proportionality

- Existing original captures, saves, backups, installed binaries/definitions and accepted scientific evidence remain protected and hash-bound. Use active archive-backed verification for relevant inputs; do not regenerate the obsolete 93,334-loose-file audit or start archival/housekeeping work.
- Task-owned temporary `.py`, `.json`, build outputs, failed disposable fixtures and intermediate diagnostics under a clearly bounded scratch folder may be replaced or discarded at Codex's discretion. Do **not** enroll every scratch file in a permanent global protected-input roster. Preserve decisive failure evidence, exact tested build identity, compact test results and necessary reproducibility instructions.
- Maintain substantive failed experiments and counterexamples in the durable record, but do not retain an unbounded tree of redundant attempt files. Do not delete pre-existing material without authority.
- Do not stage, commit, push, create a release, modify game saves/installed content, use an actual Starfield process or publish proprietary native code.

### Frozen acceptance criteria (AC1–AC8)

| AC | Mandatory test |
|---|---|
| **AC1 — Authority and integrity** | Offline/native analysis and disposable Windows targets only; active archive-backed baseline and all relevant protected originals verified unchanged; no game execution or Git staging/commit/push. |
| **AC2 — Forensic diagnosis** | Exact old boundary and its insufficiencies established; handle/context/thread-state and register-coverage hypotheses investigated. A concrete defect is identified and repaired where evidence supports it, or an evidenced specific unresolved state/limit is recorded; historical cause is never invented. |
| **AC3 — Diagnostic fidelity** | API success vs failure, immediate meaningful error, exact peer/lifetime and register/subpredicate diagnostics are durably captured and validated, without changing scientific sample claims. |
| **AC4 — Correct coverage handling** | Actual relevant live-thread DR0 loss still stops fail-closed; benign proven lifecycle transitions are handled correctly; necessary Grid-clear and source-lifetime fences remain. Unqualified state is not promoted. |
| **AC5 — Actual Windows qualification** | Targeted executable fixtures demonstrate the diagnosed/repaired path (including reset→peer coverage, thread exit/reuse, mixed rearm/queued traps, failures and complete synthetic scientific chain). All mandatory scenarios pass; negative controls are preserved. |
| **AC6 — Retail decision** | If qualified, a complete revised Phase B card binds exact build, target, risks, natural gameplay, durable evidence, crash tolerance and postflight with explicit NOT AUTHORIZED status; if infeasible, documented NO-GO with specific evidence and alternatives, not a misleading ready card. |
| **AC7 — Durable record and proportionality** | Concise diagnosis, code changes, exact methods/hashes, meaningful failures, test results, editorial review and prudent scratch handling; no large unnecessary historical reaudits or resource predictor/archival detours. |
| **AC8 — Independent review and delivery** | Separate read-only scientific and engineering assessment of original contract, exact implementation, decisive native/Windows results, failure classifications and editorial quality; mandatory PASS/FAIL/NOT TESTED ledger; exact complete/task-only diffs, status, inclusion/exclusion manifests, forward/reverse verification and separately reviewed final delta where needed. |

**Completion rule:** Successful Phase A engineering closure requires passing the mandatory repaired-coverage and Windows qualification criteria; a well-documented failure or engineering non-go is truthful scientific/feasibility evidence but **not** an automatic engineering ACCEPT. Where a specific Windows/Starfield distinction cannot be resolved offline, identify it and do not claim retail safety. A reviewer must not turn an unresolved required capability into PASS merely because a report is detailed. If mandatory criteria fail within the authorized technical scope, continue diagnosis/correction and requalification; escalate only a genuine evidenced blocker or required new authority.

### Required delivery

Deliver a concise `docs/experiments/resource-retained-population/d5o-report.md` or equivalent, revised native implementation and focused tests, source/provenance register, acceptance table, independent review, and (only when justified) a Phase B run card. Include the exact final source/build/policy identities and observed versus inferred limitations. Produce verified complete and task-only diffs including untracked files; expose their locations and SHA-256 hashes. Respect `docs/EDITORIAL_STANDARD.md`, complete manual review and final exact-delta review. Recommend a commit message only upon mandatory acceptance. Preserve prior D5N failure record and the unchanged frozen resource-science conclusions.

**Not authorized:** Any retail Starfield launch/attach, a new live run, source/planet change, arbitrary debugger architecture replacement, SFSE-plugin or P-code reconstruction project, forced regeneration, save write/restoration, or publication/B6 activation. The maintainer must separately authorize Phase B after reviewing Phase A.
