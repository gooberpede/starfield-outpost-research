# Selected Evidence

- **SOR-EV-0053 / SOR-EXP-0045:** [C2 report](../cargo-links/transport/report.md), [source pins](../cargo-links/transport/sources.csv), [native locators](../cargo-links/transport/functions.csv), [review](../cargo-links/transport/review.md). Authored interpretation/metadata REVIEW-REQUIRED; raw installed PEX/PSC/native/definition/save derivatives LOCAL-ONLY under ignored `.local-work/c2-transport/`. No live capture or publication clearance.

- **SOR-EV-0052 / SOR-EXP-0044:** [C1 report](../cargo-links/configuration-ui/report.md), [pins](../cargo-links/configuration-ui/sources.csv) and [review](../cargo-links/configuration-ui/review.md). Authored synthesis/metadata REVIEW-REQUIRED; screenshot, save, SWF/ABC, installed source and native exports remain LOCAL-ONLY under `.local-work/c1-cargo/`, `.local-work/recon/c1-cargo-*` and `.local-work/screengrabs/`. No runtime capture or publication clearance.


- SOR-EV-0042: [Resource availability report](../resource-availability/report.md), [source pins](../resource-availability/sources.csv), [validation](../resource-availability/validation.md), [review](../resource-availability/review.md). Native/raw/private inputs LOCAL-ONLY; authored selected findings REVIEW-REQUIRED. No new live observations or publication clearance.

- [Position capability register](../../position-model/capabilities.md) consolidates existing evidence IDs without reclassification. Fresh check receipts/patches indexed in [review](../../position-model/review.md); raw derivatives remain local, authored synthesis REVIEW-REQUIRED.

- SOR-EV-0039 approved live continuation: [0.6.0 native history](../position-write-history/live-attempt-01.md), [selected cases](../position-write-history/live-attempt-01-cases.csv), [provenance](../position-write-history/live-attempt-01-sources.csv), [review](../position-write-history/live-attempt-01-review.md). Exact saved/native XYZ sampled match, earlier Z discrepancy not reproduced; partial history and frame/lifetime gaps. 562,326 verified records, clean retirement/postflight, 21 sealed files. Raw evidence LOCAL-ONLY; authored result REVIEW-REQUIRED.

- SOR-EV-0039 continuation: [position-write history qualification](../position-write-history/report.md), [source/receipt hashes](../position-write-history/sources.csv) and [review](../position-write-history/review.md). Authored REVIEW-REQUIRED; raw native/save/capture/build/private artifacts LOCAL-ONLY. 16000 concurrent fixture records, 27 decoder/seven control checks and 6563 protected pins; no native 060 live equivalence/publication clearance.

- SOR-EV-0036: [EXP0028 final thread-control analysis](../event-latency/thread-control-final-report.md).
  Completed B; 32 diagnostic workflows, five API cases, retained R1/R2/repair
  negatives and independent postflights. Authored REVIEW-REQUIRED; raw traces,
  WAL/memory, executables/intermediates/private receipts LOCAL-ONLY. No live
  qualification, new scientific finding or publication clearance.

- SOR-EV-0034: [EXP0026 latency/transport review](../event-latency/README.md).
  Authored source/comparison REVIEW-REQUIRED; original 0.1.2/all six controls,
  profiling/WAL/raw/private receipts LOCAL-ONLY. No Starfield oracle evidence,
  scientific promotion or publication clearance.

- SOR-EV-0033: [EXP0025 instrumentation review](../event-instrumentation/README.md).
  Authored source/contracts REVIEW-REQUIRED; disposable/raw/native/private receipts
  LOCAL-ONLY. No new Starfield oracle evidence or publication clearance.

- SOR-EV-0032: [EXP0024 report](../event-associated-position-oracle-and-build-mode.md)
  and [review](../event-oracle/review.md). Authored native analysis/design
  REVIEW-REQUIRED; native exports/raw/private receipts LOCAL-ONLY.
  25 checkpoints/14,645 raw sections reverified; no new live oracle evidence.

- SOR-EV-0026: [durable-center review package](../durable-center/README.md), SOR-EXP-0018. Original authored numeric selections REVIEW-REQUIRED; raw saves/captures/native exports LOCAL-ONLY. No complete continuous geographic solution or publication clearance.

