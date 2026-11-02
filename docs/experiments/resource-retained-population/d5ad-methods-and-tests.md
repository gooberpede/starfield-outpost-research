# D5AD offline methods and tests

2026-11-02, Australia/Sydney. [Original brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5AD_initialization_save_load_reconstruction.md),
[report](d5ad-report.md), [sources](d5ad-sources.csv), [review](d5ad-review.md).
All receipts, native listings and decoded save/session operands are LOCAL-ONLY.
Authored methods and this synthesis are REVIEW-REQUIRED.

## Experiment boundary

The question is whether pinned native loaders, protected Save52 bytes and the
existing B1/B2 records establish initialization provenance and a specific-load
chronology. Allowed actions are hashing, read-only static export, offline byte
decoding and owned deterministic fixtures. Inputs are the pinned build and
existing analysis database, the verified controlled Save52 copy, authenticated
historical sessions/archives and existing owned research. Outputs are fresh
ignored receipts and the reviewed authored package. There is no new game run,
attachment, instrumentation, native production change or save modification.

Risks are misattribution of historical events, decoder/alias errors, source or
database drift, accidental disclosure and local scratch growth. Stop the affected
analysis on identity mismatch, unavailable input, corrupt framing or failure of
the caller-available 40,000,000,000-byte C:/D: floor. Preserve failed attempts and
opaque bytes; do not repair originals or relabel a failed test. Cleanup removes
only method-owned temporary decoded scratch through the existing reader. Raw
originals, sealed archives and failed receipts remain retained. No arbitrary
time or event quota is imposed.

The installed CPython path/version/hash is in the local baseline receipt. The
shell's `python` application alias failed here; use that verified executable.
For the commands below, set `$D5ADPython` to its actual path. Each output must
be a new local destination. Ghidra/JDK invocation uses the pinned existing
installation, `-readOnly -noanalysis` and isolated logs/cache, with pre/post
database identity checks. No symbols, comments or types are changed.

```powershell
& $D5ADPython -X utf8 -E -B research/resource-retained-population/d5ad_baseline.py FRESH-BASELINE.json
& $D5ADPython -X utf8 -E -B research/resource-retained-population/d5ad_native_audit.py .local-work/d5ad/FRESH-NATIVE-AUDIT
& $D5ADPython -X utf8 -E -B research/resource-retained-population/d5ad_chronology.py .local-work/d5ad/FRESH-CHRONOLOGY
& $D5ADPython -X utf8 -E -B research/resource-retained-population/d5ad_save_tail.py .local-work/d5ad-save/FRESH-TAIL
& $D5ADPython -X utf8 -E -B research/resource-retained-population/d5ad_save_body.py .local-work/d5ad-save/FRESH-BODY --prefix .local-work/d5ad-save/FRESH-TAIL/prefix/save-prefix.json --esm $D5ADESM
& $D5ADPython -X utf8 -E -B research/resource-retained-population/d5ad_save_destination.py .local-work/d5ad-save/FRESH-DESTINATION --esm $D5ADESM
& $D5ADPython -X utf8 -E -B research/resource-retained-population/d5ad_readiness_control.py .local-work/d5ad-inputs/FRESH-READINESS
& $D5ADPython -X utf8 -E -B research/resource-retained-population/d5ad_save_pcm.py .local-work/d5ad-save/FRESH-PCM --esm $D5ADESM
& $D5ADPython -X utf8 -E -B research/resource-retained-population/d5ad_swap_registry.py .local-work/d5ad-save/FRESH-REGISTRY
```

The body method requires explicit `--prefix` and `--esm` inputs. Set `$D5ADESM`
to the pinned installed ESM path. Use the actual prefix-receipt location emitted
by the tail method, whose nested receipt directory is recorded in its output.
Exact policy checks are documented in the scripts. Save analysis
uses the existing streaming/framing reader under SOR-P-0002 and retains its
earlier source-informed provenance. Existing notices and external-source gates
are unchanged. No third-party implementation or dependency is newly included.

## Executed evidence and limits

