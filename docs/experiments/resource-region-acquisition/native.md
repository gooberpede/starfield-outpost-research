# Safety qualification and native engineering boundaries

[C1 native contract](../resource-geometry-observation/native-contract.md) is the
unchanged rich-capture specification; this document prioritizes smaller routes.
All addresses here are **preferred static VAs**, retail 1.16.244.0, image base
`0x140000000`, EXE SHA256
`7e9adb1414a8e1b325e5e1f097b9b17b78deb7eebeda37a333351a43a60f9d28`.
Runtime base must be measured later; save tokens are never VAs. No new layout.

## Architectures evaluated

| Architecture | Concrete feasibility decision |
|---|---|
| External debugger at area callback terminal | Maps current region at `1421e1060`, rejects `1421e174e`, accepts `1421e1772`; callback EAX=1 is not region acceptance. Could expose exact per-use state but suspension, exceptions and queued owned traps outliving detach were actual historical failures. NO-GO for reuse. A different debugger design needs explicit retirement proof, not original-byte checks alone. |
| Plugin/hook with owned event records under natural shared lock | `1421e09d4..0a77` traverses manager+130 ProcGen; callsite `1421e0a46` enters `1421e0f50`. This is the best rich observation boundary. Mapped shared +40 lock excludes mapped producer/reset, not destruction/all aliases. Owner fence and uninstall/retirement unresolved. CONDITIONAL engineering candidate, NOT qualified for installation/live use. |
| External snapshot or suspend-all quiescence | Can copy resident maps but stopping application threads may stop a lock holder, does not repair already freed pointers or certify source/population age. PSS/full dump acquisition and protections are not qualified here; existing archived extents lack required arrays. Potential selected-cache offline parsing after separately qualified snapshot, but no same-evaluation branch without an additional event. No claim that snapshotting supplies native coherence automatically. |
| Generator-only hook | `14079f860` inserts a source-pointer cache entry then invokes `14079b520 → 14079c470 → 14079a330`; visited append does not certify completion. Actual input/path receipt useful, but cannot assert which later query consumes it without a lifecycle join. Auxiliary, more intervention than the initial manual route. |

Smallest later native target: one natural IL consumer evaluation and Cu control,
capturing selected Workshop/extractor/base/IRES, source/resource slot, actual
used region bound/count/points and per-use query/radius/upper, terminal branch
and selected resource gate. Full population is required only for population
equality/absence; bounded subset can prove an individual actual acceptance.
Never call truncation complete, nor infer rejected tails after early acceptance.
`1421f68f0` and `1421f6b3a..6b5c` select spatial/skip-vein/atmosphere collections;
that resource gate is not complete placement admission. Colored preview drawing
is still not joined to this predicate. No forced generation/reset is proposed.

Producer stage, if later justified, needs owner+80, packed cell, CRC/MT state,
effective descriptor/BIOM/RSGD/family/weight/order, source anchor/orientation,
prior competing population and readiness result as actually observed. A consumer
cache hit cannot recover them. Preserve source/cache identity, producer success,
generation/output and consumption digests separately. Pointer/hash equality does
not exclude ABA or certify lifecycle. No native monotonic generation counter has
been established; side tokens require complete witnessed transitions.

## Risk → qualification → objective decision

Every row is a future test specification. No unrun row is a PASS. Manual route
prerequisites are practical operator/capture tasks; they do not depend on solving
the unresolved native owner problem.

