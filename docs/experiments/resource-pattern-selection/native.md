# Native selection and source ledger

All VAs are preferred static addresses for Starfield 1.16.244.0, image base
`0x140000000`, EXE SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Member offsets are bytes relative to the named object. ESM offsets below are
original file offsets, not decompressed record or executable offsets.
[Exact artifact hashes](sources.csv) pin the local evidence and owned methods.

`Nnnn` means `.local-work/resource-pattern-selection/native/nnn.request.tsv`.
`M012` means `.local-work/resource-geometry-mature-context/native/012.request.tsv`.
`Gnnn` means `.local-work/resource-geometry/native/nnn.request.tsv`.
Full decompilation is distinct from the reader's 600-instruction listing cap.

| Boundary | Primary evidence and decisive locations | Supported interpretation |
|---|---|---|
| PNDT serialized tree reference | M012, `FUN_14076ec00`, non-BDST FNAM case `0x4d414e46` | Four-byte reference is stored as a tagged reference at PlanetData `+0x38`. BDST FNAM is separate orbital data. |
| Typed resolution and owner initialization | M012, `FUN_140770eb0`, `0x140771024..0x1407710a8`; N010, `FUN_140773d80`, `0x140773fde..0x14077400e` | Resolves the tree in the form namespace, requires type `0xb6`, installs pointer at PNDT `+0x38`, copies owner to tree `+0x54` and derives system/body fields `+0x58/+0x5c`. Failure clears the pointer. |
| Tree lookup versus creation | N003, `FUN_14096b8e0`, complete function; N009, `FUN_1407791d0` | Resolves typed PlanetData `0xba`; returns its existing `+0x38` tree. Only a missing tree, nonzero owner and creation request take allocation/registration/`0x14096e060`. The alternate N006 `FUN_1418af8e0` has the same existing-tree test before its generation call. |
| SFTR definition loader | N007, `FUN_140970830`, CNAM call at `0x140970b7e`; N009, `FUN_14096fde0`, FNAM case in full decompilation | CNAM/DNAM specify faces/resolution. FNAM/GNAM arrays supply FormIDs and flags. Loader stores words at face offset plus hierarchy index into tree `+0x68`. Main-file FormID namespace is qualified; arbitrary plugin remapping is not transcribed here. |
| Hierarchy versus face slot | N012, `FUN_14096df80`; G007, `FUN_14096eb90` | Native lowest-level cell index is coarse X times resolution plus coarse Y. Tree face offsets and hierarchy prefix are distinct from the FNAM-local index. Do not transpose precomputed arrays as though they were BIOM raster bytes. |
| SFPT registry insertion | N002, `FUN_140594ad0`, default type table; N003, `FUN_140591d40`, `0x140591d73..0x140591db1`; N004, `FUN_1422cc0d0` | Type `0xb5` maps to handler lock `+0x1170`, array count `+0x1178`, pointer `+0x1180`. Insertion appends at prior count under the lock. This establishes a producer, not the historical arrival order or an exhaustive registry mutation audit. |
| File-loader registration | N004, `FUN_14059e000`, default extended-type path | A new form is created, loaded and registered; an existing form follows a different load path. Physical record order, registration arrival order and effective pointer-array contents must not be conflated. |
| Candidate style filter | N002, `FUN_14096b9c0`; N003, `FUN_1405afc70` | Nonnull entries whose SFPT `+0x848` style pointer equals the BIOM style are appended to a temporary list in encounter order. No candidate-weight operand is read here. A zero BIOM style skips enumeration. |
| Generation seed and selection | Existing `exact-beacon-05.tsv`, `0x14096e0a4..0x14096e0c3`, `0x14096e624..0x14096e744`; `rg1-surface-crc-01.tsv`, full `FUN_140970d50` | CRC folds LE uint32 body index, system, effective surface seed; initializes MT. Empty candidates leave an unselected slot and consume no selection draw; one selects index zero without a draw; multiple candidates use binary32 count times uniform followed by truncation. |
| Orientation and initialization | Same selector at `0x14096e748` onward; G011, `FUN_14096be70`; G019/G020 defaults | Whole-pattern rotation/reflection can consume additional generation draws and remap SFBK lookups. The three selected installed slots have flags `0x08`; they use raw SFPT entries. Block orientation is a separate setting. Defaults are not historical loaded values. |
| Single backlink, then type check | G006, `0x140784e95..0x140784ee6`, `0x140784f52..0x140784fcd` | Nonanchor flags translate the descriptor once using stride 12. Resolved block FormID is looked up and checked for type `0xb3`. There is no second anchor-bit test before accepting a valid block. |
| Invalid/default branch | G006, `0x140784f6a..0x140784fcd`, callback at `0x140784ff6`; N002, `FUN_140849670`, corresponding fallback | Missing/wrong-type resolved block uses pointer at static global `0x145ea68a0`, restores original descriptor context and uses the retained ownership position. Null default skips the callback. Its historical value is UNKNOWN, but it is not read by the 48 tested valid-block cases. |
| Source construction and geometry | G011, `FUN_1407862a0`; G013, `FUN_140982d90`; inherited [geometry ledger](../resource-geometry/native.md) | Padding, raw/nominal dimensions and local coordinates enter the unchanged source frame. SFPT lookup and SFBK source-anchor resolution are different decisions. Source-pointer cache/visited state remains separate from table selection and epoch proof. |

## Independent installed definition chain

The main ESM SHA-256 is
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
The predictor resolves PNDT reference values, not EDID names. These offsets and
field sequences are re-read from that installed file using the owned bounded
reader; full fields stay local.

| PNDT / original offset | Upstream FNAM reference | SFTR / original offset | Selected face/index → SFPT/flags |
|---|---|---|---|
| Carinae `0x0005e4da` / 1425228291 | `6f7c1700` | `0x00177c6f` / 1395499426 | 0/28497 → `0x00212e16` / `0x08` |
| Feynman `0x0005e0de` / 1411909071 | `14881600` | `0x00168814` / 1374615748 | 0/33448 → `0x0023de88` / `0x08`; 0/33449 → `0x0023ddf6` / `0x08` |

Each selected SFTR has two 256-square FNAM/GNAM pairs. FNAM is 262144 bytes and
GNAM is 65536 bytes per face. Main-file FormIDs are little-endian uint32; flags
are bytes. The predictor rejects unsupported packed ENAM, face counts, lengths
or missing/ambiguous PNDT references. Synthetic tests distinguish the correct
native index from the incompatible BIOM raster index.

Carinae's tree also carries a `SurfaceTreePatternSwapInfo_Component` field.
Its existence is preserved in the prediction receipt. Bounded native symbol
queries and exact ASCII/UTF-16 searches did not identify a corresponding retail
consumer; that is a locator limit, not proof of no effect. This task predicts the
stored linked-table value and validates its exact witness correspondence. It
does not assert that all components, overrides or later tree mutations are inert.
The initializer named `bAllowSurfaceTreeGenerationSave:Planet` defaults false
in N008 `FUN_14008d1c0`; its name supplies no save-file persistence proof.

Actual runtime registration order, effective seed at historical regeneration,
all possible tree mutation routes and source lifetime remain UNKNOWN. Their
absence from the receipts does not block the finite installed-table prediction.
No new save decode or saved-tree persistence claim is made.
