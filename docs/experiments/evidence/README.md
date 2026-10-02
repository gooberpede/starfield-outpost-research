# Selected Evidence

**No research evidence is bundled at scaffold creation.** This is not a dumping ground for raw captures.

Keep original saves, decompressed files, game binaries/assets, imported Ghidra/debugger databases, memory dumps, private correspondence, and unreviewed bulk output outside Git. Use an external workspace or `.local-work/`; generated `exports/` is ignored except its README. A private remote is still a disclosure boundary.

Before tracking an evidence item, review its scientific relevance, provenance, permissions, sensitive data, and publication classification. Use [the bundle template](../../templates/evidence-bundle.md). Record exact source/derivative hashes, byte sizes, tools and transformations, baseline/sample IDs, supporting claim ranges, rights/approval records, and limits.

`REVIEW-REQUIRED` is a classification, not permission to commit private material. Any tracked item requires explicit approval for that repository/disclosure scope even if public-release review is still pending. `CLEARED-FOR-PUBLICATION` does not itself authorize a visibility change.

## Exact bytes

Under this directory `.gitattributes` disables Git text conversion for evidence files, even textual JSON/CSV/captures. Authored `README.md` files are the only directory-specific exception and use LF. Do not put an original byte-sensitive capture in a file named `README.md`.

Do not run formatters or encoding/line-ending normalization across originals. Preserve immutable inputs and write separately named derivatives with recorded transformations and hashes. Confirm staged blob bytes for evidence where exact identity matters. Binary classification does not authorize inclusion; ignored extensions require a narrowly reviewed exception, not habitual `git add -f`.

Avoid OS usernames, personal save names, absolute local paths, or permission correspondence in public bundle metadata. Neutral IDs can point to local sources without pretending those sources are publicly reproducible.
