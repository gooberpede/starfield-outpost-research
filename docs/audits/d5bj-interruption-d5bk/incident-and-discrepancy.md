# Incident and zero-seed discrepancy

## Observed incident

The local Codex chat **Reproduce bounded D5AQ native fixtures** was consulted
through the Codex thread reader. The interruption appears as a failed turn
with a system error on 9 November 2026, Australia/Sydney. The exact leading
error sentence is “This content was flagged for possible cybersecurity risk.”
The app provided no additional details or block identifier. The app message
and the D5BK brief provide no operation-specific classification. No control
was probed in this audit.

| Time (AEDT) or sequence | Retained evidence |
| --- | --- |
| Earlier turn | The final02 handoff reported bounded success and independent REWORK for full Option C. The exact [checkpoint report](../evidence-reproduction-d5bj/qualification.md) preserves that split. |
| 14:40:19, continuation turn starts | The maintainer asked to continue under the original contract, prioritizing seeded components, actual preparation, the started shared pool, protected first miss and isolated adverse controls. They asked for exact independent review and preserved existing boundaries. |
| Progress reports | The agent reported rectangle registration, 1,600 visits and completion, with a per-cell recording seam. Its last visible progress reported pinned-seed matches, the zero-seed Nickel/Copper disagreement and bounded worker and lookup results. |
| Before interruption | Visible commands produced the model-comparison output, ran the older continuation isolation helper and produced `preparation07.json` with exit zero. Last visible command inspected the retained D5S `export25/native.tsv` lines matching the tail of `0x1407b4bb0`. It completed. A later visible file-change record changed preparation and continuation code. |
| 15:05:09, turn ends | Codex recorded the cybersecurity message above. No final continuation qualification or exact-final reviewer return is visible. The last visible completed command cannot identify the triggering operation. |
| 16:34:55, Git commit time | The checkpoint combined the bounded work and interrupted edits. The maintainer reports ending the blocked session, submitting feedback to OpenAI and committing and syncing the checkpoint. The feedback response or disposition is unknown. |

The maintainer's report of the interruption is corroborated by the visible
system error. Whether it was a false positive remains unconfirmed. The
visible command descriptions above summarize the audit record with personal
paths, chat identifiers and command details omitted.

## Zero-seed Nickel and Copper

**The difference exists in both retained outputs, and the two implementations
use different seed contracts at zero.** `components05.json` and the byte-equal
isolated stream give Nickel `0x000057cb` as the Canyon
`0x00145440` Common root at raw RSCS zero. `model-comparison.json` repeats
the native rows and gives Copper `0x000057cf` in the authored prediction.
The comparison receipt claims all three rows match under the pinned and
incremented seeds. This is a retained differential with an isolated repeat
of its native side and a single retained model comparison.

| BIOM FormID | C1 raw seed, native and model | Zero RSCS native root | Zero RSCS authored root |
| --- | --- | --- | --- |
| `0x000fc61c` | `0x000057cb` | `0x000057cb` | `0x000057cb` |
| `0x00145440` (Canyon) | `0x000057cf` | `0x000057cb` | `0x000057cf` |
| `0x001a540d` | `0x000057c1` | `0x000057eb` | `0x000057c1` |

Every zero-seed seven-word row differs. The first row has the same root
and a different descendant slot. Canyon and the third row differ in root
and descendant slots. The audit compared all rows and preserved the original
outputs under the [checkpoint locators](checkpoint.md#key-original-outputs).

The body is Feynman V `0x0005e0de`. The reader decodes PNDT RSCS as an
unsigned little-endian 32-bit value and writes it at private PNDT `+0x50`.
C1 uses 427,600,259 (`0x197ca983`), the adjacent control 427,600,260 and
the counterexample raw zero. PPBD supplies BIOM, chance, the fallback word
and override. The prior main-file extraction records the fallback words
3,888,212,058, 1,674,147,777 and 3,427,410,394 in the table's BIOM order.
Canyon resolves the main-file BIOM RSGD `0x00258050` with no PNDT override.
Its historical pinned family is Copper, Fluorine and Ionic Liquids, with
empty Special and Everywhere slots. See [C1 inputs](../../experiments/resource-retained-population/d5aq-mask-method.md#d5aq-c1-exact-scope)
and the local historical `d5aq/extra-inputs01.json`.
[Main-file PPBD lineage, rows 455–457](../../experiments/resource-predictability-contrast/feynman-lineage.csv)

The independently qualified D5AD native input record names the zero branch
at preferred VAs `0x140779c33..0x140779c76`. The retained export
`D5AD-SV73` matches its recorded SHA-256
`896599b41f4e5b14cb2c8fd17b0530e991241c798c356dcf04eec965700f04a2`.
The code checks raw RSCS, then reseeds from each component's unsigned
`+0x48` word when RSCS is zero. The fixture writes that word from PPBD.
The model helper replaces RSCS only and calls the pinned owned builder,
whose planetary model initializes its RNG directly from the planetary seed
and accepts literal zero. It carries the PPBD field as `unknown0_uint32`.
The model and native fixture therefore share the raw control value while
their effective seed schedules differ. The receipt does not expose the
first differing native random draw or the full selection branch sequence.
The six owned model source hashes match the comparison receipt. The builder
and component adapter match their independently retained C1 method pins.
[D5AD state matrix](../../experiments/resource-retained-population/d5ad-save-state-matrix.md) ·
[Source ID](../../experiments/resource-retained-population/d5ad-sources.csv) ·
[Owned adapter](../../../research/resource-standalone/builder.py)

Both the C1 value and the adjacent seed take the nonzero branch. The recorded
C1 Canyon row also matches the earlier `extra-inputs01.json`. The seed
fallback is an evidence-backed discriminator for the zero control. The
current records do not establish a contradiction in pinned C1, an installed
override claim, a native error or a need to change the accepted D5AQ result.
An optional separately scoped qualification could compare per-biome fallback
operands, candidate order, first diverging RNG word and downstream slot writes
with a fresh seed-isolated control. That would test causal sufficiency and
fixture carryover. Neither model nor selector was changed.
