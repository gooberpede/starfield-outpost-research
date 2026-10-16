# Codex Research Brief — SOR D1: Disappearing or Substituted Inorganic Deposits

**Assignment:** One bounded, offline reconnaissance of a reported Starfield outpost defect. **One Codex attempt; no do-overs or subsequent investigative rounds under this authorization.**

**Repository:** `D:\Projects\starfield-outpost-research`.

**Decision status:** Commission research and documentation only. No game launch, SFSE/Vortex deployment, observer, native invocation, save mutation, experimental reconstruction of the game, or new gameplay session. Do not stage, commit, or push. The subsequent inorganic/organic extractor programme is separate and not authorized here.

## 1. Scientific question and observations

Investigate which *specific, testable* native mechanisms could explain a previously established outpost losing a known resource deposit, or having a deposit's resource type change (for example, Gold becoming Copper), when the player returns. Existing extractors placed on apparently lost veins may continue operating, but additional extractors cannot be placed on the absent vein. Sometimes veins later reappear.

The principal objectives are to: (a) identify concrete affected outposts and controls in the available save corpus; (b) formulate strong, falsifiable hypotheses; (c) test them offline to the extent evidence permits; and (d) state the **minimum realistically achievable falsifying test** for any hypothesis that cannot be invalidated offline. It is entirely acceptable, and likely, that no root cause will be proven. Scientific value lies in discriminating findings and native mechanisms that will inform later extractor research.

**Do not presume** a cache invalidation bug, random/procedural reseeding, saved-coordinate drift, changed vein generation, a UI/reporting anomaly, or a placement bug. Those are hypotheses only where supported by explicit native mechanisms and falsifiable predictions. Do not treat absence of a preserved deposit mesh or historical preview list in a save as proof of disappearance.

### User's historical observations (eyewitness accounts, not independently verified save states)

- **Feynman, Gold/Antimony (Au/Sb)** outpost: an existing resource deposit appeared to vanish temporarily; resource substitution, including Gold becoming Copper, is part of the general class of observed issue. Verify whether the affected Feynman site specifically showed substitution; do not silently assign the example to it.
- **Decaran, Vytinium/Helium-3 (Vy/He-3)** outpost: player selected a site with both resources, built it, and on a later visit could no longer find the He-3 deposit.
- Across incidents, **extractors built earlier could continue producing** despite the relevant deposit no longer permitting new extractor placement. Some deposits later returned. The user suspects cache-related changes after travel or visits to other outposts, but has no conclusive timing/reproduction sequence.

The initial research must locate relevant outposts across accessible saves (including—but not presuming—Save52), verify world, outpost reference/ownership, coordinates, constructed extractors and their associated resources, and report missing or ambiguous identity matches. Preserve original save bytes. Prior research includes saved-outpost inventories, extractor/resource associations, native availability output maps and resource-region lifecycle notes; reuse those as evidence and starting points, not as substitute proof.

## 2. External reports provided by the user (summarized here for offline access)

These are **players' reports, not authoritative root-cause evidence**. Keep observation, claimed workaround, inference and verified native finding separate. Read the links if accessible; use this self-contained summary if Reddit blocks access. Include original URLs and access dates in the research bibliography.

### A. Reddit — "Is anybody else noticing outpost resource sources disappearing?" (16 September 2023)
https://www.reddit.com/r/Starfield/comments/16jwju9/is_anybody_else_noticing_outpost_resource_sources/

