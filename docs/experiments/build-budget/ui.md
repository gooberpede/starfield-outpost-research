# The thin Build Limit footer bar

[Answer](report.md), [native accounting](native.md), [sources](sources.csv).
The supplied 1920x1080 screenshot `1716740_65.jpg` shows Build Limit at the lower
left beside Kreet Outpost 1, in the same footer that shows cargo/crew/power and
production. It is a location/appearance witness, with no matched raw budget,
epoch or build/configuration pin; no numerical bar reading is inferred.

Fresh read of pinned Interface.ba2 extracts **only** interface/workshopmenu.swf
into ignored `.local-work/l2-budget/WorkshopMenu.swf`, 100737 bytes, SHA256
`7f190c6753619b1646a1d3e360712ba93a653ef87f629d57501302fc714a5757`.
The adapted owned C1 nonexecuting ABC reader closes all 1527 bodies without an
unknown opcode. Interpretation is confined to the named footer methods.
No external decompiler, downloaded code or movie execution is used.

## Numerator, denominator and native cache

`140f4cb70` (n005/n023) reads current effective U and the same positive
WorkshopBudgetBaseline AV/fallback M as admission. If M==0 it returns 0;
otherwise **binary32 U/M**. There is no native min/max clamp and no selection
of draw versus triangle ratios. BudgetEnabled is not tested by this ratio
helper, so disabling accounting does not intrinsically clear an old meter.

`1421f2cb0` pops an 8-byte queued handle/refresh-mask request, resolves a valid
Workshop and ExtraBC, and for mask 0x10 (zero-based bit index 4) calls the ratio helper and stores
ExtraBC+90. Other refresh masks update power, production, cargo and crew.
It compares the old summary and emits status notification type 4 when budget
changes, or a broader summary notification when requested. This is summary
recalculation, not an item-population budget recount.

Add/subtract helpers explicitly emit underlying refresh event type 4; entry
`1421b64c0` emits type 5. Receiver `1421f2ac0`, bound by vtable 144d4b8d8+8,
maps type 4 to mask 0x10 and type 5 to mask 0x1f, merging flags for an already queued
owner handle. Pump `1421ba960` forwards to `1421f2cb0` (n018/n023-025).
The producer does not guarantee the
display cache has refreshed in the same instruction/frame as the AV write.

`140f34590` copies 24 summary bytes from +7c, or zeros for invalid context.
`14143f690` obtains them for the explicit Workshop or selected global
145f5d8e8 and queues an owned copy. `14143fdc0 -> 14143f8a0` forwards summary
float lane 5 (offset 14 hex) unchanged to the first float field of
WorkshopStatusData. `14143fb40` binds it as **fBuildLimit**.
`14143f450` publishes the WorkshopStatusData provider and subscribes to the
summary event; `14143fa60` receives it and invokes `14143f690`.

## Compiled render binding and full-state behavior

WorkshopMenu's FooterContainer constructor subscribes OnStatusDataUpdate to
WorkshopStatusData. ABC **method 621**, code bytes 0..34, does:

`Info_mc.BuildLimitMeter_mc.gotoAndStop(Math.round(framesLoaded * data.fBuildLimit))`.

Exact method byte offsets: get framesLoaded 19, get fBuildLimit 26, multiply 29,
round 30 and gotoAndStop 34. No ActionScript clamp or continuous fractional scale
is added in this handler. The constructor separately binds `$BUILD LIMIT`.

`timeline01.json` resolves the actual named instance through PlaceObject3 at
decompressed SWF offset 17794, owner sprite 141, to sprite **118** at 13569.
That sprite declares **100 frames** and contains exactly 100 ShowFrame tags.
Consequently U/M=1 requests frame 100; .995 also rounds to frame 100, even though
positive remaining capacity may still admit a small candidate. Values above 1
request above 100 and values near zero can request 0. Exact out-of-range handling
by Scaleform is left at that supported boundary; it was not invoked or inferred
from the screenshot. No claim of a particular overflow colour follows.

For the observed Kreet base usages and conditional M=2500, U=7/8/10/9 gives
ratios .0028/.0032/.004/.0036. All request frame 0 after rounding. This is an
explanation for very small constructions being visually unresolvable, **not**
a measurement of the attached image or a claim that its usage was one of these.
The saved counter and exact admission are more informative than that thin bar.

Rounding, pending summary refresh, the cached candidate charge and changed
allowance are four separate reasons for apparent meter/admission mismatch.
Historical UI freshness and arbitrary hot-setting behavior remain unobserved.
