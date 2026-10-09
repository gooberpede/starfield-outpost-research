# Codex implementation and validation brief — Scoped ordinary outpost beacon detection

**Project:** `starfield-outpost-research`  
**Status:** Proposed; implement and return for critical review  
**Task type:** Offline, read-only research tooling and validation  
**Commit:** Do not stage, commit, or push.

## 1. Objective and governing standard

Build a small, reusable **read-only research detector** that identifies serialized references representing **ordinary player-buildable outpost beacons** and reports their available saved active/disabled-state evidence. The detector should make useful scoped findings now, rather than withholding all positive results until every exceptional outpost and ownership rule is understood.

Apply the newly committed project-wide evidence methodology: keep **confidence**, **coverage**, and **completeness** separate. Preserve existing `PROVEN`/`STRONG`/`PROVISIONAL` classifications and source provenance. Do not claim an authoritative universal active-player-outpost count or a definitive zero-outpost result without the additional evidence those guarantees require.

The immediate research outputs are:

1. **Ordinary beacon identification:** a reproducible, inspectable predicate for the supported serialized representations.
2. **Saved state reporting:** distinguish an explicit disabled-clear bit, an explicit disabled-set bit, and flags omitted or otherwise unresolved.
3. **Scoped interpretation:** report the strongest justified inference about ordinary beacon active state, without silently promoting it into a universal ownership claim.
4. **Visibility into exceptions:** report recognized special/faction beacons and unresolved beacon-like candidates separately, not as ordinary matches and not as grounds to suppress valid ordinary-case results.
5. **Validation and counterexamples:** challenge the detector against known controls and other available corpora.

Do not expand this task into an importer, editor, universal save parser, generic flag investigation, quest-status decoder, or runtime outpost-enumeration project.

## 2. Research basis and required preliminary review

Read the current committed versions of `AGENTS.md`, `WORKFLOW.md`, `docs/EVIDENCE_STANDARD.md`, `docs/RESEARCH_STATE.md`, and the relevant finding/state/decision registers **before changing code**. Use the actual project structure and file names, rather than assuming an outdated layout.

Review and reuse the existing research on:

- Save change-record framing and reference queues;
- conditional beacon base/initial-data representations, including cases 4–7;
- effective base-form resolution and its known limits;
- saved disabled-state reconstruction, including omitted flags;
- ordinary beacon records, faction-template leads, and the separate workshop/ownership predicates;
- the Save3/S0/S1 controlled corpus and mature Save52 results;
- the known ambiguity between an enabled beacon, player ownership, and a complete active-outpost registry.

Preserve the established interpretation that Save52 contains **19 identified beacon candidates**, **17 with disabled clear and two with disabled set**, corresponding to the independently documented 17-outpost network and two historical beacon-like references. That is a strong scoped correlation, not proof of all deletion pathways or all outpost types.

**`IsDeleted` is shelved** as an outpost membership criterion. Record it only if already available essentially for free; do not investigate it further absent an observed outpost-specific set case or an identified outpost-related setter/clearer path. Do not equate the engine's flag names with gameplay operations.

## 3. Detector output contract

Implement the detector as a narrow module or command using the existing offline save-analysis infrastructure. Prefer a structured, machine-readable per-save result (e.g. JSON) plus a compact human-readable summary. Preserve exact provenance for all extracted values.

For each candidate reference, report when available:

- Save identifier, hash/provenance reference, parser/schema/version profile and coverage status;
- physical and logical record location (stream/chunk, record offset/index, reference identifier); clearly distinguish these address domains;
- raw and resolved base identity, including ESM/base FormID only where actually resolved;
- identification category: **ordinary**, **exceptional/faction**, or **unresolved beacon-like**;
- source and confidence for the category (saved value, ESM linkage, static reconstruction, structural evidence, etc.);
- saved disabled-state evidence: **explicitly clear**, **explicitly set**, **omitted**, or **unresolved**, with raw flags/mask and reconstruction basis when available;
- carefully scoped interpretation: ordinary recognized beacon with disabled-clear / disabled-set / unknown state, versus independently established player membership;
- concrete representation/ownership gaps, if any, rather than generic speculation.

Include per-save counts by category and saved-state class. Distinguish:

- **`NO_RECOGNIZED_ORDINARY_BEACONS`** (a scanner observation with stated coverage), from
- **`NO_ACTIVE_PLAYER_OUTPOSTS`** (an authoritative absence conclusion, *not* authorized merely by zero matches).

A save-wide headline should make positive recognized evidence visible. If the implementation also emits an authoritative membership classification, it must remain distinct and may be `INDETERMINATE` while the detailed ordinary-beacon result is positive.

Do not silently skip unresolved or exceptional candidates; provide a bounded way to inspect them without mistaking every generic changed reference for a beacon.

## 4. Primary ground-truth validation

Use **verified, archived copies**, never live originals, for all analyses. Resolve precise paths and hashes from existing project manifests and evidence indexes.

| Corpus/checkpoint | Independent ground truth | Mandatory detector outcome |
|---|---|---|
| Pristine Save3 | No outpost constructed | No recognized ordinary beacon; no universal absence claim inferred solely from this |
| S0 and S0C | No outpost yet | No recognized ordinary beacon |
| S1 and S1C | One ordinary beacon placed, active outpost | Exactly one recognized ordinary beacon, with disabled-clear state where the saved evidence supports it |
| Mature Save52 | 17 active outposts in independent network documentation; two formerly removed beacon-like references | 19 recognized ordinary beacon candidates if the existing resolved identification remains justified; 17 disabled-clear and two disabled-set; report any discrepancy rather than force totals |

