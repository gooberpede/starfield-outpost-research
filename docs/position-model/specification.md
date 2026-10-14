# Durable ordinary-outpost position specification

2026-10-13, Australia/Sydney. Offline consolidation under the
[authorized brief](../implementation-briefs/CODEX_BRIEF_SOR_durable_position_consolidation_application_readiness.md).
Authored synthesis REVIEW-REQUIRED; raw inputs LOCAL-ONLY. Existing finding
classifications are preserved, not automatically promoted by consolidation.

| Element | Answer |
|---|---|
| Question | Which durable positioning operations can downstream research safely consume? |
| Best-supported answer | Ordinary saved beacon/body/site identities and compensated local centers are useful now within their decoded scope. Version 2 deterministically supplies native/packed cell representations when the upstream base is qualified; it retains unknown cells otherwise. |
| Confidence | Exact sampled bytes/arithmetic PROVEN; ordinary semantic associations retain their scoped STRONG proposals. General loaded-frame equivalence OPEN. |
| Coverage | Pinned retail 1.16.244.0, 23 frozen inputs; controlled Save25/26, manual corpus and mature Save52. Native horizontal comparison: two geometries on Kreet, 20 calls each. |
| Evidence | [Capability register](capabilities.md), [self-check](self-check.md), [prior v2 instruction specification](../experiments/position-resumption/algorithm.md). |
| Limitations | Not complete active-player enumeration, exact geographic beacon position, placement eligibility or universal native XYZ. |
| Next step | Review the constrained interface, then separately brief authoritative object membership. |

## Supported domain and identity

