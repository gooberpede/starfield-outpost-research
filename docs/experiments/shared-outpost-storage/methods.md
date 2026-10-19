# SD2 methods and evidence locators

[Plan](plan.md). Raw evidence and disposable helpers live under ignored
`.local-work/sd2-shared/` and `.local-work/sd2-*.py`. They remain LOCAL-ONLY.
Authored conclusions and numeric registers require maintainer review.

Native addresses are preferred static hexadecimal VAs, base `140000000`;
subtract that base for RVA. Object offsets are hexadecimal. Save offsets are
decimal decoded-stream offsets. File/plugin-local FormIDs, saved identities,
runtime handles and pointers are separate domains.

`nNNN` means `native/NNN.request.tsv` beneath the local evidence root. Every
export identifies EXE SHA-256/base/language. Existing RTTI/symbols are analysis
inputs; semantic aliases are analyst interpretations, never safe callable APIs.
Ordinary exports cap instruction lists at 600 and decompiled text at 50,000
characters; use full exports or exact windows for consequential omitted spans.
Search/symbol/xref caps are reconnaissance limits, not scientific absence tests.

Fresh baseline.json verifies 19 protected SD1 inputs including installed EXE,
main ESM, development ZIP, Misc.ba2 and existing Ghidra database files. It pins
HEAD/index and the supplied untracked brief. Separate new inputs receive fresh
pins. No game or script/native function is invoked. Existing CPython 3.14 and
stdlib, Ghidra 12.1.2/Temurin 21.0.12 and Git are used offline. No downloads,
new dependency, outside implementation, account action or disclosure.

| Disposable helper | Reads and writes / effect | Provenance |
|---|---|---|
| sd2-start.py | Hash protected inputs; new baseline/process receipts, hidden readOnly/noanalysis worker and isolated cache/logs | Adapted owned SD1 launcher under SOR-P-0002 |
| sd2-more.py | Exclusive numbered requests or console-only exported-function selections | Owned sd1-more.py adaptation |
| sd2-defs.py | Installed add-on physical records and pinned main index; physically reread selected main records; definitions01.json | Original selector; owned catalog/ESM framing |
| sd2-context.py | Installed dependency records, development PSC members, main/add-on BA2 PEX parses; exclusive local receipts | Owned ESM/DA1 PEX framing, original selection |
| sd2-survey.py | Canonical historical originals, fresh pre/post hashes, strict temporary decode and inline-base/extra/inventory search; per-save receipts and corpus01.json | Owned SD1/S1/CR1 typed framing; new special-base selector |
| sd2-resume.py / sd2-resume03.py | Protected rehashes; restart only failed offline worker with new logs; preserve failed requests and explicit failure markers | Original recovery, same read-only authority |
| sd2-joins.py | Fresh H18/H36/H257 original reads and positive owner/base joins, player-body capture; joins01.json | Owned typed framing/extra readers, original selector |
| sd2-player-candidates.py | Frozen player bodies only; diagnostic empty-stack-extra subgrammar candidates; no field-identity claim | Original bounded scan, owned compact-count reader |
| sd2-controls.py | Fresh main-ESM physical controls and default binding; controls01/02.json | Owned S1 physical reread, original selection |
| sd2-tables.py | Completed local receipts, helper/source hashes; authored corpus/source/function CSV | Original metadata-only register writer |
| sd2-verify.py | Protected inputs/originals, native identity and saved joins, source-class controls and authored text; exclusive verification receipt | Original scoped checker; not gameplay oracle |
| sd2-retire.py | Completed requests and owned process receipt; writes local stop sentinel and waits at most ten seconds per poll | Original normal offline-worker retirement; no process signal |
| sd2-shared/package.py | HEAD/index, tracked changes and untracked authored text; exact complete/task-only patches and isolated forward/reverse reconstruction | Owned SD1/CR1 exporter adaptation; scratch under `.local-work/review-patches/` |
| native/Cr1Recon.java | Existing strings/xrefs/functions/instructions; exclusive exports; whole-image literal +1008 operand census | Owned SD1 reader with task-specific selector; no symbols/types/comments/analysis changed |

Save decoder context managers remove temporary decoded scratch on completion or
exceptions. Originals remain immutable. Broad survey capability failures retain
their exception and source pin; they cannot support an absence claim. Both-drive
free-space guards use the existing 40,000,000,000-byte requirement. There is no
new scientific session deadline or sample cutoff.

## Preserved failures

The initial definition pass passed None to an ESM reader requiring a membership
predicate, causing TypeError before any receipt or source write. AllTags supplied
the intended physical-record census; successful definitions01 is separate.

Request n003 contained a blank selector rather than a zero-selector file. The
reader's null address caused NullPointerException, terminating only the offline
session. stdout.log/session01.log and partial n003 remain retained. Its explicit
failure marker says failed; the exception's actual type is NPE (the first
recovery marker mistakenly names InvalidInputException). Protected pins passed
before recovery. No absent-function conclusion uses this failure.

An attempted shell Python edit for the +1008 census failed with a quoting
SyntaxError. Request n015 raced that failed edit and reached an unsupported
selector, causing the same null-address NPE. stdout02/session02 and partial
n015 remain retained. The Java selector was then added with apply_patch and
resubmitted as n016 after a protected rehash and new read-only session. These
are acquisition failures, not semantic negatives or protected-input changes.

The first chest selector guessed a substring absent from the actual editor ID
and raised StopIteration before writing a receipt. The corrected selector used
SD1's classified CONT with capacity 150; controls01 retains its successful
result. controls02 broadens the cargo substring to cover actual installed names.
One context-mismatched apply_patch failed atomically before the corrected edit.
Early guessed native interior addresses return NO_FUNCTION_AT; these are failed
locators, not absence findings. The scratch-reference draft initially identified
player+1000 with the per-menu aggregate; the argument-owned allocation in n007
does not establish that identity. The corrected report preserves them separately.
