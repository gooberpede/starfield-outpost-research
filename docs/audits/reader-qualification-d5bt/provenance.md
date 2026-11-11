# D5BT input and reader provenance

## Input custody and framing

Only the two selected members in the [D5BF asset ledger](../release-assets-d5bf/release-assets.json)
and [B4/F1 file dispositions](../publication-readiness-b4/f1/file-dispositions.csv)
were opened. The exact member path and original basename are keyed by member ID
in D5BF. The local staging receipt binds the complete container digest to
the exact selected member and contains the private absolute locator.

| Member | Exact container | Codec | Container bytes | Container SHA-256 | Member bytes | Member SHA-256 |
| --- | --- | --- | ---: | --- | ---: | --- |
| B4-F054 | `sor-1.16.244.0-b4-f1-core-stored-provisional.zip` | ZIP_STORED | 104046934 | `b27bb842770d51499bec30042660789f1e539a3187d0d63f226fafcedd405105` | 2085680 | `ab28c98940b019320cda4d6a0db54c9d88b721a18fba4c6a701fbed0966b42fe` |
| B4-F067 | `sor-1.16.244.0-b4-f1-addendum-deflate-provisional.zip` | ZIP_DEFLATED | 80827444 | `d904b452fcfe1a82e6c4ceae5dfd1396b4fa088868587605ced7e2e57de278a3` | 17016320 | `8ad36c6bfa6035c66f0a1c62d64a704496d2ae01f7d1fac567ea979a4f7404ec` |

The staging helper checked archive names, traversal, duplicates including
case-folded collisions, selected identity, codec, size and SHA-256. It streamed
the selected members into a new directory with exclusive file creation and
rehash, leaving the remaining members unopened. The selected compressed ZIP
payload sizes were 2,085,680 and 16,872,325 bytes, respectively.

| Member | BCPS1 streams | Decoded bytes | Decoded SHA-256 |
| --- | ---: | ---: | --- |
| B4-F054 | 22 | 5539576 | `b236f22dd601b2dab59d5640967b12ab1f4dd5b3e4aac58cfae593bf43989579` |
| B4-F067 | 154 | 40291019 | `9bf6c3c4068adbfd274cf4b194891151ec732377ad79bce081689ef449d66887` |

Python was CPython 3.14.3 AMD64, with stdlib and zlib runtime `1.3.1.zlib-ng`.
Both drives exceeded the 40,000,000,000-byte floor. The two staged files
total 19,102,000 bytes. The largest decoded scratch file is 40,291,019 bytes.
Their combined peak is 59,393,019 bytes before small source copies, receipts
and patches. Executions were sequential and reserved space for the one active
decode. The qualified entry points use the caller-available Windows counter
from the existing [session guard pattern](../../../runtime/session-tools/common.py)
at setup and through decode writes. The decoder cleans up its scratch and the
source-only verification removes its disposable tree. Original bytes, historical
evidence and new local receipts retain their respective custody.

## Source lineage and effects

- The [reader](../../../save-analysis/scripts/d5bt_reader.py) uses
  [typed_records](../../../save-analysis/scripts/workshop_population.py),
  [reference_prefix and linked_prefix](../../../save-analysis/scripts/workshop_inventory.py),
  the [stream decoder](../../../save-analysis/scripts/stream_save.py), the
  [R3 framer](../../../save-analysis/scripts/outpost_record_framing.py) and the
  [plugin/form resolver](../../../save-analysis/scripts/extractor_resources.py).
  The [P1 extra reader](../../../research/p1-power/saved_instances.py) uses
  the existing owned ExtraBC grammar through an explicit opt-in. Its default
  branch still refuses the original beacon at ExtraBC. The older loose
  `authority_probe.py` was unavailable at its recorded locator and the new
  reader has no dependency on it. Supply and demand use the accepted
  attribution in the [authority report](../../experiments/power/save29-authority.md).
- The [display reader](../../../save-analysis/scripts/d5bt_display.py) adapts
  the owned pending-dialogue capability in the tracked
  [component walk](../../../save-analysis/scripts/workshop_components.py).
  B3-C0115 matched SHA-256
  `552f8a77334a2f96f159b67db1739cd1babee4f2dabdfcd2d4a01bc60722fc91`.
  Its only behavioral delta against the tracked precursor is the pending-dialogue
  fixed-four-byte payload after the typed ID/index. B3-C0124 matched
  `21e08f62629ed4f350f4f7b462f1c52fbc71b787214b418c4f2427604d15cb73`.
  That acquisition precursor has a top-level loop and was inspected only.
  B3-C0116's tracked [extra reader](../../../research/historical-methods/b3/sd1-containers/extras_sd1.py)
  matched its loose original at
  `d3fa720e91ffc9fa8b82f69c618b5fe286a2fd772f32210ed36624d08d416e50`.
  The [SD1 source ledger](../../experiments/containers-displays/sources.csv)
  pins the historical instance-join receipt at
  `7cfcf0c202faa1ac8c8812deb6012e29d6b733c8dd9a39114ff43b4798f8d663`.
  Both item counted ends precede their REFR ends by one byte, as that receipt
  records. No old acquisition or active-copy mode ran.
- Maintainer-owned adaptations use GPL-3.0-or-later under SOR-P-0002. Existing
  game and tool attribution remains in [CREDITS](../../../CREDITS.md) and
  [SOURCES](../../SOURCES.md). The remaining observed project imports in the
  clean copy are `analyze_manual_corpus.py`, `analyze_structural_containment.py`,
  `archive_manual_corpus.py`, `inventory_historical_saves.py`,
  `outpost_membership.py`, `probe_manual_candidates.py`,
  `probe_output_link_structure.py`, `validate_mature_outposts.py`,
  `validate_output_link.py` and `workshop_global_units.py` under
  `save-analysis/scripts/`. Their historical input and output modes remain
  outside the entry points. The local clean-copy receipt binds each exact
  source digest and demonstrates the module closure without private paths or
  assets in the source tree. The only data reads in the qualified commands
  are explicitly supplied SFS files. The historical receipts are verification
  context and no raw component payload was promoted.
