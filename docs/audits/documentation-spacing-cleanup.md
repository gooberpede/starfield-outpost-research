# Documentation spacing cleanup review

2026-10-14, Australia/Sydney. Governing [brief](../implementation-briefs/CODEX_BRIEF_SOR_documentation_spacing_cleanup.md).

**COMPLETE — PASS**, documentation maintenance only, submitted for maintainer and
ChatGPT critical diff review. One primary agent; no reviewer or specialist agent,
as explicitly required by this brief. No scientific evidence state, claim,
confidence, acceptance verdict, attribution or permission decision was changed.

## Scope and changes

The full Git-visible authored documentation inventory contained **372 Markdown
files**, including root documentation, templates, historical authored reports,
tool READMEs and authored evidence-directory READMEs. **255 existing files** were
corrected. This new audit report adds one task-authored file: **256 task-changed
files**, with **373 authored Markdown files** checked including this report.
The supplied, pre-existing untracked brief is preserved verbatim and included only
in the complete patch. There were no pre-existing tracked modifications.

The other Git-visible documentation format was a third-party `LICENSE.txt`;
it was classified as a protected legal/source document and excluded. No affected
authored TXT, RST or AsciiDoc documentation was found. Raw evidence and original
outputs, scientific source/tests, machine-readable data and local receipts were
excluded from editing. No game, save, native tooling or analysis database access
was needed.

Representative corrections:

| Before | After |
|---|---|
| `the657-root` | `the 657-root` |
| `adds191` | `adds 191` |
| `848total` | `848 total` |
| `89FURN` | `89 FURN` |
| `observer0.5.0` in prose | `observer 0.5.0` |
| `40GB` in prose | `40 GB` |
| `fullXYZ` in prose | `full XYZ` |
| `AllCS1–CS8` | `All CS1–CS8` |

Counts glued to known sample labels were separated contextually, including
`S1 59 template`, `Save52 371 templates`, and `S1 297569` / `Save52 1451260`
end offsets. The latter offsets are independently restated in the population
[validation document](../experiments/workshop-population/validation.md). The
`060 16824` version/count separation agrees with the cross-session
[report](../experiments/cross-session-center/report.md). Digits were not changed.

## Protection and exclusions

Preserved technical identities include `Save52`, `ExtraFlags9C`, `Extra80`,
`ExtraWorkshop`, `FormID`, `Starfield.exe`, `0x140F4AB80`, `+0xD3`, `ff01b58f`,
`FURN`, `STAT`, `PKIN`, `A0`, `CS1`, `Is3DLoaded`, `binary32`, `uint32`,
filenames, source locators, URLs, options, offsets and evidence IDs. Code fences,
inline code, quoted primary material, blockquotes, link destinations/reference
definitions, literal expressions and serialized examples remain unchanged.
Historical source locator short names in the population route table remain exact.

Remaining broad letter/digit detector matches are classified in the local
candidate ledger as technical notation/identity, source/path, protected material
or unresolved shorthand. Ambiguous shorthand such as `ref94`, `ref912`,
`save162`, `Extra78d370`, `EFlags514` and `Workshop002` remains unchanged:
spacing could imply an offset, test count or different identity. Field/model
notation such as `coarseX`, `fineY`, `lat0`, `mod49152`, `seq1–3` and `xor1`
also remains unchanged. Known malformed ordinary prose has been repaired.
Literal expressions such as `17R1+21R2+9R4=47units` are protected examples,
not prose transformation targets. This is a typography conclusion, not semantic
validation of those expressions or shorthand.

## Cause and checks

### Independent-review REWORK and correction

The initial submission was **REWORK**, not accepted: independent review found
`KERNEL32`, native `Wait3D` and section `2a` incorrectly split. The original
non-whitespace comparison passed despite these false positives; its identifier
inventory was too narrow. That initial PASS claim is superseded by this rework
and the stronger checks below. The maintainer's correction is adopted here;
the revised package still awaits critical review.

The entire inserted-space population was revisited against the original-byte
snapshot, rather than applying global replacements to the three examples.
The initial inventory contained 5,818 changed alphanumeric token occurrences
(3,461 unique before/after pairs). A second inventory examined letter-only
splits, including coordinate/field aliases; source-token collisions were checked
against existing repository text without executing research tools.