| Risk | Mitigation and bounded verification | Objective pass/fail | Abort/fallback and residual uncertainty |
|---|---|---|---|
| Original/current saves altered by gameplay/cloud | Isolated disposable state; hash original and current playthrough; resolve actual write/cloud path with unrelated disposable test before target load | All tested manual/autosave/exit writes confined to disposable location, source manifest unchanged, cloud behavior accounted for. Otherwise FAIL admission | No target load; retain logs, correct isolation under later authority. Unknown untested platform paths remain explicit; do not claim all configurations safe |
| Wrong P3/extractor or ambiguous twins | Saved Workshop/body/parent/base join plus continuous three-landmark map/operator confirmation; compare selected IL/Cu card | Unique correspondence or SITE_ONLY/UNKNOWN; name alone FAILS exact extractor join | Stop exact-object arm; reconcile existing map offline. Visual association is not runtime ID resolution |
| View/reticle drift or UI negative mistaken for native absence | Fixed camera and stationary repeat; three original landmark feature pairs, direct pixel displacement with no fit/warp, independent reader recomputation; 3px admission/6px edge exclusion; Cu positive control; retain rejection text | Each landmark displacement at most 3px, unambiguous independent admission and readable/covered stated ROI; otherwise spatial comparison FAILS. Blocked is BLOCKED, loss/unreadable UNKNOWN | One deliberate recapture, then site-level only. Ghost/world coordinates, unseen area, parallax and native gate remain unknown |
| Capture loss/clock ambiguity | Chunked ordinary video, sequence log, flush/close and hash manifest; disposable recording test includes menu/load transition | Continuous before/control/after spans, readable labels and recorded loss status; any gap touching required span FAILS that pair | Preserve intact groups, recapture only the missing finite pair under authority. Unknown loss is not zero loss |
| Game evolution confounds reload | Stationary no-action control; record actions, loading/time/weather; compare saved decoded fields in optional A arm | Stable control needed to attribute association specifically to reload; otherwise observational difference only | Stop causal arm, report confounder; no repeated travel hunt. Even stable control does not prove identical effective native inputs |
| Native owner freed/reused or alias writes | Trace complete owner birth/destruction/alias paths; identify a real fence spanning callback and copy. Inspect normal and unwind paths before any runtime design | Static coverage demonstrates retained owner and mutation exclusion for exact copied scope; missing alias/fence FAILS. Synthetic lease alone cannot pass | Reject native arm, manual route remains available. No new reference/lock mutation to paper over missing proof |
| Native copy overrun/cold latency/overflow | Checked nested counts/capacities, preallocated owned queue, nonblocking producer, no deferred pointers; disposable owned-array fixtures and future measured cold-copy tests | Overflow/truncation/loss sticky and rejects complete-population claim; no allocation/I/O in lock; bound justified by actual selected scope and measured costs. Retail costs NOT TESTED | Refuse capture before unsafe copy; preserve minimal scalar/LOSS only if qualified, otherwise disable admission. Synthetic timing is not retail timing |
| Reentrancy, exceptional exits, state perturbation | Per-thread lifetime/nesting sequences, preservation contract for ABI/registers/flags/MXCSR; explicit unwind/LOSS terminal; disposable harness | Every admitted group has one terminal or declared loss; no undeclared state change across normal/nested/unwind paths | No live deployment on failure. Harness coverage cannot prove every retail path |
| Cross-epoch attribution/readiness | Witness birth/reset/replacement and producer success; owned snapshot, source key plus lifecycle token; actual complete vs partial collection | No gap between positive producer/population/consumer join; missing readiness/transition evidence FAILS end-to-end replay, not a valid consumer-only sample | Downgrade to consumer-only; unknown history retained. Reset `14079ddf0` and destruction `14079d910` are distinct; travel binding unmeasured |
| Hook/debugger retirement or queued trap after removal | Prefer no instrumentation for first route. Any future design must close admission, drain callbacks/queues, prove instruction/trap ownership and no post-retirement deliveries under normal/STOP/exception paths | Original bytes plus survival are insufficient. Demonstrated quiescence and no residual trap/worker across all approved teardown paths required; previous debugger remains FAIL | Do not attach/install. Later recovery/normal-exit authority required; never improvise detach/kill or suppress exceptions |
| Disk/integrity/worker failure | Both-drive 40GB decimal guard, protected hashes, complete flush, health and operator STOP | Any guard/hash/worker failure halts affected admission; delayed poll/operator alone is not failure | Preserve evidence and safe authorized normal recovery; no cleanup of historical evidence, no arbitrary healthy-run time/event cutoff |

No native prototype was built: it would not establish the missing retail fence
or retire the historical trap failure. The actual offline prototype addresses
the selected manual route's evidence-accounting risks. Full native qualification
would require separate source-bound engineering and live approval. This is a
specific conditional route hierarchy, not an assertion of universal impossibility.
