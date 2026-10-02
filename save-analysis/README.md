# Offline Save Analysis

No parser, compressor, schema, dependency, or save sample is supplied or approved. Candidate public implementations are research leads in [SOURCES.md](../docs/SOURCES.md), not adopted code.

Future project-authored scripts belong in [scripts/](scripts/README.md). Use immutable, hashed local copies; originals and decompressed output stay outside Git. Default analysis is read-only and writes new, separately named outputs. No save rewriting, repacking, repair, or loading a modified save without a separate approved experiment.

Label original-file, decompressed-stream, and record-relative offsets explicitly. Record format/version fields as observed, bounds, transformations, dependencies, and unresolved encodings. Do not assume another game's layout or a historical parser's compatibility. A byte diff is a lead, not automatically a record or semantic field.

Correlate controlled runtime observations and reload behaviour with saved representations. Use no-action controls and independent samples appropriate to each claim. Preserve uncertainty between stored, inherited, reconstructed, and transient state. See [EVIDENCE_STANDARD.md](../docs/EVIDENCE_STANDARD.md).
