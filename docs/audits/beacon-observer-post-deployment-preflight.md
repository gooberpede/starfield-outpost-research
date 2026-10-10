# SOR-EV-0023 — Observer post-deployment preflight

2026-10-10, Australia/Sydney. SOR-EXP-0016 / SOR-D-0034. Authored report and [operator run card](../experiments/beacon-observer/Save25-operator-run-card.md) REVIEW-REQUIRED; private receipts, binaries, logs and saves LOCAL-ONLY.

**Actual installed file, configuration, output-path, control-helper and available-space checks pass. Live observer readiness remains NOT_OBSERVED.** No Starfield launch was performed. Return this report and run card for review before launch. No substantive implementation defect has been established; no approved observer source, binary, configuration or package was rebuilt, replaced or modified.

## Authority and scope

The user explicitly approves the plugin, reports deployment of SFSE 0.2.21 and SorBeaconObserver-0.1.0.zip to Vortex profile `Starfield - SFSE`, and reports successful startup, Save25 load and normal exit. Those events and the profile name are USER-REPORTED. This task authorizes actual-installation preflight and preparation of a run card, with review before launching. It prohibits rebuilding/replacing/modifying the approved observer and requires substantive changes to return for review. Partial readings, missing optional fields and unexpected values must continue unless there is a genuine instrumentation-integrity or machine-safety failure. Earlier offline/staged-only descriptions are preserved historical records, superseded for deployment status by this report only.

## Direct checks

Receipt time: `2026-10-10T00:49:44.207413+00:00` (11:49:44 AEDT). Game root: `C:\Program Files (x86)\Steam\steamapps\common\Starfield`. No `Starfield.exe` or `sfse_loader.exe` process was found. The actual deployed `Data\SFSE\Plugins` contains the observer DLL/config and Vortex folder marker; its recursive DLL inventory contains only this observer.

| Actual deployed file | SHA-256 |
|---|---|
| `Starfield.exe` | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` |
| `sfse_1_16_244.dll` | `28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b` |
| `sfse_loader.exe` | `16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526` |
| `Data\SFSE\Plugins\SorBeaconObserver.dll` | `0e910a3ec6362adf050add3a9cd754246ac12f25e5ae55426d1c44ed93848a31` |
| `Data\SFSE\Plugins\SorBeaconObserver.config` | `edf6c20d8bff667783467d8ac6094b331355c07adf4c5ee323e923e407033177` |

The deployed observer DLL/config equal both selected review-03 ZIP members and Vortex staged files byte for byte. ZIP hash remains `ecbf7db0330e0c4aa9f94af8bc294fdba9af0517a610e6231327f877cda57f92`. Manifest source hashes still match the approved build. Windows version resources report game `1.16.244.0`, SFSE DLL `0.0.2.21` (SFSE 0.2.21), loader `0.1.1.1`. The local SFSE readme states support for Steam 1.16.244. These match the observer's pinned inputs; loaded-module and code-window checks await a fresh process.

The actual 72-byte config is UTF-8 without BOM, one LF, no CR, containing exactly:

```text
D:\Projects\starfield-outpost-research\.local-work\beacon-observer-live
```

The output root did **not exist before preflight**. No observer sessions, READY records or failure records were available. The available SFSE logs under `C:\Users\User\Documents\My Games\Starfield\SFSE\Logs` predate the reported smoke test: `sfse.txt` last write 2026-10-06 23:28:35 UTC and `sfse_loader.txt` 23:22:21 UTC. They cannot independently establish observer activity during that test. This discrepancy is unresolved, not proof of a plugin defect. A fresh matching READY record is mandatory at the main menu in the proposed run; absence is an instrumentation-readiness issue, not an optional scientific field.

Preflight inspected path ancestors for reparse points, created the configured output root, exclusively wrote/fsynced/read back a non-control probe, then removed that probe. The root is left empty. No actual session/control file was created. This verifies current-account path access, not the future process's loaded observer. The unchanged request helper was exercised only in a separate synthetic session: settled request accepted; duplicate, traversal and unsettled requests refused; STOP accepted. Actual worker polling, request consumption and retirement have not been exercised in this task.

| Volume | Final caller-available bytes | Required minimum | Result |
|---|---:|---:|---|
| C: | 89,898,340,352 | 40,000,000,000 | PASS |
| D: | 140,183,183,360 | 40,000,000,000 | PASS |

These are `GetDiskFreeSpaceExW` available-to-caller values, not total/free estimates from formatted shell output. The guard means 40 billion bytes, not 40 GiB. Unchanged approved code checks both volumes at startup/idle and during output at 64 KiB intervals; a failed query or value below the threshold stops acquisition. Earlier disposable qualification covers exact threshold, one byte below and query failure. This preflight did not fill disks, force an actual low-space event or execute the DLL. Capacity must be rechecked immediately before the reviewed launch; background writers can change it.

## Preservation, outputs and limits

Exact SOR-SAMPLE-0030 Save25 original and frozen archive remain 2,403,744 bytes, SHA-256 `d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5`. Selection uses `.local-work/two-outpost-anchor/exact-beacon-01/manifest.json`, not an ambiguous Save25 glob. Protected installed files, ZIP and both saves were hashed before and after preflight and were identical. No game launch, debugger, deployment, native query, save modification, configuration change, Ghidra execution/edit, dependency download, staging, commit, push or disclosure occurred.

Local original preflight script and receipt: `.local-work/beacon-observer-preflight/post-deploy-01/check.py` and `preflight.json`; isolated helper fixture alongside them. Script reads installed/staged/package/source identities, exact saves, versions, process inventory, log identities, path state and disk capacity; writes its receipt, the isolated fixture and the temporary output probe described above. Dependencies: existing CPython 3.14 stdlib and Windows APIs; no target-process effect. Prior build/test basis: [SOR-EV-0022](../experiments/beacon-observer/README.md). No scientific finding or publication eligibility is promoted. The run card remains proposed until reviewed; the user's smoke-test report and future runtime qualification are separate evidence.
