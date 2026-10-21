# CR2 offline evidence aids

Authority and frozen criteria: [plan](../../docs/experiments/crew-skills/plan.md).
These are finite research readers, not an importer, mod or gameplay interface.
Run from the repository root with the existing absolute CPython 3.14 executable
`C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe`.
No package installation or network is needed. Existing Ghidra12.1.2 and
Temurin21.0.12 read existing analysis only; do not import/reanalyse the EXE.

| Aid | Reads | Writes / prerequisites |
|---|---|---|
| `definitions.py` | Installed pinned main ESM through owned `inspect_outpost_definitions.esm_records` | Exclusive `.local-work/cr2-skills/definitions01.json`; all NPC/PERK/SPEL/MGEF/KYWD/AVIF records, source hash before/after and both-drive guard |
| `grants.py --output .local-work/cr2-skills/NEW.json` | Pinned Misc.ba2, quest/source-discovery receipts and owned CR1 PEX parser | Exclusive local compiled-grant receipt; never executes PEX; replay01 is byte-identical to grants-pex01 |
| `catalogue.py` | Local definition, grant, focused, robot-recipe receipts and CR1 candidate metadata | Rewrites the four authored metadata CSVs it names and creates catalogue01 receipt; preserve an existing receipt separately before explicit regeneration |
| `saved.py` | In-memory independently framed Actor4b/version 153 record and resolved queue identities | Pure return or ValueError, no I/O; deliberately supports only the documented suffix/mask branch |
| `scan_saves.py` | Seven protected original paths/pins through owned CR1 corpus receipts and streaming/typed-prefix readers | Exclusive local rank receipts, controlled ignored decoded scratch and authored saved-ranks.csv; originals hashed before/after; unsupported fields UNKNOWN |
| `verify.py --run NAME` | Protected baseline, fresh ESM record bytes, catalogue/grants/save receipts and independent retained CR1 Actor bodies | Exclusive verification-NAME.json; integrity/adversarial checks and both-drive guard; no live semantic oracle |
| `XrefContext.java` | Existing references/call instructions | Exclusive local bounded call-context export; check cancellation/remaining flags |
| `LiteralUses.java` | Existing instructions in explicit start/end static-VA range | Exclusive local literal-operand census; check coverage/cancellation; operand match is a lead, not typed identity proof |

See each Java file's argument validation. Their actual command arrays and output
pins are in the local process receipts and [source ledger](../../docs/experiments/crew-skills/sources.csv).
Use `-readOnly -noanalysis` with the existing project and explicit script path.
The owned E2ReadSession/Cr1Recon/TransitCalls orchestration accepts numbered local
request files; its stop file ends idle processing. Exact function selectors,
reference inventories and bounded instruction windows only read existing state.
The last worker exited on an invalid second instruction-window selector; its
first window and independently complete callbacks remain usable with that scope.
An export's `.done` means reader returned, not semantic verification: inspect
errors and caps as well. No game process was started or attached.

Additional focused acquisitions used the same owned ESM iterator: all LVLN plus
selected ACHR/ACTI/AVIF/GBFM records (`focused01`), crew QUST/LVLN (`quests-lists01`),
and five COBJ products identified by CNAM (`robot-recipes01`). The full NPC census
also produced noncandidate crew-flag holders and an initial ancestor-union lead.
These are local discovery receipts; native template-part selection subsequently
rejects treating that union as inherited perks. Installed development PSC source
was read from ContentResources.zip for discovery; actual ten crew quest grants
were independently decoded from shipped compiled PEX. Do not substitute unused
VMAD properties or source names for executed AddPerk operands.

Save scan order is HIST-0255, HIST-0021/22/24, HIST-0036/0077, Save52. The original
source path/pin, decoded offset domain, typed record boundary, queue references,
private mask and independent terminal grammar are retained in each local receipt.
The nine public-facing numeric rows expose no raw body. Re-running scan_saves
requires fresh exclusive receipt names; it intentionally refuses overwrite.

Owned reuse under SOR-P-0002: CR1 crew/current-prefix and PEX research; E1-E3
definition, timer and production contracts; P1 generator consumer; S1/S2 capacity,
inventory and links; C2/C3 cargo consumers; mature-corpus framing/streaming and
both-drive guard. Exact imported helpers and export hashes are in sources.csv;
no third-party implementation or new dependency was acquired. Bethesda's game
data/scripts/native code and maintainer saves remain LOCAL-ONLY. Authored
interpretation and numeric metadata are REVIEW-REQUIRED, not publication-cleared.

Local packaging adapts the owned CR1 package helper, preserving that provenance.
It reads HEAD/index and the complete changed/untracked text inventory, creates
exclusive complete/task-only diffs under `.local-work/diffs`, and applies/reverses
only in fresh `.local-work/review-patches/sor-cr2-skills-*` scratch trees. It also reverse-checks the
actual tree without applying there. It never stages, commits, changes refs or
uses the network. The supplied untracked brief belongs only to the complete
patch; task-only compares against the pinned initial untracked brief.
Raw saves/decoded bytes/native exports/databases and local receipts are excluded
with explicit path/hash inventories. Keep those exclusions when sharing a patch.
