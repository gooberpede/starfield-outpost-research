# Power and generator fuel

[Subject navigation and ABI limits](README.md) · [RVA index](index.md)

Entries use the pinned `Starfield.exe` 1.16.244.0 image. Internal-only observation. External invocation remains unvalidated.

Follow a mapped path

- [Electrical neighbor worklist](power.md#rva-0x00677c50)
- [Crew contribution](power.md#rva-0x00f3dd50)

## RVA 0x00030f50

**OpenCloseFormState string initializer** · Level B · preferred VA `0x140030f50`

Analysis labels recorded in the original sources are `FUN_140030f50`.

Recorded scope — OpenCloseFormState string initializer

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 281).

- **Inputs** — Static initialization
- **Outputs** — Query key binding
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Does not prove an authoritative Papyrus property
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 281) · `N280`

## RVA 0x000391d0

**Open animation variable initializer** · Level B · preferred VA `0x1400391d0`

Analysis labels recorded in the original sources are `FUN_1400391d0`.

Recorded scope — Open animation variable initializer

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 282).

- **Inputs** — Static initialization
- **Outputs** — Animation variable key
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — State binding separate from powered
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 282) · `N281`

## RVA 0x00039200

**Close animation variable initializer** · Level B · preferred VA `0x140039200`

Analysis labels recorded in the original sources are `FUN_140039200`.

Recorded scope — Close animation variable initializer

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 283).

- **Inputs** — Static initialization
- **Outputs** — Animation variable key
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — State binding separate from powered
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 283) · `N282`

## RVA 0x0003e540

**Initialize the queue-selection default** · Level C · preferred VA `0x14003e540`

Recorded scope — Initialize the queue-selection default

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 135)

## RVA 0x0003e570

**Initialize a Workshop power default object** · Level C · preferred VA `0x14003e570`

Recorded scope — Initialize a Workshop power default object

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 49)

## RVA 0x0009bc60

**Initialize the power route keyword default object** · Level C · preferred VA `0x14009bc60`

Recorded scope — Initialize the power route keyword default object

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 221)

## RVA 0x002cee60

**saved reference to current validated handle restoration** · Level B · preferred VA `0x1402cee60`

Analysis labels recorded in the original sources are `FUN_1402cee60`.

Recorded scope — saved reference to current validated handle restoration

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 304).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 304) · `N303`

## RVA 0x002cef80

**saved FormID remap and reference lookup** · Level B · preferred VA `0x1402cef80`

Analysis labels recorded in the original sources are `FUN_1402cef80`.

Recorded scope — saved FormID remap and reference lookup

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 305).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 305) · `N304`
- [docs · function register](../function-register.md) (line 112) · `SOR-FN-0049`
  Original group scope — Workshop resource-prefix loading path

## RVA 0x002cf060

**validated reference handle callback** · Level B · preferred VA `0x1402cf060`

Analysis labels recorded in the original sources are `FUN_1402cf060`.

Recorded scope — validated reference handle callback

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 298).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 298) · `N297`
- [power · load determinism](../experiments/power/load-determinism.md) (line 54)
  Original report discusses this roster entry under Pinned evidence and identity correction.

## RVA 0x0038a200

**forward value assignment to AV base setter** · Level B · preferred VA `0x14038a200`

Analysis labels recorded in the original sources are `FUN_14038a200`.

Recorded scope — forward value assignment to AV base setter

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 262).

- **Inputs** — AV owner; AV; value
- **Outputs** — Virtual+20 assignment
- **Conditions** — Pinned retail 1.16.244.0; Persisted ExtraBF base write path
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 262) · `N261`
- [build budget · functions](../experiments/build-budget/functions.csv) (line 76)
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 12)

## RVA 0x0050feb0

**ExtraAction bit clearing** · Level B · preferred VA `0x14050feb0`

Analysis labels recorded in the original sources are `FUN_14050feb0`.

Recorded scope — ExtraAction bit clearing

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 277).

- **Inputs** — Extra list; reference; mask
- **Outputs** — Cleared action flags
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Not a getter or direct serialized payload
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 277) · `N276`

## RVA 0x0050ffe0

**default-open saved-difference restore** · Level B · preferred VA `0x14050ffe0`

Analysis labels recorded in the original sources are `FUN_14050ffe0`.

Recorded scope — default-open saved-difference restore

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 288).

- **Inputs** — Extra list and saved 400000 caller
- **Outputs** — Restored default bit
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Native mutator; no direct Extra0D save payload
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 288) · `N287`
- [power · followup](../experiments/power/followup.md) (line 208) · Toggle saved-reference extra flag
  Invoked by reference restore when change mask 0x400000 is present.

## RVA 0x00518750

**reverse4D deduplicating append** · Level B · preferred VA `0x140518750`

Analysis labels recorded in the original sources are `FUN_140518750`.

Recorded scope — reverse4D deduplicating append

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 296).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 296) · `N295`

## RVA 0x00526bb0

**post-load forward to reverse ownership rebuilding** · Level B · preferred VA `0x140526bb0`

Analysis labels recorded in the original sources are `FUN_140526bb0`.

Recorded scope — post-load forward to reverse ownership rebuilding

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 295).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 295) · `N294`

## RVA 0x005315c0

**Enter the alternate association insertion route** · Level C · preferred VA `0x1405315c0`

Recorded scope — Enter the alternate association insertion route

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 72)

## RVA 0x005407b0

**Dispatch direct or queued association insertion** · Level C · preferred VA `0x1405407b0`

Recorded scope — Dispatch direct or queued association insertion

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 72)

## RVA 0x00540a90

**Forward the alternate association route** · Level C · preferred VA `0x140540a90`

Recorded scope — Forward the alternate association route

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 72)

## RVA 0x005431d0

**ExtraPowerLinks obtain or create** · Level B · preferred VA `0x1405431d0`

Analysis labels recorded in the original sources are `FUN_1405431d0`.

Recorded scope — ExtraPowerLinks obtain or create

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 244).

- **Inputs** — Extra list
- **Outputs** — ExtraCB object
- **Conditions** — Pinned retail 1.16.244.0; May allocate and mutate extra list
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 244) · `N243`
- [power · native](../experiments/power/native.md) (line 100) · Get linked-ref extra data
  CB extra exposes count at +0x18, capacity +0x1c and array pointer +0x20.

## RVA 0x00543c80

**Process queued association insertion** · Level C · preferred VA `0x140543c80`

Recorded scope — Process queued association insertion

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 72)

## RVA 0x00545e40

**Extra9C flag restoration** · Level B · preferred VA `0x140545e40`

Analysis labels recorded in the original sources are `FUN_140545e40`.

Recorded scope — Extra9C flag restoration

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 294).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 294) · `N293`
- [power · saved](../experiments/power/saved.md) (line 186) · Apply restored extra flags
  Invoked by the ExtraFlags case; historical power bit is a saved observation.

## RVA 0x00580d20

**global0A saved notification list restoration** · Level B · preferred VA `0x140580d20`

Analysis labels recorded in the original sources are `FUN_140580d20`.

Recorded scope — global0A saved notification list restoration

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 302).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 302) · `N301`

## RVA 0x005810b0

**global0A finish object-loaded notifications** · Level B · preferred VA `0x1405810b0`

Analysis labels recorded in the original sources are `FUN_1405810b0`.

Recorded scope — global0A finish object-loaded notifications

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 303).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 303) · `N302`

## RVA 0x005893c0

**Visit the cell-finish notification path** · Level C · preferred VA `0x1405893c0`

Recorded scope — Visit the cell-finish notification path

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 261)

## RVA 0x005a0520

**Enter a forward-derived reconstruction path** · Level C · preferred VA `0x1405a0520`

Recorded scope — Enter a forward-derived reconstruction path

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 72)
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 17)

## RVA 0x005afea0

**Process association during reconstruction** · Level C · preferred VA `0x1405afea0`

