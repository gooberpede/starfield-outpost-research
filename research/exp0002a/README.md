# Offline native-save site inspection

`inspect_sites.py` reads the explicit hash-pinned Starfield PE and the project's original EXP0002 PE helpers using CPython's standard library. It writes one create-new LOCAL-ONLY JSON beneath `.local-work/exp0002a`, with <=32 windows of 32 bytes, explicit static VA/RVA/file-offset domains, hashes and E8 relative-call destinations where applicable. It neither disassembles nor executes code, accesses a game process, parses/modifies saves, edits Ghidra, installs dependencies or copies third-party implementation.

Example, under the invoked SOR-EXP-0002A brief:

```powershell
& 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe' research/exp0002a/inspect_sites.py --game D:/ReverseEngineering/Starfield/Starfield.exe --output new-sites.json 0x166c1be 0x183c590
```

Wrong executable hashes and non-file-backed ranges stop inspection. Existing output names are never overwritten. Raw bytes remain ignored/local, not publication-cleared. These independent PE checks corroborate direct-call operands in existing Ghidra exports; they do not prove live reachability or a callable ABI. Sources SOR-S-0104/0105/0113, [experiment](../../docs/experiments/SOR-EXP-0002A-native-save-thread-mapping.md).
