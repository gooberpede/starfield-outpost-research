# Static-Analysis Scripts

SOR-EXP-0015 extends `OutpostRecon.java` with `refall:VA` existing-reference export, cap4096; ordinary `ref:` retains24 cap. Reads existing state, creates no references/types/comments, reports cap overflow. [Report/ledger](../../docs/experiments/exact-beacon-planetary-coordinates.md). Continue readOnly/noanalysis, quoted PowerShell addresses, new local export filename; full native text LOCAL-ONLY.


EXP0002A adds `saves`, a bounded scan of existing defined strings for savegame/saveload/manualsave/quicksave/deletesave/save game/saving game/savecomplete. It uses the existing 350-string/eight-reference caps and never creates analysis. Selected exports, failed attempts and database preservation are indexed in [SOR-EV-0005](../../docs/experiments/evidence/exp0002a-static/README.md).

Add only authorized project-authored or explicitly permission-cleared work. Every script documents prerequisites, inputs/outputs, effects and validation; preserve provenance and credit.

## Initial reconnaissance helpers

`OutpostRecon.java` is original project code using Ghidra 12.1.2 APIs (SOR-S-0105). It reads existing program metadata/defined strings/references/instructions and selected decompilations. No symbol, function, type, comment, byte or analysis writes. No network or runtime-process access. Outputs are game-derived, LOCAL-ONLY.

`Invoke-OutpostRecon.ps1` documents the local pinned project/JDK paths and reads installed `launch.properties` VM arguments, invoking the installed Ghidra launcher class with `-process -readOnly -noanalysis`. It redirects cache/settings/logs to `.local-work/recon/`. No dependency installation/download. The normal batch launcher failed on a user-preference write; this wrapper avoids changing global settings. Adapt paths explicitly for another workstation. Existing Ghidra imports must already be analyzed and available; stop on lock/hash mismatch or export error. Before/after hash database files separately. Read-only flags alone are not preservation proof.

Examples (repository root):

```powershell
./ghidra/scripts/Invoke-OutpostRecon.ps1 -Target Starfield -OutputName new-interfaces.tsv -Addresses interfaces
./ghidra/scripts/Invoke-OutpostRecon.ps1 -Target Starfield -OutputName new-membership.tsv -Addresses 142073cf0,140517d60
```

No Addresses means a vocabulary scan; `interfaces` narrows it to API/RTTI leads. Limits: 350 matched strings, 8 xrefs each; caps are marked. Up to 12 explicit function addresses or `ref:<static-address>` queries; functions export at most 600 instructions and 50,000 decompiler characters with 30-second timeout, with truncation markers. Missing function definitions yield at most 40 existing instructions until branch/terminal; no function is created. Explicit reference queries cap at 24. These are bounded discovery aids, not exhaustive maps. Decompilation is interpretation and cannot substitute for instruction evidence.

Exports are UTF-8 text with tagged rows and free-form decompilation sections (despite `.tsv` suffix, function exports are not rectangular tables). Metadata includes imported SHA-256, preferred base and language/compiler. `CREATE_NEW` prevents overwriting; failed/partial files remain local and must be labelled failures. The PowerShell wrapper checks process exit and file presence, not semantic completeness; inspect markers/logs. No automatic cleanup of evidence. These tools were compiled/run under the authorized brief; no live compatibility or general-purpose exporter guarantee.

EXP0002 adds `exp0002` for exact relevant API strings and `win:<static-address>` for 12 previous / 45 forward existing instructions. Missing center instructions fail; no disassembly or database editing occurs. Quote address strings, particularly hex values containing `e`, to prevent PowerShell numeric/scientific conversion. One partial export demonstrated this risk; corrected exports are indexed separately. The wrapper still requires log inspection because Ghidra can report script failure with process exit 0.


## Membership offset search

[OutpostMembershipRefs.java](OutpostMembershipRefs.java) reads existing instructions only in preferred-VA range `[0x140001000,0x143400000)`, selecting exact non-stack memory operand offset `0x298`, with1000-match and cancellation markers. Writes one exclusive ignored TSV; no disassembly, analysis, symbols/types/comments or project edits. Use the wrapper's `-Reader OutpostMembershipRefs.java` with `-Target Starfield -OutputName <fresh.tsv>`; readOnly/noanalysis is retained. Matching offsets can belong to unrelated structures and are not semantic proof. [SOR-EXP-0010](../../docs/experiments/active-outpost-membership-completion.md) records actual scans, failures and preservation.

## Surface-placement vocabulary — SOR-EXP-0013

`OutpostRecon.java` adds optional `surface` vocabulary selection for latitude/longitude, landing, planetary, worldspace-overlay and unique-pattern-placement strings. It retains existing 350-string/8-xref bounds, exact-query behavior and readOnly/noanalysis execution. `full:<static-address>` uses the existing 250,000-character decompiler allowance; instruction export still caps at600. [Surface-anchor report/evidence](../../docs/experiments/planetary-surface-anchor/README.md) records 15 actual export hashes, capped/failed probes and complete database preservation. No third-party implementation, symbols/types/comments, game or source modifications.
