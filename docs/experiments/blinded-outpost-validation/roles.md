# Roles and enforced access boundary

[Report](report.md), [operator protocol](protocol.md),
[launcher source](../../../research/blinded-outpost-validation/boundary.ps1).

| Role | Permitted inputs and ownership | Prohibited access before freeze |
|---|---|---|
| Location custodian | Sole reader/owner of the newly created raw save; existing bounded readers and installed identities; private extraction receipts | May not transfer resource-bearing rows or choose a location by resources |
| Prediction runner | Provisioned allowlisted location, approved definition corpus, frozen code and runtime; writable output directory | Raw saves, extractor rows, native captures, custodian logs and revelation products |
| Revelation custodian | Retains independently acquired resource evidence and collector receipts | May not release resource-bearing bytes until independent freeze acceptance |
| Independent gate | Exact bundles, externally expected digests, clock and persistent trial registry | Must not let predictor write registry, sealed bundles, policies or custodian evidence |
| Comparator | Sealed prediction and independently authenticated post-freeze revelation | May not revise a prediction, select an alternative by truth or infer absence from incomplete acquisition |

The location custodian's newly created save remains local and protected under
the existing [save policy](../../SAVE_PROTECTION.md). A future run needs a named
human operator to own custody, source-save backup readiness, provisioning and
the independent gate. This Stage A creates no new experimental save.

## Windows mechanism and threat model

The task-owned C# launcher creates a fresh AppContainer profile with no
capabilities. It launches the provisioned Python executable suspended, checks
`TokenIsAppContainer`, exact AppContainer SID and zero capabilities, then resumes
only that disposable worker. No inherited handles are supplied. New grants give
that SID read/execute access to the copied runtime and filtered input, and
modify access to its output. Source ACLs are untouched. The profile is deleted
after completion; copied files and evidence remain for review.

The trusted host process never becomes the predictor. A previously exposed
Codex agent cannot claim personal blindness. For an authentic trial, the operator
must run the frozen worker in this independently provisioned context and keep
raw saves/logs/truth out of Codex's prediction conversation. Manual role switching
in one unrestricted agent is expressly insufficient. A dedicated offline VM or
separate account, provisioned by the operator and independently tested, is the
alternative if this host boundary cannot be qualified for the actual run.

The guarantee concerns an unprivileged worker on this Windows host. It does not
protect against a malicious administrator, a compromised Windows kernel,
dishonest custodians or resources deliberately encoded by a trusted custodian in
allowed coordinate bits/hashes. Fixed schemas eliminate ordinary extra-field
and free-text leakage; they cannot mathematically eliminate all covert channels.
The independent custodian must verify operands against their actual source.
Registry hashes provide an external witness to exact bytes; they are not digital
signatures or a trusted timestamp service.

## Provisioning and attacks

Inputs require an exact filename/hash manifest and a separately expected worker
hash. Hidden extras, nested directories, reparse inputs/ancestors and path
traversal are rejected before launch. The copied worker/input bytes are checked
again. Runtime contents are inventoried and bound in freeze dependencies. A
flat, approved installed corpus may contain resource definitions; raw saves,
generated source geometry and answer-bearing sidecars may not masquerade as
that corpus. Dataset preparation and its provenance require independent review.

The actual child attempts reads of an existing protected save and synthetic raw
save, extractor table, native capture, hidden log and revelation file; directory
listing of save/custodian/native areas; traversal; and an input write. Windows
must deny them. An unexpected accessible probe stops qualification. Missing-path
errors alone do not prove denial. The recorded token and ACL evidence accompanies
these tests. AppContainer profile creation inside Codex's own execution sandbox
failed; the authorized host-context qualification succeeded. This host-context
requirement is an operational prerequisite, not an elevation/account requirement.
