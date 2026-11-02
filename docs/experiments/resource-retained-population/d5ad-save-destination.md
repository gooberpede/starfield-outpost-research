# D5AD Save52 destination operands and ordinary load branch

2026-11-02, Australia/Sydney. [Original contract](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AD_initialization_save_load_reconstruction.md),
[chronology](d5ad-load-chronology.md), [report](d5ad-report.md),
[source ledger](d5ad-sources.csv). This followup addresses the concrete saved
operands required by D5AD-Q2; it supplies no new runtime observation.

**Save52 explicitly records the Lodge CELL destination and a Jemison planetary
context.** Its native-backed branch prefix contains static saved identity
`0x0006bb29`, installed CELL `CityNewAtlantisLodgeInt`, planetary-context flag
one, system 71456/body index 3, and no alternate reference. Thus the ordinary
successful-resolution load route is constrained by actual saved operands;
it is not an arbitrary choice among all callbacks in the loader. The saved
context selects the Jemison initialization opportunity before publication and
processing of the pending interior transition. This does not measure the actual
call time, reset caller, worker schedule or a Lodge resource-generation demand.

Native global dispatch `0x141825e00`, **case 9**, calls `0x141829ec0`.
Case 7 instead calls `0x1418b22c0`; the global-type number is material to the
framing. The paired type-9 writer is `0x1418286f0`.

Exact primary windows and whole-input hashes are D5AD-SV66–67 for the two
prefix helpers, D5AD-SV68 for the complete destination loader, D5AD-SV69 for
the paired writer, D5AD-SV70–71 for token decoding/remapping, and D5AD-SV72
for global dispatch. D5AD-SV64–65 preserve the initial method and receipt;
D5AD-SV76 pins its repeated run and process-level negative controls. The current
method and CELL-DATA-qualified receipt are D5AD-SV77–78. D5AD-SV81–82 bind the
CELL DATA loader and its independently identified class vtable.

## Saved operands and independent identity checks

The exact protected controlled-copy hash remains
`6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8`.
Its decoded stream remains
`e3c0dc34cbbdcd26bb85d212fc458378b44404b37a5f54b635070e03e1565b93`.
All offsets in this table are **decompressed logical-stream offsets**; tokens
are serialized identities before native load-order/reference remapping.

| Offset | Size | Native-backed field | Save52 result |
|---|---|---|---|
| `0x1b82a1` | 3 bytes | Initial world token, read by `0x14182d350` through legacy-ID reader and TESWorldSpace cast | Null token `000000`. |
| `0x1b82a4` / `0x1b82a8` | 4 bytes each | Saved cell-grid operands | Unsigned 0 / `0xffffffff`, interpreted as signed 0 / -1 where consumed as signed coordinates. |
| `0x1b82ac` | 3 bytes | Destination token, read by `0x14053a2d0` | `46bb29`; tag 01 gives direct static saved identity `0x0006bb29` before remapping. |
| `0x1b82af` | 12 bytes | Saved local XYZ, three little-endian binary32 values | Exact bits/numbers retained in the local receipt; this is saved local position, not a geographic pair or resource query. |
| `0x1b82bb` | 1 byte | Planetary-context-present flag | 1. |
| `0x1b82bc` / `0x1b82c0` | 4 bytes each | System and body-index operands to `0x142332ea0` | 71456 / 3, uniquely matching installed PNDT `0x0003f5a1`, `JemisonPlanetData`. |
| `0x1b82c4` | 16 bytes | Two binary64 context-pair values | Approximately 2.2813010500281132 / 0.7110440698595923; exact values retained locally. No angular-order/unit interpretation is added. |
| `0x1b82d4` | 8 bytes | Packed context/world key | `0x022e401882204260`, agreeing with saved type-3 context and the decoded Jemison system/body. |
| `0x1b82dc` | 1 byte | Alternate-reference-present flag | 0; optional reference reconstruction and its further conditional operands are skipped. |

The type-9 payload is 136 bytes, ending at `0x1b8329`. This method decodes
the initial 60-byte branch prefix ending at `0x1b82dd`. It preserves the
remaining 76 bytes as an opaque tail hash; it does not claim a full type-9
decoder. The loader consumes that later data through its common final buffer
path after destination processing, so those tail bytes are not substituted for
the initial branch operands.

Independent installed ESM examination finds exactly one record for the direct
saved identity: CELL `CityNewAtlantisLodgeInt`, ESM record-header
offset `0x157a2bac` in the pinned ESM. That is an **ESM file offset**, not a save
offset or runtime pointer. The separate PNDT match is at ESM offset `0x53928960`.
The installed ESM retains SHA-256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
These identity checks do not bypass the native remapper or prove that every
historical runtime lookup succeeded.

