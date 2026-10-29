# RG2-D5P-R3 — Grid Membership and Context Validation Repair

**Project:** `starfield-outpost-research` (`D:\Projects\starfield-outpost-research\`)  
**Assignment:** Offline native Grid/membership investigation; evidence-justified validation repairs; disposable native qualification; independent review; proposed retail run card.  
**Retail phase:** **NOT AUTHORIZED**. No Starfield/SFSE launch, Vortex install/enable/disable, deployment, live sampling, or protected-save/configuration mutation. A later retail experiment requires a separate explicit maintainer GO.  
**Current scientific status:** D5P retained-population hypothesis **UNRESOLVED**. R2 retail diagnosed an observer inspection bound, not historical source construction/reuse. B6/publication **ON HOLD**.  
**Governing rule:** **Permissive acquisition; conservative conclusions.** Freeze R3-AC1–R3-AC9 before work begins.

## 1. Purpose and evidence baseline

The D5P-R2 retail diagnostic captured **9,736 authenticated admitted records**, including **6,101 source-demand observations** rejected at validator **reason 24 (`GridCoverageLimit`)**. The reported native Grid **count was 324, capacity 512**, while the observer's inspection bound was **256**. This is an *observer-imposed coverage limitation*: the count is within the reported capacity. **5,190 queue-full losses** make coverage incomplete. In admitted demands, checks after the coverage predicate (including membership and later lifetime/identity checks) were not reached; do not claim they passed or failed. The original D5P Phase B 319 context-invalid demands, its historical precise cause, the selected-source causal chain and retained-population hypothesis remain unresolved. Preserve these distinctions in all reports and readers.

**Objective:** Establish the game's actual Grid representation and defensible source-membership semantics; remove/repair the artificial 256-member barrier where native evidence warrants it; execute and discriminate the *subsequent* context predicates in realistic disposable tests; preserve strict failure on genuinely malformed, unreadable or ambiguous contexts. The acceptance target is **not** merely changing `256` to `512` or producing a successful 324-member synthetic case. The retail candidate must remain explicitly unverified until a separate live run.

**Primary eventual retail witness (unchanged):** Save52, second Feynman V source `0:37536:20928:0029d20e`, chart 0, owner FormID `0x0005e0de`. Historical conditional masks 0/3 and native geometry are held-out evidence, not values to fit or force through context validation.

## 2. Mandatory repository and native-baseline inspection

Before coding, read current `AGENTS.md`, `WORKFLOW.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/SAVE_PROTECTION.md`, `docs/EDITORIAL_STANDARD.md`, the original D5P brief and implementation, D5P Phase B and R1/R2 briefs/reports/reviews/ledgers, particularly `docs/experiments/resource-retained-population/d5p-r2-retail.md`, its authorization, source ledger and independent review. Inspect actual native plugin source, versioned DLL and decoder (`sor-d5p/2`), native qualification harness, build methods, retained binary/relocation pins, and locally held R2 primary receipts if available. Source files and existing data take precedence over summaries. Capture actual git HEAD/status and record all reference identities. Inspect related tested SFSE patterns in `starfield-reference-handles` only where needed. Do not revive the old debugger architecture or unrelated research.

Verify any disassembly-based claims against the **pinned installed retail build**, not generic presumed structures. Separate static inferences, direct native observations, executable fixture results and operator reports. Keep proprietary executable excerpts and large decompilation dumps local-only. Treat all address/offset and function-entry claims as build-specific.

## 3. Design decision gate — before substantive implementation

Write and date a concise architecture/semantics decision record **before editing production validation logic**, including:

1. **Grid layout:** provenance of count, capacity, underlying storage pointer/allocation extent, member layout/stride, ownership and lifetime; whether the array is fixed or dynamic and what native guards establish readable boundaries. Explain any unresolved uncertainty.
2. **Membership semantics:** what *membership* means to the consumer, whether the game already offers a native indexed/direct lookup, keyed map or trusted helper; whether that operation has side effects, mutation, locking, lazy initialization, ambiguous identity or lifetime hazards. Avoid introducing a new native CALL solely for convenience without ABI and safety justification.
3. **Competing strategies:** (a) native direct/index lookup if proven nonmutating, correctly keyed and safely observable, (b) validated traversal over the *actual native extent*, and (c) documented finite fallback as a last resort. Compare source attribution, pointer/ABA risks, O(n) latency, memory-read exposure and failure cases. **Prefer direct lookup only if semantics and lifetime safety are demonstrated**, otherwise use safely bounded traversal. Do not presume 512 is universal or set an arbitrary huge replacement cap.
4. **Downstream checks:** exact execution order and native semantics for member-array validity, source identity/membership, invocation/current Grid correspondence, manager/source lifetime and reset/retirement. Identify what must be tested after the old reason-24 gate and which checks, if any, require correction.
5. **Recorder interaction:** expected hook hot-path overhead/event-volume change; why proposed implementation preserves R1 loss accounting, continuity epochs and evidence durability.

If no strategy safely covers valid larger Grids, return an explicit bounded **NO-GO/ESCALATE** with the missing native guarantee; do not silently loosen predicates to obtain positive results. A larger fixed limit is allowed **only** if independently justified as a bounded native representation envelope, with unambiguous coverage-limit reporting for larger valid instances.

## 4. Implementation contract

Implement only changes justified by the recorded decision and actual native evidence. Preserve the eleven-hook architecture unless an additional observation boundary is demonstrated essential; any hook change requires separate site, ABI, prologue/relocation, trampoline and version/identity safety proof. Do not alter gameplay, source population, generation inputs, resource mask, caches, saves or other game state. Preserve operator-only deployment.

- A valid Grid with count **324**, capacity **512** must not be rejected **solely** because its count exceeds 256. It may still fail for an independently genuine predicate; record which one and its valid observed operands.
- Do not equate reported count/capacity with verified allocation or readable byte extent; validate native storage and arithmetic (overflow, stride, pointer addition, partial reads, alignment where material) before inspecting members. Fail closed per *claim* on genuinely malformed/unreadable or raced state, without crashing or stalling the host.
- Membership result must distinguish **present**, **absent after a complete qualified inspection**, **inspection incomplete**, **read failure**, **mismatched identity/lifetime** and **unsupported structure**. A truncated scan must never become a proven negative. Do not equate matching addresses alone with stable source identity or confuse geographic keys with native pointers.
- Do not assume Grid and related objects remain unchanged across concurrent callbacks, reset or retirement. Preserve generation/lifetime tokens and conservative ABA invalidation; where snapshots cannot be made consistent without unsafe locking, represent the uncertainty rather than claiming complete membership.
- Minimize work inside hooks: finite work per invocation, safe nonblocking producer path, no filesystem I/O or heavy formatting in interceptors, and measurement of worst-observed as well as mean latency and reader-visible diagnostic volume. If a safe larger-Grid path requires expensive scanning, justify the trade-off and seek a non-mutating alternative rather than indefinitely blocking.
- Preserve schema provenance and independent interpretability. If the scientific event/diagnostic schema changes, version it deliberately and update readers, fixtures and package manifests; no silent reinterpretation of historical `sor-d5p/2` R1/R2 records. Historical R2 records and their first-failure reason 24 must remain byte-for-byte intact and replayable.
- Preserve recorder resilience after ordinary drops, cause-specific accounting, authenticated durable prefixes, output-fault handling and conservative global loss/continuity-epoch logic. No arbitrary run-wide event-count, file-size or byte-volume cap; retain bounded in-memory queue and established **40,000,000,000-byte free-space floors on applicable C: and D:** and genuine safety STOPs.

**Downstream repairs:** Codex is authorized to correct source membership, invocation/current Grid identity or lifetime predicates **only when their actual native semantics and failing test evidence justify a correction**. Otherwise retain the check and mark gaps honestly. Do not stop after a 324-member Grid crosses the previous barrier: execute the remaining predicates and distinguish their independently observed outcomes.

## 5. Offline qualification — production-path, adversarial and regression

Run disposable **Windows native** fixtures/isolated hosts exercising the *actual compiled production validator and instrumented DLL paths* wherever technically feasible; not exclusively mock JSON or a rewritten validator. Record explicitly when a narrower harness exercises production code but cannot prove full DLL/retail integration. Use actual version-pinned build inputs and reproducible clean rebuilds; do not modify live installed Starfield.

Required targeted matrix:

1. **Boundary and valid extent:** counts 0/1, below 256, **256**, **257**, **324/512**, at validated capacity, and valid larger-than-324 cases if native representation supports them. Check member early/middle/last (including positions beyond 256) and genuine absence after a full scan. Distinguish `count > capacity` from count valid but beyond any observer-supported envelope.
2. **Adversarial storage:** null/partially readable member pointer, inconsistent count/capacity, stride/pointer arithmetic overflow, stale or aliased allocations, partial/raced reads, zero/huge or corrupted claimed extent, and structurally valid but unsupported layouts. Demonstrate bounded latency, no unsafe memory traversal, and no fabricated negatives or zero-valued operands after read failure.
3. **Downstream chain:** verify that valid large Grids advance past the old reason-24 gate into **membership, invocation/current Grid and lifetime** checks. Exercise both passing and independently failing versions of each; validate first-failure order, reason/operand validity and complete chain qualifications only when all requisite predicates genuinely pass. If a route cannot be exercised, provide static evidence and explicitly mark it untested.
4. **Concurrency/lifetime:** nested and concurrent demands, manager reset, Grid clear, source retirement, pointer address reuse/ABA, cross-invocation aliasing and partial generation. Preserve valid join/invalidations and non-target source discrimination; no prefiltering by assumed Feynman V pointer, mask or geographic descriptor.
5. **Recorder and reader:** force one/multiple queue-full and contention drops, recovery after loss, output failure, torn/corrupt tails and abrupt termination, with surviving authenticated prefixes and no unsupported cross-gap claims. Regression test older R1/R2 evidence decoding, diagnostics and original eleven-hook lifecycle.
6. **Performance and safety:** report measured mean, p95/p99 and max *observed* hot-path timings across realistic Grid sizes if measurement is practicable; account for capture overhead and saturation in unpaced multithreaded load. Do not call measured maxima a universal guarantee. Explain trade-offs and any still-unbounded native behavior. Measure record volume and drop pressure; **recorder architecture overhaul is out of scope**, but simple justified local optimizations with unchanged scientific semantics may be proposed or implemented if independently verified.

A single 324-member green fixture **does not qualify** R3. Qualified negative cases, downstream checks and adverse structural cases are mandatory. Where instrumentation cannot safely reproduce a relevant retail condition, disclose this limitation and keep retail compatibility unproven.

## 6. Proposed retail follow-up — preparation only

If offline acceptance succeeds, prepare a reviewed package and a **PROPOSED / NOT AUTHORIZED** operator run card based on the current R2 retail session and approved source identity. Retain Save52, second Feynman V and shortest evidence-supported ordinary gameplay sequence unless genuinely new evidence requires a justified revision. Distinguish diagnostic success (valid downstream context discrimination) from full construction–retention–reuse scientific success. Do not claim the original D5P historical cause has been retroactively resolved merely because the R2 first-failure bound has been removed.

The proposed card must pin plugin DLL, source/build, archive/ZIP, game/SFSE and schema identities; include independent fresh READY with all required hooks before protected Save52 load; maintainer-only Vortex installation/disable/removal and `sfse_loader.exe` launch; Cloud/profile checks; 40 GB C:/D: floors; manual STOP; recorder-loss tolerance; protective postflight, archived primary evidence and actual verification scope. A crash after already durably authenticated decisive evidence can preserve useful results, but cannot waive safety/postflight. **No automatic repeated runs, game launch, plugin install, Vortex change, save/config mutation or B6 publication under R3.** Do not assume a future GO from an accepted offline patch.

## 7. Authority, preservation and deliverables

Keep all protected saves/backups, original observed evidence, binaries and historical ledgers unchanged. Work in task-owned repo/local ignored scratch. Apply the active source/provenance, preservation and editorial policies; preserve original R2 receipt identities and exact failed-run conclusions. Do not automatically copy private evidence into public tracked paths or publish proprietary dumps. No broad archive cleanup, new reverse-engineering initiative, unrelated plugin changes, publication or integration. Do not stage, commit or push.

Deliver:

- Dated **pre-implementation Grid/membership design decision**, with competing strategies, native provenance and rejected options.
- Focused R3 scientific/engineering report: original observation, Grid layout, chosen semantics, code delta, downstream findings, observed negatives, performance, uncertainties and residual retail risks.
- Task-owned changed plugin sources/build tools, native/disposable fixtures, independently readable evidence schemas/reducers (only where modified), qualification manifest and reproducible version-pinned build; one proposed reviewed deployment package if justified.
- `docs/experiments/resource-retained-population/d5p-r3-review.md`: frozen criteria, independent engineering/scientific/editorial assessments, deviations, exact source/binary/package identities and unresolved limitations.
- `docs/experiments/resource-retained-population/run-card-d5p-r3.md`: **proposal only**, operator and Codex responsibilities, readiness/STOP/postflight protocol.
- Concise updates to `docs/RESEARCH_STATE.md`, `docs/SOURCES.md` and other required durable records, without recasting prior results.
- Complete and task-only diffs, exact hash-bound manifests, independent final closure, repository status and exclusions; no staging/commit/push.

Use established repository layouts; if names differ, explain the change. Minimize redundant manifests and durable scratch. Preserve reproducible evidence rather than voluminous disposable intermediates.

## 8. Frozen acceptance criteria

| ID | Mandatory disposition requirement |
|---|---|
| **R3-AC1 — Authority/protection** | Offline only, no retail game/SFSE/Vortex/save actions, all protected/historical inputs intact, disk and repo rules followed. |
| **R3-AC2 — Evidence-grounded prior design** | Dated architecture/semantics decision **before substantive coding**; correct Grid layout and count/capacity/member provenance, explicit direct-lookup vs validated traversal vs fallback evaluation; unresolved native assumptions disclosed. |
| **R3-AC3 — Real large-Grid coverage** | A valid **324-count/512-capacity** Grid no longer fails *solely* at the former 256 inspection bound; validated storage, complete-vs-incomplete membership, legitimate negative, corruption/overflow guards and explicit remaining supported envelope. |
| **R3-AC4 — Downstream context validation** | Actual production validation reaches and correctly discriminates membership, invocation/current Grid and lifetime predicates in positive and negative native fixtures; any unsupported route marked NOT TESTED, never waved through. |
| **R3-AC5 — Scientific integrity** | No fabricated memberships, first-ever construction, ownership, reuse or source associations; source/manager lifetimes and cross-loss gaps conserved; older R1/R2 evidence remains valid and readable. |
| **R3-AC6 — Performance/resilience** | Safe finite hot-path work, bounded memory, no arbitrary total capture cap, recorder continues after ordinary drops, crash/error prefixes intact; measured overhead and queue pressure disclosed; no unjustified recorder rewrite. |
| **R3-AC7 — Native qualification** | Real Windows compiled production-path controls for boundary, malformed, end-of-array, downstream and concurrent/lifetime cases; documented limitations and reproducible build pins; no synthetic-as-retail claim. |
| **R3-AC8 — Retail proposal only** | Candidate/package and proposed R3 run card with fresh READY, operator-only Vortex/SFSE, Save52 protections, 40 GB guards, postflight and independent GO gate; no live run. |
| **R3-AC9 — Independent delivery** | Independent technical/scientific/editorial review against all criteria, required rework or honest bounded NO-GO, exact manifests/diffs, final provenance and no stage/commit/push. |

**Completion rule:** An implementation may be accepted as a *bounded offline investigation* even if some native routes remain unresolved, but it must not be called **retail-ready** or presented for retail GO consideration unless **R3-AC3 and R3-AC4** are credibly qualified at the stated production-path scope. A failure at an earlier step must not be hidden by a passing test of a later step. If the scope cannot safely establish those gates, report the obstacle and propose the smallest evidence-based next step.

**No R3 outcome automatically authorizes a retail run or B6 publication.**
