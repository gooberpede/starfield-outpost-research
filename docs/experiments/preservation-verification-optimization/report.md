# Preservation verification: measured savings and the remaining protection gap

2026-10-25, Australia/Sydney. **REWORK: the frozen AC4 efficiency contract is not
satisfied.** No replacement policy is effective. The
[authorized brief](../../implementation-briefs/CODEX_BRIEF_SOR_preservation_audit_optimization.md)
governs this offline audit and disposable prototype.

| Element | Result |
|---|---|
| Question | Can routine historical verification fall by at least 80% while retaining comparable preservation? |
| Best-supported answer | The tested journal design removes repeated historical reads for journaled filesystem activity, but loses detection of changed readable bytes without a journal event. The full-byte fallback retains that detection and misses the 80% target. |
| Confidence | PROVEN for receipt counts and the executed synthetic measurements; STATIC for the documented coverage difference. This is not an impossibility result for all storage architectures. |
| Coverage | D5C/D5D/D5E/D5G receipts; current metadata for the 93,334 D5G paths; synthetic Windows NTFS W1/W2 and adversarial controls. No game, original-save mutation, raw-volume mutation or deployed workflow. |
| Evidence | [Baseline](baseline.md), [measurements](measurements.csv), [qualification](qualification.md), [sources](sources.csv); primary receipts remain ignored under `.local-work/preservation-verification/`. |
| Limitations | Historical elapsed time and actual physical I/O are UNKNOWN. Synthetic warm-cache timing is not a timing of the original 93,334-pin audit. No external immutable trust root or transactional historical snapshot is implemented. |
| Next step | Maintainer review of the exact detection guarantee and proposed storage boundary. Activation or any weaker guarantee needs a separate decision; the existing rules continue. |

## What the audits actually did

D5C records 77,893 paths. D5D adds 542, D5E changes none of that inventory, and
D5G adds 14,899: 93,334 total. Shared expected hashes remain equal at each join.
The D5G source makes 78,435 inherited expected-pin comparisons and then 93,334
inventory hashes before work; its after branch makes another 93,334. That is
265,103 payload hash calls inferred from the successful executed method, before
separate save-protection, scientific-input, review and archive checks. Eight
workers parallelize the after branch; they do not remove its reads.

The growth is an expanding path union, including earlier build/qualification
outputs and receipts. It is not proof of an equally large increase in distinct
scientific observations. D5G's fixed-list after branch detects changed or missing
listed bytes, but does not itself enumerate unexpected additions. The
[protection ledger](threat-model.md) distinguishes that historical coverage from
the broader prospective requirements.

## Measured W1 results

All rows use the same frozen 4,096-file historical fixture, with 35,651,584
historical payload bytes. Every mode also hashes 17 scientific and eight critical
stand-ins twice. Five warm-cache trials per mode are in the CSV; the historical
timer includes baseline loading/hashing and, where used, journal scanning.

| Historical work per pre/post pair | Legacy model | Full-byte prototype | Conditional journal prototype |
|---|---:|---:|---:|
| Filesystem entries enumerated | 4,113 | 8,226 | 0 |
| Logical pins visited | 12,339 | 8,226 | 0 |
| Unique payload files read | 4,096 | 4,096 | 0 |
| Opens / payload hash calls | 12,288 | 8,192 | 0 |
| Payload bytes read and hashed | 106,954,752 | 71,303,168 | 0 |
| Historical wall time, median seconds | 2.4663882 | 1.7363372 | 0.0056180 |
| Total verification wall time, median seconds | 2.4894118 | 1.7604960 | 0.0255848 |
| Total process CPU, median seconds | 2.484375 | 1.765625 | 0.03125 |

The full-byte mode saves 33.33% of historical hash bytes/calls, 0% of unique file
reads, and 29.60% of historical time. Enumeration increases 100% because it checks
the namespace both before and after. Its total time falls 29.28%.

The conditional mode saves 100% of historical payload enumeration/reads/hashing,
99.77% of historical time, and 98.97% of total time. It still reads and hashes a
794,624-byte SQLite control manifest and reads 784–1,168 journal bytes per pair in
these trials. Those costs are included, not hidden. Its **changed-readable-byte
coverage is weaker**, so these savings do not count as an AC4 PASS.

The fixture is a scaled D5G-like operation model, not a sample that estimates
the corpus's exact file-size distribution. The inherited fraction is modeled as
all historical fixture files; actual D5G inherits 78,435 of 93,334. All denominators
were frozen before the first successful performance evaluation. No projection
of these seconds onto D5G is claimed.

## Setup, W2 and protection

One new fixture/baseline setup takes 11.7278728 seconds, hashes 37,814,431 bytes
across 4,121 payload files, and creates a 794,624-byte manifest. This includes
synthetic fixture creation and file-identity collection; no original evidence is
migrated. Conditional setup plus one task is 11.7534576 seconds, slower than the
legacy model. At 5, 10 and 100 tasks, the simple setup amortization is respectively
2.3711594, 1.1983721 and 0.1428635 seconds per task. The same cursor must remain
usable; journal gaps, incidents or storage changes require new qualification and
new setup. Setup is not eliminated work.

W2 uses full verification on both arms, with namespace checks, eight synthetic
save/backup/EXE/ESM identities, all scientific hashes and before/after C:/D:
40,000,000,000-byte free-space guards. Median total costs are 1.7624911 versus
1.7593843 seconds: about 0.18%, ordinary variation, with no claimed optimization.
Historical payload reads/hashes remain 71,303,168 bytes and 8,192 calls in both
arms. This is a protection-control simulation, not a live preflight.

For this assignment, the unchanged save helper separately verifies 12,974
historical rows with 173 qualified active-transient exclusions and zero protected
changes before work. Its measured 154.2483605 seconds are a fresh task protection
cost, not a D5G timing. Task source identities, final preservation and unchanged
HEAD/index are recorded in [review](review.md). No historical evidence has been
deleted, normalized, compressed, repacked or rewritten.

## Outcome and decision boundary

The useful positive result is a working, measured, conditional NTFS change
detector with fresh scientific/critical hashing and explicit failure behavior.
The useful negative result is that this design does not meet the frozen
equal-protection efficiency contract. Merkle roots or signed manifests alone
do not repair the missing current-byte observation; [design comparison](designs.md)
also examines immutable storage and a smaller full-pass refactor.

The assignment remains **REWORK**, rather than accepted engineering. The
[policy proposal](policy-proposal.md) is a concrete, inactive review artifact;
it preserves a full fallback and identifies the missing storage/guarantee
decision. B6, RG2-D5H, publication and all live operations remain outside scope.