Recorded scope — Process association during reconstruction

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 72)

## RVA 0x005ccd00

**settled open-close action completion** · Level B · preferred VA `0x1405ccd00`

Analysis labels recorded in the original sources are `FUN_1405ccd00`.

Recorded scope — settled open-close action completion

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 286).

- **Inputs** — Reference and desired state
- **Outputs** — Settled action bit
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Does not by itself determine all getter overrides
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 286) · `N285`

## RVA 0x005cd370

**reference open-close state setter** · Level B · preferred VA `0x1405cd370`

Analysis labels recorded in the original sources are `FUN_1405cd370`.

Recorded scope — reference open-close state setter

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 284).

- **Inputs** — Reference; desired state; animation/snap options
- **Outputs** — Action state and queued work
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Mutator; not safe arbitrary invocation
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 284) · `N283`
- [power · followup](../experiments/power/followup.md) (line 192) · Set initial open-close action state
  Selects bit set/clear helpers and can queue completion.

## RVA 0x005cd7a0

**open-close action animation dispatch** · Level B · preferred VA `0x1405cd7a0`

Analysis labels recorded in the original sources are `FUN_1405cd7a0`.

Recorded scope — open-close action animation dispatch

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 285).

- **Inputs** — Reference; available animation interfaces
- **Outputs** — Dispatched actions
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Current state includes transition timing
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 285) · `N284`
- [power · followup](../experiments/power/followup.md) (line 197) · Dispatch open-close follow-up
  Part of action-state processing after update.

## RVA 0x005cdc70

**Read supported open-close state** · Level C · preferred VA `0x1405cdc70`

Recorded scope — Electrical gate excludes state one; the general switch semantics remain bounded.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 214)

## RVA 0x0065bc30

**Load linked refs from definition** · Level C · preferred VA `0x14065bc30`

Recorded scope — Game-file XPLK is a different input channel from save restoration.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 121)

## RVA 0x0065be30

**load saved electrical entries** · Level B · preferred VA `0x14065be30`

Analysis labels recorded in the original sources are `FUN_14065be30`.

Recorded scope — load saved electrical entries

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 246).

- **Inputs** — ExtraCB; save reader
- **Outputs** — Restored identity-word array
- **Conditions** — Pinned retail 1.16.244.0; Count; translated reference reads; four-byte word
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 246) · `N245`
- [power · saved](../experiments/power/saved.md) (line 144) · Restore saved linked-ref array
  Reads packed count and fills each stride-eight entry with remapped ID plus word.

## RVA 0x0065bf00

**Insert linked-ref pair under protection** · Level C · preferred VA `0x14065bf00`

Recorded scope — Uses an extra-list lock before membership insertion.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 102)

## RVA 0x0065bfc0

**Remove linked-ref membership** · Level C · preferred VA `0x14065bfc0`

Recorded scope — Removal preserves survivor order on the observed path.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 103)

## RVA 0x0065c1b0

**copy restored electrical array** · Level B · preferred VA `0x14065c1b0`

Analysis labels recorded in the original sources are `FUN_14065c1b0`.

Recorded scope — copy restored electrical array

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 247).

- **Inputs** — Source and destination arrays
- **Outputs** — Success low byte
- **Conditions** — Pinned retail 1.16.244.0; Stride 8 copy; allocation; not final handle fixup
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 247) · `N246`
- [power · saved](../experiments/power/saved.md) (line 155) · Copy saved linked-ref array
  Copies restored stride-eight arrays, independently of later runtime graph use.

## RVA 0x0065c2f0

**insert electrical membership** · Level B · preferred VA `0x14065c2f0`

Analysis labels recorded in the original sources are `FUN_14065c2f0`.

Recorded scope — insert electrical membership

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 245).

- **Inputs** — Extra list; reference and connection word
- **Outputs** — Array upsert
- **Conditions** — Pinned retail 1.16.244.0; Locks list; deduplicates full handle-word pair
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 297).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 245) · `N244`
- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 297) · `N296` · ExtraCB FormID entry insertion
- [power · native](../experiments/power/native.md) (line 102) · Append unique linked-ref pair
  Deduplicates the full FormID and relationship word.

## RVA 0x00668130

**Interpolate wire cable geometry** · Level C · preferred VA `0x140668130`

Recorded scope — Uses wire length setting for bend or sag, independently of endpoint policy.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 90)

## RVA 0x00668380

**Resolve spline endpoint** · Level C · preferred VA `0x140668380`

Recorded scope — Recovers one endpoint of a cable spline.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 119)

## RVA 0x00668560

**Interpolate cable sag** · Level C · preferred VA `0x140668560`

Recorded scope — Uses wire length setting in presentation geometry.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 90)

## RVA 0x00668fa0

**Test simple relationship words** · Level C · preferred VA `0x140668fa0`

Recorded scope — With mode 1, checks whether all connection words equal one.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 156)

## RVA 0x00669090

**Look up existing wire connection** · Level C · preferred VA `0x140669090`

Recorded scope — Called from endpoint-pair qualification.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 62)

## RVA 0x00669670

**connection-and-receiver predicate** · Level B · preferred VA `0x140669670`

Analysis labels recorded in the original sources are `FUN_140669670`.

Recorded scope — connection-and-receiver predicate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 236).

- **Inputs** — Reference
- **Outputs** — Boolean low byte
- **Conditions** — Pinned retail 1.16.244.0; Effective AV and Workshop exclusion
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 236) · `N235`
- [power · native](../experiments/power/native.md) (line 42) · Classify power receiver
  Checks effective receiver actor value and has a Workshop-base exclusion branch.

## RVA 0x00669700

**electrical endpoint predicate** · Level B · preferred VA `0x140669700`

Analysis labels recorded in the original sources are `FUN_140669700`.

Recorded scope — electrical endpoint predicate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 237).

- **Inputs** — Reference
- **Outputs** — Boolean low byte
- **Conditions** — Pinned retail 1.16.244.0; Effective connection AV; keyword; receiver
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 237) · `N236`
- [power · native](../experiments/power/native.md) (line 43) · Classify power connector
  Tests effective connection value, connection keyword or receiver classification.

## RVA 0x006697f0

**nominal generator predicate** · Level B · preferred VA `0x1406697f0`

Analysis labels recorded in the original sources are `FUN_1406697f0`.

Recorded scope — nominal generator predicate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 238).

- **Inputs** — Reference
- **Outputs** — Boolean low byte
- **Conditions** — Pinned retail 1.16.244.0; Positive base PowerGenerated
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 238) · `N237`
- [power · native](../experiments/power/native.md) (line 44) · Classify nominal generator
  Tests positive base PowerGenerated under Workshop-base exclusion.

## RVA 0x00669880

**conditional generator contribution** · Level B · preferred VA `0x140669880`

Analysis labels recorded in the original sources are `FUN_140669880`.

Recorded scope — conditional generator contribution

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 239).

- **Inputs** — Reference and Workshop/crew context
- **Outputs** — Nonnegative binary32 contribution
- **Conditions** — Pinned retail 1.16.244.0; Base and three AV modifiers; crew entry DB
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 239) · `N238`
- [power · native](../experiments/power/native.md) (line 257) · Calculate conditional power contribution
  Supplies one nonnegative contribution, independent of a given consumer's reachability.
- [robots · functions](../experiments/robots/functions.csv) (line 8) · preliminary power gate then DB
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 16)
- [crew skills · native](../experiments/crew-skills/native.md) (line 31)
  Original report discusses this roster entry under DB: additive power on each generator.
- [crew skills · processes](../experiments/crew-skills/processes.md) (line 12)
  Original report discusses this roster entry under processes.
- [robots · effects](../experiments/robots/effects.md) (line 53)
  Original report discusses this roster entry under effects.

## RVA 0x006699b0

**radiation predicate** · Level B · preferred VA `0x1406699b0`

Analysis labels recorded in the original sources are `FUN_1406699b0`.

