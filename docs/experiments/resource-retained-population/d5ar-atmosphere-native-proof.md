# D5AR native atmospheric dependency investigation

2026-11-05, Australia/Sydney. Native reflected readers provide a concrete route
from the pinned ATMO file operands to the effective InorganicResources array.
The normal pinned C19B definition route explicitly clears its inherited
InorganicResources array. STATIC reader and postlink evidence is backed by
three owned original-instruction array controls. This does not observe the
historical A0 AtmosphereModifier lookup or loaded PerBiomeData components. Original instructions and complete
operands stay LOCAL-ONLY; this synthesis is REVIEW-REQUIRED.

All native addresses are preferred static VAs for executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`,
base `0x140000000`. Source, file FormID, reflected class identifier and field
index are distinct domains. The method reads only pinned original PE/existing
analysis state. Exports use the verified disposable Ghidra copy in readOnly and
noanalysis mode. No game, original database, save, installation, configuration,
network or Git state is modified. Fresh ignored logs and receipts preserve
copy/input hashes and disk-floor checks.

## Positive native chain

| Operation | Exact original evidence | Limit |
| --- | --- | --- |
| PNDT atmosphere operand | `0x140773450` reads sixteen bytes; typed AtmosphereModifier copy ultimately stores them; `0x1409dd080` resolves the first u32 and checks ATMO type. `atmosphere-definition01.json` binds the actual nested INAM16 and all three non-overridden ATMO definitions. | Native namespace/load and component persistence remain separate. |
| Reflected field identity | Metadata constructor `0x1408bda70` names BGSAtmosphere::MiscSettings and its InorganicResources field, with byte offset `+0x08`, TypeInfo `0x145975240`. | This identifies the native field, not an external LIST by position alone. |
| Original file RDIF dispatch | `0x140852f20` compares RDIF at `0x140853111`, then calls `0x140852e80` at `0x1408531d0`. The latter buffers exact bytes by FormID in global `0x145e91e30`. | The following postlink step provides the application and ordering; buffering alone is not application. |
| Generic DIFF dispatch | `0x1427be8e0` selects DIFF at `0x1427be936`, calls `0x1427becd0`, which consumes the root u32 and calls `0x1427c3480`. The latter binds current TypeInfo and reaches `0x1427c56c0`, then `0x1427c3a20`. | The class resolver below binds file class/property names to native metadata. |
| Checked field selection | Under DIFF flag reader `+0x80`, `0x1427c3a20` reads a u16, rejects indices outside field count `+0x1a`, stops at `0xffff`, and dispatches descriptor `(index+1)*0x20` to `0x1427c5a40`. | It must be the intended class metadata. |
| Native field operand | `0x1427c5a40` uses resolved property metadata at descriptor `+0x10`, obtains native offset/type, creates the exact typed field address, and calls `0x1427c3c70`. Its fallback also compares actual field names byte-for-byte. | No layout is inferred from a human label alone. |
| Array value dispatch | `0x1427c3c70` maps wire type `0xffffff03` directly to `0x1427c2f90`. | A wire type is not a FormID. |
| LIST count / clear | `0x1427c2f90` consumes an eight-byte LIST prefix; at `0x1427c3042` its upper u32 becomes requested count, then calls native TypeInfo vtable `+0x50` at `0x1427c3062`. TypeInfo `0x145975240` has vtable `0x144b5ad88`, whose `+0x50` is `0x1408e2df0`; the latter sets count zero at `0x1408e2e0d` before reserve. | Zero count establishes clear for the bound field without needing to decode an element FormRef. It does not by itself establish field binding or later mutation absence. |

The actual child RDIF contains a single DIFF body, followed by LIST payload
`01ffffff00000000`. Its DIFF selects root field 0 (Settings), nested field 0
(parent reference), field 5 (Misc), then field 0 (AtmosphereType) and
field 1 (InorganicResources), with three `0xffff` end markers. The original class binder and checked wire audit below establish these
associations within the pinned healthy definition route. This does not adopt
the external exporter's provisional zero-LIST heuristic.

## Read-only discovery and preserved alternatives

`d5ar_reflection_scalar_export.py` adapts the owned guarded exporter under
SOR-P-0002. It scans only existing original instruction operands for an exact
requested REFL/RDIF/LIST scalar and refuses more than twelve containing
functions. `reflected-list-scalar01` found six original LIST consumers, including
readers `0x1427be8e0` / `0x1427c2f90` and a parallel writer family. An independent
raw executable-section byte inventory located REFL/RDIF at the original
`0x140852f20` routine; original instruction exports then established instruction
boundaries and the comparisons above. A raw byte hit alone is not semantic
proof.

Earlier exports of the human label Inorganic Resources reached unrelated
metadata; a substring hit reached a MiscStat name. Both rejected alternatives
are preserved locally. Exports of `0x140853430` and `0x1409dd100` provide copy
and reflected pointer-restoration alternatives; neither is silently called the
ESM list reader. The former virtual-slot guesses do not support the chain.
No restricted xEdit exporter is executed, copied or adapted, and its heuristic
supplies no scientific evidence here. Main-file RFDP/REFL/RDIF operands and
original native methods are the independent evidence.

The existing Save52 type-3 parser's typed tail is positively GameDaysPassed /
PlanetWorldSpaceData, not AtmosphereModifier. PerBiomeData factory copying and
actual typed save restoration/activation remain a separate active branch; cold
component initialization cannot be substituted for loaded runtime state.
See [the effective-input gate](d5ar-effective-input-gate.md) for positive source
dimensions, settings/load, definition/override and atmospheric sensitivity work.


## Class binding, ordinary application and executed array control

Original schema reader `0x1427bdbd0` dispatches CLAS to `0x1427bce70`. It
inserts the parsed object in the exact class-ID map consumed by `0x1427bd320`.
Parser `0x1427d3850` reads a twelve-byte header and twelve-byte property
records, resolves class names through the string table and registered TypeInfo
lookup, and compares each property name byte-for-byte with native metadata.
The resolved field pointer is then available at descriptor `+0x10`. A serialized
property offset is not substituted for the resolved native property offset. The
actual native path is Settings `+0x38`, Misc `+0x90`, InorganicResources
`+0x08`, ending at form `+0xd0` where the original postlink reads the count
and `+0xd8` data pointer. The file Settings offset is `0x118`; treating it as
the runtime offset would read the wrong bytes.
The enum reader `0x1427c5c70` consumes a checked u16 length and advances by that
length, supplying the intervening actual atmosphere enum operand's boundary.

The actual ATMO primary table `0x144b6d668` binds ESM reader `+0x88` to
`0x140852f20` and postlink `+0xf8` to `0x140853520`. The latter detaches its
pending FormID row, recursively completes parent postlink at `0x1408536a5`,
and copies parent properties at `0x140853774` before decoding the child's diff.
Factory `0x1427bd510` takes the actual format-1/no-secondary-stream branch to
`0x1427bdbd0`; the installed reader table `0x144d9afb8` has first entry
`0x1427be8e0`, the original DIFF/LIST dispatcher invoked at `0x140853845`.
Only afterwards does ATMO primary `+0x338` invoke `0x1409dcf70`, which rebuilds
the derived IRES array from the now-cleared reflected resource field. The
parent copy cannot restore members after this clear in the examined route.
ATMO primary save/changeform slots `+0xd0/+0xd8` use original base handlers
`0x1405df980/0x1405dfa40`: self identity and generic change-bit-0 flags only.
The earlier `0x1409dd100` pointer helper is primary `+0x318`, not a saved
reflected-resource-array reader.

`d5ar_atmosphere_reflection_audit.py` checks the exact child RDIF framing,
all ten serialized classes, the five selected fields, all three end markers,
the zero-count LIST, native metadata names and original dispatch slots. Local
`atmosphere-reflection04.json` returns `PASS_SCOPED_C19B_DEFINITION_ROUTE_CLEAR`
(SHA-256 `33afb14e4fa7f412cba5ba836336df64510518005740440b4e2d46a6df17de53`).
The final receipt checks that original property mover `0x1427c8420` preserves
R9 across the native `+0x08` metadata offset assignment.
The first attempted audit refused an incorrect descriptive field spelling:
actual serialized field `Misc` has class `BGSAtmosphere::MiscSettings`.
No field is identified solely by the raw position of a trailing LIST.

`d5ar_atmosphere_list_controls.py`, local `atmosphere-list-native02.json`
(SHA-256 `bcfb6a92e37b4e4b682098a082cb0c6adcd37a796ec8a03bf848ab86d37a529a`),
executes unchanged original `0x1408e2df0`, `0x1422cc2c0` and `0x1402c5be0` with
actual allocator vtable bytes and three owned array states. Populated and
allocated-empty arrays both clear count and release their storage; an already
unallocated empty array requires no release. Only native heap free is replaced
with a pointer/size logger; owned backing is not freed by retail code. The first
owned attempt faulted because it omitted the actual reserve release dependency.
The function-plus-caller reserve export separately refused its explicit function
bound; the one-body export preserved the bound and recovered the needed branch.
Both failures are preserved. None of these controls is an executed retail
parent/apply operation or an observed historical A0 runtime array.

For the ordinary, healthy pinned definition route, C19B contributes no
atmospheric inorganic resource. This resolves the child-list semantics without
needing to infer parent/root effective membership or interpret an unused zero-list
element kind. Whether the historical A0 run followed this exact modifier lookup
and retained initialized resource slots after Save52 is still a separate
admission premise. The original effective-input gate remains open for those
loaded-state and historical generation operands.
