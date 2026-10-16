# Production UI provenance: 1.66/MIN and 1.67/MIN

[Report](arithmetic-report.md), [source pins](arithmetic-sources.csv).
Native addresses are static VAs in the pinned retail build; object offsets are
hexadecimal. `aNN` identifies local `e1-arithmetic-NN.tsv` exports.

**Both inspected screens read the same cached binary32 production field,
ExtraWorkshop+84. Their installed formatting algorithms differ.** For an equal
ordinary positive number near 1.666…, the build footer displays 1.66 and
LOCATIONS displays 1.67. Equal historical raw bits are not recoverable from
the two labels, but a different rate calculation is unnecessary to explain them.

## Screenshot evidence and scope

The maintainer supplied `.local-work/screengrabs/1716740_61.jpg` (814,056 bytes,
SHA-256 `00e3769e6d1f40832c3eb59762f2da820e555771abda2322ef3c0f5f0c4caf7c`)
and `1716740_62.jpg` (132,080 bytes,
`14444e97c9e2a9ba761d053b049ea5643c5715b4a85e175e6c74d1b4b5bf4ccd`).
They show Kreet Outpost 1, crew/cargo 0, needed power 5 and total power 6.
The first image's footer at the lower right reads PRODUCTION 1.66/MIN;
the second LOCATIONS page reads 1.67/MIN. The brief supplies the one-small-Iron,
one-solar, Save3-derived gameplay provenance. It supplies no fresh save file,
internal raw value, exact capture interval or matched scheduler state.
The images are preserved locally and untracked; they are not timing controls.

## Common statistic and separate native UI adapters

| Stage | Build-mode footer | Database / LOCATIONS |
|---|---|---|
| Native source | 140f34590 validates a Workshop reference/category, selects ExtraBC and copies 24 bytes from +7c; missing/invalid source gives zeros. | 141360e80 enumerates global Workshop handles at 145f0ba78/80, resolves each, skips the positive 140f3bfc0 predicate and validates Workshop/ExtraBC. |
| Production field | Summary+8 is ExtraWorkshop+84. | 141361186 loads the +7c block; 1413611c8 extracts float lane 2, also ExtraWorkshop+84, into named 72-byte row+20. |
| Update/queue | 14143f690 snapshots the summary using explicit Workshop or global 145f5d8e8; queued 14143fdc0 invokes 14143f8a0. | 14136ac90 copies the row vector with 141363960 and queues 14136dc00; 141361c10 adapts row+20. |
| UI value | 14143f8a0 at 14143f8e1..e9 passes summary+8 to 1404bcc80. That setter copies binary32 unchanged and marks the value dirty. | Adapter directly copies binary32 to the corresponding TUIValue. |
| Binding | 14143fb40 binds `fProduction` in WorkshopStatusData. | 14136c980 binds `fProductionPerMin` in Almanac::OutpostEntry. |
| Final consumer | Workshop menu FooterContainer.OnStatusDataUpdate. | LOCATIONS page LocationsPage.OnOutpostSelectionUpdated. |

Source exports: a03/a05 binders/model lifecycle, a09 adapters, a11/a13 summary
and setter consumer, a15/a16 full Almanac producer, a18 float setter.
Summary layout from ExtraWorkshop+7c is generated power u32, required power
u32, production float, cargo u32, crew u32 and build-limit float (24 bytes).
This investigation identifies these fields without calculating power totals.
The display path does not perform a fresh terrain/resource-availability query.
Registry membership, resolved extras and update epoch remain prerequisites.
Persistence of the cached summary itself is UNCLASSIFIED here; serialized
producer rows do not automatically establish serialization of the summary.

## Cache producer and meaning of the rate

1421f2cb0 (a18) pops one 8-byte request under its owner lock: low 32 bits
Workshop handle, high 32 bits refresh flags. It validates/resolves the Workshop
and ExtraBC, snapshots the old summary and selectively recomputes fields.
Mask 2 clears production+84 and invokes 1421f36b0 over the ExtraWorkshop
resource-keyed producer map at +20. The latter walks slots of stride 18 and
rows of stride 1c, requires **cached eligibility row+18**, resolves the handle
and excludes the fueled-generator predicate 140f7cb70. Valid rows contribute
140f7bf80's binary32 rate by VADDSS at 1421f3839/383e.

