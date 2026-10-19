# S1 capacity completion and review package

[Original brief](../../implementation-briefs/CODEX_BRIEF_SOR_S1_capacity_inventory_state_completion.md),
[frozen contract](capacity-contract.md), [report](capacity-report.md),
[native](capacity-native.md), [saved calculations](capacity-saves.md),
[sources](capacity-sources.csv), [instrument documentation](../../../research/s1-storage/README.md).
SOR-EXP-0042 / SOR-EV-0050 continuation. Implementer accounting below is not approval.

| Mandatory criterion | Assessment | Evidence / limits |
|---|---|---|
| 1. Answer-first scoped report | PASS | report distinguishes STRONG model, actual saved facts and conditional/current-live limits |
| 2. Verified native arithmetic | PASS scoped | native derivation; effective CarryWeight, MISC mass, positive counts, float/cache/invalidation, derived full; exceptional inputs excluded |
| 3. Actual insertion semantics | PASS scoped | c01/c02/c07/c16–c22; local descriptor through source subtraction and destination add; production/generic differs; manual captured predicate remains bounded |
| 4. Actual representative saved calculations | PASS conditional ordinary model | calculations03.json; nine examples, 113 physical rereads, mixed warehouse, empty controls, exact fallback-boundary stores/cargo/water; actual effective live/historical full state NOT TESTED |
| 5. Runtime/save matrix and S2 handoff | PASS | report separates persisted, definition, effective/cache values and minimum observations/deltas |
| 6. History, scope, permissions | PASS | accepted S1 documents retained; appended registers/state/backlog/credits; no new policy decision, promotion or authority |
| 7. Evidence, integrity, review | Receipt-controlled | verification01.json: 102 checks, four regression suites, protected pre/post; actual independent decision below |
| 8. Complete review package | Receipt-controlled | package-review03.json: corrected task-only/complete patches, untracked brief, status/exclusions, exact forward/reverse reconstruction and strengthened text audit |

## Actual checks, failures and limits

`.local-work/s1-capacity/baseline.json` freshly pins HEAD/index, supplied brief,
executable/ESM, stopped database and four originals. verification01.json records
102 successful checks and four existing regression suites (inventory framing,
outpost framing, streaming and extractor-resource reader). Actual outputs are
retained; these establish reader integrity, not live behavior. Independent
expected binary32 bits and decimal arithmetic check boundaries/mixed weight.
Disk guards on C: and D: retain the 40,000,000,000-byte threshold.

c05/c06 failed on invalid range-window syntax after earlier complete selected
exports; c17/c19 failed on guessed non-instruction window centers. Full logs and
partial exports remain hashed locally. Corrected checked windows are in
c07/c09/c20/c21/c22. NO_FUNCTION_AT guesses do not establish absence. Process exit0
does not override script errors. No missing later selector is claimed.

An initial interpretation of generic add's return as rejected stock was
contradicted by the actual mutation count and corrected before submission.
Health/weight getter identities and production call location were likewise
checked rather than trusted from guesses. The final report cites actual spans.
No original evidence or accepted S1 conclusion was rewritten to hide failures.

Scientific result: positive bounded native/save ordinary model, proposed STRONG;
conditional exact-boundary and over-nominal saved witnesses, no live transfer
trial. Engineering: disposable evidence readers/calculations, no production tool.
Target survival/live cleanup: not applicable, no game accessed. Authorizations:
no deviation or new third-party incorporation identified. Publication: authored
REVIEW-REQUIRED, raw/private/native data LOCAL-ONLY. No decisions update is needed:
execution of the existing brief creates no new policy or experiment approval.

## Snapshot and independent decision

`.local-work/s1-capacity/package-review03.json` indexes the corrected patches under
`.local-work/diffs/`, changed/untracked text path hashes, unchanged HEAD/index,
status, exclusions, whitespace/link/encoding audits and exact forward/reverse
reconstruction in disposable .local-work/review-patches trees. Complete includes the supplied brief
unchanged; task-only excludes it. Ignored raw/native evidence, binaries, saves,
databases and disposable trees are disclosed exclusions; no raw bytes enter patches.

The actual independent reviewer response is retained verbatim in
`.local-work/s1-capacity/independent-review-encoding-final.md`, bound to that manifest and
working snapshot. Until it exists and says ACCEPT, accepted completion is not
claimed. Any changed reviewed content requires regenerated artifacts and re-review.
The final chat reports the actual disposition. ACCEPT supplies no maintainer
integration, publication, live or Git authority.

Suggested Conventional Commit subject:
`docs(storage): establish capacity and inventory receiving semantics`

No staging, commit, push, live experiment, new save or S2 execution follows.

## Encoding correction — 2026-10-17

User correction adopted in this chat: repair the two affected Markdown files,
check all newly authored text, strengthen text validation, regenerate final diffs
and obtain independent acceptance; no further native investigation or save-file
analysis. This is a text/packaging correction under the existing brief, not a
scientific reclassification or new experiment.

Fifteen corrupted symbols were repaired: two minus signs in capacity-report.md;
three minus signs and ten multiplication signs in capacity-saves.md. A local
authoring helper used the Windows default code page to read UTF-8 before writing
UTF-8 again; its reads now specify UTF-8 explicitly. Earlier exports, acceptance
and the original verification01.json remain preserved as historical snapshots.
That scientific verification is not rerun or represented as checking revised
validator code. Scientific source/calculation receipts are unchanged.

The new shared text validator is called by the review exporter and by
verify_capacity.py's text-only mode. It rejects likely UTF-8 bytes misdecoded
as Windows-1252/Latin-1, replacement characters, C1 controls and BOMs. It scans
entire new authored files and added/changed text in tracked files; strict UTF-8
decoding covers their current bytes. Two whole-file scan hits in CREDITS.md:99
and docs/SOURCES.md:182 are identical in HEAD and are excluded legacy text,
not new corruption or silent fixes to unrelated history.

Text-only regressions exercise both observed sequences, other misdecoded symbols,
malformed UTF-8, legitimate Unicode and controls. The initial C1-control test
failed because splitlines consumed U+0085 before checking it; splitting only at
LF corrected detection and the test now passes. The same LF-only logic now covers
tracked added-line extraction; two additional tests exercise corrupted tracked
additions and unchanged legacy exclusion. All seven text-only tests pass.
Actual outputs and original corruption detection are retained in
encoding-checks02.json; textvalidation02.json
records the final authored-text scan. No native exports, save reads/analysis,
game access, original-input mutation or external actions were performed for this
correction. The new snapshot's actual independent disposition is kept separately
from the original independent-review-final.md.
