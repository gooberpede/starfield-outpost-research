# R1 bounded offline research aids

[Contract](../../docs/experiments/robots/plan.md), [report](../../docs/experiments/robots/report.md),
[source pins](../../docs/experiments/robots/sources.csv). Run from repository root
with existing `C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe -B`.
Stdlib and owned project readers only; no install/network. These are research
aids, not a production census/importer or save editor.

`acquire.py --run NEWNAME` reads pinned installed ESM, ContentResources.zip and
Misc.ba2. It walks the robot construction category and related definition types,
retains only selected robot placed-base leads rather than every REFR/ACHR, reads
source separately, and fully decodes 17 selected compiled script members as data.
It writes exclusive ignored definitions/scripts JSON under `.local-work/r1-robots`.
Input pre/post hashes and both-drive 40 GB guards apply. Final successful run:
`definitions-final.json` / `scripts-final.json`, 34,926 records. Earlier broad
acquisition and exclusive-output collision remain local disclosed history.

`scan.py` inventories 278 frozen metadata inputs first, selects 106 supported CR1
mature originals, hashes/decodes each and records typed Actor/base plus beacon
rows. `--extend` adds 32 remaining current-build mature inputs to seek the missing
robot-only category. One frozen source is missing; 137 were read. Existing
per-input receipts are reused explicitly; deleted/unsupported state is never
replaced with an absence conclusion. Temporary decoded scratch is removed by
the existing decoder. Outputs: ignored per-save body/queue receipts and authored
metadata-only corpus CSV. It never writes source saves.

`links.py` adapts owned CR1 current.py with only the already established fixed-u32
Extra9C branch before the first explicit 4C. It retains buffer 153/type/queue/body
bounds and supported zero-change nested NPC framing. It does not decode the
entire actor extra `15` tail or default/loaded state. `verify.py --run NEWNAME` independently
physically rereads 26 selected ESM records, rehashes 137 originals, checks eight
reciprocal robot/owner joins and raw queue/mode offsets, preserves the old `9C`
failure, rejects wrong versions/short queues and checks protected inputs plus
HEAD/index. Exclusive ignored receipt; no runtime semantic oracle.

`RobotFields.java` is an original bounded existing-instruction lead selector
adapted from owned Cr1Recon.java. It runs only with Ghidra readOnly/noanalysis;
no symbols/types/comments/bytes or analysis are changed. It writes a new local
TSV in three specified Workshop ranges for requested field literals, or two
NPC/template ranges for script-inheritance leads; scripts-binding additionally
covers the bounded VM policy range and NPC mask offsets fe/ff. Offset/literal matches are
leads, not typed alias proofs. Existing owned E2ReadSession/Cr1Recon/TransitCalls
under the local native directory handle exact function/data/xref exports.
Requests, source versions, commands, worker stdout and caps/errors remain local.
The task-owned offline worker restart is recorded separately from game activity.

Local `analyze.py` derives authored catalogue, exact saved joins and nonrobot
controls from pinned receipts; `document.py` writes indexes and metadata source/
function registers. The local review exporter adapts the owned CR3 package
helper: complete/task-only patches, disposable exact forward/reverse reconstruction,
text/link/whitespace checks, manifests and exclusions, without staging or applying
anything to the workspace/index. Helpers and source hashes are in the ledger.

Substantive provenance: CR1 assignment/capacity/PEX and current typed actor links;
CR2 variant/perk/template/rank/consumer research; CR3 remote storage/life-state/
load replay; E1–E3 production, P1 generation, S2 remote scheduling and Workshop
membership/population; mature streaming/framing/guard readers. Owned reuse is
authorized under SOR-P-0002. Bethesda payloads and maintainer saves remain
LOCAL-ONLY; metadata/interpretation REVIEW-REQUIRED. Existing Ghidra 12.1.2,
Temurin 21.0.12, CPython 3.14/stdlib and Git are tools. No new external code or
dependencies, live/game/save/configuration/database edits, deployment, staging,
commit, push or publication.
