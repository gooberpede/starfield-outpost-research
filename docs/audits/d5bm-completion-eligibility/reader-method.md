# Local verification and reader boundary

The D5BM checkpoint includes **local data checks and prior isolated native
components**. The [D5BJ reader guide](../evidence-reproduction-d5bj/README.md)
defines separate supported reader methods for the bounded numeric, geometry,
dispatch, source and N2 tiers. No runnable Stage A or Stage B native method
has been qualified.

| Local input | SHA-256 |
| --- | --- |
| Starfield.exe 1.16.244.0 | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` |
| Starfield.esm | `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7` |
| Starfield - PlanetData.ba2 | `2fb1fff5d8fc074718bf05022c099f3c87ef70e00050229b368ae7d680fbe5d5` |
| Starfield - DensityMaps.ba2, local candidate | `5e848b813df9a278b0b080f9b14f1b764cc25b9082944049510a652ad626b13b` |
| CPython 3.14.3 interpreter executable | `cce21c0e8710e304273e98ac4b2b0f5aceb639acbcd2343cbaa5c4e81619c45b` |
| Windows UCRT | `3c60056371f82e4744185b6f2fa0c69042b1e78804685944132974dd13f3b6d9` |
| D5AS candidate | `d0d35ed2193527dd8215a647178614a5403e814bf14c3f9d1f0a448c53a1043c` |
| D5BI candidate | `a47bbd302553755d0fe87d746234d0d6c527ee7297cfda2e38915072edb7c3d7` |

The host was AMD64 Windows 10 build 19045, Intel Core i7-10700F and
Git 2.53.0.windows.1. The data-only helpers use the standard library and
owned source readers. The inherited native reader contract also requires the
Windows x64 ABI, the pinned CRT, AVX, FMA3 and enabled SSE/YMM state.
The earlier native component runs used the pinned host preflight. The solo
continuation exercised the data paths. Supply lawful local game files.
These checks start with files already held by the reader.

From a clean source export with the current D5BM sources, run the data-only
first-root projection with explicit reader inputs:

```powershell
& $py -I -B research/resource-retained-population/d5bm_first_root_inputs.py `
    --esm $esm --planet-data $planetData --density-maps $densityMaps
```

The command authenticates those three files, projects the selected
main-file tag rows and archive keys, and writes JSON to stdout. No asset
body is written. It uses the owned C1 source census and exact archive/tag
readers. The [continuation checkpoint](continuation-2026-11-10.md) records
the native component receipts separately.

## Earlier static checkpoint

The local reproduction used Git archive from the pinned HEAD, expanded into
`baseline/` under the private D5BM directory. The export has no
`.local-work/` member. With paths supplied explicitly, the method-level
commands from the project root are:

```powershell
& $py -I -B "$scratch/check_evidence.py" $repo $exe "$scratch/baseline"
& $py -I -B "$scratch/check_density_members.py" "$scratch/baseline" $esm $planetData $densityMaps
& $py -I -B "$scratch/compare_root_neighbor02.py" "$scratch/baseline" $esm
```

The first helper reads the EXE as data, validates the whole-file pin and PE
format before the range checks, and verifies retained D5H and D5BJ local
source/receipt bytes. The second checks the ESM and raster, recomputes the
first density request's candidate source, checks archive bounds and names
and hashes the decoded candidate members and the whole archive. It checks
archive identity for stability within the read. The observed digest and
stem/count selection do not qualify exact DensityMaps mismatch refusal.
The third helper recomputes the two static padded footprints. All emit JSON
to stdout after checks.
No executable memory mapping, game process or debugger is involved.

Local execution evidence for these helpers is under `.local-work/d5bm/`.
`static.stdout.json` SHA-256
`fd9c2d17f9ce4332f85468a902489699e5251d008d6cb9748e5a2f5b706fcb7e`
records 15 image spans across 14 function entries, both PE tables and
24 historical invocation stream pairs. `density02.stdout.json` SHA-256
`ef2c48b610768fe2e517689e49a9ae932a560069a73c880f0d45ccf51d647cce`
records the corrected candidate input check. `root-neighbor02.stdout.json`
SHA-256 `6db5c9b85167ccf048bd0271141ce9d0ed818d82d03693ed92daf47bdda2a716`
records the two distinct static footprints. All three succeeded with empty
stderr. The first density attempt and the first root/neighbor assertion
failure remain separately retained. The wrong-image static control exited 1
at the full EXE hash check before reading PE ranges. The controls do not
qualify native input refusal.

Retained helper SHA-256 values are
`c834c75ce0d88fd7be2f55893c97ddba1b94d328d38018fa59a9b7a1382d61b1`
for `check_evidence.py`,
`95f712dd295bcf8ade4fa9318da48e5039d4315d27885c59b4c91edf0a417ceb`
for `check_density_members.py`, and
`c8b60f21afd13e3e6d4fc0b8d71eace1cffea6db436e776788e626bf6bd13de7`
for `compare_root_neighbor02.py`. These identify the retained scripts.
There was no separate pre-run source seal.

The first local helper requires privately retained sources and streams.
Isolating the authored export does not make those inputs a public route.
The two candidate helpers use exported authored source and explicit local
game files. D5AS compares complete represented geometry and D5BI verifies
projected N2 evidence. Their exact proposed ZIPs were hash-checked locally.
Their file-specific rights/privacy, transfer, retention, B6 and hosting
remain pending. [D5AS](../evidence-access-d5be/d5as.md) ·
[D5BI](../evidence-derivative-d5bi/README.md) · [Reader policy](../../PUBLICATION.md#reader-supplied-game-inputs)
