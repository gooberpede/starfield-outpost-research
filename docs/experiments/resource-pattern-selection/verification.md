# Reproduction and actual verification

Use installed CPython 3.14 at
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`, with `-B`,
from repository root. No dependency installation or target execution is needed.
All authored analytical methods use stdlib and existing project-owned methods
under SOR-P-0002. [Exact per-use pins](sources.csv) include the unchanged RG1
math, ESM reader, C2C analysis, independent receipt framing and review exporter.
Bethesda supplies the native/definition evidence. Ghidra 12.1.2/JDK, CPython and
Git are separately installed tools; no outside implementation is incorporated.

## Actual calculation and test commands

```powershell
python -B research/resource-pattern-selection/predict.py --output .local-work/resource-pattern-selection/blind02.json
python -B research/resource-pattern-selection/predict_installed.py --output .local-work/resource-pattern-selection/installed01.json
python -B research/resource-pattern-selection/predict_installed.py --output .local-work/resource-pattern-selection/installed03.json
python -B research/resource-pattern-selection/validate.py --prediction .local-work/resource-pattern-selection/installed01.json --output .local-work/resource-pattern-selection/validation05.json
python -B research/resource-installed-settings/replay.py --settings .local-work/resource-installed-settings/settings01.json --output .local-work/resource-installed-settings/c2d-replay01.json --geometry .local-work/resource-installed-settings/c2d-geometry01.json
python -B -m unittest discover -s research/resource-pattern-selection -v
python -B research/resource-pattern-selection/export_results.py --output-directory .local-work/resource-pattern-selection/export03
python -B research/editorial/screen.py --changed
```

Use fresh names when reproducing: result creation is exclusive. The selected
export recipe is version-bound and also exclusively creates its destinations.
It must not be rerun over the delivered numeric files. The corrected export03
files replaced the authored derivatives only after preserving the entire failed
review01 tree locally. Native exports use the
existing owned OutpostRecon reader in a `-readOnly -noanalysis` worker; the
12 numbered request files, exact Java command, script identities and logs remain
under `.local-work/resource-pattern-selection/`. No symbols/types/comments,
analysis bytes or game processes were changed. The worker was stopped through
its own stop file after completing the bounded requests.

| Method | Reads, writes and limits |
|---|---|
| `selector.py` | Pure generation-control and single-backlink calculations; no I/O. Registry order, map and effective settings are explicit operands. Unsupported default/seam/orientation branches remain explicit. |
| `predict.py` | Reads the owned definition/map derivatives and frozen site geography; writes a local default-generation trace. Accepts no witness or geometry input. |
| `installed.py` / `predict_installed.py` | Reads the pinned main ESM, selected PNDT links and referenced SFTR tables; writes local complete tables and selected traces. No runtime witness dependency; arbitrary plugin namespaces and packed ENAM are unsupported. |
| `validate.py` | Checks closed predictor identity before opening witnesses; reads frozen context, installed requests and seven raw native geometries. Writes local full generation and per-cell/source comparisons. Uses the old retained pattern only for the clearly separate C2C before state. |
| `export_results.py` | Reads final receipts and pins; creates selected JSON/CSV only. Complete SFTR arrays, native decompilation and full generated paths stay local. |
| Tests | Sixteen new synthetic controls exercise order/null/style eligibility, empty/single/multiple draw schedules, CRC operand order, seed sensitivity, rotation stream shifts, one versus recursive backlinks, invalid/default/neighbor cases and PNDT/SFTR decoding. No proprietary fixtures. |

The new tests and inherited suites pass: 16 selector/installed-tree, 24
geometry/context, four C2C enumeration, 15 installed-settings, one ancestry,
12 spatial-consumer and eight editorial tests; **80 total, zero skips**.
Commands, exit codes and log hashes are in `tests02.json`. `determinism02.json`
records identical selected traces and both complete installed-tree tables across
two runs. The generation-control tables also equal the inherited selector's
entire output for both planets.

`validation05.json` directly reparses the seven captured regions and finds one
exact resource/bound/ordered-XYZW match each. Feynman's full 156-path geometry
sequence is unchanged after excluding source labels from that comparison;
source identity changes are separately recorded, not hidden by this check.
Carinae generates 1326 paths from six sources. Every new source footprint and
four-cell margin passes the expected uniform ordinary-mask check. The fresh
C1H replay regenerates the 1051 frozen paths, retains four accepted Feynman
matches and all three chance controls. It does not substitute for a new live test.

## Preserved diagnostics and protection

The default-generation prediction was calculated first and remains falsified
against the held-out Carinae SFPT. An initial validator attempt failed with
`KeyError: source` because a local geometry row identifies its source under
`request.source`. That schema access was corrected; no result file had been
written. `validation01` retains the corrected conditional-generation diagnostic;
`validation02..04` preserve linked-tree, direct-seven-path and footprint-check
iterations respectively. They are separate derivatives, not overwritten freezes.
Independent review01 returned REWORK for stale cell/source-route labels, an
unsupported nonzero-default classification, two missing fresh replay pins and
the audit denominator wording. The entire 27-file failed tree and actual review
are retained locally. `validation05` corrects route/reason labels; its geometry
is byte-identical to validation04. A new regression distinguishes an unrepresented
nonzero default from null. Both fresh C1H outputs are now explicitly source-pinned.
The first correction export, export02, began before the repeat-test receipt
closed and failed on the missing determinism02 file. Its partial local output
is preserved; no authored derivative was replaced from it. The exporter now
checks required closed receipts before creating output. A shell-quoting failure
while preparing the second test recipe also performed no calculation or input
write; a saved Python preparation recipe replaced that failed command.

Native exploratory selectors at `0x14096b930` and `0x140770e00` were not existing
function entries; their NO_FUNCTION_AT diagnostics are retained. A broad symbol
substring locator reached its 256-symbol cap and was used only to locate the
specific tree vtable. Instruction caps remain explicit; full decompilation and
existing complete instruction windows support the cited branches. Exact
SwapInfo string/symbol searches did not establish a consumer. No absence or
publication claim is derived from those failed locators.

Before/after broad audits contain 12974 total rows, including 173 excluded active
transient rows. They report zero protected changes and retain the historical
missing-exitsave discrepancy separately. The inherited 63 installed/configuration/EXE
pins are covered by that protected audit. A separate 68-file snapshot preserves
the C2C/A1/C1H historical records and analysis database files. Consumed predictor,
definition, geometry and capture hashes are checked independently in the actual
calculations. HEAD/index remain identical to `baseline.json`. Both-drive
40000000000-byte free-space guards pass. These are offline integrity checks,
not authority to launch or a claim of historical loaded-state equality.

No new live collector or run card was needed after resolving the installed-tree
route. No game launch, attachment, new acquisition, configuration/save change,
third-party reuse decision, disclosure, staging, commit, push or publication
occurred. Exact final editorial/review/package disposition is in [review.md](review.md).
