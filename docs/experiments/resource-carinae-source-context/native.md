# Typed source ancestry and missing operands

[Report](report.md), [pins and source effects](sources.md). Static addresses below
are preferred VAs for retail 1.16.244.0, image base `0x140000000`; runtime VAs
use the measured relocation base. Object members are byte offsets. Saved tokens,
Workshop identifier bytes, runtime FormIDs, pointers, ordinals, owner keys and
packed geographic keys are separate domains.

| Join | Type | Evidence and limit |
|---|---|---|
| Save52 → designated outpost | SAVE/maintainer context | Original Save52 hash and prior saved joins; saved beacon token `82be17` and owner notation `ff02be17` are not runtime pointers or expanded native handles. |
| Updater → Workshop → three terminals → transfer | OBSERVED | Captures 1270/1280/1301/2587, PID 8920, TID 24296, thread lifetime 21, updater token 1. Typed BC bytes `91bac704da9b1e34`; exact resource-pointer transfer membership. Runtime reference FormID `0xff02b6a8` is separately observed. |
| Consumer source map → slot/key/wrapper | OBSERVED | Ordinal 24; slot-value VA `0x214579cc3c8`, key `0x21c42d53ba0`, wrapper `0x21c49c637c0`. Same invocation and slot observations, not a permanent source identity. |
| Key → geographic source object | STATIC / runtime referent UNKNOWN | `resource-milestone-b-producers-01.tsv`, `0x14079fcc2..0x14079fcd4`, `0x14079fe0f..0x14079fe18`: map lookup/insertion uses source pointer as key. Existing C2A copies do not dereference it. |
| Manager → ProcGen → occupied map | STATIC / captured manager UNKNOWN | `resource-availability-ui-15.tsv`, `0x1421e09d4..0x1421e0a77`: global `0x145fd9c30`, manager `+0x130`, ProcGen slots `+0x20`, capacity `+0x28`, stride `0x18`. Existing callback's ProcGen pointer is observed; no captured manager join. |
| Source → anchor/padding/raw dimensions | STATIC / actual fields UNKNOWN | RG1 `013.request.tsv` constructor `0x140982d90`, and provider origin/index dataflow in producers01. Source `+0x10/+0x14` anchor, `+0x20/+0x24` padding, `+0x28/+0x2c` raw dimensions; `+0x18/+0x1c` remain raw copied words here. Constructor zeroes those words before later processing; do not call them effective dimensions without the applicable producer. |
| Source selectors and visited key | STATIC / actual fields UNKNOWN | Source `+0x38..+0x68` raw selector/cache fields; provider `0x14079fc37` reads `+0x68` for a separate visited test. This is not the source-pointer key or the vein packed cell key. |
| Source local frame → outpost frame | DERIVED conditional / historical UNKNOWN | Existing RG2-A1 angular/snap and descriptor trace; descriptor (21408,15648), primary site (21399,15640), source origins `100*(anchor-padding)`. Frozen translation (-900,-800) maps saved site-local XY into modeled descriptor-local XY. Actual historical source and selected manager descriptor remain unbound. |
| Manager owner → CRC suffix | STATIC / installed DERIVED / native historical UNKNOWN | PNDT `0x0005e4da` → owner 386266 through loader/lookup/manager setter in RG2-A1 N001–N013. CRC consumes packed cell LE64 then owner LE32; source slot and pointer are not CRC inputs. |
| Source/manager → generator entry | STATIC / historical UNKNOWN | Provider `0x14079fe81..0x14079ff18` selects manager descriptor `+0xc8` or `+0x1c0`, transforms frame/origin and passes source, BIOM, owner and output map to `0x14079b520`. Miss/visited/hit paths differ; insertion and return are not completion certificates. |
| BIOM → component → RSGD/DNAM → resource order/masks | DERIVED installed / historical UNKNOWN | `0x14079b625..0x14079be20`, C1G native ledger. Captured C1G DNAM equality elsewhere is not a Carinae RSGD identity. All three consumed resources can share a wrapper without sharing construction epoch or effective selection. |
| Region collection → producer epoch | UNKNOWN | No construction invocation/output join, source creation/reset sequence or historical population receipt. Neither equal pointers nor a geometry digest closes this edge. |

The earliest responsible missing observation is therefore the key's referent and
manager frame **at the bound consumption stop**. The new adapter obtains that
snapshot with existing breakpoints; actual historical packed cell key, selected
BIOM/RSGD/DNAM/mask/order and predecessor population still require a producer
witness if the source-context discriminator agrees. No claim of persistence or
safe callable mod integration follows from any field described here.

## Installed prediction context, not observed slot-24 identity

All four requests use BIOM `0x001160d9`, selected RSGD `0x0018ce04`, family
root Iron `0x000057c7`, owner 386266 and mask 4. Descending rarity order is
Rothicite 4, Alkanes 1, Iron 0, each with active weight 1. They share the same
selected 560-byte DNAM, SHA-256
`fd99c23e35f6b3c0b2abefbfb224920c0cea7787dae4a4e8c71dee6b29e83111`;
raw definitions remain local. Rothicite can reject later Alkanes and Iron;
Alkanes can reject later Iron. Earlier same-resource paths are excluded from
competition under this model. The native historical order,
DNAM and predecessor populations remain UNKNOWN for all three accepted paths.

| Prediction source identifier | Geographic fine-cell anchor | Descriptor-local anchor | Nominal dimensions | Padding per axis | Generator origin in native units | X/Y half-open cell range |
|---|---|---|---|---|---|---|
| `0:21372:15612:002493eb` | (21372,15612) | (-36,-36) | 22 × 22 | 2 | (-3800,-3800) | [1,25) / [1,25) |
| `0:21384:15636:0006ce55` | (21384,15636) | (-24,-12) | 10 × 10 | 2 | (-2600,-1400) | [1,13) / [1,13) |
| `0:21396:15624:002493e7` | (21396,15624) | (-12,-24) | 22 × 22 | 2 | (-1400,-2600) | [1,25) / [1,25) |
| `0:21396:15648:002493ed` | (21396,15648) | (-12,0) | 10 × 10 | 2 | (-1400,-200) | [1,13) / [1,13) |

Raw block dimensions are nominal dimensions plus twice padding: 26 × 26 or
14 × 14 respectively. These are DERIVED frozen request operands. No row is
assigned to native ordinal 24 without the missing source/frame join. The
whole-source candidate replay changes the frame and keys consistently and
retains every predecessor needed by this ordering; it does not compare only
paths starting inside the 150-unit outpost query.