Recorded scope — radiation predicate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 240).

- **Inputs** — Reference
- **Outputs** — Boolean
- **Conditions** — Pinned retail 1.16.244.0; Base PowerRadiation and special exclusion
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 240) · `N239`
- [power · native](../experiments/power/native.md) (line 45) · Classify power radiation
  Tests positive base radiation and a separate reference predicate.

## RVA 0x00669a10

**Classify snap power propagation** · Level C · preferred VA `0x140669a10`

Recorded scope — Tests effective snap-transmits-power value.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 46)

## RVA 0x00669a60

**Classify demand-side candidate** · Level C · preferred VA `0x140669a60`

Recorded scope — Checks applicable nonconnector/receiver with graph exclusions.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 47)

## RVA 0x00669ac0

**allocation node exclusion** · Level B · preferred VA `0x140669ac0`

Analysis labels recorded in the original sources are `FUN_140669ac0`.

Recorded scope — allocation node exclusion

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 241).

- **Inputs** — Reference and optional state override
- **Outputs** — Boolean low byte
- **Conditions** — Pinned retail 1.16.244.0; Invalidity; activation query; fuel suppression
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 241) · `N240`
- [power · native](../experiments/power/native.md) (line 212) · Gate electrical contribution by state
  Handles invalid references, category exemptions and a supported activator state.

## RVA 0x00669c60

**electrical partition gate** · Level B · preferred VA `0x140669c60`

Analysis labels recorded in the original sources are `FUN_140669c60`.

Recorded scope — electrical partition gate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 253).

- **Inputs** — Restriction bytes; source; target-spline-word descriptor
- **Outputs** — Boolean
- **Conditions** — Pinned retail 1.16.244.0; Restricted direct word 1 edges fail; spline bypass
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 253) · `N252`
- [power · native](../experiments/power/native.md) (line 138) · Apply graph partition gate
  Shared by recursion and queue-based traversal.

## RVA 0x00669d60

**Create reciprocal simple power memberships** · Level C · preferred VA `0x140669d60`

Recorded scope — Word 1 can associate a Workshop beacon; includes radiating generators under scoped guards.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 112)

## RVA 0x00669ff0

**Gather simple or snap power candidates** · Level C · preferred VA `0x140669ff0`

Recorded scope — Collects candidates by the documented relationship classes.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 124)

## RVA 0x0066abc0

**apply inverse unpowered flag** · Level B · preferred VA `0x14066abc0`

Analysis labels recorded in the original sources are `FUN_14066abc0`.

Recorded scope — apply inverse unpowered flag

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 256).

- **Inputs** — Reference; unpowered byte
- **Outputs** — ExtraFlags mask 40 and event consequences
- **Conditions** — Pinned retail 1.16.244.0; Mutates; marks changed; producer and animation refresh
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 256) · `N255`
- [power · native](../experiments/power/native.md) (line 237) · Write inverse powered flag
  Writes ExtraFlags mask 0x40 using the mode supplied by powered-set differencing.

## RVA 0x0066b100

**electrical cumulative allocator** · Level B · preferred VA `0x14066b100`

Analysis labels recorded in the original sources are `FUN_14066b100`.

Recorded scope — electrical cumulative allocator

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 248).

- **Inputs** — Root reference; caller result set; optional override
- **Outputs** — Powered-reference set
- **Conditions** — Pinned retail 1.16.244.0; Component supply; discovery-order base demand; visited set
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 248) · `N247`
- [power · native](../experiments/power/native.md) (line 168) · Allocate connected power supply
  Uses gathered supply and ordered demands; does not choose globally smallest fitting demand.

## RVA 0x0066bad0

**simple radiating connector exclusion** · Level B · preferred VA `0x14066bad0`

Analysis labels recorded in the original sources are `FUN_14066bad0`.

Recorded scope — simple radiating connector exclusion

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 242).

- **Inputs** — Reference
- **Outputs** — Boolean
- **Conditions** — Pinned retail 1.16.244.0; Nonproducer radiator with only unresolved/simple nonspline links
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 242) · `N241`
- [power · native](../experiments/power/native.md) (line 160) · Recognize generation-side category
  Includes a non-generating radiating class under the documented guards.

## RVA 0x0066bcb0

**Accumulate generation during traversal** · Level C · preferred VA `0x14066bcb0`

Recorded scope — Callback used to collect generation contributions.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 258)

## RVA 0x0066bd50

**wire pair admission predicate** · Level B · preferred VA `0x14066bd50`

Analysis labels recorded in the original sources are `FUN_14066bd50`.

Recorded scope — wire pair admission predicate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 243).

- **Inputs** — Two resolved references
- **Outputs** — Boolean low byte
- **Conditions** — Pinned retail 1.16.244.0; Both endpoints connect; absent or word 1 prior edge
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 243) · `N242`
- [power · native](../experiments/power/native.md) (line 61) · Test proposed wire endpoint pair
  Both reference operands must qualify as connectors; consults existing connection.

## RVA 0x0066bec0

**Test explicit word-3 relationship** · Level C · preferred VA `0x14066bec0`

Recorded scope — Inspects the matching resolved entry for exact word 3.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 155)

## RVA 0x0066bfc0

**connect electrical graph and reallocate** · Level B · preferred VA `0x14066bfc0`

Analysis labels recorded in the original sources are `FUN_14066bfc0`.

Recorded scope — connect electrical graph and reallocate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 254).

- **Inputs** — Two endpoints; word; optional spline
- **Outputs** — Mutated graph and power state
- **Conditions** — Pinned retail 1.16.244.0; Reciprocal memberships; power events; reference cleanup
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 254) · `N253`
- [power · native](../experiments/power/native.md) (line 81) · Add electrical connection
  Called with two endpoint references, relationship word and optional spline.

## RVA 0x0066c4f0

**Participate in the power AV modifier caller set** · Level C · preferred VA `0x14066c4f0`

Recorded scope — Participate in the power AV modifier caller set

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · followup](../experiments/power/followup.md) (line 56)

## RVA 0x0066ccd0

**Participate in the power AV modifier caller set** · Level C · preferred VA `0x14066ccd0`

Recorded scope — Participate in the power AV modifier caller set

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · followup](../experiments/power/followup.md) (line 56)

## RVA 0x0066d4b0

**Refresh owner-linked power components** · Level C · preferred VA `0x14066d4b0`

Recorded scope — Recomputes affected components for selected owner-linked roots.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 241)

## RVA 0x0066d890

**Participate in the power AV modifier caller set** · Level C · preferred VA `0x14066d890`

Recorded scope — Participate in the power AV modifier caller set

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · followup](../experiments/power/followup.md) (line 56)

## RVA 0x0066e9b0

**remove electrical connection and reallocate** · Level B · preferred VA `0x14066e9b0`

Analysis labels recorded in the original sources are `FUN_14066e9b0`.

Recorded scope — remove electrical connection and reallocate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 255).

- **Inputs** — Two references
- **Outputs** — Mutated graph and power state
- **Conditions** — Pinned retail 1.16.244.0; Deletes memberships/splines; recomputes sets
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 255) · `N254`
- [power · native](../experiments/power/native.md) (line 85) · Remove electrical connection
  Invoked by replacement and participates in affected-component recomputation.

## RVA 0x0066f3e0

**Create automatic graph relationships** · Level C · preferred VA `0x14066f3e0`

Recorded scope — Creates relationship word 2 across classified categories.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 113)

## RVA 0x0066f880

**schedule power recomputation** · Level B · preferred VA `0x14066f880`

Analysis labels recorded in the original sources are `FUN_14066f880`.

Recorded scope — schedule power recomputation

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 257).

- **Inputs** — Reference; optional override
- **Outputs** — Direct or queued worker
- **Conditions** — Pinned retail 1.16.244.0; Engine-thread scheduling and handle conversion
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 257) · `N256`
- [power · native](../experiments/power/native.md) (line 235) · Schedule electrical recomputation
  Runs directly or queues an engine-thread worker.

