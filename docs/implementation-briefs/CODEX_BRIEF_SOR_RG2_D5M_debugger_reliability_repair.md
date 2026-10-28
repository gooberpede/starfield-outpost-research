# Codex implementation brief — RG2-D5M

## Debugger Reliability Repair and Requalification (Phase A)

**Project:** `starfield-outpost-research`  
**Status:** Proposed, authorized for **Phase A offline/native analysis, repair and disposable Windows qualification only**. **Phase B retail Starfield execution is NOT AUTHORIZED.**  
**Date:** 2026-10-28 (Australia/Sydney)  
**Primary reference:** `docs/experiments/resource-retained-population/phase-b-postmortem.md`  
**Related records:** `phase-b.md`, `phase-b-sources.csv`, `run-card.md`, `native.md`, `validation.md`, `review.md` in the same experiment directory; `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `WORKFLOW.md`, `AGENTS.md`.

## 1. Original question and reason for this assignment

RG2-D5L Phase B failed during travel before it could establish the construction–retained-population–reuse chain. The observed retail sequence included an initial access-denied debugger attachment under `typhon\codexsandboxoffline`, followed by an approved ordinary-user attempt that armed fourteen software-breakpoint sites, observed source initialization and Grid-clear traffic, and ended unexpectedly.

Preserved Windows Error Reporting identified **exception `0x80000003` at module-relative offset `0x9829b0`**, exactly the armed `native_grid_clear` site (runtime address in that process `0x7ff6215629b0`). The final scientific capture was not an exception-context/continuation record, so the specific delivery, rearm or continuation failure is **unknown**. Do not declare a root cause by association alone.

Independent static review separately established a **real debugger-event handle-ownership defect** in `research/resource-retained-population/controller-tail.inc`: the controller retained handles borrowed from CREATE debug events and closed them itself on exit/dead-peer/cleanup paths. Windows owns those event handles; independently retained handles require explicit duplication/opening and clear single-owner closure. Two thread-exit events (TIDs 21752 and 22888; journal lines 95–96) exercised the defective path *before* native sample 1. There is no established causal link from this defect to the later Grid-clear failure.

**Scientific requirement:** Repair and requalify the observer so that a subsequent, separately approved D5L live run can positively observe an initial source request/mask, completed region creation and retained ownership, and subsequent same-lifetime lookup/reuse. A stable observer that drops lifecycle fences or yields only decision-level evidence is not an acceptable substitute.

## 2. Authority, fixed scope and exclusions

**Authorized now:** Read the pinned local native analysis, previous reports and source; inspect an existing crash dump if available **read-only** and securely qualified to the D5L target; investigate Windows debugger event/exception ownership semantics; modify the task's observer/collector and directly dependent native orchestration and tests; build and test against disposable Windows processes; use bounded static Ghidra/native analysis if needed; prepare an updated proposed Phase B run card; independently review and package changes. Prefer reusing accepted D5L infrastructure rather than creating a new framework.

**Not authorized:** Launch or attach to Starfield; modify game executables, ESM/BA2, Steam configuration, protected save files or independent backups; force resource generation, reset caches, alter Save52, change the planetary target, enter game for a test; delete original evidence; perform archival migration or historical scratch housekeeping; commit/stage/push/publish; automatically approve or execute Phase B. B6/publication remain on hold. Any materially different live intervention or new target needs the maintainer's separate approval.

Continue using **the active archive-backed preservation baseline**. Verify directly relevant protected inputs and installed identities; do not recreate obsolete 93,334-loose-file audits. Preserve the existing Steam `remotecache.vdf` diagnostic (non-blocking) amendment and strict protections for actual designated saves and backups. Respect the existing **40,000,000,000-byte free-space floors on both C: and D:** for applicable operations.

**Research scratch policy:** `read-only` constrains protected inputs, not task-owned scratch. Codex may overwrite/remove its own disposable intermediate scripts, build scratch and test JSON; do not add every transient output to a permanent global pin inventory. Preserve decisive failed tests/counterexamples, final qualification receipts, essential primary evidence and the final independently reviewed methods. Do not indiscriminately delete older research material.

## 3. Mandatory engineering work

### A. Diagnose the observed failures without prematurely choosing a cause

1. Re-read the full post-mortem, failure timeline, original observer source and qualified test contracts. Account for the **two early thread exits**, rather than relying on a final-journal suffix.
2. Locate any already-existing WER dump, its metadata and access restrictions. If available, inspect it read-only for matching PID/process lifetime, faulting thread, exception context, owned site, breakpoint bytes and relevant thread state. If unavailable or inadequate, say precisely so. **Do not create another retail dump.**
3. Independently inspect the event-handle, exception, `ContinueDebugEvent`, trap/rearm and peer-fencing paths. Distinguish *confirmed defect*, *observed retail failure*, *supported causal theory* and *unknown*.
4. Record alternative explanations and what each would predict. Repair defects even if their historical causal contribution cannot be proved.

The native `Grid-clear` breakpoint is a **lifetime fence**; simply removing, suppressing or silently disabling it is not a repair. A replacement must provide equivalent ancestry/lifetime evidence and be separately qualified.

### B. Repair handle ownership and launch admission

1. Track the origin and ownership of every process/thread handle: borrowed Windows debug-event handles; explicitly duplicated handles; handles obtained via `OpenThread`/`OpenProcess`; temporary handles; and any aliases held in maps/queues. Define exactly who closes each owned handle and when. Never close borrowed event handles.
2. Check handle duplication/opening and closing failures, PID/TID reuse, stale queued events, early exits, process exit and `ContinueDebugEvent` transitions. Do not correlate distinct thread lifetimes by reused numeric handles.
3. Require **ordinary-user account compatibility before consuming the live admission**; do not retry attachment under the sandbox account or demand administrator elevation. A concrete user/context mismatch must fail with useful diagnostics and no Starfield mutation. Do not weaken Windows security settings.
4. Preserve the one-use, exact-build, process-creation-time and image-identity gates. Existing Cloud-metadata diagnostic treatment remains intact.

### C. Repair/diagnose Grid-clear exception and rearm correctness

1. Persist durable low-overhead event-control diagnostics **before continuation**: sequence, PID/TID and lifetime, debug-event kind, exception code and address, first-/second-chance, site identity, original instruction-byte/readback status, thread/site step owner, stop/rearm state and chosen disposition.
2. Record `ContinueDebugEvent` return and actual error code, breakpoint restoration, RIP rewind, TF ownership and clearing, single-step delivery, site rearming/readback, peer suspend/resume transitions, created/exited threads and handle ownership/close results. Ensure diagnostics survive target or controller failure without masquerading as qualified scientific samples.
3. Investigate simultaneous/successive `Grid-clear` and source-init hits, queues during one-byte restore/single-step, exceptions that are not owned breakpoint events, unexpected trap instruction bytes, thread creation/exit during arming and rearm, and stop/teardown behavior.
4. Fail closed on lost ownership, missed coverage or unsafe continuation. Do not indiscriminately swallow `0x80000003` or report an exceptional termination as an ordinary completed acquisition. Do not degrade scientific observations merely to keep the target alive.
5. Engineering latitude: use corrected software breakpoints, a targeted hardware/software hybrid or a different qualified observer mechanism **if justified by specific evidence**. Preserve logically continuous source-decision, successful region-copy/ownership, same-lifetime reuse and reset/destruction fences. Material instrumentation changes require corresponding focused qualification, documentation and review—not an implicit live authorization.

### D. Qualify against real disposable Windows processes

Reproduce the relevant conditions and then stress the repaired mechanism. Include at least: early post-arm thread exits before first native sample; reused TIDs/handles; same-thread and concurrent `Grid-clear` bursts; source-init/Grid-clear interleaving; pending queued traps on same and different sites; thread start/exit during rearm; nested events; deliberate `ContinueDebugEvent`/handle/byte-readback failure; unexpected first- and last-chance breakpoint events; collector/pipe failure and STOP; and process teardown.

The **scientific positive fixture** must demonstrate a source-qualified miss → original query/mask → successful actual region append and copied retained geometry → source/wrapper/lifetime-joined later hit of identical data. The **negative fixtures** must prevent spurious completion when a wrapper is inserted but generation fails, the visited guard bypasses lookup, a pointer is reused after reset, or coverage is incomplete. Preserve contradictory observations.

Use the real Windows debugger architecture in disposable targets, not merely a mocked reducer. Apply realistic concurrency and sufficient repeated traffic to exercise the previously failing path; set no arbitrary healthy-session wall-clock or scientific-event quota. Retain focused regression tests for relevant inherited D5L contracts; do **not** rerun unrelated historical geometry experiments or launch a fresh source-selection project.

## 4. Phase B readiness — proposed only

Prepare a revised run card under `docs/experiments/resource-retained-population/` based on the existing D5L card. Preserve unless concrete evidence requires a separate decision:

- **Target:** second Feynman V, chart 0, source `0:37536:20928:0029d20e`, planet owner `0x0005e0de`.
- **Protected save:** Save52 original SHA-256 `6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.
- **Start:** normal ordinary-user launch to main menu; full verified instrument arm/readback before operator loads Save52.
- **Gameplay:** one load and ordinary travel to the target, no forced generation, cache reset, Build Mode requirement, site substitution or automatic second run.
- **Risk:** software breakpoints/all-stop timing alter execution; unsafe loss still leads to controlled termination; no unqualified safe-detach claim.
- **Gates:** exact current native build and module hashes, saved/protected checks, active archive-backed baseline, installed content identity, transient-save and nonblocking Steam metadata policy, operator confirmation of Cloud state, both disk floors, definitive one-use GO with source and PID creation-time binding.
- **Results:** distinguish attachment failure, breakpoint engineering failure, bounded scientific non-hit, retention without later hit, and qualified complete same-lifetime chain. None implies a confirmed mask/bug explanation absent direct operands.

