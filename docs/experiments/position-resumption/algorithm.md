# Version 2 saved-position algorithm

2026-10-11 Australia/Sydney. SOR-EXP-0030 / SOR-EV-0038.
[Report](../durable-position-resumption.md) and [branch ledger](dependencies.md).
Authored research REVIEW-REQUIRED; original native exports/raw saves LOCAL-ONLY.

[Runnable v2](../../../save-analysis/scripts/durable_position_v2.py) consumes the
unchanged `sor-position/1` extracted-input schema and returns
`sor-position-result/2`. The original model, reader, observer, 23 inputs and
predictions are preserved. This is a scoped offline reconstruction, with no
fresh native end-to-end validation. Per-stage labels describe the evidence basis
of the operation, not authenticity of arbitrary caller-created JSON.

1. Validate pinned executable hash, typed body/system/index/world joins, source
   decoded hash/offset, supported ordinary case 5 frame 0b/2b, normal/zero float32
   position and compensation, finite integer-conversion domain. The extraction
   is a prerequisite; input receipt hashes do not establish semantics themselves.
2. Unpack the secondary-world key: low 16 X, next 16 Y, then tag 3, body 6,
   system 18. Reject reserved bits/sentinel/out-of-range fields. **Convert packed
   coordinates to native hierarchy coordinates:** for tags 2/3 use
   `X'=49151-X, Y'=49151-Y`, preserving tag. Tags 0/1 copy both axes.
3. **Precondition:** caller-qualified ordinary activator/Workshop-keyword/extra-bc
   branch, inherited from the frozen schema scope. Native 140f4aba5..140f4abea
   tests nonnull reference+98, its type 1e, nonnull keyword global 145f0b380/type 4,
   predicate 14047fce0 and extra-bc lookup 140347170. Failure of any gate returns
   the initially copied raw XYZ; arbitrary inputs do not establish these gates.
   This reproducer supplies conditional arithmetic for qualified ordinary inputs,
   not captured execution of their runtime keyword predicate.
   Within that branch, copy XYZ exactly if the entire compensation vector compares equal to zero;
   otherwise add every component in binary32. This preserves signed-zero bits
   on the copy path. Restrict unsupported FTZ/DAZ/subnormal arithmetic domains;
   no observed MXCSR is available. Z remains local Z, not body altitude.
4. Frame 0b selects the converted native descriptor origin. Frame 2b selects an
   upstream qualified site cell, tags 0/1 only. Site-cell derivation is not a
   native-validated algorithm input stage: the saved-frame association is a
   model supported by the qualified corpus/static frame branch. A missing site
   returns null cell/base and UNKNOWN, retaining valid center/body/residual.
   No descriptor origin or mathematical angular result substitutes for it.
5. For each XY: `q=floor(f32(C*f32(.01)))`, then
   `r=f32(C-f32(100*q))`. Order matters. Normal inputs whose scaling can become
   subnormal are rejected as environment-unqualified. No integer indefinite,
   nonfinite, subnormal-input, overflow or arbitrary rounding mode is modeled.
6. Apply signed C remainder of q modulo 49152 to native base axes. Wrap each
   crossing; xor tag with 1 for X, 3 for Y, 2 for both. Decompose indices as
   `coarse=i//192, sub=(i%192)//12, fine=i%12`. These are **native hierarchy**
   outputs. To report packed coordinates, reapply the tags 2/3 reflection using
   the **resulting** tag. Do not treat packed keys and native indices as one
   address/coordinate domain.
7. Return both representations, center and residual bits, source identities,
   selected-base/floor trace and explicit stage unknowns. This does not predict
   a future activated edge, loaded XYZ or continuous geographic coordinates.

## Preserved counterexample and correction

Pinned input key `02b20e7a01c8007b`, frame 0b, XYZ=(100,0,0), zero compensation:
the original model returns `[2,124,456]`. Native unpack/offset gives hierarchy
`[2,49029,48695]`, and repacking gives `[2,122,456]`. This accepted-input defect
was found by the specialist from instructions, not a retail runtime observation.
All 23 frozen cases use applicable nonreflected bases and remain unchanged.
Old source/predictions are historical version 1, not overwritten expected values.

## Native-order angular diagnostic

[Diagnostic source](../../../save-analysis/scripts/position_quantizer_diagnostic.py)
implements the recovered vector-to-square arithmetic and nested quantizer.
It is separate from v2: imported scalar cosine remains a Python surrogate,
never a native oracle. Both bounded SIMD sine branches are implemented with
explicit AVX/FMA dispatch candidates and assumed round-to-nearest arithmetic.
The native wrapper's SIMD lanes add pi/2 before sine. CPU global 1458c6b50 selects
14374dda0 or 14374e650 through 14374dcc0: separate multiply/add versus FMA
reduction/Horner. Canonical angles stay below the 2^24 large-reduction threshold.
Selected dispatch, resolved scalar-cos provider/version and FP environment were
not archived. Current installed CRT state cannot establish which provider
executed historically. These are specific missing inputs/validation, not a
claim that the static functions are intrinsically unrecoverable.

`1423321f0` accumulates norm² as `(Y²+X²)+Z²`, converts to binary32,
uses sqrtss and binary32 reciprocal, then scales double XYZ. South negates X;
divide X/Y by `1+abs(Z)` and clamp each to[-1,1]. Radicands use distinct
orders `(a²+2)-b²` and `(2-a²)+b²`, plus/minus `2.8284271247461903*a/b`.
Replace a radicand by positive zero only when `abs(r)<1e-7`; this is not
`max(0,r)`. Multiply each double square root by .25 before subtraction. No FMA
occurs in this inspected path. Invalid/nonfinite diagnostic domains fail.

With B12,R256,M192,N49152: clamp `w=u+.5` to `[0,1-1/(B*N)]`;
`coarse=floor(R*w)`; `t=(fmod((M*R)*w,M)*(1/M))*16`;
`sub=floor(t)`; `fine=floor((t-double(sub))*B)`. Separate multiply/remainder
rounding must not be flattened to `floor(N*w)`. Forward cell centers multiply
by the precomputed double reciprocal: `(double(I)+.5)*(1/double(N))-.5`.

Landing-origin snapping is a different operation. Its 96-step interior rule
does not describe hemisphere corners: subX<4 selects0,4..11 selects8,>=12
increments coarseX and may toggle hemisphere; the Y>=12 branch depends on
whether X already crossed, and the Y boundary reflects coarseX. V2 does not
invoke this snap or fabricate a corner result. Terrain pattern orientation and
2×2 footprints likewise affect asset lookup, not ordinary REFR axis rotation.

Tests cover all tag/crossing combinations, signed-remainder multiples, native
packed reflection, signed zero through inherited tests, negative floor,
binary64 neighboring quantizer boundaries, poles/equator, missing upstream
site and unsupported domains. Synthetic instruction/algebra expectations are
labelled separately from the 23 frozen regressions and archived native evidence.
