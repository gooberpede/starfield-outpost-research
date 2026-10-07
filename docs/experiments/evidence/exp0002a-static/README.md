# SOR-EV-0005 — Native save mapping and unsuccessful live setup

2026-10-07 Australia/Sydney; SOR-EXP-0002A / SOR-ENV-0003 / SOR-D-0014. [Report](../../SOR-EXP-0002A-native-save-thread-mapping.md). Authored index REVIEW-REQUIRED; every raw artifact LOCAL-ONLY. Static candidate mapping succeeded within its stated limits. No ordinary manual-save trace or credible native invocation contract was acquired. Stage C not entered. The user exited normally and reported sync complete/no manual save. No game crash recorded; debugger interventions are disclosed separately from evidence completeness.

All paths below are repository-relative ignored local locators. No raw binary, decompilation, debugger database, private save name or memory log is incorporated into Git. Hashes identify exact artifacts, not semantic truth. Exact addresses/call sites and source credits SOR-S-0120/0121 are in the report. Public source consultation did not broaden SOR-P-0001; no new third-party code incorporated.

## Decisive locators and limits

- save-leads: existing string/xref scan, ending SCAN_END cancelled=false. Per-string xref caps still apply. source-sites: PARTIAL/FAILED at stale instruction142551f1b; paired independent PE source-sites.json rejects old E8 call transfer.
- save-functions: FUNCTION14166c190 new-slot argument setup/call14166c1be, FUNCTION14183c830 call14183c9a0, FUNCTION141814050 and FUNCTION141814220; serializer finished-saving diagnostic is not final completion.
- request-functions: FUNCTION14183c590 call14183c65d/state/gates, FUNCTION141821b70 call141821ba8, FUNCTION14183aaf0 finalization setup, manager-constructor lead141839c60.
- ui-thread-functions: FUNCTION14166c0a0 direct/queued dispatch, FUN14166f3c0 thunk, FUNCTION14184eec0 naming, finalization thunk141855a20. Large functions'600-instruction caps mean no exhaustive call graph. Full decompilation sections remain interpretations.
- final-windows: PARTIAL/FAILED at guessed center14183b7da. final-sites: corrected WINDOW14183b86d includes clear at14183b850 and wake jump; WINDOW14183a11e thread label; supporting gate/status/file-object functions. Wrapper exit0 alone did not prove success.
- capture-sites.json: independent E8 edges and32-byte site hashes. manual-002/sites-validated.json records runtime base0x7ff60a5b0000 and loaded-code checks before intended breakpoint insertion.
- manual-001: access-denied setup, no attach/sites. manual-002: four intended and four unintended default TLS sites; ten-second bound, zero save hits, detach/restoration. tls-cleanup.json independently compares32 bytes at each extra TLS location with installed DLL bytes. manual-003: automatic TLS disabled, no paused context within five seconds, no research sites armed, detached. v1/v3 raw true restoration flag is vacuous for zero validated sites, not a proof; current v4 reports null/counts.
- Synthetic two-thread/zero-hit/25-hit tests pass with restored bytes, detach and normal fixture exit. transport-tls-disabled passes with corrected settings. Earlier failed tests/logs remain in the same ignored root and are unassessed where independent cleanup/target outcome was unavailable. They were not erased or promoted by later success.
- Each manual attempt's used-source directory retains exact reconstructed controller/helper revisions, accepted only after matching every original preflight source SHA-256. used-source-preservation.json records all12 matches. This preserves v1/v2/v3 provenance separately from current unrun v4. Synthetic fixture binary below is the final build, not an asserted identity for earlier failed builds.

## Preservation and artifact handling

before.json versus final.json: all15 existing Starfield Ghidra project files retain size/hash; four project-container index files (~index.dat/~index.bak under idata/versioned) have changed mtimes. Thus byte preservation passed, full metadata preservation did not. This launcher/project side effect is retained; no analysis/symbol/type/comment mutation is claimed. Seven baseline input files are unchanged. Save3 original/backup remain byte-equal and individually hash/size/mtime-identical to the historical baseline. No CK project editing. Final free C:/D: exceed40,000,000,000 bytes. Raw exports came from read-only/noanalysis operation; independent comparison, not flags alone, supplies byte-preservation evidence.

post-exit.json records one incidental exit save copied after user normal exit/sync confirmation. Source/copy/source checks and byte comparison pass; size2,083,584, SHA-256 `f3151898f7dcfb430457bcfea7916d49c2b98d5e28937eac03bdecf6b79fe387`. The live copy remains. This is not a qualification/manual save, no reload/semantic analysis occurred, and no deletion safety is established.