## RVA 0x0066fa50

**recompute powered set differences** · Level B · preferred VA `0x14066fa50`

Analysis labels recorded in the original sources are `FUN_14066fa50`.

Recorded scope — recompute powered set differences

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 258).

- **Inputs** — Request with root handle and optional override
- **Outputs** — Power changes
- **Conditions** — Pinned retail 1.16.244.0; Old/new set differences; event emission
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 258) · `N257`
- [power · native](../experiments/power/native.md) (line 236) · Apply old/new powered-set differences
  Newly and formerly powered references flow to the inverse bit setter.

## RVA 0x006700f0

**Resolve paired spline endpoint** · Level C · preferred VA `0x1406700f0`

Recorded scope — Participates in recovering the two cable endpoints.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 119)

## RVA 0x00671f70

**generation traversal dispatcher** · Level B · preferred VA `0x140671f70`

Analysis labels recorded in the original sources are `FUN_140671f70`.

Recorded scope — generation traversal dispatcher

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 249).

- **Inputs** — Root; override; output operands
- **Outputs** — Collection and supply via outputs
- **Conditions** — Pinned retail 1.16.244.0; Setting chooses queue or recursive route
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 249) · `N248`
- [power · native](../experiments/power/native.md) (line 133) · Collect generation-side component
  Collects eligible generators and totals their qualified supply.

## RVA 0x006722f0

**Append eligible allocation neighbors** · Level C · preferred VA `0x1406722f0`

Recorded scope — Supports the allocator's second-stage increasing-index walk.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · followup](../experiments/power/followup.md) (line 102)

## RVA 0x006728e0

**owner reverse-link generator root collector** · Level B · preferred VA `0x1406728e0`

Analysis labels recorded in the original sources are `FUN_1406728e0`.

Recorded scope — owner reverse-link generator root collector

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 271).

- **Inputs** — Owner extra list; current handles; Workshop keyword
- **Outputs** — Ordered generator roots
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Root order is runtime reverse-list order; not serialized 4C order
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 271) · `N270`
- [power · followup](../experiments/power/followup.md) (line 61) · Collect owner-linked generator roots
  Filters resolved stride-0x10 entries by keyword and nominal-generator predicate.

## RVA 0x00675c50

**queue generation traversal** · Level B · preferred VA `0x140675c50`

Analysis labels recorded in the original sources are `FUN_140675c50`.

Recorded scope — queue generation traversal

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 250).

- **Inputs** — Root and traversal/output state
- **Outputs** — Deduplicated generators and binary32 supply
- **Conditions** — Pinned retail 1.16.244.0; Visited handles; edge gate; contribution helper
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 250) · `N249`
- [power · native](../experiments/power/native.md) (line 135) · Traverse generation graph with pending queue
  Default-true setting uses the pending queue and visited checks.

## RVA 0x00676350

**Traverse generation graph recursively** · Level C · preferred VA `0x140676350`

Recorded scope — Alternate setting uses recursive traversal.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 136)

## RVA 0x006779e0

**enumerate electrical neighbors** · Level B · preferred VA `0x1406779e0`

Analysis labels recorded in the original sources are `FUN_1406779e0`.

Recorded scope — enumerate electrical neighbors

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 251).

- **Inputs** — Reference and traversal context
- **Outputs** — Queued qualified neighbors
- **Conditions** — Pinned retail 1.16.244.0; Resolves direct/spline links
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 251) · `N250`
- [power · native](../experiments/power/native.md) (line 144) · Enumerate electrical graph neighbors
  Uses stored CB entry order and resolves direct or spline endpoints.

## RVA 0x00677c50

**Handle pending and unseen electrical neighbor identities** · Level B · preferred VA `0x140677c50`

Analysis labels recorded in the original sources are `FUN_140677c50`.

Promotes an already queued neighbor or evaluates an unseen neighbor's edge.

The earlier static contract identified visited, queued and edge checks. The follow-up resolves the intervening branch. An already pending identity moves to the front before the unseen-neighbor edge gate. An earlier queue insertion therefore does not imply FIFO discovery order. Effective connection predicates, actual restored component state and current runtime ordering remain source-scoped.

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 252).

- **Inputs** — Traversal state; target; optional spline; word
- **Outputs** — Traversal continuation
- **Conditions** — Pinned retail 1.16.244.0; Visited/queued identity and edge filtering
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 252) · `N251` · enqueue electrical neighbor
- [power · followup](../experiments/power/followup.md) (line 75)
  Promotes an already queued neighbor or evaluates an unseen neighbor's edge.
- [power · followup](../experiments/power/followup.md) (line 85)
  Promotes an already queued neighbor or evaluates an unseen neighbor's edge.
- [power · native](../experiments/power/native.md) (line 145) · Schedule eligible graph neighbor
  Checks visited and queued identities, then admits via edge gate.

## RVA 0x00678f60

**Resolve recursive graph neighbors** · Level C · preferred VA `0x140678f60`

Recorded scope — Follows direct and spline endpoints.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 136)

## RVA 0x006791d0

**Recurse to eligible graph neighbor** · Level C · preferred VA `0x1406791d0`

Recorded scope — Applies partition gate and visited check before recursion.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 137)

## RVA 0x006797c0

**generation pending front insertion** · Level B · preferred VA `0x1406797c0`

Analysis labels recorded in the original sources are `FUN_1406797c0`.

Recorded scope — generation pending front insertion

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 273).

- **Inputs** — Initialized deque; handle identity
- **Outputs** — Front handle insertion
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Not FIFO append
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 273) · `N272`
- [power · followup](../experiments/power/followup.md) (line 82) · Push pending graph handle to front
  Decrements front index +0x18 and increments count +0x20.

## RVA 0x00679890

**pending range rotation** · Level B · preferred VA `0x140679890`

Analysis labels recorded in the original sources are `FUN_140679890`.

Recorded scope — pending range rotation

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 274).

- **Inputs** — Deque iterators begin / found / found+1
- **Outputs** — Already pending target promoted to front
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Use instruction arguments; decompiler loses iterator fields
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 274) · `N273`
- [power · followup](../experiments/power/followup.md) (line 89) · Rotate already-pending graph handle
  Uses begin, found and found+1 boundaries.

## RVA 0x00922b30

**Resolve the child handle in open-state follow-up** · Level C · preferred VA `0x140922b30`

Recorded scope — Resolve the child handle in open-state follow-up

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · followup](../experiments/power/followup.md) (line 118)

## RVA 0x00a74420

**switch activation category predicate** · Level B · preferred VA `0x140a74420`

Analysis labels recorded in the original sources are `FUN_140a74420`.

Recorded scope — switch activation category predicate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 270).

- **Inputs** — ACTI or MSTT base
- **Outputs** — Boolean
- **Conditions** — Pinned retail 1.16.244.0; Default keyword at 145eaad58; subtype checks
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 270) · `N269`

## RVA 0x00afe0d0

**Continue initialization association** · Level C · preferred VA `0x140afe0d0`

Recorded scope — Continue initialization association

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 72)

## RVA 0x00b02630

**Conditionally emit the loaded reference event** · Level C · preferred VA `0x140b02630`

Recorded scope — Conditionally emit the loaded reference event

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 111)

## RVA 0x00b0fd40

**Process reference attach association** · Level C · preferred VA `0x140b0fd40`

Recorded scope — Process reference attach association

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 72)

## RVA 0x00b11780

**Process the cell-attach callback** · Level C · preferred VA `0x140b11780`

Recorded scope — Process the cell-attach callback

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 110)

## RVA 0x00b19a60

**Initialize the reference association path** · Level C · preferred VA `0x140b19a60`

Recorded scope — Initialize the reference association path

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 72)

## RVA 0x00b1e190

**cell reference pointer-array visitor** · Level B · preferred VA `0x140b1e190`

