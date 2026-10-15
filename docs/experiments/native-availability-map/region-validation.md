# Resource-region offline qualification and preservation

[Contract](region-contract.md), [report](region-dependencies.md),
[review](region-review.md). Receipts are ignored LOCAL-ONLY artifacts.

## Qualification actually executed

Installed `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`
(CPython 3.14.3), stdlib/project-owned modules only, no downloads.

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/native-availability-map/verify.py --run region-dependencies01
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/native-availability-map/verify-region-dependencies.py --run checks01
```

Results: **66 native records / 26 source pins / 16 existing instruction contracts
PASS**; **45 availability + 12 spatial tests PASS**; **eight focused lifecycle
assertion groups / 12 additional source pins PASS**. Receipts:
`.local-work/native-availability-map/region-dependencies01.json` and
`.local-work/resource-region-dependencies/checks01.json`. These validate metadata,
source transcriptions and existing conditional evaluators. They do not execute
native code, establish remote/local sufficiency, or validate complete upstream
geometry. The existing 35,574 evaluations / 11,128 descriptors / 346 UI-fold
counts are inherited qualified runtime evidence; this assignment adds no fresh
capture census or independent spatial oracle.

## Focused exports and preservation

Six fresh bounded exports `.local-work/recon/resource-region-dependencies-01.tsv`
through `06.tsv` completed with `DECOMPILED true` for the requested existing
functions and no ERROR in adjacent logs. Exact commands are preserved in those
logs and `.local-work/resource-region-dependencies/exports.json`; content pins
are in [region-sources.csv](region-sources.csv). They use existing
Ghidra 12.1.2_PUBLIC / Temurin 21.0.12+8-LTS, wrapper
`ghidra/scripts/Invoke-OutpostRecon.ps1` SHA256
`23849f10be61a17ff681529aae96e12e98f0f5f77b858a0029d36b924ac6d8dc`
and reader `OutpostRecon.java` SHA256
`8faa1330593d3874150b269b3b4b9cf5b5becab9fc35bb003e1d960a61ea65b7`.
Command form:

```powershell
& ghidra/scripts/Invoke-OutpostRecon.ps1 -Target Starfield -OutputName resource-region-dependencies-01.tsv -Addresses @('full:1407a0fa0','full:1407a0bf0','full:1407b5470','full:14078c4e0','full:140985870','full:140478a30','refall:1407b5160','refall:14076c560','refall:14079ddf0','full:14078fc90','full:14078f670','refall:14079df60')
```

The wrapper uses `-readOnly -noanalysis`, writes new ignored exports and tool
settings/cache/logs, and does not request database edits. The exact selector lists
for 02–06 are in `exports.json`, avoiding a second divergent command inventory.
No broad rescan or function-definition/symbol/type/comment change occurred.

Protected-input audit reuses the owned earlier method against the 070 baseline
and seal, adapted only to a separate task-local directory. Before receipt:
`.local-work/resource-region-dependencies/preservation-before.json`: **6,868
pins equal**. C: caller-available 94,245,421,056 bytes; D: 117,985,001,472 bytes,
both above the 40,000,000,000 guard. HEAD
`6475a1fb4a70711d3035e2c89a05085b9b57f5b4`; index SHA256
`0e869b2c4add032b12ff8b2593cf326821b613f78a43efa49a18ca15946b94ca`.
After receipt `preservation-after.json`: **6,868/6,868 pins equal**, same HEAD/index;
C: 94,244,999,168 bytes and D: 117,982,257,152 bytes available. Separate
`ghidra-before.json` / `ghidra-after.json`: **15/15 existing project files
byte-identical**, including analysis and user databases. No original capture, save, binary,
prediction or evidence file was intentionally written or removed.

## Packaging checks

Preserved qualification failures/corrections: initial exporter `review01` stopped
at `git diff --check` for a new blank line at the brief-index EOF; no patch was
emitted. The whitespace correction briefly introduced default-encoding mojibake
in that index, detected by primary diff inspection. Rebuilding that file from
the verified UTF-8 HEAD plus the task's two added lines removed those unrelated
changes. `review02` is superseded; `review03` passed exact reconstruction after
the correction. These are packaging defects, not failed native scientific tests.

Task-only and complete patches use the existing owned exporter adapted locally
from the recorded HEAD, with task-local base/prefix changes. The complete patch
includes the unchanged user-supplied untracked brief; task-only excludes it.
The initial brief-only attribution baseline was corrected after files authored
during the lengthy hash audit appeared in its late untracked snapshot. No user
content was removed or reclassified as task-authored.

The exporter checks Git whitespace, authored new-file LF/BOM/trailing whitespace,
relative Markdown link files, path/content coverage, and exact forward/reverse
apply in disposable D:/tools trees; no working-tree apply, staging or index write.
Its package manifest records all included files/hashes, status, exclusions,
patches/hashes and exact applicability. Ignored raw/native/proprietary evidence,
saves, binaries, Ghidra databases and bulk derivatives stay excluded/local.
The review package identifies actual export revision and reviewer disposition.