The Lodge's installed CELL DATA bytes are `25000000`, a four-byte
little-endian value `0x25` with interior bit `0x1` set. This is a native-backed
field join: PE/RTTI inspection identifies TESObjectCELL vtable
`0x144b93b20`, whose load slot at vtable `+0x88` is `0x140ae6830`.
The DATA branch at `0x140ae6a2d..0x140ae6add` writes the selected bytes to
receiver `+0x48`; its two-byte compatibility path zero-extends into that field.
The 60-byte destination-prefix result and this independent installed definition
therefore qualify the ordinary interior branch's actual input representation.
They do not assert that a runtime override or subsequent mutation is impossible.

## Operand-constrained native route

All VAs below are preferred static addresses for Starfield 1.16.244.0,
image base `0x140000000`; they are not observed runtime call timestamps.

| Decision or edge | What the saved operands establish | Remaining runtime qualification |
|---|---|---|
| Native legacy token read | `0x1418650d0 → 0x1418599a0` decodes the three-byte token. Tag 01 supplies static saved ID; `0x14180b410` still performs native remapping. | Actual global map/loaded form resolution is separate from saved identity. |
| Planetary-context branch | Flag 1 causes system/body, pair and key reads; `0x142332ea0(71456,3)` supplies the Jemison body identity under the installed catalog. | Successful body resolution uses the current native registry. |
| Alternate-reference branch | Flag 0 leaves the optional actor/reference pointer and its retained component handle absent on this route. | No optional-reference failure/recreation branch is imported into the actual prefix. |
| Destination-kind branch | Successful resolution of saved `0x0006bb29` to its ordinary installed CELL selects the loader's form-type `0x49` branch at `0x14182a9c6..0x14182a9cc`. | Failure, substituted form type or a different effective override requires its own evidence; the script does not simulate the live registry. |
| Context initialization | Nonzero resolved Jemison identity reaches `0x14078af30` at `0x14182ab2d`, with the saved pair/key and zeroed additional operand block. | Internal owner/component/reuse/reset and readiness predicates still apply. No new reset caller witness is created. |
| Cell preparation | `0x1418290d0` is called at `0x14182ab48`, with the destination and saved grid/world operands, after the initialization call. | Current cell/context contents and services affect its downstream behavior. |
| Pending interior transition | Installed Lodge DATA value `0x25` reaches destination cell `+0x48` through its native loader. The test at `0x14182ab94` admits the ordinary interior CELL/context payload, followed by `0x141a67830` at `0x14182abfd` and `0x141a20380` at `0x14182ac09`. | Effective historical overrides or later flag mutation remain distinct; no new runtime memory snapshot is claimed. The paired writer independently corroborates CELL-versus-WRLD selection. |

The paired writer supplies an additional positive qualification: it selects
the parent CELL identity when the parent cell's `+0x48` bit `0x1` is set;
its ordinary exterior branch selects the world identity instead. Save52's
CELL token therefore agrees with the ordinary interior serialization route.
The writer separately records planetary context when its manager/context
predicates admit it. A null initial world token does **not** mean absence of
planetary context: the context-present flag and tuple are positive counterevidence.

This closes the claim that all saved-destination branch operands were simply
unavailable. Native lookup success, context reuse/reset predicates, queued work
and historical scheduling remain separate. Root review determines whether the
connected chronology meets the original Q2 contract; this bounded followup
does not independently declare D5AD complete.

## Reproduction, controls and limits

Use the verified interpreter and ESM paths from the local receipts:

```powershell
& $D5adPython -E -B research/resource-retained-population/d5ad_save_destination.py .local-work/d5ad-save/FRESH-DESTINATION --esm $D5adEsm
```

The [owned method](../../../research/resource-retained-population/d5ad_save_destination.py)
uses the existing length-closed global suffix, full-stream decoding and an
independent selected-block decompression. A separate fixed-layout `struct`
read agrees with actual prefix fields; the existing saved-token decoder
independently agrees on the static identity domain. Synthetic positive controls
cover context-present and context-absent layouts. Four malformed/unsupported
controls reject truncated XYZ, truncated context, invalid context kind and
an alternate-reference branch outside this method's scope. Actual global type 7
is a negative control and rejects this destination-prefix grammar.

The fresh receipt is `.local-work/d5ad-save/destination01/destination.json`.
Initial-method repeat `.local-work/d5ad-save/destination02/destination.json` is byte
identical. Three process controls reject an existing output, optimized execution
and a wrong ESM without creating failed output; their exact returns are retained
in `.local-work/d5ad-save/destination-checks.json`.
The current method adds the native-backed CELL DATA check and succeeds in
`.local-work/d5ad-save/destination03/destination.json`; the earlier process
controls are not relabelled as execution of that new check. The original method
was reconstructed by exactly reversing those two DATA additions and verifying
its bytes against the original frozen SHA-256. D5AD-SV64 now names that local
historical copy; D5AD-SV77 names the current method. D5AD-SV83 records preservation.

The first fixture attempt incorrectly expected prefix lengths 59/27; it failed
before output creation. Correct lengths are 60/28; actual offsets and field
widths above use the corrected independently checked arithmetic. Protected-copy
and ESM hashes match before/after, and decoded scratch is removed. No game,
database, protected-save, configuration or production-observer change occurs
in this followup.