- SOR-EV-0024: [initial observer live results](../../audits/beacon-observer-initial-live-results.md), SOR-EXP-0016. Nine snapshots/5,233 verified raw sections, protected Save25 and archived Save26; scoped workshop offset and post-reload XYZ observations. Raw/session/save/logs LOCAL-ONLY; authored interpretations REVIEW-REQUIRED.

- SOR-EV-0023: [actual observer deployment preflight](../../audits/beacon-observer-post-deployment-preflight.md), SOR-EXP-0016. Installed identity/configuration/output/control/space checks; original receipts LOCAL-ONLY. User-reported smoke test distinguished from unobserved fresh runtime readiness; [operator card](../beacon-observer/Save25-operator-run-card.md) REVIEW-REQUIRED before launch. No new scientific finding.

- SOR-EV-0022: [broad beacon observer offline qualification](../beacon-observer/README.md), SOR-EXP-0016. Selected authored hashes/results REVIEW-REQUIRED; full synthetic captures, binaries, private input/source/database receipts stay LOCAL-ONLY. No Starfield evidence, semantics promotion or publication clearance.

SOR-EV-0020: [two-outpost anchor report](../two-outpost-site-anchors-and-beacon-coordinates.md) and [selected evidence/review](../two-outpost-anchor/README.md). Save25 manifest, exact parent/pair/XYZ comparisons and native export identities; REVIEW-REQUIRED, original/bulk payload LOCAL-ONLY.

SOR-EV-0019: [planetary surface-anchor report](../planetary-surface-anchor-semantics.md) and [selected numeric/hash/locator evidence](../planetary-surface-anchor/README.md), SOR-F-0018. Six source/decoded hash rows, 21 saved pair observations, three fixed-world values and 15 native-export identities are authored REVIEW-REQUIRED derivatives. Raw saves, decompressed streams, ESM payloads, Ghidra exports and private locators stay LOCAL-ONLY; native instruction limits and incomplete generic wire closure remain explicit. No publication clearance.

**No research evidence is bundled at scaffold creation.** This is not a dumping ground for raw captures.

Keep original saves, decompressed files, game binaries/assets, imported Ghidra/debugger databases, memory dumps, private correspondence, and unreviewed bulk output outside Git. Use an external workspace or `.local-work/`; generated `exports/` is ignored except its README. A private remote is still a disclosure boundary.

Before tracking an evidence item, review its scientific relevance, provenance, permissions, sensitive data, and publication classification. Use [the bundle template](../../templates/evidence-bundle.md). Record exact source/derivative hashes, byte sizes, tools and transformations, baseline/sample IDs, supporting claim ranges, rights/approval records, and limits.

`REVIEW-REQUIRED` is a classification, not permission to commit private material. Any tracked item requires explicit approval for that repository/disclosure scope even if public-release review is still pending. `CLEARED-FOR-PUBLICATION` does not itself authorize a visibility change.

## Exact bytes

Under this directory `.gitattributes` disables Git text conversion for evidence files, even textual JSON/CSV/captures. Authored `README.md` files are the only directory-specific exception and use LF. Do not put an original byte-sensitive capture in a file named `README.md`.

Do not run formatters or encoding/line-ending normalization across originals. Preserve immutable inputs and write separately named derivatives with recorded transformations and hashes. Confirm staged blob bytes for evidence where exact identity matters. Binary classification does not authorize inclusion; ignored extensions require a narrowly reviewed exception, not habitual `git add -f`.

Avoid OS usernames, personal save names, absolute local paths, or permission correspondence in public bundle metadata. Neutral IDs can point to local sources without pretending those sources are publicly reproducible.

## SOR-EV-0012 — Mature-save validation index

