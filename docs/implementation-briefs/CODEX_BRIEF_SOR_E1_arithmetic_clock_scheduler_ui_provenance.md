# Codex Research Brief — E1: Production Arithmetic, Clock Domains, Scheduler and UI Rate Provenance

**Repository:** `starfield-outpost-research`  
**Assignment:** Focused offline research continuation of E1 (inorganic extraction)  
**Authority:** Research, analysis, documentation, narrowly necessary non-game verification only. No Starfield launch, observer implementation, save restoration or modification, deployment, staging, commit, or push.  
**Status:** Implementation/research brief for Codex; independent review mandatory.

## 1. Purpose and finish line

Complete the **native production calculation and presentation contracts** sufficiently that another researcher can identify how Starfield obtains an inorganic extractor's per-cycle quantity, production interval, effective modifiers, scheduler behavior, and the production rate displayed in two in-game interfaces. The subject is Starfield's existing native machinery, **not** an extractor-management application or an independent replacement simulation.

The investigation must trace the native producers, consumers, operands, conditions, and units wherever evidence permits, with particular attention to logic likely shared by greenhouses, animal husbandry, and builders. Do not declare the central arithmetic solved merely because an RVA, definition value, or approximate rate is known. Conversely, do not require complete reproduction of every exceptional engine state where the native evidence reaches a justified boundary.

This brief supplements the committed E1 research, `production-report.md`, `production-modifiers.md`, `stacking-report.md`, and related native references. Preserve their established findings and annotate genuine corrections with evidence.

## 2. New independent visual reference: one-extractor Kreet outpost

The maintainer provided two screenshots from **a gameplay state built starting from Save3**, with one **small Iron extractor**, one **solar array**, no crew and no cargo links. Both show required power **5**, total power **6**. The top-right build-mode outpost summary displays **PRODUCTION 1.66/MIN**; the outpost database's **LOCATIONS** view displays **PRODUCTION 1.67/MIN**, for the same outpost. The database screen shows one stored Iron item, which is **not** the subject of this study.

These are independent **observed UI labels**, not captured internal raw values. **Do not assume the protected original Save3 contains that constructed outpost**, nor that the screenshot supplies a fresh saved file. Do not infer exact production interval, item quantity, clock basis, truncation or rounding merely from the displayed values.

Treat the difference as a discriminating trace target: identify the actual native data producers and both UI formatting paths. One plausible hypothesis is truncation versus rounding of a common underlying value near 1.666…, but this is a **hypothesis**, not a conclusion. Other possibilities include different derived or cached values, different update epochs, formatting implementations, and different source units. State what the code confirms and rejects.

If the local screenshots are not present in Codex's workspace, this paragraph is the durable transcription; do not invent access to the image files. Record provenance as *maintainer-supplied screenshots, captured from a Save3-derived gameplay state, not a known existing save snapshot*.

## 3. Required research workstreams

### A. Nominal base interval, quantity, and unit contract

Identify the originating definitions/records and native reads establishing the **base interval** and **base item quantity** for ordinary inorganic extractors. Trace conversions, constants, types, unit interpretation and rounding. Include worked examples grounded in actual definitions for a **small Iron extractor** and, where supported without unnecessary expansion, representative gas/liquid extractors.

Answer explicitly: “N units per what?” Distinguish extractor size/base, produced resource and recipe effects. Never assume the screenshot's rate proves a 36-second cycle or any illustrative quantity.

### B. Clock domain and elapsed-time scheduler

Identify the clock actually used by each relevant scheduling path, including its native producer and unit conversion: real elapsed seconds, universal game time, planetary local time or combinations. Address Jemison's approximately 49-hour local day as a **test of conceptual precision**, not evidence about scheduler internals. Distinguish local-day display time, UT/game simulation, real wall-clock duration, pause/wait/sleep effects, and game-time acceleration where the code differentiates them.

Trace loaded and unloaded scheduling where present, elapsed-time accumulation, countdown resets, fractional carry, multiple due cycles, clamping and overflow/guard handling. Report whether catch-up is calculated on load or continually in another context. Avoid inventing a universal answer when different paths use different clocks.

### C. Effective interval and multiplier sources

Complete the path from nominal cycle interval through applicable actor/player perks and the effective `HarvesterRateMult` (or the exact native equivalent). Trace where the effective extractor multiplier is **calculated or read**, not merely where it is multiplied. Document evaluation order, source types, conditional selection, binary32 details where consequential, and the distinction between effect on **duration** and on **quantity**.

Preserve previously established scoped findings about ordinary crew/robot stacking, player ranks, magazines and Research Project unlocks. Reopen them only when a specific dependency or contradiction in the arithmetic requires it. Note applicability to organic/builders only when backed by a common native call/contract.

### D. Quantity selection, special effects, and realization

Resolve the ordinary and exceptional resource/recipe quantity branches as far as reachable. Investigate whether **Special Projects** or any other distinct effect can add items per cycle independently of the timer effect, and for which production categories. Map item-creation call arguments and downstream acceptance/failure handling. Distinguish **requested output**, **actually accepted/created output**, and **nominal/effective displayed rate**. Do not enumerate stored items, reconstruct all storage logistics or calculate aggregate power generation.

Trace the operational eligibility gate only far enough to explain how power, production halt and relevant output constraints affect schedule execution and realized production.

### E. Both production-rate UI paths — mandatory

**Trace backward from the consumers**, separately:

1. The **build-mode outpost summary**, with its **1.66/MIN** observation.
2. The **outpost database / LOCATIONS view**, with its **1.67/MIN** observation.

