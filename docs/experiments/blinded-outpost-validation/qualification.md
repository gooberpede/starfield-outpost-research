# Qualification, preservation and reproducibility

[Report and AC matrix](report.md), [schemas](schemas.md), [review](review.md).
All primary outputs are under the ignored task directory
`.local-work/blinded-outpost-validation/`; literal hashes are in the delivery
manifest and source ledger. Original raw evidence is not included in review diffs.

## Actual checks and limits

| Check | Evidence | Scope |
|---|---|---|
| Original authority | `start.json` | Starting HEAD/index, both-drive free space and unchanged original brief/contract SHA-256 |
| Installed identities | `installed01.json` | Fresh EXE/ESM/PlanetData byte hashes and candidate PNDT identities; main-file identity does not establish runtime plugin overrides |
| Strict active preservation | `audit.py` failure and `remaining-before.json` | Strict namespace FAIL retained; diagnostic authenticates all 93,334 scientific expectations with 91,933 archived matches and 1,401 loose hashes, plus 12,974 protected-policy rows and zero protected changes |
| Current tests | `qualification06/tests-stderr.txt`, `comparator-delta01/stderr.txt` | 26 tests in full Windows qualification, then 27 tests after the independently requested partial-admission correction; schemas, binary32, alternatives, truth/journal guards and code/runtime/gate tampering |
| Windows isolation | `qualification06-probes/boundary.json`, `output/probe.json` | Actual AppContainer token/SID, zero capabilities, no inherited handles and 12 denied access attempts; exact ACL/runtime inventories retained locally |
| Provisioning attacks | `qualification06/` command logs | Hidden extra inputs, junction input and worker-file junction ancestor rejected before launch; existing source ACLs unchanged |
| Candidate determinism | `qualification06/summary.json` | Two separate Windows worker runs per body, byte-identical within each body; all are explicit unsupported results, not resource predictions |
| Precommit/revelation | `qualification06/` synthetic registries | Both a deliberately wrong sealed prediction and a different winning alternative remain COMPARABLE; original predictions/tools are retained |
| Historical source replay | `historical06/prediction.json`, `prediction-freeze.json` | Deterministic source-context alternatives using unchanged geometry; researcher already knew the case, so this is not a blinded prospective trial |
| Native receipt controls | `historical06/summary.json` | Ten frozen control receipts independently checked by hash/framing; no claim to rerun all ten full geometry comparisons |
| Positive native rehearsal | `historical06/positive-truth.json`, `comparison.json` | Three source/Workshop-bound positive chains from the authenticated full historical journal and five independently framed/ACK-checked primary receipts; complete native census remains false |
| Saved-location rehearsal | `historical06/saved-controls.json` | Four Save25/Save26 extracted-input controls through unchanged saved-position reconstruction and filtered bridge; effective query remains UNKNOWN |
| Delivery checks | Exact review package | Whitespace, links, source syntax, bounded screen, manual complete prose review, complete/task-only patch reconstruction and HEAD/index/brief equality; final disposition in review |

The native selected positives reproduce their existing conditional mask-3
correspondence under the fixed partial comparator. This is useful positive
evidence, not a sampled construction mask or a complete negative. The comparator
also preserves the mask-0 discrepancy. The result is never an acceptance
threshold; synthetic mismatches receive the same procedural treatment.

The child symlink escape attempt is denied by Windows. Creating a host-side
symbolic-link fixture without administrator privilege was also refused. No
elevation or Developer Mode change was requested. The independently created
junction and worker-ancestor tests exercise the shared reparse rejection; a
successful externally created symbolic-link traversal is not claimed tested.

## Preserved failures and corrections

- Early copied-runtime preparation expected `_struct.pyd`; this CPython builds
  that module in. The copy list was corrected. An initially incomplete stdlib
  lacked `linecache`; the provisioner now copies the existing stdlib while
  excluding external site-packages.
- AppContainer profile/launch calls failed inside Codex's execution sandbox.
  SID string marshaling was corrected; an explored restricted-token route also
  failed there and was removed. Actual host-context AppContainer qualification
  then succeeded without elevation. The retained smoke directories are diagnostics.
