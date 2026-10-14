# Offline Save Analysis

The [manual S0–S7C brief](../docs/implementation-briefs/CODEX_RESEARCH_BRIEF_manual_save_corpus_S0-S7C.md), explicitly invoked by the user, authorizes narrow project-authored offline scripts and copies of 17 named saves. The [completed first pass](../docs/experiments/manual-save-corpus-S0-S7C.md) uses installed CPython/standard-library zlib for a bounded empirical container transform and descriptive comparisons. No general save parser/editor or third-party parser implementation is adopted. Candidate public implementations remain research leads in [SOURCES.md](../docs/SOURCES.md).

Future project-authored scripts belong in [scripts/](scripts/README.md). Use immutable, hashed local copies; originals and decompressed output stay outside Git. Default analysis is read-only and writes new, separately named outputs. No save rewriting, repacking, repair, or loading a modified save without a separate approved experiment.

Label original-file, decompressed-stream, and record-relative offsets explicitly. Record format/version fields as observed, bounds, transformations, dependencies, and unresolved encodings. Do not assume another game's layout or a historical parser's compatibility. A byte diff is a lead, not automatically a record or semantic field.

Correlate controlled runtime observations and reload behaviour with saved representations. Use no-action controls and independent samples appropriate to each claim. Preserve uncertainty between stored, inherited, reconstructed, and transient state. See [EVIDENCE_STANDARD.md](../docs/EVIDENCE_STANDARD.md).


## Active identification diagnostics (SOR-EXP-0009)

[Research report](../docs/experiments/active-outpost-identification.md). `scripts/outpost_record_framing.py` reads in-memory bytes and returns exact directory-bounded R3 records plus a narrowly guarded case-5 beacon-prefix diagnostic; it writes nothing. `scripts/investigate_active_outposts.py --run FRESH-NAME` verifies existing protected/control/HIST/donor manifests, reads originals/archives in memory, applies existing physical/disk guards and writes exclusive ignored JSON under `.local-work/active-outpost/`. Original/archive hash changes abort. No save/target/database mutation or raw decoded output. Stdlib and existing project modules only; requires already-verified local manifests/copies and installed Python. This is hypothesis tooling, not a tracker importer or active-outpost classifier; semantic results remain INDETERMINATE for explicit reconstruction/ownership gaps. `scripts/test_outpost_record_framing.py` runs six synthetic test methods; `--corpus --run FRESH-NAME` independently walks 11 selected verified saves and writes an exclusive ignored receipt. No live access, dependencies/downloads or automatic upload.

## Two-outpost anchors — SOR-EXP-0014

[Report and evidence](../docs/experiments/two-outpost-anchor/README.md). `scripts/research_two_outpost_anchors.py` explicitly copies/hashes Save25 into an exclusive ignored corpus, verifies available frozen originals/archives, streams read-only decoded copies, records all supported candidates/parents/pairs/prefix XYZ/name queues and the old cache ambiguity, then compares fixed ESM/private network only after extraction. Reads catalog/ESM/executable and stdlib/project modules; no target/database/network/Git effects. `scripts/analyze_two_outpost_anchors.py` reads that result and exclusively writes selected authored CSV/JSON to the given output directory. No guessed scale/orientation or importer schema. Both scripts’ exact command/prerequisite/effect/scratch/40 GB guard details are in the evidence README; raw receipts stay local and authored results await critical review.

## Workshop membership and native roots — SOR-EXP-0032

[Interface/schema](../docs/experiments/workshop-membership/schema.md) documents `workshop_inventory.py`, qualified CLI `research_workshop_inventory.py`, exact all-type definition context and original adversarial tests. Full instance/member/possible-missed ledgers stay ignored/local; unknown categories/names and historical owners are preserved. `verify_workshop_inventory.py` checks completed 27-label action/control results, selected 63 prior extractor owners, 17 outside-base leads, comparative names and protected/frozen/sealed input hashes, writing a new local receipt. No target/save/database/Git changes or third-party dependencies. Current modern explicit root representation only, no general importer or exhaustive player population.

## Workshop population rework — SOR-EXP-0033

[Qualified interfaces](../docs/experiments/workshop-population/schema.md) add actual ordered type decoding, full reference-prefix audit, global/component framing and an independent root supplement. 657 preserved +191 supported =848, with full member/owner and candidate ledgers retained locally. 18 new adversarial tests supplement 61 existing regressions. Original exhaustive population acceptance remains distinct from positive detection. All tools are offline, stdlib/project only, source-hashed with 40 GB C/D guards; no live/save/database/Git effects.