Analysis labels recorded in the original sources are `FUN_140b1e190`.

Recorded scope — cell reference pointer-array visitor

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 309).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 309) · `N308`
- [docs · function register](../function-register.md) (line 78–83) · `SOR-FN-0055`
  Original group scope — Terrain coverage route stage

## RVA 0x00b230a0

**reference definition subrecord loader** · Level B · preferred VA `0x140b230a0`

Analysis labels recorded in the original sources are `FUN_140b230a0`.

Recorded scope — reference definition subrecord loader

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 293).

- **Inputs** — Definition REFR input and initialized reference
- **Outputs** — Original default-open bit
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Bounded ONAM interpretation; not all definition grammar
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 293) · `N292`
- [power · followup](../experiments/power/followup.md) (line 206) · Load reference definition
  ONAM sets extra flag mask 0x08 in the observed definition path.

## RVA 0x00b29470

**reference original default-open helper** · Level B · preferred VA `0x140b29470`

Analysis labels recorded in the original sources are `FUN_140b29470`.

Recorded scope — reference original default-open helper

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 287).

- **Inputs** — Current reference and change-record manager
- **Outputs** — Default Boolean
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Separate from current-open difference 800000
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 287) · `N286`
- [power · followup](../experiments/power/followup.md) (line 204) · Get default reference change flags
  Evidence distinguishes two change-mask branches.

## RVA 0x00b29700

**reference save-body dispatcher** · Level B · preferred VA `0x140b29700`

Analysis labels recorded in the original sources are `FUN_140b29700`.

Recorded scope — reference save-body dispatcher

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 289).

- **Inputs** — Reference; save buffer; change flags
- **Outputs** — Serialized reference body
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Open-state difference is carried by change mask
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 289) · `N288`
- [power · followup](../experiments/power/followup.md) (line 211) · Serialize changed reference state
  For the documented state branch, change flags carry the distinction without a separate 0x800000 body payload.
- [storage · functions](../experiments/storage/functions.csv) (line 34) · `S1-033` · reference inventory change serialization gate
- [storage · native](../experiments/storage/native.md) (line 202)
  Original report discusses this roster entry under Link and inventory persistence are separate.

## RVA 0x00b29990

**reference saved-state restore dispatcher** · Level B · preferred VA `0x140b29990`

Analysis labels recorded in the original sources are `FUN_140b29990`.

Recorded scope — reference saved-state restore dispatcher

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 290).

- **Inputs** — Reference; load buffer; change flags
- **Outputs** — Restored extra/default data
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Does not certify final post-load getter or graph order
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 290) · `N289`
- [experiments · active outpost identification](../experiments/active-outpost-identification.md) (line 54) · Load changed reference
  Calls saved form flag reader in the REFR load path.
- [power · followup](../experiments/power/followup.md) (line 207) · Restore saved reference state
  Uses saved change flags to restore per-reference fields.
- [construction variants · functions](../experiments/construction-variants/functions.csv) (line 60)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 15)

## RVA 0x00b2bc70

**reference post-load open-state reconstruction** · Level B · preferred VA `0x140b2bc70`

Analysis labels recorded in the original sources are `FUN_140b2bc70`.

Recorded scope — reference post-load open-state reconstruction

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 291).

- **Inputs** — Supported base; default and change flags; animation
- **Outputs** — Restored action/animation branch
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Bad recovered large switch; use o009 instruction windows; transition can defer
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 291) · `N290`
- [power · followup](../experiments/power/followup.md) (line 213) · Reconstruct reference action after load
  Applies animation/action state after saved field restoration.
- [spatial placement · functions](../experiments/spatial-placement/functions.csv) (line 111)

## RVA 0x00b3cbc0

**reference initialization open-state request** · Level B · preferred VA `0x140b3cbc0`

Analysis labels recorded in the original sources are `FUN_140b3cbc0`.

Recorded scope — reference initialization open-state request

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 292).

- **Inputs** — Reference; current load/reset conditions
- **Outputs** — Open-close initialization
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Not universal settled state certification
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 292) · `N291`
- [power · followup](../experiments/power/followup.md) (line 218) · Route load or reset action initialization
  Invokes the open-close state initializer.

## RVA 0x00b40430

**Emit the loaded-reference event from a move or 3D path** · Level C · preferred VA `0x140b40430`

Recorded scope — Emit the loaded-reference event from a move or 3D path

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 113)

## RVA 0x00b40660

**Check whether to admit the loaded reference** · Level C · preferred VA `0x140b40660`

Recorded scope — Check whether to admit the loaded reference

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 112)

## RVA 0x00b47420

**ExtraAction bit set and current-open difference marking** · Level B · preferred VA `0x140b47420`

Analysis labels recorded in the original sources are `FUN_140b47420`.

Recorded scope — ExtraAction bit set and current-open difference marking

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 275).

- **Inputs** — Reference; extra lock; mask
- **Outputs** — Updated action and change state
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Mutator; save bit differs from powered 40
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 275) · `N274`
- [power · followup](../experiments/power/followup.md) (line 193) · Set reference ExtraAction bit
  Used with mask four by the documented open-close setter.

## RVA 0x00b475b0

**ExtraAction bit clear and current-open difference marking** · Level B · preferred VA `0x140b475b0`

Analysis labels recorded in the original sources are `FUN_140b475b0`.

Recorded scope — ExtraAction bit clear and current-open difference marking

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 276).

- **Inputs** — Reference; extra list; mask
- **Outputs** — Updated action and change state
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Cell/template exclusions apply
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 276) · `N275`
- [power · followup](../experiments/power/followup.md) (line 193) · Clear reference ExtraAction bit
  Used with mask four by the documented open-close setter.

## RVA 0x00b58cf0

**Apply the cell-finish visitor predicate** · Level C · preferred VA `0x140b58cf0`

Analysis labels recorded in the original sources are `FUN_140b58cf0`.

Recorded scope — Apply the cell-finish visitor predicate

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 262)
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 232)

## RVA 0x00b5c350

**finish cell visitor deferred notification** · Level B · preferred VA `0x140b5c350`

Analysis labels recorded in the original sources are `FUN_140b5c350`.

Recorded scope — finish cell visitor deferred notification

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 310).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 310) · `N309`
- [power · load determinism](../experiments/power/load-determinism.md) (line 261) · Check reference flags during the cell-finish notification
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 226)

## RVA 0x00b6d720

**restore AV negative modifier** · Level B · preferred VA `0x140b6d720`

Analysis labels recorded in the original sources are `FUN_140b6d720`.

Recorded scope — restore AV negative modifier

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 261).

- **Inputs** — AV owner; target AV and amount
- **Outputs** — Modifier restoration
- **Conditions** — Pinned retail 1.16.244.0; State mutation; fuel calls with base rating
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 261) · `N260`
- [fuel · functions](../experiments/cargo-links/fuel/functions.csv) (line 11)
- [outpost defense · functions](../experiments/outpost-defense/functions.csv) (line 18)

## RVA 0x00b90250

**Dispatch deferred cell-finish event work** · Level C · preferred VA `0x140b90250`

Analysis labels recorded in the original sources are `FUN_140b90250`.

Recorded scope — Dispatch deferred cell-finish event work

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 263)
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 228)

## RVA 0x00b979c0

**reference notification via separate source** · Level B · preferred VA `0x140b979c0`

Analysis labels recorded in the original sources are `FUN_140b979c0`.

Recorded scope — reference notification via separate source

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 311).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 311) · `N310`
- [power · load determinism](../experiments/power/load-determinism.md) (line 263) · Dispatch the distinct reference-bearing cell-finish event
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 229)

## RVA 0x00b97ac0

**Participate in dispatch for an admitted loaded reference** · Level C · preferred VA `0x140b97ac0`

Recorded scope — Participate in dispatch for an admitted loaded reference

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 112)

## RVA 0x00b9a110

