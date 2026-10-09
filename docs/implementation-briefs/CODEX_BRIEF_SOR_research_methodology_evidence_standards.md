# Codex Brief — Research Methodology and Evidentiary Standards Refinement

**Project:** `starfield-outpost-research`  
**Task type:** Documentation and research governance only  
**Status:** Implementation brief for critical review; **do not commit or push**

## 1. Objective

Refine the project's existing research methodology so that Codex reports and uses the **strongest conclusion justified by evidence, within explicitly stated coverage**, rather than withholding useful findings until a universal engine-level account is available.

This is a **refinement, not a relaxation or replacement**, of the project's established evidence standard. Maintain provenance, reproducibility, counterexamples, honest uncertainty, and critical review. Avoid allowing speculative exceptions to block a valid scoped conclusion. Equally, never call absence definitive where completeness has not been established.

**This task does not reopen the active-outpost investigation.** The recent beacon decoding and membership-limit work has been committed and synced. Do not modify its underlying observations, classifier, scripts, or scientific conclusions as part of this task.

## 2. Inspect existing governance first

Read the current authoritative versions and reconcile their actual terminology, relationships and precedence before editing:

- `AGENTS.md`
- `WORKFLOW.md`
- `docs/EVIDENCE_STANDARD.md`
- `docs/RESEARCH_STATE.md`
- `docs/DECISIONS.md`
- any directly linked fact, hypothesis, state or provenance register instructions required to keep definitions consistent.

Use the current repo's naming and classifications as authoritative. In particular **retain the existing `PROVEN`, `STRONG`, `PROVISIONAL` and other established states as defined there**; do not invent a competing confidence hierarchy or silently redefine their meanings.

Keep changes minimal and coordinated. Put normative rules primarily in the appropriate evidence/methodology document; use concise cross-references elsewhere rather than duplicating paragraphs across many files.

## 3. Introduce a separate coverage dimension

For each substantive semantic finding distinguish:

1. **Evidential confidence:** How strongly the stated interpretation is supported by available observations, interventions, static analysis and corroboration, using the project's existing taxonomy.
2. **Coverage:** The set of object classes, gameplay conditions, save versions, record representations, subsystems and other circumstances actually supported by that evidence.
3. **Completeness, where claimed:** Whether a detector or rule is demonstrated to cover **every qualifying instance within its explicitly claimed scope**.

Confidence, coverage and completeness are different properties. A finding may be `STRONG` within narrow coverage and unresolved outside it; do not downgrade a supported ordinary-case result merely because a distinct exceptional case is not yet understood.

Coverage need not become a rigid new schema or exhaustive form. Use concise, testable statements such as “ordinary player-built beacons in the tested save layouts” and explicitly distinguish **tested**, **inferred**, and **unknown** coverage. Do not imply coverage is exhaustive just because no counterexample was found.

## 4. Adopt an operational rule for scoped conclusions

Document this governing principle:

> Report and use the strongest interpretation supported by reproducible evidence, stating its confidence and demonstrated coverage. Do not require exhaustive understanding of all engine exceptions before using a sound, scoped research result.

Consequences:

- A `STRONG` scoped semantic association may be treated as established working knowledge **within that scope** in later analyses.
- Distinguish recognizing a structure's role from decoding its entire representation, lifecycle, ownership and runtime authority.
- Do not collapse a concrete positive detection into generic `INDETERMINATE` merely because a stronger universal classifier is unfinished. Report the detected property accurately, while leaving unproved membership or universality unresolved.
- Treat accepted findings as **revisable** if contradicted; never shield them from falsification.
- Do not retroactively promote, demote, or rewrite existing findings solely because these methodology instructions changed.

## 5. Specify when to reopen an accepted finding

A finding merits reconsideration when new evidence:

- contradicts it **within its claimed coverage**;
- demonstrates that coverage or provenance was misstated;
- exposes an error in decoding, analysis, experiment or inference;
- or supports a materially better explanation of the same observations.

For new exceptional cases, first determine whether the case is in scope. If outside the demonstrated coverage, record a separate exception or coverage gap rather than suspending the ordinary-case conclusion. The appearance of an exception may justify a **new focused investigation**, but not automatic invalidation of unrelated established results.

Avoid vague objections such as “other representations may exist” as a reason to withhold a scoped finding. An objection should point to a concrete counterexample, observed alternative, relevant executable code path, or an explicit completeness gap that matters to the claim being made.

**Important qualification:** A lack of known counterexamples is not proof of universality or of absence.

## 6. Separate standards by claim and intended use

Distinguish at least the following:

- **Research finding:** A bounded semantic conclusion, supported by the evidence and stated within coverage.
- **Read-only detector/report:** Must state what it actually detects, which versions/representations are supported and which states remain uncertain. A sound positive indicator can be reported even if it does not imply complete membership.
- **Definitive count / absence claim:** “Exactly N active player-owned outposts” or “no active outposts” requires a justified completeness argument for all qualifying representations **within its claimed scope**. An empty candidate list, empty relationship collection or failed signature match alone is insufficient.
- **Save modification or production-grade guarantee:** May require substantially stronger correctness, preservation, recovery and compatibility proof; do not import that standard wholesale into exploratory research.

