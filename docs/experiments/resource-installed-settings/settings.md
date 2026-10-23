# Verified installed-settings provenance

[Report](report.md), [exact binary32 ledger](settings-provenance-v1.json),
[source pins](sources.csv), [prior native mapping](../resource-selection-operands/native.md).
Retail 1.16.244.0; preferred static VA base `0x140000000`.
EXE SHA-256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
main ESM SHA-256 `1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.

## Settings and exact defaults

All names begin with `fInactiveResourceChanceMult`. FormIDs below belong to
`Starfield.esm`. Bits are unsigned binary32 words, not memory addresses.
The JSON also records exact float values and little-endian DATA byte sequences.

| Rarity/domain | Initializer static VA | Payload static VA | EXE default bits | Installed bits | GMST FormID | Record-header file offset |
|---|---|---|---|---|---|---|
| Common, 0 | `0x140051240` | `0x145e901b8` | `0x3e99999a` | `0x3e99999a` | `0x002d40c0` | `0x2c27d` |
| Uncommon, 1 | `0x140051270` | `0x145e901d8` | `0x3e4ccccd` | `0x3e4ccccd` | `0x00226b0c` | `0x26c05` |
| Rare, 2 | `0x1400512a0` | `0x145e901f8` | `0x3dcccccd` | `0x3dcccccd` | `0x00226b0e` | `0x26c9b` |
| Exotic, 3 | `0x1400512d0` | `0x145e90218` | `0x3c23d70a` | `0x3d4ccccd` | `0x00226b0d` | `0x26c51` |
| Unique, 4 | `0x140051300` | `0x145e90238` | `0x00000000` | `0x00000000` | `0x002f031c` | `0x2c8e7` |
| Special setting/domain, 5 | `0x140051330` | `0x145e90258` | `0x3e99999a` | `0x3e99999a` | `0x002d40ce` | `0x2c2c7` |

The pinned native `019.request.tsv` lists each constructor's actual constant
load and name. Unique explicitly zeroes XMM2 at preferred static VA
`0x140051304`; it is not a missing record or guessed fallback. Fresh PE reads
verify the other defaults at constant static VAs `0x144f04250`, `0x144f041cc`,
`0x144f040c0` and `0x144f03eec`. The ledger retains their original EXE file
offsets. Defaults are approximately 0.3, 0.2, 0.1, 0.01, 0 and 0.3;
installed Exotic is exactly binary32 0.05000000074505806.

## Resolution, selection and consumers

The bounded reader walks GMST records in all 39 currently installed ESM/ESP/ESL
files, retaining same-name or same-numeric-ID candidates. It validates each main
record's type, FormID, EDID and four DATA bytes. All six candidates belong to the
main ESM. The other plugin files contain no matching name/ID candidate; this is
not a general load-order merger or a claim about plugins not installed here.
The full per-file walk counts and hashes are in the versioned ledger.

The 23 configuration files inspected are root INIs and plugin/load-order lists
under the game directory, Documents/My Games/Starfield and AppData/Local/Starfield.
Their exact paths and hashes are recorded; no setting-name occurrence was found.
Historical configuration, console changes and an INI route for these specific
settings remain UNKNOWN. No default is substituted for missing settings: the
replay requires all six main records and rejects additional candidate overrides.

STATIC native setter/loader anchors remain those verified in C1G settings01–08:
constructor `0x1402d65e0` writes live value at setting-object offset `0x8` and
initial shadow at `0x10`; collection/name lookup `0x1406846f0` and dispatch
`0x1406843d0` feed DATA reader `0x140684160`, which calls float setter
`0x140684b30`. Its write at `0x140684b43` can replace the initializer value.
The separate text-command route at `0x140c228a0` demonstrates mutability;
neither route was executed here. All addresses are build-pinned static VAs.

Ordinary consumer `0x14079b520`, decisive instructions
`0x14079bdad`–`0x14079be20`, uses inactive settings when the low-nibble mask is
8 or rarity exceeds the mask. Otherwise it uses active weight 1. Rarities
0 through 5 select their separate settings; higher ordinary rarity retains zero
on the inactive path. Everywhere processing is a separate branch with weight 1
in the frozen qualified model, even when rarity 6 in an ordinary call would
receive zero. No selected Special branch occurs in these two source sets.

Cell chance is DNAM block offset `0x1c`, block stride `0x28`, indexed by rarity
plus 7. The native first gate multiplies that chance by the effective weight;
it does not replace the RSGD Cell chance with a GMST value. Mask, rarity, branch,
Cell chance and default/installed weight bits remain separate output fields.
C1G directly observes selected new-epoch weights and comparisons; it supplies
no complete historical winning-setting or RSGD-identity audit.
