# Retention tiers and the 10 GB planning question

[Retention table](retention.csv), [scenario strata](planning-scenarios.csv),
[accepted scope](scope-amendment.md). Saved files are outside these estimates.

The complete eligible non-save set retains 242,995 paths / 32,930,782,429 bytes.
The conservative essential proposal retains 238,875 paths / 32,892,968,157 bytes.
The distinction is independent of the 10 GB target: only 4,120 deterministic
stand-in `.dat` payloads, 37,814,272 bytes, have a concrete reproduction proof.

Those files come from the previous preservation audit's run04 performance
fixture, not from protected game saves despite some synthetic role names.
The proof pins the exact builder and original fixture SQLite, reconstructs every
expected digest from the known generation formula and compares current hashes.
The builder, baseline, ZIP, measurement receipts, failures and actual execution
observations remain retained. No retirement is performed or approved.

Large JSON variants, repeated native/observer fixture directories, prior exports,
source packages and intermediate analyses may be candidates for later review.
They remain KEEP/HOLD here. A recipe's existence does not prove that its precise
executed version, inputs, toolchain and output bytes can be recovered. A failed
run's diagnostic can itself be an irreplaceable observation. Names, sizes, age
and a matching filename are never sufficient evidence for retirement or dedup.

Every other unique or unknown payload stays essential. Opaque containers are
held UNKNOWN outside current scope, not excluded as valueless evidence. Reusing
source maps or old digest groups cannot silently merge observations with different
provenance. No save deduplication result enters this task's current plan.

## Feasibility rather than a fabricated fit

Complete and essential content require compression ratios at most 0.30367 and
0.30402 respectively to fit 10,000,000,000 bytes, before any uncounted operational
material. Non-save samples demonstrate useful ratios, but they are purposive
whole-file examples rather than a random sample. Actual estate strata include
23.295 GB of text, 8.751 GB of binary/opaque stream types and 0.885 GB of other
eligible files. Content complexity within each stratum is not known from extension.

The favorable transfer scenario applies the observed large-definition text ratio
and native-capture binary ratio, storing other types. It estimates 2.87 GB with
the synthetic full-cardinality index. The cautious transfer scenario uses the
observed receipt/text ratio, treats binary and other data as incompressible, and
adds tar serialization overhead: 14.66 GB. Neither is a statistical interval,
universal upper bound or a measured full-estate archive. The raw-tar budget is
33.33 GB including index/padding; preferred zstd output needs its own actual
measurement and framing/write reservation.

The evidence therefore makes 10 GB **plausible but unconfirmed**. The same two
budgets conservatively apply to the essential proposal; no invented compressed
benefit is assigned to the small stand-in omission. If full measurement exceeds
10 GB, retain local completeness and prioritize irreplaceable observations,
methods and identity/provenance for any separately approved backup selection.
Do not demote unknowns or delete primary evidence to satisfy the target.

No off-device copy is confirmed. A possible 10 GB Drive allocation is not a known
entitlement, consent to connect/upload, or rights clearance. Proprietary native
material, donor restrictions and personal metadata need separate destination
review. Two on-device replicas would still share device/host failure exposure
unless actual physical independence is verified; they are not an off-device
backup. Deletion requires the future explicit recovery/backup decision in
[Stage B](stage-b-plan.md).
