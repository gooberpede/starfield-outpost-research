# Native observation map

**Current disposition: NO-GO.** This map describes the unchanged historical candidate. [Reassessment](scientific-value-reassessment.md) rejects the proposed first live session; native findings and observation limits are unchanged.

[Contract](contract.md), [prior detailed register](../native-availability-map/functions.csv),
[dataflow](../native-availability-map/dataflow.md), [lifecycle](../native-availability-map/region-lifecycle.md),
[26 exact source pins](sources.csv).
Retail 1.16.244.0 executable SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
preferred static base `0x140000000`. Below are **RVAs**; static VA = that base +
RVA. Future runtime VA must use actual recorded module base. No runtime pointer
is a FormID, source key, serialized identity or file offset.

| Natural CALL site RVA → target RVA | Capture / native ABI | Evidence and justified use |
|---|---|---|
| 021b26bc / 021b42e3 / 021b6931 → 021e07d0 | RCX initialized state; RDX 24-byte indexed descriptor; XMM2 radius, XMM3 upper scalar; AL refresh. Preview bridge separately retains RBX reference. | 0.7.0 lineage plus ui-15 and producer call exports. H1/H4/H6; classify init/preview/operation by site. Init is an established-path candidate, not proof of player ownership. |
| 021e0a46 → 021e0f50 | RCX closure; R8 address of occupied source-slot value; RDX/R9 forwarded unchanged integer channels. Return continuation in EAX, not acceptance. | ui-15 VA 1421e09bd..0a4b; ui-16 entry and full decompilation. H1/H3; closure points to indexed query, output-set local, then two f32 bounds. |
| 007b526a / 007a1a3c → 0079f860 | RCX ProcGen; RDX discrete Int2 pointer; R8 aggregate-output wrapper; fourth integer channel forwarded. Return bits retained without success label. | ui-32 full callers and producers-01 full provider. H2; direct task/layer call versus aggregate fallback distinguished by site. No synthetic provider call. |
| 01581a96 → 01578500 | Integer command/model channels; model callback before/after | 0.7.0 native/ABI lineage. H5 independent consumer identity. |
| 015785c9 / 015785e8 → 021f8120 | Actual spatial/atmosphere begin/end and fold | 0.7.0 native/ABI lineage. H5 union inputs. |
| 0157862e → 0042e250 | Actual selected special resource append | 0.7.0 native/ABI lineage. H5 selected water and duplicate policy. |
| 015787e9 → 0157fcf0; 015787fc → 0157fde0 | Row fast/growth; bridge retains RDI resource and RSI payload | 0.7.0 native/ABI lineage. H5 actual IRES-to-row association and final census. |
| 015784a0 → 022cdf60 | Returned command identity | 0.7.0 lineage. H5 allocation candidates; not a unique producer ancestor. |

The build verifies E8 displacement, original five bytes and 32-byte window hashes
for all thirteen sites, plus target entry hashes. Exact bytes/hashes belong in
the local build manifest/generated header, not copied proprietary bulk here.
CALL replacement preserves instruction boundaries; x64 near relays lead to normal
ABI wrappers. Original four channels, mixed float argument slots, result and
unwind behavior are forwarded. No additional engine function is invoked by the
observer. Disposable synthetic ABI evidence is distinct from retail compatibility.

Field offsets in this map are hexadecimal. The indexed descriptor contains
binary32 XYZ at +0/+4/+8, a u32 index at +c and a domain pointer at +10.
The 0x68-byte state snapshot includes vector triples at +0/+18/+30 and prior
position/domain data at +48/+54/+58. A source visit reads a 0x18-byte closure,
an 8-byte source-value slot and a 0x40-byte source header. The source map's data
pointer at +20 and capacity at +28 remain sampled header fields. The provider
capture reads the 8-byte Int2 input, a 0x78-byte ProcGen snapshot and the 8-byte
output pointer slot. It does not dereference the full source index, visited
keys, regions, points or output aggregates. Failed reads are unavailable
operands; zero read-ok never means an empty list.

The native updater holds ProcGen+40 shared lock across the callback; provider
has its own exclusive interval internally. Extra header reads before/after the
provider are non-atomic and do not establish that interval or a coherent census.
TLS ancestry relates same-thread natural nested calls only. No cache epoch can
be inferred from pointer equality. Unhooked reset/destruction/replacement paths
remain outside this candidate, so global freshness is UNKNOWN.

0079b520 constructor, 00f4a140 established builder and 00b4cee0 preview helper
are source-backed anchors, not new hook surfaces. Constructor has additional
arguments/ownership prerequisites; wrapping it with the four-integer helper would
be incorrect. Capturing complete geometry plus each accepted/rejected decision
requires new internal preservation and decision-coverage qualification; this
candidate explicitly reports that measurement UNQUALIFIED. It cannot validate
native spatial equivalence or provider hit/miss/generation success.
