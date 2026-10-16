# Codex Research Brief — E1 Continuation: Inorganic Production Arithmetic, Modifier Sources, and Live-Validation Feasibility

**Project:** Starfield Outpost Research (SOR)  
**Repository:** `D:\Projects\starfield-outpost-research`  
**Assignment type:** Offline native research, source/definition/save analysis, documentation, and an experiment-feasibility decision.  
**Authority:** No Starfield launch, deployment, native invocation, observer implementation, save modification/restoration, staging, commit, or push.

## 1. Purpose and research endpoint

Continue E1 rather than moving immediately to organic production (E2). The prior E1 result was **CONDITIONALLY COMPLETE**: native pathways for inorganic extractor identity, states, links, and scheduling were mapped, but the **effective production-interval arithmetic, output-quantity selection, and modifier sources** were not fully characterized.

The objective is to document Starfield's existing native functions, data and calculations at a level another researcher can leverage. **Do not build an extractor tool, a simulation, or a reimplementation of the whole production system.** The investigation must distinguish static game definitions, serialized save data, offline disassembly-derived runtime behavior, and actual runtime observations; **none are interchangeable**.

The work has two deliverables with independent completion assessments:

- **E1 production arithmetic and native contracts:** identify how nominal intervals/quantities become effective rates and realized production, mapping native operations and dependencies as far as justified.
- **Live-validation feasibility assessment:** establish whether a small, controlled live experiment would materially resolve a specific remaining uncertainty. Decide GO / REVISE / NO-GO, but do not implement or run it.

## 2. Research inputs and starting points

Read `WORKFLOW.md`, applicable project instructions, the existing E1 documentation in `docs/experiments/inorganic-extractors/`, the native function register and research state, prior resource-availability output contract, and D1 disappearing-deposit hypothesis ledger. Reuse their conventions and cited native evidence rather than constructing a competing register. Identify source-build and RVA provenance for every native finding.

E1 previously identified resource-defined production intervals, native interval conversion, multiplier/entry-point dispatch, binary32 producer-row scheduling, due-cycle calculation, eligibility checks, and resource/recipe-dependent quantity creation. **Verify these relationships against the pinned native evidence; do not treat this brief's description as proof.**

Preserve established project-owned research material, saves, Ghidra projects, source exports, protected installations, raw traces, and frozen test corpora. No destructive or in-place changes to originals.

## 3. Mandatory investigation: production arithmetic

Map the actual native calculation from extractor and resource definitions through operation and item creation. The report must separate:

1. **Nominal production:** base cycle duration and quantity, definition and recipe sources, units, defaults, and classification differences where demonstrable.
2. **Effective production:** evaluation order for interval modifiers, quantity modifiers, rounding/truncation, binary32 transformations, stacking, clamping, and conditions, as supported by actual code.
3. **Realized production:** elapsed-time/countdown processing, number of due cycles, eligibility/halted/power checks, output item count, storage/output interactions only where they materially affect whether resources are created.

For each missing step, identify the exact function, relevant arguments or state, and what evidence would settle it. Numerical examples are useful only if derived from qualified definitions or explicit synthetic cases; distinguish them from measured retail-game results. Preserve edge cases and exceptions, avoiding intuitive replacement of native arithmetic.

Produce a compact operation/dataflow map showing interval and quantity calculations separately and identifying the point at which actual output is created. Aim for an actionable native contract, not necessarily a standalone reproducer.

## 4. Modifier-source investigation

Examine whether, where, and under what conditions these potentially influence inorganic production:

| Candidate source | Required determination |
| --- | --- |
| Assigned outpost crew | Whether bonuses affect eligibility, cycle duration, output quantity, or another relevant state; native dispatch and prerequisite conditions |
| Robots | Same, including whether the mechanism is shared with crew or distinct |
| Player skills/perks | Applicable entry points, predicates and direction of influence where supported |
| Skill magazines/permanent bonuses | Determine whether these contribute; **do not presume that they do** |
| Other discovered effects | Document only effects actually encountered in traced native paths |

For every source, classify **confirmed participant**, **excluded within a precisely inspected path**, or **unresolved**. Identify and distinguish modifier producer (e.g., perk/actor/definition) from consumer (the extractor/scheduler) and whether modifiers apply to *interval*, *quantity*, *operational eligibility*, or *another stage*. Describe observed ordering and combination if recoverable.

Do not expand into comprehensive crew AI, robot systems, skill-magazine catalogs, player progression, outpost power distribution, cargo logistics, or general perk machinery. Follow those dependencies only far enough to establish and properly bound their effect on the production calculation. Note potential reuse by organic production without asserting identical mechanics.

## 5. Controlled save inventory and live-test feasibility

**Save4 / S4 on Kreet is only a candidate control.** Verify the exact saved identity, available backup, character, load-menu metadata, Workshop/extractor inventory, resource associations, and any relevant configuration from existing files and accepted save-analysis tools. Do not assume it contains a suitable working extractor or a useful modifier contrast. Compare other available saves and recommend a better candidate if justified.

**Important operator/run-card requirement:** The original S4 save file is **not currently present in the game's `Saves/` directory**; only the research backup remains. If a future approved experiment uses S4, its proposed run card **must contain explicit, safe steps to restore the correct byte-verified backup to the game's `Saves/` directory before launch**. Specify the grounded source and destination paths only after verifying them; include filename/identity, original hash, collision/overwrite safeguards, expected load-menu display, and a post-experiment integrity/cleanup plan. Do not restore or modify any save as part of this offline assignment. Never silently overwrite an existing save. A save backup or a copied file's timestamp may not accurately reflect the original in-game displayed timestamp; verify instructions using the project's save-menu tooling and provenance.

