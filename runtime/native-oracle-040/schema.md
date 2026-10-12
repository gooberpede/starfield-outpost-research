# Native grid schema4

Header is11 little-endian uint64 fields (88 bytes), then17 Blob records (1040 bytes
each): Event17768 bytes, unchanged binary layout from schema3. Header names:
sequence, invocation, parent, QPC, reference, context, thread, kind, status, MXCSR,
LastError. Blob: address uint64, length uint32, read-ok uint32, bytes[1024]. Failed
reads retain address/length and explicit false; zero-filled storage is not evidence.
Names/order remain ref/base/extra/cell/world/context_raw/source/candidate/translation/
landscape/center/input_hierarchy/floor_xy/result/block/merge/scale.

Kinds7–12 retain complete Q/E normal/unwind contracts from project030. Kinds1–6,
13–21 are retained regression code, not activated hooks in this candidate.

| Kind | Boundary and bytes |
|---|---|
|22/23/24|77FC20 enclosing begin/normal/unwind. input_hierarchy holds7 actual uint64 ABI arguments. reference is the selected/source argument4, context is output owner argument1. source copies request64 bytes, center copies output angle16 bytes, context_raw copies owner48 bytes. Entry output copies may be stale; they are never fresh results.|
|25/26|77DEF0 eligibility before/after; native AL is low8 of result RAX.|
|27/28|77F900 search before/after;6 raw arguments. center copies fifth-argument XYZ12 bytes. Normal result is reference RAX; ref blob copies that returned reference.|
|29/30|77E350 fallback before/after;5 raw arguments. center is fifth-argument XYZ; result RAX reference is distinct from shortcut.|
|31/32|96EB90 source before/after;3 raw arguments; candidate mutable44-byte hierarchy, center actual input angle16 bytes. Only after is a produced source.|
|33/34|96F5C0 generic grid before/after;3 raw arguments. candidate is actual mutable44-byte descriptor both phases, floor_xy signed int32 XY8 bytes, landscape96 bytes including resolution/body/system/index. center is chosen reference's parent world bytes (not a workshop center). result is RAX separately, never the native grid output.|
|35/36|96F940 displacement before/after;4 raw arguments. candidate=third hierarchy44, floor_xy=fourth hierarchy44, center=second output int32 pair8 bytes.|
|37/38|AD3B20 known-reference eligible-path site7800D6;3 raw arguments. candidate selected metadata48, floor_xy body uint32 output, center angle16 output.|
|45/46|AD3B20 exclusive direct-config site77FCE9. Same ABI; separately attributed from eligibility/search/fallback.|
|39|Any new route child unwind; status=original begin kind. No fabricated return/output.|
|40/41/44|17DFDF0 selected-reference sentinel begin/normal/unwind, active TLS ancestry. ref copies selected reference912 bytes. input_hierarchy stores6 slots: four real args plus two zero observer slots.|
|42/43/44|Explicit selected-reference AD3B20 observation; ref912 bytes, body4 and angles16. It does not create ancestry to a later producer by temporal proximity.|
|48/49/44|Explicit producer78B030 invocation: selected reference RDI and operation RSI observed by bridge at17DF4E2. input_hierarchy=[selected,manager,operation,request,body,out]. source=request64, candidate=operation144, floor_xy=body4. Actual four native arguments forwarded unchanged; active TLS parent encloses route.|

All route child invocations have unique IDs and parent=enclosing route, same thread;
call-return windows are bounded by the route. Q/E retain natural scope ancestry.
Selected lifetimes occupy TLS scopes, so synchronous sentinel/explicit producers
bind child route ancestry. A standalone operation and later equal-valued buffers
are not an ancestry join. Header reference in route children remains selected/source
argument4; **chosen** reference is owner+18 in context_raw and ref.address at grid.
Owner+20 residual XYZ is translation, not the workshop compensation vector.

Shared copies: ref/base/extra-bc/cell and manager current world are samples.
world is current manager+120 generated world, including packed+310; center at grid
is the chosen reference's exterior parent world, so distinct source/current frames
can be inspected. cell+110 retains that parent pointer. Extra-bc, when found, remains
separately sampled for saved association. No borrowed pointer is deferred to worker.
For route children, block is a derived16-byte contract: bytes0..3 native setting
storage, bytes4..7 original native read-ok uint32, bytes8..15 actual native CALL
return VA (subtract runtime module base and5 for RVA). Blob address retains the
native setting address; Blob ok describes the derived contract copy, not the
native read. Only original read-ok=1 permits setting bytes as evidence. A failed
native read retains false even though zero storage and CALL attribution are
readable. Other events retain the original4-byte native block Blob. merge/scale
retain native setting bytes. On child/selection unwind, status is assigned the
original begin kind after sampling; sample race/list status bits are not retained
in that unwind discriminator, while individual Blob validity is retained. Each direct helper wrapper has its own original CALL/relay guard.

Queue records own bytes. Raw records flush before their JSONL hash/extent/sequence
journal. Only newline-complete valid journal entries are recovered; orphan raw bytes
and incomplete journal tails are retained/reported. Sequence integrity is global
(sorted IDs, because concurrent queue publication may reorder reservations).
Per-invocation phase/thread/ancestry and source freshness must also reconcile.
Health counters count Q, E, and aggregate route/selection lifetimes, with independent
worker nonce acknowledgments. Stale/failed/unpaired/unknown provenance cannot become
scientific equivalence. STOP keeps edits resident/inert; original-byte restoration
is qualified only in disposable fixtures before their process exit.
