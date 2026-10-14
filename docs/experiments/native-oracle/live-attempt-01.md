# Controlled live attempt 01 — SOR-EXP-0031 / SOR-EV-0039

2026-10-11, Australia/Sydney. **Acquisition result: NOT_OBSERVED.** The approved
Save25/Save26 route and build controls produced zero journaled callback, center
or grid events. Native equivalence remains NOT TESTED. Startup and capture
retirement checks succeeded within their recorded scope; useful-event acquisition
did not. **The attempt did not satisfy the approved startup exclusivity condition:**
Steam/NVIDIA overlay modules were present, and Codex proceeded without resolving
their conflict with the card's no-other-injector requirement. No implementation
defect or corrective patch was established by the
bounded offline investigation. No retry or broader experiment was performed.

## Authority and exact experiment

After [Phase A independent acceptance](independent-review.md), the user approved
the plugin and [exact run card](run-card.md), reported deployment in Vortex profile
`Starfield - SFSE` with no other plugins enabled, made execution conditional on
preflight, and authorized plugin patching on failures while excluding broader
experimentation. The user retained Vortex deployment, loader launch and gameplay
controls. Full statement/pins are retained in
`.local-work/native-oracle/operations/live-authorization-01.json` and matching MD.
No additional authority is inferred from the no-hit result.

Approved component SorNativePositionOracle0.1.0, build `final-review-04`:
ZIP SHA256 `4769f2482f06d009126395c34e280b3011763fe0e5a979598bdc4b8217d6ec79`;
DLL `c4c3e23c9a741d7d2937fce7ffb38013b0036e4d5a07143c1d6c57d4045c2584`.
Game/SFSE/loader and original Save25/26/archive/frozen 23/observer 0.1.1 pins remain
those in the approved ledger. The reviewed source and card were not changed.

Session: `.local-work/native-oracle-live/session-30640-210023156/`;
PID 30640, creation FILETIME 134361872572484823, loaded game base
`0x00007ff65b0f0000`, QPC frequency 10,000,000. Static VA, runtime VA, RVA and PE
file offset remain separate domains; no game-memory reader/debugger was used.
In-process code/vtable patches affect execution and are not described as
non-invasive. They remain resident/inert after STOP until normal process exit.

## Recorded procedure and observations

Deployed preflight passed 33 checks: exact package/DLL/config, game/SFSE/loader,
sources, six protected pins, process absence, sole deployed SFSE plugin and disk.
All 25 reviewed text-file hashes and HEAD/index also matched before launch.
These automated checks do not establish all operational admission conditions.
User launched via Vortex's `sfse_loader.exe` and reported a responsive main menu.

READY was present after a 59,329 ms startup wait. Process creation time was checked
through QUERY_LIMITED_INFORMATION against READY. File/module hashes, both channels,
schema 17,768, four patch locations/original hashes and SFSE success log passed.
Startup module inventory contained 90 modules, including Steam/NVIDIA overlays;
there was one SFSE plugin. No unexpected second SFSE plugin was observed. This
inventory does not prove arbitrary injectors absent or all module behavior safe.
Patch installation/integrity is plugin-attested, not independently read from live
memory. READINESS is not proof that any patched callback executes.

**Operational deviation:** the card requires no other code hook/injector, and
the architecture excludes other plugins/injectors from its startup assumption.
The user reported no other Vortex plugins; that did not waive the broader
condition or explicitly except Steam/NVIDIA overlays. Codex saw the inventory
and incorrectly proceeded to save/gameplay controls without resolving this
conflict. No retained authorization supplies such an exception. Full startup
exclusivity was not established, so automated runtime checks PASS must not be
read as all mandatory admission gates PASS or qualified safe activation. This
also does not prove that an overlay caused a race or the no-hit result; no such
runtime causal evidence was captured. The reviewed startup assumption is not
retroactively weakened. The attempt is already retired/exited/removed; no retry
or overlay/configuration change is performed. Future live admission requires
an explicitly reviewed disposition of this condition before scientific actions.

| Operator-confirmed phase | Recorded result |
|---|---|
| Save25 load at SOR-003, closed/no-action | Responsive; zero records |
| Save25 SOR-003 build open, no changes | Responsive; zero records |
| Save25 fast travel to SOR-002, closed/no-action | Responsive; zero records |
| Save25 SOR-002 build open, no changes | Responsive; zero records |
| Save25 fast travel back to SOR-003, closed | Responsive; zero records |
| Save26 load at SOR-003, closed/no-action | Responsive; zero records; location initially unconfirmed, then explicitly confirmed and separately marked |
| Save26 SOR-003 build open, no changes | Responsive; zero records |
| Save26 fast travel to SOR-002, closed/no-action | Responsive; zero records |
| Save26 SOR-002 build open, no changes | Responsive; zero records |
| Save26 fast travel back to SOR-003, closed | Responsive; zero records |

Each phase has operator marks, exclusive analysis outputs and health snapshots.
Request marks precede actions and do not falsely attest completion. Location
testimony is not native reference identity. No arbitrary collection timeout,
object change, placement, relocation, deletion, manual/scripted save, console
command, new site, debugger, setting change or instrumentation expansion occurred.
The initial request mark is 21:18:18 Sydney; final-return health check 21:32:07.
Exact primary timestamps remain UTC in local receipts. Continuous capture was
armed before save loading. No no-hit phase was represented as arithmetic failure.

