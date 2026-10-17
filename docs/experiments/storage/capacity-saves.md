# Actual saved contents and weight reconstruction

[Report](capacity-report.md), [native procedure](capacity-native.md),
[calculation table](capacity-examples.csv), [reader](../../../research/s1-storage/capacity.py).
SOR-EXP-0042 / SOR-EV-0050 continuation. All save offsets below are decimal
**decoded logical-stream offsets**. ESM offsets are decimal physical file bytes.
FormIDs belong to their named saved/definition domain, not current runtime handles.

The instrument reads the four accepted S1 receipts, rehashes their original saves
and generating reader, resolves item masses and physically rereads 113 selected
ESM records including base properties, CarryWeight and all supported MISC item
definitions. Final receipt: `.local-work/s1-capacity/calculations03.json`.
Initial calculations01 is retained; calculations02 additionally asserts the
selected MISC form flag bit2 is clear and counts are nonnegative without u32
overflow. Final calculations03 additionally verifies named prospective item
filter compatibility and rereads five filter lists. No grammar extension or
universal stock extractor was needed.

| Original / S1 receipt | SHA-256 | Selected inline-base candidates; decoded / no inventory / stack gap / leading gap |
|---|---|---|
| HIST-0036 / saved05 | 7e6642f49774c9827fe5230f8cdccdff6b00e4af8738dac11018b56e7ffeca37 | 382; 279 / 86 / 10 / 7 |
| HIST-0077 / saved03 | 3830eb374f086bece85ca3e92ff2d13a3d5aa811193f0c2e583c4564000551bc | 254; 180 / 57 / 8 / 9 |
| HIST-0083 / saved04 | babba0dd0e1822d7afebea5ddee4461392070c25423daa494910fee831f07caa | 382; 279 / 86 / 10 / 7 |
| mature-Save52 / saved06 | 6b4a10084c7e752c31fd2de121a00850aaa2bf1decd700b437d7dccfcdbc82e8 | 382; 279 / 86 / 10 / 7 |

This is a genuine bounded search of known S1 candidates, not a claim to scan
every protected save or every representation. Nominal W>=C cases in these four
subsets number 103/75/106/107 respectively; these are conditional calculations,
not counts of proven currently full stores. Because known candidates already
provide exact fallback-boundary witnesses, no corpus-wide negative search or
parser expansion is warranted. Unknown branches remain unknown and are counted.

## Calculation receipts

All capacities in this table are the selected **definition fallback C0**. Each
example's counted reference extras are closed; its inventory stacks have empty
extra lists; no ExtraE1 is present; decoded BF base/modifier sections contain no
CarryWeight entry. This establishes no explicit saved override in those sections,
not that every runtime provider is zero. W0 is the ordinary materialized-inventory
model under these pinned definitions. Free F0 and fit are conditional on effective
C=C0 and the ordinary eligible MISC/base mass path. Actual live C/W are UNMEASURED.

| Sample / saved reference / base | Contents and mass arithmetic | C0 / W0 / F0 | Prospective compatible item / fit |
|---|---|---|---|
| H36 ff018b64 / 0023aed9 | Lithium 0000557f ×150 @.5 =75 | 75 /75 /0 | Lithium: 0 |
| H36 ff018b66 / 00273199 | Chlorine 0000557c ×150 @.5 =75 | 75 /75 /0 | Chlorine: 0 |
| H36 ff018b61 / 002c5913 | Caesium 000057df ×94 @binary32(.8) | 75 /75.20000457763672 /−.20000457763671875 | Caesium: 0 |
| H36 ff02c339 / 0029b453 | Isocentered Magnet 00246b77 ×41 @binary32(1.8), plus Paramagnon Superconductor 00246b73 ×3 @4 | 75 /85.79999542236328 /−10.799995422363281 | Magnet: 0 |
| H36 ff01c792 / 0023aed9 | Explicit zero item count | 75 /0 /75 | Lithium: 150 |
| H36 ff01ac54 / 00219173 | Explicit zero item count | 300 /0 /300 | Caesium: 375 |
| H36 ff018b73 / 00219171 | Caesium ×375 @binary32(.8) | 300 /300 /0 | Caesium: 0 |
| H36 ff01a4fb / 0006ac92 | Atmospheric Water 00005591 ×20 @.5 | 10 /10 /0 | Water: 0 |
| H77 ff0294fd / 0005ef19 | Iron 0000556e ×17 @binary32(.6) | 10 /10.200000762939453 /−.20000076293945312 | Iron: 0 |

Mixed warehouse detail: binary32(41 × 1.7999999523162842) =
73.79999542236328; binary32(3 ×4) =12; binary32(sum) =85.79999542236328.
Decimal 85.8 is a readable shorthand, not the exact native float. Neither raw
count44 nor the number of item forms2 determines occupied weight.

These saved Lithium/Chlorine and cargo/water stocks are actual exact
definition-fallback boundary witnesses. They satisfy the ordinary saved-boundary
objective conditionally; they are not a controlled live partial-transfer trial
or proof of the historical effective full flag. The Caesium and mixed warehouse
examples are concrete **over-nominal** cases; do not silently clamp their saved
quantities, redefine capacity to their count, or infer corruption. The native
precheck-plus-batch mechanism permits a crossing, while historical effective
overrides/definitions remain alternative explanations for these particular stocks.

## Exact source joins

[S1 saved joins](saves.md#object-level-evidence) retain each record/inventory
offset and owner edge. The CSV repeats those offsets, including H36 ff018b64
2982305/2982405, mixed warehouse 3870343/3870446, empty solid 3184787/3184884
and H77 Iron 3339175/3339286. Item identities come from actual queued inventory
rows, not a search for plausible bytes. The local receipt retains every stack
offset and original queue through the pinned S1 input.

Physically reread MISC DATA sources: Lithium0000557f at ESM6976950;
Chlorine0000557c at6975811; Caesium000057df at6990695;
Magnet00246b77 at7265207; Superconductor00246b73 at7263770. Full selected
definition identity/offset inventory, Water/Iron and base offsets are in
calculations03.json and the fresh source ledger. Weight is the little-endian
binary32 DATA+4 word, with native loader/component corroboration in capacity-native.md.
Filters are checked by item keyword membership under the actual base ONAM list;
an empty incoming cargo's null filter differs from a dedicated store's keyword.

## What is reconstructable

The selected explicit quantities and item identities are saved. MISC base mass,
base capacity and filter are definition-supplied. Explicit BF bases and all three
modifier mask slots are retained distinctly by the owned reader; omitted entries
are not fabricated zeros. No selected stack has an instance mass extra, and the
closed reference extra lists exclude E1 in this subset. Ordinary fallback is
therefore a useful STRONG reconstruction with named current definitions, not an
unsupported parse-as-empty assumption. Winning plugin data and load-time/provider
application can alter the effective result; the receipt does not reconstruct all
those runtime conditions from a historical save.

No empirical evidence need is escalated merely because current live values were
not measured. If S2 later needs an actual partial-transfer observation, the minimal
separate controlled case is one identified protected-copy store with measured
effective C/W and known compatible item mass, request k+1 when k units fit, and
before/after source and destination counts plus a no-action comparison. Match
category and readiness checks and save both snapshots; do not assume a UI full
label supplies those operands. This is a prerequisite description, not authority
to launch, instrument or create/edit saves.
