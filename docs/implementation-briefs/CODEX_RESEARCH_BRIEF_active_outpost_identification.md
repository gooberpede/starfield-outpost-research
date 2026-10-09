# SOR Research Brief — Active Outpost Identification from Save Files

**Project:** `starfield-outpost-research`  
**Work type:** hypothesis-driven research, implementation and independent validation  
**Priority:** core research blocker  
**Disposition:** work remains uncommitted pending critical review

## 1. Objective and required outcome

Starting with the controlled **no-outpost Save3** and **one-outpost S1** saves, determine **what serialized information distinguishes a save that reconstructs at least one active player-owned outpost from one that reconstructs none**. Develop a reproducible method for identifying active outposts and, if the evidence permits, conclusively establishing their absence.

**Do not stop at a suggestive signature, a list of candidates, or another report of uncertainty.** Continue generating and challenging hypotheses, writing and using offline tooling, consulting existing project research, and testing against independent evidence until one of two substantive outcomes is reached:

1. **Answer:** a defensible, reproducible identification method, with precisely defined applicability, evidence, counterexamples, and tests; or
2. **Demonstrated obstacle:** a rigorous account of why an answer cannot presently be established from the available evidence and permitted methods, identifying the exact missing information, showing which attempted approaches failed and why, and specifying the smallest concrete observation or capability that would overcome the obstacle.

A generic statement that save data is complex, distributed, compressed, version-dependent, or insufficiently understood **does not satisfy outcome 2**. Nor does exhaustion of one parser design, one byte pattern, or a self-imposed investigation budget. If a line of attack fails, change the method rather than merely restating uncertainty.

## 2. Starting assumptions — not a proposed solution

Use the following as an investigative premise:

> A Starfield save, together with the game's installed engine and content definitions and any required dependencies, must provide sufficient persistent state for Starfield to reconstruct the saved active game state reliably. An active outpost cannot depend solely on transient state from a previous process that is unavailable after restart.

This is **not** a claim that the `.sfs` contains every static asset or definition, nor that outpost membership is necessarily stored as a flag, one record, one collection, or any particular field. An ESM or other installed content can define *what an object type is*; save-dependent state must still distinguish the particular gameplay state being restored. If investigations reveal qualifications involving external data, load order, missing plugins or version migration, document them precisely.

**Do not let this premise predetermine the search strategy or representation.** Discover the representation from evidence. You are expressly authorized to challenge assumptions in earlier SOR research, including the meanings assigned to previously identified candidate structures.

## 3. Primary ground truth and supporting evidence

Identify the exact files and existing verified archive records; do not guess paths or hashes.

- **Save3:** pristine state before constructing the first outpost; known zero-active-outpost starting point.
- **S0 and S0C:** no-outpost manual checkpoint and no-action control from the controlled session.
- **S1 and S1C:** one beacon placed, constituting one outpost, and its no-action control.
- **Subsequent S2–S7C / L0–L2C:** controlled changes and independent corroborating structures.
- **Save52:** mature character with 17 documented active outposts and complex cargo relationships, including additional beacon-like records outside the known network.
- **Other historical and launch-era saves:** diversity and counterexample corpus, **not automatically labelled ground truth** merely because a previous heuristic classified them.

Ground truth for Save3, S0/S0C and S1/S1C is based on the operator's controlled gameplay actions, not on the current save parser. Verify source identity, integrity and experimental provenance before analysis.

The maturity, historical complexity, and suspected bugs of older saves do not invalidate them as observational inputs, but they make them inappropriate as replacements for clean causal controls.

## 4. Research autonomy

You have **broad authority to decide how to investigate the question**. In particular, you may:

- compare the controlled files at any informative level of encoding or serialization;
- build, revise or replace narrowly motivated offline parsers, comparators, structural decoders, reference resolvers or diagnostic tooling;
- analyze adjacent or globally shared save structures if necessary to understand membership;
- propose multiple competing hypotheses and design tests intended to falsify them;
- examine any already-authorized, locally available research save copies and historical corpora, including older-version formats;
- use documented xEdit/ESM identities, static binaries, prior Ghidra work, and other source evidence relevant to outpost reconstruction;
- conduct **offline** static analysis of loading/deserialization and workshop membership mechanisms if the save-byte evidence alone does not settle the question;
- leverage maintainer-authored code from `gooberpede` repositories under the standing provenance rule;
- revise earlier classifications when contradicted by stronger evidence.

The permitted scope is **whatever general serialization knowledge is genuinely necessary to answer this outpost-specific question**, not an unrelated survey of Starfield's entire save format.

**No preferred method is prescribed.** Do not treat prior candidate beacon tokens, the bounded relationship collection, the `0x79` grammar, compact reference tables or name strings as mandatory starting explanations. They are available evidence, not required solutions.

## 5. What counts as an active outpost

The primary target is an **active player-owned outpost that Starfield reconstructs as part of the player's current game state**. Distinguish that from:

- residual or retained data associated with a deleted outpost;
- a beacon-like record without established active membership;
- static world/content definitions;
- generic workshops or unrelated objects;
- transient runtime or serialization bookkeeping;
- historical associations in the player's save.

Do not require proof that absolutely no outpost-related bytes remain to classify **zero active outposts**. Conversely, absence from one known relationship collection is insufficient, as demonstrated by the S1 counterexample.

## 6. Scientific milestones

### A — Positive identification

Produce a save-side identification rule that recognizes S1 and S1C as containing an active outpost, excludes Save3/S0/S0C, and survives independent challenge against later controlled and observational samples.

An algorithm that merely recognizes a particular one-outpost fixture without a justified underlying semantic relation is not enough.

