# Licensing, public comparisons and publication surface

**The project already makes an explicit GPL-3.0-or-later grant for material
its contributors can license.** That does not clear game-derived evidence,
private state or an exact public tree/history boundary. This is an audit of
existing statements and decisions, not legal advice or clearance.

## Local grant and incorporation boundary

[LICENSING.md](../../../LICENSING.md) explicitly chooses version 3 or any later
version, separates project-authored code/documentation from outside content,
and avoids adding downstream permission requirements. Root LICENSE contains
the GPLv3 legal text; that text alone would not establish the or-later choice.
It was not modified. Many source files carry an SPDX identifier; coverage is
not uniform and is inventoried locally in `source-notices.json`. Missing an
individual SPDX line is a notice-consistency question, not evidence that the
root grant vanished or that unknown third-party material became owned.

[Notices](../../../THIRD_PARTY_NOTICES.md) and [SOR-P-0001](../../PERMISSIONS.md)
identify the exact Ian Patterson SFSE PluginAPI.h header-only MIT grant,
copyright/permission/disclaimer, pinned upstream commit and user's specific
acceptance. This does not include the SFSE runtime, other SDK source,
CommonLib or Address Library data. No new component or licence basis was
introduced by RR1. No incompatible licence was newly demonstrated; that
bounded result is not a full per-line rights audit of all historical source.

SOR-P-0002 authorizes maintainer-authored sibling material with provenance,
excluding embedded third-party content; SOR-P-0003 only permits local donor-save
examination and expressly excludes original payload redistribution. Installed
Ghidra/xEdit/compilers are separate tools, not vendored dependencies. Bethesda
inputs, snippets, compiled assets and derived tables need their own review.
Confirm public author/credit wording and contributor rights rather than infer
legal identity or ownership from a login. Existing source/credit registers were
read and remain untouched under RR1's new-files-only boundary. This document
records RR1 comparator consultation provenance locally instead of editing them.

## Three independently inspected public comparators

Retrieved **2026-10-20, Australia/Sydney**, through read-only GitHub connector
and web views. URLs below identify actual inspected files on main; exact remote
commit was not supplied by these retrievals. Local selected reference text and
SHA-256 manifest are retained under `.local-work/rr1/comparators/`. Treat this
as a retrieval-date comparison, not a verified immutable commit snapshot or
proof that every comparator file is mutually current. No fork, full mirror,
package installation, source execution or wholesale documentation copying.

