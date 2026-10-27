# Operator protocol and repeat policy

**Current readiness: NO-GO for Stage B.** [Candidate gaps](report.md) and the
[draft card](stage-b-draft.md) must be resolved and independently reviewed first.
The commands below qualify offline tooling; they authorize no game operation.

1. Assign separate location, revelation and gate custodians. The operator owns
   the raw-save namespace and independent registry. Provision the prediction
   worker through the tested Windows boundary; keep truth outside its input,
   writable output and conversation. Record actual people/accounts/processes.
2. Before choosing any site, record candidate support/gaps, exact installed input
   hashes, frozen algorithms/dependencies, eligibility, selection and repeat
   policy. Choose planet/site without resources; normal player placement need
   not hit a preselected pixel or exact beacon offset. This step belongs only to
   a future independently authorized card.
3. Location custodian alone extracts the unique saved Workshop and raw operands
   using existing bounded readers. Independently verify identity/provenance and
   source-save protection. Emit only the strict allowlisted transfer. Reject
   ambiguous Workshop, missing frame/site or unknown installed inputs. Saved
   compensation does not establish the engine-effective query.
4. Verify approved input filenames/hashes and worker hash, then launch the fresh
   AppContainer. Inspect token, ACL, denied-probe and runtime-manifest evidence.
   The prediction worker reads only provisioned inputs and writes a new output.
   Keep its output immutable in the independent custodian's sealed bundle.
5. Assemble prediction, protocol, exact code and dependencies, runtime inventory,
   installed identities, corpus and all eligibility/transform/comparison/collector
   rules. Independently compute the inventory digest, validate it through the
   gate, and retain the returned freeze hash outside predictor-accessible storage.
   A current candidate `UNSUPPORTED` response is an honest engineering refusal,
   not clearance to start a trial.
6. Revelation custodian checks independent freeze acceptance before releasing
   authenticated truth. The gate reauthenticates every frozen dependency and
   refuses any change. Native positives remain positive-only. No complete native
   negative oracle is implemented in this revision.
7. Apply the fixed comparator. Preserve identities, all alternatives, exact
   contradictions, partial matches, unknowns and acquisition failures. A qualified
   mismatch is a valid scientific outcome and never an engineering failure.
   Keep accuracy outside procedural acceptance.
8. Preserve original prediction/outcome after exposure. A suspected tool defect
   compromises the affected trial when justified; retain it, obtain separate
   approval for corrected tools and use a genuinely new trial. Do not tune,
   retry, exclude or reclassify a case merely because it disagrees.

## Offline commands

Run from repository root with the existing pinned CPython executable. Choose
fresh labels; no tool overwrites an earlier trial or qualification output.

```powershell
python -B research/blinded-outpost-validation/test_toolchain.py
python -B research/blinded-outpost-validation/qualify.py --label qualificationNEW
python -B research/blinded-outpost-validation/installed.py .local-work/blinded-outpost-validation/installedNEW.json
python -B research/blinded-outpost-validation/rehearse.py --label historicalNEW
```

`qualify.py` must run in the operator's normal host context; Codex's execution
sandbox cannot create this AppContainer. It uses only temporary profiles and
task-local copies. It records commands/logs, actual token/access tests, isolated
candidate outputs, runtime and source hashes, and synthetic freeze examples.
`rehearse.py` accesses only explicitly pinned archive members through the existing
controlled lease mechanism. Historical results are not novel prospective evidence.
Raw paths and exact invocation outputs remain local-only.

`gate.py inventory --bundle BUNDLE` computes a candidate inventory; an independent
custodian must verify it against the approved contents. `freeze` additionally
requires registry, trial and independently expected inventory hash. `reveal`
requires the retained freeze hash and independently supplied truth hash. A hash
calculated by the predictor from its own altered files is not independent
authentication. [Schemas](schemas.md) define the mandatory artifact set.

## Repeats and retention

Assign a new unpredictable 128-bit trial identifier before each future trial;
retain every attempted identity, eligibility decision, refusal, compromised case
and scientific discrepancy in the independent registry. Never reuse an ID or
delete its failed freeze to obtain a second attempt. Repetition policy and any
new tool version require approval before resource exposure. Prior outcomes may
motivate a separately approved general method change, but may not enter a
supposedly unchanged frozen version as location-specific tuning. Retain source
hashes, dependencies and exact alternatives per version. No selective exclusion
or unreported post-hoc fitting is permitted.
