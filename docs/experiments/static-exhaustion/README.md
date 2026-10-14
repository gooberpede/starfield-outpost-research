# SOR-EV-0028 — Continuation review package

[Answer-first report](../activated-overlay-static-exhaustion.md) ·
[Terminal dependency ledger](dependency-ledger.md) ·
[Save/frame call map](call-and-dataflow.md) ·
[Residual/ambiguity map](residual-map.md) · [Trace history](trace-notes.md).
Authored evidence REVIEW-REQUIRED; raw inputs LOCAL-ONLY. No integration,
publication, live action, staging, commit or push follows from this package.

## Selected artifacts

| File | Contents / limits |
|---|---|
| [saved-world-context.csv](saved-world-context.csv) | Six unit 3 envelopes/decoded hashes/active keys and component-run counts; Save2 has no selected beacon-component scan. |
| [saved-world-descriptors.csv](saved-world-descriptors.csv) |111 numeric body/key/saved-token descriptors across 38 installed bodies, exact sampled ID-domain and offsets retained; not raw assets. |
| [saved-center-frame.csv](saved-center-frame.csv) |25 selected beacon joins, including 23 active and two disabled; exact controlled center invariance, signed-floor result. |
| [residual-countermodels.csv](residual-countermodels.csv) |23 numerical same-phase ambiguity examples, explicitly unvalidated; neither geographic estimates nor accuracy bounds. |
| [native-exports.csv](native-exports.csv) | Existing-state export/log SHA receipts and cap/error/coverage flags. Partial 50 and lock-failed 19 are retained separately in local history; successful retries qualify used results. |
| [native-functions.csv](native-functions.csv) | Exact completed decompilation locators for explicitly addressed functions; static VA/RVA domains. Capped instruction windows are disclosed, not mistaken for capped full decompilation. |

## Reproduction and tool effects

Use installed CPython 3.14 at
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`, with `-B`.
Bare `python` resolves to an inaccessible WindowsApps shim on this host.
No package installation or build-time download is needed. New tools and tests
are original stdlib/project code; each module documents reads/writes/prerequisites.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B -m unittest discover -s save-analysis/scripts -p 'test_*.py'
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/audit_saved_world_context.py --samples .local-work/durable-center/static-exhaustion-01/results.json --source-map .local-work/static-exhaustion/context-source-map.json --before .local-work/durable-center/static-exhaustion-01/before.json --esm 'C:/Program Files (x86)/Steam/steamapps/common/Starfield/Data/Starfield.esm' --output .local-work/static-exhaustion/saved-context-NEW
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B save-analysis/scripts/audit_saved_center_frame.py --samples .local-work/durable-center/static-exhaustion-01/results.json --components .local-work/static-exhaustion/saved-context-04/saved-world-components.csv --descriptors .local-work/static-exhaustion/saved-context-04/saved-world-descriptors.csv --output .local-work/static-exhaustion/saved-center-frame-NEW
```

Replace NEW with an unused simple output name; tools reject existing directories.
World audit redecodes only explicitly mapped archived sources, requires frozen
source/decoded hashes and the pinned ESM hash, directly walks PNDT GNAM, and
checks originals before/after. Center audit reads these qualified receipts only;
it does not establish their native semantics by passing its own comparison.
`audit_static_exhaustion.py` compares frozen extraction with the separate manual
network; identities and exact input paths/hashes are retained in
`.local-work/static-exhaustion/independent-body-01/receipt.json`.

Pure `planet_world_key.py`, `saved_world_components.py` and `residual_ambiguity.py`
perform no I/O. Tests cover packing/envelope bounds/legacy token width,
ambiguous or unterminated component runs/body mismatches, selected frame,
negative floor/seams/disabled rejection and same-phase countermodels. They do not
execute native code or validate continuous geography.

Existing Ghidra/JDK launcher `ghidra/scripts/Invoke-OutpostRecon.ps1` reads the
existing pinned database with `-readOnly -noanalysis`, Xmx2G. `OutpostRecon.java`
adds original existing-function inventory, symbol/data windows and literal-offset
censuses. It creates a new report only; no analysis/symbol/type/comment changes.
Full decompilation timeout 30 seconds, full character cap 250k (ordinary 50k),
instruction window 600; refall4096, symbol 256, per-call 12 selectors. These are
output protections; a relevant capped edge was rerun or otherwise qualified.
Whole literal census examined 14,392,060 existing instructions, with uncancelled
receipts. Literal offsets are candidates, not whole-program typed alias proofs.
After the preserved export 19 lock failure, its successful retry and subsequent
opens waited for the preceding job to exit. Final database hashing follows all
job exits. Export 50's invalid range failed after a partial first inventory;
retry 50 qualifies the intended ranges. Neither failure is a scientific blocker.