The positive detector domain is framed ordinary case-5 inline initial data with
resolved Starfield.esm base 002C60E9 and the expected repeated self reference.
Saved disabled-state reporting is separate from active-player ownership.
Excluded: alternate/template initial records, faction/quest cases, reference-only
decoys, unsupported flags, historical formats without semantic qualification,
arbitrary caller-created JSON and ship landing markers. Empty detection does
not establish absence of all outposts. See [SOR-F-0016](../known-facts.md#sor-f-0016--scoped-ordinary-beacon-identification-and-saved-state-reporting).

The serialization identity is sample/hash + record offset + saved-reference
namespace, with typed parent/secondary/body joins and Workshop identifier as
corroboration. Reference/parent tokens can remap across saves. Names, local XYZ,
runtime VAs, handles and serialized tokens are not interchangeable identities.
The Save25/26 Workshop identifier correspondence is supported for those samples;
it is not a universal UUID/lifetime guarantee. Retain all candidates on collisions;
never choose the first name/nearest point. A body groups sites, not outposts:
SOR-002 and SOR-003 share Kreet but have distinct references, parents, identifiers
and anchors. [Two-outpost evidence](../experiments/two-outpost-site-anchors-and-beacon-coordinates.md)
retains the ambiguous unframed cache window.

## Executable input and output contract

Use [durable_position_v2.py](../../save-analysis/scripts/durable_position_v2.py)
over the existing `sor-position/1` schema; the original v1 and 23 expected results
remain historical fixtures. No new scientific algorithm or public API is introduced.

| Input | Representation and provenance requirement |
|---|---|
| schema / exe_sha256 | `sor-position/1`; pinned executable SHA256 `7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`. No transfer to another build without qualification. |
| source | sample, 64-hex decoded SHA256, nonnegative record_offset in decompressed-stream domain, evidence citation. Valid syntax alone proves no provenance. |
| identity | body 8-hex FormID in qualified content namespace; saved_reference/parent/secondary 6-hex serialized tokens; workshop_id 16-hex byte identity. |
| descriptor | 16-hex packed key, matching body/world_token, system_id and body_index checked against decoded key. Typed save/world/installed PNDT joins are upstream prerequisites, not implied by accepting JSON. |
| frame | integer 0b or 2b only. Saved initial-data flag, not an arbitrary live caller frame index. |
| position_hex / compensation_hex | Exactly 12 bytes each as 24 lowercase hex digits, little-endian binary32 XYZ and ExtraWorkshop+60 vector. Original offsets/hashes stay in extraction receipts. |
| site_cell | null or qualified `[tag,x,y]`; 2b supports tags 0/1 only. Angles are upstream evidence, not a substitute for qualified discrete input. |

Associated site longitude/latitude (double radians, longitude first), parent
world/body and terrain descriptor belong in the evidence envelope even though
the arithmetic schema consumes a qualified discrete base instead of angles.
An anchor is associated overlay/site geography, not exact subcell beacon geography.

`sor-position-result/2` preserves identity/source, body, saved_frame,
center_hex/center, residual_hex/residual, selected_base, source_origin in both
packed/native domains, native_cell (tag/xy/hierarchy_xy/domain), packed_cell,
trace, stages and unknowns. Null cells with `UNKNOWN` are valid partial results.
Center/residual are native local numerical units; 100 is the recovered local
cell span, not an independently calibrated metre conversion. Z is local Z,
not planetary altitude. Grid resolution is 49152; hierarchy radices are
256 coarse, 16 middle, 12 fine, with index `192*coarse+12*middle+fine`.

## Ordered transformations

1. Validate original schema, executable, identity joins, flags, normal/zero finite
   binary32 input and supported integer domain. Ordinary helper arithmetic assumes
   the activator/Workshop-keyword/extra-bc eligibility branch; JSON cannot prove
   that a reference took this path live.
2. Decode packed key low 16 X, next 16 Y, tag 3, body 6, system 18; reject reserved,
   sentinel and out-of-range domains. For tags 2/3 reflect **both** packed axes:
   `native = 49151-packed`. Tags 0/1 copy. Terrain pattern orientation does not
   rotate ordinary reference XYZ.
3. Copy XYZ bits when the entire compensation vector compares equal to zero
   (including signed zeros). Otherwise add all components in binary32. This is
   `C=P+D`, not subtraction. Save26 SOR-003 moves P and accumulates D while C
   remains byte-identical to Save25.
4. Select converted descriptor origin for frame 0b, upstream qualified site base
   for frame 2b. Missing 2b site leaves cell/base null and UNKNOWN while preserving
   center/body/residual. Never infer a discrete cell from an arbitrary angle or
   silently fall back to descriptor origin.
5. For XY use `q=floor(f32(C*f32(.01)))`,
   `r=f32(C-f32(100*q))`. Preserve operation order, binary32 rounding and negative
   floor. Reject nonfinite/subnormal/overflow/environment-unqualified scaling;
   round-to-nearest is a precondition, historical MXCSR was not captured.
6. Add signed C remainder of q modulo 49152 to native base, wrap crossings and
   xor tag by 1 for X, 3 for Y, 2 for both. Decompose hierarchy. Repack using the
   **resulting** tag reflection. Preserve residual Z as local C.z.

Landing-origin snapping is a separate upstream operation: the interior 96-step
rule has corner/reflection branches. It is not applied to ordinary local offsets.
The mixed double/binary32 angular projection and nested quantizer remain a
separate [diagnostic](../experiments/position-resumption/algorithm.md#native-order-angular-diagnostic),
with scalar cosine/provider, dispatch and environment qualification gaps; ideal
inverse-map round trips cannot establish native exact continuous geography.

## Necessary inputs, sufficiency and counterexamples

Within supported arithmetic, qualified center/base and the stated numeric
environment suffice to deterministically calculate cell and residual. Actual
saved input authenticity also requires extraction/framing and typed identity
qualification. Frame 2b needs a qualified site cell for a cell result; center/body
remain usable without it. These are sufficient for this offline calculation,
not for future native loaded-edge selection, current active ownership or world
coordinates. Saved data are durable serialization inputs. Runtime center returns
are transient invocation-specific values requiring identity, caller and frame.

Preserve these falsifiers: v1 reflected key `02b20e7a01c8007b` produces
`[2,124,456]`; v2 yields native `[2,49029,48695]`, packed `[2,122,456]`.
All 23 frozen bases remain unchanged; this synthetic instruction counterexample
is not a retail reflected-world oracle. Mature negative X/frame 2b cannot be
resolved by zero compensation. Phase 1 retained-prior-site output defeats a
universal passive-center oracle. 050 raw XYZ differs from saved XYZ while
translated XY/grids agree conditionally; 060 initial setters/centers match saved
XYZ at different boundaries, with zero AD0C36 calls. Real downstream indexed
frame translation/flags do not prove the missing historical transform or writer.
[Caller ledger](../experiments/workshop-caller-semantics/native-ledger.md) and
[cross-session comparison](../experiments/cross-session-center/report.md) govern
these limits. Full writer/lifetime and full XYZ equivalence remain unproven.
