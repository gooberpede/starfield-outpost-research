# D5D offline verification

[Research and authority](../../docs/experiments/resource-construction-demand/report.md).
Run from the repository root with installed CPython 3.14.3 and `-B`; stdlib and
existing project-owned methods only. No dependencies are downloaded. All receipt
outputs are exclusive and ignored under `.local-work/resource-construction-demand/`.

| Helper | Reads / writes / effects |
|---|---|
| `audit.py before` | Adapted from D5C at HEAD `bd3d0485ccc0abc5405ee57f076945fb047bb551`, under SOR-P-0002. Reads historical D5B inventories, all D5B artifacts, recon exports, D5C artifacts, specialist exports and the 15-file analysis database pin set. Verifies historical expected pins and current protected-save policy before writing before receipts. Requires game absence and both-drive 40,000,000,000-byte free-space guard. No target/database/save writes. |
| `audit.py after` | Rehashes that exact before set and protection policy; checks HEAD/index equality and empty staged diff. Writes separate after receipts, never originals. It checks byte preservation, not native semantics. |
| `assess.py` | Verifies inherited immutable local source pins and D5C method pins, recounts nine closed journals, derives small selected boundary/phase metadata, checks five new native exports and the unchanged ten-control ledger/frozen alternatives. Writes ignored `assessment.json` and exclusively creates the authored `sources.csv`. Run once per fresh delivery tree; it intentionally refuses to overwrite that ledger. Does not rerun geometry or all historical SRO1/ACK qualification. |
| `package.py --label review01` | Adapts D5C's exporter, importing unchanged `runtime/session-tools/export_review.py`. Reads actual Git tracked/untracked text and before receipt. Writes complete/task-only patches, SHA-256s, inclusion/exclusion/status/check manifests, and disposable forward/reverse comparison trees under `.local-work/review-patches/`. Stops parent Git discovery at `.local-work/`. No staging, refs, network or repository history writes. Use a fresh label for each export. |

Actual commands:

```powershell
$d5dPython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $d5dPython -B research/resource-construction-demand/audit.py before
& $d5dPython -B research/resource-construction-demand/assess.py
& $d5dPython -B research/resource-construction-demand/audit.py after
& $d5dPython -B research/editorial/screen.py --changed
& $d5dPython -B research/resource-construction-demand/package.py --label review01
```

The unchanged `research/workshop-population/export.ps1`/`ReadSpecialist.java`
reads the existing analysis with `-readOnly -noanalysis`; five actual selector
lists and log-derived invocations are retained in local `commands.json` and
`d5d-demand01..05.log`. Fresh TSV/logs and tool cache/settings are the only
requested native-tool outputs. Database bytes are checked against the inherited
15-file pin set; read-only flags alone are not preservation evidence. Installed
Ghidra 12.1.2/JDK 21.0.12.8 tool pins are inherited and verified in `sources.csv`.

The first assessment reached CSV serialization after its checks, then refused
an absolute installed-tool path outside the repository. The corrected serializer
retains that absolute path. It did not overwrite an output. One navigation-edit
recipe failed decoding UTF-8 prose through Windows' default encoding before any
navigation writes; explicit UTF-8 corrected it. Initial locator/early export reads
also encountered unavailable or still-incomplete paths; they were retried using
actual paths and completed exports, never treated as absence evidence.

The changed-text screen also detected Windows encoding damage in the new
acquisition table after an early edit. The table was repaired from the reversible
encoding transformation and manually reread; runtime pointer/PID transcriptions
were independently checked against the journal metadata before review.
