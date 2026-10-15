# Prose correction and diff-scoped audit

2026-10-15. [Governing correction brief](../../implementation-briefs/CODEX_BRIEF_SOR_080_prose_correction_scientific_go_nogo.md),
[scientific decision: NO-GO](scientific-value-reassessment.md),
[independent reassessment review](reassessment-review.md).

The original handoff contained recurring missing spaces and compressed technical
phrases. The earlier implementer and reviewer missed them. This correction
repairs their full task-added documentation surface and separates historical
engineering acceptance from the decision to conduct a useful experiment.

## Scope and method

The audit inventory is the 24 authored Markdown paths in the earlier
`.local-work/local-readiness/final/changed-files.json`, excluding the unchanged
user-supplied original brief. Existing files were inspected in the context of
their task-added hunks, not reformatted repository-wide. New experiment files
were read as complete documents. The three correction documents are also in the
final review surface. Both supplied briefs remain unchanged inputs.

A contextual manual pass covered headings, paragraphs, tables, instructions,
links and technical notation. A literal edit list assisted the repair; 71
file/phrase replacements in 16 documents were recorded before further manual
sentence repairs and status updates. That count describes the first edit pass,
not an assertion that exactly 71 defects existed or that pattern matching proved
the prose sound. Exact before/after text is available in the correction-only
patch and the local baseline snapshot.

The local task baseline is `.local-work/local-readiness-reassessment/baseline.json`,
with the 51 pre-correction files copied byte-for-byte under `before/`. It also
pins 377 immutable code, source-ledger, candidate-build, prior-review and selected
evidence files. No build, observer/native program, qualification suite or live
operation was run for this documentation task. Validation consists of text,
link, patch and preservation checks; it cannot validate a scientific hypothesis.

## Representative defect log

The malformed strings in the Before column are intentionally quoted defects.

| File | Before | After / repair |
|---|---|---|
| CREDITS.md | `project-owned070/060/evaluator` | A complete sentence naming project-owned observers 0.7.0 and 0.6.0 and the evaluator/save-menu/shared-session methods. |
| docs/RESEARCH_STATE.md | `prepare observer0.8.0` | `prepare observer 0.8.0` in the initial prose pass; the entry now states the NO-GO disposition and unchanged engineering history. |
| docs/SOURCES.md | `owned070/060`; `HEAD0906…` | Names the two observer versions with spaces; separates HEAD from the unchanged, exact commit hash. Repairs the missing verb in the methods-reuse sentence. |
| docs/function-register.md | `RVA021e0a46` | `RVA 021e0a46`; the address itself is unchanged. |
| docs/state-register.md | `Schema8` | `Schema 8`; no schema identifier or bytes changed. |
| docs/implementation-briefs/README.md | New entry's `invoked2026-10-15` | `invoked 2026-10-15`; the correction and original briefs have distinct status entries. Older committed entries outside this task were left untouched. |
| runtime/README.md | `observer0.8.0` | `observer 0.8.0`, with the NO-GO disposition made explicit. |
| runtime/session-tools/README.md | `version8`; ambiguous `remains 070` | `version 8`; `remains for 0.7.0`. Adds the withdrawn 0.8.0 proposal's status without changing the adapter. |
| local-readiness/contract.md | `indexed24`, `cache0x68`, `closure0x18`, `source-value slot8` | `24-byte indexed descriptor`, `0x68-byte cache snapshot`, `0x18-byte closure`, `8-byte source-value slot`. H1–H6 remain identifiable historical hypotheses. |
| local-readiness/native-map.md | `state0x68 includes vector triples`; `Source visit reads closure0x18, slot8` | Rewrites the layout paragraph into complete sentences with explicit snapshot lengths and hexadecimal field offsets. Separates VA from its unchanged address. |
| local-readiness/schema.md | `schema8`, `version0.8.0`, `Tags101–110`, `at most256` | `schema 8`, `version 0.8.0`, `Tags 101–110`, `at most 256`; rewrites tag roles so blob names and byte lengths are unambiguous. |
| local-readiness/release.md | `schema8, retail1.16.244.0`; `runtime0.2.21`; `hashes,13` | Adds spaces around schema/build/runtime versions and count; preserves every artifact/member hash and numeric value. |
| local-readiness/review.md | `separate0.8.0`, `observed070`, `verifies611,926`, `supplies080`, `exit0` | Expands versions/counts into readable prose and uses `exit code 0`; labels the earlier PASS/ACCEPT accounting as historical. |
| local-readiness/run-card.md | `least40,000,000,000`; `active0, queued0, losses0, failed0` | `least 40,000,000,000`; explicit zero-valued counters. Marks the entire procedure withdrawn and the old approval premise superseded. |
| local-readiness/processing.md | `070 actual … /35,574 … /346`; compressed resource names | A grammatical reference sentence with unchanged counts and spaced resource names. Keeps code identifiers intact. |
| local-readiness/validation.md | `entry32-byte`, `All6847`, `including080`, `comparisons0` | Separates counts/version labels, uses `6,847` and `comparisons: 0`; labels all results historical and not rerun. |
| local-readiness/invocation-assessment.md | `cannot oracle missing geometry/freshness` | `cannot serve as an oracle for missing geometry or freshness`. The recommendation remains premature; no invocation work follows. |