For each, identify the responsible native consumer, intermediate data provider(s), input structures/fields, update path, underlying rate calculation or cached summary, conversion to “per minute,” and final numerical formatting. Determine whether they consume a shared native statistic or compute separately. If the source is derived from a saved/global Workshop summary rather than active nearby terrain, document the native evidence and prerequisites; do not infer true remote scheduling or accurate freshness merely because the database UI can show the number at a distance.

Use the observed paired values as a fixed test case. Establish, if possible, the exact source of the hundredth discrepancy. If not, leave explicit competing hypotheses and the minimum attainable discriminating evidence. Include the raw numerical type/precision and rounding/truncation semantics wherever determined. Trace UI consumption with the same scientific care previously used for beacon-preview resource availability.

## 4. Consolidated production dataflow and native function reference

Extend the **existing** native-function register and E1 documentation rather than introducing a competing index. Provide a connected map of:

- extractor/resource/recipe definitions → base rate/quantity;
- source of applicable modifiers → effective interval/quantity;
- elapsed-time clock source → scheduler/countdown/due cycles;
- eligibility and item creation → requested vs realized output;
- outpost aggregate/statistics provider → both UI consumers and formatting.

For relevant native functions record pinned Starfield version, VA/RVA, arguments, outputs, state dependencies, side effects, callers/consumers and confidence/evidence. Distinguish static disassembly, definition records, saves, existing live traces and maintainer screenshots. Mark deferred organic and builder dependencies instead of fully tracing those separate systems.

## 5. Validation and scientific closure

Use only existing pinned executables/Ghidra exports, static game records, save evidence, previous trace corpus and authorized offline scripts. Concrete worked numerical examples must be reproducible from cited game definitions and native operations. If an independently established input is unavailable, show the derivation and the exact missing operand rather than inserting a guessed value.

Require a question-by-question status table: **ESTABLISHED (scope specified)**, **BOUNDED/CONDITIONAL**, or **UNRESOLVED** for the time domain, nominal interval, effective multiplier, requested quantity, scheduler, realized-output conditions, and *each* UI rate path. Explain what a perfect offline result settles and what it does not. No blanket “complete” based on tests exercising a mirrored model.

If specific runtime uncertainty persists, include a **separate GO/REVISE/NO-GO scientific-value assessment** of the smallest realistic live validation that could decide it. The proposed experiment must identify competing hypotheses, an attainable native or visible observation, usable controls/saves, expected conclusions for each outcome, and credible implementation costs. It must not be an excuse to build a broad observer or gather redundant telemetry.

**Save4/S4 consideration:** Existing research identified the relevant controlled-save backup as **Save12**. If an eventual live proposal chooses S4, first verify the exact backup identity, path, hash, configuration and expected in-game load-menu label. The proposed run card must include an explicit, safe restoration from the protected backup to the game's `Saves/` directory, check for pre-existing destination and overwrite collisions, and preserve original metadata/provenance. **Do not restore a save now.** The screenshot outpost is not automatically a usable persisted control save.

## 6. Deferred documentation correction

Add a prominent, accurate supersession note to the earlier `production-feasibility.md` and the appropriate research index: the later stacking analysis resolved the ordinary multiple-crew selection question statically and its previously proposed crew-stacking live test is no longer recommended. Other runtime questions remain open. Preserve the historical report and prior outcome instead of silently rewriting it.

## 7. Scope boundaries and stopping rules

- Offline research only. No Starfield launch, live actions, injection, observer, deployment, controlled native invocation, save restoration/editing, staging, commit or push.
- Do not build an extractor app, a production simulator or a replacement game subsystem.
- Do not widen into organic-facility eligibility, full builder mechanics, production-network logistics, generator totals or vanished-deposit reproduction.
- The standing D1 hypotheses remain durable references; update a falsifier opportunistically **only** if this assignment produces genuinely decisive evidence.
- Follow significant native dependencies *within the arithmetic and UI provenance scope* until established or an evidence-bounded limit is reached. Do not stop merely because a function has been named, but do not chase unrelated subsystems to achieve cosmetic completeness.
- Respect protected input pins and original evidence. No automatic deletion or modification of research source material.

## 8. Review and deliverables

Use the project's research execution/completion workflow: primary agent, optional narrowly targeted specialist, and **mandatory independent reviewer** (at most two concurrent subagents). The reviewer must challenge clock-unit interpretation, numerical assumptions, UI rounding claims, counterexamples, and premature bounded outcomes. Resolve in-scope reviewer rework within the assignment and document any residual limitations.

Deliver:

1. A technical report answering each of A–E and documenting exact/native units and sample calculations.
2. A two-path UI-provenance comparison explaining what is known about **1.66/MIN versus 1.67/MIN**.
3. Updated native function register/dataflow and relevant E1 research records.
4. A clear producer-modifier matrix covering crew/robots/skills/magazines and any new quantity-related effects, scoped to supported code.
5. Updated historical live-feasibility supersession notice.
6. Reproducible verification commands/results, preservation checks, a scientific uncertainty/possible-live-validation assessment, and an independent review record.
7. `-task-only.diff` and `-complete.diff` in `.local-work/diffs/`, including **untracked authored text**, plus a manifest with SHA-256 hashes, diff reconstruction checks and repository status.
8. An explicit prose-quality audit of new/changed documentation, checking for concatenated words, fused version/address/count tokens and other malformed prose.

Suggested conventional commit only; do not commit. The final summary must clearly distinguish **base production**, **effective production**, **actual produced items**, and **UI-displayed production rate**.
