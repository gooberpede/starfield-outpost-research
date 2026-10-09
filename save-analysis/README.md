# Offline Save Analysis

The [manual S0–S7C brief](../docs/implementation-briefs/CODEX_RESEARCH_BRIEF_manual_save_corpus_S0-S7C.md), explicitly invoked by the user, authorizes narrow project-authored offline scripts and copies of 17 named saves. The [completed first pass](../docs/experiments/manual-save-corpus-S0-S7C.md) uses installed CPython/standard-library zlib for a bounded empirical container transform and descriptive comparisons. No general save parser/editor or third-party parser implementation is adopted. Candidate public implementations remain research leads in [SOURCES.md](../docs/SOURCES.md).

Future project-authored scripts belong in [scripts/](scripts/README.md). Use immutable, hashed local copies; originals and decompressed output stay outside Git. Default analysis is read-only and writes new, separately named outputs. No save rewriting, repacking, repair, or loading a modified save without a separate approved experiment.

Label original-file, decompressed-stream, and record-relative offsets explicitly. Record format/version fields as observed, bounds, transformations, dependencies, and unresolved encodings. Do not assume another game's layout or a historical parser's compatibility. A byte diff is a lead, not automatically a record or semantic field.

Correlate controlled runtime observations and reload behaviour with saved representations. Use no-action controls and independent samples appropriate to each claim. Preserve uncertainty between stored, inherited, reconstructed, and transient state. See [EVIDENCE_STANDARD.md](../docs/EVIDENCE_STANDARD.md).


## Active identification diagnostics (SOR-EXP-0009)

[Research report](../docs/experiments/active-outpost-identification.md). `scripts/outpost_record_framing.py` reads in-memory bytes and returns exact directory-bounded R3 records plus a narrowly guarded case-5 beacon-prefix diagnostic; it writes nothing. `scripts/investigate_active_outposts.py --run FRESH-NAME` verifies existing protected/control/HIST/donor manifests, reads originals/archives in memory, applies existing physical/disk guards and writes exclusive ignored JSON under `.local-work/active-outpost/`. Original/archive hash changes abort. No save/target/database mutation or raw decoded output. Stdlib and existing project modules only; requires already-verified local manifests/copies and installed Python. This is hypothesis tooling, not a tracker importer or active-outpost classifier; semantic results remain INDETERMINATE for explicit reconstruction/ownership gaps. `scripts/test_outpost_record_framing.py` runs six synthetic test methods; `--corpus --run FRESH-NAME` independently walks 11 selected verified saves and writes an exclusive ignored receipt. No live access, dependencies/downloads or automatic upload.
