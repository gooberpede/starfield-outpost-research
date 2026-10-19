# E1 verification and independent review package

2026-10-16, Australia/Sydney. [Brief](../../implementation-briefs/CODEX_BRIEF_SOR_E1_inorganic_extractor_native_mapping.md),
[contract](contract.md), [report](report.md). Proposed scientific disposition:
CONDITIONALLY COMPLETE. Independent disposition: **ACCEPT** after review01
remediation; no integration authority follows.

| Mandatory criterion | Result | Evidence and scope |
|---|---|---|
| Identity/inventory | PASS scoped research | definitions.md and existing 63 Save52 owner/resource/root joins; no exhaustive active-player census |
| Family/size/exception coverage | PASS scoped research | Recomputed 159-base catalog; family census 89 solid/43 gas/24 liquid/3 missing; independent MODL examples, atmospheric/liquid/X-Tech exceptions; universal numeric tier unresolved |
| Resource association | PASS scoped research | Existing controlled chain plus freshly checked CONT/AVIF/IRES/COBJ bytes; configured resource distinct from deposit geometry |
| Current power contract | PASS STATIC | Native condition and ExtraFlags 9C mask 40; no current instance result |
| Activation distinction | PASS qualified research | Separate halted keyword/group predicate and power branch identified; universal activation Boolean/UI setter unresolved, not declared nonexistent |
| Operating contract | PASS STATIC | Current reason evaluator, CanProduceForWorkshop wrappers and update recheck; eligibility not actual output |
| Outgoing targets/direction | PASS STATIC with SAVE corroboration | Native binding/add/remove/direct destination lookup and save/load; historical endpoint/control framing preserved |
| Production quantity/timing/effective dependencies | PASS qualified research | Native producer rows, elapsed/due loop, interval hours conversion, HarvesterRateMult/default binding, entry point 0xa1, recipe count and unit creation boundaries; complete effective formula and actual values unresolved |
| D1 preservation/cross-check | PASS | report.md keeps D1-H1–H4 predictions/falsifiers/dispositions and the Decaran eyewitness chronology; no new incident falsifier satisfied |
| Registry/dataflow/source inventory | PASS | Existing CSV extended N73–N94; native.md/links.md layouts; sources.csv pins |
| Offline verification/protected evidence | PASS with disclosed first-export limit | verification02.json and preservation.json; details below |
| Independent critical review | PASS / ACCEPT review02 | Reviewer independently challenged and accepted corrections to production representation, power-bit persistence wording and prose; exact snapshot pins retained locally |
| Prose/links/patch completeness | PASS | Local prose-audit.json and final package manifest supply actual checks/hashes; reviewer independently reconstructed exact patch bytes and confirmed coverage |

PASS qualified research means the reference answers with a supported inference
and names its unresolved contract; it does not turn missing runtime/current-value
tests into passes. Actual current power, activation, output quantity and elapsed
production for a chosen loaded object are NOT TESTED. No synthetic operating-state
or rate tests were invented to impersonate native measurements.

Actual verification:

- `python -B research/e1-extractors/verify.py --run verification01`: PASS,
  13,276 definition records, 159-base family census, seven then-existing native
  exports, original input hashes. Local receipt retained.
- Same command `--run verification02`: PASS, 13,278 records including two selected
  DFOBs, all eleven complete native exports and original ESM/save input hashes.
  Uses installed CPython at
  `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`; the shell
  WindowsApps alias was inaccessible. No save decoding or runtime invocation.
- `python -B -m unittest discover -s save-analysis/scripts -p test_extractor_resources.py`:
  11 existing unit tests PASS. These qualify the established association reader;
  fresh full-save corpus tests were not rerun. Prior corpus controls are cited.
- Eleven new native exports used the existing owned wrapper/reader and pinned
  Ghidra 12.1.2_PUBLIC / Temurin 21.0.12+8, readOnly/noanalysis. Exact selectors,
  tool messages and source hashes are retained locally; sources.csv lists them.

Preservation limitation and failures: the initial `python` alias failed before
the first export, and the shell continued to execute that read-only export.
An attempted concurrent all-file database hash then encountered an inaccessible
lock file. Neither failure is counted as preservation success. After export01
closed, the 15 historical database-file pins were independently rehashed and
all matched the earlier workshop-caller-db-before.json; the executable hash also
matched. This first task snapshot brackets subsequent exports, not export01.
Final equality is recorded in preservation.json. It does not supply a missing
fresh pre-export01 receipt. No database content change was observed.