**Reach the source for the reference-bearing cell-finish event** · Level C · preferred VA `0x140b9a110`

Recorded scope — Reach the source for the reference-bearing cell-finish event

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 264)

## RVA 0x00bf34a0

**BodyHasKeyword condition** · Level B · preferred VA `0x140bf34a0`

Analysis labels recorded in the original sources are `FUN_140bf34a0`.

Recorded scope — BodyHasKeyword condition

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 268).

- **Inputs** — Condition reference; keyword
- **Outputs** — Numeric condition output
- **Conditions** — Pinned retail 1.16.244.0; Planet-context lookup; manager keyword-source evaluation
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 268) · `N267`
- [limits · functions](../experiments/limits/functions.csv) (line 35)
- [power · definitions](../experiments/power/definitions.md) (line 87)
  Original report discusses this roster entry under Planet selection and exporter exceptions.
- [resource query reachability · native](../experiments/resource-query-reachability/native.csv) (line 200) · `D5H-N199`

## RVA 0x00c05630

**IsPowered condition wrapper** · Level C · preferred VA `0x140c05630`

Recorded scope — Uses the extra-list helper and writes numeric result through R9; AL reports evaluation completion and a null reference can leave the output untouched.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 249)

## RVA 0x00c0ad70

**body keyword source evaluation** · Level B · preferred VA `0x140c0ad70`

Analysis labels recorded in the original sources are `FUN_140c0ad70`.

Recorded scope — body keyword source evaluation

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 269).

- **Inputs** — Body manager/key; keyword and output
- **Outputs** — Boolean numeric via output
- **Conditions** — Pinned retail 1.16.244.0; Body-derived keyword sources and component/trait fallbacks
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 269) · `N268`
- [limits · functions](../experiments/limits/functions.csv) (line 40)

## RVA 0x00c4a810

**Resolve the command-side power actor value** · Level C · preferred VA `0x140c4a810`

Analysis labels recorded in the original sources are `FUN_140c4a810`.

Recorded scope — Resolve the command-side power actor value

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · definitions](../experiments/power/definitions.md) (line 87)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 128)
- [limits · functions](../experiments/limits/functions.csv) (line 36)

## RVA 0x00c94350

**perk operation 2 arithmetic** · Level B · preferred VA `0x140c94350`

Analysis labels recorded in the original sources are `FUN_140c94350`.

Recorded scope — perk operation 2 arithmetic

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 260).

- **Inputs** — Entry value and in-out float
- **Outputs** — Added binary32 value
- **Conditions** — Pinned retail 1.16.244.0; Dispatch-bound arithmetic; not external API
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 260) · `N259`
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 23)
- [crew skills · native](../experiments/crew-skills/native.md) (line 31)
  Original report discusses this roster entry under DB: additive power on each generator.

## RVA 0x00f35090

**Invoke the follow-up for a changed power reference** · Level C · preferred VA `0x140f35090`

Recorded scope — Invoke the follow-up for a changed power reference

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · followup](../experiments/power/followup.md) (line 58)

## RVA 0x00f3dd50

**Fold eligible crew power additions per generator** · Level A · preferred VA `0x140f3dd50`

Analysis labels recorded in the original sources are `FUN_140f3dd50`.

Dispatches DB entries for eligible assigned actors and can invalidate failed E2 handle slots.

Caller `0x140669880` applies a preliminary base-plus-modifiers power gate. The fold visits E2 actors under the mapped state gates and accumulates DB additions per generator, with no separate player dispatch in this path. For a failed actor resolution it overwrites the actual E2 slot with invalid handle from `DAT_1461fae94`, unlike A1's local lookup. For the checked robot definition, rating bands use generator base rating. Neither an assignment nor a positive computed rating alone proves active entries, fuel, delivered power or a consumer allocation. Full declaration remains unknown.

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 259).

- **Inputs** — Generator; PowerGenerated AV; base value
- **Outputs** — Modified binary32 base
- **Conditions** — Pinned retail 1.16.244.0; Assigned actor leases; entry DB; no extra player dispatch
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 259) · `N258` · crew power contribution modifier
- [robots · effects](../experiments/robots/effects.md) (line 53)
  Dispatches DB entries for eligible assigned actors and can invalidate failed E2 handle slots.
- [robots · effects](../experiments/robots/effects.md) (line 58)
  Dispatches DB entries for eligible assigned actors and can invalidate failed E2 handle slots.
- [robots · functions](../experiments/robots/functions.csv) (line 7) · robot power DB fold
- [robots · lifecycle](../experiments/robots/lifecycle.md) (line 66)
  Dispatches DB entries for eligible assigned actors and can invalidate failed E2 handle slots.
- [crew lifecycle · functions](../experiments/crew-lifecycle/functions.csv) (line 78)
- [crew lifecycle · native](../experiments/crew-lifecycle/native.md) (line 18)
  Original report discusses this roster entry under Assignment to a real query.
- [crew lifecycle · report](../experiments/crew-lifecycle/report.md) (line 9)
  Original report discusses this roster entry under report.
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 15)
- [crew skills · native](../experiments/crew-skills/native.md) (line 31)
  Original report discusses this roster entry under DB: additive power on each generator.
- [crew skills · processes](../experiments/crew-skills/processes.md) (line 12)
  Original report discusses this roster entry under processes.
- [robots · lifecycle](../experiments/robots/lifecycle.md) (line 67)
  Original report discusses this roster entry under lifecycle.

## RVA 0x00f4a910

**Workshop descriptor boundary predicate** · Level B · preferred VA `0x140f4a910`

Analysis labels recorded in the original sources are `FUN_140f4a910`.

Recorded scope — Workshop descriptor boundary predicate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 267).

- **Inputs** — Workshop; position; bounds descriptor
- **Outputs** — Boolean low byte
- **Conditions** — Pinned retail 1.16.244.0; Polygon height; component or rectangle; unrestricted mode
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 267) · `N266`
- [power · native](../experiments/power/native.md) (line 74) · Test Workshop spatial boundary
  Used in wire endpoint candidate checking.
- [workshop caller semantics · native ledger](../experiments/workshop-caller-semantics/native-ledger.md) (line 108) · Dispatch Workshop geometry predicate by status
  Selects geometry predicates by uint32 status, including a tail call to the circle test.
- [workshop origin · native map](../experiments/workshop-origin/native-map.csv) (line 10) · `SOR-FN-0044` · predicate
  mode dispatch; circle XY <= radius squared and upper Z
- [spatial placement · functions](../experiments/spatial-placement/functions.csv) (line 39)
- [docs · function register](../function-register.md) (line 124) · `SOR-FN-0044`
  Original group scope — Descriptor, drawing, predicates, clamp and loaded-state output; full permission not established

## RVA 0x00f4aab0

**candidate world and position gate** · Level B · preferred VA `0x140f4aab0`

Analysis labels recorded in the original sources are `FUN_140f4aab0`.

Recorded scope — candidate world and position gate

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 266).

- **Inputs** — Workshop; indexed candidate position; bounds
- **Outputs** — Boolean low byte
- **Conditions** — Pinned retail 1.16.244.0; World equality and translation; boundary helper
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 266) · `N265`
- [power · native](../experiments/power/native.md) (line 71) · Qualify endpoint spatial context
  Called from candidate highlighting.
- [workshop caller semantics · native ledger](../experiments/workshop-caller-semantics/native-ledger.md) (line 105) · Check Workshop descriptor world and point
  Compares world context and passes point after qualified indexed frame translation.
- [resource retained population · d5v sources](../experiments/resource-retained-population/d5v-sources.csv) (line 119) · `V-S118`
- [spatial placement · functions](../experiments/spatial-placement/functions.csv) (line 30)
- [spatial placement · functions](../experiments/spatial-placement/functions.csv) (line 138)
- [spatial placement · native](../experiments/spatial-placement/native.md) (line 49)
  Original report discusses this roster entry under Territory and POI context.