## Validation and preserved working base

Actual offline test run: **121 tests passed**. Fresh corpus checks: 23 saves,
128 selected prefixes, 19 mature zero compensation vectors, seven no-action
pairs, nine terrain snapshots, 41 angular rows with maximum errors
8.881784197001252e-16 longitude /3.3306690738754696e-16 latitude radians.
These are discrete-pair reproduction errors, not continuous center accuracy.
The successful fresh observer verification checks 5265 archived files; a first
attempt's volatile scratch conflict is preserved, not hidden or called evidence.
Six-save context audit: 111 descriptors/38 bodies and 724 local-only component rows;
five component-qualified samples cover 28 selected object parents. Frame audit:
25 beacon rows, two disabled, two controlled cross-save identities invariant;
independent active mature body/system matches 17/17.
Final frame run 03 additionally rejects unsupported saved-frame flags and any
site/component body disagreement. It reproduces the run 02 selected frame and
countermodel tables byte-for-byte; all 121 tests pass after the guard change.

The [local verification receipt](../../../.local-work/static-exhaustion/review/verification.json)
records protected before/after content hashes, metadata changes, Git HEAD/index
checks, C:/D:free-space, source/tool identities, link/whitespace results and file
manifest. Ghidra index timestamp churn is separated from byte changes. The
baseline snapshots 28 prior authored files; earlier activated-grid report/tables
and tools, and both supplied briefs, are preserved byte-for-byte. Shared research
registers gain new entries without rewriting older evidence.

Final verification: 41 protected files, **zero byte changes**, four Ghidra index
files with timestamp-only changes; all 5265 archived observer files and the
separate imported executable also pass their final hash checks. Internal links, tracked diff check and authored
new-file whitespace pass. HEAD/index unchanged. C: 87,030,018,048 and
D: 139,845,558,272 bytes free at the check, both above 40 billion. The full manifest
has 52 files; 34 changed in this continuation and 18 prior files are byte-identical.
There are 69 export TSVs (one retained partial script-error output) and 170 selected
completed function locators. These counts describe evidence coverage, not a
function-count stopping criterion.

Full review artifacts, including new files:

- [Complete diff](../../../.local-work/static-exhaustion/review/complete.diff), against HEAD plus all untracked files, including the supplied briefs and prior EXP0019 work.
- [Continuation-only diff](../../../.local-work/static-exhaustion/review/continuation-only.diff), against the saved working base for prior files and HEAD for newly modified tracked files; supplied briefs unchanged.
- [Changed-file manifest](../../../.local-work/static-exhaustion/review/changed-files.json), full paths, hashes and whether this continuation changed each file.
- [Actual Git status](../../../.local-work/static-exhaustion/review/status.txt).

New continuation source modules/tests are `audit_static_exhaustion.py`,
`test_static_exhaustion.py`, `planet_world_key.py`, `test_planet_world_key.py`,
`saved_world_components.py`, `test_saved_world_components.py`,
`audit_saved_world_context.py`, `audit_saved_center_frame.py`,
`test_saved_center_frame.py`, `residual_ambiguity.py`, `test_residual_ambiguity.py`.
`OutpostRecon.java` is modified. The main report and this directory are new;
CREDITS and the decision, permission, provenance, research-state, source,
function, hypothesis, finding and state registers gain EXP0020 entries.
The manifest/diffs are the exhaustive file listing, including the earlier base.

## Review boundary

All investigated relevant ledger entries have terminal dispositions. Scope
exclusions and reopened historical interpretations are explicit; no universal
function absence, exact future runtime frame, whole-save decoding, exact off-grid
embedding, metric error, authoritative ownership or mod integration claim.
No new third-party incorporation/permission issue or external disclosure arose.
Critical review is still required; future acquisition must have its own finite
authorization. Suggested commit subject only, if later approved:

```text
research: exhaust activated-overlay and continuous-coordinate static paths
```
