# SOR-EV-0027 — Activated-overlay/grid review package

2026-10-10 Australia/Sydney. [Answer-first report](../activated-overlay-and-grid-geometry.md),
[authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_activated_overlay_and_planetary_grid_geometry.md).
Strong partial; critical review required. Authored text/numeric selections
REVIEW-REQUIRED. Raw saves, assets, captures, native text and databases LOCAL-ONLY.

The durable answer is a body/site/frame/local-center representation. Activation
and rebase stages are mapped, designated discrete cells use their centers, and
actual2×2 subdivision spans are supported. General selected saved-frame restoration
and a continuous residual-to-surface consumer remain unqualified. Invariance and
quantized angle agreement cannot establish a unique continuous geographic center.

## Exact deliverables

Modified registers: [CREDITS](../../../CREDITS.md), [decisions](../../DECISIONS.md),
[sources](../../SOURCES.md), [provenance](../../PROVENANCE.md),
[permissions](../../PERMISSIONS.md), [research state](../../RESEARCH_STATE.md),
[findings](../../known-facts.md), [functions](../../function-register.md),
[states](../../state-register.md), [hypotheses](../../hypotheses.md).
New: this README, report, two original scripts and the12 selected CSVs below.
The supplied brief pre-existed untracked and is retained unchanged; it is included
in the full diff, excluded from the task-only authored diff. No prior report edited.

| File | Selected content and limits |
|---|---|
| [invariance.csv](invariance.csv) | Four compensated-center/angle rows, exact identities, bytes and decoded offsets; continuous candidates explicitly unqualified. |
| [terrain-captures.csv](terrain-captures.csv) | Nine separately decoded origin/grid snapshots. |
| [active-terrain-pairs.csv](active-terrain-pairs.csv) | Nine active pairs from mode-selected member; no selected-edge payload observation. |
| [projection.csv](projection.csv) |41 repeated/control/site/city angular rows; no continuous truth oracle. |
| [object-transforms.csv](object-transforms.csv) | Own XYZ/rotation, qualified versus unqualified subtraction. |
| [controls.csv](controls.csv) | Seven no-action comparisons. |
| [decoded-inputs.csv](decoded-inputs.csv) |23 selected decoded hash/size receipts, no raw saves. |
| [block-dimensions.csv](block-dimensions.csv) |14 distinct installed dimension pairs/counts/examples; undersized arithmetic explicitly diagnostic. |
| [pattern-positive-spans.csv](pattern-positive-spans.csv) |16 deterministic positive-span examples, first eight distinct pattern/block joins per span. Full53165-slot count remains in local summary. |
| [orientation-matrices.csv](orientation-matrices.csv) | Eight original numeric PE table selections. |
| [native-map.csv](native-map.csv) |40 decisive function addresses/RVAs and exact export locators. |
| [native-exports.csv](native-exports.csv) |12 local export/log hashes, inventories and limits. Raw native text excluded. |

Original scripts: [audit_activated_grid.py](../../../save-analysis/scripts/audit_activated_grid.py)
and [test_activated_grid.py](../../../save-analysis/scripts/test_activated_grid.py).
The audit reads the pinned PE/ESM, prior manifests and selected raw terrain; hashes
before/after, checks matrix identity, walks SFBK/SFPT with existing original reader,
and writes only a fresh local numeric/receipt directory. Stdlib/project modules
only; no target/save/database/network/Git actions. The mathematical helpers are
research models, not a native ABI or continuous location API. C:/D:40GB guard;
existing reader payload/decompression bounds remain in force.

## Reproduction

