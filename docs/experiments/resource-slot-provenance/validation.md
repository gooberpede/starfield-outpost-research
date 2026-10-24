# D4E validation and reproducibility

2026-10-25, Australia/Sydney. [Contract](contract.md), [result](report.md),
[provenance](sources.csv), [independent disposition](review.md).
All paths below are relative to the repository. Raw and derived evidence stays
under ignored `.local-work/`; none is included in the research patches.

## Prediction separation and primary comparison

`freeze01/prediction-v1.json` is generated exclusively from pinned installed
definitions, the owned selection model and label-free body requests. Its script
does not read D4D receipt/event files, old component predictions or expected
candidate names. The prior reports and brief disclosed the answers, so this is
mechanical prediction separation, not researcher blindness.

The freeze is persisted before `compare.py` decodes original SRO1 captures
358–374. Final `comparison03/comparison.json` compares every one of 48 slot
words, all eight BIOM/root/second-key identities and every map/staging boundary.
All match, including zeros and repeated identities. The existing comparator
checks cleanup-to-return map equality, ready-array/call correspondence, source,
frame, owner/type/range and invocation consistency. The final selected-root
array and all four ordered calls match the independently predicted result.
This explicitly cropped construction is not a new audit of all 3357 receipts;
the separately preserved D4D audit covers that session.

The later general small-list tie refinement consumes frozen component maps,
installed rarities and pinned sort instructions. Build02 persists
`candidate-freeze-v2.json` before generating geometry. It does not alter the
original eight-component target freeze, its hash or D4C's historical prediction.

## Regression and cohort accounting

The complete final receipt is `validation03/summary.json`, with individual
native comparisons, both corpus representations, full case inventory and all
46 association rows. The native roster is four Feynman controls (299, 325, 696,
716), three Carinae controls (1270, 1280, 1301), and three Archimedes controls
(829, 2881, 2941). The Archimedes comparisons additionally require exact source
identity. Resource, ordered binary32 XYZW, 16-byte native sphere bound and
callback decisions are separate checks. Matching one geometry never qualifies
the entire generated population.

`historic-regressions01/roster.json` retains 34 unchanged frozen D2/D3 request
replays, 17 from each roster, with exact parsed output equality and eight denied
inference probes. Both original D1 requests and all seven original controls are
rerun in both frozen representations by the inherited validation driver. Its
ancillary historical startup/ablation/size receipts are retained; D4E draws no
new performance or compression conclusion from them.

There are 19 Save52 case rows: 17 active-qualified predictions and two preserved
disabled exclusions. Saved-active qualification is not complete authoritative
player membership. Every saved resource association retains its original D2/D3
classification beside the new D4E diagnostic classification. Separate Water
admission remains separate. Unsupported masks/descriptor choices do not become
resource absence and unresolved positive associations are never silently changed.

Final results: all ten controls match exactly in normalized and expanded form.
All 17 active-case predictions agree between representations. Among held-out
association rows, D4E gives 26 positive correspondences, nine indeterminate pairs
and four separate alternative-admission Water pairs. Only Archimedes Tungsten
changes diagnostically from D3's potential false negative to positive
correspondence. The Lithium regression is resolved by the source-backed small-list
sort; no prior positive is lost in the final diagnostic table. Frozen D2/D3
classifications remain unchanged on disk. These are conditional association
results, not native absence or historical epoch findings.

The final canonical Save52 payload grows by 838 bytes: body candidate data adds
784, generation-block dependencies add 53, and the schema tag adds one. The
control corpus grows by 110 bytes: 56, 53 and one respectively. There is no new
inference field. `checks01/field-costs.json` independently recomputes the deltas
from prior/new serialized field values. New raw installed lineage stays local.

## Failures and corrections

