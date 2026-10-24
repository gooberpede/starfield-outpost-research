# Executed checks and reproduction

Run commands from the repository root using installed CPython at `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`; `python` on PATH is an inaccessible Windows alias on this host. All outputs listed here are ignored/local. No package installation is needed. Each output directory must be fresh; preserve previous attempts.

| Check | Actual result | Primary receipt |
|---|---|---|
| Protected inputs and inherited D4A framing | 6626 baseline pins; 3027 receipt/ACK pairs; 9081 records; no protected changes | `resource-tungsten-repair/audit-before.json`, `audit-final.json` and matching protected receipts under `.local-work` |
| Build | MSVC 19.51.36256.0, fresh d4b-build04, exit 0 | `resource-tungsten-acquisition/d4b-build04/build.json` and `build.log` |
| D4A full synthetic suite | 46 cases pass, including nested/thread/cache, malformed input, transport and crash cases | `resource-tungsten-acquisition/d4b-qualification03/summary.json` |
| Terminal repair | 12 real Windows cases pass expected outcomes; intentional failure cases retain controller exit 2 | `resource-tungsten-repair/terminal04/summary.json` and per-case events/receipts |
| Legacy comparator | Post-ACK rearm reproduced; historical API error not reproduced | `resource-tungsten-repair/legacy-terminal04/summary.json`; failed strict-error trials 01/02 retained |
| D4 inherited selection | 34 cases pass | `resource-selection-context/d4b-regression01/qualification.json` |
| C1G inherited weight/selection | 27 cases pass | `resource-selection-operands/d4b-regression01/qualification.json` |
| C1E inherited region ancestry | 32 cases pass | `resource-region-ancestry/d4b-regression01/qualification.json` |
| C1D inherited retail-adapter fixture | 13 cases pass | `resource-oracle-retail/d4b-regression01/qualification.json` |
| C1C inherited collector/transport | 19 cases pass their positive/negative expectations | `resource-oracle-collector/d4b-regression01/qualification.json` |
| Python semantics and receipts | 31 standalone, five D4A contract and eight transport tests pass | `resource-tungsten-repair/python-checks01/summary.json`, stdout/stderr and transport receipts |
| Archimedes diagnostic reconstruction | Three exact region matches, with and without competition | `resource-tungsten-repair/replay02/summary.json` and full outputs |
| Frozen D2/D3 and seven native controls | Unchanged active request rosters and exact Feynman/Carinae geometry checks | `resource-tungsten-repair/regressions01/roster.json` and `seven-controls/comparisons.json` |

The C1D suite name does not imply retail execution: these are its disposable fixture tests. Expected invalid acquisition results in C1C are preserved as negative controls, not promoted to successful scientific captures. The older single-thread D4A suite alone did not test the repaired terminal obligation. [Detailed engineering limits](teardown.md) explain the distinct API-error reproduction result.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-tungsten-repair/audit.py before
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-tungsten-acquisition/build.py --name d4b-build04
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-tungsten-acquisition/qualify.py --build .local-work/resource-tungsten-acquisition/d4b-build04 --output .local-work/resource-tungsten-acquisition/d4b-qualification03
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-tungsten-repair/teardown.py --build .local-work/resource-tungsten-acquisition/d4b-build04 --output .local-work/resource-tungsten-repair/terminal04
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-tungsten-repair/replay.py --output .local-work/resource-tungsten-repair/replay02
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-tungsten-repair/regressions.py
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-tungsten-repair/checks.py
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/resource-tungsten-repair/audit.py after
```

Inherited commands use each directory's `qualify.py --build ... --output ...`, with builds D4 build12, C1G build05, C1E build06, C1D build14 and C1C build08. Each qualifier checks its source/build manifest before execution. Exact stdout, exceptions and events remain beside the summary. Rerunning the scripts with their original output names intentionally refuses overwrite; select a fresh output/name or adapt only the local destination for a new qualification.

One missing native function was exported with the existing owned `research/workshop-population/export.ps1 -OutputName d4b-owner-map01 -Addresses @('1407bc3d0')`. The runner uses Ghidra 12.1.2, existing project, `-readOnly -noanalysis`, and `ReadSpecialist.java`; it writes only a fresh local TSV/log. No symbol, type, comment or analysis-content change was requested. Existing cont-01/cont-11/ui-29 exports supply the surrounding paths.

Preserved diagnostic failures include the inaccessible PATH Python alias, an initial replay import-path error corrected before any result, two strict legacy `win32=31` reproduction failures, and superseded build/test snapshots. No failure was deleted or relabelled as evidence of a native quota or clean historical exit.