## Exact artifact identities

| Local artifact | Bytes | SHA-256 |
|---|---:|---|
| `.local-work/recon/exp0002a-final-sites.tsv` | 25317 | `fe20f505bee4dc4a8a3cdd70c67ee27771402f8394e73b8e4ac300b61ac8f75a` |
| `.local-work/recon/exp0002a-final-sites.tsv.log` | 4011 | `ca455e61f2b1ffaeda6feabdea9f0ec545374ea2639fd348dbc6005dd936c128` |
| `.local-work/recon/exp0002a-final-windows.tsv` | 230 | `f92ff850e50c1d7165c4415da2153be86b0a29a15d540213898d7d593f597a64` |
| `.local-work/recon/exp0002a-final-windows.tsv.log` | 5271 | `938984f9832cfd1392d1de0bef71b0db769d0649892010249ba8ba272a947601` |
| `.local-work/recon/exp0002a-request-functions.tsv` | 75804 | `7e0f66b998b9be75e740e095b7e9553380b6a03bd9db804429ba8f019bd3589b` |
| `.local-work/recon/exp0002a-request-functions.tsv.log` | 4087 | `cf5e674d8681002e6729d5ceb93b649a408c8f696fe4f50688e8b12f46d677e1` |
| `.local-work/recon/exp0002a-save-functions.tsv` | 133560 | `01169b9021317a7ea57a689e2618c2794045f52e1eadb1ce77ce737009bf2fe2` |
| `.local-work/recon/exp0002a-save-functions.tsv.log` | 4057 | `93103e1e7bbd02687a755f0f6bab6d864dfaab40f70cc13f2060798b75488fc6` |
| `.local-work/recon/exp0002a-save-leads.tsv` | 39311 | `045a184865ea9d7218ed27c3e6b2d01d62363c232f7b528dae0d40f95c87324c` |
| `.local-work/recon/exp0002a-save-leads.tsv.log` | 3922 | `65c8eafa5c910c40fea5e922da437847980c63f7292085ee176dc4ae1269f692` |
| `.local-work/recon/exp0002a-source-sites.tsv` | 224 | `19028108a9bf8e3c5ee0e3656201aa3cc6b2395f164ae0b16a2b674253f413dd` |
| `.local-work/recon/exp0002a-source-sites.tsv.log` | 5213 | `cb0c08d9b641eec0ed5ecf0844a1b0200b65eeabdc662f0ac036f0ab00bc563b` |
| `.local-work/recon/exp0002a-ui-thread-functions.tsv` | 136927 | `43a7d43eb7c63ec40cc727b7c460464c9bd404ebc53847d1703f106d46243230` |
| `.local-work/recon/exp0002a-ui-thread-functions.tsv.log` | 4071 | `b70a540585603fa1a5a03114427e7ffb1d50820f5c9a9a4169bce4caae18dec4` |
| `.local-work/exp0002a/before.json` | 8806 | `48deb38d06ad9b73c95cf4974473fd9ee03f49ef1dc8c666383672df27d4117b` |
| `.local-work/exp0002a/after.json` | 8806 | `eac710145fd16f01e6c1d40a17a297ac2173db384c9f9813098525d340a17f26` |
| `.local-work/exp0002a/final.json` | 8806 | `0921e03432ed4eb9e5f97d481a454c0476b97bc0b5855519acf4d35a86a8c3c8` |
| `.local-work/exp0002a/source-sites.json` | 2006 | `ba0feb810cbcaeb80e6b8610326b9b37aaba1d77894155210ba97f13f88ec010` |
| `.local-work/exp0002a/capture-sites.json` | 3083 | `f71bcc7a415a5b2c5714d0d123490aaf2c855e9a76bc4252e3cf2c86bb9b8ab2` |
| `.local-work/exp0002a/post-exit.json` | 1855 | `06d79aa76a098e199637cf7449fa784f1ba9be7061d5970f2e650458b49f1fee` |
| `.local-work/exp0002a/used-source-preservation.json` | 2243 | `84a9daa21797cd6008c0e5cd8e121452aca4949f9d1e7ba0d0cbe99a25f3e3d3` |
| `.local-work/exp0002a/fixture-build/fixture.exe` | 103424 | `6e0b2aa854382444df3c48cbfa00e49bbf7f1f2874389519d5a062d337b88aab` |
| `.local-work/exp0002a/transport-two-threads-03/result.json` | 831 | `35dac2d9d6e16ac7a1eae2a1baa9a5fe128d4f40bcd789cb400efc199f8995c2` |
| `.local-work/exp0002a/transport-two-threads-03/debugger/transport.jsonl` | 13292 | `b729f765ee52a2294d0a129d43168f7c3afffa6ef71b53475a54793cdac87ca5` |
| `.local-work/exp0002a/transport-zero-hit-02/result.json` | 257 | `e63eb913338a5b43f2bd97145a8d9dfce6bb6e1fe72330202ed1f6cc020334b8` |
| `.local-work/exp0002a/transport-zero-hit-02/debugger/transport.jsonl` | 12600 | `40c03b732f11df22911281f1e7f9ac716c6b641cae77b683eb2e4341db96085c` |
| `.local-work/exp0002a/transport-hit-cap-02/result.json` | 7386 | `725e5ef4733446fc98a7491bfedd38597379eb5a132504b212662e7452733ca3` |
| `.local-work/exp0002a/transport-hit-cap-02/debugger/transport.jsonl` | 18723 | `fd9c719373292ad2263749ee928a6da6a1e7129d7bcc861b863c1bcbd4c50c55` |
| `.local-work/exp0002a/transport-tls-disabled/result.json` | 832 | `b5e379fca25541ebe61c8cc78663e5c02d9dc552c8667de8d736c8e716235e56` |
| `.local-work/exp0002a/transport-tls-disabled/debugger/transport.jsonl` | 13283 | `c531f4bccf5ec3198142f0bcd8ac78e8dd9141798d578405aa5590d1a2da3e57` |
| `.local-work/exp0002a/manual-001/preflight.json` | 50933 | `fa65df2835c640b349e9398f21a5383865c59695d3b3437245730f00381f3000` |
| `.local-work/exp0002a/manual-001/result.json` | 39646 | `0fad3243d7b714440cc657c44b2684e71f6730e5ea67d8433d36e1b9058a0824` |
| `.local-work/exp0002a/manual-001/debugger/transport.jsonl` | 3097 | `8f5b664c754b3c29cef004dda1a9eea5cdc38f2d4860058886d877014b46f3cc` |
| `.local-work/exp0002a/manual-002/preflight.json` | 50349 | `91cea0b3ff10f37d432c91b88e1fa54dc3063f740f5a97cca1906c1a126cac0f` |
| `.local-work/exp0002a/manual-002/result.json` | 39620 | `9bc1dd08ed02774eb4840f88ee9519e169c16b72826f2ce00a8f53ecc9936b73` |
| `.local-work/exp0002a/manual-002/debugger/transport.jsonl` | 172548 | `e29524246a7da02ae00246f78866185f26c06c7975dbfb83f52ed573a2b127fd` |
| `.local-work/exp0002a/manual-003/preflight.json` | 50517 | `b28e2926ed5df4c98d13f25ca300baf63faa6939d4d195b5f75555d3d47ce492` |
| `.local-work/exp0002a/manual-003/result.json` | 39646 | `50a3bfa47a639cc1a4935631bfc483978c0d2f1e0a94b9673a8c16d98f457ecd` |
| `.local-work/exp0002a/manual-003/debugger/transport.jsonl` | 169675 | `9c93d00eb353a6c17c9ab8b00ff98fd61f42ccbf603101a51f7718cd59604634` |
| `.local-work/exp0002a/manual-002/sites-validated.json` | 1047 | `9745e8217579e607fa872880283abe3c9c4ab66bed428839ed9a6fe4fe425540` |
| `.local-work/exp0002a/manual-002/tls-cleanup.json` | 1775 | `37948c435dd3acc2b330f1965c99acde210b0b3b58b8432958e9b5f7447fa68f` |

## Review package

Local [complete diff](../../../../.local-work/exp0002a/review.diff), [status](../../../../.local-work/exp0002a/status.txt), [validation](../../../../.local-work/exp0002a/validation.json), [changed-file hashes](../../../../.local-work/exp0002a/hashes.json), and [raw evidence manifest](../../../../.local-work/exp0002a/evidence-manifest.json). The diff includes untracked additions and the unchanged user-supplied brief, separately identified in hashes.json. No staging/commit/push. These links require the maintainer's local checkout and are not a published evidence bundle. Review can reproduce hashing/syntax/plan comparisons without launching the game; live retry requires resolving the reported setup failure and preserving the original bounds.

Suggested commit after critical review: `docs(research): map native save execution path`. No successful native-save qualification claimed. Do not resume EXP0002 construction from this completion summary.
