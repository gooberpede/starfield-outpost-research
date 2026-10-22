# Codex implementation brief — RG2-C1E: Native Resource-Region Ancestry and Geometry Reconciliation

**Project:** `D:\Projects\starfield-outpost-research` / `gooberpede/starfield-outpost-research`  
**Status:** AUTHORISED FOR OFFLINE PREPARATION ONLY. **RETAIL LIVE EXECUTION REQUIRES A NEW, EXPLICIT MAINTAINER APPROVAL AFTER RUN-CARD REVIEW.**  
**Primary case:** Save52, Feynman V “Cu Co Ni IL” (P3), Ionic Liquids; Copper positive control.  
**Fallback / later cross-check:** Save52 Carinae III-a “Rc Fe”, Iron, only as separately proposed below.  
**Publication:** B6 remains on hold.

## 0. Mission and hard stop

Build on the successful RG2-C1D native oracle. Follow the **actual P3-bound Ionic Liquids spatial-transfer result backwards** through the native area consumer into the accepted cached resource regions, their source identities, query operands and, where achievable, generating context. Acquire *new discriminating evidence* capable of distinguishing a wrong offline source/context, a wrong generator interpretation and a wrong spatial consumer. Copper provides a control. Keep RG1/RG2 frozen predictions unchanged. Biome-source selection at mixed-biome Feynman is an explicit hypothesis, not a presumed cause. Cache/resource mutation is an input/lifecycle uncertainty, not a bug-reproduction mandate.

**Two-phase authority:**

- **Phase A — offline implementation, synthetic qualification, run-card preparation, independent review:** authorised now. Read-only static native research, read-only existing local receipts, collector modifications, synthetic executable/debugger tests, offline comparison/replay, protected evidence inventories and documentation are permitted under existing project policies.
- **Phase B — Starfield live pilot:** **NOT authorised by this brief**. Before any Steam launch, game process creation, Save52 loading for testing, Starfield attachment, retail debugger arming, native runtime sampling, save creation, or controlled in-game activity, STOP and deliver the complete run card and Phase A evidence to the maintainer for review. **Only a fresh explicit maintainer go-ahead may authorise Phase B.** The general willingness expressed to conduct live tests is not that go-ahead. Do not silently proceed after independent reviewer acceptance or successful synthetic preflight. If the maintainer later authorises a pilot, obey the exact approved run card and scope; changed target, additional tries, or expansion require approval as specified in that card.

Do not confuse preparing a preflight script with executing a retail preflight that starts the game. File/hash checks of installed binaries and backup saves may be done offline and recorded; the final time-of-execution preflight must be rerun after a future approval.

## 1. Required existing evidence and policy intake

Read and apply current `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_EXECUTION_PROTOCOL.md`, `docs/PERMISSIONS.md`, `docs/templates/completion-contract.md`, and the existing frozen AC/records. Resolve filename or scope differences from repository contents rather than guessing. Relevant existing records include:

- `docs/experiments/resource-oracle-retail/{report,implementation,run-card,review}.md` and existing ignored RG2-C1D receipts/analysis, including the P3-bound refresh payload at static VA `0x1421e0bf4`;
- `docs/experiments/resource-geometry-observation/{native-contract,report,cases}.md`;
- `docs/experiments/native-availability-map/{output-contract,region-lifecycle}.md`, region/point predicate provenance;
- `docs/experiments/resource-geometry/{native,evaluator}.md` and `docs/experiments/resource-geometry-mature-context/{report,f1-reconciliation,seed-lineage}.md`;
- `docs/experiments/resource-ui-oracle/` and `docs/experiments/resource-oracle-collector/`;
- `docs/experiments/disappearing-deposits/` where relevant.