- Original poster described an Andraphon Iron/Aluminium/He-3 outpost: He-3 disappeared after exiting/restarting, including when reloading saves that previously showed the vein. Existing extractors worked, but they could not place new ones or move old extractors to new He-3 locations.
- Replies include apparent **resource substitution** (He-3 replaced with Aluminium; another site's deposits moved or Neodymium appeared), restored deposits after a shutdown or reload for some people, and cases where reload did not help.
- One commenter described Helium-3 extractors remaining operational while new Neodymium deposits appeared underneath them. Another reported a former He-3 deposit becoming Beryllium.
- Do not collapse these reports into a single proven failure mechanism; commenters differ in symptoms, versions and recovery behavior.

### B. Reddit — "Mineral Veins disappearing" (4 September 2023)
https://www.reddit.com/r/Starfield/comments/169ko1k/mineral_veins_disappearing/

- Original poster reported a vein disappearing after building an outpost, exiting and reloading; an existing extractor still occupied the area but additional extractors could no longer be placed on the vanished resource.
- Comments describe inconsistent resource lists between saves (Al/Fe/He versus Al/He versus Al only), sometimes restoration after repeated reloads, and one anecdote that connecting power to extractors appeared to help. **The power claim is an uncontrolled anecdote, not established causality.**

### C. Starfield Community Patch — issue #703 "Resource / ore veins dissapearing / changing" (opened 29 November 2023)
https://github.com/Starfield-Community-Patch/Starfield-Community-Patch/issues/703

- Specific report on **Kaptyen I**, game 1.8.86.0, involving He-3, Aluminium, Nickel and Platinum: Nickel disappeared, while a Platinum vein changed into Nickel. Already placed extractors reportedly continued working.
- Reporter observed no change across certain intra-landing-area movements, ship travel and immediate return, but did observe changes after taking off and traveling within the system, returning from a different location, and occasionally after reopening a save. This is an **individual's limited empirical sequence**, not a validated deterministic trigger.
- As checked 16 October 2026, issue #703 appeared **open**, marked **Needs Vetting**, without a documented fix or linked PR in its page. Do not present it as a confirmed root cause or established repair.

### Additional context from initial public search (not mandatory hypotheses)

- March 2024 Reddit posts describe disappearing Iron/Copper deposits and inconsistent effectiveness of reloads: https://www.reddit.com/r/Starfield/comments/1blg5g6/ .
- January 2025 discussion distinguishes non-depletion of veins from intermittent resource reassignment and reports old extractors continuing to produce: https://www.reddit.com/r/Starfield/comments/1i90iio/ .
- April 2026 report says a previously scouted Lead vein was missing after a trip for construction supplies: https://www.reddit.com/r/Starfield/comments/1svi772/outpost_resource_vein_disappeared/ .

**Codex must perform a broader, time-aware search** for credible explanations, reproductions, game patches, Bethesda statements, SFCP issue history or accepted fixes (using accessible public sources, GitHub issue searches, official patch notes, other community reports and local references). Record exactly what was inspected and distinguish current verified fixes from speculation. An inability to access Reddit is not a reason to abandon the task: the above summaries provide the required seed evidence. Do not assert a known root cause solely because users recommend reload/power cycling. If search facilities are unavailable, document the limitation and use accessible local/public records; never fabricate search results.

## 3. Save identification and test/control design

1. Inventory accessible save material and existing extractor/outpost metadata tools. Identify exact save names, version/build, character, outpost/Workshop IDs, planetary bodies, coordinates and resource associations for Feynman Au/Sb and Decaran Vy/He-3; name ambiguities and temporal coverage.
2. Where saves permit, compare chronological snapshots from the *same* outpost and distinguish persistent extractor associations, site geometry/context, Workshop resource metadata and installed equipment. Distinguish what the save **actually serializes** from generated runtime resource geometry that it may not contain.
3. Choose **justified controls**: e.g., unaffected outposts with similar inorganic extractors, resources, saved chronology, and/or same-planet context where available. Explain what each control can discriminate; avoid claiming an outpost is definitively unaffected simply because no report exists.
4. Reuse existing native mapping of resource-region generator/provider, current ProcGen maps, Workshop updater, descriptor construction and extractor associations. Trace only additional native placement/production/geometry/cache paths necessary to evaluate a specific hypothesis. Do not expand into a general extractor or terrain-generation survey.

## 4. Hypothesis protocol — falsification comes first

Each retained hypothesis requires a compact evidence table containing:

- **Mechanism:** precise native dataflow, storage/lifetime, serialization, coordinate or state relationship that could produce disappearance/substitution.
- **Distinct prediction:** what should differ between affected examples and controls, or between earlier and later snapshots; which component would remain stable if installed extractors keep operating.
- **Falsifier:** a specific achievable observation that would *rule out the hypothesis as stated*, not merely fail to confirm it.
- **Offline test and actual finding:** source and saved bytes, extraction method, test case/control, observed values and ambiguities.
- **Disposition:** falsified within tested scope; remains possible with positive supporting observations; unresolved due to unavailable evidence; or discarded as unfalsifiable/unmotivated. Do **not** label a surviving hypothesis "confirmed" merely because a proposed falsifier was not found.
- **Minimum further falsification test:** if offline evidence cannot decide, state the smallest *realistically available* native observation, existing save comparison, repeatable game procedure or bounded code-analysis step that could produce the falsifier; explain concrete feasibility, required inputs and controls, limits, and cost. Do not invent an omniscient oracle, inaccessible telemetry or magical reconstruction of unrecorded historical state.

Do not mandate a number of hypotheses. Prefer a few mutually discriminating, mechanism-grounded tests over a long speculative list. Explicitly consider whether the observations describe (i) the Available Resources set, (ii) actual geometric vein/deposit locations, (iii) extractor placement eligibility, and/or (iv) persistent extractor production: evidence for one is **not** evidence for the others.

Plausible starting candidates **only if native evidence supports them**: different generated region geometry/seed/context after load; incorrect coordinate translation or reference frame; inconsistent source/map caching or lifecycle; changed type assignment to spatial source/region; separation of production's persistent extractor-resource association from placement's contemporary vein geometry. Other candidates may supersede these. A candidate is not valid unless it has a distinct obtainable falsifier.

## 5. One-attempt rule, stop condition and boundaries

- **Exactly one integrated Codex attempt.** A single planned primary investigation, with the normal independent reviewer reviewing that finished work and allowing ordinary factual/formatting fixes *within that same attempt*. No fresh investigative rounds, repeated implementation cycles or automatic follow-up after an inconclusive review. Prioritize the highest-value discriminating tests and stop at the agreed research budget rather than attempting to exhaust all conceivable dependencies.
- No edits to protected saves, binaries, executables, historical observer captures or Ghidra projects. No in-game action or live experiments, no observer/injector/DLL implementation, no arbitrary native calls, no new resource/extractor implementation, and no attempt to reproduce the bug by changing save files.
- No requirement to reach a single root cause. An evidence-bounded inconclusive result is acceptable if it establishes concrete findings, falsifications and achievable next tests. Reject hypotheses that survive only by being made unfalsifiable.
- Keep **E1 inorganic** and **E2 organic** research strictly out of scope. The eventual broader project needs inventories, type/size, power, links, production cadence/quantity (plus organic current/eligible output and input sufficiency), but **none of those full subsystem deliverables are required in D1**. Map incidental native connections only where they directly test a D1 hypothesis.
- Follow `WORKFLOW.md` and the current repository's research/execution protocol; respect existing frozen evidence, provenance and branch requirements. No staging, commit or push before maintainer review. Keep an ordinary mandatory independent review, no uncontrolled sub-agent proliferation.

## 6. Deliverables and final decision

Produce a compact but durable research package under an appropriate `docs/experiments/` location, integrated with existing native-function registers and provenance rather than duplicating them:

1. **Findings report:** definition of observed phenomenon, exact matched/unmatched affected saves and controls, meaningful negative findings, and what the investigation learned about the relevant native machinery.
2. **Save and control matrix:** identifiers, source provenance, hashes, timestamps/builds where reliable, extractor/resource associations, direct serialized evidence and absence-of-evidence limitations.
3. **Hypothesis/falsification ledger:** mechanism, distinct predictions, attempted offline falsifiers, actual result, confidence and minimum realistic further tests.
4. **Public-source ledger:** summarized user-linked reports, dates/builds, broader public search, credible known fixes if any, contradictory accounts and citation URLs; separate claims from primary native evidence.
5. **Native technical additions:** only necessary new function references, RVAs/build pins, field relationships and call/dataflow evidence; annotate static versus runtime-validated claims.
6. **Independent review and verification:** selected preservation hashes, links, reproducible commands/results, and explicit challenge to the quality of each hypothesis and its falsifier; prose-quality audit of the *entire changed text* for fused words/version tags (past recurring defect).
7. **Review artifacts:** task-only and complete unified diffs (complete includes new/untracked text), review package/manifests and hashes under `.local-work/` according to project convention; avoid raw proprietary assets in the diff.

**Final judgment:** `EXPLAINED`, `PARTIALLY DISCRIMINATED`, or `INCONCLUSIVE`, with evidence for the exact disposition. None is a failure to complete this one attempt. Say explicitly whether a proposed subsequent test would be useful enough to justify its cost; **do not commission it here**. Suggest an accurate Conventional Commit subject, but do not commit.

## 7. Pre-submission sanity questions

Before delivery, Codex and the independent reviewer must answer:

- Were the Feynman and Decaran sites actually identified, or merely inferred from names/memory?
- Did a saved extractor association get mistakenly presented as evidence of a currently visible vein?
- Does each surviving hypothesis have a real falsifier and a concrete, feasible minimum further test?
- Have we tested against substantive controls, or merely accumulated anecdotes?
- Does public searching reveal a documented cause/fix, or only affected users and suggested workarounds?
- Did any scope creep from D1 into full extractor research, speculative implementation or live experimentation?
- Did the final documentation avoid malformed prose and accurately mark incomplete or negative evidence?
