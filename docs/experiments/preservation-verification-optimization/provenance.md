# Source and execution provenance

[Pinned local source ledger](sources.csv), [governing brief](../../implementation-briefs/CODEX_BRIEF_SOR_preservation_audit_optimization.md),
[research methods](../../../research/preservation-verification/README.md).

All new code is original task implementation using installed CPython stdlib,
Windows APIs, SQLite and existing Git. No third-party package, code snippet,
dependency download, external implementation or outside communication is used.
Existing maintainer-authored methods are consulted or invoked under SOR-P-0002:
the D5C/D5D/D5G audits, D5E retained receipts, `protection.py`, `save_policy.py`,
the editorial screen and `research/review_package.py`. Their input hashes are
in the ledger; executable originals remain outside authored deliverables.

D5G's retained before-method and final audit source distinguish executed before
behavior from the later eight-worker after branch. Its reviewed completion
record independently supplies the expected audit-receipt hash. Before/after
receipt equality is independently recomputed, not inferred from a PASS label.
The 64 initial source identities cover actual reconstruction/policy/method inputs;
the subsequently used D5G source ledger is checked against exact HEAD bytes
before parsing and separately pinned. Task-result receipts are new originals,
not historical expected inputs. Reviewer and delivery manifests bind later
supplementary results and final method hashes.

The imported tungsten `save_policy.py` and policy JSON are exact-byte copies of
the Carinae versions pinned at intake. A final dependency-path check separately
verifies both actual imported paths against those expected hashes and HEAD;
their physical-path verification was late, not a claimed pre-execution check.
The intake helper now includes both actual paths prospectively. This correction
does not change protection behavior or rewrite the original 64-input receipt.

Windows SDK 10.0.26100.0 `winioctl.h` was consulted for interface constants and
structures. Microsoft documents
[journal querying](https://learn.microsoft.com/windows/win32/api/winioctl/ni-winioctl-fsctl_query_usn_journal)
and [journal reading](https://learn.microsoft.com/windows/win32/api/winioctl/ni-winioctl-fsctl_read_usn_journal).
These are factual API sources, not incorporated implementation. The actual
unprivileged root-handle behavior was tested locally; neither documentation nor
an available API establishes the integrity of unread historical bytes.

The existing installed CPython 3.14.3 and Git 2.53.0.windows.1 are reused. Their
observed identities, the SDK-header digest, failed journal probes and OS details
are retained in ignored environment receipts. No Windows privilege elevation,
software installation or volume/journal reconfiguration occurred. The temporary
read-deny ACE is confined to one generated fixture per permission test and is
removed in the test's finally block; raw ACL diagnostics stay local.

Raw historical manifests contain personal machine paths and remain LOCAL-ONLY.
Authored aggregate tables contain relative source locators, counts, hashes and
synthetic measurements. They copy no game binary, save, memory/native capture or
analysis database. Authored synthesis and new code remain REVIEW-REQUIRED;
publication/B6 is not cleared by this audit or by an independent review.

Initial `git status --short` showed only the supplied brief. The durable
`start.json` was captured after three new task scripts had been created, and
truthfully includes that new research directory. `export-baseline.json` combines
the initial tool-observed clean-plus-brief status with the later HEAD/index
identity; its stated basis is explicit. No Git index/ref write occurred between
those reads. The original brief's bytes and line endings remain intact, and it
appears only in complete-patch accounting, not as task-authored text.
