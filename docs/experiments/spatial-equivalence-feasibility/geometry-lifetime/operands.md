# Branch-specific native operand and dataflow map

[Decision](report.md), [ownership/build/address domain](ownership.md),
[admission](capture-contract.md), [pins](sources.csv).
Locations below are hexadecimal module RVAs; stack offsets refer to the named
function's **current native** RBP/RSP, never an observer's stack. All floating
values are little-endian IEEE binary32 words. D means directly located in static
instructions, I a scoped inference; neither means successfully captured live.
Every proposed site remains unqualified for interception, storage and retirement.

| Native path / field and representation | Source and native consumer | Proposed observation and lifetime | Confidence / replay condition |
|---|---|---|---|
| Region identity / ordinal; pointer u64, resource key u32 | Callback 021e0fb3 source value; resource slot displacement R12; R13 resolved IRES; collection count+8/data+10; RBX current 0x30 region at 021e1060 | Entry before 1060 plus caller token at 021e0a46. Keep source key, slot address/value, resource slot and region ordinal separately | D; pointers only invocation-scoped, no persistence identity. Invalid resource definition/empty collection is skipped, not spatial REJECT |
| Indexed XYZ, u32 frame index and domain pointer | Closure RSI+0; descriptor XYZ/+c index/+10 domain. P15 constructs stack closure at 021e09bd..09cf from updater query and scalar registers | Updater/callback entry for ancestry; dereference only during proven lifetime | D layout, I scalar stack-local stability within mapped path; no observed runtime epoch. Domain pointer does not establish planet/world identity |
| Broadphase resolved XYZ, center XYZ, radii | 021e1091..1114 resolves query via count RVA 061fae80, pointer 061fae88, row index*0xc or raw XYZ; center copied from RBX+0/+4/+8. 1119..112a computes XY distance² | Before 021e1119 capture actual query [RBP+70/+74/+78], center [RSP+40/+44/+48], XMM0/XMM2 low lanes; center source provenance at entry | D actual reduced XYZ. Broadphase uses XY only; Z is frame provenance. Region radius loads 112e to XMM1; query radius from closure+10 enters 1133 |
| Broadphase radius sum and decision | 021e1133 VADDSS, 1138 square, 113c compare, 1140 JA to reject | Before 1138 capture native sum XMM0 and loaded region radius XMM1; before/after compare retain native flags/edge witness. Preserve closure radius bits separately | D derived sum and original radius location. Recovering original query radius by subtracting rounded sum is invalid. Closure construction/no mapped writes supports scoped stability, but an unqualified pre-read alone does not prove the consumed memory word. Require qualified stability or actual load observation and agreement with consumed sum |
| Zero / one count, u32 | After broadphase pass, 021e1146 loads region+18 to EAX; 114c count1 accepts; 1154 count0 rejects | At 1149 EAX is actual count; record branch witness. Full points are unused | D. Count0/1 conclusions require broadphase pass. Count pointer/capacity need no invented semantics; malformed capture UNKNOWN |
| Ordered XYZ/width, count/capacity/pointer | Region+18/+1c/+20; 021e115a..1165 forms end; 1180..119b loads current XYZ; 1739 loads width, 12c1 current width; previous XYZ/width carried between iterations | Full owned source snapshot during conditional window; count*0x10 bytes in order. At each visited strip optionally retain endpoint bits as provenance cross-check | D source/stride; G UNKNOWN. Consumed pairs are 0–1 through n−2–n−1. Full snapshot reads possible unvisited tail; no last-to-first segment |
| Strip normalization / rotation / derived quad | 021e11ca..11f2 B−A, VDPPS 7f, VSQRTPS, VDIVPS and zero/infinity masks. 123c calls 004a7f90 with angle from static RVA 04f052b0; 1251..12b0 matrix products; 12bd..1349 widths/endpoints form ordered quad | Sufficient source = stable full endpoints/widths plus pinned constants/mode. Four ordered vertices before 1393 at R9 are optional diagnostic derivative, copied before cleanup | D transformations; frozen source unchanged. Angle bfc90fdb; polynomial sin bf7ffffe, cos b4000000 per existing constant receipt, not ideal exact perpendicular. Capture actual polynomial result at 1241 if mode/constant assumptions cannot be qualified |
| Containment XY, per strip | 021e1393 reloads descriptor pointer, index and translation count/table. 13fe loads selected XY; 1402 stores [RBP−20/−1c]; 140a/140f loads XMM6/XMM7. 1420..144b ordered crosses; JA at 1450 exits on first positive | At 1407 capture stored XY, RDX descriptor and strip token; quad bytes still live. Capture crossing branch or completed four-cross witness, then 145c/1460 acceptance route | D. No Z or upper comparison. Four nonpositive crosses accept; otherwise proceed through vertices/edges. Broadphase query equality does not establish this query |
| Vertex XY/radius/upper, each executed helper | 021e148b/1490 loads upper/radius into XMM6/7 once for the strip's helper series. Calls 14a0/14b5/14ca/14df reach 00f4ac50, which resolves XYZ anew each time. At 00f4acbb [RSP] is resolved XYZ, R8 vertex, XMM4 radius, XMM5 upper | At helper 00f4acbb capture XY, vertex XYZ and XMM4/5 with exact return-site ancestry and vertex ordinal; helper AL at 14a5/14ba/14cf/14e4 is branch diagnostic | D. Helper consumes resolved XY only; resolved query Z is unused. XY distance² <= radius² AND vertex.z <= upper, inclusive SETNC in qualified ordered domain. Upper is absolute, not Q.z+height. Uncalled later vertices are NOT_EVALUATED |
| Edge XYZ/radius, per strip | After all vertices fail, 021e1466 loads radius to XMM12; 146b..152d resolves query again, reusing RDX and R10/R11 from containment selection. 1544..1555 copies XYZ and radius to [RSP+24..30] | At 155b record actual [RSP+24/+28/+2c], XMM12 and [RSP+30], descriptor/index provenance. No worker reread | D. Translation table pointer/count are reused from containment, but selected row and raw coordinates are read again. Neither broadphase nor vertex snapshots substitute for these bits |
| Edge descriptor A, delta, length²; seven f32 | 021e155b..16b8 builds four 0x20-stride stack descriptors from quad: A XYZ, B−A XYZ, length². CALLs 16c6/16e3/16f7/170b to 01116580 | Helper entry RCX points to seven f32; RDX points to resolved XYZ. Capture descriptor and return XMM0 as optional subcomponent diagnostic; associate edge ordinal | D. Full region replay derives descriptors from source geometry, not fitted quad data. Capturing descriptor only narrows claim to edge arithmetic |
| Edge distance subbranches and caller comparison | 011165e4..6601 dot; 660f tests projection>0; 663f interior versus reconstructed A+delta endpoint; 6695 max residual with 0. Caller compares XMM0 to XMM6 radius² at 021e16d0/16e8/16fc/1710; JBE accepts | Capture actual caller edge outcome and distance bits before corresponding JBE; edge 0 sets squared radius at 16cb, later edges reuse XMM6 | D. Full 3D, no upper scalar. Projection<=0 endpoint A, >=length² reconstructed endpoint, else max(distance²−dot²/length²,0). False helper/edge is not region REJECT |
| Terminal region verdict and loop | REJECT 021e174e before ADD RBX,0x30. ACCEPT 021e1772 before MOV RBX,[RSI+8], reached directly for count 1 or after quad free at 1769. Failed strip frees at 1719, advances point loop at 1748 | Observe actual edge with active region token, RBX, RSI, R13, branch witnesses. Snapshot cannot wait until acceptance to read quad | D actual native verdict. Later accepting region skips remaining regions of resource; callback sets EAX=1 at 18f2 regardless of region acceptance |
| Numeric mode and constants | Separate AVX scalar/vector f32 operations, no inferred FMA. VCOMISS/JA/JBE and SETNC ordered behavior only within qualified finite domain | Save MXCSR control/status with records; bind pinned helper/constants/evaluator hashes. Capture site liveness must preserve GP/flags/XMM/YMM/x87 and LastError as applicable | D instructions; retail mode/state preservation NOT TESTED. Existing corrected x87 qualification applies only its fixture storage/continuations |

