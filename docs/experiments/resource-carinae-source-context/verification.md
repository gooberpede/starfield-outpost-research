# C2B verification, failures and reproduction

[Report](report.md), [source pins](sources.csv), [review matrix](review.md).
Run from repository root with installed CPython 3.14, `-B` and no `-O`.
Use new output names; existing artifacts are never overwritten.

```powershell
$c2bPython = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $c2bPython -B research/resource-installed-settings/replay.py --settings .local-work/resource-installed-settings/settings01.json --output .local-work/resource-installed-settings/c2b-replay01.json --geometry .local-work/resource-installed-settings/c2b-geometry01.json
& $c2bPython -B research/resource-carinae-source-context/investigate.py --output .local-work/resource-carinae-source-context/investigation02.json --geometry .local-work/resource-carinae-source-context/site-frame-geometry02.json
& $c2bPython -B -m unittest discover -s research/resource-installed-settings -v
& $c2bPython -B -m unittest discover -s research/resource-geometry -v
& $c2bPython -B -m unittest discover -s research/resource-carinae-source-context -v
& $c2bPython -B research/resource-carinae-source-context/build.py --name build06
& $c2bPython -B research/resource-carinae-source-context/qualify.py --build .local-work/resource-carinae-source-context/build06 --output .local-work/resource-carinae-source-context/qualification06
& $c2bPython -B research/editorial/screen.py --changed
```

| Check | Actual result and limit |
|---|---|
| Original native receipts | 2587 SRO1/ACK pairs agree with events; three main-file-qualified accepted resources share the concrete Workshop/updater/transfer join. Original geometry comparison gives 0/0/0 matches; no census claim. |
| Unchanged replay | Baseline populations regenerate exactly: Feynman 156, Carinae 895. Installed replay preserves four exact native Feynman paths and three chance-stage comparisons. |
| Finite frame counterfactual | Four complete site-frame candidate sources generate 849 paths: Iron 234, Alkanes 484, Rothicite 131. Zero full/XYW matches, including the separately labelled (900,800) conditional consumer projection. Other historical contexts NOT TESTED. |
| Settings regressions | 15 tests PASS, including active mask 4, inactive mask 8, nonfinite/unknown rejection, unchanged populations, four exact paths and three chance controls. No skips. |
| Shared geometry regressions | 24 tests PASS; no shared algorithm/context/resolver edits. |
| C2B contract tests | Four tests PASS: exact corpus-disposition gate, coherent binary32 frame projection, three-resource transfer requirement, truncated/lost receipt and bad ACK rejection/exclusive receipt write. |
| Debugger fixture suite | 42 cases PASS on the final qualified build. Includes wrong Workshop/source, source-slot reuse, partial/budget/corrupt reads, maximum geometry, nested/thread lifetimes, short-circuit, stale updater transfer, no-hit/retained-cache, rejected ACK, guard LOSS and crash before/after evidence. These are synthetic transport/identity tests. |
| New reader unit controls | Synthetic memory reader rejects changed second copy, partial copy, wrong wrapper and wrong ProcGen. Two different unobservable producer histories with identical consumer bytes yield identical snapshots and null history; no stale-producer detector is claimed. |
| Input protection | All 12973 present entries match prior pins; one historical exitsave is absent. The later 12974-entry task-start audit has zero further changes. Save52 and independent master match the original hash. Added exitsave and absent historical exitsave are separately recorded; no restored/deleted/rewritten save. |
| Current corpus and Steam | Live and historical backup each contain 271 files; one exitsave basename differs. All shared files agree. Historical backup equals original protected inventory. Steam remote/cache equals its pinned historical namespace. No current Cloud-disabled state inferred from hashes. |
| Future admission refusal | Actual offline preflight persisted full protected/Steam/corpus diagnostics and refused the missing explicit disposition, before supplemental backup or Save52 scratch copy. No Phase B admission receipt was produced. |
| Retail operations | NOT TESTED / NOT AUTHORIZED. No game launch, attachment, breakpoint, termination, forced generation, save/config edit or restoration in this assignment. |

## Preserved defects and corrections

The first strict old-protection-list audit stopped at the missing exitsave;
the corrected diagnostic records missing files without overwriting/restoring
them. A full current save inventory then identified the added exitsave; equal
file counts had hidden the rotation. The future gate requires explicit exact
corpus acceptance and an independent supplemental backup before launch.
No historical expected hash or protection rule was silently replaced.

The first C1H replay invocation used the new task output folder and was refused
by the inherited output-root guard. The successful invocation uses the existing
authorized installed-settings output root. The first alternative replay omitted
the shared native constants table and returned UNKNOWN; the corrected version
merges both pinned tables exactly as the qualified C1H replay does. The unchanged
algorithm was not modified to mask either diagnostic.

Independent review identified that unaligned numeric equality alone did not
test a coherent frame change. The corrected second investigation adds the fixed
previously evidenced (900,800) native-to-site binary32 projection as a separate
conditional spatial comparison; it still fails all three matches. Earlier
investigation01/builds/qualifications and diagnostics remain local. A sibling
Git read initially failed ownership checking; per-command read-only
`safe.directory` supplied the exact path without changing configuration.

The audit, checks and full derived geometries are under
`.local-work/resource-carinae-source-context/`; source pins bind their actual
bytes. [Editorial finalization](editorial-finalization.md) records whole-prose
coverage separately from tests. [Review](review.md) records the original AC1–AC8,
actual independent disposition and delivery manifests. Neither scientific
validity nor synthetic readiness grants retail execution or publication authority.
