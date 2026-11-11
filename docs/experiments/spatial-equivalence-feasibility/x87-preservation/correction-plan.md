# One authorized preservation correction

2026-10-16, Australia/Sydney. SOR-EXP-0034 / SOR-EV-0042 continuation.
Recorded after `diagnostic-03` and before implementing the correction.
[Governing brief](../../../implementation-briefs/README.md#archive-lookup) (`implementation-briefs.zip :: docs/implementation-briefs/CODEX_BRIEF_SOR_experiment_A_x87_state_preservation.md`).

The qualified pre-trap duplicate FXSAVE64 images agree. Both full-width pointers
are nonzero above 4 GiB. All required x87 fields still agree at the first assembly
VEH entry. In 99 minimal and 1,111 adversarial records, the Windows FltSave image
contains only the low pointer words and the post-continuation FXSAVE64 also has
only those low words. The six unpatched controls per process agree throughout.
See local `diagnostic-03/{minimal,adversarial}/comparison.json` for every field
and file offset; `states.bin` preserves the original representations.

Hypothesis: ordinary exception-context continuation restores a representation
that lacks the high pointer words, despite those words remaining recoverable
at first VEH entry. The exact Windows instruction responsible is unobserved;
no kernel/dispatcher attribution is claimed. Context representation diverges
before this handler's manipulation; architectural loss is bounded between the
entry capture and controlled continuation boundary.

Implement exactly one correction: capture full-width x87 pointers at assembly
handler entry, merge those 16 bytes into an invocation-owned copy of the Windows
FltSave image, and execute FXSAVE64's matching FXRSTOR64 in the leaf continuation
before the displaced MOV or ADD. Leave the supplied CONTEXT unchanged except
for the existing RIP selection. Use its XMM/MXCSR and other x87 fields, whose
equivalence is checked independently; retain all original context bytes in the
evidence. The existing fixture's R15 snapshot carrier owns this restore image.
Nested probes have separate carriers. This is fixture storage, not a proposed
retail register convention or evidence of native storage lifetime.

Prediction: raw CONTEXT still differs in full FIP/FDP, while the corrected
post-continuation FXSAVE64 agrees exactly in every required x87 field. GPR,
flags, XMM/YMM and MXCSR controls remain unchanged. Re-run minimal and adversarial
conditions, nested/interrupted sequences, four-thread stress, STOP/quiescence,
both decision continuations, geometry correspondence and malformed decoder tests.
If that one correction fails the preservation contract, return NO-GO; no second
preservation strategy or alternate breakpoint mechanism is authorized.

The diagnostic buffer sizing fix and explicit signed fixture-exit detection
repair the measurement harness; neither is a preservation correction. Failed
`diagnostic-01` remains local, including its truncated adversarial coverage.