### B — Conclusive zero-active-outpost identification

Develop a defensible **completeness argument** within an explicit scope: demonstrate why the identification procedure cannot silently miss a differently represented active outpost in the supported save format/state. The aim is a warranted `NO_ACTIVE_OUTPOSTS` result, not a convenient default when searches fail.

A scoped conclusion (for example, supported version range/record families/content conditions) is preferable to an unjustified universal claim. State exactly what remains indeterminate and why.

### C — Broader validation

Apply the method blindly to historical, mature and third-party saves, recording predictions **before** consulting previous heuristic classifications or, where applicable, the external network JSON. Challenge it with known counterexamples, cross-session token remapping, partially decoded saves, earlier versions and residual beacon-like records.

Use three outputs where justified:

- `OUTPOSTS_PRESENT`
- `NO_ACTIVE_OUTPOSTS`
- `INDETERMINATE` — with a specific technical reason, not simply “no match found.”

Report counts only for classes genuinely justified by the validation. Do not force total classification of all third-party saves without evidence.

## 7. Hypothesis quality and falsification

For every promising proposed rule, record:

1. its precise mechanism and expected serialized observations;
2. predicted results for the controlled positives and negatives **before** running the relevant validation;
3. independent corroboration and potential circularity;
4. counterexample searches and observed failures;
5. distinctions between raw bytes, parsed structure, reference identity and game-level semantics;
6. its claimed coverage and what could invalidate that coverage.

Separate source-grounded observations from inferences. An exact byte pattern or count that tracks an action is evidence, but does not by itself establish authority or completeness. A working classifier and a convincing argument for *why it works* are both required.

Do not treat the mature-save JSON as an oracle for all historical saves or as a parser input that bakes in desired answers.

## 8. Persistence and structural constraints

Track file offsets, compressed-block positions, logical record locations and reference identities separately. A save loaded and re-saved may legitimately change offsets, short tokens and emission order without changing the original saved file. Candidate rules must not assume the old file itself mutated.

Cross-version files remain eligible for analysis. Distinguish unsupported layouts from corrupt or empty states, and distinguish format drift from different gameplay history.

Avoid unbounded artifacts; retain existing safeguards around disk capacity and raw evidence. Use ignored `.local-work/` locations for save copies, decompressed blobs and large scratch output; preserve original bytes and hashes.

## 9. Safety and scope boundaries

Authorized without further consultation: extensive **offline, read-only** research on verified copies; code development, synthetic tests, local evidence analysis, static inspection, and durable documentation.

**Not authorized by this brief:**

- launching or loading Starfield saves in the game;
- new live gameplay/control experiments (including beacon deletion);
- SFSE deployment, debugger attachment to the live game or code injection;
- editing, rewriting, replacing, deleting or moving original saves;
- redistributing third-party saves or substantial raw extracted payloads;
- incorporation of unrelated third-party code outside established permission policy;
- staging, committing or pushing.

If a genuinely decisive live test becomes necessary, do all offline work possible, state the specific proposition the test would discriminate, and request separate authorization. **Do not use lack of live authorization as an excuse to terminate exploratory offline work prematurely.**

## 10. Required durable outputs

Produce a research report and, if successful, a usable, testable identification implementation or reference algorithm. Include:

- definitive file/ground-truth provenance for Save3, S0/S0C, S1/S1C and validation sets;
- hypotheses considered, including failed and falsified alternatives;
- exact structural/identity evidence supporting the chosen rule;
- positive and negative classification behavior on known controls;
- completeness reasoning for any `NO_ACTIVE_OUTPOSTS` claim;
- blind corpus testing, counterexamples and version coverage;
- explicit differentiation of observations, inferences and unresolved issues;
- bounded reproducible commands/tests and expected outputs;
- limitations and smallest targeted follow-up needed if any milestone remains blocked.

Update current research registers and relevant experiment/state documents to reflect **validated** findings. Preserve prior negative results and provenance; do not silently relabel old inconclusive samples. Maintain the standing distinction between controlled Save3 micro-experiments and mature-save observational discovery.

## 11. Persistence and review discipline

This is intentionally **not a quick first-pass task**. Pursue multiple grounded lines of inquiry in one execution rather than returning with a generic “further research needed” recommendation. Do not arbitrarily stop after finding that the first attractive signature fails.

Nevertheless, scientific honesty is mandatory: do not declare conclusiveness without evidence, invent completeness, or manufacture a success to satisfy the brief. If no warranted final rule can be demonstrated, the report must supply a **persuasive technical obstruction** with concrete counterexamples, exhausted avenues, missing capabilities/information, and an actionable decision point—not a vague plea for more time.

A partial validated milestone is valuable and must be reported, but is **not** equivalent to completing the whole objective.

## 12. Validation and handoff

Before returning:

- verify original and archive hashes of every source used;
- run synthetic and corpus regression tests and preserve failures;
- run `git diff --check` and validate changed internal Markdown links;
- verify no raw save/dump/binary is newly tracked;
- inspect `git status --short`;
- provide an exact changed-file inventory and provenance for any reused code.

Return:

1. the strongest identified rule or explicit technical obstacle;
2. milestone A/B/C outcome separately;
3. reproducible test method and empirical results;
4. known counterexamples and blind validation coverage;
5. whether a definitive zero-outpost result is justified, and under exactly what conditions;
6. supporting evidence paths and durable records;
7. implementation/tooling changes;
8. failed alternatives and unresolved points;
9. any narrowly justified request for a **separate** live experiment;
10. review diff, checks and `git status --short`.

**No commit or push.** Proposed commit message, only after critical review:

```text
research: identify active outpost membership in save files
```
