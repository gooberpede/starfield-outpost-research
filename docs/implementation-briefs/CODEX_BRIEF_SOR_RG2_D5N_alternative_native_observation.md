# Codex implementation/research brief — RG2-D5N
## Alternative Native Observation Feasibility and Scientific Coverage

**Project:** `D:\Projects\starfield-outpost-research\`  
**Authority:** Phase A only — offline native analysis, implementation where justified, and disposable Windows-process qualification. **No Starfield launch/attachment, retail code patching, new save operation, or Phase B execution.**  
**Follow-on:** One proposed Phase B retail run card requiring separate explicit maintainer GO.  
**Status:** Proposed original contract; freeze AC1–AC8 before execution.

## 1. Scientific purpose and inherited baseline

Two independently documented retail attempts with the D5L/D5M fourteen-site software-breakpoint observer ended with `0x80000003` at the armed Grid-clear RVA `0x9829b0`. The D5M control journal recorded no corresponding exception delivery on the faulting main thread, although its recorded continuations succeeded. Earlier handle-ownership defects were corrected; the initiating cause remains **UNKNOWN**. Do not attribute it to a particular Windows fault without evidence and do not reauthorize the existing fourteen-INT3 configuration by default.

The research question remains: **Does a source's first successful resource-construction query determine the region population retained and later reused by the native ProcGen manager?** D5C established process-local source-pointer-keyed retention and hit bypass; D5H/D5I established conditional alternative first-miss masks for six researched sources. Neither proves an actual historical first construction and later reuse for Save52.

Primary prospective target remains chart-0 second Feynman V source `0:37536:20928:0029d20e`, owner `0x0005e0de`, with qualified mask 0/3 alternatives and D5B mask-3 native consumer geometry. Protected Save52 and installation pins remain as in the committed D5M run card. Preserve historic conclusions and explicit unknowns.

Read first: `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/templates/completion-contract.md`, `docs/reviewers/research-completion-reviewer.md`, `docs/experiments/resource-retained-population/d5m-phase-b-postmortem.md`, `docs/experiments/resource-retained-population/d5m-phase-b.md`, `docs/experiments/resource-retained-population/debugger-repair.md`, and the current D5M run card. Follow actual repository state if names/paths differ; record divergences rather than guessing.

## 2. Governing experimental principle: evidence survival, not graceful target exit

**A clean Starfield shutdown is optional. A crash, intentional termination, or other abrupt end is not by itself a scientific or operational failure, provided the decisive evidence was durably flushed, authenticated, and available before termination; protected saves/content remain intact; and the end condition and incomplete coverage are accurately reported.**

Conversely, a zero process exit code, healthy collector, or complete-looking journal cannot substitute for intact decisive evidence. A crash **before** the necessary capture is a non-hit or failed acquisition, not a positive scientific result. An unexpected crash must be documented and analyzed to determine whether it invalidates the causal chain or warrants changing the method. Do not sacrifice crash-tolerant evidence durability to pursue graceful detach. Preserve safe containment, target identity, save protection and operator STOP behavior; do not suppress exceptions or claim target survival without evidence. A clean shutdown is useful engineering information, **not an acceptance gate** for a scientifically complete capture.

## 3. Phase A work programme

### A. Minimal native observation contract

Trace the existing pinned implementation and earlier acquisition evidence to identify the minimum native witnesses necessary for:

1. **Construction input:** qualified manager/source identity and lifetime, initial caller query and effective frame, actual sampled ordinary mask, and first observed map miss/visited state.
2. **Completed population:** evidence that region geometry was successfully copied into a retained source wrapper/collection—not merely wrapper allocation, insertion, visited marking or return status.
3. **Reuse:** a later map hit for that same retained population, or another native-equivalent reuse witness proven to carry identical region bytes in the **same** qualified lifetime.
4. **Lifetime fences:** reset/replacement/destruction, source-pointer reuse and relevant manager changes; identify how a reduced observer avoids falsely joining different lifetimes.

Classify each witness as indispensable or replaceable by an explicitly demonstrated stopped-thread snapshot. A complete source census and Workshop callback are optional for this witnessed-region claim. A first **observed** construction must not be called first-ever or the historical Save52 construction. No correlation by geographic label, pointer or timestamp alone counts as causal ancestry.

### B. Compare acquisition approaches before substantial build work

Make a compact evidence-based decision matrix for:

- **Hardware-first Windows debugger:** per-thread DR0–DR3 constraints, actual thread creation/inheritance, thread and process identity, register/snapshot access, and ability to maintain coverage with no INT3 patches at Grid-clear.
- **Hybrid:** precisely which sites remain software-patched and why; do not assume a hybrid is safe just because Grid-clear moves to hardware.
- **In-process native observer:** potential observation fidelity, required injection/plugin/loader mechanism, invasiveness, thread/scheduling effects and qualification burden. No retail deployment in Phase A.

Assess whether the Grid-clear fence can be replaced by a provably equivalent lifetime mechanism (e.g. manager generation/state, retained ownership and intervening allocation/reset barriers); do not silently omit it. Evaluate minimal event/snapshot designs that reduce required simultaneous traps. Record which claims would be lost if reduced coverage is unavoidable. Prefer the lowest-risk method capable of complete causal evidence; don't build a large new framework if the existing architecture can be responsibly reused.

### C. Implement and qualify where justified

If a defensible approach is feasible within this task, implement the minimal observer/adapter in maintained research code and qualify it with **real disposable Windows processes**. Test at least: relevant first miss → completed region → same-lifetime reuse; later different query with retained geometry; source/manager reset and same-address reuse; concurrent requests; early and repeated thread creation/exit; rapid Grid-clear-equivalent activity; interrupted collection and crash **after** durable ACK; crash **before** complete evidence; lost coverage or corrupted/incomplete receipts; safe containment and postflight identities. Include contradictory masks/geometry and unexpected event ordering as controls. Preserve failures that materially affect interpretation without pinning every scratch artifact.

If no approach can credibly establish the indispensable chain, deliver a rigorously bounded **NO-GO feasibility result**, including exact missing witnesses, alternatives actually investigated, demonstrated failures/risks, and a narrow recommendation. Do **not** label an unimplemented design an accepted implementation or dilute the evidential contract to force ACCEPT. A genuine unresolved prerequisite is a specific escalation, not an invitation to another broad infrastructure programme.

### D. Operational design and proposed Phase B card

Retain second Feynman V as default, with main-menu observation before loading Save52 and ordinary travel. Only recommend a target change if evidenced information gain or feasibility justifies it. No forced resource regeneration, cache resets, saved-game mutation, arbitrary repeated sessions or automatic retries. Maintain ordinary unelevated Windows account/session checks, pinned executable/ESM/PlanetData and observer identity, Cloud-state confirmation and the prospective diagnostic-only treatment of `remotecache.vdf`. Preserve the C:/D: **40,000,000,000-byte free-space floor**, protected research saves, independent backups and fresh checks. Historical four-ZIP discrepancy remains historical; don't silently repair or relax scientific pins.

The run card must specify the actual observer architecture, exact sites or native hook endpoints and admitted interventions, pre-attach/ARM-READY barrier, operator actions, real-time receipt/ACK durability, explicit STOP/crash/termination handling, postflight, source-lifetime verification, evidence-tier interpretation and a one-session approval boundary. In particular, a **post-capture crash is acceptable when verified data survives**. Do not impose arbitrary elapsed-time, receipt-volume or healthy-session quotas. Phase B remains **NOT AUTHORIZED** until maintainer approval after review.

## 4. Evidence and workspace discipline

Use the **active archive-backed preservation baseline**, verifying exact task scientific inputs, designated protected saves/backups and necessary installed content. Avoid obsolete whole-corpus loose-file scans and unrelated archive migration. Read-only research means protecting original inputs, not freezing `.local-work/`. Task-owned temporary code, test logs, JSON and failed intermediates may be overwritten/removed; retain concise decisive counterexamples, primary evidence required for findings, and reproducible final methods. No new dependency installations, staging, commit, push, publication, or alteration of historical scientific classifications without separate authority. B6 remains on hold.

Distinguish scientific evidence integrity, observer safety, target process survival and protected-input integrity as **separate** result dimensions. Target survival is not a proxy for data validity.

## 5. Frozen completion contract and acceptance criteria

**Task type:** Bounded native feasibility / research implementation and offline engineering qualification.  
**Mandatory output:** Method-selection rationale, minimal causal contract, qualified implementation **or** evidenced NO-GO, tests/primary evidence, Phase B proposal as applicable, reviewed documentation and exact delivery package.  
**Negative-result completion:** An independently scrutinized infeasibility conclusion must demonstrate investigated viable routes, concrete blocking evidence and lost scientific capability; no mere unsuccessful prototype or arbitrary time exhaustion.  
**Authority boundary:** Only Phase A work. New live execution, installation or protected modification requires explicit maintainer approval.  
**Continuation:** Diagnose in-scope failures, correct and retest rather than stop at a first test failure; preserve decisive failed cases.  
**Review:** Independent scientific and engineering reviewer, editorial review of changed text, and exact final-snapshot/delta review under existing protocol.

| AC | Mandatory requirement |
|---|---|
| **AC1 — Authority and protection** | No retail Starfield run or attachment; protected inputs unchanged; active archive-backed checks and free-space safeguards respected; task-owned scratch treated as disposable by default. |
| **AC2 — Feasibility comparison** | Evidence-based hardware-first, hybrid and in-process assessment, with explicit intervention, risk, cost and scientific-coverage trade-offs. |
| **AC3 — Minimal native contract** | Exact required construction, mask, completed retained geometry, same-lifetime reuse and lifetime-fence witnesses identified; alternative snapshots prove equivalent information or retain limitations. |
| **AC4 — Acquisition qualification / honest NO-GO** | Working method qualifies the contract in disposable Windows processes; **or** genuinely evidenced feasibility blocker and separately classified engineering NO-GO. Do not misreport a design-only outcome as a working observer. |
| **AC5 — Scientific discrimination and durability** | Valid and contradictory synthetic histories distinguish complete, partial, missed and invalid ancestry; independently authenticated decisive evidence survives a deliberately terminated/crashed target where capture preceded termination. **Graceful exit is not required.** |
| **AC6 — Live readiness** | If qualified, a complete source-specific Phase B run card with exact admission, controls, operator actions, stop/recovery rules and no implicit GO; otherwise explicit missing prerequisites and NO-GO. |
| **AC7 — Reproducibility and proportional evidence** | Decisive evidence, relevant input hashes, meaningful failures, concise scientific/engineering report, usable methods, proportionate tests and editorial finalization; avoid scratch-file proliferation. |
| **AC8 — Independent completion review** | Independent scientific/engineering challenge of actual code, primary tests and all ACs; exact complete/task-only diff manifests and hashes, final editorial review, closure-delta review as needed. No staging/commit/push. |

**Disposition discipline:** For each AC record PASS / FAIL / NOT TESTED with exact supporting evidence. If AC4 cannot qualify an actual observer, report the bounded scientific feasibility finding and engineering NO-GO explicitly; the reviewer may accept an adequately evidenced negative feasibility study while leaving engineering/live readiness unfulfilled. Never move the goalposts or treat a safe crash after durable data capture as failure solely because the game did not exit cleanly.

## 6. Delivery

Produce durable project documentation, a concise evidence/qualification matrix, new code only when warranted, a proposed run card or evidenced NO-GO, independent reviewer record and exact complete/task-only patches including untracked deliverables. State current HEAD and worktree/index baseline, frozen input identities, selected design, observed tests, unproven assumptions, genuine residual risks, and next required maintainer decision. Preserve the historical D5L/D5M post-mortems and frozen D5C–D5I resource conclusions unchanged.

**Do not conduct Phase B during this assignment.**