[Separate report](../mature-save-outpost-validation.md), [validation and review inventory](../mature-save-validation/validation.md). SOR-EXP-0006 / SOR-SAMPLE-0029 / SOR-F-0012 / SOR-ST-0015–0016. Selected authored reference/count/window/topology ledgers are REVIEW-REQUIRED; no raw evidence is added under this directory. Local `.local-work/mature-save-validation/run-07/` holds immutable save extraction (SHA-256 `a1d4490a6b41c05ad08f68b2efa28f71d6ebac56cb9aabf55eb61356833b57e2`), comparison, input/script identities, corpus grammar and negatives. Separate independent-checks/corpus-challenge/source-inputs/preservation/review artifacts remain local. Scientific confidence does not clear publication; exact local sample/JSON names and private UUIDs are omitted from selected tables.

## SOR-EV-0013 — Historical inventory and location triage

[SOR-EXP-0007 report](../historical-save-inventory-triage.md), [validation and review inventory](../historical-save-inventory/validation.md). Selected neutral-ID/hash/numeric manifest, presence matrix, version ledger and location-candidate hops are REVIEW-REQUIRED. Exact personal paths/names, originals, copies, complete fingerprints and failed/exploratory receipts remain LOCAL-ONLY under `.local-work/historical-inventory/`; no raw evidence is added here. Frozen scan-04 hashes identify 278 originals and 275 full fingerprints, with independent control/baseline comparisons. Location fallback remains separate from classification. Publication and scientific confidence remain independent.


## SOR-EV-0015 — Active identification record/native evidence

[SOR-EXP-0009](../active-outpost-identification.md), [validation/inventory](../active-outpost-identification/validation.md). SOR-F-0014 / SOR-ST-0017 / SOR-H-0006. Selected source-hash/count/flag ledgers are authored REVIEW-REQUIRED material. Full fingerprints, executable text, Ghidra TSVs, raw source locators and failed probes stay LOCAL-ONLY under `.local-work/active-outpost/` and `.local-work/recon/active-outpost-*`. Frozen flags-03 digest and independent 11-save/874,242-record audit are in the report. Exact mechanical framing and conditional flag mappings do not establish active ownership or conclusive zero. No raw evidence is newly added under this directory.


## SOR-EV-0016 — Alternate beacon identity and membership follow-up

[SOR-EXP-0010](../active-outpost-membership-completion.md), SOR-F-0015 / SOR-ST-0018 / SOR-H-0007; [validation and local evidence identities](../active-outpost-membership-completion/validation.md). Selected numeric/hash/offset ledgers are authored REVIEW-REQUIRED. Raw saves, decoded payloads, private locators, BA2/PEX probes and Ghidra native exports remain ignored LOCAL-ONLY. Conditional R1 association, inherited flags and quest-control uncertainty remain visible; no complete membership/absence or publication claim.

- SOR-EV-0017: [scoped ordinary beacon detector](../ordinary-outpost-beacon-detection.md), minimal numeric ledgers and validation under `../ordinary-outpost-beacon-detection/`; REVIEW-REQUIRED. Full receipts/raw inputs/private oracle remain LOCAL-ONLY; no publication clearance.

- [SOR-EV-0025 — Workshop relocation and bounds](../workshop-origin/README.md): selected capture/native/transition ledgers and local reproduction/provenance; full raw/native evidence LOCAL-ONLY.

- **SOR-EV-0035 / SOR-EXP-0027:** [startup fail-fast investigation](../event-latency/startup-failfast-investigation.md),
  exact compiled exception boundaries, 19-case matrices, preserved pilots and
  [qualification/review](../event-latency/startup-review.md). Private receipts,
  dumps, raw fixture WALs and binaries stay in ignored `.local-work/adapter-startup`
  and separately named event-instrumentation runs. No new Starfield sample or
  semantic promotion; authored REVIEW-REQUIRED, raw LOCAL-ONLY.

- **SOR-EV-0040 / SOR-EXP-0032:** [Workshop membership/root inventory](../workshop-membership/README.md), [source hashes](../workshop-membership/sources.csv) and [validation/review](../workshop-membership/review.md). Selected authored reference counts/native contracts REVIEW-REQUIRED. Full instance/member/unresolved ledgers, protected archive/game/database inputs, native exports, reproduction and failed/superseded probes remain ignored LOCAL-ONLY under `.local-work/workshop-inventory/`. No raw/private evidence copied into this directory or cleared for publication.

