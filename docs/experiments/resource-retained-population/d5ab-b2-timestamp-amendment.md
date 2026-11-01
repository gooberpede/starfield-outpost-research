# B2 configuration timestamp amendment and explicit retry

2026-11-01, Australia/Sydney. **Correction QUALIFIED / ACCEPT; explicit retry completed and final review ACCEPT.**

After the first approved attempt refused main-menu admission on an unchanged
`StarfieldPrefs.ini` with a changed timestamp, the maintainer instructs:
“Let's try that again - the timestamp change isn't important as long as the
contents haven't changed.” This authorizes one subsequent B2 attempt under the
same card after correction, independent qualification and a fresh successful
preflight. It does not authorize continuing the refused session, silently
replacing a baseline, skipping preservation or automatic further retries.

The first attempt remains preserved as an admission failure before Save52 load
or travel. Its original source/package/plan/preflight and failed receipt remain
historical. Its full postflight must finish before changing pinned source.

## Narrow correction contract

- B2-T01: Configuration guards compare exact preflight byte length and SHA-256;
  timestamps alone do not fail admission. Changed contents must fail even at the
  original size and timestamp. Missing, unpinned or unsafe paths fail closed.
- B2-T02: Keep source/version pins, installed binary/definition metadata guards,
  protected-save/remote namespace gates, disk floors, worker/controller/ownership,
  STOP, evidence and optimization requirements. Do not add full save/raw scans
  during play. Only the existing small configuration files are hashed.
- B2-T03: Disposable positive/adverse controls, affected P4 regressions, exact new
  package/plan/dependency correspondence and independent review pass before GO.
  Native DLL and hook boundaries remain unchanged unless a demonstrated need
  receives separate qualification. The approved named ZIP remains byte-identical.
- B2-T04: Preserve and archive the first partial attempt; use a distinct second
  attempt label, original one-load/one-direct-travel scope and fresh preflight.
  Independent final evidence review and complete/task-only diffs are mandatory.

The [live ledger](d5ab-b2-live-ledger.md) and [approved card](run-card-d5x-b2.md)
retain the governing scientific question and outcome definitions. No original
protected bytes are modified/restored, and no native safety check is waived.
The maintainer owns re-enablement, launch, save load, travel, STOP, normal exit
and Vortex disablement. No commit, push, external disclosure or publication.

## Correction and current qualification

`lightweight` now requires a disjoint configuration/definition roster and exact
coverage by preflight file guards. Every configuration is checked through the
existing regular-path guard, original byte length and original SHA-256, even if
its timestamp still matches. Timestamp changes are returned as diagnostics.
Definition and installed binary/asset metadata checks are unchanged. No new
save/raw/large installed-asset hashing occurs during play.

The source hashes are:

| Source | SHA-256 |
|---|---|
| `d5ab_p4_operations.py` | `b8f4ad8e2262d2ea2c9e389ff604c262e2b96ad4258757a063e42f50892ba238` |
| `d5ab_p4_qualify.py` | `27fc8483d7835b921c042ac6621c60c4e72ff325fe0aad839e79da63d4e1f799` |

Final disposable procedure qualification passes 59 controls, including actual
timestamp changes, same-size content mutation with restored timestamp, missing
pins/files, roster ambiguity, real junction rejection and target-preserving
cleanup. File-symlink rejection is separately labeled modeled. Hash-read
instrumentation confirms small configuration hashing without save/definition/
installed-asset payload reads. Independent repetition also passes all 59.
The existing 218 optimizer controls and 28 admission controls pass with current
source pins. Exact receipts are under `.local-work/d5ab/p4-b2-timestamp-*`;
original versions/failures are retained without overwrite.

The new helper bundle is `.local-work/d5ab/p4-b2-content-package01/`, containing
100 staged members and 99 plan pins. Manifest SHA-256 is
`fe903c92b125e52d98db85fb9a0a7f4e67b1cc5be87576aa1a464a8b22f9379d`;
plan SHA-256 is
`5dc416b48dac92903bc8fa2a006adc562a407dec79236c26e92fabae2639f1c9`.
The named native ZIP and DLL retain their original hashes. Native compiler
inputs, ABI, queue and event schema are unchanged; no native rebuild is needed
for this configuration-only guard correction. The [card](run-card-d5x-b2.md)
now names this plan and attempt 002, preserving its scientific definitions,
phase gates and one-load/one-direct-travel scope.

The package's prospective 29-module roster is explicitly derived from the prior
measured closure with current hashes; it is not labeled a fresh execution trace.
The completed traced attempt-002 full preflight corroborates all 29 modules and
all seven protected equality fields against the first preflight. Preflight
SHA-256 is `9af6437d5c1e615b71e4f3a20c84f0f4040a59e4ec2423d1ea8025f74400e6d5`;
actual closure SHA-256 is
`e1d24e45607475994dd9ad8876c62af783417490406e27c9383474b66a89a7db`.
All 28 actual disposable controller cases pass. The independent reviewer accepts
the exact correction, package, card and preflight, with its full actual return
in `.local-work/d5ab/B2-APPROVED-002-notes/correction-independent-review.md`,
SHA-256 `6aeb8982637c6a70729e39696c57c97d9da6e2de0cc347423be969e4f5624016`.
B2-T01/T02/T03 PASS. B2-T04 PASS: the first partial archive is preserved,
the explicit retry is finalized and independently reviewed, and delivery is
verified. The [final review](d5ab-b2-review.md) records acceptance and limits. Deployment/lightweight checks are
required before retry launch GO; main-menu READY and fresh ACK remain required
before loading Save52. No further automatic attempt is admitted.