- [docs · function register](../function-register.md) (line 124) · `SOR-FN-0044`
  Original group scope — Descriptor, drawing, predicates, clamp and loaded-state output; full permission not established

## RVA 0x00f65ae0

**commit selected explicit wire** · Level B · preferred VA `0x140f65ae0`

Analysis labels recorded in the original sources are `FUN_140f65ae0`.

Recorded scope — commit selected explicit wire

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 265).

- **Inputs** — Workshop UI selected endpoint handles
- **Outputs** — Reciprocal word 3 relation
- **Conditions** — Pinned retail 1.16.244.0; Resolves selections; connects; updates UI
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 265) · `N264`
- [power · native](../experiments/power/native.md) (line 80) · Commit selected wire connection
  Resolves endpoint handles and adds reciprocal word-3 relation; full preview predicate is distinct.

## RVA 0x00f65c50

**Replace old wire connection** · Level C · preferred VA `0x140f65c50`

Recorded scope — Removes the previous connection before adding its replacement.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 85)

## RVA 0x00f7c060

**React to actor-value changes** · Level C · preferred VA `0x140f7c060`

Recorded scope — Calls owner-linked power refresh after relevant changes.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 242)
- [build budget · functions](../experiments/build-budget/functions.csv) (line 87)

## RVA 0x00f83120

**Refresh producer eligibility after resource changes** · Level C · preferred VA `0x140f83120`

Recorded scope — Dispatches resource-AV refresh and updates cached producer eligibility.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 259)

## RVA 0x00f83450

**Refresh producer eligibility after state changes** · Level C · preferred VA `0x140f83450`

Analysis labels recorded in the original sources are `FUN_140f83450`.

Recorded scope — Updates cached producer eligibility; this cache is separate from electrical graph result and live ExtraFlags.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 260)
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 21) · `S2-020`
- [local output links · native](../experiments/local-output-links/native.md) (line 141)
  Original report discusses this roster entry under Actual movement triggers and scheduler boundary.

## RVA 0x01825e00

**global-data load dispatcher** · Level B · preferred VA `0x141825e00`

Analysis labels recorded in the original sources are `FUN_141825e00`.

Recorded scope — global-data load dispatcher

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 301).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 301) · `N300`
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 73) · `D5AD-SV72` · Global type 9 dispatcher edge; type 7 negative distinction
- [docs · function register](../function-register.md) (line 88) · `SOR-FN-0052` · Save unit 3 dispatch counterpart
- [resource retained population · d5aa gameplay transition map](../experiments/resource-retained-population/d5aa-gameplay-transition-map.md) (line 65)
  Original report discusses this roster entry under Save loading and interior residency.
- [resource retained population · d5ad load chronology](../experiments/resource-retained-population/d5ad-load-chronology.md) (line 29)
  Original report discusses this roster entry under Native dependency order.
- [resource retained population · d5ad save destination](../experiments/resource-retained-population/d5ad-save-destination.md) (line 18)
  Original report discusses this roster entry under d5ad save destination.
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 156) · `D5AD-N006`
- [resource retained population · d5z report](../experiments/resource-retained-population/d5z-report.md) (line 206)
  Original report discusses this roster entry under Persistence and load.
- [resource retained population · d5z sources](../experiments/resource-retained-population/d5z-sources.csv) (line 306) · `D5Z-S0233`
- [static exhaustion · dependency ledger](../experiments/static-exhaustion/dependency-ledger.md) (line 152)
  Original report discusses this roster entry under Final graph expansion and dispositions.
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 125)
- [static exhaustion · trace notes](../experiments/static-exhaustion/trace-notes.md) (line 280)
  Original report discusses this roster entry under Seventh trace round: native packer and six-save context audit.
- [static exhaustion · trace notes](../experiments/static-exhaustion/trace-notes.md) (line 298)
  Original report discusses this roster entry under Seventh trace round: native packer and six-save context audit.

## RVA 0x01827380

**global-data finish dispatcher** · Level B · preferred VA `0x141827380`

Analysis labels recorded in the original sources are `FUN_141827380`.

Recorded scope — global-data finish dispatcher

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 300).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 300) · `N299`
- [resource retained population · d5ad load chronology](../experiments/resource-retained-population/d5ad-load-chronology.md) (line 31)
  Original report discusses this roster entry under Native dependency order.
- [resource retained population · d5ad save state matrix](../experiments/resource-retained-population/d5ad-save-state-matrix.md) (line 268)
  Original report discusses this roster entry under PCM lifecycle, consumers and the ordinary load boundary.
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 157) · `D5AD-N007`
- [resource retained population · d5z sources](../experiments/resource-retained-population/d5z-sources.csv) (line 307) · `D5Z-S0234`
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 126)
- [static exhaustion · trace notes](../experiments/static-exhaustion/trace-notes.md) (line 279)
  Original report discusses this roster entry under Seventh trace round: native packer and six-save context audit.

## RVA 0x01865370

**Read compact save count** · Level C · preferred VA `0x141865370`

Recorded scope — Used by native ExtraCB loader at call site 0x14065be49.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · saved](../experiments/power/saved.md) (line 151)
- [resource retained population · d5ad sources](../experiments/resource-retained-population/d5ad-sources.csv) (line 109) · `D5AD-SV108` · Compact unsigned count 1/2/4/5-byte grammar

## RVA 0x018686b0

**Write save body bytes** · Level C · preferred VA `0x1418686b0`

Recorded scope — Writes the four-byte relationship word to the body.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · saved](../experiments/power/saved.md) (line 142)

## RVA 0x01868770

**Write compact save count** · Level C · preferred VA `0x141868770`

Analysis labels recorded in the original sources are `FUN_141868770`.

Recorded scope — Used for count in ExtraCB and other save components.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · saved](../experiments/power/saved.md) (line 141)
- [containers displays · functions](../experiments/containers-displays/functions.csv) (line 117)
- [crew · current functions](../experiments/crew/current-functions.csv) (line 33)

## RVA 0x01868de0

**Encode saved FormID** · Level C · preferred VA `0x141868de0`

Analysis labels recorded in the original sources are `FUN_141868de0`.

Recorded scope — Serializes saved identity independently of following relationship word.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · saved](../experiments/power/saved.md) (line 142)
- [crew skills · functions](../experiments/crew-skills/functions.csv) (line 58)
- [static exhaustion · native functions](../experiments/static-exhaustion/native-functions.csv) (line 142)

## RVA 0x0187b5a0

**reference relationship cleanup** · Level B · preferred VA `0x14187b5a0`

Analysis labels recorded in the original sources are `FUN_14187b5a0`.

Recorded scope — reference relationship cleanup

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 313).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 313) · `N312`
- [power · load determinism](../experiments/power/load-determinism.md) (line 271) · Perform relationship cleanup for the unresolved owner

## RVA 0x0187bb60

**unresolved-owner reference cleanup entry** · Level B · preferred VA `0x14187bb60`

Analysis labels recorded in the original sources are `FUN_14187bb60`.

Recorded scope — unresolved-owner reference cleanup entry

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 312).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 312) · `N311`
- [power · load determinism](../experiments/power/load-determinism.md) (line 270) · Handle unresolved-owner cleanup

## RVA 0x0187d800

**Continue conditional unresolved-owner cleanup** · Level C · preferred VA `0x14187d800`

Recorded scope — Continue conditional unresolved-owner cleanup

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 271)

## RVA 0x018bcfb0

**pending open-close completion retirement** · Level B · preferred VA `0x1418bcfb0`

Analysis labels recorded in the original sources are `FUN_1418bcfb0`.

Recorded scope — pending open-close completion retirement

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 280).

- **Inputs** — Current reference pointer
- **Outputs** — Retired pending entry
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — No persistence payload demonstrated
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 280) · `N279`
- [power · followup](../experiments/power/followup.md) (line 199) · Retire pending action entries
  Tracks and removes completed pending entries.

