# Debugger Research

No backend, version, attach workflow, or script is selected or qualified in this project. Ghidra debugger, dbgeng/Pybag, x64dbg, or another tool may be considered in a separately authorized investigation; none is an approved dependency merely because named here.

Future project-authored automation belongs in [scripts/](scripts/README.md). Prefer observation-only work, but record that attachment, pausing, stepping, and breakpoints can perturb timing/state. Explicitly scope attach/detach, breakpoints, target pause/resume, reads/capture, error handling, and cleanup before a run.

No instruction patching, target-memory/register writes, exception suppression, target termination, or deployment under an observation-only task. A software breakpoint may itself alter executable bytes; disclose the mechanism rather than claiming zero process impact. Any intervention needs explicit authorization and suitable controls.

Record the actual module/ASLR base, executable hash, normalized RVA/static-address mapping, thread/stack provenance, loaded state, timing, instrumentation, and sample IDs. Keep dumps/raw captures local. A functioning debugger connection is not evidence of outpost semantics.