- **SOR-EV-0041 / SOR-EXP-0033:** [Workshop population rework](../workshop-population/README.md), selected authored counts/contracts/source hashes REVIEW-REQUIRED. Full historical/typed/component/default ledgers, native exports and failed probes remain ignored LOCAL-ONLY under `.local-work/workshop-population-rework/`; original 657 evidence remains unchanged.

- **SOR-EV-0044 / SOR-EXP-0036:** [Local readiness pre-live package](../local-readiness/review.md).
  Authored schema/maps/qualification REVIEW-REQUIRED. Raw reference captures,
  native exports, disposable fixture WAL, DLL/ZIP/builds and private review/pin
  receipts remain ignored LOCAL-ONLY under `.local-work/local-readiness/`.
  No new live evidence or publication clearance.

  The [scientific reassessment](../local-readiness/scientific-value-reassessment.md) rejects the proposed live session. Earlier engineering receipts remain preserved historical evidence.

- **SOR-EV-0046 / SOR-EXP-0038:** [E1 inorganic extractor reference](../inorganic-extractors/report.md), native/state/directional-link/production map and selected pins REVIEW-REQUIRED. Raw saves, definitions, exports and receipts remain LOCAL-ONLY in ignored .local-work/e1-extractors and .local-work/recon. No new live evidence.

- **SOR-EV-0046 continuation:** [Production arithmetic/modifiers](../inorganic-extractors/production-report.md) and [pins](../inorganic-extractors/production-sources.csv), REVIEW-REQUIRED authored reference; native/definition/save receipts under `.local-work/e1-production/` and `.local-work/recon/` remain LOCAL-ONLY. Feasibility REVISE; no new live evidence.

- **SOR-EV-0046 stacking continuation:** [Report](../inorganic-extractors/stacking-report.md) and [pins](../inorganic-extractors/stacking-sources.csv), REVIEW-REQUIRED. New raw exports/definition/script inventories and receipts remain LOCAL-ONLY under `.local-work/e1-stacking/` and `.local-work/recon/`; no new runtime/save evidence.

- **SOR-EV-0046 arithmetic/UI continuation:** [Report](../inorganic-extractors/arithmetic-report.md) and [pins](../inorganic-extractors/arithmetic-sources.csv), authored REVIEW-REQUIRED. Raw native exports, definitions, screenshots, BA2/SWF/ABC and verification receipts remain LOCAL-ONLY under `.local-work/e1-arithmetic/`, `.local-work/screengrabs/` and `.local-work/recon/`. No new runtime evidence.

E1 interval/size continuation: raw inventories, exact physical-field spans, pinned native exports and review receipts remain ignored under `.local-work/e1-intervals/` and `.local-work/recon/e1-intervals-*`. Authored [report](../inorganic-extractors/resource-intervals.md) and tables are REVIEW-REQUIRED; raw definitions/decompilation are LOCAL-ONLY.

- **SOR-EV-0047 / SOR-EXP-0039:** [E2 organic native reference](../organic-facilities/report.md) and [pins](../organic-facilities/sources.csv), authored REVIEW-REQUIRED. Raw definition/native/UI/save receipts remain ignored under `.local-work/e2-organic/` and `.local-work/recon/e2-specialist-*`; game assets and saves are excluded from review patches. No new runtime acquisition.

- **SOR-EV-0053 / SOR-EXP-0045 transit continuation:** [model](../cargo-links/transport/transit.md), [source pins](../cargo-links/transport/transit-sources.csv), [native locators](../cargo-links/transport/transit-functions.csv), [review](../cargo-links/transport/transit-review.md). Additional raw/native/definition receipts remain LOCAL-ONLY under ignored `.local-work/c2-transit/`; authored metadata/interpretation REVIEW-REQUIRED. No live capture or publication clearance.

- **SOR-EV-0064 / SOR-EXP-0056:** [SD2 report](../shared-outpost-storage/report.md), [sources](../shared-outpost-storage/sources.csv), [methods](../shared-outpost-storage/methods.md) and [review](../shared-outpost-storage/review.md). Raw definitions/PEX/native exports/original-save derivatives remain ignored LOCAL-ONLY under `.local-work/sd2-shared/`; authored interpretation and compact numeric metadata REVIEW-REQUIRED. No distribution clearance.
