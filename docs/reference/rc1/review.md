# RC1: frozen contract, checks and independent review

2026-10-20, Australia/Sydney. [Answer](report.md), [ledger](sources.md).
Original supplied brief hash is recorded in sources.md. The unchanged AC1–AC8
contract is reproduced below. No amendments. No staging, commit or push.

Criterion | Implementer assessment before independent review | Primary evidence and limit
--- | --- | ---
AC1 | PASS | sources.md and local baseline.json pin HEAD/index, all starting files and three installed sources. Ending checks must match; no save/database/target writes authorized.
AC2 | PASS | gap-reconciliation.md has A01–A60 exactly once, exact original question labels/dispositions, primary/review citations and stable linked children. Historical source files untouched.
AC3 | PASS | Report and updated rows A02/A09/A10/A12–A15/A23/A40/A41/A46/A48/A50 separate later positive results and remaining qualifications; monitoring/engineering dependencies are not false research failures.
AC4 | PASS | capability-access.md C01–C31 span all requested families and actions, with separate definition/Papyrus/configuration status, named inputs/consumers, bounded absence and no prescribed technology.
AC5 | PASS | papyrus-interfaces.md P01–P22, member hashes and local three-check receipts preserve exact signatures, qualifiers, corrected locators and declaration versus registration/consumer distinctions. No calls executed.
AC6 | PASS | Report/publication flags and ledger retain source classifications, counterexamples, release gates and rights limits. No claim that native implementation mandates a native extension.
AC7 | PASS | check02 validates UTF-8/LF/whitespace/table/link/ID/source checks and exact reconstruction. Link existence does not certify semantics or complete historical source accessibility.
AC8 | NOT TESTED at initial submission | Independent verdict pending; complete/task-only exact forward/reverse checks, manifests and integrity checks must pass. This initial pending state is retained in review01 package; never self-accepted.

## Validation and package procedure

Run from repository root using the explicit Python executable in sources.md:
`.local-work/rc1/package.py --run <unique-name>`. This original task-specific
adaptation of the existing coverage packaging method has documented reads/writes
and pinned method provenance. It checks all baseline file hashes, HEAD/index,
three installed input hashes, two-drive space guards, complete 60-ID equality,
child IDs, table shape, all new-document relative links and UTF-8/no-BOM/LF/trailing
whitespace. Selected source hashes are inventoried. It creates exact new-file
Git-style diffs without staging, independently reconstructs bytes forward/reverse
in standalone trees, checks actual-tree reverse applicability without applying,
and compares inventories to actual Git tracked/untracked text status.

Local manifests: `.local-work/rc1/package-<run>.json` and status-<run>.txt.
Patches: `.local-work/diffs/rc1-<run>-complete.diff` and
`.local-work/diffs/rc1-<run>-task-only.diff`. Complete includes the unchanged
supplied untracked brief; task-only includes only the new audit directory.
Exclusions are explicit in the manifest: ignored local receipts/helpers/scratch,
all proprietary/raw game/script/native/map/save/database inputs and pre-existing
local bulk evidence. No binary patches or raw evidence are included.

Actual runs, failures/corrections and reviewer decisions are appended after they
occur. Repeated package runs use exclusive names, retaining earlier results.
Independent reviewer instruction: [repository procedure](../../reviewers/research-completion-reviewer.md).
Reviewer checks original contract and primary evidence, not just these assessments.
No review verdict supplies maintainer integration or publication authorization.

## Executed validation and preserved corrections

check01 failed the whitespace assertion before package creation: the verbatim
frozen contract contains original Markdown two-space line breaks. The correction
checks authored prose for trailing whitespace and separately asserts exact full
contract equality to the brief; it preserves unchanged wording/Markdown after CRLF-to-LF newline normalization rather
than editing the acceptance criteria. Local failure01.txt records the actual
failure and correction. No scientific check failed or input changed.

check02 passed: 1,546 starting repository files unchanged, three installed inputs
unchanged, 60 exact original IDs/question labels/historical dispositions, eight
unique child gaps, 31 capability rows, 284 relative-link occurrences and 177 cited
or guidance source hashes. Editorial counts: 33 RESOLVED, six CONSOLIDATE, three
TARGETED RESEARCH CANDIDATE, 16 DEFERRED and two PUBLICATION BLOCKER. These are
proposal counts, not scientific completion percentages. Table shape, strict
UTF-8/no-BOM/LF, authored whitespace, selected encoding sentinels and Git diff
whitespace checks passed. Manual prose/semantic review complements mechanical
checks; lint cannot prove no possible malformed word or unsupported inference.

Both patches reconstruct exact current bytes forward and baseline bytes/absence
in reverse in standalone trees. Actual-tree reverse checks and inventory equality
passed: eight task files, nine complete files including the unchanged brief.
HEAD/index unchanged. check02 package is a preserved pre-review snapshot; a fresh
review01 package includes this validation record before independent review.
Raw/header/member integrity is separate from correctness of semantic synthesis.

