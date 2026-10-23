# Reproduction, checks and evidence boundaries

2026-10-24, Australia/Sydney. Offline D1 only. [Report](report.md),
[algorithm](algorithm.md), [schema](corpus.md), [rights](rights.md).
Use existing CPython 3.14 at
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe` with `-B`.
The WindowsApps `python` alias was inaccessible during this task; commands below
use `python` as a short label for that verified executable, not the alias.
No package installation is needed.

## Commands and effects

From repository root, using fresh output names:

```text
python -B research/resource-standalone/builder.py --output .local-work/resource-standalone/build03
python -B research/resource-standalone/inventory.py --build .local-work/resource-standalone/build03 --output .local-work/resource-standalone/field-inventory05.json
python -B research/resource-standalone/verify.py --build .local-work/resource-standalone/build03 --output .local-work/resource-standalone/verify03
python -B -m unittest discover -s research/resource-standalone -v
python -B research/editorial/screen.py --changed
```

The builder requires the pinned installed main ESM, EXE and PlanetData archive
and six pinned owned planetary modules at the paths declared in its source.
It freshly walks definitions, extracts two maps in memory, recomputes planetary
components, projects the three supported tiles, and writes two corpus variants,
a flat five-module bundle and a local manifest. It neither reads native
geometries nor imports old prediction JSON. Every output destination is fresh
and under ignored `.local-work`; primary receipts are never overwritten.
All source hashes are checked before and after preparation. The preparation
pipeline includes `inventory.py`, which verifies completed corpus
pins and writes field counts to a separate ignored receipt without changing the
builder's primary manifest or payloads. These are actual serialized field counts.
The full immutable
installed-source selection is intentionally local, not an asserted public API.

To run inference independently, copy only the completed `code/` directory and
one corpus JSON to another directory. Supply a request JSON with the eight
[specified fields](corpus.md). Invoke:

```text
python -I -S -B <portable-code>/predictor.py --corpus <portable-corpus.json> --request <caller-request.json>
```

The predictor imports only those five authored modules and Python's standard
library. Geometry is generated afresh. Results are printed to stdout, including
structured UNKNOWN responses. The request files used here are retained locally
under `verify03/0005e0de-request.json` and `verify03/0005e4da-request.json`.
They contain geographic location/footprint facts, with no source anchors,
surface-pattern IDs, expected regions or resource target labels.

## Negative dependency test

`verify.py` launches a fresh `-I -S -B` process in an empty directory for each
variant/body. `isolate.py` installs an audit hook before loading the predictor.
Its read allowlist is exactly the supplied corpus/request files, flat authored
code directory and interpreter standard-library installation. Site-packages,
writes, subprocesses, sockets and ctypes operations are denied. Eight deliberate
probes test denial of game ESM/EXE, Ghidra, xEdit, native exports, a Carinae capture,
frozen Feynman predictions and prior full geometry outputs.

Audit logs distinguish those guard probes from inference. The four completed
inferences each have eight denied probes and zero forbidden inference reads.
This is a Python audit boundary, not an operating-system sandbox; it does not
claim to intercept every metadata query or prove security against hostile native
code. The tested implementation uses ordinary Python/stdlib reads and no native
escape mechanism. All observed open/list/scandir operations are recorded locally.
The installed game and research files were not renamed or made globally
inaccessible; they were denied to inference by this controlled allowlist.

Each predictor output is persisted and hashed before the verifier opens native
controls. The verifier then checks original SRO1 framing, sequence/digests and ACK
identity, plus the independent C2D ledger's raw-capture hashes. It compares exact
resource identity, complete ordered XYZW bytes and the first 16 native-bound bytes.
Callback decisions are independently required to match, not merely reported.

## What the controls establish

Four Feynman controls are C1E captures 299, 325, 696 and 716; three Carinae controls
are C2A captures 1270, 1280 and 1301. Each has exactly one matching generated path
in each representation. At radius 150, the Feynman model resolves four sources
and 103 paths; Carinae resolves six and 1326. Larger historical Feynman halo
predictions remain intact. The narrower request's 103 paths do not contradict
the earlier 156-path population generated for a larger request neighborhood.

Seven accepted paths establish neither a native population count nor absence of
other accepted paths. The 99 additional Feynman and 1323 additional Carinae paths
are UNVERIFIED against this seven-control set, not proved native extras. Missing
control count is zero. Spatial point membership, area availability, callback
acceptance and source enumeration are separately reported in the local summary.
No connected-deposit or extractor count is inferred from a path count.

Sixteen authored synthetic tests cover wrong schema/definition, corrupted digest,
malformed types, missing dependency groups, invalid expanded routes, forbidden
witness fields, chart/seam/numeric domains, missing and partial coverage,
single-backlink semantics, mixed masks, unsupported resource branches, point
boundaries, unresolved clipped-area propagation and unused descriptor tails.
The boundary-aggregation test injects an authored region and tests UNKNOWN
propagation; it is not a native generation observation. Existing geometry,
selection, settings, enumeration, ancestry, spatial and editorial suites are
run separately with actual logs and counts. [Review](review.md) records final
editorial/manual/independent dispositions and verified delivery identity.

## Preserved failures and scientific limits

The initial builder rejected a Feynman biome because it contained an Everywhere
entry. Inspection showed its own generation block has chance zero; the strict
gate cannot emit paths and each resource/cell reseeds independently. The builder
now verifies that zero before omitting only that geometric pass. It still makes
no Water availability or final admission claim. Nonzero/unresolved Everywhere
remains unsupported. No historical prediction or primary evidence was rewritten.

Early verification runs `verify01` and `verify02` completed the exact geometry
comparisons but failed an ablation that replaced a source width dimension with
the same value. Their receipts are retained and are not successful engineering
closure. The corrected test adds 12 to a used source's raw dimension. Independent
review also found expanded-schema/malformed-type gaps and a callback assertion
omission; corrections and synthetic regressions precede the final run.
Harness changes made while earlier runs were executing are not attributed to
those executions. The final run pins its own verifier/isolation sources at entry.
After that run, only the isolation module's header was clarified to distinguish
standard-library native modules from custom native libraries. Its executed source
is preserved at `.local-work/resource-standalone/science03-source/isolate.py`;
an AST comparison excluding the module docstring verifies identical behavior.
The final source and that historical executing snapshot have separate ledger pins.

The model uses pinned main definitions and no plugin/archive merge. Historical
overrides, tree mutation, generation epoch, effective component/atmosphere state,
native source census, seams/rotation/default sources, nonuniform masks and
universal marginal native floating-point equivalence remain unresolved.
No live evidence is required to establish this bounded seven-control result;
no live run card is proposed or executed. A broader predictor would first need
additional portable tiles and qualified component/source branches, followed by
separately authorized discriminating evidence where offline inputs are inadequate.

Protection uses the existing prospective save policy: classified active
autosave/exitsave churn is diagnostic; designated research/manual/quicksaves,
archives and unclassified saves remain strict. Before/after broad audits and a
separate frozen historical-evidence/analysis-state snapshot are local. HEAD and
index equality and both-drive 40,000,000,000-byte free-space guards are checked.
These checks establish preserved bytes within the audited inventory, not game
semantics or publication rights.