Paths abbreviated as `local-readiness/…` in the table are relative to
`docs/experiments/`. The exact file manifest disambiguates them.

## Full original-task documentation audit

Each row received a contextual pass; the result is not inferred from absence of
the representative strings above. Technical literals were preserved where they
are actual identifiers, paths, hashes, register names or native field notation.

| Audited path | Result / nature of edit |
|---|---|
| CREDITS.md | Corrected the new credit paragraph and added reassessment credit; old entries unchanged. |
| README.md | Replaced only the new summary paragraph with the NO-GO status and current links. |
| docs/README.md | Updated only the new index entry to the reassessment and audit. |
| docs/RESEARCH_STATE.md | Corrected and superseded only the new experiment entry; native findings untouched. |
| docs/SOURCES.md | Repaired only SOR-S-0150 prose and cited the same evidence for the reassessment. |
| docs/experiments/README.md | Updated only the new experiment entry's disposition. |
| docs/experiments/evidence/README.md | Preserved the new evidence classification and added the historical-receipt distinction. |
| docs/function-register.md | Repaired the new RVA label; added the experimental-disposition caveat without changing contracts. |
| docs/implementation-briefs/README.md | Corrected the task entry; indexed the correction brief and superseded the original handoff. |
| docs/state-register.md | Repaired schema label; kept state semantics and classifications unchanged. |
| docs/subsystems/initial-map.md | Checked the new section in context; added the NO-GO link without revising native findings. |
| runtime/README.md | Corrected version spacing and replaced only the current task's introduction/status. |
| runtime/session-tools/README.md | Corrected the added adapter description and clearly marked 0.8.0 as unadopted. |
| runtime/local-readiness-080/README.md | Corrected prose/version labels and added a NO-GO banner; code and historical build unchanged. |
| docs/experiments/local-readiness/contract.md | Repaired measurements/versions; retained original hypotheses and criteria as historical, with explicit H1 interpretation caveat. |
| docs/experiments/local-readiness/native-map.md | Repaired layout sentences, version/VA labels and current-status wrapper. |
| docs/experiments/local-readiness/schema.md | Repaired tag descriptions and prose labels; binary/schema semantics unchanged. |
| docs/experiments/local-readiness/run-card.md | Repaired counter/number prose; retained actual scenario coverage as a withdrawn historical procedure. |
| docs/experiments/local-readiness/processing.md | Repaired reference sentence and versions; plan remains historical. |
| docs/experiments/local-readiness/invocation-assessment.md | Repaired the oracle sentence and added current-disposition context. |
| docs/experiments/local-readiness/release.md | Repaired version/count prose; preserved numeric/hash tables and disclosed documentation-versus-build-pin divergence. |
| docs/experiments/local-readiness/validation.md | Repaired prose counts/versions and historical tense/status; no qualification rerun. |
| docs/experiments/local-readiness/review.md | Repaired prose and superseded current readiness; retained previous engineering accounting and review locators as history. |
| docs/experiments/local-readiness/independent-review.md | Audited the returned prose; preserved it verbatim and added only a dated supersession wrapper. |

