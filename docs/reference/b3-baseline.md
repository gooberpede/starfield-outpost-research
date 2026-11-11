# Primary investigated game baseline

2026-10-21. **One native/definition research baseline: Starfield.exe 1.16.244.0.**
This populated documentary manifest follows the
[B3 correction](../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_B3_source_completeness_reproducibility_baseline.md`).
Older save creation metadata is not a second analyzed executable.
Research release ID/tag remains TBD; publication **NOT CLEARED**.

| Item | Identity and provenance |
|---|---|
| Executable | Starfield.exe; retail resource version 1.16.244.0 reported by coordinate-sufficiency provenance and repeatedly byte-pinned by later studies; 102,476,200 bytes |
| EXE SHA-256 | `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28` |
| Main ESM | Starfield.esm; 1,457,098,709 bytes; SHA-256 `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`; independently pinned data identity, not a guessed ESM product version |
| Preferred image base | `0x140000000`; existing native export metadata and B2 notation; no new PE/native investigation |
| B3 verification | Existing LO1 protected pins independently rehashed before work: EXE/ESM/Misc.ba2/development ZIP/Interface.ba2 and protected analysis/screenshots; exact scope in local baseline and review receipts |
| Existing-only identities | Localization.ba2, PlanetData.ba2, SFBGS00D.esm and Papyrus archive members use existing verified source ledgers; not freshly hashed/extracted by B3 |
| Load/configuration limits | Exact historical winning overrides, loaded modules and effective settings are claim/session-specific or UNKNOWN; a common EXE hash does not establish them |

[Structured input manifest](../../research/evidence-data/publication-readiness-b3/baseline-inputs.csv) identifies eight installed
inputs, eight Papyrus declaration members and three separately pinned SWF
derivatives, their exact bytes/hashes and
verification distinction. It links original source ledgers; no executable,
archive, ESM or script member is supplied. The installed add-on is not assigned a
fabricated release/build version. The existing SD3/LO1 reports separately identify
LocationsPage SWF/ABC metadata; those local derived members are not a new game
baseline. Their exact source/member pins remain in the cited source ledgers and
the per-method dependency inventory. No Ghidra, xEdit or game program was run.

| Existing semantic identity | Version-specific locator and domain | Controlling evidence |
|---|---|---|
| SOR-FN-0060: AreaResources producer/row binder | Preferred static VAs `0x141578500` / `0x141581290`; RVAs `0x01578500` / `0x01581290` | [Function register](../function-register.md), [availability register](../experiments/native-availability-map/functions.csv) and source-pinned native reports |
| SOR-FN-0061: source updater | Preferred static VA `0x1421e07d0`, RVA `0x021e07d0`; placement/established callers retain their separate VAs | Same register; [output contract](../experiments/native-availability-map/output-contract.md) |
| C3 fuel readiness/charge | Preferred static VA `0x140f7d120`, RVA `0x00f7d120`; mode 0 and mode 1 are different consumers | [C3 native](../experiments/cargo-links/fuel/native.md), [function rows](../experiments/cargo-links/fuel/functions.csv) |
| SOR-ST-0031: source collections/producer objects | Runtime-derived collections versus persisted Workshop producer rows; no universal serialized address | [State register](../state-register.md), [availability schema](../experiments/resource-availability/schema.md) |
| SD1 item interface | Vtable **byte offset** `0x130`; distinct menu object members `+0x4C8`, `+0xD68`, `+0xD70` | [B2 notation](notation.md), [SD1 native](../experiments/containers-displays/native.md) |
| L2 budget functions | Existing preferred-VA/RVA/source hash/range rows; no fresh census or remapping | [L2 function register](../experiments/build-budget/functions.csv) |

These are significant existing aliases and illustrative maintenance joins, not
new function discoveries. All addresses/fields remain bound to the pinned EXE.
RVA = preferred VA minus `0x140000000`; a runtime pointer additionally needs the
loaded base and epoch. A vtable displacement is not an object member or slot
index. Physical ESM/save-file offsets, decoded-stream/record-relative offsets,
SWF offsets and ABC byte offsets each keep their own origin. FormIDs, handles,
saved tokens and pointers are not interchangeable. Local nNNN labels need their
experiment namespace under the [B2 export-ID guide](native-export-ids.md).

| Saved evidence stratum | Creation-version evidence | Originating EXE hash / compatibility limit |
|---|---|---|
| Coordinate Save37–39 | Supported format 27 / buffer 153, embedded 1.16.244.0, reported contemporary controlled inputs | Originating executable hash not established solely by metadata; native analysis uses the single EXE above. [Exact evidence](../experiments/coordinate-sufficiency/evidence.md) |
| Mature HIST collection / Save52 | Mixed historical saves; per-file metadata and hashes in original inventory; no universal creation version assigned | UNKNOWN at this summary level; do not infer shared chronology, loaded authority or native cross-version research. [Inventory](../experiments/historical-save-inventory-triage.md) |
| Launch-era donor TDX1798, 111 files | Both embedded version strings are 1.7.23.0 in all 111; observed metadata, not measured originating binaries | Originating EXE hash UNKNOWN; scoped syntactic observations only, donor rights remain separate. [Report and manifest](../experiments/launch-era-third-party-save-corpus.md) |
| Other first-party/manual controls | Per-sample manifests govern; unestablished creation version UNKNOWN | Filename numbers/header format words do not identify an executable or native layout |

Later executable qualification/crosswalk work is explicitly deferred to a new
update brief under [B0 version policy](../audits/README.md#archive-lookup) (`audits.zip :: docs/audits/publication-readiness-b0/versioned-baselines.md`).
No historical address, object layout or evidence verdict is transferred to another
build by this manifest. B4/B6 and maintainer approval remain separate gates.
