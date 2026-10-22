# Region ancestry and receipt contract

[Report/authority](report.md), [exact pins](sources.csv),
[inherited per-use map](../spatial-equivalence-feasibility/geometry-lifetime/operands.md).
Retail 1.16.244.0 EXE SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
All full addresses below are preferred static VAs, base `0x140000000`.
RVA subtracts that base; runtime VA adds the measured module base. Object/stack
offsets are hexadecimal. Source keys/slots, resource FormIDs, runtime pointers,
saved tokens and Workshop identifier bytes have separate domains.

## Decisive native lineage

| Static source / callsite | Observed STATIC role and collector use |
|---|---|
| ui15 `1421b6931→1421e07d0`, return `1421b6936` | Actual C1D alternate established-site caller. At updater entry R14 is caller reference, RCX spatial state, RDX descriptor. Admit shared state `base+5f5d800` and descriptor `base+5f5d618`; other callers remain UNKNOWN. |
| ui15 updater `1421e07d0..0808` | Entry RSP=E; updater RBP=E−38; saved caller R14 at RBP+18 and return at RBP+38. Allocate observer invocation token on every actual updater entry, scoped by PID/thread lifetime. Recursion has a separate lower stack frame/token. No pointer/time epoch. |
| ui15 `1421e09bd..09cf`, `1421e09db..0a46` | Closure at updater RBP−48: descriptor+0, temporary set pointer+8, radius+10, absolute upper+14. ProcGen from manager+130; shared lock+40. Occupied source slots are 24 bytes, array+20/capacity+28. RDI ordinal; R8=slots+24*ordinal+8; call callback at a46, return a4b. |
| ui16 callback `1421e0f50..0fb6` | Callback entry C: RBP=C−1c8. Saved updater RBP at callback RBP+1c0, return+1c8, saved updater R15/ProcGen+190 and RDI/source ordinal+1b0. RSI is closure. Source wrapper retained at callback RBP−58. These independently derive the actual source slot at each terminal. |
| ui16 `1421e100a..1060` | R12 is byte displacement into wrapper+20 resource slots, R13 resolved IRES/type9f, slot key is runtime resource FormID, slot+8 collection. Collection count+8/capacity+c/data+10; region stride30. Current RBX must lie exactly on a region boundary within that collection; compute ordinal without searching for a matching FormID. |
| ui16 `1421e1091..1114` | Query is reduced into callback RBP+70/+74/+78. Full exported body has no later mapped writes to these words before a terminal. Capture as retained Qb bits, not a direct observation of every earlier load. |
| ui16 `1421e1119..1154` | XY bound/query sphere broadphase; count1 accepts after broadphase; count0 rejects; multipoint paths use strips and helper branches. Bounds are not the complete strip. |
| ui16 `1421e174e`, `1421e1772` | True REJECT before ADD RBX,30; true ACCEPT before MOV RBX,[RSI+8]. At ACCEPT RBX still names the region. Callback normal EAX=1 at18f2 is unrelated to individual acceptance. |
| ui16 `1421e1772..18b3`; ui15 `1421e0aa5..0bf4` | Accepted R13 enters temporary pointer-keyed set; later enumerate occupied set slots into transfer vector. At bf4, RDX is native24-byte begin/end/capacity header before helper installation. Match accepted resource pointer, updater token/frame and temporary set address (updater RSP+60), not FormID/time proximity. |
| Provider `14079f860`, `14079b520→14079c470→14079a330` | Existing [lifecycle](../native-availability-map/region-lifecycle.md) and [seed lineage](../resource-geometry-mature-context/seed-lineage.md) establish static source/BIOM/descriptor/key/RNG paths. No observed producer-to-this-population join exists. No producer site is armed by Stage1. |

The source slot key is copied as u64 from slot−8; it is a native source-map key,
not an independently decoded packed generation key or BIOM. Current source
ordinal and wrapper are captured, resource slot and complete region bytes are
copied, but source frame/owner/BIOM, effective generation BIOM/RSGD, component,
family/masks/weights, packed cell key, RNG seed/order, competition and cache epoch
remain UNKNOWN. A beacon's BIOM is not automatically the queried/source/generation
BIOM. ProcGen lock excludes the mapped writer paths; all-owner/alias lifetime
and absence of in-flight native mutation are not proved by two equal headers.

## Implemented receipt class

`SRO1 SESSION → SAMPLE → END` frames use unchanged C1B/C1D framing and transport.
Every sample preserves raw Windows context (including MXCSR), actual site/RVA,
module base, PID/TID/thread-lifetime/thread-sequence, debug-event/capture number,
read calls/bytes/copy milliseconds. Entry creates updater token/parent; actual
saved caller/reference/Workshop and source checks qualify BOUND_CALLBACK. A
callback token is null: callback entry itself is not observed. Updater token plus
source slot and saved callback frame identify this synchronous source traversal,
not an arbitrary cross-event lifetime. Unwitnessed generation epoch stays null.

Decision samples preserve native edge, selected source ordinal/key/wrapper,
resource slot/header/type, collection count/capacity/data and region ordinal;
region bound XYZ/radius, count/capacity/pointer and complete ordered XYZW as
little-endian raw bytes. Whole paths include unvisited tails. Retained Qb,
descriptor XYZ/index/domain and radius/upper closure words have independent read
flags; failed required reads add a durable loss reason. Null points differ from
an actually read count-zero empty sequence. Associated-file decoder is unchanged
C1D; only its narrow single ordinary Starfield.esm/compile-index0 mapping is used,
not full runtime load order or winning-definition semantics.

The external analyzer requires an ACCEPT, complete geometry/selected ancestry,
qualified namespace and exact resource pointer in a later bound transfer under
the same PID/TID/lifetime/updater-token/frame/temp-set. A native insertion may
deduplicate a resource admitted by another region/source. One accepted region is
positive evidence; remaining regions of that resource can be short-circuited.
No callback/resource/source census is inferred from terminal-only records.

Qc/Qv/Qe are **null** in this minimal observer. Retained Qb and stack closure
stability support only explicitly conditional singleton/broadphase diagnostics.
Multipoint full single-query replay stays UNKNOWN. Terminal/copy success is
neither historical generator identity nor coloured-overlay equivalence. The
[comparison plan](comparison.md) specifies the guarded per-use escalation.

Four hardware sites, no new framework: updater entry, accept, reject, transfer.
Owned C1D Windows DR/DR6/RF/context readback/attachment/gated-fixture engine is
adapted; source-file and identity decoders, SRO1 framing/persistence remain owned
shared dependencies. The fixture and retail builds are separate. Read-at-stop
copies precede ACK; no borrowed target pointer is queued to a worker. Budgets:
4096 source/resource/region/point capacities, point read<=65536 bytes, each read
<=65536, all reads<=1MiB/stop, JSON<=1MiB. Refusal is incomplete/loss, not absence.
No actual OS allocation-failure injection or universal scheduler/XSTATE proof.
