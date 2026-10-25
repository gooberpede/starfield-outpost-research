# Discovery boundaries, dependencies and ownership

[Report](report.md), [scope amendment](scope-amendment.md),
[directory inventory](directory-inventory.csv), [research areas](research-areas.csv).

The observed namespace is the complete `.local-work/` tree, not the 93,334-pin
historical subset. Inventory03 records paths, directories, sizes, file identities,
hardlink counts, extensions and prior-pin overlap without hashing all payloads.
It is a traversal observation, not an atomic filesystem snapshot. No omissions
were reported. Current original data were not moved or normalized.

Ordinary allocation is estimated by rounding logical bytes to 4,096-byte clusters:
49,001,279,488 bytes for the frozen estate. No compressed/sparse attributes were
observed. This is not exact occupied disk: resident MFT data can make small-file
rounding overestimate; hardlinks double-count four fixture names; directory/MFT,
ADS, security and filesystem metadata are omitted. Actual recovery requires a
future free-space measurement, not subtraction of logical byte totals alone.

Thematic grouping is provisional. Direct authored path references and source
records supply linked IDs and provenance; an ID anywhere in a linked document
is not automatic membership of all its files. Each area contains mixed primary,
critical, derived, working and diagnostic roles. Missing per-member semantics,
active reuse and ownership remain UNKNOWN. The present Stage A workspace is
known active; elapsed age does not establish that anything else is inactive.

## Central ownership and meaningful shared inputs

The candidate-owner SQLite and compact CSVs assign every eligible path to one
system archive in each scheme, or give an explicit held/loose reason. These are
proposals, not approved production manifests. An archive may serve many briefs;
an original path is retained in the master index with hash, length, version,
owner/member locator and provenance. Shared use adds references, never a second
archive payload. Exact duplicate aliases need authenticated byte equality first.

`manual-S0-S7C` is shared controlled research, not exclusively storage evidence:
`research/e1-extractors/verify-production.py` directly reads its manifest.
Historical inventory scans serve limits, storage, construction and resource
research. Their analytical indexes stay eligible; saved/decoded payloads are held.
The `recon` exports are shared native sources; they have a methods owner and
cross-system references, not a copy in every system.

Crash dumps under `exp0002a-adapter-0.1.3` are specifically documented primary
observations in the evidence index. A diagnostic basename does not make them
regenerable. `disappearing-deposits` joins resources/production with identity
references. The `c2-transit`/`c2-transport`, `p1-*`, `q030`/native-oracle and
ship-relocation families are grouped by subsystem rather than folder count.

## Compatibility routes

| Consumer class | Current behavior | Required future treatment |
|---|---|---|
| Python/PowerShell readers of absolute or constructed local paths | Open loose files and manifests directly | Explicit locator adapter or controlled extraction to an approved root; qualify unchanged expected inputs |
| Save-derived analytical readers | Consume corpus indexes and derived tables | Keep research receipts resolvable; do not bring held saved payloads into this task |
| Native exports, old debugger/tool evidence | Read native TSV/binary/log inputs at fixed paths | Authenticate selected member bytes; original tool/database dependencies may need loose retention |
| Full preservation and save-protection helpers | Compare protected names and expected bytes | Keep current behavior until separately approved; an archive receipt is not active-save readiness |
| Review exporters and evidence links | Refer to old paths and frozen hashes | Preserve original locators/version records; new archive references must be explicit |
| Unknown/dynamic/external consumers | Not exhaustively visible to literal scanning | HOLD the affected cutover until discovered and tested |

The 52,741 mention rows remain local. The authored table groups them by research
area and consumer class, with example source/line anchors. It deliberately does
not publish a bulk path corpus or equate prose mentions with actual I/O. Exact
legacy read examples include E1's manual manifest, L1/SD1/SD2/SD3/BM1's historical
scan-01 inventory, and D1/E3's scan-04 inventory. No consumer is rewritten here.

## Preserved discovery failures

The first traversal used Windows `DirEntry.stat`, which returned zero identity
fields; its claim of one unique object is invalid and superseded. A retry using
`Path.stat` exposed unsigned Windows device identifiers that exceeded SQLite's
signed integer range. Inventory03 stores identity components as text and is the
accepted metadata baseline. Earlier databases/receipts remain unchanged.

An initial source-text check found legacy CRLF versus LF differences. Exact
current bytes are pinned; HEAD text equality is checked allowing only that line
ending representation difference. No source is normalized. A dependency grouping
attempt repeatedly searched the entire path list and was stopped as a diagnosed
algorithmic inefficiency, not a scientific timeout; the cached mapping replacement
completed. Failed method versions are retained locally.

Scope qualification later added 26 `.decoded.bin` streams and the source-documented
`probe-S5.bin` to the raw-save hold. The corrected non-save denominator and all
held classes reconcile to the same frozen whole estate. Initial pre-amendment
tables and suspended save work remain local historical derivatives.
