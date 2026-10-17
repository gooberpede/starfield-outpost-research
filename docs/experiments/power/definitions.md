# P1 power definitions and supplied-exporter verification

The installed main-game definitions implement ordinary solar and wind ratings
through **different base ACTI forms selected by planetary-keyword conditions**.
The basic solar ratings 2 / 4 / 6 / 8 and wind ratings 3 / 6 / 10 agree with the
supplied exporter. Advanced wind is 6 / 14 / 25; it is not a constant multiplier
of basic wind. These are definition-backed results, not current generation
measurements. The [native report](native.md) must establish any effective-value
modifiers, switching/fuel gates and temporal update behavior.

## Inputs, provenance and coverage

All eight-digit FormIDs here are file-relative **Starfield.esm** identities.
All CSV offsets are decimal original ESM file offsets, not save offsets or VAs.
The installed ESM is 1,457,098,709 bytes, SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
No DLC/plugin winning-override merge or loaded menu enumeration was performed.

The maintainer-owned source is `gooberpede/starfield-outpost-network`, local
`D:\Projects\starfield-outpost-network`. Its `.git/HEAD` selects `staging`;
the ref file read during this task resolves to
`9e3005aff9487f11343b39a7534a2070b429ad5f`. Git initially refused a normal
`rev-parse` because of checkout ownership; the ref files were read directly.
No Git configuration was changed. Working-file hashes, rather than the ref
alone, identify the consulted content:

| Input | SHA-256 | Use |
|---|---|---|
| `D:\tools\xEdit.4.1.5p\Edit Scripts\Starfield - Export Planet Directory.pas` | `5fdae92aa88534797d824a79af345301ca80c33e8961627d992dbc9e72710731` | Read-only supplied version 4, declares tested xEdit/SF1Edit 4.1.5p; 16,551 bytes |
| Sibling `reference-source/planet-directory.csv` | `c460062747126a2168109739e75742d325cedf54b98577e5a017b5108ec5eb90` | Source-reported planetary rows compared independently with installed records |
| Sibling `src/domain/powerEfficiency.ts` | `2a5e299293e8a403b3284e1667027eeb5d7d73460c3b62e12982a87085ddef06` | Qualitative categories from canonical ratings; no native dynamics claim |

