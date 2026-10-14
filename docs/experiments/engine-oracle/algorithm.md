# Supported positional algorithm and executable model

[Model source](../../../save-analysis/scripts/durable_position_model.py),
[input adapter](../../../save-analysis/scripts/prepare_position_cases.py),
[selected inputs](inputs.json), [predictions](predictions.json).
All results currently STATIC/REPRODUCER. No new native oracle observations exist.

## Domain and input authority

Schema `sor-position/1`, pinned retail 1.16.244.0 executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Modern ordinary case 5 Workshop references, qualified saved flags `0x0b/0x2b`,
finite normal/zero binary32 vectors, encoded tags 0–3, resolution 256 and block 12.
Body comes from the typed parent/component/secondary-world descriptor join and
installed PNDT system/body-index agreement. Names and manual network JSON are
not algorithm inputs. Saved tokens are retained in their own domain, not promoted
to runtime FormIDs. Workshop identifier 98 joins the controlled cross-save cases.

The adapter consumes existing independently framed extraction; it is not a new
whole-save decoder. Each input records decoded SHA, record offset, saved identities,
original XYZ/compensation bits, secondary descriptor/key and qualified site cell.
Input hashes attest provenance linkage, not automatic authenticity of arbitrary
caller-created JSON. The caller must supply the qualified upstream extraction.

## Execution order

1. Validate version, source fields, typed identity agreement, descriptor key and
   supported frame/domain. Unsupported/missing/disabled inputs fail explicitly.
2. Unpack secondary-world key: X16, Y16, tag 3, body-index 6, system 18; reject
   reserved bits/sentinel/unsupported indices. Native `14096fb40` reverses the
   lookup axes for tags 2/3; encoded chart axes remain the representation here.
3. Decode reference XYZ and Workshop compensation as LE binary32. The native
   helper `140f4ab80` first copies XYZ. In the qualified activator/keyword/extra-bc
   branch, **all three zero compensation components bypass addition**. Otherwise
   add every component and round each sum to binary32. Preserve the zero bypass,
   including signed-zero bits. Missing type/keyword/extra branches return raw XYZ
   natively; this Workshop-only model rejects unsupported inputs upstream.
4. Select base: descriptor encoded origin for flag 0b; qualified saved site cell
   for flag 2b. This is a saved-frame representation, before a later runtime
   activation/rebase epoch. No local-axis rotation is applied.
5. Per XY axis: `q=floor(f32(C*f32(0.01)))`,
   `r=f32(C-f32(100*q))`. This is neither truncation nor double `C/100`.
   Local |XY| must be below 2^24; overflow/indefinite SIMD conversions, nonfinite,
   subnormal/FTZ/DAZ behavior and arbitrary MXCSR changes are unsupported.
6. Apply signed C remainder `q % 49152` to each base axis. Wrap once into the
   chart, changing tag by xor1 for an X crossing and xor3 for a Y crossing.
   Both crossings xor2. Native `14096f5c0` then decomposes coarse/sub/fine and
   may refresh pattern/block handles. Those opaque asset identities are not
   needed to report the durable cell and are not fabricated by the model.
7. Return body, saved/reference/frame provenance, exact center bits, cell,
   residualXY and saved localZ, with branch/intermediate trace. Return no guessed
   continuous planetary angles or later loaded-world XYZ.

## Supported completeness and concrete boundaries

For the origin-relative controlled cases, the model covers the complete
qualified saved-input-to-index/residual calculation. For site-relative cases,
the exact discrete site cell is an **explicit upstream derived input** from
EXP0020; the model does not replace the native mixed-precision angular quantizer
with an allegedly bit-exact implementation. Prior mathematical angular agreement
does not establish arbitrary quantization-boundary behavior. This is a concrete
coverage limit, not a per-case fit: one rule handles all 17 active mature cases.
Raw-angle-to-cell branch completeness remains outside this executable's claim.

Typed save/load paths, ordered valid-edge selection and mutable rebase are
inherited from [EXP0020](../static-exhaustion/call-and-dataflow.md). They are not
silently replaced with a universal origin. The exact future edge store, height,
validity and rounding history require a specified live epoch. A translated
float32 center can differ by rounding even when the discrete cell agrees; no
tolerance is inferred after seeing such a discrepancy.

Native stored center output (`terrain+130 → +90`) is a different downstream
representation, with active-workshop freshness still to validate. Native
terrain coverage applies `f32(C+translation)` before quantization; it may thus
have a different local floor from saved C. The capture contract records both
the input base and translation to make frame comparisons falsifiable.

Historical simple `f32(P+delta)` wording remains correct numerically for the
finite sampled values. The explicit zero-vector copy branch adds bit-level
precision for signed zero, without reclassifying prior evidence.

## Independent predictions and regressions

23 selected active inputs: four Save25/26, two S1/S1C and 17 Save52.
Two disabled mature records are explicitly unsupported for active placement.
Inputs carry no prior center/output fields. Predictions were generated before
any new live observation. Existing EXP0020 outputs provide regression expectations,
not an independent oracle. The eight new model tests cover controlled invariance,
distinct identity, no-action, mature negativeX, two-axis seam, signed-zero
vector branch, unsupported fields/domain and typed-identity rejection.