Run at repository root with the separately installed CPython3.14 runtime. Fresh
output names required. Prior frozen local manifests/archives must be present.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/research_durable_center.py --run NEW-RUN
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/research_workshop_origin.py --run NEW-CAPTURES
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/audit_durable_center.py --receipts .local-work/durable-center/NEW-RUN/results.json --captures .local-work/workshop-origin/NEW-CAPTURES/captures.json --fixed docs/experiments/planetary-surface-anchor/fixed-anchors.csv --session .local-work/beacon-observer-live/session-17596-91165828 --output .local-work/activated-grid/NEW-CORPUS
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/audit_activated_grid.py --exe D:/ReverseEngineering/Starfield/Starfield.exe --esm 'C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm' --session .local-work/beacon-observer-live/session-17596-91165828 --output .local-work/activated-grid/NEW-GEOMETRY
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B -m unittest discover -s save-analysis/scripts -p 'test_*.py'
```

Actual fresh corpus: `.local-work/durable-center/activated-grid-01/`; captures and
5265-file verification: `.local-work/workshop-origin/activated-grid-01/`; selected
audit `.local-work/activated-grid/corpus-audit/`; final geometry `geometry-03/`.
Corpus and geometry CSVs are copied byte-for-byte into this authored selection.
Native exports use existing `ghidra/scripts/Invoke-OutpostRecon.ps1 -Target Starfield
-OutputName activated-grid-NN.tsv -Addresses @(...)`; exact args in each hashed log.
Existing Ghidra12.1.2/JDK21, Xmx2G, readOnly/noanalysis. Four instruction caps in
batches06/10 retained; no export error or decompiler cap observed. A final batch12
provides direct bodies for registration functions previously present as xrefs.
Existing reference inventory/finite windows are not exhaustive writer coverage.

## Actual checks, failures and limits

**95 Python tests pass**, including four new tests: all49152 hierarchy indices,
signed seam/remainder transitions, designated-center/pole roundtrips and eight
square-permutation transforms with a synthetic2×4→4×2 footprint. These execute no
native code; the non-square test is mathematical capacity, not an installed asset.
Final geometry audit separately checks the extracted native matrix table against
the expected eight matrices.23-save/128-prefix, seven controls,19 zero mature
compensations,18 beacon observations/nine terrain snapshots all pass.41 angular
rows max errors8.881784197001252e-16 lon/3.3306690738754696e-16 lat radians.
Geometry scan1753blocks/258patterns yields48960 positive1×1 and4205 positive2×2
slots; no non-square block dimension pair. Nine active pairs agree with origin,
max reconstructed angle error1.6653345369377348e-16 radians.

The first geometry attempt incorrectly passed a volume root to the output-size
guard, which enumerated that root and stopped with `output bound stop` before
creating output. Corrected to guard only the actual output parent (the helper
itself checks both volumes); no target/write effect. `geometry-01/02` are retained
development receipts; final03 includes deterministic16-row selection and pinned
matrix comparison. Failed Reddit fetches do not block independent engine research.

Protected pre-export baseline17 files is `.local-work/activated-grid/protected-before.json`.
Fresh source/archive reader receipts and final protected/source identities,
metadata changes, script/output hashes, Markdown file-link checks, diff whitespace,
HEAD/index preservation and free-space values are retained in
`.local-work/activated-grid/review/verification.json`. Metadata churn is recorded
separately from byte preservation; it is not silently restored. No original save
overwrite or Ghidra analysis-content edit is authorized/performed.

Final verification rechecks41 distinct protected/source/archive/manifest files:
zero byte/size changes. Four Ghidra index files changed filesystem timestamps;
their hashes/sizes remain identical. All changed Markdown file/anchor links pass,
all authored new-file and tracked whitespace checks pass, and HEAD/index are
unchanged. The supplied brief's three pre-existing Markdown hard-break lines are
reported separately and preserved. Final guard values exceed88GB on C: and139GB
on D:.26 task-authored changed/new files plus the unchanged supplied brief are
listed individually in the manifest. A Windows null-path check attempt was corrected
to `/dev/null`; the check exposed only those supplied-brief hard breaks.

Review files (ignored, local):

- `.local-work/activated-grid/review/task-only.diff` — all authored changes including new files.
- `.local-work/activated-grid/review/complete.diff` — full tracked/new-file-inclusive changes, including supplied brief.
- `.local-work/activated-grid/review/changed-files.json` — exact paths/status/hash manifest.
- `.local-work/activated-grid/review/status.txt` — final `git status --short` snapshot.
- `.local-work/activated-grid/review/verification.json` — actual check receipts and limits.

No staged changes, commit/push, new live work, third-party incorporation, fork/PR,
contact or publication. Missing selected-frame join and continuous consumer are
review blockers for a **complete geographic claim**, not reasons to withhold the
supported discrete/frame result. Proposed acquisition requires a separate brief.

Suggested commit after review:

```text
research: trace activated overlays and planetary grid geometry
```
