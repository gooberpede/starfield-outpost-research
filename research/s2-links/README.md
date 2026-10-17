# S2 bounded offline evidence aids

[Contract](../../docs/experiments/local-output-links/contract.md),
[report](../../docs/experiments/local-output-links/report.md).
Original GPL-3.0-or-later code; reuses project-owned S1/E1-E3/P1 readers and
methods under standing maintainer scope. Standard library only, no added dependency.

Use the installed CPython executable with `-B` from repository root. All inputs
must already exist and match recorded pins. Run names are fresh alphanumeric
labels; receipts are exclusively created under ignored `.local-work/s2-links/`.
Both-drive caller-available40GB guards apply. No source/input/save/configuration/
Ghidra database/Git mutation, game/process access, native invocation or network.

- `saved_examples.py --run saved01`: reads the pinned S1 saved05/E3 HIST-0036
  receipts and their original, redecodes to cleaned scratch, verifies the supported
  edge envelope and 18 fixed inventory/owner/producer joins; writes local JSON.
  Does not expand inventory grammar or provide a generalized inventory extractor.
- `verify.py --run verification01 --tables`: reads protected baseline and receipts,
  pins evidence, checks fixed scalar examples and native locators, runs four
  existing framing regressions, rehashes protected inputs. Writes ignored JSON
  and optional source/function metadata CSVs. These checks establish evidence
  binding/arithmetic/reader integrity, not runtime realization.

Read-only native exports use unchanged `ghidra/scripts/Invoke-OutpostRecon.ps1`
and `OutpostRecon.java`, Ghidra12.1.2/JDK21, readOnly/noanalysis. Commands/logs
and proprietary exports remain ignored. Failed instruction-window guesses and
partial exports are retained; machine spans must exist before being cited.
No analysis symbols/types/comments are changed.

Local initialization/review helpers are adaptations of the owned S1 package
helpers; source paths/hashes and effects are in package receipts. They read
HEAD/index/text, write only ignored patches/manifests and disposable D:/tools
trees, and verify exact forward/reverse application. No working-tree Git apply,
staging, ref changes or publication follows. Existing starting untracked S1 text
validator files are byte-preserved and excluded from task-only changes.