Assess candidate live tests only against specific remaining native-production uncertainties, for example:

- Whether a particular native interval/quantity modifier's input and output actually correspond to effective producer-row values;
- Whether a controlled variation in skill/crew/robot state changes native calculation through the identified path;
- Whether scheduler output agrees with the native quantity and elapsed-time calculations;
- Whether power, halted/activation, and operational status are distinct in a qualified live extractor.

These are suggestions, **not** required experiments. First determine what the current static evidence can already settle. Never propose instrumentation simply because a field can be observed.

For each proposed experiment, explicitly state: (a) a consequential uncertainty; (b) competing hypotheses; (c) the *minimum practical observation* that discriminates them; (d) suitable saved/control conditions; (e) what an ideal success, counterexample, or no-signal result would establish; (f) observer/callback and lifetime risks; and (g) why existing captures cannot answer it. Identify whether an existing, qualified observation boundary could suffice or whether new instrumentation would be necessary. Do not falsely claim an existing hook is qualified for a new type of read.

**Hard scientific-value gate:** If perfectly collected data would settle little or merely duplicate existing evidence, recommend **NO-GO**. Permit **REVISE** if a worthwhile test exists but controls or contracts are insufficient. Recommend **GO** only for a feasible, discriminating test with a meaningful expected conclusion. A GO is permission to *propose* a subsequent brief, **not** permission to instrument or launch.

Do not introduce arbitrary time or record-count targets, new observer builds, direct native calls, or broad studies of remote resource queries.

## 6. Connection to D1 without enlarging scope

Consult the durable D1 ledger (D1-H1 through D1-H4) and its falsification tests. If traced extractor scheduler/association behavior directly tests an existing prediction—especially whether installed extractors retain a persistent resource identity independent of current deposit geometry—record the qualified evidence against that stable identifier. Otherwise preserve the hypotheses unchanged and do not investigate the deposit bug anew.

The separate backlog investigation of creation/deletion chronology, **including runtime as well as save-derived evidence**, remains deferred. Organic E2 likewise remains separate.

## 7. Evidence quality and completion standards

A valid finding must identify its basis:

- Native instructions or pinned decompiler evidence (with executable version, VA/RVA, call/branch relationship and provenance);
- Game definitions/records (with exact form/reference identities and definitions);
- Save records (with save identity, exact file hash and extraction scope);
- Prior live captures (with actual archived observation scope);
- Inference or hypothesis (clearly labeled, not promoted to observed fact).

Distinguish *what the executable could calculate* from *what it actually calculated for a specific extractor during live gameplay*. Distinguish powered, halted/activated, eligible, and producing if native code supports distinct states. Avoid claims about current in-game values derived solely from saves or static instructions.

Classify the **arithmetic mapping** as COMPLETE / CONDITIONALLY COMPLETE / INCOMPLETE against the agreed technical-reference endpoint. Every unresolved component must identify whether it is consequential and why. Classify **live-test feasibility separately** as GO / REVISE / NO-GO, with meaningful falsifiers and cost/risk analysis. Do not broaden the research merely to avoid a conditionally complete result.

## 8. Workflow, quality, and deliverables

Use the project's research-execution and independent-review protocol: primary Codex implementer, independent reviewer, and at most one specialist where useful; no more than two sub-agents concurrent. The reviewer must independently challenge native-contract claims, modifier participation/exclusion, separation of evidence types, and the scientific-value assessment. Complete justified corrections within this assignment.

Perform a **prose-quality audit** of all authored/changed Markdown and reports. In particular, detect and correct fused words, glued numbers/RVAs/version identifiers and malformed spacing; preserve literal code, identifiers and filenames. Verify links, scripts, source pins, relevant existing regression tests, and preservation within the supported local environment. Report test coverage honestly; don't replace inaccessible native checks with asserted success.

Provide:

1. Concise primary report and completion classification;
2. Native interval/quantity/realized-output dataflow and function-register updates;
3. Modifier-source evidence matrix including negative and unknown findings;
4. Controlled-save inventory and **conditional S4 restoration run-card fragment**, only if S4 is credibly selected for a proposed experiment;
5. Independent GO/REVISE/NO-GO live-validation feasibility report with test predictions and minimum observation contract;
6. D1 continuity notes only for newly relevant evidence;
7. Independent reviewer findings, changes/corrections, verification commands/results, preservation receipts, and a remaining-uncertainty register;
8. Task-only and complete review diffs under `.local-work/diffs/` (including newly created text files), output manifest and relevant SHA-256 hashes, clean repository status report, and a suggested Conventional Commit subject.

**Authorization boundaries:** Work offline only. No Starfield game launch, live observer or Vortex package creation, SFSE injection, direct invocation of native game functions, game save restoration, save mutation, historical evidence replacement, staging, commit, or push. Further live work requires a separately reviewed and authorized brief and package.

## 9. Stopping rule

The research is successful if it provides a materially clearer, evidence-backed account of effective production arithmetic and its actual modifier dependencies, even if some arithmetic remains unresolved. An independently justified NO-GO on live validation is an acceptable and complete feasibility result. Stop at the agreed subsystem boundary and report unresolved dependencies; do not create an ever-expanding sequence of ancillary investigations.