- `qualification01` asserted Win32 error 5 for every denied CRT file read. Those
  reads return `PermissionError`/errno 13 with no Win32 field; directory listing
  reports error 5. The assertion was corrected without changing access policy.
- `qualification02` failed to create its junction because PowerShell `-Command`
  did not populate the intended argument array. A task-owned parameterized script
  corrected that fixture. `qualification03` passed the earlier boundary/tests.
- `historical01` stopped on an incorrect `Store.restore` keyword before restoring
  payloads. `historical02` restored 23 selected members but then hit a Python
  module-path collision. `historical03` corrected import precedence, authenticated
  the full historical journal and completed rehearsal. `historical04` reuses that
  exact verified lease rather than repeating restoration.
- Preliminary independent review found missing native-census refusal and
  worker/runtime/transitive-dependency enforcement. Both were corrected. It also
  found omitted full-journal/ACK-order guards and an ad hoc partial comparison.
  The reducer now consumes authenticated full journal bytes with ordered actual
  ACKs; the fixed comparator reports positive partial matches. Negative tests
  cover missing/early/duplicate ACKs and intervening phase/loss/exception/thread
  end/competing updater events. Earlier outputs remain preserved.
- `qualification04` passed after these changes. Subsequent inspection corrected
  file-ancestor reparse validation and added the dedicated ancestor/symlink
  attacks plus start/end source-equality receipts. `qualification05` passed those
  changes. Further review required truth-region/presence consistency and nonempty
  accepted regions; these are now enforced and tested. Integer saved-frame types
  and unsupported nonzero rarity-6 generation are rejected explicitly. Invariance
  accounts for weights as well as paths. `qualification06` is the final Windows
  qualification; `historical05` reruns the affected fixed partial comparison
  against the unchanged authenticated lease. No prior verdict is overwritten.
- Candidate02 independent review returned REWORK for AC6: partial geometry
  inclusion did not compare actual positive admission against each alternative's
  predicted admission set. `comparator-delta01` adds and tests that comparison,
  including matching geometry with modeled admission rejection. Unobserved
  resources remain UNKNOWN. `historical06` repeats the fixed comparator against
  the same authenticated lease. The Windows boundary/worker/location/generator
  and native reducer bytes are unchanged from qualification06; only comparator
  and its tests change. Earlier synthetic predictions and outcomes are retained.
- Candidate01 review export rejected its final working-tree equality check when
  the source ledger changed during that draft export. Candidate02 regenerated
  both patches and passed exact inventory/application/source equality. No
  rejected package is presented as the final reviewed snapshot.

## Preservation boundary and dependencies

The unchanged strict active verifier detects four previously acknowledged,
externally removed excluded observer ZIPs under
`continuous-beacon-preview/builds/qualification-03` through `qualification-06`.
The historical pin roster itself has no missing/changed scientific row. The
adapted D5H diagnostic method preserves the strict FAIL while independently
authenticating archive/index/baseline/journal and current protected/save contents.
It changes no verifier, expected identity, archive or policy. No missing ZIP is
restored and no obsolete loose-pin audit is reinstated.

Routine controlled archive access supplies two disposable leases under
`.local-work/resources-evidence-consolidation/`: `d5k-historical02-lease` and
`d5k-historical03-lease`. They contain explicitly selected historical members,
not new archives. Their manifests/digests are retained locally and their exact
bytes are checked after reading. No original, archive or historical output is
deleted. Task-only exported diffs exclude all restored/raw/native/runtime data.

The source ledger pins owned method reuse under SOR-P-0002, starting revision,
Bethesda input identities and the relevant prior scientific contracts. There is
no newly incorporated outside code, dependency download, licence acceptance,
external contact or disclosure. Copied CPython runtime/licence files are existing
local execution dependencies and remain ignored/local-only; no redistribution is
proposed. Source dependency inventories bind exact bytes rather than inferred
version labels. Postflight repeats the scoped diagnostic without converting the
strict namespace failure into PASS.