| Public project / inspected sources | Observed practice | Appropriate lesson and limits |
|---|---|---|
| [Resource Research README](https://github.com/gooberpede/starfield-resource-research/blob/main/README.md), [index](https://github.com/gooberpede/starfield-resource-research/blob/main/docs/README.md), [Ghidra guide](https://github.com/gooberpede/starfield-resource-research/blob/main/ghidra/README.md), [notices](https://github.com/gooberpede/starfield-resource-research/blob/main/THIRD_PARTY_NOTICES.md) | Current baseline precedes historical experiments; supported model, validation scope and superseded allocation trail are explicit. Research owns evidence/history; reproducer owns executable model. Export guide describes reads/writes and analysis assumptions. Original authored material has explicit or-later grant, targeted game evidence excluded from that grant. | Add a current baseline/reader layer here and keep failed routes visible. Its selected-evidence distribution is not permission to distribute this archive's inputs. Comparator validation totals were reported there, not rerun by RR1. |
| [Resource Reproducer README](https://github.com/gooberpede/starfield-resource-reproducer/blob/main/README.md), [pyproject](https://github.com/gooberpede/starfield-resource-reproducer/blob/main/pyproject.toml), [notice](https://github.com/gooberpede/starfield-resource-reproducer/blob/main/THIRD-PARTY-NOTICE.md) | Python >=3.12, stdlib runtime and separate dev test dependency; packaging explicitly says GPL-3.0-or-later. Canonical inputs differ from validation-only oracle. Installation/test/exporter routes are documented; historical commands may be superseded. Normalized game-derived records are outside authored GPL grant. | Separate executable method inputs from original oracle/evidence, and explain what lawful acquisition requires. Public normalized data there is not blanket rights clearance here; do not turn this research archive into a product package. |
| [Outpost Network README](https://github.com/gooberpede/starfield-outpost-network/blob/main/README.md), [package](https://github.com/gooberpede/starfield-outpost-network/blob/main/package.json), [notices](https://github.com/gooberpede/starfield-outpost-network/blob/main/THIRD-PARTY-NOTICE.md) | Reader-oriented capability/development/documentation routes; Node 24 and locked dependency install instructions; ordinary build inputs distinguished from game-dependent regeneration. Authored grant, software notices, separately licensed artwork and official text/data are distinct. Publication/launch still requires explicit decisions. | Adopt clear prerequisites, output/rights boundaries and honest release status. Its artwork/dependency arrangement is not an approved template for this project. Retrieved README candidate-version prose differs from package version; do not assume comparator consistency or treat moving main as one frozen release. |

These comparisons credit gooberpede's authored organization and explanations
as reference evidence. No external implementation or text was incorporated
into tracked source. Third-party notices were consulted to understand boundaries,
not accepted as a new licence for reuse. No upstream contact or disclosure.

## Current inclusion, history and security checks

Before RR1, Git-visible contents were 1,554 tracked files plus the unchanged
supplied brief; 80,916 ignored files were metadata-inventoried at the initial
scan. Ignored source/configuration candidates were inspected for temp/path
effects, but ignored raw saves/captures/binaries were not secret-scanned or
copied. They are excluded from the review patches and proposed release corpus.

`rev-list --objects --all` enumerated **95 commits, 3,783 reachable objects and
2,751 blobs (48,132,323 bytes)**. Every enumerated blob was read by a bounded
metadata-only detector; none exceeded its ten-million-byte skip threshold, so
zero blobs were skipped. Current tracked file bytes were separately scanned.
Detectors cover PEM private-key headers, common GitHub/AWS access-token shapes,
quoted password/secret/API-key/token assignments, email-shaped strings, Windows
user paths, NUL/binary content and named sensitive suffixes. No credential,
private-key, email or binary candidate matched in this inspected surface.

There were **182 reachable blobs with Windows-user-path indicators**; this is
blob count, not distinct usernames or necessarily sensitive personal identity.
Current HEAD also contains machine-local user paths. Values are not pasted into
security receipts: only path/object/type/count metadata is retained. Selected
general project paths already required by the brief appear in the audit's path
inventory. Private correspondence/contact records were not read or exported.

Limits: patterns are not a commercial secret scanner or entropy analysis;
nonstandard tokens, non-path PII and proprietary textual excerpts may escape.
Reachable refs were inventoried; dangling objects, reflogs, remote-only refs,
GitHub release assets and account/security configuration were not cleared.
`git count-objects -v` reported ten pre-existing temporary garbage objects;
these were not deleted, opened or incorporated. No history rewrite or remote
change was made. Named textual derived evidence still needs B4 rights review
even when it is not a proprietary binary or credential match.

Publicly rerunnable scripts also require effect review. Existing observer and
debugger source deliberately contains invasive operations; an audit does not
make those safe quick starts. The current Ghidra wrapper confines output to
local work but hardcodes prerequisite roots; historical packagers can recreate
old external scratch. B3/B5 should distinguish supported entrypoints from
historical records before any public reproduction instructions are adopted.

Maintainer/specialist decisions remain: included claims and build matrix;
per-item game-derived evidence boundary; save/screenshot privacy; author and
contributor notices; intentional public local-path/history policy; exact refs
and release surface. A private repository or a clean HEAD scan does not waive
these decisions. No secret value, payload, legal eligibility or release approval
is asserted by this audit.
