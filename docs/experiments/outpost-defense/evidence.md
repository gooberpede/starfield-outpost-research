# DA1 evidence and reproduction record

SOR-EXP-0054 / SOR-EV-0062, 2026-10-19. [Plan](plan.md), [review](review.md),
[methods/checker](../../../research/outpost-defense/README.md).

## Input and address provenance

The fresh baseline rehashes the prior protected installed files and existing
Ghidra persistent input state before acquisition. Retail EXE 1.16.244.0 SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`;
main ESM SHA256
`1dabed00c3f4282dd3bb54d2e9601e40b577d8742d078b7ccef203adbfef0da7`.
Each native export independently reports that EXE hash, image base 140000000,
x86:LE:64/default and windows compiler specification. The reader runs the existing
analysis with **readOnly/noanalysis**, with local settings/cache and hidden JVM.
No symbols, types, comments, bytes or analysis state are edited.

[sources.csv](sources.csv) records byte counts/hashes and repository-relative local
locators. [functions.csv](functions.csv) gives VA/RVA and exact raw export hashes;
[definitions.csv](definitions.csv) supplies FormID/type/editor ID and original
physical ESM record offsets; [scripts.csv](scripts.csv) pins uncompressed shipped
members and original BA2 offsets. The physical ESM checker rereads fields at
those offsets; a metadata name search alone is not a causal check.

The screenshot is the user's local `1716740_65.jpg`. Its source epoch/build and
exact saved extractor are unmatched. The installed UI witness is separately
pinned Interface.ba2 -> **interface/workshopmenu.swf**, 100737 bytes, SHA256
`7f190c6753619b1646a1d3e360712ba93a653ef87f629d57501302fc714a5757`.
The retained L2/C1 owned ABC reader closes all 1527 method bodies; DA1 inspects
methods 1429 and 65. These assets/compiled payloads stay local.

## Decisive locator map

Raw receipts are rooted at `.local-work/da1-defense/` unless named otherwise.

| Claim | Exact primary locator | Independent check / coverage limit |
|---|---|---|
| Timer arming, constants, one-shot callback | scripts04.json: OutpostBeaconScript variables; OnLoad byte3457, StartAttackTimer2770/2791, OnTimer2709; complete OnWorkshopObjectPlaced/OnUnload functions | Installed beacon VMAD binds SQ_Parent; complete call-site inventory, no timer rearm in OnTimer |
| Planet/cooldown/formula/event selection | SQ_ParentScript.CheckForAttack instructions43725..45106, named variable constants; development PSC lines 1264..1398 | Fully closed PEX, installed two AV bindings and111-entry MB_Parent resource configuration |
| Special condition/chance/event | vmad01.json SQ_Parent property5206..5335; physical CNDF002baa4b; SMQN00349ca0 and quest00349c9c | Quest repeats condition on event ref; CountsAsAttack property713..732 false; installed stage50 fragment calls StartAttack(false) |
| Selected beacon -> real quest/spawning | QUST00341fcd alias231 ALFE/ALFD, alias232 ALCO/ALCA, LandingLocation CTDA; attached VMAD ship/spawn/human scripts | PEX LandShip, InitialGroupSpawn/Spawn, SpawnGroupReference and SpawnEvent; packages00346853/00361c0f |
| Explicit destruction after unload | SQ_OutpostAttackHumansScript remote OnUnload: started/alive, GetDestructibleOutpostObjects, Is3DLoaded(false), SetDestroyed | Complete base/creature control functions lack human-only override; native SetDestroyed tail jump n007 |
| Actual native target membership/filter | n005141fe1740 and n0061420c02b0; linked keyword global145f0b3d8 | Both actual collectors use reverse linked members and flag24 set/23 clear; actor process/beacon gates n004141fc53a0 |
| Integrity native/provider/movie | n00214158cf50; n00814158a6e0 division/value lane; n032140d96b20 Health registration; L2 menu01.json methods 1429/65 | REFR AV vtable and getters n026/027; native versus movie clamp distinguished |
| Nonactor maximum Health | n030140b82b40 instructions140b82c03..c67; n031's completed1405bf6d0 export identifies component, duplicated source-locator context in source ledger | DEST physical fields; decompiler does not correctly express all XMM return values, so actual instructions control the float interpretation |
| Damage/destruction/Health | n03214206b1b0/14206b300; n034142065260; n0361418be6e0; n033140b56c50; n0351405c02a0; n0371405c0530 lines 202..259,347..348,422..426; n0381405bfe60 | Modifier storage n028140b6d4d0; direct SetDestroyed/IsDestroyed n007 and n009140b73230; no general weapon balance claim |
| Ordinary repair and no material charge | n0171421e3f50; n0141421e9b50; n019 HUD/build wrappers; n011140f36310; n0121405c42d0 | Complete ordinary action/service branches inspected; direct Repair binding n007/n009 is a separate entry with fewer UI checks |
| Save BF persistence | n01814051ea30 case BF and140521620 case BF; n020/0211419aec20/1419aeff0 | Fresh framed saved values and independent literal float reread; no reconstructed attack writer |
| Turret intervening E6 grammar | n018 writer case E6 and loader dispatch; n020140554bd0 | u32 count +five wire bytes per entry, no queued refs; two actual first4C joins, owner beacon and independent CB members |
| Form-flag reload | n0251405dfa40, reference merge maskd12960 includes00800000 | Native load mapping, not a new runtime load or saved destroyed-positive example |

Instruction listings have a 600-instruction export cap; full selected
decompilations use a 250000-character cap and report warnings. Large generic
dispatchers have decompiler type/indirect-jump warnings. The decisive script,
field, branch and instruction operands are checked individually; no claim of
complete disassembly follows from a decompiled listing or hash. The sole failed
native request031 is excluded as a completed multi-selector request; its
already completed component-registration function is separately identifiable,
and no failed window is semantic evidence.

## Preserved failures and corrections

- Initial combined guidance reads exceeded output budgets. Focused guidance,
  contract, reviewer, prior subsystem and locator reads followed. Several guessed
  file paths/rg wildcards were invalid. They are locator failures, not absence.
- Inherited CR1 PEX grammar mis-sized struct-set opcode 39. Correcting to three
  operands closed Armillary/OE ships; SQ_Parent then reached unsupported
  try-lock opcode 50. Its result-plus-counted-operands shape and corrected
  array-matching opcode 47 shape (six operands) close all 38 selected shipped
  members. scripts01/02/03.json and failed members retain the actual failures;
  scripts04.json is the accepted complete acquisition. No installed PEX was edited.
- New local VMAD reader initially rejected type 7 struct. Corrected handling of
  type 17 arrays of type 7 structs closes the selected script property prefixes;
  quest fragment/alias extensions are explicitly outside its prefix decoder.
- Native request031 asked for a guessed window center that was not an existing
  instruction. Ghidra retired that reader with a script error; the failed request,
  partial text and logs remain. The owned reader restarted readOnly/noanalysis,
  skipped the failed request with an explicit FAILED receipt and completed later
  exports. Existing instruction evidence at 140b82c03 onward supplied the needed
  Health operands. No database analysis or symbol creation was used to repair it.
- Initial author tables used guessed large-extractor base IDs. Actual saved-base
  rereads corrected Water to 0020a090, He-3 to 0020a084 and Antimony to 0020a052
  before review. The exact generated definitions ledger is the independent check.
- A documentation edit used Windows default cp1252 decoding: it rewrote one
  authored file with mojibake, then failed reading the next. The package text
  validator rejected the first export before patch creation. The malformed copy
  is retained locally; reversing that encoding conversion restored UTF-8. All
  subsequent authored reads are explicit UTF-8. No raw source was normalized.
- Some asynchronous export reads occurred before completion. Later .done and
  log/closure checks control acceptance; partial/missing output is not a PASS.

## Provenance and rights

Bethesda installed native/definition/compiled/development-script and UI material
provides primary evidence. Maintainer saves, screenshot and previous project
Workshop membership, E1–E3/P1/S1–S2/CR1–CR3/R1/L1–L3 discoveries supply concrete
dependencies and owned research methods. Reuse/adaptation falls under SOR-P-0002;
exact method hashes are in sources.csv. Existing Ghidra 12.1.2, Temurin 21.0.12,
CPython 3.14/stdlib and Git support read-only analysis/checking. No new outside
implementation, package, download, web consultation, contact or disclosure was
used. Bethesda/game-derived bytes are not copied into patches; numerical/hash
metadata and authored interpretations remain REVIEW-REQUIRED. No permission
for publication, staging, commit or push is inferred.