The new scientific assessment, this audit and the independent reassessment record
also receive the final contextual/link/whitespace pass. Their conclusions concern
this candidate and actual first card; no universal impossibility claim is made.

## Ambiguities and explicit interpretation corrections

- `Int2`, `u32`, `XMM2`, `R8`, `SHA256`, `SOURCE_VISIT`, field names, numeric RVAs,
  `ProcGen+40`, exact paths, filenames and machine schema strings are legitimate
  technical notation. They were not split or renamed. Standalone 070/060 version
  shorthand in authored prose was expanded where needed; path components and
  original returned quotations retain their exact spelling.
- H1's original wording overstated what no callback could imply: no child can
  also mean an empty map traversal, not just a skipped scan. The original hypothesis
  is retained; the new assessment and contract wrapper explicitly qualify the
  interpretation. This is a flagged scientific-design correction, not a silent
  rewrite of native findings or historical evidence.
- The release prose previously called a reviewed source revision "approved".
  It now says reviewed and never user-approved, matching the user's explicit
  correction. This is an authorization-status correction, not a hash change.
- A README repaired here is listed in the old build's source manifest. That old
  manifest/README snapshot is preserved; it is not relabelled as a pin of the
  corrected tree. No source pin was updated to bypass the mismatch, and no rebuild
  is requested under this NO-GO disposition.
- Two local documentation-helper attempts failed before writing status changes:
  a default Windows text encoding failed to read UTF-8, and a shell-quoted helper
  correction was malformed. Running the helper with Python's UTF-8 mode succeeded.
  These were documentation-tool failures, not observer/test failures; original
  evidence and candidate artifacts were unaffected.

The independent reviewer found three residual prose defects after the first
manual pass: `adapter080` in the run-card narrative, the contract wrapper's
awkward double negative, and `section7` in the old review's authored preamble.
They were corrected to the exact plan literal `adapter: "080"`, a sentence
about the absence of a callback, and `section 7`, respectively. The last edit is
outside the verbatim returned review, which remains byte-for-byte unchanged.
These misses are preserved as review rework, not erased by the final pass.

No unresolved prose ambiguity remains identified in the audited task-added
surface after those corrections. This excludes untouched committed prose,
supplied briefs and verbatim historical quotations. No sweeping formatting or
numeric/scientific data rewrite was made.

## Validation and review exports

The final local review manifest records the exact correction-only and complete
path lists, source hashes, link/UTF-8/whitespace checks, forward/reverse exact-byte
patch reconstruction, unchanged HEAD/index and immutable-input checks. The
correction-only patch is relative to the pre-correction working tree; the complete
patch is relative to HEAD and includes the earlier uncommitted implementation and
both unchanged supplied briefs. No staging is used to create either patch.

Output namespace: `.local-work/local-readiness-reassessment/`; patches use
`.local-work/diffs/local-readiness-reassessment-<snapshot>-{task-only,complete}.diff`.
Earlier `.local-work/local-readiness/` packages/diffs/builds remain untouched.
Raw evidence, proprietary content, binaries and private receipts are excluded
from patch payloads and identified separately in the exclusions/check manifest.

Focused runtime/decoder tests were not rerun because no implementation or schema
bytes changed. Historic passing tests support engineering history only. The
scientific decision stands on observability, existing evidence and actual card
coverage, not on test counts.

Coherent suggested commit subject for the correction/disposition:
`docs(research): reject 0.8.0 live proposal and repair task prose`.
It is not authorization to stage or commit either the correction or the larger
uncommitted implementation, and it does not authorize live deployment.
