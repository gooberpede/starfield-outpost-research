# Offline Workshop caller chronology

Original project work, GPL-3.0-or-later. [Scientific report](../../docs/experiments/workshop-caller-semantics/report.md).
Uses installed CPython3.14.3 and standard library only; conceptually extends
owned `research/cross-session-center/verify.py` and imports its independent
schema decoder/journal validation. Save replay reuses owned
`save-analysis/scripts/stream_save.py` for decompression, with that limitation
explicit. Native source informs interpretations, not a clean-room claim.

Run from repository root, with unused output names:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' research/cross-session-center/verify.py --output .local-work/workshop-caller-semantics/replay-NEW
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' research/workshop-caller-semantics/chronology.py --output .local-work/workshop-caller-semantics/chronology-NEW
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -m unittest discover -s research/workshop-caller-semantics -p 'test_*.py' -v
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -m unittest discover -s research/cross-session-center -p 'test_*.py' -v
```

Prerequisites: sealed050/060 sessions and original manifests at the paths defined
in the cross-session verifier, source/build pins, archived Save25/26 and installed
executable read access. Both drives must retain40,000,000,000 caller-available
bytes. The tool reads events/journals/ready/retired/operator marks/ACK/checkpoint
requests and hashes inputs. It writes only a new derivative directory:
events.csv (all center before/return metadata), bins.csv (five-second counts),
summary.json (pooled/per-thread intervals, brackets, action-prefix counts, pins).
No game launch/process read, native execution, database edit, save/configuration
write, network or dependency installation. Tests operate on synthetic timing data.

Reproduction compares semantic output (events/bins/groups/pooled/action marks)
byte-for-byte; free-space values are expected to change. Existing files are never
overwritten by the analyzer. Raw/private derivatives remain ignored and local.
No UTC normalization is invented for060. Parent0 does not identify native callers;
pooled intervals do not measure frame cadence; brackets include instrumentation.
Counts of incoherent samples remain distinct from four-pair arithmetic quarantine.