Other preserved unsuccessful routes: selectors 140f7c0f0 and 140f9a000 yielded
NO_FUNCTION_AT; guessed override-interior xrefs supplied no semantic contract.
Decompiler type-propagation/jumptable warnings and 600-instruction caps are
coverage limits, not permission to trust all inferred prototypes. The specialist's
initial PowerShell family probe failed on absent KWDA and retained stale-variable
counts; a corrected census and the primary direct-byte verifier returned 159.
The local author helper first failed under the Windows default text encoding
before writes; rerun with `-X utf8` succeeded. None is scientific absence evidence.

Local outputs are under `.local-work/e1-extractors/`: input verification,
database/executable preservation, Git snapshot, package manifests, prose audit
and reviewer verbatim messages. Native exports/logs remain under `.local-work/recon/`.
Review patches use `.local-work/diffs/e1-extractors-<revision>-task-only.diff`
and `-complete.diff`. The complete patch includes the supplied previously
untracked brief, unchanged; the task-only patch excludes it. No private raw
payload, binary or executable/analysis database is bundled.

The package exporter reads HEAD/index and changed UTF-8 text, writes exclusive
local patches/manifests and disposable .local-work/review-patches apply trees. It checks forward
and reverse application against exact bytes and compares changed path inventories,
not merely reverse applicability. It adapts the maintainer-owned native-output-
contracts helper; exact input hash and reuse mode are in local provenance.json.
No staging, workspace application, branch/ref change or network access occurs.

Prose audit covers every task-authored document, register addition and verification
script. Correct joined numeric/address tokens and review readable prose manually;
regex checks are supplementary. Existing unrelated historical formatting remains.
Link checks cover task Markdown file destinations; historical missing targets
are recorded separately, not silently fixed. Anchor validation is stated in the
package's check limits. New files are UTF-8 without BOM and LF.

Outcome dimensions: positive STATIC/SAVE native-reference result with qualified
current/effective limits; verification integrity separate from native semantics;
target survival/restoration not applicable because no target process was used;
offline authority honored with the first-export receipt deviation disclosed.
No new rights-holder permission issue, incorporation, external communication,
publication, integration, staging, commit or push is authorized.

## Independent disposition and remediation

Review01 returned **REWORK**. The reviewer independently matched all 20 tree
hashes, both exact reconstructed patch streams, source inventory pins and all
16 protected hashes; inspected eleven read-only logs and decisive native
contracts; read the executable constant as binary32 3600.0; and passed whitespace.
They did not rerun definition/unit checks or decode saves. HEAD/index remained
unchanged throughout. Actual return is retained in local reviewer-review01.md.

Remediation preserves three defects: (1) decompiler types caused an erroneous
i32 countdown/interval and integer return interpretation; direct VMOVSS/VSUBSS/
VMULSS stores and XMM0 return prove binary32 instead. Corrected native layout,
rate summary, state register and N83 output; cycle-count integer conversion stays
separate. (2) ExtraFlags mask 40 persistence lacked a qualified serializer;
labelled UNCLASSIFIED in E1 while retaining current native predicate and separate
producer-byte persistence. (3) repaired two mask40 fusions and completed the
primary task-wide prose audit. The first failed prose scan remains in
prose-audit-review01-fail.json; the successful final scan is prose-audit.json.

Review02 returned **ACCEPT**, independently confirming all 20 file hashes and
changed/untracked coverage, six remediation files, both exact reconstructed patch
streams and forward/reverse applicability, source pins, whitespace and verifier
syntax. The package SHA256 is
`3aa9b7775a17b14a43dab0da96aa736a26c342a2c615db888ed80043dde9f0e3`;
HEAD/index remained unchanged. Actual return is retained in reviewer-review02.md.
The reviewer accepted all eight capabilities at the bounded CONDITIONALLY COMPLETE
native-reference endpoint, with current instance values, universal activation/tier
and complete effective arithmetic unresolved. No broader investigation or live
experiment is required. Final factual disposition recording is packaged separately
and receives snapshot confirmation; no scientific content is changed by it.
Maintainer critical review remains required.
