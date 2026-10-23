# Carinae case, source ancestry and capture contract

[Brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_C2A_carinae_native_iron_region_qualification.md),
[primary saved identities](../resource-geometry-observation/cases.md),
[active candidates](../resource-geometry-mature-context/active-candidates.csv),
[hardware joins](../resource-geometry-mature-context/f1-witnesses.csv),
[C1E native trace](../resource-region-ancestry/contract.md), [source pins](sources.csv).
Preparation is offline; actual runtime binding remains a future observation.

## Immutable case and predicted baseline

Save52 / HIST-0267 SHA-256 is
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.
The live copy and independent protected backup are checked by full hash, not
by filename alone. Carinae III-a PNDT is Starfield.esm `0x0005e4da`.
Saved beacon token `82be17`, parent token `84655c` and Workshop identifier bytes
`91bac704da9b1e34` identify P4. Tokens are serialized identities, not runtime
FormIDs, handles or pointers. The ordinary beacon base is Starfield.esm
`0x002c60e9`.

| Saved object token | Base / resource in Starfield.esm | Saved XYZ | Supporting decompressed-stream range |
|---|---|---|---|
| `82bea6` Iron | `0x0005ef19` / `0x000057c7` | (139.2847900390625, 6.59259033203125, -3.1037063598632812) | 3777176 to 3777622 |
| `82bea9` Alkanes | `0x000083fc` / `0x000057c9` | (41.5740966796875, 85.6727294921875, -2.474609375) | 3777758 to 3778204 |
| `82bea4` Rothicite | `0x00202f4f` / `0x00005df1` | (125.4991455078125, 148.8143310546875, -14.003398895263672) | 3776662 to 3777108 |

These supported saved joins use WorkshopItem owner `DYNAMIC:ff02be17` and the
same saved parent; that serialized owner notation does not predict a runtime
reference FormID. Iron is 82.78385990069492 model units from the beacon.
Its saved-to-model XY is (-760.7152099609375, -793.4074096679688).
The frozen beacon model center is (-813.3619384765625, -729.5208740234375),
using translation (-900, -800). Nominal query radius 150, Z 0 and upper 0
are prediction assumptions; future captured operands replace none of them in
the immutable baseline.

The versioned [C1H prediction](../resource-installed-settings/predictions-installed-v1.json)
uses four complete source requests and 895 surviving paths: Iron 259,
Alkanes 505, Rothicite 131. Whole-source counts are 354 for
`0:21372:15612:002493eb`, 84 for `0:21384:15636:0006ce55`, 364 for
`0:21396:15624:002493e7` and 93 for `0:21396:15648:002493ed`.
Source BIOM `0x001160d9`, PNDT-selected RSGD `0x0018ce04`, owner 386266,
mask 4 and Rothicite → Alkanes → Iron order are conditional source operands.
They are not inferred from a future wrapper pointer. Installed settings audit,
full local geometry, original v2 freeze and their ledger remain immutable.

## Natural consumer path and runtime identity

All following addresses are RVAs for pinned Starfield 1.16.244.0, preferred
static base `0x140000000`. Runtime VA is the measured module base plus RVA.
The full EXE SHA-256 is
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
The unchanged C1E trace establishes these native operations:

| RVA | Capture and independent guard |
|---|---|
| `0x021e07d0` | Updater entry. Saved return must be module + `0x021b6936`; caller R14 is the actual reference, RCX shared spatial state + `0x05f5d800`, RDX descriptor + `0x05f5d618`. Create a thread-lifetime-scoped updater token. |
| `0x021e1772` | True accepted-region edge, before `MOV RBX,[RSI+0x8]`. Current RBX region, R13 IRES and R12 resource-slot displacement are still available. |
| `0x021e174e` | True rejected-region edge before `ADD RBX,0x30`. A final callback return is not this decision. |
| `0x021e0bf4` | Pre-install transfer. RDX is the native vector header; match exact accepted resource pointer under the same reference/updater/frame/temp-set. Installation is not observed. |

Callback saved return must be module + `0x021e0a4b`. The collector re-derives
ProcGen/source ordinal and occupied 24-byte slot from saved callback state,
checks the actual wrapper, IRES key/type, collection and region ordinal, then
copies the 48-byte region and all ordered 16-byte XYZW points. Capacity limits,
pointer checks and repeated region headers are inherited. Retained Qb XYZ,
24-byte descriptor and closure radius/absolute-upper words have separate read
flags. No generation epoch is assigned from a pointer or digest.

The concrete runtime join is caller reference → ordinary beacon base/type →
typed ExtraWorkshop BC at reference extra list → exact eight Workshop bytes.
The BC vtable must be module + `0x04c24e60`. The expected identifier is passed
as a little-endian scalar `0x341e9bda04c7ba91` to the generic decoder.
Raw reference bytes preserve the actual runtime FormID/handle candidate/XYZ;
no saved token is expanded into any of these. IRES must have qualified
Starfield.esm provenance, not merely an Iron label or matching low FormID.

C2A also copies the reference's stored CELL pointer at object offset `0xb0`
and its 280-byte prefix: type `0x49`, flags at `0x48`, runtime identity at
`0x28` and stored world pointer at `0x110`. The project-owned
`runtime/beacon-observer/capture.h` supplies this existing typed-prefix method;
the prior native cell/fallback analysis in
[Z restoration](../workshop-z-restoration/dependencies.md) limits its meaning.
Unreadable, mistyped or interior cells refuse a bound observation. A different
valid exterior cell cannot be rejected from the saved parent token alone.
Its runtime identity is retained for independent operator/site and later frame
checks; fallback resolution and saved-parent equivalence remain UNKNOWN.
The fixture's wrong-cell test is explicitly the interior-cell negative case.

Ordinary Save52 travel to the named Carinae site and one established build-mode
entry are the proposed natural trigger. The prior Feynman call path is static
evidence for this candidate route, not proof that Carinae will execute it.
If it does not execute, retain no-hit/retained-cache evidence and stop under
the [card](run-card.md); no forced regeneration is allowed.

## Status, lifetime and loss

Each stop copies external memory before any ACK. SRO1 records are fsynced,
closed, reread and independently verified before a numbered ACK. Source-slot
reuse remains separate observations with wrapper/key and invocation scope;
it is not a stable source identity. Nested updater tokens and thread lifetimes
prevent cross-invocation joins. Failed geometry reads produce null points,
not an empty region. Incomplete snapshots, invalid ancestry, fatal LOSS events,
ACK refusal and unwitnessed regions remain visible in qualification receipts.

The scientific event budget is the finite action sequence, with no arbitrary
time/event/volume cutoff. Engineering capacities remain 4096 entries/points,
64 KiB per read, 1 MiB per stop/frame, 64 queued transport lines and 4096
active wrapper invocations. Refusal is loss/incomplete evidence, not absence.
Both-drive 40,000,000,000-byte free-space guards remain mandatory.
