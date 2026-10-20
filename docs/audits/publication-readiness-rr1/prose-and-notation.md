# Prose, encoding and technical notation

**Confirmed defects remain; a passing UTF-8 decoder is insufficient.** RR1
performs discovery and classification only. It does not edit any inspected
document or equate typography with scientific invalidity.

## Earlier reviews retrieved before scanning

| Source | Defect lesson and protected counterexample |
|---|---|
| [Spacing cleanup review](../documentation-spacing-cleanup.md), original failure/rework section | Missing spaces affected counts and observer versions; a prior broad correction incorrectly split KERNEL32, Wait3D and section 2a. Non-whitespace equality did not protect identities. |
| [Independent reassessment](../../experiments/local-readiness/reassessment-review.md), actual returned criterion table | Independent reviewer returned fused adapter and section labels plus a double negative. The preserved prose audit quotes those original defects deliberately. |
| [Robot spacing review](../../experiments/robots/prose-spacing-review.md) | Model A03 prose differs from exact OutpostRobotModelS01 EditorID; ExtraBC, Save52 and binary32 remain valid. Local actual reviewer return `.local-work/r1-prose-spacing/independent-review01.md` was also read. |
| [L3 prose review](../../experiments/spatial-placement/prose-review.md) | Radius 150, retail version and saved-ID labels need readable boundaries. Bit 24 and mask 0x01000000 differ. Local independent return confirms identifiers and historical quoted text must survive. |
| [LO1 methods failures](../../experiments/locations-outpost/methods.md#preserved-failures-and-corrections) | Reading UTF-8 with Windows default encoding corrupted a copied contract; the corrected derivative preserved the original. Successful decoding does not prove the earlier text was never corrupted. |

The fixture was validated before the corpus loop, in
`.local-work/rr1/fixture-before-scan.json`. Twenty-one cases passed: seven
positive controls (fused sample/predicate, record/hex offset, threshold, section,
observer version, HEAD/hash and matches/count) and fourteen negative controls
(Save52, kernel32.dll, KERNEL32, Wait3D, Is3DLoaded, 2a, +a08, +0x88,
0x140000000, FNAM, ExtraBC, OutpostRobotModelS01, binary32 and radius 150).
These are test strings, not findings about every occurrence of those families.

## Method, coverage and candidate accounting

The initial tracked corpus is 1,040 MD/CSV/TSV/TXT files, 775 Markdown and
104,755 lines. Discovery skips fenced blocks and labels inline-literal matches
for contextual review. Machine-readable CSV identities remain candidates for
classification, never automatic edits. Exact regexes, fixture outcomes and
full initial context are in `.local-work/rr1/audit.py`, `fixture.json` and
`prose-candidates.json`; the [durable ledger](prose-candidates.csv) records
decisions and explicit unresolved shorthand. Its counts are match occurrences,
including two overlapping HEAD/hash rule hits, not unique defect counts.
The final 528-row ledger replaces the initial 97 encoding rows with the
122-row expanded set: 117 prose correction candidates, 122 encoding correction
candidates, 124 uncertain notation cases, 37 retained historical/literal cases,
121 retained technical CSV encodings and seven retained technical locators.
Those classifications apply conservative inspected-context/family decisions;
uncertain cases explicitly remain unresolved rather than being called clean.
Independent challenge moved activated-grid native-map.csv line 38's bit8 from
the initial blanket CSV category to uncertain bit notation: it is human-readable
description, not an encoded type/slot column. Other CSV retention is limited to
the inspected type/slot/source-locator families. The original source is untouched.

The first pass returned 503 candidates: 397 count/identifier elisions, two
additional hash-rule hits, six hex-elision hits, one fused sample-tail and
97 encoding sentinels. A broader CP1252/Latin-1 continuation detector then
returned **122 encoding occurrences in six files**. It catches multiplication,
minus and arrow corruption missed by the first narrow sentinels. The expanded
encoding ledger is independent of the original 503-count ledger.

| Expanded encoding file | Occurrences | Adjudication |
|---|---|---|
| CREDITS.md | 22 | Corrupted authored headings/separators; correction candidate, preserve attribution. |
| docs/SOURCES.md | 70 | Corrupted authored source descriptions/headings; correction candidate. |
| docs/experiments/durable-position-resumption.md | 2 | Authored math/text corruption; compare exact algorithm/source before replacement. |
| docs/experiments/position-resumption/algorithm.md | 9 | Authored mathematical operators/notation; preserve numeric semantics. |
| docs/experiments/native-oracle/continuation-020-run-card.md | 16 | Historical authored operational prose/operators; correct with a disclosed derivative/wrapper policy, never reinterpret old authority. |
| docs/experiments/ship-relocation-050/run-card.md | 3 | Historical authored operational notation; same preservation boundary. |

Strict UTF-8 decoding and BOM checks found no failures in the selected tracked
text corpus. That negative coexists with actual mojibake: the damaged character
sequence itself is valid UTF-8. Local `encoding-expanded.json` records exact
line/codepoint locations without publishing corrupted source excerpts here.

Two table-width transition flags identify **one** malformed row:
static-exhaustion `dependency-ledger.md:31` contains an unescaped pipe inside
an expression. The next row simply restores the expected width; it is not a
second table defect. This width scan is not a full Markdown parser.

## Contextual determinations and false-negative challenge

Confirmed reader-facing examples include `docs/PROVENANCE.md:5` HEAD/hash and
matches/count boundaries; crew-skills stacking rank prose; cargo transport
`cycle.md:57-59` adds/count and retains/count; and the workshop-population
validation line 24 sample/count compression. Quoted Before examples in previous
correction reviews, supplied historical briefs, CSV encodings such as `type1:`
and `slot3`, actual filenames and source locators are retained. Ambiguous
`actor4C`, `type4b`, `mask10` and `bit10` require domain-specific treatment,
not a blanket inserted space.

Likely false negatives were inspected deliberately: LO1 `methods.md:15-30`
contains count/hash boundaries outside the initial prefix vocabulary;
`docs/RESEARCH_STATE.md:633` contains compressed Model A03 prose; native-map
`minimum-inputs.md:18-24` contains fused RVA labels. These extend the cleanup
brief's contextual work; zero regex matches cannot certify universal cleanliness.
Original evidence/logs and literal API/filename spellings remain outside
automatic correction. Full source-adjacent CSV was scanned for discovery,
but every cell is not independently semantically reinterpreted.

## Address and identity domains

| Inspected example | Audit determination / proposed convention |
|---|---|
| LO1 methods baseline; native/static ledgers | Preferred image base 0x140000000 and pinned executable identity define static VA; RVA is VA minus that base. Preserve source zeros and hex value; label domain rather than infer from digit length. |
| native-availability minimum-inputs table | RVA labels are explicit but fused with addresses. A readability repair can separate the label without reclassifying as VA or runtime pointer. |
| build-budget ui lines 25/33 | “mask bit10 hex” mixes mask/index vocabulary. The table should state the actual mask (0x10) where supported, and separately any bit index. No assumption that decimal bit index 10 equals that mask. |
| static-exhaustion dependency ledger lines 56–58 and trace notes | Existing correction says older bit2 meant mask 0x02, zero-based bit 1. Preserve that supersession; never reinterpret the old string as mask 0x04. |
| coordinate-sufficiency inputs/evidence/positions | Decoded-stream offsets differ from compressed disk offsets; physical ESM offsets and ABC method numbers are decimal under that report's declaration. No stylistic hex-only conversion is warranted. |
| L3 prose/native descriptor | Reference offset 0xd3, reference-byte mask 0x04 and change-state bit 24/mask 0x01000000 are separate channels. Existing corrected domain declaration is a positive model. |
| crew current assignments | Saved 4C/E2 targets, FormIDs, dynamic runtime IDs and loaded actor pointers are distinct. Explicit saved reciprocal joins do not establish post-load pointer equivalence. |
| coordinate and position reports | Cell geographic address, local XYZ, compensation and lon/lat are different frames/units. Keep conditional transforms and untested vertical/common-frame claims attached to outputs. |

No new semantic inconsistency was established merely because some tables omit
`0x` under an explicit all-hex declaration. EditorIDs, FormIDs, handles, saved
keys and decimal counts need contextual labels, not stylistic uniformity at
the expense of historical meaning. Proposed batch B2 must preserve identifiers,
source pins and exact historical quotations while updating reader-facing text.
