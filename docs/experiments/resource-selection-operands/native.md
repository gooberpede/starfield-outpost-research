# Native operands, settings writers and definition provenance

[Answer](report.md), [exact local export pins](sources.csv).
Retail1.16.244.0, EXE SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
All nine-digit addresses are **preferred static VAs**, base `0x140000000`;
RVA subtracts that base, runtime VA adds the actually measured module base.
Object/stack offsets below are hexadecimal. File offsets are explicitly decimal.
Raw runtime pointers, source descriptors, source-map ordinals, owner keys,
FormIDs, packed keys and saved Workshop identifiers are distinct domains.

STATIC denotes exported instructions; OBSERVED below means synthetic acquired
operands unless explicitly labelled existing C1E native evidence. DERIVED denotes
calculation/predicate from those bytes. No current game observation is implied.

## Qualified observation boundaries

| Site / native evidence | Operand and implemented meaning |
|---|---|
| `14079b520`, cont01; provider producers01 `14079fed3..ff18` | Entry RSP=E. RCX=actual source; RDX=local integer origin pointer; R8=selected source descriptor; R9D=manager owner key; `[E+28]`=BIOM; `[E+30]`=output map. Return must equal relocated `14079ff1d`. Copy source70, descriptor18, BIOM30, origin8, manager200 and manager global pointer `145fd9c30`; compare owner with manager+80. This is source-generation identity, not Workshop binding or a permanent source lifetime. |
| `14079b53e..554`, cont01 | Seven pushes + allocation2a0 give b520 working frame F=E−2d8. Entry native saved arguments at F+2e0/+2e8/+2f0/+2f8/+300/+308 are separate from original Win64 caller home/stack arguments. |
| `14079b8af..8ed`, `ba15..ba38`, `bb23..bb73` | Per-biome result selects RSGD-related record at F+80 (resolved/typeab), root IRES id at F+58 from F+130, selected DNAM pointer at F+68. Capture raw per-biome result F+e0 length68, selected record prefix when non-null and final DNAM. `14079c540` and subsequent fallback/component/BIOM-array branches can select another descriptor. Raw selection evidence is not a complete winning-override reconstruction. |
| `14079bdad..be20`, cont01; pinned native019 and settings01/02 | DIL=ordinary low-nibble mask; IRES byte+110=rarity. Start active XMM8 (unit constant); mask8 or rarity>mask enters inactive path. Inactive starts XMM7 zero, then rarities0..5 select six separate setting payloads; >5 keeps zero. Collector retains DIL, stack mask F+30, full IRES prefix and actual XMM3 at the CALL. `mask_branch` is **DERIVED_STATIC_PREDICATE_NOT_BRANCH_TRACE**, independent of scalar value. It is not an observed sequence of taken jumps or proof of no earlier concurrent definition write. |
| `14079be20→14079c470`, ui29 | RCX=F+180 generation context (28 bytes), RDX=current IRES, R8=selected DNAM, XMM3 low32=effective multiplier. Preserve ordered list begin F+50/count F+40, current RBX slot and observed per-invocation call ordinal; no re-sort/tie reconstruction. Main-file qualification uses unchanged C1D associated-file decoder. Ordinal excludes null/skipped/nonordinary calls. |
| `14079c470..c4f7`, ui29 | Weight moves XMM3→XMM6 at c493, then stack argument at c4e8. Inner generator is called at c4f7, returnc4fc. Outer X/inner Y and special alternatives remain native scheduling, not receipt timestamp order guesses. |
| `14079a59e`, cont01 `a39a..a59e` | At chance stop S=cell working RSP. Resource RSI, DNAM pointer `[S+230]`, block R14, observed packed key `[S+a0]`. Actual comparison has just executed VCOMISS XMM1,XMM7; CF=1 follows ADMIT fallthrough, CF=0 takes REJECT JNC. Retain raw flags/MXCSR and XMM1 draw×100/XMM7 threshold bits; NaN/nonfinite cases require separate interpretation, not a percentage assertion. |
| Same cell frame | Saved cell-pointer `[S+218]`, origin-pointer `[S+220]`; exact caller returns `[S+208]`=c4fc and `[S+278]`=be25; E=S+558. Resource and DNAM pointers must match the last qualified resource-call token. Copy signed XY/origin, block40 and native post-first-draw MT header at `145920b00`; do not label that header an original seed. Native CRC seed before draw remains unobserved; packed key+owner permit a separately labelled derivation. |
| `14079a3a1..3be`, cont01 | Cell rarity block is DNAM+40×(rarity+7), chance scalar+1c. Native multiplication uses stack weight at S+238; `effective_weight_bits`, `cell_chance_bits` and actual XMM7 threshold are separate fields. Upper biome-generation blocks are not this cell threshold. |
| `14079ff1d`, producers01 | Synchronous provider continuation after b520, before visited append; exact RSP must equal E+8. Copy source and output map prefix. This witnesses return even after native early exits; it is not a region census/completion/installation certificate. |

