# LO1 provenance, methods and retained failures

[Plan](plan.md), [source pins](sources.csv), [native coverage](functions.csv),
[review](review.md). Primary receipts are machine-local under
`.local-work/lo1-locations/`; SD3 compiled receipts remain under
`.local-work/sd3-stored/`. These paths identify existing local evidence, not files
available in a clean checkout. No raw bytes are included in the tracked package.

## Baseline and identity

Starting HEAD `1210c1ff5a9501f321eb8de04a604331e84f1447`; index SHA256
`9cd26b9990214da8ab572109457445aea18f5f798218b52d37b3179b4dd1756a`.
The only starting untracked file was the supplied LO1 brief,14992 bytes,
SHA256`2691dd9d50b7787140f2d46ce4a14c2310ce0a104abba98498402cd2ace80fa8`.
It is preserved unchanged, included in complete coverage and excluded from
task-authored coverage. The original eight criteria are frozen in local
frozen-contract.md and [review](review.md); no amendments were adopted.

Baseline freshly matches **22 protected files** against SD3's retained pins:
installed EXE/ESM/Misc.ba2/development ZIP,19-input installed/analysis baseline
including 15 Ghidra project files, Interface.ba2 and both supplied screenshots.
EXE retail 1.16.244.0 SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
main ESM SHA256`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`;
Interface.ba2 SHA256`dab6aeebb7e54282818e9a1957e80baef22ae992c6363cbe910f92b8adf3e702`.
Every used native export reports the same imported EXE hash, image base 140000000,
x86:LE:64:default and Windows compiler. Object offsets are hex; physical ESM
and decompressed SWF byte offsets decimal; ABC method numbers decimal.

Supplied screenshots remain local:1716740_66.jpg,201834 bytes,
SHA256`7d29d00e1966bce47b3945d39843257f0b146fce28da4aaed864c9f9b46efc47`;
1716740_62.jpg,132080 bytes,
SHA256`14444e97c9e2a9ba761d053b049ea5643c5715b4a85e175e6c74d1b4b5bf4ccd`.
They are visual witnesses without paired saves/raw cache bits/build-time state.
No fresh save was requested, decoded or loaded. Historical corroboration is
inherited from accepted subsystem documents, not promoted to a new LO1 result.

## Reuse and effects

Existing installed Ghidra 12.1.2/Temurin 21.0.12, CPython 3.14.3/stdlib and Git are
separate tools. No package installation, download, external implementation,
contact or network operation occurred. Original project methods are adapted
under SOR-P-0002; exact immediate-source hashes are recorded in sources.csv.
Bethesda installed data and the maintainer's screenshots are credited primary
sources; existing project discoveries retain their own citations and limits.

| Method / exact local source | Reads, writes, dependencies and target effect |
|---|---|
| lo1-start.py; immediate source sd3-start.py | Hashes protected inputs/brief/index, invokes owned disk guard; writes exclusive baseline/frozen contract and hidden readOnly/noanalysis static worker. No target process. |
| native/E2ReadSession.java, Cr1Recon.java, TransitCalls.java; immediate SD3 versions | Existing project strings/xrefs/functions/instructions/decompilation only; exclusive numbered local exports. Local reader adds exact field-name selectors and full-instruction export for two long functions. No symbols/types/comments/bytes or analysis changes. |
| lo1-resume.py | Rehashes 22 protected inputs after a failed locator caused worker exit; preserves failure and restarts readOnly/noanalysis using the corrected pending request. |
| lo1-peek.py; immediate sd3-peek.py | Reads completed exports or creates exclusive numbered selector requests. Never invokes a native function. |
| lo1-defs.py; owned inspect_outpost_definitions.py/catalog.py | Complete header/group walk with bounded selected metadata types; local metadata01. All 123 STDT records retained as local reconnaissance, not a new catalogue or published raw data. |
| lo1-controls.py / lo1-controls02.py | Physically reread finite PNDT/STDT/LCTN/FACT/KYWD/DFOB controls with group/decompression closure;14 final selected records. Reads installed English string member in Localization.ba2 with pre/post hashes; writes local selected values/hashes. No save changes. |
| lo1-assets.py; immediate sd3-icon-tree.py/assets.py | Immutable SD3 Locations SWF and metadata; frame counts/labels, SymbolClass and named instance joins only. Writes assets01. No ActionScript/movie/render execution or artwork export. |
| Config locator and selected-PE receipt | Original finite RIP-relative LEA locator over installed PE .text finds initialization addresses for seven chosen globals; exact Ghidra windows distinguish real instructions. pe-selected01 records selected names/constants, not decompiled source. |
| [verify.py](../../../research/locations-outpost/verify.py) | Approved offline research verification: retained primary exports/selected installed bytes/compiled spans/metadata and authored text only; exclusive local receipt. No game, decoder, source rewrite, database or Git mutation. |
| Local package.py; immediate SD3 package.py | Authored text/HEAD/index reads; exclusive exact complete/task-only patches and isolated forward/reverse reconstruction under .local-work/review-patches. No workspace apply or staging. |