Pin actual `Starfield.exe` **1.16.244.0** SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` and installed definition identities. Treat preferred static VA, RVA, runtime VA, object offset, save reference token, runtime reference/handle, source index and native resource FormID as separate domains.

C1D proved a P3-bound **pre-install spatial transfer** containing IL `Starfield.esm:0057d4` and Copper `Starfield.esm:0057cf`; it did **not** prove cache installation, current generated-region positions, historical generator inputs, or a P3-bound catalogue invocation. Preserve precisely those distinctions. No source-selection claim may rely merely on same FormID or nearby time.

## 2. Backward ancestry to be investigated

Begin with actual source-verified C1D transfer lineage rather than assigning a visually plausible region. Map native execution and dataflow across:

1. Area updater `FUN_1421e07d0`, spatial callback `FUN_1421e0f50`, temporary accepted-resource set, enumeration and transfer at `0x1421e0bf4`.
2. Each IL/Copper accepted region's true ACCEPT/REJECT edge, native resource identity, order/ordinal, query coordinates/radius/upper bound, and source/resource collection ancestry. The callback's normal function return is **not** a per-region acceptance verdict.
3. Cached-region provenance: source selection, region bounds and complete ordered XYZ/width points; distinguish single-point disk, multipoint strip and bounding representations. Never infer the game-drawn coloured overlay directly from an unjoined consumer.
4. Candidate producer/source upstream (`FUN_14079f860` and generation chain `FUN_14079b520 → FUN_14079c470 → FUN_14079a330`) where exact observational joins are available. Record effective BIOM/RSGD, component, family/masks/weights, source frame/owner, packed spatial key, RNG seed/order, other-resource competition and lifetime/epoch if observed. **Do not manufacture historical generator input values from current cached regions.**
5. Mixed-biome source selection: distinguish beacon biome, queried cell biome, selected procedural source biome and effective generation biome. Treat the discrepancy as hypothesis-driven, not an excuse for unsupported fitting.

Prefer an actual naturally occurring consumer call which can be bound to P3 and whose accepted region(s) explain IL's inclusion. The design must explicitly cover whether the current observer can capture the accepted temporary set's provenance before it is reduced to bare resource pointers. If not, give a concrete guarded additional breakpoint/callback/region sampling plan.

## 3. Collection contract: scientific minimum and completeness

The prospective receipt should, as feasible, bind:

- exact executable/session and loaded game/save identity; Workshop identifier and runtime reference/parent chain; case, resource and associated file;
- area updater/callback ancestry and per-thread nested invocation tokens; observed payload-to-callback association, not time proximity;
- actual per-use native Qb/Qc/Qv/Qe coordinates, radius and upper/descriptor operands with floating-point bit representations where necessary;
- accepted and rejected region decisions at their true native edges; source key/slot and resource collection; bounds and complete ordered points/widths for IL and Copper regions that were actually examined or accepted;
- collection completeness, short-circuit behaviour, unknown/truncated fields and recorded loss;
- source/owner/BIOM descriptor and cache lifecycle/epoch association where **witnessed**, else UNKNOWN.

A single identity-bound accepted IL region with its geometry and consumer query is a valuable first success. The design must not label that a complete P3 region census unless source enumeration/short-circuit coverage is established. If a full deep copy is unsafe or exceeds bounds, define a minimal read-at-stop variant with durable partial evidence and clear scope. The collector may not invent empty lists from failed reads.

Separate **consumer geometry evidence** from **producer evidence**. Stage 1 tests actual consumed regions against the unchanged offline evaluator. Stage 2 (generation observations or recreation under qualified exact inputs) is contingent on what Stage 1 establishes and must be proposed in the run card; do not install an expansive generator observer unnecessarily.

## 4. Offline engineering and qualification: mandatory implementation effort

Extend the demonstrated C1D controller and SRO1/receipt/accounting pipeline. Do not replace it with a new framework unless a specific demonstrated blocker and an actionable replacement are documented. Implement useful retail-specific read/decode/ancestry logic and guarded observation points **offline**. Required tests include:

- real Windows debugging against disposable synthetic native-layout fixtures, not fixture-supplied fake capture values;
- source- and stack-bound callbacks leading to accepted-resource transfer, positive and negative regions, singleton disk and multipoint paths;
- nested/reentrant callbacks, multi-thread lifetime changes, stale or wrong Workshop, wrong source, wrong-region FormID, caller mismatch, partial/empty/corrupt collections, invalid/unreadable pointers, oversized counts and allocation/byte budget refusal;
- exact read/ack/durable-flush/independent-parse before controlled target termination; crash-before and crash-after capture; abort/LOSS accounting;
- association of the region to the actual P3 transfer under a demonstrable ancestry token or an explicitly weaker observation class; no pointer+timestamp epoch invention;
- retention of existing C1D regression coverage and zero modifications to protected real saves, definitions and previous raw receipts.

Supply performance/copy ceilings informed by fixture and static evidence. Existing C1D synthetic success does not itself prove retail lifetime safety. The test may tolerate a disposable game crash **after** complete externally verified evidence in a future authorised pilot; no unbounded writing, undocumented native mutation or implicit auto-restoration of saves.

## 5. Frozen offline comparison / replay

Plan a mechanical comparison against existing frozen RG1/RG2-A1/F1 geometry before changing any prediction. Define which observations discriminate:

- different effective source/owner/biome/frame inputs → context selection mismatch;
- same effective generation inputs but different native paths → generator interpretation mismatch;
- matching paths but different native area verdict → consumer/query interpretation mismatch;
- identical local computation but different cached population/epoch → lifecycle/source-history mismatch.

Do not infer deterministic input uniqueness from one catalogue resource set. Quantify coordinate-frame precision and spatial matching rules. Copper is an independently saved positive control, not a tuning target. Preserve original prediction versions unchanged; any revised hypothesis/prediction requires its own version and evidence. If generation inputs are unavailable, report a consumer-only verdict honestly.

## 6. Prospective retail run card — submit for human approval, DO NOT EXECUTE

Prepare a complete stand-alone run card, including:

1. **Proposed exact target and conditions:** pinned EXE, Save52 identity (and archival SHA), Feynman V P3 Workshop binding, IL primary and Copper control, target event/addresses with relocation and instruction guards; natural trigger and evidence expected at each stop.
2. **Launch, attach and breakpoint schedule:** operational steps and commands for a user and/or Codex, ordering of load/build-mode action, expected debugger stops, maximum approved *proposed* attempts/sessions and fallback behaviour. If a specific number is not technically justified, propose a small bounded number and explain why.
3. **Save preflight and recovery:** complete SHA-256 inventory of relevant live saves and separately held backups; verify both, prove scratch restoration on disposable copy, check write/sync paths and Steam Cloud status; controlled deviations classified. Some risk to hash-backed live saves is permitted; sole recoverable copies are not expendable.
4. **Stop and postflight:** externally fsynced/readback/independently parsed evidence must precede successful stop. Disposable retail process may crash or be terminated afterward. Rehash live and backup saves after each attempt, record additions/removals/changes, and propose restoration from verified backups if needed; restore only under documented authority and verify restored SHA-256. Preserve crash/incomplete evidence and diagnostics.
5. **Scientific classification:** observed region/source/context versus unknowns, comparison artifacts to frozen predictions, exact stopping/escalation criterion and independent review of output.
6. **Fallback:** Carinae III-a Iron may be proposed if a *specific Feynman obstacle* is demonstrated. It is **not authorised as an automatic live switch**; include its own identity, preflight, scope and approval step. Feynman VIII-b instability is out of scope unless independently authorised.
7. **Operational authority statement:** clear box at the top: `NO LIVE RETAIL TEST IS AUTHORISED BY RG2-C1E; A SEPARATE MAINTAINER GO-AHEAD IS REQUIRED AFTER REVIEW OF THIS CARD.`

Complete offline preparation and present the run card **before** Starfield execution. Don't present a prospective plan as an executed measurement. Don't use reviewer acceptance as implied permission to launch.

## 7. Deliverables

Durably record, in a new appropriately named research experiment folder or consistent extension (choose stable names): (a) research finding and source/callsite ledger, (b) collector code and synthetic tests, (c) region/ancestry and receipt contract, (d) offline comparison specification, (e) **approval-ready live run card**, (f) risk/mitigation and evidence-integrity report, (g) verification and independent review. Update relevant research register/index/next-step only where justified. Exclude proprietary binaries/decompilation dumps, native raw exports, private saves and raw/debugger receipts from committed authored material under established permissions. Keep local exact-hash receipts ignored and preserved.

Produce verified final **complete** and **task-only** diffs, changed/new-file manifest, independent final review and pre-submission summary. Nothing is staged, committed, pushed, cleaned up or published by Codex. Do not run B6.

## 8. Frozen acceptance criteria AC1–AC8

- **AC1 — Authority and preservation:** Offline Phase A only; no Starfield launch/attach/live gameplay; protected inputs/previous receipts/frozen predictions/HEAD/index unchanged. Clear future live approval gate and backup-hash practice.
- **AC2 — Native result ancestry:** Exact code/dataflow from P3 spatial transfer toward region callback, actual acceptance edges and source populations; unsupported joins labelled.
- **AC3 — Working acquisition implementation:** Meaningful collector extension plus real synthetic-debugger qualification, not only a design report. A region/geometry receipt is actually obtained from synthetic target memory.
- **AC4 — Scientific coherence:** Complete identification and coordinate/region/query contract, honest partial/unknown/lifecycle treatment, no invented P3 equivalence.
- **AC5 — Model discrimination:** Frozen offline comparison/replay procedure, explicit four-way possible divergence, Copper control and biome alternative.
- **AC6 — Constructive route:** Actionable retail observation plan capable of obtaining *new* accepted-region/source geometry; demonstrated blockers must receive testable mitigations, not an all-NO-GO report. Carinae fallback precisely bounded.
- **AC7 — Approval-ready run card:** All launch, bounded sampling, identity, save pre/postflight, evidence durability, stop/failure and post-analysis steps specified and **submitted for maintainer review without execution**.
- **AC8 — Independent review and delivery:** Independent critic assesses AC1–AC7, code and actual synthetic results, authoritative and reviewed research assertions, changed-text/source integrity, and exact final complete/task-only patches. No omitted post-review deltas.

**Stop condition for this brief:** once Phase A implementation, qualification, independent review, exact diffs and the live run card are delivered, **STOP**. Await an explicit new maintainer instruction; do not start retail Phase B on your own.