## Re-resolution and sufficient-input rule

For each entered region, Qb is reduced at 021e1091. For every visited strip,
Qc is reduced at 021e1393; on containment failure, Qv0..Qv3 are reduced in the
vertex helper only as calls execute; if none accepts, Qe is reduced at 146b.
The latter reuses captured table base/count from the containment reduction, not
necessarily a fresh global pair. The resolved coordinates themselves are the
minimal arithmetic inputs. A later table snapshot cannot reconstruct which
value each earlier load consumed. Translation operations are separate f32 adds,
with operand order shown by native instructions. Domain identity stays separate.

The frozen `evaluate_region` accepts one query, one radius and one upper scalar.
Admission therefore requires all **used** Qc/Qv XY and Qe XYZ to agree bitwise
with the corresponding Qb components, and all consumed radii to agree. Used
upper values must agree with the supplied upper. Do not demand Z equality for
containment/vertex, where Z is not used. If use values differ, the bytes remain
valuable dataflow evidence but full single-query replay is INCOMPLETE/UNKNOWN,
not an evaluator mismatch. No rewrite to accept varying queries is authorized.

Mapped closure scalars originate in updater stack locals and the callback has no
mapped write to +10/+14, unlike global translations. This is positive scoped
stability evidence, not a general alias exclusion theorem. Edge radius is locally
held in nonvolatile XMM12; vertex helper preserves caller XMM6/7 and uses captured
XMM4/5 locally. These register lifetimes reduce needed probes. Source closure
bits and broadphase derived sum must remain distinct until exact consumed source
qualification is available; sum agreement alone is not unique reconstruction.

Independent replay retains separate native branch witnesses; it never selects
inputs or tolerances from verdicts. Reconstruct normalization, polynomial rotation,
widths, crosses and segment distance with the frozen arithmetic order. Qualify
round-to-nearest, masked exceptions, FTZ/DAZ behavior, finite normal/zero inputs
and intermediates. Reject subnormal, overflow/nonfinite and unsupported mode from
admission as UNKNOWN. Signed-zero bits are retained; degenerate zero-length masks
are not silently replaced with a conventional polygon rule. Rounding and
comparison boundaries remain potential native counterexamples, not permission
to adjust the frozen model.
