# D5BJ qualification and handoff

**Local bounded replay passed. Full Option C remains REWORK.** The
[original brief](../../implementation-briefs/CODEX_BRIEF_SOR_RG2_D5BJ_D5AQ_Native_Fixture_Public_Reproduction.md)
continues to govern Q1–Q5. The [reader guide](README.md) names each local tier.

## Isolated test

On 2026-11-09 AEDT, CPython 3.14.3 ran
`-I -B .local-work/d5bj/isolation.py isolated04`. The driver exported the
start HEAD with `git archive --format=zip HEAD` into a new disposable source
directory and copied in the five D5BJ entrypoints. The resulting 3,964 source
files contained no `.local-work/` or bytecode caches. The driver staged copies
of both exact candidate ZIPs in a separate sibling directory. Game inputs
were explicitly supplied from the compatible installation. Child commands
used `-I -B -X faulthandler` and an audit hook for Python reads, writes and
process/network calls. The hook did not monitor arbitrary native memory/API
operations. The narrow PE page plan, explicit imports, fixture substitutions
and before/after hashes provide separate checks.

The local receipt `.local-work/d5bj/isolated04/receipt.json` has SHA-256
`0b5d41d95cd12ecd9c9fe28acc9f057b2cd2445605ff3d1b77b436f772c12900`. It records
the exact command arguments, exit status, source and input pins and stdout and
stderr fingerprints for all 15 invocations. The driver SHA-256 is
`0b059833f42aad0e453aa88f01ff65b32998a8c449fdfb4b55e454f69310839e`.
The same baseline files, staged ZIPs, selected original receipts, index and
disposable source tree matched before and after. The final separately
measured free space was 91,082,285,056 bytes on C: and 77,579,784,192 on D:.

| Check | Result |
| --- | --- |
| Sampler | Exit 0. Both arithmetic branches match the independent atlas cell, normalized coordinates, actual masks and preimage for C1. Each also returns 14 zero and 182 three at fine Y +1. |
| Geometry and fresh process repeat | Both exit 0 and emit byte-identical summaries. Both native sampler branches determine the stage input. Mask 0 returns 74 regions/193 points and mask 3 returns 78/180. Planar point/bound comparison, complete canonical-body equality, same-mask repeat, cross-mask inequality, deep copy, separate append/allocation refusals and first-resource spatial discriminator pass. |
| Dispatch and source controls | Both exit 0. Each dispatcher order matches the deque model. Native direct and shared queue contrasts pass. Wake states 1/9/25 publish 1/0/0 pumps. The populated receiver runs the first supplied command under lock, returns unlocked at state 9 and leaves the second command pending through wake state 25. The original pump services the second command and clears to 1. The source command verifies the static LoadingCells closure and seven dispatch slots. Four corners pass all 24 permutations each. Small shift retains the source and the repeated-shift control retires at shift 38. |
| N2 | Exit 0. All 392 typed allocation IDs, density order/provider sequences, source allocation and consumed C1 descriptor join. Changed body and fine phase refuse in memory. One observed sample remains at sequence 3962. |
| Wrong EXE, ESM, BA2 | Each exits 1 with its specific SHA-256 refusal before mapping game pages. The main-file hash also protects the GMST and definition inputs. |
| Missing atlas or D5AS ZIP | Each exits 1 with a missing-file diagnostic. The substituted D5AS ZIP with altered bytes exits 1 at package identity. |
| Unsupported retail assertion argument | Exit 2 at CLI parsing. The scientific protection is the stage/event distinction in the output contracts and independent interpretation. The CLI refusal alone does not adjudicate a claim. |
| Inherited D5AS and D5BI adversarial suites | Both exit 0 with intended refusals. D5AS changes point bytes and other representation/roster inputs in memory. D5BI exercises 24 projected-event cases, including missing publication, wrong request, reader/owner transition and contrary history. |

The canonical-body digests are `bba4c877bc14d8abd3cfe36313e4cd62fd98e510dbf18441b250eacb57b942c4`
for mask 0 and `7b66c2cce4b0c4c2d52a91a41d02997f12632d0c197681fcf4f21cb87bdbf653`
for mask 3. These identify the outputs of direct in-memory comparisons.
The D5AS byte domain excludes envelope metadata and region padding. The
same-mask native repeat also compares all 24 captured header bytes, in
addition to the canonical 21-byte header prefix.

## Mandatory criteria

This table gives the implementer disposition against the full brief.
The separately retained independent return governs any acceptance.

| ID | Result | Basis |
| --- | --- | --- |
| AC01 | NOT TESTED to full acceptance | Applied reading is recorded in [reading](reading.md). Remaining original-only preparation and full exact coverage need separate qualification. |
| AC02 | PASS within recorded operations | Start snapshot, authorized specialist sequence, bounded hosts and exact selected preservation receipt. |
| AC03 | FAIL for entire exact fixture | Tested reader route exists for native numeric, geometry and named controls. Portable seeded selection, complete preparation/receiver qualifications and public asset routes remain incomplete. |
| AC04 | PASS for advertised native computations | Original instructions run from exact reader files in separate private processes. Substitutions and checked outputs are in [dependencies](dependencies.md). |
| AC05 | PASS at C1 numeric and projected typed tiers | Both arithmetic branches and the exact 196-row atlas comparisons, phase control, wrong body and descriptor refusals, typed N2 join and actual sample all pass. |
| AC06 | PASS at fixed ordinary geometry stage | Complete comparison against D5AS in two fresh processes, independent planar check and exact repeated mask-3 comparison. Main-file and supplied-family scope apply. |
| AC07 | FAIL for full continuation reproduction | The bounded execution and static placement checks pass. The populated service fixture uses supplied commands. The actual rectangle-preparation producer, component initialization and the full source-to-protected-miss composition retain original qualifications. |
| AC08 | PASS at staged local evidence tier | Uses existing D5AS and D5BI bytes and verifiers, with release/rights/hosting status explicit. |
| AC09 | FAIL for full reproduction | Isolated source export and explicit staged inputs pass for the named methods. Full exact fixture and hosted-input execution remain pending. |
| AC10 | FAIL for full exact contract | The named malformed and changed-input tests and inherited semantic controls pass. The nonempty preparation and complete original-path adversarial replay remain untested. |
| AC11 | PASS for authored checkpoint | Public reader policy and D5BG/run-card holds are explicit. The historical records and other claim statuses are preserved. |
| AC12 | See independent disposition | The independent read-only return and exact patch manifest are retained under `.local-work/d5bj/`. |

The decisive remaining experiment is an offline port that derives the
required main-file component and preparation inputs and challenges the
nonempty preparation/service edge with the original receiver and same-pool
constraints. The [continuation audit](continuations.md) records exact
counterexamples and historical dependencies. This is open engineering work.
Separate rights and hosting gates apply to the staged evidence copies.

The local delivery under `.local-work/d5bj/` records changed files, paths
excluded from the patches, checks and independent disposition. Both unified
diffs are in `.local-work/diffs/`. Only the complete patch includes the
supplied brief. The D5BG verifier and four graph refusal controls pass.
