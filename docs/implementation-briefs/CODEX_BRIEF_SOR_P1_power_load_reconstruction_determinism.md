# Codex research brief — P1 follow-up: Load-time power reconstruction and determinism

**Project:** Starfield Outpost Research (`starfield-outpost-research`)  
**Type:** Focused offline native/save investigation, documentation, and independent review  
**Status:** Proposed follow-up to the **uncommitted** P1 generation/allocation/switch package  
**Authority:** Read-only investigation only. No game launch, controlled save creation, injection, observer build/deployment, original-save mutation, staging, commit, or push. Do not discard or overwrite the existing P1 changes.

## 1. Purpose and decisive question

The completed P1 follow-up demonstrated that consumer allocation is sensitive to traversal/root order, and that a saved electrical graph alone may not identify the root of the **last runtime recalculation**. That finding **does not establish** that allocations differ after loading identical saves.

Investigate:

> For a saved outpost with insufficient available power, how does Starfield establish its **settled** per-consumer powered state on load, and does the load/rebuild process deterministically reproduce the same allocation from identical saved state and game definitions?

The scientific concern is substantial: if root/iteration ordering varied across reloads and affected final allocations, identically loaded deficient outposts might power different consumers. Treat this as a **hypothesis to discriminate**, not an established defect. Do not assume the final state is the result of replaying the last pre-save recalculation. Equally, do not infer repeatable load outcomes simply because some containers appear ordered.

### Required plain-language answers

Start the report with a compact answer table:

1. **What does the game do on load?** Does it restore saved powered bits, recompute allocation, or use both in a specific order?
2. **What chooses the effective load-time root(s) and sequence?** Is the sequence invariant, deterministically rebuilt from saved/definition data, dependent on runtime registration/order, or unresolved?
3. **Would identical save reloads necessarily power the same consumers?** Answer **established yes / established no / not yet established**, with the exact scope of evidence. Never equate “not yet established” with “nondeterministic.”
4. **Can an offline reader predict those settled outcomes?** Identify the smallest sufficient saved inputs, definition inputs, and any genuinely runtime-only inputs.
5. **What is the smallest decisive next test if static evidence stops short?** Specify it precisely; do not execute it without separate authority.

Put detailed Ghidra reasoning, offsets, traversal pseudocode, and negative findings below this executive answer. Avoid using “conditionally reconstructable” as the entire conclusion.

## 2. Required starting evidence

Read `WORKFLOW.md`, `AGENTS.md`, `docs/RESEARCH_STATE.md`, `docs/DECISIONS.md`, and the existing *uncommitted* P1 package under `docs/experiments/power/`: especially `report.md`, `native.md`, `saved.md`, `followup.md`, `availability.md`, `uncertainties.md`, and `review.md` **where present**. Consult earlier Workshop/save population and E1 power-state evidence only as needed. Reuse the pinned retail executable/native exports, existing function register, protected original save corpus, and established verification conventions.

Verify actual paths and build/RVA pins before referring to them. Existing P1 addresses and labels are leads, not substitutes for checking native instructions.

Carry forward these distinct previously reported facts/questions without conflating them:

- Graph connections have saved representations (`ExtraPowerLinks`, type `0xCB`); their order is not by itself proof of load-time allocator order.
- A runtime owner reverse-reference index (`Extra4D`) influences generator-root gathering; its rebuild order and provenance require tracing.
- Event-triggered allocations may begin from a changed reference or connection endpoint; these do not automatically establish the load-time entry point.
- Consumer powered-state flag (`0x40`) exists separately from switch open/closed persistence. Its read/restore/recalculation lifetime requires investigation.
- Previous offline fixtures demonstrated order sensitivity with different starts, **not** variation over repeated loads of the same save.

Inspect the uncommitted task-only/complete diff and manifest as necessary to avoid treating the current Git HEAD as the complete P1 state.

## 3. Workstream A — Load/rebuild lifecycle

Trace the **actual native path** from serialized reference/extra-data restoration through Workshop association, electrical link resolution, graph/index rebuilding, power initialization and the final stable powered-state update. Identify:

- Which saved fields initialize per-object powered state; whether the `0x40` bit is authoritative, temporary, overwritten, or treated as a dirty/cached value.
- Which callbacks can update power during load, reference resolution, cell attach/activation, Workshop initialization, registration and later deferred jobs; their ordering and dependencies.
- Whether a Workshop-wide or network-wide final refresh supersedes earlier object-local recalculations, and how the **last effective writer** is chosen.
- Whether results can change after apparent loading has completed due to delayed references, asynchronous tasks, fuel/activation changes or subsequent attach events. Define a practical **settled state** boundary, not merely a first-frame sample.

Produce an ordered, evidence-linked lifecycle diagram or table distinguishing **saved data**, **restored intermediate state**, **first allocator call(s)**, and **settled result**. If a necessary step is not statically demonstrable, mark the edge unknown rather than inventing an initialization sequence.

## 4. Workstream B — Sources of order and reproducibility

For each load-time path actually implicated by A, trace the provenance and ordering of:

- Generator roots, including `Extra4D` reverse-index construction/registration and any owner-level enumeration.
- Electrical adjacency (`ExtraPowerLinks` / `Extra4C` as applicable), traversal queue/front promotion, visited tracking, consumer-vector expansion, and recursive/nonrecursive setting.
- Handle resolution, reference creation/registration order, map/hash/container enumeration, pointer or allocator-address dependence, and any parallel/deferred timing relevant to final allocation.

Separate **deterministic relative to a particular initialized runtime graph** from **deterministic across independent reloads of the same save**. Identify exact potential sources of variation (if any) and whether native code actually exposes them on the final load path.

Revisit the prior example networks only insofar as their identities, connections, powered bits, and roots can be grounded in protected real saves. A synthetic replay may verify logic for controlled input orders, but **cannot** alone prove repeated-load consistency. Avoid claims about construction order as a priority unless independently proved.

## 5. Workstream C — Competing hypotheses and falsifiers

Explicitly test the available offline evidence against at least these models:

| Hypothesis | Discriminating evidence sought |
|---|---|
| **H1: Deterministic recomputation** | An invariant load-time initialization/refresh chain with reproducible roots and ordering |
| **H2: Deterministic restoration** | Saved powered states retained as the settled outcome, or restored before a bounded deterministic refresh |
| **H3: Rebuild order varies but does not change final outcome** | Ordering differences proven immaterial under relevant deficits / canonicalized before assessment |
| **H4: Outcome genuinely varies across reloads** | A reachable source of varying final assessment order **and** material impact on which consumers receive power; ideally repeated identical-save live observations |

Other models may be added. Do not mistake failure to establish H1/H2 for proof of H4. Distinguish code paths that are merely possible from those established as load-reachable. Explicitly state whether the native and saved evidence can discriminate the hypotheses without a live experiment.

## 6. Bounded validation plan — proposal only

If offline investigation cannot decisively establish repeated-load behaviour, specify a **separately approvable** practical experiment:

- One deliberately power-deficient outpost with identifiable equivalent consumers and stable generation/fuel conditions; preserve a baseline save and its hash.
- Reload the **same unchanged save** multiple independent times; make no building, switching, wiring or inventory changes.
- Record the same identified consumers' powered states after a defined settled-state criterion, along with total supply/demand, connectivity, switch positions and any transient recalculations.
- Propose the **least invasive** observation method first (game UI or an already-qualified read-only facility, if it can genuinely distinguish per-consumer state). Only propose new runtime instrumentation if necessary, with separate scientific and safety approval.
- Explain what observations would falsify deterministic outcomes and what repeated identical outcomes would and **would not** prove. Describe a second contrasting configuration only if the first cannot discriminate the question.

**Do not run this experiment, alter saves, start the game or build an observer under this brief.**

## 7. Evidence, documentation and completion

Integrate findings in the existing `docs/experiments/power/` package rather than creating a rival P1 reference. Write a focused load-determinism report, update existing native/saved/uncertainty and function-register entries as warranted, and append new research-state/decision/backlog entries only for substantiated results or explicit deferred questions. Preserve earlier claims and record corrections transparently.

For each consequential conclusion identify the pinned executable/version, exact function RVA or save field, provenance, and whether evidence is **native-static**, **definition-backed**, **save-corroborated**, **synthetic/offline-tested**, or **live-observed**. State confidence separately from **COMPLETE / INCOMPLETE / BLOCKED** assignment disposition. COMPLETE means this **bounded offline task** is adequately investigated and any remaining empirical boundary is precisely identified; it does **not** mean reload determinism was proven.

Required deliverables:

1. A short **plain-English executive answer** followed by the traced load/rebuild lifecycle, ordering provenance, and a hypothesis-discrimination matrix.
2. A specific saved-versus-runtime availability statement: can the eventual powered set be decoded, computed, only observed live, or not yet determined?
3. Exact unresolved predicates and a feasible minimal follow-on experiment, **only if** offline evidence cannot settle them.
4. Independent reviewer assessment per `WORKFLOW.md`, addressing especially any conflation of “missing last-event root” with “nondeterministic reload,” and any conflation of saved flag with settled state.
5. Focused source/native checks, relevant tests and receipts, protected-input hash comparison, and a prose audit for fused words, malformed Markdown, wrong RVA/version notation and corrupted encoding.
6. Task-only and **combined complete** textual diffs (including relevant untracked text), forward/reverse exact patch reconstruction checks, and an output manifest/checksums under `.local-work/` conventions. Keep proprietary binary/native/save evidence out of review diffs.
7. Suggested Conventional Commit subject for the **entire still-uncommitted P1 package**.

Do not expand into generation ratings, day/night, general fuel logistics, unrelated save decoding, local storage, cargo links, implementation of a production power calculator, or speculative debugging branches. Do not stage, commit, push or claim approval to perform a live test.

## 8. Success criterion

A reader must be able to distinguish **(a)** why event-triggered allocation can be order-sensitive, **(b)** what actually happens during restoration and post-load recalculation, and **(c)** whether identical-save final allocations are demonstrably reproducible. If (c) cannot be proven offline, the report must explain **which exact missing observation** prevents a yes/no answer and provide a practical, discriminating next test—without presenting uncertainty as evidence of a Bethesda defect.
