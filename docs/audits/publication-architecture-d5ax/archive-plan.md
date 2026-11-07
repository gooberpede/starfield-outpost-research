# Historical brief and audit archive design

## Accounting universe

All frozen paths under `docs/implementation-briefs/` and `docs/audits/`, plus the supplied untracked D5AX source brief. The 371 tracked paths and one supplied path are the complete input universe. New D5AX deliverables and future ZIP containers and indexes are outside this frozen denominator. The full path census classifies them separately when they enter a later candidate.

| Category | Paths | Rule |
| --- | ---: | --- |
| ARCHIVED_SOURCE_DOCUMENTS | 188 | 186 historical briefs/amendments and two standalone administrative reports |
| REMAINING_LOOSE_SOURCE_DOCUMENTS | 136 | 135 tracked eligible sources and supplied D5AX |
| GUIDING_READMES_AND_INDEXES | 4 | Directory READMEs |
| MANIFESTS_OR_OTHER_GENERATED_METADATA | 44 | Structured inventory or audit metadata retained at existing paths |
| EXCLUDED_NON_SOURCE_FILES | 0 | No path meets the placeholder or out-of-scope extension rule |
| Whole frozen universe | 372 | 188 + 136 + 4 + 44 + 0 |
| TOTAL_ELIGIBLE_SOURCE_DOCUMENTS | 324 | 188 + 136 |

The 4 READMEs are classified individually in the [path census](tracked-inventory.csv). B0–B5, RR1 and D5AS–D5AX governing briefs identified by the proposed naming rule remain loose, alongside any files whose names do not designate a standard historical brief or amendment. They count in the eligible denominator. Seven briefs initially assigned to archives remain loose following Review01. These preserve active reading, fallback Grid and scratch policy, completion governance, D5AT's amended scope and C2B save-protection authority. The [navigation exceptions](navigation-exceptions.csv) give the current direct routes. All current publication audit packages, scientific reviews and audit scripts remain loose. The initial narrow administrative group contains the documentation spacing and scaffold-validation records. A wider administrative archive should be separately enumerated after current-reader routes stabilize.

| Proposed path | Members | Selection |
| --- | ---: | --- |
| `docs/implementation-briefs/assignment-history.zip` | 99 | Historical named briefs/amendments outside resource-generation family |
| `docs/implementation-briefs/resource-generation-history.zip` | 87 | Historical RG2 and Episode-era briefs/amendments |
| `docs/audits/administrative-history.zip` | 2 | Standalone administrative provenance |
| Total | 188 | Exact [member map](archive-members.csv) |

## Lookup and lossless migration

Keep a local README and an adjacent per-container member CSV with stable brief or audit identifier, exact original repo-relative path, ZIP member path, worktree bytes and SHA-256, source commit/index blob, context and current authority. Include container hash/size, tool/version and compression settings in a separately enumerated metadata row. The proposed member path is the complete original repo-relative path, preserving name, case and directory context. Check exact and case-folded uniqueness, portable normalization, reserved names, traversal, absolute/drive/UNC targets, links and ZIP extraction hazards. The census found no case-folded path collisions. Re-run on the final membership and validate the whole planned extraction tree before writing.

Use standard ZIP Deflate with a deterministic order and documented metadata. Record how CRLF and index bytes differ. Archive exact approved original source bytes using the chosen checkout policy, then compare each ZIP member's length, SHA-256 and stream bytes against that exact original. Read ZIP directory records and reject extra/missing members or unexpected type/name/size. Validate isolated extraction under a fresh safe root and repeat checks after the final candidate checkout. A checksum in the ledger is evidence of identity. The future byte verification requires both original and extracted bytes.

A GitHub link can lead to the local README's stable archive entry, the archive file, or an explicitly selected immutable historical commit path. A member citation shows archive name and internal path as text. Provide download and safe extraction steps. Current links to a loose source must be rewritten to the README, original report/review or a stable archive entry before removal. Keep a separately indexed loose file or navigation stub where a current-facing inbound route warrants it. A stub is a new guide/index entry, outside the source-member count. Preserve historical Git links at their original commits and preserve relative text inside original source members.
