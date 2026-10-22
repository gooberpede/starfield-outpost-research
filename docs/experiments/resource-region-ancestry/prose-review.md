# Uncommitted documentation prose review

2026-10-22 Australia/Sydney. This is an editorial correction requested by the
maintainer after the [Phase B result](phase-b.md). It changes no research claim,
measurement, acceptance criterion, permission or live-execution authority.

The request was to examine malformed prose case by case, preserve valid
identifiers such as `Save52` and `binary32`, obtain independent review and supply
a complete diff of all uncommitted files. No regex or blanket conversion rule
was used to find or change prose.

## Coverage and decisions

The complete new `phase-b.md` and `phase-b-review.md` documents and the complete
small modified `report.md` and `review.md` documents were read. In the large
research-state, source and experiment indexes, review covered the uncommitted
additions. Their older committed entries were not silently included in this
editorial task; some retain older spacing defects. The source CSV and comparison
Python file were inspected for preservation and remain byte-identical to the
task's starting snapshot. Raw receipts and verbatim reviewer returns were not
rewritten.

| Document | Case-specific corrections |
|---|---|
| [Phase B result](phase-b.md) | Separate ordinary count/ordinal/process/version labels from values; repair punctuation spacing and table prose; spell out capture references; separate measurements from units; show the actual `ACK 967 STOP` command; use “Stage 2” for the prose stage named that way in the brief. |
| [Phase B review](phase-b-review.md) | Repair “all 967”, “fresh 32-case”, “9-file” and “all 1,938”, with spacing around the receipt/frame separator. |
| [Phase A review](review.md) | Repair the final receipt count and the file/source/receipt count list. Historical findings and review scope remain unchanged. |
| [Research state](../../RESEARCH_STATE.md) | Separate the sentence ending “match.” from the following count of 967. |
| [Experiment index](../README.md) | Separate “pilot,” from the following count of 967. |

`Save52`, `binary32`, `P3`, `C1D`, `RG2-C1E`, `IRES0057ce`, `IRES0057cb`,
`Starfield.esm:0057d4`, source keys, timestamps, hexadecimal values, filenames,
paths, hashes, schema fields and the quoted human approval retain their values.
Formatting the source keys as code does not alter their contents. “IL capture
299” and “Cu capture 325” make receipt references explicit rather than creating
new resource identifiers. Counts, point ordering, coordinates and scientific
uncertainty are unchanged.

## Independent challenge and checks

A fresh-context, read-only independent reviewer examined the original prose and
then the corrections. It supplied an explicit list of individual defects,
confirmed the two additional index errors, checked ambiguous capture and source
labels, and used the brief to distinguish the prose stage from identifiers.
It recommended keeping source keys and IRES identifiers exact and disclosing the
large-index coverage limit. The implementer adopted those findings.

The reviewer challenged whether “source0:…” was a literal identifier. Inspection
of the unchanged `comparison-attempt01-v2.json` established that its actual source
keys begin with `0:`; “source” is the prose label. The reviewer withdrew that
objection, and the corrected label plus exact backticked key was retained.
A proposed expansion of “39 definitions/configuration” was reverted to the
original wording with spacing only, avoiding any reinterpretation of that count.

The final independent disposition is retained verbatim at
`.local-work/prose-spacing-review/final-independent-review.txt`. That return,
with its exact snapshot hashes, governs final acceptance; this report does not
substitute self-review for the critic's decision.

Checks include a case-by-case second read, comparison against exact before bytes,
UTF-8/LF and whitespace checks, local-link validation, preservation of the CSV
and Python file, and unchanged HEAD/index. No game or experimental tool was run.
No scientific evidence or frozen prediction was modified. Historical Phase A/B
review patches and raw reviewer returns remain intact; their acceptance covers
their original snapshots, not these later editorial changes.

## Complete review package

The starting tree already contained nine uncommitted Phase B files. The complete
patch includes all of them in their final state plus this new review report;
the task-only patch isolates these editorial corrections and report against the
exact starting snapshot. Neither patch is constructed by staging files.

Final artifacts:

- `.local-work/diffs/rg2c1e-prose-final02-complete.diff`
- `.local-work/diffs/rg2c1e-prose-final02-task-only.diff`
- `.local-work/review-deliveries/rg2c1e-prose-final02.json`
- `.local-work/review-deliveries/rg2c1e-prose-final02-status.txt`

The manifest records file hashes, prior-work/task scope, exclusions and byte-exact
forward/reverse applicability checks against standalone scratch trees and the
actual working tree. Ignored raw/native/save/binary/private evidence and local
review working files remain excluded. No staging, commit, push, publication or
cleanup of existing work was performed.
