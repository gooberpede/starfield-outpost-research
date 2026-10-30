# RG2-D5X — Construction-Winner Observer Feasibility and Qualification

**Project:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research\`)  
**Assignment:** Offline-only design, implementation if justified, disposable-native qualification, independent review, and preparation of *proposed* retail validation cards.  
**Retail operation:** **NOT AUTHORIZED**. No Starfield/SFSE launch, Vortex installation, debugger attach, protected-save mutation, or deployment.  
**Scientific parent:** D5R's broader open reproducibility question; build on D5Q–D5W, especially D5S/D5T/D5U source variability, D5V lifecycle, D5W operational contract, and D5P–R3 instrumentation failures.  
**Publication/B6:** ON HOLD. No staging, commit, push, release, disclosure or integration.

## 1. Controlling question and completion contract

**D5X-Q1:** Can a minimal, version-pinned, in-process observer safely and reliably establish which **original construction query** first takes the qualifying source-map miss for a specified source during a genuinely cold, ordinary construction episode, and which ordinary mask was actually sampled for that invocation?

**D5X-Q2:** Can that evidence be captured and independently qualified without the mutable ordinary-Grid member scan, external debugger exception delivery, or high-volume geometry tracing that limited earlier attempts?

**D5X-Q3:** Can a first retail *instrumentation-validation* session be specified so it diagnoses failures at individual boundaries, without treating hook installation/READY as proof that native events were observed or authorizing scientific acquisition prematurely?

**Target:** the source relevant to **Feynman V Cu IL F / second Feynman V** (verify identity from existing D5 records; analytical source `0:37536:20928:0029d20e`, body FormID `0x0005e0de`), with pinned Starfield 1.16.244.0 research executable and static data **reverified locally**, not assumed. The operator's previously observed Mask 3 correspondence is context, *not* an oracle to select a winner. Retain both Mask 0 and Mask 3 as acceptable genuine observations.

**Question-level outcomes (mandatory project governance):**
- **COMPLETE:** Q1–Q3 are answered by a functioning, qualified offline observation design, authentic integrated receipts, independent reduction, and an executable *proposal* for the first retail validation gate. This is **not** retail qualification.
- **BLOCKED / ESCALATE:** demonstrate the exact indispensable native boundary, unsafe/unavailable mechanism or missing authority; show attempts, counterexamples, viable alternatives, why they cannot proceed under authorization, and the smallest resumption action. Do **not** fabricate a working plugin.
- **INCOMPLETE / REWORK:** a material authorized route remains untested or a mandatory safety/qualification criterion fails. Do not accept a polished feasibility report as closure.

Record frozen questions/criteria and parent linkage at the start in an **active investigation ledger**. Follow material native, threading, record-transport and attribution dependencies within the offline scope. Independent scientific/completeness review must explicitly challenge the highest-value omitted avenue and any premature narrowing.

## 2. Grounding and architecture decision before implementation

Read the actual current `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md`, `docs/reviewers/research-completion-reviewer.md`, and applicable D5P–D5W reports, source ledgers, decisions, failed-run receipts and existing SFSE source/build/test tooling. Inspect the existing project and maintainer-owned `starfield-reference-handles` observer implementations under recorded permissions. Do not assume their code or native addresses are correct merely because historical disposable tests passed.

Before major coding, issue a durable architecture decision comparing at least:
1. Narrowing and reusing D5P-R1 `SorRetainedPopulation` recorder/hooks;
2. A purpose-built, minimal SFSE observer;
3. A smaller alternative native observation boundary, if it can supply the identical claim.

Compare exact evidence value, hook count/call-site coverage, ABI and relocation safety, expected event rate, in-hook work, recorder pressure, source lifetime, implementation/test burden, deployment risk and diagnostic yield on failure. **Prefer the smallest justified design.** Do not rebuild the D5P eleven-hook geometry observer merely by habit. Do not call engine helper functions from a live hook just to establish identity; don't add a mutable ordinary-Grid scan or an unqualified native lock acquisition.

Relevant verified starting *static* boundaries (recheck exact build/instructions): provider `0x14079f860` receives ProcGen in RCX, original Int2 pointer in RDX and aggregate holder in R8; selected-entry load/store near `0x14079fa90–0x14079fa93`; visited guard and exclusive source-pointer map lookup on the provider path; ordinary sampler `0x142339340` called near `0x14079b8e8`. These are **not** runtime addresses. A map miss, wrapper insertion, visited check, generator entry and actual sampled mask are different events; receipt semantics must preserve those differences. D5Q–D5W specify the relevant source selection, provider dispatch, source-lifetime and first-winner constraints.

## 3. Minimum scientific evidence contract

Design a low-volume causal witness that can independently demonstrate:

1. **Readiness and capture coverage:** exact module/DLL/SFSE identities, relocation/prologue checks, each installed observation site, recorder health and a fresh startup nonce/session identity. READY means installed and armed, **not** executed.
2. **Original request:** exact signed Int2 input, ProcGen identity, provider invocation ID (thread and nested/re-entrant identity), and relevant effective descriptor/frame identity or a defensible join to it.
3. **Selection:** source pointer actually selected by the provider's cell cursor, together with independently checked geographic/source identity where safe. A selected pointer is not by itself a stable lifetime token. Preserve null/unknown/unreadable rather than inventing a zero descriptor.
4. **Decision:** visited bypass versus qualified source-map hit/miss, *in the same invocation*, including the exclusive interval that authorizes the construction attempt. A first observed miss is not necessarily the first-ever miss; evidence must qualify a cold source/visited/map state or state the narrower conclusion.
5. **Sample:** a **directly observed** ordinary low-nibble sample associated with that constructing invocation; record the sampled value and sufficient correlation, without retrospectively fitting to visual geometry. Generator prerequisites that skip sampling are separate outcomes.
6. **Continuity:** enough epoch, invalidation, process/thread and invocation evidence to exclude false joins due to source retirement, reset, overlapping providers, pointer reuse, recorder loss or missing observation coverage. Record only necessary lifetime witnesses; avoid pursuing later cache-hit continuity or all geometry points.

The minimal positive claim is **a qualified first constructing query and its sampled ordinary mask** in the specified observed cold episode. It does not require a complete generated population, proven later reuse, extractor result or a frequency estimate. Define weaker outcomes explicitly: provider-only, selection-only, bypass, map hit, miss without sample, context invalid, lost coverage, no relevant call, contradictory chain.

## 4. Acquisition and operational resilience

Preserve the D5P-R1 principle **permissive acquisition, conservative conclusions**:
- Ordinary queue saturation or bounded producer contention does **not** retire the entire observer. Count loss by cause and preserve authenticated records before and after; a loss invalidates only claims whose requisite coverage cannot be proven.
- No arbitrary total event, evidence-byte or healthy-session duration cap. Keep bounded memory queues, safe hot-path work and the existing **40,000,000,000-byte free-space floor on both C: and D:** for any future run. An essential hard guard requires demonstrated engineering reason and separate maintainer approval before retail.
- Avoid indefinite blocking, filesystem I/O, expensive formatting, unbounded traversals or unsafe native lock calls inside hooks. Define output-failure and crash behaviour; keep durable, independently authenticatable prefixes, honest tail uncertainty and explicit losses/flush acknowledgements.
- Prefer timestamp/counter-based chronology plus externally recorded gameplay checkpoints; clock domain, monotonicity and precision must be specified. Diagnostic telemetry itself must not swamp the recorder.
- Provide a failure taxonomy identifying exactly which prerequisite/boundary failed. Absence of a record must never prove absence of native activity without established coverage.
- Instrumentation must not change gameplay/resource state, force generation, alter scheduling deliberately, patch saves, or unload live hooks unsafely. Native code patching necessary for observation remains explicitly version-pinned and separately reviewed.

## 5. Disposable qualification before any retail consideration

Exercise the **actual compiled and packaged instrumentation and evidence reader**, not only mocked JSON or an isolated validator. Use disposable Windows native processes or a rigorously justified equivalent native host with exact production hook code. The integrated rehearsal must cover startup → exact READY → deliberately induced observation events → independent evidence reduction → STOP/finalization → postflight. Distinguish the retail SFSE/game integration boundary that remains untested.

Mandatory positive and negative controls:
- Source selection by fill, edge and corner cells; source absent, invalid/read-failure context, descriptor collision, and source identity distinct from native pointer identity.
- Nested/concurrent provider calls and competing queries; correct request → selected source → visited/map decision → direct ordinary sample linkage, including intentional conflicting masks.
- Visited bypass, existing map hit, actual miss with sampler prerequisite failure, successful sampling, and ambiguous prior-cold-state cases.
- Reset, source retirement, reused pointer, overlapping lifetimes, and interruption between selection and protected construction; demonstrate that unsafe continuity is rejected, *not* promoted by pointer equality.
- Forced single and repeated recorder loss, sustained unpaced native production and recovery, independent intact post-loss chains, crash before/after durable evidence, output failures and damaged/torn evidence.
- Explicit hook-site/version/prologue mismatch refusal; callback ABI/trampoline correctness and timing overhead/burst pressure with observed maxima/percentiles, not a promise of worst-case timing.
- A deliberate diagnostic failure for each scientific boundary, proving the reducer can name the missing prerequisite or uncertainty.

Require repeatable positive claims and adversarial controls on the same compiled version. Preserve contradictory results and unsuccessful development attempts. Tests must show why the former retail 256-member Grid rejection and eleven-hook throughput problem are not inherited, rather than asserting that a different hook count eliminates them. If any old Grid traversal remains, its use and scientific necessity require explicit new qualification; default is to exclude it.

## 6. Two separately gated retail phases — proposals only

Prepare two distinct prospective run cards, **both marked NOT AUTHORIZED**:

**B1 — Instrumentation-validation visit:** maintainer-owned install/enable via Vortex and launch via `sfse_loader.exe`; fresh exact-identity READY before opening Save52; verify real target execution boundaries when they can occur, authenticated evidence, capture health and deterministic diagnostic reduction. A successful startup alone does not qualify the observation boundaries. If save loading is needed to exercise a boundary, identify this explicitly and obtain independent authorization for that exact action. No scientific winner claim required at B1. The first run should be short and operationally controlled but not terminate automatically on an arbitrary time/record quota.

**B2 — Scientific acquisition:** separately authorized only after B1 review; a **genuinely cold and independently qualified** first construction episode for the selected Feynman V source, with agreed ordinary gameplay steps, a predetermined operator STOP, and proof of what fresh state was achieved. Loading Save52 must not be assumed to mean cold construction. No forced cache clearing, resaving, automatic retries or trial repetitions. A later statistical program would require independently reset/new construction episodes, not repeated visits to retained geometry, and its own authorization.

Each proposed card must specify preflight and postflight protected-save/backup/content checks, exact installed versions and hashes, both disk floors, operator-only Vortex removal/disablement, deployed-DLL absence, Steam Cloud verification where applicable, safe crash handling, evidence authentication, and explicit Codex/operator duties. Preserve evidence even from failed or partially complete trials; safety incidents supersede continued capture. No Codex game launch, user-save modification or plugin installation/removal under this brief.

## 7. Research outputs and visualization

Produce a focused design/qualification report and concise observation-boundary diagram showing the actual causal chain and loss/uncertainty points. The diagram is **schematic**, not a spatial map. Any spatial overlay included must use the previously verified **absolute native descriptor-frame coordinates** with genuine outpost centre, beacon where justified and 150-unit boundary; source-relative or outpost-relative axes may only appear as clearly labeled supplementary views. Don't create decorative maps unrelated to this assignment.

Keep exact source/claim evidence and execution/fixture provenance; native disassembly, proprietary binaries, memory and raw captures remain local-only under existing protection/publication policies. Preserve all original D5P failed-run evidence and the D5S–D5W results unchanged. Document the minimal evidence and exact failure discrimination needed for a future retail session; do not imply a historical or retail winner from a synthetic fixture.

## 8. Frozen acceptance criteria

| ID | Mandatory outcome |
|---|---|
| **D5X-AC1 — Authority and identity** | Reverify executable/data/SFSE/observer and repo identities; no game, Vortex, save mutation, staging, commit, push or publication; exact protection and exclusions. |
| **D5X-AC2 — Question, ledger and architectural decision** | Freeze Q1–Q3, success/negative closure and parent; active ledger begun before major work; compare and decide observer alternatives *before implementation* with scientific and safety rationale. |
| **D5X-AC3 — Native boundary sufficiency** | Establish original query, invocation identity, actual selected source, visited/map decision and direct ordinary sample contract without unsafe ordinary-Grid traversal; demonstrate branch/ABI/provenance consistency. |
| **D5X-AC4 — Credible first-construction attribution** | Define cold-state and lifetime/coverage conditions that justify first constructing miss; correctly reject unqualified first-observed, map-hit, visited, reused-pointer and skipped-sample cases. |
| **D5X-AC5 — Implemented qualified candidate or evidenced blocker** | Actual integrated version-pinned plugin and authenticated reader/reducer built and reproducible, *or* terminal BLOCKED proof satisfying project governance. Do not claim implementation PASS if no working candidate exists. |
| **D5X-AC6 — Resilient evidence acquisition** | Ordinary losses do not stop acquisition; finite in-memory safety; authenticated/durable prefixes, truthful loss accounting and post-loss recovery; no unjustified total volume limit. |
| **D5X-AC7 — Disposable integrated and adversarial qualification** | Exercise the exact built hook/recorder/reducer through all required positive, negative, concurrency, invalidation, overload, crash and damage controls; disclose retail integration limitations and timings. |
| **D5X-AC8 — Diagnostic discriminability** | Prove that a failed attempt identifies its first missing scientific boundary or returns explicit uncertainty; READY alone never counts as native event coverage or scientific acquisition. |
| **D5X-AC9 — Two proposed retail cards and protection** | Prepare separately gated B1 instrumentation and B2 science cards, both NOT AUTHORIZED; exact operator/Codex ownership, fresh-episode requirement, READY and postflight, 40 GB guards and STOP rules. |
| **D5X-AC10 — Independent adversarial review** | Separate scientific/completeness, engineering/evidence and editorial review of original questions, native assumptions, exact binary/reader, fixture controls, safety, viable alternatives and omissions; REWORK unfinished in-scope paths, ESCALATE real blockers. |
| **D5X-AC11 — Durable delivery** | Report, architecture decision, boundary/evidence schema, tests and receipts, provenance/source ledger, diagram, candidate package if qualified, review record, exact-hash manifest, complete/task-only diffs including untracked text, status and exclusions. No staging/commit/push. |

## 9. Reporting and exit discipline

Distinguish **scientific qualification**, **instrumentation integrity**, **retail integration readiness**, **target survival**, and **publication eligibility**. A disposable green suite never authorizes Starfield, Vortex or a protected save. An accepted negative method result leaves the larger D5R/winner-preference scientific questions OPEN. Reject unsupported claims that any mask is intended/preferred because it matched a prior observed map.

Codex should diagnose and correct ordinary test failures within this same assignment rather than return the first unresolved hook or recorder issue as a new research proposal. An independent reviewer must identify the strongest remaining plausible authorized route before accepting a BLOCKED claim. On actual missing authority, safety/integrity risk, inaccessible essential dependency or tool/session exhaustion, preserve a durable checkpoint and give the smallest precise request. Do not silently reduce the scientific target to installation readiness.

**No D5X offline result constitutes a retail GO.**
