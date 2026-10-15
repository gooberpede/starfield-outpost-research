# Native boundary and minimum operand inventory

[Report](report.md). All offsets and addresses below are hexadecimal unless
explicitly labelled decimal. Preferred static base is `0x140000000`; RVA is static
VA minus that base. Future runtime addresses require the measured runtime module
base. Build: retail Starfield.exe 1.16.244.0, SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
The installed executable and primary exports were hashed in this task; no game
code was executed. Pointer, source-slot key, FormID and save token remain distinct.

## Primary evidence locators

Existing files are under ignored `.local-work/recon/`; no native listing is copied
into the tracked package. Hashes are independently rechecked in the local receipt.

| Key | Existing export | SHA256 |
|---|---|---|
| P15 | `resource-availability-ui-15.tsv` | `08e3b170efd28e4e1f76d1935f723423c09a8e6673f5fe3f87a543458372ff56` |
| P16 | `resource-availability-ui-16.tsv` | `3e29f0c813e9a49aa9c53eada6dee052056dfd659979aeea89868fe7c8447aca` |
| P17 | `resource-availability-ui-17.tsv` | `80e244d7388c0c781a0fd87ab2adb318cde226468c46771ab379e263a2b02894` |
| PS | `resource-milestone-b-spatial-02.tsv` | `d9492a14851533ff9777734a6b5733bde2f66c1002db4c0707be9c866d7e0ed9` |

The separate [existing source manifest](../native-availability-map/sources.csv)
and [Milestone B pins](../resource-availability-milestone-b/native-sources.csv)
control inherited provenance. Export headers identify the program hash, base,
Windows compiler and little-endian x86-64 language. Large inherited exports may
have instruction display caps; the cited P16 callback includes its return tail
through `1421e194a`. At `1421e18f2` it sets EAX to one. That constant traversal
return independently rules out interpreting callback return as region acceptance.

## Natural ancestry and actual result

| Boundary, RVA | Instruction evidence (static VA) | Meaning and suitability |
|---|---|---|
| `021b42e3 → 021e07d0` | P15 updater; existing [caller register](../native-availability-map/functions.csv) | Windows x64 mixed ABI: RCX state, RDX indexed descriptor, XMM2 radius, XMM3 upper scalar. AL reports refresh, not geometric admission. |
| `021e0a46 → 021e0f50` | P15 `1421e09bd..1421e0a77`; P16 entry | RCX closure; R8 address of source-map slot value. Closure +0 points to query, +8 to output set, +10/+14 hold radius/upper f32. Source is dereferenced immediately. Callback traversal result is not a region Boolean. |
| Region entry `021e1060` | P16 `1421e102d..1421e1119` | RBX is the current 0x30-byte region; R13 resolved IRES; R12 source resource-slot displacement; RSI closure; source retained at `[RBP-58]`; collection end at `[RBP-60]`. Not an ABI CALL boundary. |
| Resolved broadphase input `021e1119` | P16 `1421e1091..1421e113c` | Query XYZ at `[RBP+70]` (+78 is Z); region center copied to stack +40/+44/+48. Region radius `[RBX+c]`, query radius `[RSI+10]`. This boundary follows the actual translation additions. |
| Broadphase/count `021e1140..021e1154` | P16 VCOMISS/JA then count loads/JZ | JA rejects; equality passes. Count one jumps directly to acceptance, zero to rejection. No point array is consumed in those cases. |
| Containment/vertex `021e145c..021e1460` | P16 `1421e1393..1421e14ec` | AL=true is a real strip acceptance, originating from four nonpositive crosses or a true vertex helper return. False proceeds to edges; it is not yet a region rejection. |
| Edge comparisons `021e16d4/16ec/1700/1714` | P16 `1421e1466..1421e1714`; PS `141116580..1411166e0` | JBE from squared-distance comparisons accepts. Helper returns XMM0 distance², not a region Boolean. False on one edge/strip does not reject a multi-strip region. |
| Region rejection `021e174e` | P16 `1421e1140/1154/116c`, `1421e1741..1421e175c` | Reached after failing broadphase, zero count or exhausting strips. Observe before ADD RBX,0x30 to retain this region identity. This is a native control-flow decision, not a decision recomputed by the observer. |
| Region acceptance `021e1772` | P16 `1421e114c`, `1421e145e..1460`, `1421e1761..1776` | Observe before MOV RBX,[RSI+8]. RBX still identifies the region; the next instruction destroys that role. R13 supplies IRES. Geometry cleanup at 1761 precedes this join; snapshot geometry earlier. Set insertion happens afterward and is not the oracle. |