All recorded disk checks retained 40,000,000,000 caller-available bytes on each
drive; the smallest recorded C: value was 83,208,355,840 bytes and D: value
138,839,465,984 before retirement. All phase protected-input checks passed.
No failure/not-ready marker, raw tail or journal truncation was observed.
Marker absence alone was not treated as an independent worker heartbeat.

After the complete sequence, Codex wrote the approved STOP. Matching retired.json
was produced after the STOP file: events 0, lost 0, depth_errors0, resident inert,
patches retained. The game remained responsive at that check. This demonstrates
worker execution at retirement and a completed capture drain; it does not prove
continuous worker scheduling, callback reachability or original-byte hot restoration.
The `utc` value inside retired.json is the shared startup identity timestamp,
not a retirement time; STOP/terminal file ordering and verification receipt
timestamp provide the retirement observation.

User then reported normal game exit, completed Steam sync and plugin disable.
Postflight passed 29 checks, separately rehashed deployed game/SFSE/loader, confirmed
both deployed observer DLL/config paths absent and target/debugger process absence.
Six protected pins and source hashes remain unchanged. C:/D: free space at the
supplemental postflight was 85,922,119,680 /138,838,753,280 bytes. No forced exit,
unhook, file deletion, save modification, staging, commit, push or upload by Codex.
Incidental autosave activity is not claimed absent; no prelaunch full save-folder
inventory was captured. Protected originals/archives are the verified guarantee.

## Bounded offline diagnosis

The authorized specialist independently rechecked existing primary static exports:

| Question | Evidence and scoped conclusion |
|---|---|
| Wrong vtable slot or devirtualized dispatcher? | `exp0002-selection-sites.tsv`877/915: static 140B1E2C0/140B1E33C call `[vtable+10]`; both original callback slots were patched. `engine-oracle-02.tsv`159–164 constructs exact 144B916E8 before B1E190. These observed branches support the chosen slot; no concrete copied-vtable/devirtualization defect found. |
| Can upstream gates prevent callback dispatch? | `engine-oracle-02.tsv`76/82/95–127 requires resolved overlay, active landscape, matching hierarchy and overlay+20 bit 0. Selection export 827–915 additionally filters nonempty reference collections, flags and non-null base. These are STATIC gates, not observed runtime causes. |
| Does existing-site travel guarantee candidate search? | `durable-center-04.tsv`2212–2245: the known 77FC20 path tests eligibility, searches existing references via 77F900, then reaches 77E350 as fallback. No evidence that existing-site fast travel traversed that fallback. Other callers/paths are not excluded. |
| Could an internal Workshop predicate alone explain zero begins? | `core.h` emits begin before original callback execution. That later predicate alone cannot explain absent begin records, assuming the observed callback is dispatched and admission works. |
| Does zero center capture exclude fresh build-mode centers? | No. Only CALL RVA AD0C36 inside the scoped callback is patched. Other F4AB80 callers/consumers are not observed; the center channel is independently enabled but not a broad helper-entry observer. |

Selected static export hashes are in [native-sources.csv](native-sources.csv).
The specialist found no concrete patchable implementation fault. Remaining
alternatives include upstream branch/gate non-traversal, absence of eligible
reference enumeration, an unobserved alternate path, or an uncaptured observer
admission/transport condition. No runtime gate values/call counters were captured
to select among them. STOP response narrows the worker-liveness concern only at
retirement. Installing guards, a responsive target and an empty file are not
proof of semantic execution or a generally safe integration point.

No unchanged-card action is statically demonstrated to improve reachability;
identical repeats have no established diagnostic gain. Adding upstream hooks or
changing gameplay triggers would exceed the reviewed card and needs a specific
review/authorization decision. Patching permission was retained but not used to
invent a speculative fix or silently broaden acquisition.

## Outcome dimensions and review package

| Dimension | Result |
|---|---|
| Automated deployed/runtime checks | Individual checks PASS for recorded pins/guards/startup; no proof of callback execution |
| Full operational admission/card conformance | NOT SATISFIED: injector-exclusivity conflict was unresolved before proceeding; not qualified safe activation |
| Useful native oracle acquisition | NOT_OBSERVED; zero callback/center/grid records |
| Deterministic model comparison/branch coverage | NOT TESTED; no support or counterexample added, frozen 23 unchanged |
| Capture health/retirement | Matching STOP/retired0/0/0; no failure markers, complete empty journal/raw prefix |
| Target survival | Operator reports responsive throughout and normal exit; process absence corroborated |
| Cleanup/protected inputs | PASS postflight/removal/hash checks; no hot-unhook claim |
| Diagnosis | No established implementation defect; actual runtime blocking branch UNKNOWN |
| Scientific/publication state | No semantic promotion or publication clearance |

Local primary evidence is the session, operations/live-preflight-01.json,
live-authorization-01.json and live-postflight-01.json. Exact raw file/mark/log/
receipt hashes are inventoried in `.local-work/native-oracle/live-attempt-01/`.
Complete/task-only review patches use `native-oracle-live-01-*.diff` under
`.local-work/diffs/`; task-only applies to the retained pre-live working tree,
complete to HEAD. Raw/native/proprietary material stays local/untracked.
[Independent critical review](live-attempt-01-review.md) ACCEPTS this scoped report
and bounded diagnosis, not operational conformance. This report does not establish
negative feasibility for every acquisition method or complete the wider
native-equivalence objective.
