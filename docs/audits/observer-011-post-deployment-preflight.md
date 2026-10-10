# SOR-EV-0030 — Observer0.1.1 installed preflight

2026-10-10 Australia/Sydney. SOR-EXP-0022 / SOR-D-0041.
**PASS for actual installed-file preflight; return for review before Phase1.**
The approved ZIP, packaged DLL/config, Vortex staging and installed files agree.
Smoke-session startup independently confirms the expected observer loaded and
became ready. No scientific checkpoints were collected in that session; no new
position-oracle comparison is claimed.

[Task scope](../implementation-briefs/observer-011-post-deployment-phase1.md) ·
[Phase1 Save25/26 run card](../experiments/engine-oracle/Phase1-Save25-Save26-operator-run-card.md) ·
[Separate fixed-POI candidate plan](../experiments/engine-oracle/fixed-poi-validation-candidates.md).

## Exact approved deployment identity

The user reports deploying to **`Starfield - SFSE`** and successful game start,
Save25 load, build-mode enter/exit and normal game exit. Those gameplay events
and the profile display name remain USER-REPORTED. Vortex's actual deployment
manifest corroborates source folder `SorBeaconObserver-0.1.1` and
`hardlink_activator`; it does not independently identify the profile display name.

**Approved source ZIP absolute path:**

```text
D:\Projects\starfield-outpost-research\.local-work\beacon-observer-builds\engine-oracle-011-02\SorBeaconObserver-0.1.1.zip
```

[Open the approved ZIP](../../.local-work/beacon-observer-builds/engine-oracle-011-02/SorBeaconObserver-0.1.1.zip).
89,135 bytes; SHA-256:
`9570c9da1b206c6b611e31273e71b5cf84b10e10b6b7fc2e479e7aa1fd445023`.
This is the final `engine-oracle-011-02` package, not the earlier011-01 build or
historical0.1.0 ZIP. This task did not rebuild, replace or repackage it.

| Component | Directly checked identity |
|---|---|
| Packaged and installed DLL | SHA-256 `4ae2a1e329a498b12352f4145db546fdb1317048dced5dede8c16f3fabe30504`, 163,328 bytes |
| DLL exported version | `SFSEPlugin_Version`: dataVersion1, pluginVersion65537 = `0x00010001` = **0.1.1**; name `SOR Beacon Coordinate Observer` |
| Export location | PE export RVA`0x27000`, file offset155136; parsed from bytes without loading the DLL |
| Windows DLL version resource | Absent; exported SFSE metadata is the directly checked plugin version, corroborated by startup record and SFSE log |
| Config | 72 bytes, SHA-256 `edf6c20d8bff667783467d8ac6094b331355c07adf4c5ee323e923e407033177`; UTF-8 without BOM, one LF, no CR |
| Actual installed plugin folder | `C:\Program Files (x86)\Steam\steamapps\common\Starfield\Data\SFSE\Plugins` |
| Vortex staged mod root | `C:\Users\User\AppData\Roaming\Vortex\starfield\mods\SorBeaconObserver-0.1.1` |

Config member `Data/SFSE/Plugins/SorBeaconObserver.config` and the installed
`SorBeaconObserver.config` contain exactly this path followed by one LF:

```text
D:\Projects\starfield-outpost-research\.local-work\beacon-observer-live
```

All **five ZIP members** match staging and installed bytes, including the three
notice/README files. Vortex strips `Data/` from plugin members; root
`ResearchNotices/` members deploy under the game `Data/ResearchNotices/` folder,
as corroborated by `Data/vortex.deployment.starfield-data-folder.json`.
The ZIP CRC/member uniqueness checks pass. All12 source hashes still match the
approved build manifest. Recursive installed plugin DLL inventory contains only
`SorBeaconObserver.dll`; an old0.1.0 staging directory is not evidence it is loaded.

## Executable, SFSE and startup checks