## Independent review01 and in-scope corrections

Review01 returned **REWORK** for manifest package-review01.json, SHA256
`40f24c9aaf611098e67829e7c09889ac2b9b71d9d0435883a6b933d386f69ed4`.
AC1/AC2/AC3/AC5/AC6 PASS; AC4/AC7/AC8 FAIL. The actual return is retained
verbatim locally as independent-review01.md. Reviewer independently tested the
60-ID comparison, baseline/current/source/installed hashes, eight archive member
hashes and asserted declaration lines, 284 links, normalized contract equality,
patch inventories/payload reconstruction and actual-tree reverse applicability.
It inspected standalone apply and historical experimental receipts without
rerunning those experiments. Its initial checker syntax/decoding/encoding-name
errors were corrected; no product failure or source mutation followed.

Corrections preserve the unchanged contract: C01/C03 and analogous cells now
keep definition relationships distinct from game-configuration operands. C09 names
actual INI/GMST/AV budget operands; other positive configuration cells name or
cross-reference their concrete inputs. C20 adds the existing redistribution call;
C21 adds the cargo target-menu invocation and keeps pairing lifecycle separate.
P18–P22 and local papyrus-check03.json confirm exact additional movement/menu,
power/read/event declarations on the same ObjectReference member hash. Additional
declarations remain explicitly static/unexecuted; full native semantics are not
inferred from names or comments. Contract checks preserve normalized text, not
the supplied brief's original CRLF byte sequence. The first exact-text correction
helper assertion failed before writes; failure02.txt preserves that corrected
literal mismatch. No scientific criteria or historical finding changed.

The corrected package freezes these corrections for independent re-review. This
paragraph records no future verdict. Final acceptance must still be supplied by
the independent reviewer; no integration or publication authority follows.

## Separate outcomes and untested work

Review02 returned **REWORK** for package-review03.json, SHA256
`276356b41c774c5b2603f6ba37d53f249f360a75f58cf00f9f58eb8e7a8c9c31`:
AC1–AC6 PASS, AC7/AC8 FAIL solely because a blank line before P18 broke the
Papyrus table. Actual return: local independent-review02.md. The new contiguity
check deliberately reproduced that defect as PAPYRUS_TABLE_NOT_CONTIGUOUS
(tablecheck01; failure03.txt), then the blank line was removed. A first patch
also included an unrelated heading context and failed atomically before writes;
the corrected narrow patch succeeded. The refreshed package checks P01–P22 as
one contiguous table, not just row delimiters. No signature or semantic finding
changed. Reviewer repeated baseline/current/source/protected hashes, new
declarations, links, normalized contract, patch inventories/reconstruction and
actual-tree reverse checks; isolated apply/history receipts were inspected.
Final independent acceptance remains pending for this corrected snapshot.

Scientific result: bounded reconciliation and declaration audit, not new native
research or reclassification. Engineering result: documentation/patch integrity
only; no implemented gameplay/tool/monitor capability. Target survival is NOT
APPLICABLE; no target process operated. NOT TESTED: runtime calls/events, current
loaded states, realized production, new definitions, full API census, save reload,
winning overrides, general integration safety, release privacy/history/rights
clearance. Authority: no live/configuration/save/database/Git integration or
external disclosure performed. No additional permission needed for completed
in-scope documentation; later work remains separately gated.

Suggested commit, after maintainer critical review:
`docs(audit): reconcile outpost gaps and capability access`.

## Final independent acceptance and delivery

Independent review03 returned **ACCEPT**, AC1–AC8 all PASS, for
package-review04.json, SHA256
`ed3244d1fd49527c69c4e7c417dad57449ad38f030d63e4ad9843499350e6a01`.
The actual return is local independent-review03.md. Prior REWORK responses,
failed checks and corrected snapshots remain intact. The original table above
records pre-review implementer assessments; the current mandatory outcome is:

Criterion | Final result | Primary evidence / coverage
--- | --- | ---
AC1 | PASS | baseline.json, sources.md, package integrity/status receipts; 1,546 starting files and three inspected installed inputs unchanged, HEAD/index preserved.
AC2 | PASS | gap-reconciliation.md, original coverage.md and exact 60-ID/label/history comparison; eight distinct child gaps.
AC3 | PASS | Updated crosswalk/report and five cited primary packages; qualified ordinary/nominal answers and deferred engineering/realization questions separated.
AC4 | PASS | capability-access.md C01–C31, separate route statuses, named configuration operands and accepted concrete consumers.
AC5 | PASS | papyrus-interfaces.md P01–P22, member hashes and three local declaration receipts; signatures independently checked, no runtime invocation claimed.
AC6 | PASS | sources.md/report boundaries and publication flags; no source reclassification, prescription, legacy edit or expanded permission.
AC7 | PASS | package checks and independent P01–P22 table continuity, 284 links, UTF-8/LF, whitespace and normalized original-contract equality.
AC8 | PASS | independent-review03.md ACCEPT; preserved failures/rework, inventories, exact reconstruction receipts and independently checked patch payloads/reverse applicability.

