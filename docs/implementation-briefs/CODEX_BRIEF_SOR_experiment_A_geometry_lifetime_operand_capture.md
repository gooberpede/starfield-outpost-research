# Codex Research and Offline Qualification Brief

## SOR — Experiment A: Resource-Region Geometry Lifetime and Complete Native Operand Capture

**Status:** Implementation/research brief for Codex; not authorization for live experimentation.

**Project:** `starfield-outpost-research` (use repository `WORKFLOW.md`, `AGENTS.md`, established scientific provenance and review conventions).

**Context:** The spatial-equivalence feasibility assessment identified internal native ACCEPT and REJECT edges. The subsequent disposable offline qualification demonstrated internal breakpoint/VEH observation under limited conditions; a further x87-focused qualification identified loss of full FIP/FDP pointers at the uncorrected continuation and qualified one targeted restoration mechanism in synthetic tests. These results are **not** validation in retail Starfield and **not** native spatial equivalence. The current problem is whether actual Starfield geometry can be snapshotted coherently and whether the exact native spatial inputs can be obtained and attributed to each decision without unsafe or disproportionately invasive observation.

## 1. Scientific objective and value gate

Produce a defensible, branch-complete plan for independently testing the existing reconstructed spatial predicates against **real native candidate-region inputs and real native accept/reject edges**.

A future live experiment is scientifically worthwhile only if the proposed evidence can support an independent comparison, including rejected candidates, for the applicable native branches. The goal is not to accumulate region counts, callback headers, final resource sets or further UI confirmations. Do not silently substitute those for paired native operand/decision records.

The present assignment has two **separately judged** technical questions:

- **G — Geometry snapshot:** Who owns the actual ordered resource-region points and widths, how are they protected, and is there an evidence-backed interval in which an observer can take a complete, coherent copy without changing native semantics?
- **O — Operand completeness:** Can every native operand used by the spatial algorithm (including repeated coordinate resolution, frame translation, numeric domain and branch-specific values) be observed or established stable and unambiguously paired with the terminal native decision?

Retain a hard GO/REVISE/NO-GO gate. An inability to establish either G or O is not a reason to build a larger observer by default. Failure or evidence-bounded inconclusiveness is a valid completed outcome.

## 2. Evidence and constraints

Start with the existing pinned Starfield executable/native exports, function register, spatial reconstruction and tests, the Experiment A feasibility report and boundary/coverage documents, the accepted internal-observation offline qualification, and the accepted x87 correction evidence. Locate current exact files and hashes within the repository; do not trust this brief as a replacement for pinned versioned evidence.

Relevant prior mapped landmarks **for navigation, subject to verification against pinned source**:

- Spatial region evaluation vicinity: RVA `0x021E1060`.
- Resolved query/translation vicinity: RVA `0x021E1119`.
- Native rejection edge: RVA `0x021E174E`.
- Native acceptance edge: RVA `0x021E1772`.
- Native availability updater: RVA `0x021E07D0`.

Never infer a native calling contract or a lifetime guarantee from an address alone. Mark separately what is proven directly by static instructions, inferred from caller/callee structure, demonstrated in fixtures, and untested in the game.

Preserve raw saves, native exports, Ghidra projects, binaries, evidence, frozen predictions and tests. Use disposable outputs and normal project-local review paths. Do not modify the prior accepted x87 fixture findings to make new tests pass.

## 3. Geometry ownership, mutation and lifetime analysis (G)

Trace the actual resource-region representation consumed by the spatial evaluator, not a convenient substitute. Establish, to the extent supported by the native evidence:

1. Allocation and ownership of region records, point/width arrays, capacity/count fields and referenced/transformed data.
2. Pointer movement and indirection from ProcGen owner/source collections to callback and spatial evaluator; explicitly record all relevant layouts/offsets with source provenance.
3. Population, mutation, reallocation, replacement, invalidation and destruction functions; distinguish actions possible generally from actions proven reachable during a spatial evaluation.
4. Traversal, locks, reference counts, task/lifecycle fences, thread affinity or other lifetime protections; identify exactly **which objects** each protection covers and its acquire/release extent.
5. Whether a complete array can be copied at a stable native boundary, including validity of count and the full ordered point/width payload, and whether a second read/version check is genuinely necessary or useful.
6. Whether taking the snapshot would require blocking inside sensitive native execution, unbounded callback allocation, unsafe pointer walking or assumptions that cannot be substantiated.

A lock observed elsewhere in the pipeline is **not** automatically a guard for the region-point array. Likewise a cache entry, source visit or pointer that is non-null does not establish a completed or stable geometry record.

Write an **ownership/lifetime table**: object, owner, producer, consumer, mutation/destruction path, synchronization, read/snapshot window, evidence, confidence and unresolved conditions. Where the current native data does not establish safety, say so explicitly.

## 4. Complete operand dataflow and capture plan (O)

For every path represented by the frozen spatial evaluator, trace the true native instruction dataflow. Identify **source operands**, derived/re-resolved operands, numerical transformations and terminal decision edges, distinguishing direct observations from reconstruction assumptions.

At minimum address:

| Native path | Minimum assessment |
| --- | --- |
| Region entry and XY broadphase | Actual indexed XYZ, frame/reference domain, region center/radius, query radius, upper scalar and source identity; broadphase branch and early rejection |
| Zero/one-point cases | Count-dependent path, exact fields consumed and terminal interpretation |
| Multi-point tapered strips | Complete ordered points and widths, point transformations/normalization, segment and width semantics, actual comparison domain |
| XY containment | Resolved XY and numeric inputs used by containment, without invented Z conditions |
| Vertex proximity | XY tests and native upper-coordinate condition, including strict/inclusive comparisons |
| 3D edge-distance | Source/derived XYZ, radius and all required inputs to the distance comparison |
| Terminal edges | Actual ACCEPT/REJECT reached for **this region**, not callback traversal status or final UI resource membership |

Pay particular attention to **repeated coordinate resolutions** during a region evaluation. Either identify capture points for values as consumed or supply convincing native evidence of stability across those uses. Record translations, frame indices and floating-point precision/rounding (including any intermediate operation that materially affects equivalence). Avoid a demand to hook every arithmetic instruction: prefer original sufficient operands and verified transformations, but do not assert sufficiency without tracing.

Establish a concrete correlation contract across entry, operand reads, nested calls, concurrent threads, terminal edges, aborted/unwound calls, STOP and truncated snapshots. Distinguish `ACCEPT`, `REJECT`, `NOT_EVALUATED`, and `INCOMPLETE/UNKNOWN`. Capture rejected candidates; do not treat unvisited later segments or region entries as negative decisions.

Deliver a **branch-by-branch operand matrix** with field/type/representation, provenance, native consumer/instruction, proposed observation point, lifetime and confidence. Provide a minimally sufficient native-event schema and an independent replay admission rule. This is a research schema, not an authorization to implement a live decoder.

## 5. Narrow, evidence-triggered offline qualification

**Static analysis is the first gate.** Only implement an offline synthetic/native-equivalent fixture when it addresses a specific G or O assumption that remains consequential after native evidence inspection. For every proposed fixture, state the unresolved proposition, why static evidence is insufficient, what an affirmative and negative test would show, and its finite acceptance criteria. Skip tests that cannot discriminate a genuine uncertainty.

Permitted tests include a narrowly adapted disposable geometry-ownership/mutation stressor, multi-use coordinate snapshot and provenance test, or correlation/STOP boundary test that reuses the accepted fixture and decoder. Neither synthetic fixture ownership nor its passing controls can prove Starfield's actual allocation/lifetime or retail safety. Where source evidence is insufficient, retain `UNKNOWN` and do not manufacture confidence with a synthetic demonstration.

