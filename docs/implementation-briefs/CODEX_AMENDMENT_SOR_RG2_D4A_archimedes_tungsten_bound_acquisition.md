# Codex amendment — RG2-D4A: Archimedes Tungsten-bound acquisition

**Project:** `D:\Projects\starfield-outpost-research\` (`gooberpede/starfield-outpost-research`)  
**Date:** 2026-10-24  
**Type:** Focused Phase A engineering amendment to RG2-D4; **offline implementation and synthetic qualification only**  
**Live authority:** **NONE.** RG2-D4's existing Phase B run card remains **NOT AUTHORIZED and is superseded for prospective use by a revised card**, pending explicit maintainer approval.  
**Research question:** Why does Save52's Archimedes III outpost display a localized Tungsten deposit while the frozen D3 predictor selects a Chlorine-family context and omits Tungsten?

## 1. Intent and binding context

The RG2-D4 Phase A collector is useful but its prospective Phase B stop criterion—*first complete Archimedes-body-owned generation invocation*—has inadequate minimum scientific information gain. It may stop on an unrelated source before the Tungsten-bearing outpost is evaluated, or observe no generation because relevant regions were cached. **Do not run that card.** The engineering goal of this amendment is to observe the **actual resource-consumption chain for the selected outpost and Tungsten**, while retaining generation-context observations when they can be validly joined.

Read and follow `AGENTS.md`, `WORKFLOW.md`, `docs/PERMISSIONS.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/EDITORIAL_STANDARD.md`, `docs/templates/completion-contract.md`, and the applicable independent-review procedure. The original D4 AC1–AC8 and approved D4 Phase A findings remain historical and unchanged. Relevant source material includes:

- `docs/experiments/resource-selection-context/{report,native,comparison,implementation,run-card,review}.md` and `research/resource-selection-context/`.
- `docs/experiments/resource-carinae/{phase-b,phase-b-review}.md`, `docs/experiments/resource-carinae-source-context/{phase-b,phase-b-review}.md` and their qualified collector techniques.
- `docs/experiments/resource-region-ancestry/`, `docs/experiments/resource-oracle-retail/`, `docs/experiments/resource-geometry-observation/native-contract.md`, `docs/experiments/native-availability-map/output-contract.md`.
- `docs/experiments/resource-save52-d3/` and the RG2-D2 baseline; Feynman/Carinae seven native geometry controls.
- `SAVE_PROTECTION.md` and the C2B transient-save-protection amendment.

The existing Archimedes case is Save52/HIST-0267; Archimedes III `0x0005de4c`, beacon saved token `81a75b`, Workshop identifier bytes `e07e10e02770599b`, and the qualified saved identity joins in the existing D4 run card. Tungsten is the target; Chlorine is the control. **Saved tokens are not runtime pointers or handles.** Current gameplay shows a visible Tungsten region and separate Chlorine deposits, but screenshots do not establish native path counts or generator inputs.

## 2. Required scientific evidence and stopping condition

The **primary useful-success result** for the prospective live pilot must be a coherent, positively identified **Archimedes Workshop → area evaluation → accepted Tungsten region → spatial transfer** association, with the native source wrapper/key and geometry attached to the accepted-region observation. Collect:

1. Correct running executable and actual area-updater reference positively bound to the saved Workshop (including appropriate native reference/BC identity checks).
2. Evaluation identity: thread-lifetime/invocation tokens; query XYZ, radius and upper bound; actual callback ancestry. Distinguish relevant area query from construction query and downstream placement query.
3. **Tungsten IRES** resolved to the installed, plugin-qualified definition, actual region ACCEPT branch (not merely function return), complete bounded region coordinates/points/widths/bounds and selected source key/wrapper/anchor where safely readable.
4. The **same evaluation's spatial transfer** containing the very same resource pointer; retain terminal and membership evidence. A resource-name match or two temporally adjacent events is not a valid join.
5. Source/manager current BIOM, relevant descriptor/component/family identity and resource-mask/selection data **only where natively witnessed or demonstrably bound**. Label absent generation operands `UNKNOWN`; do not infer historical generation epoch from consumption-time state.
6. Chlorine region and context as secondary control where naturally traversed, without allowing unrelated Chlorine or body-only generation to satisfy useful stopping.

**The collector MUST NOT stop successfully merely because it recorded the first complete body-owned generation invocation.** It may preserve unrelated generation events as diagnostics while continuing the approved normal-play action sequence. A complete Tungsten ACCEPT/transfer identity result is intrinsically informative even if the generating call never executes; the prospective pilot must be able to succeed on a cache hit. Avoid designing a stop criterion that requires simultaneous natural generation and consumption.

The exact form of a source-to-generator epoch join remains conditional. If an existing source snapshot suffices to distinguish the frozen predictor's BIOM/family/source assumption, that is useful without asserting historical cause. If only a source snapshot is obtained, record its exact scope and stop it from being labelled a complete generation-provenance capture. If a direct Workshop-to-consumer Tungsten join is technically unavailable, the fallback must acquire a **different, specific, previously unknown and diagnostically relevant operand** and explain in advance which hypothesis it distinguishes; otherwise **do not propose a live run as scientifically ready**.

## 3. Implementation scope — Phase A authorized now

Reuse the established Windows hardware-breakpoint controller, native memory readers, durable SRO1/ACK transport, C2A/C2B region and source ancestry techniques and D4 selection-context observers. Do not replace the debugger architecture without an evidenced blocker. Adapt the already qualified consumer capture to Archimedes, and correlate its positive Tungsten chain with any natural D4 selection-context invocations. The design may collect both streams in one process if justified and synthetically qualified; it must not assume that data gathered on different callbacks or threads share one epoch.

Resolve hardware debug-register slot contention explicitly. Existing observer families have more named observation locations than physical DR slots; provide a verified scheduling strategy (phase-specific stop configurations, conditional arming, or another supported method) with event-loss accounting. Do not silently drop one of the required identity/region/transfer edges to make the site count fit.

Use source-backed instruction locators and register/stack/owner layout guards for the pinned `Starfield.exe` 1.16.244.0 build only. Observe native ACCEPT/REJECT edges and the pre-install transfer. Treat a short-circuited callback as incomplete region coverage, not evidence of absence. Copy target-owned data while safely addressable, reject malformed lengths/counts and pointer alias ambiguities, and durably flush, read back, hash and acknowledge receipt bytes **before any approved target disposal**. The disposable game session may become unstable after capture, but incomplete or unacknowledged evidence never qualifies as scientific success.

Implement an **offline comparator** against frozen D2/D3 Archimedes predictions and the existing installed-data model. It must show (a) the exact assumption challenged by the observed Tungsten region/source, (b) whether the candidate source/family was represented in the offline inputs, and (c) whether geometry matches, differs, or is unsupported. No parameter fitting, geometry translation to force a match, silent selection of Tungsten-compatible BIOM, or rewriting of frozen predictions. Retain Feynman and Carinae seven-region exact regressions.

## 4. Synthetic qualification and no-hit policy

Build source-shaped synthetic targets exercising real Windows debugger attachment, native memory copying and external ACK transport. Demonstrate at least these cases:

- Correct Workshop-bound Tungsten ACCEPT, source, geometry and same-evaluation transfer; successful durable STOP.
- A first unrelated Archimedes generation event **followed by** a correct Tungsten event: no premature success or disposal.
- No producer invocation, but a **cached** Tungsten region accepted and transferred: still scientifically successful, with generation epoch `UNKNOWN`.
- Wrong Workshop, another body, matching Tungsten FormID on unrelated source, wrong transfer epoch, pointer reuse and reused thread/stack identifiers: reject false joins.
- Chlorine-only evaluation, callback short-circuit, empty transfer, no qualifying event, incomplete region points or source data, malformed pointers, dropped/partial ACK, target termination and breakpoint-slot contention: retain loss/UNKNOWN accurately, never report Tungsten absent from no-hit.
- Native selection masks and initial construction query distinguished from later geographic/area queries; known D4 regression cases unchanged.

Predeclare a finite **normal-play action sequence** for a later run (one Save52 load, normal travel to Archimedes III W H2O Lub, one genuine Build Mode entry, no construction or edits). There is no automatic retry or forced regeneration. If the sequence ends without a coherent Tungsten observation, preserve diagnostic events and classify `NO_HIT`/`PARTIAL` precisely. This is an unsuccessful scientific acquisition, **not an acceptable minimum-success outcome**. Provide a concrete mitigation or alternate targeted capture plan before proposing another session.

## 5. Prospective Phase B card — prepared, NOT executable

Replace/supersede the candidate-source run card for prospective approval, without rewriting its historical record or pretending it was executed. The revised run card must specify:

- Exact pinned executable/content/configuration, inspected native observation sites, controller build hash, synthetic qualification hashes and objective GO/NO-GO conditions.
- Save52 and the Archive/Workshop identity checks; an operator-readable path to the named outpost.
- Preflight hashes of designated research/manual/quicksaves and **independent** backups, scratch-restoration rehearsal, Steam Cloud controls, protected-input checks and postflight restoration/escalation. Active exitsave/autosave rotation is diagnostic only; historical protected backups remain strict.
- The specific Tungsten-bound receipt/transfer/identity criterion, permitted diagnostic data, buffer/slot/read safeguards and durable ACK/STOP order.
- No-hit handling, useful partial-result classification, scientific comparison, controlled termination and postflight sealing/review steps.
- Explicit prohibition on unrelated body-only success, automatic retries, forced native generation or cache invalidation, target/source modifications, committing or publishing without authorization.

**Do not launch Starfield, load saves into a live process, attach a debugger, instrument retail execution or produce new gameplay saves under this amendment.** No acceptance of Phase A, nor independent approval of a run card, constitutes Phase B authorization. Return the final run card for **explicit maintainer approval of the precise experiment** first.

## 6. Frozen amendment acceptance criteria

These are supplemental to the original D4 AC1–AC8, which must remain passed and unmodified.

| ID | Mandatory acceptance requirement |
|---|---|
| A1 | Preserve original D4 research, D2/D3 predictions, all native receipts, installed inputs, protected saves/backups and Git HEAD/index; no live action. |
| A2 | Source-backed consumer dataflow binds the actual Archimedes Workshop to a **Tungsten ACCEPT** and the same evaluation's spatial transfer, with exact geometry and source ancestry, or transparently demonstrates a blocker and builds an independently useful alternative with objective discrimination. |
| A3 | Working integrated native collector extension; hardware-slot scheduling, identity, bounds, callback short-circuit, cache-hit and generation/consumption epoch limitations explicitly addressed. |
| A4 | Real synthetic Windows debugger tests prove target-bound acquisition, prevent unrelated first-source stopping, and preserve complete/partial/loss classifications and durable ACK semantics. |
| A5 | Offline comparison contract identifies the earliest evidence-supported mismatch without fitting and preserves all seven native geometry controls. |
| A6 | Revised approval-ready one-session run card includes meaningful scientific success, finite actions, no-hit mitigation, pre/post save integrity and no unauthorized retail operation. |
| A7 | Durable provenance, implementation commands, source/receipt/test pins, failure history and **mandatory editorial finalization** for every changed text file. |
| A8 | Independent scientific, engineering and editorial review against the original D4 requirements and amendment A1–A8; verified complete/task-only diffs, exact file manifest and protected-evidence checks. |

The reviewer must explicitly challenge any attempt to substitute the old body-only stop for the Tungsten-bound success criterion. An all-NO-GO finding with no working, scientifically discriminating mitigation fails; so does documentation alone when implementation is feasible under the authorized scope. If a blocker prevents completing a mandatory test, report `REWORK` or `ESCALATE` with concrete evidence; never reclassify an untested condition as PASS.

## 7. Delivery and finalization

Deliver a concise implementation/scientific report, new/updated collector and synthetic tests, a verified offline comparator, the superseding **unexecuted** run card, explicit preflight/postflight recipe, independent original/final-delta review, and verified complete/task-only Git patches with hashes and inclusion/exclusion manifest. Reuse the standard completion contract and project review procedure.

Run automated editorial screening, then manually read the complete changed prose for malformed word/number joins, encoding, conventional `0x` notation and byte offsets, identity-domain clarity, and distinctions between observations, inferences, cache state and generation history. Reviewer verifies the **exact final snapshot**; after-review changes need a scoped independent delta check. No redundant decimal labels or conversions unless useful.

Preserve original raw captures, saves, game-derived payloads and temporary binaries under local-only/ignored storage. Authored code and documentation remain subject to existing attribution/publication review; this amendment authorizes **no public release, B6 work, staging, commit or push**.

Suggested commit after maintainer review: `feat(research): qualify Archimedes Tungsten-bound native acquisition`.