Do not feed these expected labels into the detector. Apply the rule to raw decoded evidence, then compare its outputs to independently known gameplay state.

Treat existing interpretations as preregistered hypotheses, not hard-coded desired answers. Any substantive mismatch must be surfaced with record-level evidence and investigated within scope.

## 5. Broader challenge corpus and coverage

After the primary cases pass or expose a concrete issue, run a **bounded challenge** across available previously inventoried saves, including controlled transitions, later mature saves, older-format saves and the separately sourced launch-era third-party corpus where permitted.

- Record parser compatibility and exact support boundaries by relevant version/record representation.
- Test ordinary positive detections and inspect purported exceptional/faction and unresolved candidates.
- Do not use previous signature-derived labels as independent ground truth.
- Separate a real contradiction within claimed coverage from an unsupported representation or an unverified gameplay state.
- Report concrete false-positive/false-negative counterexamples where independently established; otherwise use `UNVERIFIED`, not invented truth labels.
- Do not let quest/faction outpost exceptions suppress or downgrade the ordinary player-buildable case if it continues to pass its scoped tests.
- Historical version differences are eligible research material, not automatic grounds for rejection.

Respect TheDailyXPerience/Nexus corpus provenance and no-redistribution constraints; source raw saves remain untracked and are never copied into public deliverables.

## 6. Implementation and scientific autonomy

Codex has authority to revise existing offline decoding helpers, design bounded synthetic fixtures, test competing ordinary-beacon predicates, and examine relevant ESM/static code if needed to resolve **concrete candidate-identification problems**.

Do **not** require a fresh discussion for each offline hypothesis. Prefer the smallest implementation that produces inspectable positive evidence. Do not duplicate an existing reader unless the replacement demonstrates a clear need.

A valid outcome can be a scoped detector that is useful for ordinary beacons while leaving exceptional ownership and definitive zero-outpost membership unresolved. Do not manufacture certainty, and do not return only `INDETERMINATE` when detailed supported results are available.

If ordinary detection itself remains blocked, explain the **specific actual failed test or missing mechanism**, what was attempted, and the smallest further step capable of resolving it. A hypothetical exceptional representation is not a sufficient blocker.

## 7. Evidence reporting and durable updates

Produce a report that starts with **best-supported answer**, then confidence, coverage, decisive evidence, and actionable limitations.

Include:

1. The exact ordinary-beacon predicate and saved-state decoding procedure;
2. Supported representation/version scope, plus excluded and unresolved cases;
3. A per-save result table for Save3/S0/S0C/S1/S1C/Save52;
4. Detailed Save52 17-clear/two-set correspondence, with source identifiers and independent oracle provenance;
5. A challenge-corpus summary and counterexamples;
6. Tests of positive detection, unknown flags, alternate base representations, parser limitations, and no-recognized-beacon reporting;
7. Explanation of what remains necessary for full player ownership enumeration or conclusive absence;
8. Recommended next highest-information step, prioritizing outpost location only after this scoped tool is ready.

Add/adjust durable research findings only where the new evidence warrants it, using the project's approved confidence/coverage/completeness rules. **Do not silently retroactively promote old findings.** Maintain history and superseding interpretations where needed.

## 8. Hard boundaries and preservation

- Offline and read-only only; **no Starfield launch, live observer, SFSE deployment, debugger attach, save loading or in-game actions**.
- Do not modify source `.sfs` files, the mature network JSON, previous experiment archives, or raw evidence.
- No save editor or write-back functionality.
- No renewed generic `IsDeleted`, native-save automation, Terran Armada quest progression, full workshop-registration, production or coordinate investigations.
- No new third-party source incorporation without the project's current permission/provenance process. Existing maintainer-owned `gooberpede` reuse exception applies, with provenance still required.
- Maintain free-space/resource safeguards and bounded scratch output.
- Keep raw saves/dumps/decompressed blobs and any substantial third-party extracted payloads in appropriately ignored local storage.
- **Do not stage, commit or push.**

## 9. Validation and review handoff

Run the project's appropriate unit/synthetic tests, independently check key candidate counts/flags against known records, validate source hashes unchanged, verify raw-artifact exclusions, check Markdown links, run `git diff --check`, and inspect `git status --short`.

Return for critical review with:

- An answer-first conclusion with **confidence, coverage, and completeness** stated separately;
- Tool invocation and sample machine-readable output schema;
- Primary controlled/mature per-save results and independent validation;
- Bounded historical/third-party challenges and counterexamples;
- Existing limitations, including unresolved ownership and flags omitted from saves;
- Exact new/modified files and reused tooling provenance;
- Validation results;
- Task-only and complete diffs (including untracked text sources);
- Git status;
- A suggested commit message **only**, no commit.

**Suggested commit message after approval:**

```text
research: implement scoped ordinary outpost beacon detection
```

## 10. Completion criterion

**Success** means a repeatable read-only research instrument can identify ordinary beacons and their saved disabled-state evidence for the validated representations, reproducing the no-beacon/one-beacon/Save52 comparisons **without pretending that this proves exhaustive player-owned outpost enumeration**.

A material concrete counterexample must be reported and investigated; unsupported exceptional ownership semantics must be separately documented, not used as an automatic veto against the ordinary-case result.