In total, 93 false-positive or conservatively protected token/alias occurrences
were restored: 69 module, symbol, state, short-byte/section, representation or
named-source occurrences; 19 coordinate/field aliases; and five further native
offset occurrences found by the expanded check. Examples beyond the reviewer’s
three cases include `Is3DLoaded`, `System32`, lowercase `kernel32`, `0a`, `3a`,
`+a0`, `+a8`, `+a08`, `XYZ12`, `floorXY8`, `MPSC4096`, `TLSbit0`, `d3bit2`,
`floorXY`, `Xorigin` and named run/source labels such as `final04` and
`validation04`. Legitimate prose improvements, including counts, units and
version-label separation, remain. One original document now has no net change,
which reduces the changed-original count from 256 to 255.

The new checks compare protected tokens at their original character positions,
so spaces inside a token fail even when all non-whitespace characters agree.
They cover 102 reviewed technical-token occurrences, 447 short-byte/section-label
occurrences, 1,107 native offsets, 1,511 symbol/module/directory/identity-family
occurrences, and an expanded filename/source-extension inventory. All pass.
The five `+a8`/`+a08` failures were recorded and repaired before the final pass.
The local proposal detector now excludes these reviewed technical families and
short hexadecimal tokens; it does not reinterpret them as English count labels.

The prior submitted patches/checks remain in
`.local-work/spacing-cleanup/rework-01/`; restoration and identifier-check
receipts retain the false positives. Current complete/task-only patches and
receipts replace the initial handoff. No additional scientific evidence,
authority, research computation or acceptance status was introduced.

**Cause not established.** Static inspection of tracked generator/template and
text-emission sites found no demonstrated common mechanism producing the prose
defects. No generator, computation or test code was changed; no generator
regression test or expensive native test was applicable.

| Mandatory criterion | Result / limits |
|---|---|
| Entire authored documentation scope surveyed | PASS; complete path manifest and broad candidate inventory retained. |
| Confirmed spacing defects corrected | PASS; contextual refinements plus an independently rerun full detector, with remaining matches classified. |
| Scientific text/value preservation | PASS; each edited original has identical non-whitespace character sequence and digit/dot sequence. This mechanical check supports preservation, not scientific semantics. |
| Protected material and identities | PASS after REWORK; exact protected-span comparisons, original-position symbol/token/section/offset checks, addresses/hashes, stable IDs and expanded filenames checked. Non-whitespace equality alone is insufficient. |
| Links, encoding, Unicode and whitespace | PASS; internal link/path and referenced-heading checks show no regressions; UTF-8 decodes, BOM checks, original newline counts and non-whitespace Unicode sequence preserved; Git whitespace check passes. |
| Review patches and coverage | PASS; task-only and complete patches include new text; disposable forward/reverse application and reconstructed-content inventories verified. |
| Source/test/raw preservation | PASS; every baseline file outside changed authored Markdown remains byte-identical. |
| Authorization boundary | PASS; no staging, commit, push, external contact, game/native execution or next research task. |

Existing CRLF endings were retained in affected originals to avoid unrelated
normalization; Git's configured text conversion presents LF patch content. The
new report is UTF-8 without BOM and LF. Heading typography changes implicit
slugs; all existing in-repository references were checked, and their destinations
were preserved. External bookmarks were not inspected. No new semantic evidence
or publication clearance is asserted.

## Local review package

All diagnostics and original-byte snapshots remain ignored/local. Scripts use
existing CPython and its standard library: read Git metadata and repository text,
write only authorized documentation spaces and ignored audit/review artifacts;
no package downloads, subprocess target execution or analysis-project effects.
Failed provisional checks and corrected detector false positives are retained
in session history; final receipts control the submitted result.

- `.local-work/diffs/documentation-spacing-cleanup-task-only.diff`
- `.local-work/diffs/documentation-spacing-cleanup-complete.diff`
- `.local-work/spacing-cleanup/status.txt`
- `.local-work/spacing-cleanup/changed-manifest.json`
- `.local-work/spacing-cleanup/exclusions.json`
- `.local-work/spacing-cleanup/scope.json`
- `.local-work/spacing-cleanup/change-ledger.json`
- `.local-work/spacing-cleanup/classified-candidates.json`
- `.local-work/spacing-cleanup/validation.json`
- `.local-work/spacing-cleanup/package-checks.json`
- `.local-work/spacing-cleanup/rework-restorations.json`
- `.local-work/spacing-cleanup/rework-alias-restorations.json`
- `.local-work/spacing-cleanup/rework-offset-restorations.json`
- `.local-work/spacing-cleanup/rework-identifier-checks.json`
- `.local-work/spacing-cleanup/rework-reviewed-token-ledger.json`

The complete patch has one additional path: the unchanged user-supplied brief.
No local diagnostics, raw material or third-party legal file belongs in the
commit-ready task patch. Maintainer review remains the integration gate.

Suggested commit subject: `docs: repair prose spacing throughout research documentation`