Disk guard requires caller-available C:/D: free space>=40,000,000,000 bytes before
acquisition, recovery and verification. Source/metadata/patch pins verify identity,
not semantic truth. The native register explicitly preserves instruction/decompiler
limits; a limited export is not absence evidence. New decisive long-function
instructions are completed in n027. SWF metadata and ABC are read without executing
their code. Reused E1/P1/L1/L2/CR1/R1/C1–C3/SD3/BM2 calculations were not rerun as
a prerequisite to reuse; initial n001 reconnaissance includes the inherited
cargo/cache helpers but establishes no separate new arithmetic result.

## Preserved failures and corrections

- Initial combined guidance/source reads exceeded console limits; targeted reads
  recovered the relevant policies and primary records. Broad metadata printing
  also exceeded console limits; no truncated console was used as a census oracle.
- Invalid exact function guesses produce NO_FUNCTION_AT; querying an unfinished
  export or selecting an absent function raised FileNotFoundError/StopIteration.
  These are failed locators, not missing game behavior. Functions.csv retains them.
- Request 024 used an address that was not an instruction. Cr1Recon threw, leaving
  a header-only export and ending worker 63176. Recovery01 verifies all 22 protected
  files unchanged, preserves 024.request.failed/its export, and starts worker 63832
  for corrected 025 onward. No failure was reclassified as a scientific negative.
- Controls first guessed FACT 000545df and failed the finite-record assertion.
  The corrected little-endian ID000546df was still absent from a FACT-only
  selector: it is a **KYWD**. Final acquisition includes KYWD and explicitly
  separates owner FACT 000638e5 from faction-type keyword 000546df. controls-failed01
  retains the first selected-ID failure; the second failure is retained here.
- PE-selected receipt was written successfully before printing binary bytes as
  cp1252 raised UnicodeEncodeError. JSON uses escaped text; subsequent selected
  reads recovered actual ASCII names. Binary constants are not treated as text.
- Some early Ghidra instruction exports hit the 600-instruction cap. n027 completes
  both long decisive functions; register entries distinguish the earlier partial
  exports. No absent instruction claim relies on truncation.
- Verification-first reached text validation and rejected mojibake in the frozen
  contract copied into review.md: its UTF-8 source had been read using Windows'
  default encoding. The flawed derivative and failure receipt are retained locally;
  explicit UTF-8 restores the unchanged original contract. Verification-corrected 01
  passes 252 checks, including the primary joins. Protected inputs did not change.

No game launch, attach, pause, step, hook, patch, termination, save/configuration
mutation, external disclosure, staging, commit or push is authorized or performed.
Worker outcomes, evidence completeness and scientific conclusions remain separate.
Final integrity, retirement and independent disposition are recorded in review.md.
