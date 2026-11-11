# BM1 experiment plan

2026-10-20, Australia/Sydney. Authorized by the maintainer's instruction to execute
the [BM1 brief](../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_BM1_construction_component_variants_dynamic_configuration.md`).
AC1–AC8 in that file are frozen. Interim investigation; no completion claim.

Question: distinguish manual component selection, automatic snap behavior,
assembly construction, appearance and destruction, including their saved state.
Primary case: ordinary outpost hab-wall CHANGE. Required contrasts: floors and
ceilings, airlock stairs, cargo compartments, storage appearance, damaged wall,
and bounded ship architecture.

Allowed actions: read installed ESM/executable/scripts/assets, existing static
analysis and protected historical saves; create local analysis outputs and
authored research documents. Ghidra reads existing analysis with `-readOnly
-noanalysis`. No game/native-function execution, attachment, instrumentation,
save/ESM/configuration edits, database edits, staging, commit, push or disclosure.

Inputs: freshly hashed installed executable/main ESM/development script ZIP,
existing Ghidra project and owned readers, protected historical inventory and
selected archives, four supplied screenshots. `.local-work/construction-variants/`
holds baseline, requests, exports, diagnostics and receipts. Game-derived bulk
content remains LOCAL-ONLY. Authored interpretation is REVIEW-REQUIRED.

Method: start with all physical STBH/STMP/STND records and concrete hab recipes,
resolve exact relationships, trace producers and consumers independently, then
seek positive saved replacements/connections across the wider corpus. Enumerate
the searched populations and preserve exceptions. A name is a lead; screenshots
are visual witnesses, neither execution nor persistence oracles. Compare prior
Workshop, L1–L3, DA1, SD1/SD2 and Build Mode reports without promoting them.

Competing explanations: recipe/whole-root swap; generated child replacement;
in-place model/material state; automatic condition selection; destructible state.
Discriminators: native call chains, actual STBH conditions/action records,
root/child/replacement identities, and saved restoration consumers. No new saves
or live observations are required or authorized.

Controls: complete physical record-type counts, ordinary versus variant-group
entries, ship and non-hab behaviors, known prior saved relationships, exact
input/output hashes and independent source checks. Definition-derived state must
be considered before interpreting an omitted save field.

Risk/stop/cleanup: read-only tools can consume disk/CPU. Preserve the existing
40,000,000,000-byte caller-available guard on C: and D:. Stop affected work on
failed input hash, guard or worker integrity; retain diagnostics. Stop the owned
static worker through its sentinel after exports, verify database/input/HEAD/index
hashes, and leave all originals untouched. Independent review uses the original
AC1–AC8 and actual evidence; review supplies no integration/publication authority.