| Retained attempt | Failure or limitation | Correction and limit |
|---|---|---|
| `d4e-slotrefs01.tsv/.log` | Last requested address was not a function entry; no END. | Retained partial output; `d4e-producers02` exports the containing function. Complete slot writer evidence is in `d4e-slots03` and the inherited ui-28 export. |
| `comparison01` | Integer map keys versus JSON string keys falsely reported seven transition mismatches. | `comparison02` normalizes key domains; `comparison03` also explicitly primes cropped sequence state and compares all second keys. Frozen predictions are unchanged. |
| `validation01` | Completed predictions were frozen, then comparator failed with `KeyError: alternative` from an incorrect CSV-column assumption. | Original method and predictions retained. `validation02` verifies frozen output/corpus hashes before reuse, then reads the actual `d3` classification column. |
| `build01 / validation02` | Conservative unequal-rarity tie refusal made Lithium at `D2-830a80` indeterminate despite its preserved D3 positive. | Native small-list insertion instructions establish stable encounter order. `build02` versions this rule; `validation03` reruns the complete prediction roster. No resource-name exception. |

Independent review also identified that a nonnull Special selection alone does
not establish native slot-4 admission. A separate fail-closed qualifier now
requires occupancy below eight, accepted occurrence and a selected descriptor,
and rejects a difference in native/model Everywhere occupancy sets. Build02
predates this admission guard. `qualification01.json` separately verifies all 16
represented bodies and three selected Specials without changing corpus bytes;
the final check driver repeats this qualification. Two additional synthetic
rejection tests cover those boundaries. The original target freeze is unchanged.

The exact failure ledger and test logs are local. Successful tests do not erase
failed derivatives or establish universal native selection behavior. The inherited
descriptor-order ambiguity and mixed construction-query masks remain explicit.
No new acquisition route is needed for the closed sixth-slot question.

## Reproduction commands and effects

Use installed CPython 3.14.3 at
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`, with `-B`.
Every output destination must be fresh; examples below name the actual retained
directories and therefore refuse overwrite if repeated unchanged. Scripts document
reads, writes, dependencies and effects in their module docstrings. No script
launches or attaches to Starfield, modifies a save, or writes analysis content.

```powershell
python -B research/resource-slot-provenance/audit.py before
python -B research/resource-slot-provenance/freeze.py --output .local-work/resource-slot-provenance/freeze01
python -B research/resource-slot-provenance/compare.py --freeze .local-work/resource-slot-provenance/freeze01 --output .local-work/resource-slot-provenance/comparison03
python -B research/resource-slot-provenance/corpus.py --base .local-work/resource-owner-root/source-layout01/D3/normalized.json --freeze .local-work/resource-slot-provenance/freeze01 --output .local-work/resource-slot-provenance/build02
python -B research/resource-slot-provenance/corpus.py --base .local-work/resource-owner-root/source-layout01/D1/normalized.json --freeze .local-work/resource-slot-provenance/freeze01 --output .local-work/resource-slot-provenance/build-controls02
python -B research/resource-slot-provenance/validate.py --build .local-work/resource-slot-provenance/build02 --controls .local-work/resource-slot-provenance/build-controls02 --output .local-work/resource-slot-provenance/validation03
python -B research/resource-slot-provenance/regressions.py
python -B research/resource-slot-provenance/audit.py after
python -B research/resource-slot-provenance/checks.py --label checks01
python -B research/editorial/screen.py --changed
python -B research/resource-slot-provenance/package.py --label review01
```

New native exports use the existing owned `research/workshop-population/export.ps1`:
`d4e-slots03` requests `140777870`, `140779760`, their reference lists and
`14076e810`; `d4e-descendants04` requests `1407780b0`, `140777e30`,
`14077c0e0` and `14077bce0`. The script reads the existing Ghidra database with
`-readOnly -noanalysis`, writes local TSV/log/cache artifacts and leaves symbols,
types, comments and analysis settings unchanged. The initial partial and corrected
locator exports are separately pinned. No imported executable/database enters Git.

## Preservation and outcome dimensions

Before/after audits compare 26458 immutable artifact pins, protected save/content
receipts, executable, ESM, PlanetData, HEAD and index. Both pass with zero protected
changes and Starfield absent. Both drives pass the 40,000,000,000-byte guard.
No original save, frozen prediction, historical evidence, installed definition,
configuration or analysis-content mutation is performed. No restoration or cleanup
is needed. Read-only tools and local derivatives are the only target effects.

Scientific result, implementation checks, evidence integrity, target survival,
authority compliance and independent review remain separate. The final criterion
matrix and exact-snapshot disposition are in review.md. No reviewer result grants
integration, staging, commit, push, live execution or publication authority.