| Actual installed file | Version resource | SHA-256 |
|---|---|---|
| Starfield.exe | 1.16.244.0 | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` |
| sfse_1_16_244.dll | 0.0.2.21 (SFSE0.2.21) | `28c5bda41d9959c885efcb6e889de69e92767c80a1a66842d711d215f722f82b` |
| sfse_loader.exe | 0.1.1.1 | `16916c2ec47e31774e3d550609a1844fcb368b03060c03511891564b7f5f7526` |

Existing smoke evidence: local `session-6936-125088390/ready.json` under the
configured output root, UTC **2026-10-10T10:38:46.543Z** (21:38:46.543 AEDT),
version0.1.1, PID6936, worker TID7068, process creation FILETIME
`0x01dd58a384ee303c`, runtime image base`0x00007ff7e13e0000`, matching game/SFSE/DLL
hashes. Startup has74 module records and `STARTUP_RECORDED`. SFSE's actual
`C:\Users\User\Documents\My Games\Starfield\SFSE\Logs\sfse.txt` records
`SorBeaconObserver.dll ... 00010001 ... loaded correctly`.
This supports smoke-time loader/worker readiness; the historical base/PID/session
must not be reused for Phase1. Startup is not a loaded-save or build-mode capture.

The smoke session has **zero scientific checkpoint directories**, no failure
marker and no retirement marker. Normal game exit is user-reported; no cooperative
STOP was recorded, which is consistent with no request session. At preflight no
Starfield/loader process is present. Windows Toolhelp enumerated258 process
metadata entries with zero matching images, without attaching/opening the target.
Initial `tasklist` was access-denied in this sandbox; the supported metadata
enumeration resolved process absence without elevation. No live process was started.

## Path, control helper, disk and save protection

Preflight time **2026-10-10T10:52:05.288802–10:52:10.815023 UTC**.
Output ancestors have no reparse points. One newly exclusive non-control probe
was written, flushed with fsync, read back and removed from the configured root.
Existing sessions were not used for requests or modified. Nine old request files
belong to the historical0.1.0 capture session; unique labels and fresh session
selection prevent their reuse. No scientific request or STOP was sent to a real
session in this task.

The unchanged helper was exercised only in an isolated synthetic0.1.1 session:
settled request accepted; duplicate, traversal and unsettled requests rejected;
STOP accepted, exact command bytes checked. This does not qualify a new game's
request consumption or capture output; those remain Phase1 readiness checks.

| Volume | Available to caller at final check | Minimum | Result |
|---|---:|---:|---|
| C: | 86,693,048,320 | 40,000,000,000 | PASS |
| D: | 139,764,187,136 | 40,000,000,000 | PASS |

Measured with `GetDiskFreeSpaceExW`; recheck before the reviewed launch. This is
40 billion bytes, not40GiB. No artificial low-space test or disk filling occurred.
Original approved instrumentation checks both volumes and fails closed on query
failure; isolated partial/unreadable scientific fields do not stop independent
collectors. Genuine writer, integrity, runaway-output or machine-safety failures
remain terminal, preserving flushed evidence. No arbitrary tiny capture quota.

Save identities were selected from frozen manifests, not a loose Save25/26 glob:

| Sample | Bytes | Original and archived SHA-256 |
|---|---:|---|
| Save25 | 2,403,744 | `d4df86bc01c2105933fe856a1be5ebbe0c3fc78a4d67fe1a790e18129faf75f5` |
| Save26 | 2,409,024 | `2b4781e75226f2ff7c6aa47470fb47ff179c1754461aa208c46716d7c3935104` |

All **5,298 protected files** have identical before/after hashes, sizes and
modification timestamps: installation/package/build, selected source files,
Vortex deployment metadata/staging, four original/archive saves and all existing
observer-session files. No executable/config/save/profile/observer change occurred.

## Receipts and limits

Local original script and full receipt:
`.local-work/beacon-observer-preflight/post-deploy-011-01/check.py`,
`preflight.json`, `console.txt`, isolated `helper-fixture/`.
Script conceptually/adaptively reuses original project
`post-deploy-01/check.py`, adding0.1.1 PE export, all-member deployment mapping,
startup evidence and Save26 preservation. Existing Python stdlib and Windows
metadata APIs only; no new dependency or third-party implementation. Earlier
failed attempts are retained: tasklist denial; overstrict ZIP `Data/` assumption
corrected against Vortex's actual notice mapping. Neither altered protected inputs.

Working baseline HEAD`2583795c24be903de26e35d62b25e68b1d038f73`, initially clean.
No Ghidra run, game launch/load, debugger, native invocation, deployment, rebuild,
config/save mutation, actual-session command, staging, commit, push or disclosure.
This readiness result supersedes the earlier **deployment-status** description
for0.1.1 only; it does not revise prior scientific evidence classifications.
The [Phase1 card](../experiments/engine-oracle/Phase1-Save25-Save26-operator-run-card.md)
remains **PROPOSED / REVIEW-REQUIRED**. Smoke success is not scientific equivalence
or authorization to start the experiment. Publication eligibility remains separate.

[Complete handoff, diff and check receipts](../experiments/engine-oracle/post-deployment-review.md).
