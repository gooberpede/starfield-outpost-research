# Native oracle contract — retail 1.16.244.0

**EXP0025 correction, 2026-10-11:** historical AD0D3B “translated center” wording
below describes a pretranslation helper-center stack local. Actual translated
X/Y registers are observable at AD0C93/AD0C9C. See [instruction-grounded correction](../event-instrumentation/contract.md).
Historical evidence/frozen protocol are preserved; no live result is promoted.

SOR-FN-0054/0055, SOR-EV-0029. STATIC / OBSERVED-INTERNAL, review required.
Executable SHA-256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Every address below is a **static VA** at image base `140000000`; subtract that
base for RVA. At runtime add the RVA to the freshly identified module base.
No CK address, inferred decompiler prototype or unwind record establishes ABI.
Local `engine-oracle-01` through `08` Ghidra exports retain instruction windows
and call/dataflow; hashes are in the review receipt. Exports are LOCAL-ONLY.

## Selected first acquisition: stored native center and terrain radius

`1421b2570` resolves a workshop via `140f3df70`, constructs its descriptor via
`140f4a140`, and obtains its durable center via `140f4ab80` at `1421b28fc`.
The helper copies reference XYZ at `+8c/+94`, tests the activator/Workshop keyword
and extra-bc, then applies its `+60/+68` compensation with the all-zero bypass.
The caller places XYZ and radius in a 16-byte local value. At
`1421b294d/2954`, it obtains the output owner through
`[module+5fd9c30] → +130`; at `1421b29ac/29b1` it copies the four native
float32 values into that owner's `+90..9f` under the owner's `+d0` lock.
This is an engine-generated stored output, not an observer calculation.

Downstream `1407a6540` reads positive radius at `+9c` and center at `+90/+98`
(`1407a6578/6586`), computes squared distance outside an axis-aligned bound
obtained through the terrain data manager, and compares against radius squared.
It can additionally filter an identifier list. RTTI-backed callback specialization
in `1407a6150` identifies `NiPointer<BSProjectedDecal>`: this downstream path
filters **projected decals by bounds**. It establishes actual use of the native
center, not authority over every building permission or terrain-placement result.
Its thunk `1407b0880` adjusts
the predicate context by eight bytes. `1407a6150` constructs/invokes that predicate
in the terrain processing path. This supplies a concrete **terrain bounds consumer**,
not a conjectural UI label or a generic search for a float tuple.

The observer 0.1.1 reads the fresh root and raw output prefix before and after
its census. It retains pointer-field provenance, center/radius bits, raw flags
e8/e9/ea and the separate current-workshop-context global pointer at
module+61dd460. That pointer is diagnostic, not a decoded active Workshop ID.
Raw object acquisition does not acquire the native lock, pin lifetime or invoke
any routine. Two equal samples can both be stale. Native reset `1407a6690`
clears radius and sets dirty ea; `1407a50d0` changes activation state and can
release resources. Never infer freshness from a plausible center or flag alone.

**Qualification boundary:** capture while the operator has opened build mode
at a positively associated workshop; retain before/open/settled/closed controls
and both outpost transitions. Only classify an exact center match after the
native output's active-workshop association and same frame have been demonstrated.
Outside build mode, reset/inactive, ambiguous association, changed brackets or
unreadable output are STALE/UNASSESSED/PARTIAL, never model failures or successes.
The worker does ordinary guarded memory reads; non-atomicity and lifetime races
remain. No safe worker-thread query ABI is claimed. Raw outputs are runtime
state and are not automatically persisted values.

## Complementary natural-execution oracle: selected native grid

`140ad92e0` iterates planetary sites and calls `140ad08d0`.
The latter compares a site hierarchy against the selected source-world key,
requires overlay flags+20 bit1, prepares a six-pointer stack context and enumerates
references through `140b1e190`. The callback thunk `140ad8ec0` dispatches
`140ad0b90` (vtable `144b916e8`). Context layout at RSI:

| Offset | Meaning at the qualified callback |
|---|---|
| 00 | result-boolean pointer |
| 08 | caller's candidate hierarchy pointer |
| 10 | landscape pointer-to-pointer; body+54, resolution+50 |
| 18 | source-world origin hierarchy pointer |
| 20 | local-frame translation XYZ pointer |
| 28 | terrain query bounds pointer |

After type/Workshop qualification, the callback calls `140f4ab80`, adds the
context translation in binary32 before XY floor, copies the origin hierarchy,
and calls `14096f5c0` to select a native integer hierarchy. Observe **VA
`140ad0d3b`, RVA `00ad0d3b`**, immediately after that call: RBX is the current
reference, RSI is the callback context, RBP-49 is translated center XYZ,
RBP-9 is the 44-byte resulting hierarchy and RBP+6f holds the two native floor
integers. [Capture format](../../../debugger/engine-oracle/contract.py) preserves
the native output and all input base/translation bytes; it never calculates
the target's result. Hierarchy offsets 04/08,14/18,24/28 encode
coarse/sub/fine signed integers. For resolution256/block12, flatten with
`coarse*192 + sub*12 + fine`; preserve the two opaque asset-handle fields.

Later code projects with `142332410`, canonicalizes/subtracts hierarchies via
`14096eb90/14096f940`, expands coverage by native radius plus a margin, and
compares terrain bounds. The callback is a **coverage/selection operation**;
it is not the complete permissions system or a continuous geographic oracle.
Its center, floor, body, input hierarchy and output hierarchy permit independent
comparison of the model's decisive intermediates, after frame reconciliation.

Do not call this path on the observer worker. The surrounding enumeration,
stack-owned pointers, terrain objects and handle updates have execution-context
and lifetime requirements. Descriptor construction can create/retain/release
objects; an apparently simple query is not pure. Capture natural execution on
its own thread instead. An INT3 log breakpoint changes scheduling and code bytes
temporarily: it is intrusive even with auto-continue and no gameplay mutation.
The disposable fixture qualifies formatting, two-thread acquisition, restoration,
detach and zero-hit cleanup only. It does **not** prove live reachability, ABI
safety, breakpoint bytes on retail, or absence of timing effects.

`14077e350` calls `140ad92e0` during terrain/site candidate processing. Opening
an existing workshop may never traverse this path. A zero-hit session is
NOT_OBSERVED. Do not force a native call, place a new outpost, retry save debugging
or change travel scope to obtain a hit without a separately reviewed experiment.
The current runner has no live-target option; a live adapter/preflight remains
separate work under explicit authorization.

## Other candidates and exclusions

`140f4ac50` consumes a descriptor and point: descriptor+0c selects a global
frame translation in table1461fae88 when below count1461fae80; otherwise the
center is copied. It tests XY distance against radius and Z against ceiling.
At `140f4acb7`, stack XYZ and descriptor RDX are observable; AL is complete at
`140f4acf1`. This corroborates local boundary semantics, but lacks an independent
planetary address. `141884350` selects workshop or player for streaming center;
it is an additional loaded-scene dependency, not a durable body/grid oracle.
Metadata1454dd710/720 contains packed unwind RVAs, not a callable vtable.
Offset+90 matches in unrelated object types do not establish this owner chain.
