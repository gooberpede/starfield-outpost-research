# Reproduction, provenance and verification

Use installed CPython 3.14 at
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`, with `-B`
from repository root. No package installation or target execution is needed.
Existing owned geometry/context, independent SRO1 framing and C1H installed
settings methods are reused under SOR-P-0002. No sibling repository or external
source was newly consulted; [pins](sources.csv) retain exact per-use provenance.
Bethesda exports and raw definitions remain LOCAL-ONLY. Self-credit is optional;
no substantive third-party code or research was incorporated.

```powershell
python -B research/resource-source-enumeration/analyze.py --output .local-work/resource-source-enumeration/analysis05.json
python -B research/resource-installed-settings/replay.py --settings .local-work/resource-installed-settings/settings01.json --output .local-work/resource-installed-settings/c2c-replay01.json --geometry .local-work/resource-installed-settings/c2c-geometry01.json
python -B research/resource-source-enumeration/export_results.py
python -B -m unittest discover -s research/resource-source-enumeration -v
python -B -m unittest discover -s research/resource-geometry -v
python -B -m unittest discover -s research/resource-installed-settings -v
python -B -m unittest discover -s research/resource-generation-ancestry -v
python -B -m unittest discover -s save-analysis/scripts -p test_resource_spatial.py -v
python -B research/editorial/screen.py --changed
```

These are the actual output names. Reproduction uses a fresh local analysis
filename because exclusive creation refuses overwrites. The exporter is a
one-shot selected-data recipe for this frozen output version; do not rerun it
over existing CSV/JSON files. To export a later version, change both versioned
destinations and the selected local analysis input explicitly. It never changes
the frozen RG1/RG2 predictions. Analysis resource bounds are the existing finite
halo, finite installed compatible-pattern list, complete finite source cell
ranges and three captured comparisons. No scientific time/event quota is used.

| Method | Reads / writes / effects |
|---|---|
| `analyze.py` | Reads frozen v2 requests, installed-map/definition derivatives, closed C2A/C2B captures, C1H requests and constants. Pins its direct inputs before/after. Creates one exclusive ignored analysis JSON. Witnessed enumeration, independent candidate envelope and complete unfitted source generation use unchanged project math. |
| `test_analysis.py` | Synthetic pattern selection, restoration after failure, missing-anchor reporting, coherent key reframing and exact binary32 comparison controls. No proprietary fixture or target execution. |
| `export_results.py` | Reads the final local analysis and C1H control replay; exclusively creates six versioned inventory CSVs, selected JSON results/controls and a source ledger. No raw memory/DNAM/complete geometry is exported. |
| Existing C1H replay | Regenerates both complete frozen populations, resolves installed settings, reparses native controls and produces new ignored receipts/full geometry. No existing prediction is replaced. |
| Local finalization recipes | Stdlib/read-only Git/protected-input hashes, subprocess test logs, editorial receipts, manifests and exact patches only. No save, configuration, analysis database, Git index/ref, network or target mutation. |

## Actual results and preserved diagnostics

The new four-test suite and inherited suites are retained with command, exit code
and log hashes in `.local-work/resource-source-enumeration/tests.json`. Full
analysis is `analysis05.json`; earlier `analysis01..04.json` preserve incremental
diagnostics rather than replacing them. C1H controls are
`.local-work/resource-installed-settings/c2c-replay01.json` and
`c2c-geometry01.json`. Four Feynman exact matches and three native chance
comparisons pass; all 1051 frozen paths regenerate before installed resolution.

All 64 tests pass with zero skips: four new analysis controls, 24 geometry/context
tests, 15 installed-settings tests, one ancestry test, 12 area-consumer tests and
eight editorial tests. Both protection audits report zero protected changes;
`installed-check.json` confirms all 63 installed/configuration/EXE pins are
covered by that audit. The inherited missing exitsave remains historical.

An initial exploratory print attempted source resolution outside the required
halo and raised `unqualified source anchor`. No prediction was written by that
print. The delivered algorithms preserve those errors explicitly when they
occur inside their finite scope: 48 Carinae unresolved cells, zero Feynman
candidate-envelope failures. That is an actual limitation of the inherited
resolver, not a passing absence test. Two exploratory reads used nonexistent
documentation filenames; the actual phase-b-results JSON and native/source
records were then used. No scientific input was changed to repair a read error.

The broad inherited protection audit reads 12974 historical entries, applies
the accepted transient-save policy only in the active live-save namespace and
finds zero protected changes. It preserves the historical missing exitsave as a
discrepancy and excludes 173 active transient rows; it never replaces expected
hashes. Before/after audit receipts, exact consumed-input pins and unchanged
HEAD/index are retained locally. This is offline preservation verification, not
a live preflight or authority to load Save52. The 40,000,000,000-byte free-space
guard on each drive is checked before work and delivery export.

Finalization screens all changed authored text, manually reads every changed
prose/table/CSV label/comment/docstring and navigation addition, and obtains
independent scientific/editorial review of the exact final hashes. Newline,
encoding, whitespace and local-link checks are enforced by the existing review
exporter. Screen diagnostics and a manual inventory remain local. The independent
decision and exact manifest/diff identities are retained in [review.md](review.md).