Entry/terminal tokens plus exact saved returns qualify this synchronous call
lineage in the fixture. Different threads carry independent lifetimes and token
stacks; nested providers retain parents. All-stop copies protect those copied
bytes at the stop, not historical lifetime, future replacement or complete
all-writer exclusion. Pointers alone cannot join this to C1E slot31/54.

## Initializer, installed GMST and relevant writer path

The new headless exports settings01–08 use existing owned Cr1Recon.java with
`-process Starfield.exe -readOnly -noanalysis`; commands/console logs are retained
beside each export. No import, program analysis, symbol/type/comment edit or
database save. Some large original functions hit instruction-list limits while
full decompilation remains available; conclusions pin the actual listed decisive
windows. Getter xref inventory settings05 hits4096 and is not a complete writer
audit. Only the relevant named-setting paths were followed.

| Rarity | Initializer function | Setting payload VA | EXE default | Main GMST FormID / DATA |
|---|---|---|---|---|
| Common0 | `140051240` | `145e901b8` | .3 | `002d40c0` / .3 |
| Uncommon1 | `140051270` | `145e901d8` | .2 | `00226b0c` / .2 |
| Rare2 | `1400512a0` | `145e901f8` | .1 | `00226b0e` / .1 |
| Exotic3 | `1400512d0` | `145e90218` | **.01** | `00226b0d` / **.05** |
| Unique4 | `140051300` | `145e90238` | 0 | `002f031c` / 0 |
| Special5 | `140051330` | `145e90258` | .3 | `002d40ce` / .3 |

Native019 and fresh PE reads establish exact default words and switch destinations.
Exotic initializer reads constant VA `144f03eec`, EXE file offset **82851052**,
bytes `0ad7233c`. Main ESM exotic record header offset **158801**, EDID
`fInactiveResourceChanceMultExotic`, DATA `cdcc4c3d`. Main ESM hash
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
`provenance.py` walks all2312 main GMST records with the existing bounded ESM
reader and hashes the EXE/ESM before/after. This is installed main-file evidence,
not the historical winning value or an audit of every plugin/INI.

STATIC `1402d65e0` stores setting name+18, live payload+8 and initial shadow+10,
assigns SettingT<GameSettingCollection> vtable `144afa820`, and registers through
`1402faea0` collection virtual+8. The latter constructs GameSettingCollection
vtable `144afa960`, global `1461e0200`. `1406846f0` performs name-keyed lookup
in collection+118; it does not make the constructor default immutable.

STATIC settings07 `140684160` is the DATA reader: checks subrecord tag DATA
at `1406841a1`, obtains the setting's name-derived type through `1428cd500`, reads up to
four float bytes at `140684233..1406842b4` and calls `140684b30` at `1406842bd`. The float setter
unconditionally writes the supplied binary32 to setting+8 at `140684b43`, then
dispatches change callbacks where applicable. GameSettingCollection virtual+28
at `140684380` dispatches this reader via `144ae9a48` with its file/context+110.
Settings08 `1406843d0` stores the current file/context at collection+110,
looks up the supplied name through `1406846f0` at `1406843f6`, and dispatches
virtual+28 at `1406846c3`; `1428cd500` maps name prefix f to float type3.
This is a native route for loaded DATA to override a named registered setting;
its effective execution for Save52 is still unobserved.

STATIC settings06 `140c228a0` independently looks up a supplied setting name,
checks its type, converts float text and calls the same setter (`140c22a60`).
This demonstrates another relevant mutability route. No command was executed,
no console/Papyrus availability guarantee is made, and no setting was changed.
An INI route for these specific names is **UNKNOWN**, not presumed or ruled out.
Save persistence, loaded override ordering and historical change callbacks remain
UNKNOWN. The proposed collector reads the actual payload and scalar at use;
it never substitutes either default or main definition for that observation.

## Screenshot corroboration and scientific comparison rules

Seven supplied screenshots remain local/hash-pinned, not copied into Git.
Six selected ordinary entries across CanyonsDefaultRes, DesertRocksDefaultRes
and FrozenBarrenDefaultRes03 show lower **Cell Exotic Chance to Appear15**.
The water selection instead shows Everywhere Chance per Node100 in the upper
Biome panel and lower Cell Chance0. Upper Common Chance varies40/50/60, and
upper Exotic Chance per Node varies10/15. None of those is the inactive setting.
Installed RSGD records `00258050`, `000083de`, `0037c672` and repeated RNAM/DNAM
pairs are independently retained in the local provenance receipt. A screenshot
caption/selected row is not a native effective RSGD selection or IL family join.

Compare later evidence at its first supported difference: source/BIOM/RSGD/family,
ordinary mask predicate, actual setting/scalar, cell chance, path construction,
competition, accepted cached region. Keep IL and exact Cu control mandatory;
carry `0057ce/0057cb` comparisons whenever their source/population is observed.
Do not infer all later stages from a matching earlier scalar. Preserve both
frozen .01 and previous three endpoint counterexamples. The .05 test is a single
definition-backed diagnostic, never authority for parameter searching, adopted
predictions or a claim that historical native code used that value.