## RVA 0x018c2a60

**pending open-close state lookup** · Level B · preferred VA `0x1418c2a60`

Analysis labels recorded in the original sources are `FUN_1418c2a60`.

Recorded scope — pending open-close state lookup

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 278).

- **Inputs** — Current reference and pending map lock
- **Outputs** — Found and desired transition Boolean
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Not a Papyrus instance-property lookup
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 278) · `N277`
- [power · followup](../experiments/power/followup.md) (line 181) · Query pending animation/action state
  Looks up current reference in a locked pending map.

## RVA 0x018c2af0

**pending open-close enqueue** · Level B · preferred VA `0x1418c2af0`

Analysis labels recorded in the original sources are `FUN_1418c2af0`.

Recorded scope — pending open-close enqueue

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 279).

- **Inputs** — Engine task context; desired state
- **Outputs** — Queued action
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — Writes pending runtime map; not saved identities
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 279) · `N278`
- [power · followup](../experiments/power/followup.md) (line 197) · Queue pending action state
  Used by the scheduled open-close variant.

## RVA 0x018c7270

**Participate in the designated-thread power update route** · Level C · preferred VA `0x1418c7270`

Recorded scope — Participate in the designated-thread power update route

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 149)

## RVA 0x018c7550

**Participate in the designated-thread power update route** · Level C · preferred VA `0x1418c7550`

Recorded scope — Participate in the designated-thread power update route

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 149)

## RVA 0x018dba40

**Emit the loaded-reference event from a move or 3D path** · Level C · preferred VA `0x1418dba40`

Recorded scope — Emit the loaded-reference event from a move or 3D path

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 113)

## RVA 0x02116840

**cell-context reference resolver** · Level B · preferred VA `0x142116840`

Analysis labels recorded in the original sources are `FUN_142116840`.

Recorded scope — cell-context reference resolver

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 272).

- **Inputs** — Valid parent cell and context child
- **Outputs** — Conditional reference
- **Conditions** — Pinned retail 1.16.244.0; matching engine state and lifetimes
- **Effects** — Read-only inspection here; native effects described in followup.md
- **Mapped edges** — See docs/experiments/power/followup.md
- **Limits** — No universal Workshop supply or ordinary exterior fallback claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 272) · `N271`
- [coordinate sufficiency · papyrus current location](../experiments/coordinate-sufficiency/papyrus-current-location.md) (line 27) · Participate in space-reference component lookup
- [power · followup](../experiments/power/followup.md) (line 117) · Resolve cell-context handle
  Uses parent-cell fields and flags for the no-generator fallback.
- [transport · functions](../experiments/cargo-links/transport/functions.csv) (line 83)
- [crew · functions](../experiments/crew/functions.csv) (line 128)
- [shared outpost storage · functions](../experiments/shared-outpost-storage/functions.csv) (line 59)

## RVA 0x021ad290

**Workshop event listener registration** · Level B · preferred VA `0x1421ad290`

Analysis labels recorded in the original sources are `FUN_1421ad290`.

Recorded scope — Workshop event listener registration

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 307).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 307) · `N306`
- [build catalogue · catalogue](../experiments/build-catalogue/catalogue.md) (line 21) · Build menu catalogue rebuild
- [local output links · lifecycle](../experiments/local-output-links/lifecycle.md) (line 12) · Subscribe the Workshop object-loaded event sink
- [build budget · functions](../experiments/build-budget/functions.csv) (line 85)
- [build catalogue · functions](../experiments/build-catalogue/functions.csv) (line 44)
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 33) · `S2-032`

## RVA 0x021ad860

**Workshop listener vtable construction** · Level B · preferred VA `0x1421ad860`

Analysis labels recorded in the original sources are `FUN_1421ad860`.

Recorded scope — Workshop listener vtable construction

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 308).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 308) · `N307`
- [build budget · functions](../experiments/build-budget/functions.csv) (line 103)
- [power · load determinism](../experiments/power/load-determinism.md) (line 83)
  Original report discusses this roster entry under A: supported lifecycle, with unknown edges retained.

## RVA 0x021c45a0

**wire candidate highlighter** · Level B · preferred VA `0x1421c45a0`

Analysis labels recorded in the original sources are `FUN_1421c45a0`.

Recorded scope — wire candidate highlighter

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 263).

- **Inputs** — Workshop UI candidate context
- **Outputs** — Qualified highlighted candidates
- **Conditions** — Pinned retail 1.16.244.0; Assembly expansion; pair and world-boundary predicates
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 263) · `N262`
- [power · native](../experiments/power/native.md) (line 70) · Highlight candidate wire endpoints
  Expands assembly candidates and applies pair/space qualification.

## RVA 0x021eb180

**nearest eligible wire target** · Level B · preferred VA `0x1421eb180`

Analysis labels recorded in the original sources are `FUN_1421eb180`.

Recorded scope — nearest eligible wire target

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 264).

- **Inputs** — Candidate interface; source; query position
- **Outputs** — Leased target reference
- **Conditions** — Pinned retail 1.16.244.0; Squared distance; self rejection; pair admission
- **Effects** — Native effects only; never invoked; see power contracts
- **Mapped edges** — See power/native.md and fuel.md
- **Limits** — No safe invocation; current loaded values unobserved
- **Source assessment** — STATIC instruction-backed; proposed STRONG scoped

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 264) · `N263`
- [power · native](../experiments/power/native.md) (line 75) · Select nearest candidate endpoint
  Uses squared distance to supplied cursor/query.

## RVA 0x021efb30

**React to a PowerGenerated value change** · Level C · preferred VA `0x1421efb30`

Recorded scope — React to a PowerGenerated value change

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 152)

## RVA 0x021eff10

**Route reference power and open-close state changes** · Level C · preferred VA `0x1421eff10`

Recorded scope — Route reference power and open-close state changes

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 153)

## RVA 0x021f01f0

**Route reference power and open-close state changes** · Level C · preferred VA `0x1421f01f0`

Recorded scope — Route reference power and open-close state changes

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 152)

## RVA 0x021f0340

**Workshop object-loaded event power entry** · Level B · preferred VA `0x1421f0340`

Analysis labels recorded in the original sources are `FUN_1421f0340`.

Recorded scope — Workshop object-loaded event power entry

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 306).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 306) · `N305`

## RVA 0x021f3690

**Run aggregate power callback** · Level C · preferred VA `0x1421f3690`

Recorded scope — Parallel callback in aggregate refresh chain.

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · native](../experiments/power/native.md) (line 265)

## RVA 0x028ccc40

**manager handle generation and index resolution** · Level B · preferred VA `0x1428ccc40`

Analysis labels recorded in the original sources are `FUN_1428ccc40`.

Recorded scope — manager handle generation and index resolution

Source contract from [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 299).

- **Inputs** — Pinned load/reference/event context
- **Outputs** — State or event described in load report
- **Conditions** — Retail 1.16.244.0; matching engine lifetimes
- **Effects** — Read-only inspection; native effects described only
- **Mapped edges** — docs/experiments/power/load-determinism.md
- **Limits** — No safe invocation or settled determinism claim
- **Source assessment** — STATIC instruction/dataflow; STRONG scoped interpretation proposed

Original records

- [native availability map · functions](../experiments/native-availability-map/functions.csv) (line 299) · `N298`
- [local output links · functions](../experiments/local-output-links/functions.csv) (line 35) · `S2-034`
- [local output links · lifecycle](../experiments/local-output-links/lifecycle.md) (line 42)
  Original report discusses this roster entry under Positive lifecycle chain.

## RVA 0x028cce50

**Receive the unresolved-owner reference-manager operation** · Level C · preferred VA `0x1428cce50`

Recorded scope — Receive the unresolved-owner reference-manager operation

Full arguments, return channel, side effects and lifetime requirements remain unqualified in this entry.

Original records

- [power · load determinism](../experiments/power/load-determinism.md) (line 273)
