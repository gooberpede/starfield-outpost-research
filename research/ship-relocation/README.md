# Offline ship relocation audit

Original stdlib/project-only analysis; source-informed provenance is recorded in
[the report](../../docs/experiments/ship-relocation/report.md). Reads explicit
archived 040 raw/journal/ready files and unchanged extracted saved inputs/frozen
predictions. Writes stdout only. Requires installed CPython and project readers;
no install, build, game, native call, database or save write. Both-drive 40 GB
caller-available guard is inherited from the qualified project reader.

Run from repository root using the installed real Python executable:

```powershell
& 'C:\Users\User\AppData\Local\Python\pythoncore-3.14-64\python.exe' research/ship-relocation/audit.py .local-work/native-oracle-live/session-36756-82447437
& 'C:\Users\User\AppData\Local\Python\pythoncore-3.14-64\python.exe' -m unittest discover -s research/ship-relocation -v
```

Redirect/capture stdout as bytes into a **new** ignored local receipt. Never
overwrite originals. The audit checks every frozen row's source/identity,
center bits and cell, then reports nonzero/negative/carry operands separately
from the single observed native zero-offset marker component. It neither proves
native nonzero behavior nor builds an observer.

`marker_keywords.py <Starfield.esm>` separately verifies the pinned installed
ESM before/after, walks FURN/KYWD headers, and reports selected marker keywords.
Its stdout includes identity fields only; no raw assets are copied into Git.
Native global keyword binding and runtime winning override remain separate.
