# Disposable x87 preservation qualification

Original project-owned extension, GPL-3.0-or-later. Governing
[brief](../../docs/implementation-briefs/CODEX_BRIEF_SOR_experiment_A_x87_state_preservation.md),
[report and comparison table](../../docs/experiments/spatial-equivalence-feasibility/x87-preservation/report.md),
[contract and ledger](../../docs/experiments/spatial-equivalence-feasibility/x87-preservation/validation.md).
No retail observer or integration library is created.

Requires the existing Windows x64 AVX-enabled host, MSVC/MASM/Windows SDK and
CPython. No dependency installation or download. From the repository root:

```powershell
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
& $py -B research/x87-preservation/build.py --name my-baseline
& $py -B research/x87-preservation/verify.py .local-work/x87-preservation/my-baseline/minimal/states.bin --expect loss
& $py -B research/x87-preservation/verify.py .local-work/x87-preservation/my-baseline/adversarial/states.bin --expect loss
& $py -B research/x87-preservation/build.py --name my-correction --corrected
& $py -B research/x87-preservation/verify.py .local-work/x87-preservation/my-correction/minimal/states.bin --expect preserved
& $py -B research/x87-preservation/verify.py .local-work/x87-preservation/my-correction/adversarial/states.bin --expect preserved
& $py -B research/internal-observation-qualification/verify.py .local-work/x87-preservation/my-correction/adversarial/geometry.bin
& $py -B -m unittest discover -s save-analysis/scripts -p test_resource_spatial.py
```

`build.py` imports the unchanged owned predecessor's assembly generator and
adapts its native/geometry source in memory with checked replacement counts.
It writes generated source and snapshots into a new exclusive ignored directory,
builds and runs only that directory's fixture, and hashes source/tool/output
bytes in `build.json`. Existing predecessor sources are never written. The
generated `.asm`, MASM listing, `.cpp`, build log and binary images remain local.
The compiler's deprecated GetVersion warning is expected: the fixture reports
that API's packed compatibility value; the Python receipt separately records
Windows version. It is not an authoritative kernel-build measurement.

The fixture patches only its own two terminal sites, adds a process-local VEH,
runs finite authored state/geometry and four-thread controls, holds a handler
in flight during cooperative STOP, joins workers, restores sites, unregisters
and executes unpatched controls. It can fault or abort only its disposable
process; it opens no game/other-process handle, save, Vortex package or database.
No game code is loaded or executed. Unexpected writes beyond the named local
output boundary or protected-input mismatch are stop conditions. Failed runs
are retained; no automatic cleanup is performed.

`verify.py` reads owned `states.bin`, checks framing, actual seeded architecture,
adjacent-save stability, exact meaningful x87 fields, GP/flags/SIMD and restore
provenance, and writes `comparison.json` beside the input. `--expect loss`
expects and explicitly reports required preservation FAIL; a zero decoder exit
means the predicted failure was measured, not that preservation passed.
The unchanged predecessor decoder reads the separate geometry corpus and
checks replay/correspondence plus eight malformed derivatives. Both are stdlib
and owned project imports only; neither modifies its input.

Framing is six little-endian u32 words: magic `0x37385853`, version, sequence,
condition (0 unpatched, 1 minimal, 2 adversarial), mode (0 REJECT, 1 ACCEPT,
2 post-cleanup ACCEPT), and thread ID with child flag in its upper byte. This
host's observed thread IDs fit 24 bits; the stored child flag is not a universal
thread-identity schema. Version 1 contains 5,184 snapshot bytes; version 2 contains
5,696, followed by u32 trailer `0x454e4421`. Frame sizes are 5,212 and 5,724.

Snapshot-relative byte domains: pre GPR/flags/YMM/FXSAVE64 at 0/128/160/704,
post at those offsets plus 1,536; entry FXSAVE64 at 3,072; raw FltSave at 3,584;
duplicate pre FXSAVE64 at 4,096; legacy pre FXSAVE at 4,608; corrected restore
image at 5,120. Its first 512 bytes are meaningful. FXSAVE64 field-relative
offsets are CW 0, SW 2, abridged tag 4, opcode 6, full FIP 8, full FDP 16,
MXCSR 24, and eight 10-byte ST payloads at 32 plus 16 times logical index.
Reserved bytes, six-byte ST padding and software tail are not state comparisons.
Raw representations are retained rather than normalized in place.

`package.py` reads the selected preservation baseline, Git HEAD/index/worktree,
task documents and local evidence. It writes only ignored manifests and both
review diffs, checks all selected pins, links, whitespace and exact patch
forward/reverse reconstruction in disposable text trees. No staging/ref changes.
Its initial baseline receipt was captured before any experiment; its complete
path inventory is the authoritative preservation scope. Do not regenerate that
baseline to hide changes. Retain evidence until maintainer review and an explicit
cleanup decision.