140f7bf80 returns `(60 / effectiveInterval) × effectiveResourceAV`, with a zero
interval producing zero. Its effective interval uses the same timer/perk and
positive HarvesterRateMult contract as production. It does not observe created
items. The cache sum does **not** call the scheduler's current reason evaluator
140f7d120. Cached eligibility and registration age can matter.

Mask 1 refreshes the power pair through 1421f2680 and parallel callback
1421f3690 → 1421f2890; that callback writes only summary+0/+4, leaving production
zero. Mask 4's cargo helper 1421f34d0 writes only +c. Crew and build-limit
branches likewise do not supply another production factor. These exclusions
follow the called helpers, not their names (a19/a21/a22).

After refresh, requested flags or field changes emit WorkshopStatsChanged
events. With no explicit low-five-bit refresh request, an absolute production
change greater than binary32 2^-23 triggers type 1; forced refresh uses type 5.
The consumer's event subscription is not evidence that every engine state has
already refreshed. The worker 1421ba960 services updater owner 145f5db08;
queue/lifecycle details and their remaining freshness limits are retained in
the local specialist notes and [review](arithmetic-review.md).

The event sink's callback `1421f2ac0` (`a24`) maps incoming types 0/1/2/3/4/5
to refresh masks 1/2/4/8/10/1f. It converts the Workshop reference to a handle,
appends a new 8-byte request or ORs flags into the existing request for that
handle. Requests coalesce. Initialization `1421ad290` subscribes this sink to
the distinct request source `140f4fde0` when `14591ebd8` is nonzero; teardown
`1421ad550` unsubscribes it (`a22`). The updater processes one queued request
per worker invocation, not a synchronous recalculation on every UI read.

## Installed decimal formatting

The original offline readers inspect installed `Starfield - Interface.ba2`
(135,450,443 bytes, SHA-256
`dab6aeebb7e54282818e9a1957e80baef22ae992c6363cbe910f92b8adf3e702`).
They use CPython stdlib for BTDX version 2 GNRL entry framing, SWF decompression,
DoABC constant pools/method bodies and the selected AVM2 instructions. No
third-party extractor/decompiler or copied implementation was executed or
incorporated. Asset bytes and disassembled bytecode stay LOCAL-ONLY.

| Installed code | Exact ordinary-number behavior |
|---|---|
| `workshopmenu.swf`, FooterContainer.OnStatusDataUpdate | Reads fProduction, calls GlobalFunc.FormatNumberToString with PRECISION=2 and omitted third argument. |
| GlobalFunc.FormatNumberToString | Method's optional Boolean defaults to false. That branch uses Number.toString and substring through decimal point plus two digits. It does not round the ordinary positive decimal value. |
| `locationspage.swf`, LocationsPage.OnOutpostSelectionUpdated | Reads fProductionPerMin; calls RoundDecimalToFixedString(value, 2). |
| RoundDecimalToFixedString | Computes Math.round(value×10^precision)/10^precision, then toFixed(precision). |

Both normal and large menu variants were parsed and the relevant methods and
defaults independently checked by the original local verifier. The normal
workshop footer method is 621, code at decimal SWF offset 146831, ABC offset
122818, length 213 bytes; the local receipt supplies every selected method,
hash, pool identity and instruction offset. The endpoint and code-slice checks
validate the parser's selected inputs, not an independent runtime UI oracle.

Reproducible numerical illustration: binary32(60/36) is
1.6666666269302368. Passing that same ordinary value to the two algorithms gives
`1.66` and `1.67`. An integer 1 instead gives `1` and `1.00`, another discriminant.
The footer operation is string slicing, not a universal mathematical truncation
routine: scientific notation and unusual numeric values require separate rules.
No rendered-game equality was claimed from a Python illustration.

This evidence rejects the need for separate per-minute conversion formulas to
explain the paired hundredths, and establishes the installed formatting
difference within the named assets. Different snapshot epochs, cached values,
UI overrides and the screenshots' actual historical raw bits remain unmeasured.
A live experiment solely to rediscover the formatting difference is unnecessary;
freshness/actual realization is a separate [scientific question](arithmetic-live.md).