| Check | Actual outcome | Evidence and limit |
|---|---|---|
| Baseline | PASS | `baseline02.json`: exact installed inputs, database roster, Save52 copy, B2/notes and interpreter pins; both drive floors pass. It is an offline selected-input audit, not a new full live preflight. |
| Native chronology windows | PASS | `native-audit05/native-audit.json`: 18 pinned function windows, 16 exact instruction sites, independent PE/RTTI definition-table binding and singleton virtual-zero-fill check. This verifies cited bytes/locations; manual control-flow and receiver analysis supplies semantics. |
| B2 full-frame/reader authentication | PASS | Fresh chronology audit decodes all 32,141 frames with fixed offsets, CRC, sequence and owned-decoder agreement, then authenticates the unchanged reader's complete session. No all-native-path coverage claim follows. |
| B2 Lodge boundary and source metadata | PASS | Prefix 876 includes 383 births/publications, zero recorded provider calls and the first reset; second triad 881/882/883 has later native QPC. The carried-empty conclusion relies on the separately audited ordinary mutator graph. |
| B1 prefix and resets | PASS | Fresh current-reader audit authenticates 19,780 frames, pinned ACK 110 and triads 2/3/4, 115/116/117. Terminal retains 9,957 losses; no complete target history is invented. |
| Chronology adverse fixtures | PASS | Nine separate mutations reject a wrong watermark, reported loss, injected precheckpoint provider, incompatible second-reset clock, unmatched source publication, invalid cold status/hazard and mismatched end receiver/epoch. Corrected-method receipts `chronology06/07` are byte-identical. `chronology08`, after a docstring correction lists B1 reads, differs only in its method SHA-256 pin. These validate the method's refusals, not actual engine scheduling. |
| Save52 prefix/tail framing | PASS | `tail01/save-tail.json`: full-stream versus independent selected-block decoding, separate struct walk, empty/nonempty positives and five malformed-input rejections. Exact type-3 payload ends at `0x18a9`. No loaded-authority claim from framing. |
| Saved-context/body discrimination | PASS | Protected-copy and installed PNDT checks identify the saved comparison context as Jemison and match all 88 descriptor body keys. Body identity in a save does not prove a Lodge provider request. |
| Separate PCM persistence | PASS | `pcm01` and promoted `pcm02-reviewed-method` consume the full 335,338-byte type-7 payload: 478 independently joined PNDT entries, 96 world entries and final 74 IDs. Separate zlib/struct checks, empty positive and malformed controls pass. Native readers/writers and consumer/revert tracing provide semantics; counts alone do not. |
| SFTR factory namespace | PASS | `registry01` and promoted `registry02-reviewed-method` resolve all 74 direct registration names, including the inline LensFlare case. Native insertion/lookup use the same interned-name registry, and its other direct aliases/shutdown do not insert. This is the qualified ordinary graph, not an unobserved live registry snapshot. |
| Promoted analytical methods | PASS | `promoted-controls02/receipt.json` verifies equal PCM state/joins and registry rows, three additional byte-derived count refusals, one wrong-export-pin refusal and five process guards (optimization, existing outputs and wrong ESM). Historical local methods remain frozen. Original PCM CRLF output and promoted UTF-8/LF output agree after line-ending normalization and as complete JSON, not as raw bytes. |
| Final preservation | PASS | `verification.json` rechecks 84 selected original/copy inputs, unchanged HEAD/index, 15 core files in each disposable project and selected tool identities. Both drive guards pass. This establishes bounded preservation, not zero original-directory housekeeping or full procedural conformance. |
| Actual complete startup/load trace | NOT TESTED by a new capture | Existing records omit constructor and loader/caller/readiness completion fields. The retained partial order is explicit; offline methods cannot add missing historical measurements. |

Early failed diagnostics are retained. The initial chronology assertion assumed
no source births before the Lodge watermark and failed; the corrected method
accepts metadata creation while still rejecting provider activity. The first
PNDT diagnostic expected a shortened editor name; installed `JemisonPlanetData`
corrected that assertion without changing its numeric identity. A direct D5Y
forensics rerun stopped at its frozen old reader hash because the current reader
has since evolved. D5AD instead authenticates B1 with the current unchanged
schema-compatible reader and independently verifies its raw frames and ACK;
it does not claim a byte-identical rerun of the old D5Y tool environment.

Ghidra logged removal of an old temporary presave file in the original project
directory despite read-only mode. Core database pins match, and no scientific
symbols, types or comments were edited; this does not mean zero directory
writes occurred. Further exports use a verified disposable copy. One intervening
original-project export failed to obtain its lock. The first disposable path
under `.local-work` was rejected because Ghidra disallows a dot-prefixed path
element; a second verified copy under the authorized tools root succeeds.
No manual cleanup or restoration of original-project files was performed.

Root later mistakenly selected the legacy launcher for export13 after announcing
the move away from the original. That run completed read-only with unchanged core
pins and no additional presave-removal log entry; its use of the original is
still a procedural deviation. Later runs select the copy-specific launcher.
Root also briefly exceeded the brief's maximum of two active sub-agents by
restarting the reviewer while both specialists were active. The reviewer was
immediately interrupted. Neither event is waived by successful scientific tests.

The six readiness-control cases execute an owned, isolated native-code page in
the Python process, without external calls or any game attachment. They test
uncontended initial/retry acquisition, completed-state return and the flagged
single-reference branch. They do not execute engine concurrency or map I/O. The actual controlled
page effects, cleanup and bounds are documented in the method and `readiness02`.
The independent definition counterexample in `definitions-check.json` contrasts
the executable's exotic multiplier default (approximately 0.01) with the main
ESM's same named GMST (approximately 0.05); it disproves substituting a compiled
default for an effective loaded value, without asserting the historical value.

The initial local native-print helper also failed at Windows default text
encoding; an explicit UTF-8 inspection helper corrected presentation without
changing an export. Database hashing initially appeared stalled and later
completed; explicit chunk hashing independently reproduced the expected large
database hash. Neither incident establishes native semantic failure.

The first final-preservation wrapper wrongly required byte equality between
chronology07 and chronology08 despite the documented script-pin change. It
refused final receipt creation. The corrected comparison requires exact bytes
for chronology06/07 and independently checks that only the owned method pin
differs in chronology08; the event results and all other fields agree.
The historical chronology source is retained by reversing only the documented
docstring correction and verifying its original frozen SHA-256. The first PCM
promotion comparison likewise refused raw-byte equality because the original
used Windows CRLF; the corrected check explicitly verifies LF-normalized bytes
and all JSON fields. Neither failure changes a native result or is silently
relabeled as a successful run.

Manual/independent editorial inspection found actual multi-encoded arrows and
range dashes in the provisional Q3 matrix. Four inspected token classes were
restored to their intended symbols; the repaired document is reviewed again.
The old lifecycle receipt remains a historical snapshot, with the final delivery
manifest binding the repaired text. The bounded screen cannot replace this read.

Repeated checks are justified only after relevant method changes or to establish
the final repeatability receipt. The final delivery manifest identifies exact
final-method runs and excludes earlier development outputs from any claim of
byte-identical repetition. Independent review must distinguish its own reruns
from receipts it only inspected.
