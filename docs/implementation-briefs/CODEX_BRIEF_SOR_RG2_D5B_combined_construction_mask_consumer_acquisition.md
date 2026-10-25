# Codex implementation brief — RG2-D5B
## Combined Construction-Mask and Consumer Acquisition

**Project:** `D:\Projects\starfield-outpost-research\` (`gooberpede/starfield-outpost-research`)  
**Authority:** Phase A, offline implementation and real disposable **synthetic Windows debugger** qualification only. **No Starfield launch, attachment, game mutation, live sample or save creation is authorized.**  
**Next gate:** Return the completed Phase B run card and Phase A package for maintainer review. Independent reviewer ACCEPT does **not** authorize Phase B.  
**Status:** Implementation assignment; preserve prior experiments and their findings.

## 1. Background and precise scientific question

RG2-D5 determined that certain Save52 Feynman outposts have nonuniform resource masks. The native resource generator samples the effective ordinary mask from the **original source-construction query**, which can differ from the beacon position and later generation-cell/consumer queries. Existing offline evidence cannot uniquely recover this first query for the affected historical sources. RG2-D5A assessed all thirteen mixed-mask sources and selected an initial experiment by discrimination, not by the historical resource-mutation report.

**Primary target:** active second Feynman V outpost, source `0:37536:20928:0029d20e`; supported alternative ordinary masks **0** and **3**, which produce materially different Ionic Liquids, Fluorine and Copper geometry even though both alternatives may yield all three resource names. Its exact saved Workshop/source identity must be obtained from the committed D5/D5A case records, not guessed from display text.  
**Designated fallback:** Feynman VI-b source `0:29568:10932:0006ce58`, masks **0** and **8**, chiefly discriminating Aluminium. This is **not** an automatically authorized second retail target.  
**Deferred:** Feynman VIII-b historical disappearing/substituted-resource hypothesis; do not attempt bug reproduction. Other Feynman cases remain regression/case-matrix context.

**Primary question:** Which initial construction query and effective ordinary mask does the engine actually use when constructing the specified Feynman V source?  
**Secondary question:** What resource regions does the identified Workshop consume, and can those regions be positively associated with the observed construction/source lifetime? Do not require a historical producer-consumer epoch join when it cannot be witnessed.

## 2. Binding research, authority and source discipline

Before implementation, read `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EVIDENCE_STANDARD.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md`, `docs/reviewers/research-completion-reviewer.md`, and relevant D5/D5A, D4, C1G, C1E, C2A/C2B and D4B/D4D reports and native contracts. Follow the pinned evidence/source registers and existing rights policies. Do not reinterpret `FUN_` aliases as API guarantees.

Pinned retail target for prospective Phase B **only**: Starfield.exe **1.16.244.0**, SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. Actual runtime module base must be measured; static VAs, RVAs, FormIDs, source ordinals, saved reference tokens, runtime handles, pointers and file offsets are distinct domains.

Use existing debugger infrastructure, framing, independent receipt verification, amended transient-save policy and repaired terminal STOP handling. Preserve original/native evidence, frozen predictions, installed definitions and original case/screenshot bytes. Keep proprietary data, native dumps, raw captures, saves and built executables ignored/local-only; original authored implementation and research documentation may be tracked subject to normal review. No staging, commit, push, cleanup, release or publication.

### Frozen completion discipline

Treat AC1–AC8 below as frozen. Maintain substantive investigation/test logs, including failures and negative evidence. Independent reviewer must examine original contract, actual code, fixtures, primary verification receipts, scientific claims, diff, final changed text and exclusions. An approved run card is a **proposal**, not permission to execute. No arbitrary source inference, silent substitution of mask values, or selecting answers from screenshot labels.

## 3. Phase A engineering deliverables

### A. Exact observation and identity contract

Trace and pin existing native boundaries for: provider/source construction entry and first-query operands; source geographic/frame conversion; native mask sampling and active/inactive decision; resource candidate/resource-call ordering; source-wrapper/owner/cache identity; region consumer ACCEPT/REJECT and pre-install spatial transfer; Workshop/area updater identity. Specify instruction windows, caller/callee sites, live register/stack ownership, field offsets, lifetime assumptions, and exact conditions for a meaningful event. Avoid inventing fields or an epoch counter.

Produce an explicit join diagram and machine-readable receipt schema that distinguish:

1. **Construction-bound:** observed initial query, coordinate conversion, sampled mask, source identity, manager/owner, provider invocation, thread/nesting and lifetime evidence.
2. **Consumption-bound:** qualified Workshop, actual area query, accepted regions with exact ordered binary32 XYZ/width/bounds, resource identities, selected source/wrapper, same-evaluation transfer membership.
3. **Producer-to-consumer linked:** only when a positively witnessed generation/population lifetime relationship supports that claim. Same geographic source, resource set, source ordinal, pointer value or timestamp alone do not prove a shared epoch.

Capture contradictory observations separately. If the same source identity is constructed at different times with differing first queries or masks, retain both with distinct session/lifetime contexts rather than reconciling them silently.

### B. Working combined debugger acquisition

Implement and qualify an actual combined Windows controller using the existing hardware-breakpoint architecture, bounded checked cross-process memory copying, externally fsynced/closed/read-back-verified receipts and ACK-controlled stopping. Reuse corrected D4B/D4D teardown and save admission; don't revive unsafe legacy `INT3`/detach/replay behaviour by default. Handle breakpoint-slot scheduling explicitly, including events lost during switches, reentrancy, worker threads, source replacement, cache-only consumption, source map churn, and controller shutdown. Unknown ancestry is not success.

**Priority:** capture the relevant source-bound construction query/mask. Consumer sampling is secondary but should not be omitted if it is the normal route needed to bind source to Workshop; clearly classify observation completeness and the associated scientific claim.

Synthetic fixtures must exercise *actual* Windows debugger attachment and reads from target-owned source-shaped memory. A JSON-fed simulation of the desired receipt is insufficient. Create an event/selection contract that cannot be satisfied by unrelated same-planet events.

### C. Evidence and offline comparator

Provide a versioned, read-only comparator taking freshly collected receipts and the **unchanged** D5A conditional alternatives. Compare sampled mask/first-query inputs, source identity, candidate ordering and, where joined, exact native regions and consumer decisions against independently frozen mask-0 and mask-3 predictions. Preserve both alternatives, even if one agrees with a future live outcome. Record negative results (`NO_HIT`, `PARTIAL`, `UNBOUND`, `INVALID`, `LOSS`) separately from observed zero/empty resource populations. Never fit the model to observed resources.

Include a clearly delimited consumer-only result that can validate current geometry but cannot imply the historical construction query. Include construction-only result that provides valid canonical mask evidence without claiming downstream correspondence. Do not make an unrelated clean generation invocation a scientific success.

### D. Real synthetic qualification

Required scenarios, at minimum:

- Mask **0** and **3** from different initial construction queries on the same named source; exact per-invocation values retained.
- Constructed source with no later consumption; correct construction-only classification.
- Workshop-bound cached consumption with no generation call; correct consumer-only classification.
- Positively linked construction and consumption with lifetime/epoch evidence; correct linked classification.
- Same source pointer or ordinal reused with different lifetime; no false join.
- Wrong Workshop, body, source key, owner, native resource or transfer pointer; refuse scientific promotion.
- Nested and concurrent events, relevant breakpoint-slot contention, stale/queued events, unavailable registers and partial memory reads.
- Resource geometry with complete binary32 widths/bounds and intentionally corrupted/truncated arrays.
- Crash/exit before ACK, acknowledged STOP followed by thread exits, termination without breakpoint rearming, and durable receipts surviving target failure.
- A source with conflicting masks across two witnessed constructions; do not overwrite either.

Rerun appropriate inherited C1G/C1E/C2B/D4B/D4D debugging regressions, all **ten** exact Feynman/Carinae/Archimedes native geometry controls, and Save52 predictor regression checks. Distinguish genuinely executed tests from inherited reports and record exact commands, versions, outcomes and retained failures.

## 4. Phase B run card — prepare, do not execute

Prepare a self-contained, operator-readable run card for **one** prospective Steam-launched Starfield session targeting the **second Feynman V outpost and source** `0:37536:20928:0029d20e`. It must specify:

- Exact reviewed source/build hashes, guarded runtime observation points, expected Workshop/planet/source identities and case-specific discriminators; no guessed identity joins.
- Approved target and installed-content configuration prerequisites; a fresh synthetic qualification and strict preflight GO/NO-GO.
- Fresh verified master backups and SHA-256 matching for protected manual/research/quicksaves, with scratch restoration rehearsal, Steam Cloud check and strict postflight. Reliably classified active autosaves/exitsaves are nonblocking diagnostic churn; archived backup corpus remains protected.
- Normal gameplay sequence (one Save52 load, direct travel, one Build Mode entry) and what the operator must record. No forced regeneration, teleport, cache invalidation, save modification, injection, arbitrary repeat or other outpost.
- Scientifically meaningful stop classification: a **positively source-bound first construction-query/mask** is a useful *construction-only* result; add Workshop-bound consumed geometry when obtained, but do not invent a missing epoch join. An unrelated source event must not trigger successful STOP.
- Distinct no-hit/retained-cache/partial/error paths, durable ACK and process disposal, postflight verification and preserved complete/partial receipts.
- No automatic retries. Any fallback VI-b retail test requires new maintainer review and explicit approval.
- An explicit banner: **PHASE B NOT AUTHORIZED. DO NOT LAUNCH OR ATTACH TO STARFIELD.**

The run card must candidly explain the risk that construction does not occur on a normal revisit, and the exact information value of each possible outcome. The card must not promise historical mask attribution from an unrelated contemporary construction.

## 5. Frozen acceptance criteria

| Criterion | Mandatory evidence |
|---|---|
| **AC1 — Authority/preservation** | Phase A synthetic-only; protected game/save/native/frozen inputs unchanged, originals and local-only materials preserved; no live game or integration actions. |
| **AC2 — Native contract** | Source-backed, version/offset/identity qualified first-query, mask, source, region and Workshop boundaries; explicit lifetime and epoch limitations. |
| **AC3 — Working combined collector** | Implemented debugger collector with real cross-process synthetic evidence and verified ACK/STOP transport, not design-only prose. |
| **AC4 — Scientific identity/discrimination** | Construction-only, consumer-only and positively linked classes correctly distinguish target source from unrelated events; contradictory masks retained. |
| **AC5 — Offline comparator** | Both fixed Feynman V alternatives compared without fitting, including negative and incomplete outcomes; frozen source/prediction files unchanged. |
| **AC6 — Phase B preparation** | Complete one-case Feynman V run card, viable no-hit explanation and separate explicit approval gate; VI-b is not automatically approved. |
| **AC7 — Reproducibility/quality** | Actual Windows fixture results, inherited regressions, hash/preservation evidence, detailed source pins, implementation documentation and full editorial finalization. |
| **AC8 — Independent review/delivery** | Independent scientific, engineering and editorial ACCEPT on exact final snapshot; criterion matrix, failures, verified complete/task-only patches, manifests and protection/exclusion reports. |

ACCEPT of Phase A does not assert runtime generation-consumption equivalence or authorize Phase B. On engineering failure, continue correction and requalification within scope; if an evidenced hard barrier remains, return ESCALATE with a concrete alternative, not an unbounded feasibility report. Do not weaken frozen ACs to force acceptance.

## 6. Finalization, handoff and boundaries

Follow `docs/EDITORIAL_STANDARD.md` and workflow: automated changed-text screen, manual readability/notation/semantic pass over all changed prose, independent editorial verification, then exact final snapshot and any delta review. Prevent run-together word/number prose, encoding corruption, unclear decimal/hex/native-offset domains, and accidental promotion of model inference to live observation. Do not add unnecessary decimal conversions to conventional hex notation.

Return in the existing Codex completion format:

- Bounded scientific/engineering conclusion with clear confirmed/conditional/unknown status and AC1–AC8 matrix.
- File-by-file authored changes, source evidence/provenance, tests, actual commands and retained failures.
- A working controller and versioned synthetic receipts (raw protected evidence local only).
- Complete proposed Phase B run card **not executed**.
- Independently reviewed exact complete and task-only unified diffs, byte/hash manifests, forward/reverse patch checks, changed-text editorial report, unchanged HEAD/index, and no staging/commit/push.
- Suggested conventional commit message.

**Do not begin B6/publication readiness, game release, Outpost Tracker integration, performance/productization, historical resource-mutation bug reproduction or any unauthorized live activity.**