The source-informed comparison uses the standing maintainer-owned permission
[SOR-P-0002](../../PERMISSIONS.md#sor-p-0002--standing-maintainer-owned-material-grant).
No Pascal script, xEdit, sibling build or test suite was executed. No third-party
implementation was incorporated. Original repository Python readers and E2's
cached inventory are reused with provenance in the receipts.

## Catalogue and construction

[Catalogue](catalogue.csv) retains 332 candidates: 205 CONT, 93 ACTI, one DOOR,
eight LIGH, 17 STAT and eight MSTT. Selection is the union of explicit generation
property `0000032e`, demand property `00000330`, PowerCanBePowered `0005fbbb`,
WorkshopSwitchActivatorKeyword `001690a4`, and labelled outpost power/light
name candidates. The latter includes foundations and exceptional/test forms.
This union is deliberately broader than constructible generators. It is not
proof of relay eligibility or exhaustive classification of every object type.
An absent explicit demand property is not a native demand query.

[Construction](construction.csv) preserves 173 COBJ relationships with inputs
and exact CTDA metadata. The local receipt additionally preserves 724
PKIN/CELL/REFR/base joins from a complete group/header walk. Root assemblies and
their operational children remain separate identities. Name matches alone do
not establish ordinary construction reachability.

| Family | Ordinary COBJ → target | Base forms in increasing rating order | Nominal `0000032e` |
|---|---|---|---|
| Solar array | `00030239` → FLST `002031dc` | `00030238`, `002031e2`, `002031e1`, `002031e0` | 2 / 4 / 6 / 8 |
| Solar dome | `002031d9` → FLST `002031db` | `0003023a`, `002031df`, `002031de`, `002031dd` | 4 / 8 / 12 / 16 |
| Wind turbine | `0003023d` → FLST `002031da` | `0003023c`, `002031e4`, `002031e3` | 3 / 6 / 10 |
| Advanced wind | `001c5145` → FLST `001c5146` | `001c5149`, `001c5148`, `001c5147` | 6 / 14 / 25 |
| Reactor | `00007f7c` → PKIN `00042dc4` → child base `00007f7b` | `00007f7b` | 30 |
| Advanced reactor | `001c5144` → PKIN `00042dc3` → child base `001c514b` | `001c514b` | 100 |
| Fueled generator | `002b0634` → ACTI `002b063a` | `002b063a` | 20 |

Advanced wind/dome/reactor/advanced reactor construction carries respectively
Power Generation research 01 / 02 / 03 / 04 conditions (`00389f14` through
`00389f17`, wire function `036a`, comparison 1). Basic solar, basic wind apart
from its atmosphere condition, and fueled-generator construction do not carry
those research conditions. Construction resource costs are preserved separately
from ongoing fuel in the CSV. Nuclear Fuel Rods/Vytinium Fuel Rods are reactor
construction inputs; that does not establish recurring reactor fuel usage.

All 17 ordinary generator variants have WorkshopSwitchActivatorKeyword and
explicit property `000002d0` = 1. Most have WorkshopStartPoweredOn; the fueled
generator lacks that keyword and instead has OutpostFueledGeneratorKeyword
`0003e82a`. These are positive metadata observations. GeneratorMarker `0008c54a`
has rating 1000 and is retained as exceptional; the solar Dummy, advanced-wind
visual activator and foundations are not silently assigned generator output.

## Planet selection and exporter exceptions

[Environment table](environment.csv) preserves 22 list CTDA rows, with exact
list offsets, choice indices, target forms, ratings, keyword identities,
comparison and flag byte. Wire function `035a` is BodyHasKeyword: p023's
registration window `1400e14b2..1400e1538` binds command `135a` to condition
callback `140bf34a0` and command callback `140c4a810`. Both resolve the
reference's planetary context through `140910690` and call `140c0ad70`
(p024), which examines body-associated keyword sources. This independently
binds the condition's meaning; its manager/cache context is not a real-time
illumination query. Temperature choices map Deep Freeze → 2, Frozen/Cold → 4,
Temperate/Hot → 6, Scorched/Inferno → 8 for basic solar. Dome doubles those
ratings. Thin/Standard/High-or-Extreme pressure maps to basic wind 3 / 6 / 10
and advanced wind 6 / 14 / 25. OR-group metadata is retained; no assumption
about malformed combinations or evaluator iteration precedence is hidden.

Both wind construction recipes additionally carry a `035a` condition on
PlanetAtmosphereType00None `00295eaa`, comparison 0. There is **no zero-rated
wind ACTI in the three-choice ordinary lists**. The exporter's no-atmosphere
value 0 describes that eligibility boundary rather than a selected zero-rated
form. Its precedence is explicit: no atmosphere precedes pressure, then Thin,
Standard, High/Extreme, then recognized-atmosphere fallback 6. Solar source
precedence is Deep Freeze, Frozen/Cold, Temperate/Hot, Scorched/Inferno. These
precedences are source implementation facts; native list evaluation precedence
on contradictory planet keywords is not established by their numerical agreement.

The fallback 6 for recognized atmosphere without recognized pressure is the
exporter's warning policy. The inspected wind lists do not supply a matching
unconditional standard-output fallback. Do not present that exceptional policy
as native behavior. Non-landable bodies are blank in the source; orbital bodies
suppress its missing-keyword warnings. Neither behavior proves that every
non-landable or orbital definition is a usable outpost site.

The sibling CSV contains 1,776 rows. All 1,765 Starfield.esm identities join by
FormID and EditorID and have their complete PNDT physical record fields reread
and compared. Of those, 255 non-landable rows have blank outputs; 1,437 ordinary
bodies agree on solar, with 915 no-atmosphere wind zeros and 522 pressure-derived
wind agreements. The remaining 73 orbital bodies have both outputs blank and no
recognized selection keyword. Eleven non-main-ESM source rows are excluded.
There is no ordinary main-ESM example here testing the missing-pressure fallback
or contradictory-keyword precedence. This comparison establishes agreement with
the installed definitions, not independent runtime verification.

## Fueled generator recipe

ACTI `002b063a` has ResourceInorgPower01 `002b063b` = 1 and nominal output 20.
Reverse IRES NAM1 joins this AV to ResPower01 `002b0638`, ESM offset
1301667906. Its NAM2 points to COBJ `002b0639`, offset 1300741430; NAM3 points
to GLOB `002b0637`, offset 1378472. The recipe requires Helium-3 IRES
`000057f5` ×1, with trailing FVPA word 0, NNAM 1 and CNAM NULL. It is not an
ordinary item-output recipe. FLTV is binary32 `0.009999999776482582` hours;
the established hours ×3600 then binary32 conversion gives exactly 36 seconds.
That is the definition interval, not a measured consumption cadence. Native
input-link admission, due-loop processing, conditional fuel acceptance and
power-state consequences must be read with the native fuel contract.

## Reproduction and executed receipts

Run from the repository with CPython 3.14.3 at
`C:\Users\User\AppData\Local\Python\pythoncore-3.14-64\python.exe`:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/p1-power/definitions.py --run definitions03 --tables
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' -B research/p1-power/verify-definitions.py --input .local-work/p1-power/definitions03.json --run definitionVerification02
```

Use fresh alphanumeric run names because receipts are exclusive writes.
[Catalogue reader](../../../research/p1-power/definitions.py) reads the installed
ESM and the E2 cache, preserves repeated component fields and checks pre/post ESM
identity. It independently rereads 770 selected physical records including
compressed closure and exact field equality. The separate
[comparison reader](../../../research/p1-power/verify-definitions.py) rereads
all 1,765 matched PNDT physical records, checks source CSV joins, asserts all 17
ordinary ratings and the Helium-3/36-second recipe join. Both runs exited 0.
These readers write only ignored local receipts and authored numeric tables.
No original game/save/source file is written.

Local receipts are `.local-work/p1-power/definitions03.json` (SHA-256
`508a6aacf98ba5a37c52860ac940e25132d5a8066bb53103491f30b172af76f5`) and
`definitionVerification02.json` (SHA-256
`22d4392248705b5507f3e9388ff7902220f7ce1d9de64309d0bc2e3480c10b0d`).
Earlier `definitions01` failed an incorrect CTDA-length assertion 28; the actual
32-byte CTDA corrected it before outputs. `definitions02` passed before adding
the construction CSV. `definitionVerification01` passed a cache-based PNDT
comparison; version 02 strengthened it with physical PNDT equality. The initial
unqualified `python` command failed on the WindowsApps alias; the explicit
CPython path resolved execution. Failures are workflow observations, not evidence
of missing game data.

Current effective output, ordinary runtime winning overrides, native wire
admission, dynamic additions, saved damage/modifiers and current powered state
are not measured by this catalogue. Publication eligibility remains a separate
review gate for game-derived numerical tables and local raw record receipts.