The narrow full-region design is a region-entry snapshot plus independently
observed reject/accept edges, with same-invocation ancestry and branch witnesses.
These are proposed observation sites, **not qualified patch sites**. Entry/return
wrapping the source callback would hide every individual decision. Wrapping
`00f4ac50` or `01116580` could provide smaller helper comparisons, but misses
broadphase, count rules, normalization, rotation and containment. It cannot validate
the complete `evaluate_region` claim. The point loop is open; quad edge checks
are closed. Accepting one region skips remaining regions for that resource in
that source; skipped candidates have no native verdict and must never be recorded
as negative examples.

## Capture contract (proposed, not an implemented schema)

Availability codes: **D** directly readable at the stated point; **A** obtainable
through instruction-verified ancestry; **I** inferred and inadmissible as an
independent operand; **U** not established as safely/coherently obtainable by
existing machinery. D/A describe locations, not successful live read guarantees.

| Field | Availability / representation and provenance | Essential condition |
|---|---|---|
| Query XYZ | D: three little-endian f32 words at `[RBP+70]` before 1119 | Capture bits after the actual native additions. Units are native coordinate units; no metres/geography conversion established here. |
| Query radius; separate upper | D: closure +10/+14, f32; P16 1133, 148b..1499 | Preserve bits. Upper applies only to vertex Z; it is not a symmetric height extent. Snapshot actual consumed scalar values if mutable. |
| Indexed XYZ/index/domain | A: closure+0 → 24-byte descriptor, XYZ/+c u32 index/+10 domain | Ancestry/frame provenance. Domain is not itself an arithmetic operand once sufficient resolved XYZ are captured. Do not infer a planet identity from it. |
| Translations actually used | A/D: count VA `1461fae80` (RVA `061fae80`), table pointer VA `1461fae88` (RVA `061fae88`), selected 12-byte row; P16 1091..10fb, 1393..13fe, 146b..152d; P17 ac54..acb7 | Upstream table capture is unnecessary for a predicate beginning with reduced XYZ, **provided every consumed reduced position is observed or proven unchanged**. Re-reading a table once afterward is insufficient. No global-table stability proof is supplied. |
| Branch-specific resolved query | D at broadphase; A at containment reduction; D in each vertex helper local before acbb; D edge query `[RSP+24]` after 1551 | P17 resolves query anew on each vertex call; P16 also resolves for containment/edges. If consumed query bits differ, existing single-query replay is unqualified. Keep the event as a counterexample to capture assumptions, not evaluator disagreement. |
| Resource/source/region identity | A/D: updater invocation; callback ID/source-slot address/value; resource slot ordinal/key, resolved R13 pointer/FormID if read; region ordinal/RBX | Scope identities to invocation/thread and object lifetime. Pointer equality across reloads is no persistent identity proof. Preserve multiple regions and repeated evaluations independently. |
| Region bounds | D: center XYZ +0/+4/+8 and broadphase radius +c in 48-byte region; count +18, point pointer +20 | These are the query predicate's bounds. Source clipping/descriptor bounds belong to generation and are not additional necessary predicate inputs. Unused header bytes must not be assigned invented meanings. |
| Ordered points and widths | D location, U complete safe capture: count×16 bytes, each `[x,y,z,width]` f32 | For broadphase-passing count>1, capture complete ordered array with original count, no implicit last-to-first segment. No downstream quad alone validates normalization/rotation. Native early acceptance may leave an unread tail; full replay capture would read that tail as an additional intervention. |
| Zero/one/broadphase-rejected point data | Not required for these branch comparisons | Qualified count/center/radii suffice; absence of unused point bytes is not an integrity defect. Never extrapolate these pairs to the multi-point branch. |
| Actual verdict and branch | D control-flow witnesses at 174e/1772 plus entry token; strip/edge/helper ordinal and outcome as needed | No inference from final union, UI rows, source visit or callback return. A later successful strip supersedes earlier strip failures. Preserve reason/branch ambiguity if witnesses are absent. |
| Numeric environment | D register state conceptually; U qualified inline preservation/read protocol | Record MXCSR rounding/FTZ/DAZ and relevant instruction version. Replay only the evaluator's finite normal/zero qualified domain; nonfinite/subnormal/overflow or unknown mode is UNKNOWN. |
| Lifetime/concurrency | A shared ProcGen+40 interval in P15; known provider/reset use exclusive lock; invocation/thread/nesting tokens proposed | Supports map lifetime against mapped writers. Does not protect query/table by inference. U: all consumed array bytes/coherence and internal observer nesting/retirement qualification. Header equality cannot prove an unchanging array. |
| Final rows, cache/source completeness | I as a candidate verdict; not essential input | Neither needed nor admissible as the native region oracle. |

No unbounded synchronous array traversal is recommended. A future design must
own copied bytes before native lifetime ends, check pointer/count arithmetic and
read success, and reject partial arrays explicitly. Deferred worker reads of
borrowed native pointers do not satisfy this contract. Complete per-use snapshots
or a proven stability interval are alternatives; demanding both unnecessarily
would inflate the experiment.
