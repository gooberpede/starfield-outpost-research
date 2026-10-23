# Reproduction, controls and preserved failures

[Report](report.md), [sources](sources.md), [frozen acceptance matrix](review.md).
Run from repository root with the installed Python interpreter:
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`.
All commands below are offline and use existing stdlib/project methods only.

```powershell
python -B research/resource-installed-settings/settings.py --output .local-work/resource-installed-settings/settings-reproduction.json
python -B research/resource-installed-settings/replay.py --settings .local-work/resource-installed-settings/settings01.json --output .local-work/resource-installed-settings/replay-reproduction.json --geometry .local-work/resource-installed-settings/geometry-reproduction.json
python -B -m unittest discover -s research/resource-installed-settings -v
python -B -m unittest discover -s research/editorial -v
python -B -m unittest discover -s research/resource-geometry -v
python -B -m unittest discover -s research/resource-generation-ancestry -v
python -B -m unittest discover -s save-analysis/scripts -p test_resource_spatial.py -v
python -B research/editorial/screen.py --changed
```

Use fresh output filenames; analytical scripts reject existing outputs. A fresh
settings audit is semantically identical, but replay input-path pins change if
a differently named settings file is supplied. Compare the complete generated
geometry and numerical fields rather than claiming byte identity for differently
named provenance records. No target, debugger or Creation Kit is needed.

## Executed verification

| Check | Result and evidence |
|---|---|
| Original C1H settings/replay suite | 15 tests PASS. Synthetic parser identity, name/DATA length, binary32, six rarity/mask domains, nonfinite/unknown rejection, baseline and actual-corpus regression controls. |
| Editorial suite | 8 tests PASS, including seven defective and seven valid technical examples, changed-line isolation, reasoned suppression, links, fences, CSV fields and Python explanatory-text selection. |
| Existing RG1 geometry/context | 24 tests PASS; no evaluator code changed. |
| Existing C1F discrimination | 1 test PASS; flipped point/bound bits, resource identity and point order fail the exact-match oracle. |
| Existing area-consumer suite | 12 tests PASS, including binary32 boundary, height, count and UNKNOWN controls. |
| Total executed unit/regression tests | **60 PASS**, zero skips. The original five-suite run passed 59; the expanded editorial suite passed 8 after adding the CSV regression. Raw command/exit/log hashes are in local `tests02.json`, individual `*-tests02.txt` logs and `editorial-tests03.json`. |
| Complete frozen regeneration | All 156 Feynman and 895 Carinae resource/source/cell/ordered-point/native-bound entries reproduce before installed resolution. |
| Native equality | All four C1E accepted resource paths match uniquely; three C1G joined weight/draw/threshold/edge comparisons agree bit-exactly. |
| Negative/coverage controls | Copper survives; no extra IL at (11, 1); two exact membership replacements; all resources recomputed under full competition; Carinae unchanged. |
| Preservation | 7644 pre-task protected path hashes retained in local `protected-before.json`; post-task receipt checks every pin and unchanged HEAD/index. Existing source predictions, captures, protected saves/backups and definitions are included. |

The corpus tests depend on local proprietary inputs; synthetic tests alone
cannot substitute for them. The seven valid fixture examples demonstrate bounded
false-positive avoidance, not universal prose detection. Tests inspect some
private exact bytes; those bytes do not become cleared outputs.

## Failures and corrections retained

The first settings audit failed before output because Python rejected encoding
alias `utf8-sig`. The corrected spelling `utf-8-sig` completed all file scans.
The first replay failed before output because a chance-stop receipt does not
contain the resource-call weight field. The implementation now reads the raw
joined resource-call receipt and checks lifetime/frame/DNAM pointer identity.
It does not invent that missing field on a chance row.

An initial corpus test incorrectly expected one removed/added Feynman entry.
The actual output had two of each, including cell (2, 6), and the 14-test run
failed exactly that expectation. The complete produced delta was inspected;
the corrected test explicitly checks both cells and both resource identities.
No replay output or evaluator was changed to satisfy the test. A resource-warning
from an unclosed witness CSV was corrected with a context manager. These initial
failures are also retained in local `initial-failures.txt` for review.

Independent preparation flagged nonfinite setting acceptance. The parser and
inactive resolver now reject nonfinite or nonnumeric settings, with an added
synthetic regression. This validates input discipline without changing any
pinned finite result. Historical C1F endpoint failures and C1G incomplete
diagnostics remain untouched.

The first editorial screen treated CSV delimiters and identifier columns as prose
punctuation. The checker now parses CSV structure and scans labels/explanatory
fields, with explicit path/hash/ID-column exclusions and a positive/negative
regression. The corrected screen reports no suspects; manual reading still
covers all CSV headers/roles and source locators. No prose was rewritten merely
to suppress these false positives.

The independent reviewer reruns and final exact snapshot/diff checks are recorded
in [review.md](review.md), separately from these implementer results. Scientific
equality, evidence preservation, editorial compliance and publication eligibility
remain distinct outcomes.
