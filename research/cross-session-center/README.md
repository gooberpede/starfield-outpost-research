# Cross-session scientific verifier

Original project code, GPL-3.0-or-later. [Question and authority](../../docs/experiments/cross-session-center/report.md).
Independent native Event decoding uses CPython standard library only. Existing
project `save-analysis/scripts/stream_save.py` supplies BCPS decompression; it is
reused with provenance, not silently presented as an independent save parser.

From the repository root, using installed CPython 3.14.3:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -m unittest discover -s research/cross-session-center -p 'test_*.py' -v
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' research/cross-session-center/verify.py --output .local-work/cross-session-center/verification-NEW
```

Prerequisites: both original sealed sessions, selected 050/060 build manifests
and unchanged source inputs, existing saved-audit/saved-fields ledger and archived
Save25/26; installed executable accessible for read-only hashing. The verifier
fails closed if any expected hashes/record extents/identity checks disagree and
requires caller-available free space >=40,000,000,000 bytes on C:/D:.

Reads: original raw/journals, source/build/seal metadata, existing owned saved
reader, archived saves, installed executable bytes, module receipts. Writes:
only a new output directory with summary/selected ledger/pins JSON, plus exclusive
temporary decompression scratch removed by the reader. Stdlib tests create only
in-memory synthetic records. No native execution, network, target memory,
save modification, observer build, configuration or database mutation.

Limits: hardcoded candidate pointers apply only to the pinned 060 session;
later coherent ExtraWorkshop observations validate their sampled association,
not continuous lifetime. A saved numeric match is not a remapping proof. Original
capture field sampling is non-atomic. Header sequence orders emission, not native
stores across threads. Before-output buffers are not center results. Source/build
integrity and passing adverse tests cannot prove behavioral noninterference.
Raw output stays ignored/local; selected authored tables require review.