The reviewer independently rehashed baseline/current/installed inputs and checked
snapshot/HEAD/index stability. Prior passes additionally checked all 177 source
records and declaration lines. It checked patch payloads/inventories and actual
reverse applicability. Standalone forward/reverse application and original
scientific executions were inspected as receipts, not independently rerun.
Current runtime values, event completeness, arbitrary extension safety and release
clearance remain untested/separately gated. No new scientific classification.

Final administrative update records this actual verdict only. Final artifacts:
`.local-work/rc1/package-final01.json`, status-final01.txt and
`.local-work/diffs/rc1-final01-complete.diff` / rc1-final01-task-only.diff.
The manifest supplies exact hashes, all eight task files, the separately included
supplied brief, explicit exclusions and exact forward/reverse reconstruction.
Final administrative snapshot confirmation is retained separately as local
independent-review04.md, avoiding a self-referential document hash. This paragraph
does not assert that a future confirmation has already occurred.

Maintainer critical review is still required. No staging, commit, push,
publication or live-operation authority follows from independent ACCEPT.

## Original frozen contract (verbatim)

## 7. Frozen compact completion contract — AC1–AC8

**Task type:** Offline documentation and evidence-reconciliation research.
**Question/deliverable:** What gaps remain after accepted research, and what concrete definition/Papyrus/game-configuration access routes do our existing findings establish?
**Scope/bounds:** Existing repository research and provenance, limited targeted read-only interface/source verification, new audit documents and narrow index references; no live work, substantial new native investigation, protected-source edits, publication changes or Git integration.

**Mandatory acceptance:**

- **AC1 — Baseline and protection:** Actual initial provenance/status/permissions/protected-input state recorded; no protected source or unexpected workspace modifications.
- **AC2 — Complete 60-question reconciliation:** Every baseline question present exactly once in the crosswalk (with separately linked child gaps if needed), historical and proposed dispositions distinct, and primary citations supporting changes.
- **AC3 — Post-audit findings integrated:** Coordinate sufficiency, B1, BM1, BM2 and LO1 incorporated accurately; realized-production, geography/biome and active-membership boundaries stated without false reopening/closure.
- **AC4 — Concrete access-route taxonomy:** Representative capability-level matrix across subsystem families; three overlapping avenues distinguished; every asserted route tied to actual records, calls, settings or definitions; evidence classification and absence language correct.
- **AC5 — Papyrus accuracy:** Targeted API/event/property entries grounded in exact available declarations/registrations or marked unverified; native-only calls not mislabeled as Papyrus; `GetCurrentLocation()` semantics correctly separated from coordinates.
- **AC6 — Editorial boundaries and publication flags:** No SFSE/native-extension necessity claims or engineering implementation prescriptions; historical evidence untouched; publication and documentation issues distinguished from scientific gaps; clear reader guidance.
- **AC7 — Durable quality:** Answer-first report and navigable crosswalk/matrix, checked relative links, precise provenance and coverage, UTF-8/prose hygiene, documented negative and incomplete checks.
- **AC8 — Verification/review/delivery:** Reproducible validation with retained failures/corrections; independent reviewer ACCEPT against **these eight unchanged criteria** (or properly evidenced REWORK/ESCALATE when unfinished); verified complete/task-only reversible patches, manifest and integrity/status receipts, no staging/commit/push.

**Optional:** Provide an unimplemented suggestion for a public-facing access-capability index or a small concise FAQ; do not let optional polish delay closure.

**Negative-result closure:** A properly bounded absence of an observed interface is a valid documented result when the inspected surface and positive controls are reported. Never require proof that all unknown interfaces are impossible; never assert that an unexamined alternate avenue does not exist.

**Continuation authority:** Diagnose/correct/retest in-scope documentation, classification and verification failures under this assignment; reviewer REWORK does not need a new brief. Preserve original criteria and failure history.

**Exit/escalation:** Stop prohibited operations, any integrity-risking write or work requiring material new native/live investigation; retain the checkpoint and request only the minimum authorization or missing essential source. Do not relabel unfinished mandatory deliverables PASS.

**Disposition/reporting:** Return AC1–AC8 PASS/FAIL/NOT TESTED with primary evidence paths, scientific interpretation separately from tooling/safety/reviewer outcomes, explicit gaps and proposed dispositions, independent reviewer reference, full verified patch package and suggested commit. Maintainer must critically review before integration.