Deliver a specific versioned run-card diff, identified observer build/qualification artifacts and a **GO/NO-GO recommendation**. Phase B remains `NOT AUTHORIZED`; an independently accepted Phase A does not constitute operator approval.

## 5. Frozen acceptance contract — AC1–AC8

| Criterion | Mandatory completion condition |
|---|---|
| **AC1 — Authority and protection** | No Starfield run/attachment or protected input mutation; explicit active archive-backed pre/post checks on actually relevant sources; actual HEAD/index and authority recorded; task-owned scratch appropriately managed. |
| **AC2 — Fault investigation** | Full post-mortem reconciled, existing dump inspected if available, confirmed handle defect distinguished from Grid-clear failure, supported alternatives/remaining unknowns documented; no invented historical root cause. |
| **AC3 — Debugger correctness** | Handle ownership repaired; exact event/exception/continuation/rearm/peer handling implemented with durable failure diagnostics and fail-closed behavior. No removal of Grid-clear without equivalent proven fence. |
| **AC4 — Scientific coverage** | Repaired instrument demonstrably captures completed native geometry and subsequent same-lifetime reuse, preserving first-observed vs first-ever, wrapper-only vs completed, map hit vs visited bypass, and reset/pointer reuse distinctions. |
| **AC5 — Windows qualification** | Focused real-process adversarial/stress scenarios pass, including early exit, handle reuse, Grid-clear traffic, queued traps, exception/continuation errors and STOP, plus relevant D5L regressions. No unexamined material failure remains. |
| **AC6 — Retail readiness** | Executable updated Phase B run card, exact build/site/qualification pins, launch identity and risks, admission/STOP/postflight and non-hit classifications; separate GO retained. |
| **AC7 — Durable/economical record** | Concise report of findings, faults/corrections/negative tests, bounded decisive receipts, versioned code, reproduction instructions, full changed-text manual editorial pass and independent review-ready package. Disposable scratch does not become globally protected. |
| **AC8 — Independent acceptance** | Independent scientific **and engineering** review of exact snapshot, explicit AC1–AC8 PASS/FAIL/NOT TESTED with evidence references and editorial disposition; reviewer issues REWORK for unmet mandatory items; independently reviewed final delta if delivery changes after acceptance. Complete and task-only diff manifests/hash/application checks, no staging/commit/push. |

