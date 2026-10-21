# Corrections, retained exceptions and hash scope

2026-10-21. [Occurrence ledger](corrections.csv), [candidate dispositions](candidate-dispositions.csv),
[initial corpus](corpus.csv), [before/after documentation hashes](documentation-hashes.csv).
Lines in the correction ledger are those at each edit step; additions have their
own locations below. Baseline corpus/disposition line numbers refer to the B2
starting tree, rather than RR1's now-shifted research-state lines.

The ledger has **469 literal edit occurrences**: 354 prose, 103 encoding,
11 notation and one Markdown pipe repair. A full-line contextual replacement is
one edit operation even if it separates several prose labels. These are operation
counts, not distinct scientific defects or unique token counts. Later prose
review corrections, if required, are recorded separately and never erase this pass.

## Earlier reviewer failures retrieved before scanning

| Retained source / local primary review | Positive defect / resolution | Protected negative |
|---|---|---|
| [Spacing review](../documentation-spacing-cleanup.md#independent-review-rework-and-correction) | Broad spacing initially damaged technical tokens despite equal non-whitespace characters. Reviewer REWORK; 93 protected/false-positive occurrences restored. | KERNEL32, Wait3D, Is3DLoaded, 2a, +a08 and native offset/symbol families. |
| [Local-readiness reassessment](../../experiments/local-readiness/reassessment-review.md) and [correction audit](../../experiments/local-readiness/prose-correction-audit.md) | Residual adapter080, section7 and double negative corrected; earlier returned review preserved. | Plan literal `adapter: "080"`, exact source/build pins and historical Before specimens. |
| [L3 prose review](../../experiments/spatial-placement/prose-review.md); `.local-work/l3-prose-spacing/independent-review01.md` | ACCEPT for its original 14-file correction; radius/version/prose boundaries corrected, index/mask separated. | Save33/35, KREET OUTPOST1, static addresses and mask `0x01000000`. |
| [SD1 review](../../experiments/containers-displays/review.md); `.local-work/sd1-containers/independent-review01.md` | REWORK examples close5861601, contains28, known26, low3, bounded4b0 and bounded255-original; CP1252 read corrupted valid UTF-8. Explicit encoding and contextual repair corrected the pass. | Exact native call addresses and original evidence; scientific wardrobe/construction rework was separate from typography. |
| [BM1 review](../../experiments/construction-variants/review.md); `.local-work/construction-variants/independent-review01.md` | REWORK examples all87, csv333, reports72978, cover19; explicit hexadecimal opcode versus decimal condition index required. Checker-coverage overclaim corrected separately. | `0x1230`, `0x230`, decimal index 560, evidence/source CSV identities and actual prior returns. |
| [RR1 taxonomy](../publication-readiness-rr1/prose-and-notation.md) and [ledger](../publication-readiness-rr1/prose-candidates.csv) | Recover fused prose, expanded encoding sentinels and a single unescaped expression pipe. | Inline identifiers, source-locator/type/slot CSV encodings and historical defect quotations. |

Before the fresh loop, `.local-work/b2/fixtures.json` validated 37 cases
(13 positive, 24 negative), including Save52contains, recordat0x88, actual
reviewer-style fusions and a damaged multiplication symbol; negatives include
Save52, kernel32.dll, EditorID OutpostRobotModelS01, image base, +0x88,
binary32 and short-byte labels. The source and exact regexes are retained in
`.local-work/b2/audit.py`; they detect candidates and never rewrite prose.
The expanded character-run inspection additionally recognized `Ã—` as corrupted
multiplication and `Â²` as corrupted superscript. Explicit fixed literal edits,
reviewed per file/line, were applied; no corpus-wide regex rewrite ran.

## Actual fixes and retained exceptions

- Source/credit headings and separators now decode their intended dash/multiply
  characters. Position math restores multiplication/squares without changing
  operands/order. The `.25` spacing repair was checked against the retained
  project diagnostic at `save-analysis/scripts/position_quantizer_diagnostic.py:39`.
- L2 now says mask `0x10` (index 4), event types 4/5 and combined mask `0x1f`.
  Activated-grid's human-readable CSV description now says mask `0x08`, checked
  at `14096bc7a` in `.local-work/recon/activated-grid-05.tsv:1848`.
  P1's current reference bit index 10 remains an index; it is not L2's mask.
- The malformed static-exhaustion row now escapes the expression's pipe; its
  field/value and historical interpretation remain unchanged.
- S1/Save52 fused record-count prose now separates aliases from 20705/205557,
  checked in `.local-work/workshop-population-rework/typed-full03/summary.json`.
- Historical operational cards, supplied briefs, prior literal Before strings,
  primary logs and pin/source tables remain verbatim. The damaged 020 and 0.5.0
  card text has an [external annotation](evidence-dependencies.md#historical-damaged-operational-notation-retained-literally).
  Schema/version strings in those historical cards remain inputs, not new advice.
- Technical shorthand such as actor4C denotes a saved actor extra channel;
  type4b, mask00, slot3 and all-hex offset declarations are not automatically
  English spacing errors or decimal numbers. The occurrence register retains
  those domains. A detector match is not evidence of a scientific contradiction.

## Additions outside the correction ledger

The roadmap and documentation/audit/brief indexes link the B2 package. The
evidence standard links the reader notation convention. Two primary reports
(mature validation and outpost biomes) gain dated reader-context wrappers; their
original scientific text stays literal apart from explicitly ledgered corrections.
These seven files have an addition classification in documentation-hashes.csv.
New B2 files are original explanations, metadata and bounded verification source.

All 60 ledger-edited files are mechanically reconstructed from baseline text by
replaying the exact ordered occurrences. Decimal digit strings are unchanged in
464 operations; the five exceptions add explicit hex prefixes or the proven bit
index, with exact original/corrected text retained in preservation.json. Protected
identifier families receive a separate before/after inventory; whitespace equality
alone is not used as proof. Scientific tests are not rerun for editorial changes.

Historical hashes are **not repinned** to corrected explanations. All source-pin
CSVs and tracked exact evidence are unchanged; the native-map description CSV is
the sole edited existing CSV. Its earlier pin continues to identify the earlier
bytes. The new documentation hash table identifies this B2 revision independently.
Checksums establish integrity, not semantic truth or rights clearance.

## Review01 rework and residual controls

The independent reviewer returned REWORK on AC2/AC3/AC7/AC8. Four genuine
prose boundaries had been retained as shorthand: `subscribed at145916518 with`,
`Both-drive40GB guards`, `check actor3D` and `Ordinary actor3D absence`.
All four are now ledgered whitespace-only repairs; an additional contextual
check separates `ExtraOwnership type1F` without changing its established hex
type. Five explicit residual controls are in check.py and the local regression
receipt. The new total is 469 operations across 60 replayed files; the initial
464-operation snapshot and its failed disposition remain retained locally.

The initial fixture prose incorrectly reported 38/25 instead of the actual
37 cases / 24 negatives; that accounting is corrected. The original 37-case
receipt and expectations are unchanged. Residual controls are additional checks,
not retrospectively added to the pre-scan fixture set.

The revised candidate register separates `context_edited` from occurrence
disposition. An edited context can still contain a retained literal; it is not
proof every match was repaired. Each candidate is transformed through the ordered
literal edit ledger before deciding whether its original token remains. Remaining
technical shorthand/source-locator and historical-card families retain their
declared domain and rationale. This remains bounded contextual classification,
not an assertion that every possible prose error has been found.