Maintain and rerun any applicable existing state preservation (including corrected x87), general-register/SIMD, nesting/concurrency/STOP and evidence decoder regressions **if your changes touch those pathways**. Do not rework the correction, expand exception mechanics, or take on a general instrumentation architecture project. Preserve complete negative tests and outputs with hashes.

## 6. Independent scientific and engineering review

Use the repository's research execution/completion process. One primary agent and mandatory independent reviewer; one relevant specialist researcher may be used if useful, with at most two sub-agents concurrently. The reviewer must challenge:

- Whether the alleged snapshot window truly protects the point/width payload from mutation or free.
- Whether all **native consumed operands**, not merely plausible source values, are available for independent replay.
- Whether entry-to-decision pairing is valid under concurrency, nesting, exits and STOP.
- Whether proposed fixture tests distinguish a meaningful hypothesis rather than certify their own assumptions.
- Whether a successful future capture would materially test spatial equivalence, including native rejection decisions.
- Whether prose, table cells, version strings, numeric addresses and source references are readable; audit all task-authored/modified documentation for recurring fused words and missing spaces.

The reviewer may require bounded rework for issues in scope. Do not continue expanding the project to force a PASS.

## 7. Hard stopping criteria and decision

Return **PASS** only if both G and O have an evidence-backed, coherent capture design with complete data and correct native pairing, and any necessary offline qualifications pass. This is **design/fixture qualification only**, not retail safety or empirical equivalence.

Return **REVISE** only if one specifically identified, bounded residual question has a justified finite follow-up that could decisively resolve it; describe the exact evidence, effort and stop condition. Do not use REVISE to authorize an indefinite series of synthetic experiments.

Return **NO-GO** if the needed geometry cannot be read coherently with the established constraints, essential operands cannot be recovered or paired, the required interception is unacceptably invasive, or a decisive experiment cannot be justified. If the result is evidentially inconclusive, label that precisely and **do not approve live development**.

If feasible, document what would still require separate review before a live observer: exact native patch sites, runtime protection, callback costs, safe stopping, retail compatibility and operator controls. **Do not build that observer in this task.**

## 8. Deliverables and handoff

Write under the established Experiment A research documentation structure (prefer extending existing records rather than a parallel source of truth):

1. Main concise report with scoped PASS/REVISE/NO-GO, strongest evidence, limits and scientific implications.
2. Native geometry ownership/lifetime graph and evidence table, with version-pinned RVAs/offsets.
3. Complete branch-specific operand map and source-to-consumer dataflow, including coordinate re-resolution.
4. Proposed minimal observation/evidence-correlation contract and explicit exclusion conditions.
5. Justification, instructions, outputs and hashes for **only** the offline tests actually needed, if any.
6. Independent review findings and rework resolution; provenance/preservation log and prose-quality audit.
7. Updated durable research state/function map where new native facts are established.
8. Review package: current branch, complete and task-only diffs (including newly created text), changed-file inventory, proof of appropriate tests and protected-input preservation, and suggested Conventional Commit subject. Place diff/review artifacts under existing `.local-work` conventions. Do not include raw proprietary native dumps or binaries in diffs.

End with an explicit statement of **what a correctly implemented future live experiment could conclusively test**, and **what it still could not test**. No claims of native spatial equivalence before actual independent native operand/decision comparisons.

## 9. Forbidden actions / authorization boundary

- **No Starfield launch, injection, live game observation, SFSE observer, retail hook, Vortex package or deployment.**
- **No change to the unapproved 0.8.0 observer or historical qualification evidence.**
- No remote-resource query investigation, generic cache-completeness campaign, disappearing-deposit investigation or mod-specific gap analysis.
- No replacement rewrite of the frozen spatial algorithm to make tests agree.
- No unapproved destructive edits to evidence, saves, binaries, native exports or Ghidra projects.
- **Do not stage, commit or push.** The user and assistant review the complete work first.

**Success is an honest bounded decision, including NO-GO if warranted, not production of another observer.**