### Negative results and escalation

A root cause that cannot be retrospectively proved from existing D5L evidence is **not** by itself a failure of AC2 if the alternative hypotheses and repair/diagnostic qualification are complete. Conversely, fixing only the known handle bug does **not** satisfy AC3/AC5 without characterizing and covering the Grid-clear failure modes.

If substantial bounded engineering shows no safe method capable of preserving the scientific chain in the allowed observer architecture, return an independently reviewed **REWORK/ESCALATE with specific missing capability**, not a nominal ACCEPT for a weaker decision-only collector. Do not relax AC4, change target or authorize retail experiments to force completion. In-scope diagnostics, reasonable architectural alternatives and focused requalification remain Codex's responsibility; a failed first test is not an automatic handoff.

## 6. Completion and review workflow

1. Follow project `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md` and the independent reviewer instructions. Original ACs are frozen; any material change requires maintainer approval.
2. Distinguish scientifically decisive original evidence, correct/reproducible code and final results from replaceable task-owned scratch. Preserve original D5L failure records and material failed qualification counterexamples; do not preserve endless ephemeral JSON/temporary `.py` as mandatory scientific inputs.
3. Perform proportional pin checks; verify pinned Starfield.exe **1.16.244.0** SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` and relevant reference data when actually accessed, without an obsolete loose historical audit or unrelated requalification.
4. After implementation/tests, screen and **manually read all changed authored prose, docs, scripts' meaningful comments and navigation**. Correct issues before independent review. Record editorial completion; independently review the exact final implementation and statement of evidence. If final closure record alone changes, a narrow independent delta review suffices.
5. Deliver a concise implementation report, revised run card, test/result summary, independent-review matrix, exact complete and task-only diffs including preexisting untracked changes, inclusion/exclusion manifests, source/build/receipt hashes, and suggested commit message **only if AC1–AC8 pass**. Do not stage, commit, push or publish.

**Definition of completion:** Phase A provides an independently qualified, scientifically complete *capability* to witness first observed source construction, retained geometry and subsequent reuse in a disposable Windows process, together with a specific reviewed proposal for repeating the D5L live experiment. It does not require the native hypothesis to be confirmed by retail Starfield; Phase B remains separately gated.