Useful narrower negatives remain allowed: e.g., “No ordinary beacon candidates were detected by this validated scanner in these supported record representations” is not equivalent to “the save has zero active outposts.”

If current governance defines further distinctions, retain and integrate them.

## 7. Evidence evaluation and scientific autonomy

Codex should independently formulate and test competing hypotheses **within an approved research scope**. It may select the next authorized offline analysis based on likely information gain rather than automatically pursuing the last unresolved decoder field.

Give priority to well-designed causal interventions and independent corroboration, while recognizing that static executable analysis can sometimes establish semantics decisively. Do **not** codify a rigid hierarchy that mechanically overrides evidence quality or source validity.

When a claimed interpretation has concrete contradictions, investigate and preserve negative results. When an exceptional case does not contradict a scoped finding, preserve the useful ordinary-case conclusion and track the exception separately.

Maintain existing authorization gates:

- No new live gameplay, debugger attachment, game/plugin deployment or save modification without explicit authorization.
- No unapproved third-party code incorporation or licensing shortcuts; preserve the standing maintainer-owned `gooberpede` exception with provenance and the separate rights of embedded third-party content.
- Do not alter raw evidence or relax low-disk/output safeguards.
- Durable promotion/reclassification, changes beyond brief scope and commits remain subject to user review.

## 8. Progress obligation and reporting format

Each substantive research report should begin with a compact **answer-first** section or table providing:

| Element | Required content |
|---|---|
| Research question | The specific question investigated |
| Best-supported answer | The strongest currently defensible answer, not just a list of unknowns |
| Confidence | Existing evidence-state classification, accurately applied |
| Coverage | Tested conditions, supported versions/representations, important exclusions |
| Evidence | Reproducible decisive observations/tests and provenance |
| Limitations | Concrete unresolved cases and their actual impact |
| Next step | Highest-information available next test, if still needed |

Reporting uncertainty is essential. But an investigation should not terminate with generic ambiguity when a useful scoped conclusion is already supported. If no answer can be reached, identify **precisely** what prevents it, which routes were tested, what data or engine mechanism is needed, and why that obstacle cannot be resolved within current authorization and capabilities. Do not claim fundamental impossibility when only the current method failed.

Do not require every minor observation or routine document update to use a lengthy table. The convention applies to **substantive semantic findings and research conclusions**.

## 9. Include worked examples, without changing their status

Add short worked examples, grounded in the project's actual reviewed evidence and its current confidence classifications. Use the current durable records, not recollection, to verify exact terminology and limits.

Suggested cases:

1. **Ordinary outpost beacon identification:** Control saves show no beacon before placement and an enabled ordinary beacon afterward; mature Save52 has 17 enabled-clear and two disabled-set beacon records. Distinguish a supported ordinary-case indicator from unresolved exceptional faction/quest ownership and complete enumeration.
2. **Output-link relationship:** Controlled creation/removal/recreation plus no-action controls strongly associate a bounded relationship structure with extractor-to-storage linking, while record ownership, count/framing semantics and generality remain separately unresolved.
3. **Cargo topology:** Mature-save reciprocal pad references reproduce the independently maintained network's connections, but precise mapping of parallel physical-pad instances and transport semantics remains limited.
4. **Location:** Candidate save-side XYZ values have numerical consistency with independently captured local coordinates, while transform ownership, coordinate frame, planetary body and latitude/longitude remain unresolved.

Examples are **illustrative applications of methodology**, not instructions to promote existing records. Where the above informal summaries differ from the current durable reports, use the reports.

## 10. Make the change prospective and non-destructive

- Do not recalculate historical confidence ratings in bulk.
- Do not change saved evidence, parsers, CLI behavior, research algorithms or outpost-identification output in this brief.
- Do not reopen the recent beacon membership investigation or special Terran Armada cases.
- Do not turn the documentation exercise into a general philosophical standards rewrite.
- Keep the original source evidence and counterexamples intact.
- Record the new methodological decision in the project's durable decision process, with scope and rationale, without implying the old scientific results were invalid.

## 11. Validation and return package

Run appropriate repository checks, including:

- `git diff --check`;
- internal Markdown link validation;
- consistency checks for evidence-state terminology and coverage wording;
- scan for contradictory or duplicated instructions among authoritative governance files;
- `git status --short`;
- verify no raw saves, dumps, new binaries or ignored evidence artifacts were staged or tracked;
- verify scientific scripts and existing evidence files were not modified.

Return for critical review:

1. Files reviewed and their current authoritative roles.
2. Files changed and exactly why.
3. The revised confidence/coverage/completeness decision rules.
4. Any conflict resolved between prior instructions, with references.
5. Worked examples and confirmation that no historical results were automatically reclassified.
6. Validation results.
7. Correction/task-only diff and current full diff, including new documents where applicable.
8. `git status --short`.
9. Suggested next **separate** research brief scope (ordinary-case beacon detector refinement), without implementing it.

**Do not stage, commit or push.** No Starfield launch, debugger, SFSE observer work or save-corpus analysis is authorized here.

Suggested commit message for later approval:

```text
docs(research): distinguish evidence confidence from coverage
```
