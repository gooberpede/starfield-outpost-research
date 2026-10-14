param([string]$OutputName,[string[]]$Addresses)
if ($OutputName -notmatch '^[a-zA-Z0-9-]+$' -or $Addresses.Count -eq 0) { throw 'Explicit fresh output and quoted address specifications required' }
foreach ($taskDrive in 'C','D') { if ((Get-PSDrive $taskDrive).Free -lt 40000000000) { throw '40GB free-space guard' } }
$taskOutput = "D:/Projects/starfield-outpost-research/.local-work/workshop-population-rework/specialist/$OutputName"
if ((Test-Path -LiteralPath "$taskOutput.tsv") -or (Test-Path -LiteralPath "$taskOutput.log")) { throw 'Output already exists' }
$taskVm = Get-Content D:/tools/ghidra_12.1.2_PUBLIC/support/launch.properties | Where-Object { $_ -match '^VMARGS=' } | ForEach-Object { $_.Substring(7) }
& 'C:/Users/User/AppData/Local/Programs/Eclipse Adoptium/jdk-21.0.12.8-hotspot/bin/java.exe' @taskVm -Xmx2G '-Dapplication.settingsdir=D:/Projects/starfield-outpost-research/.local-work/recon/ghidra-settings' '-Dapplication.cachedir=D:/Projects/starfield-outpost-research/.local-work/recon/ghidra-cache' -cp D:/tools/ghidra_12.1.2_PUBLIC/Ghidra/Framework/Utility/lib/Utility.jar ghidra.Ghidra ghidra.app.util.headless.AnalyzeHeadless D:/ReverseEngineering/Starfield/GhidraProject Starfield -process Starfield.exe -readOnly -noanalysis -scriptPath D:/Projects/starfield-outpost-research/research/workshop-population -postScript ReadNamed.java "$taskOutput.tsv" @Addresses -log "$taskOutput.log"
if ($LASTEXITCODE -ne 0) { throw 'Read-only export failed; preserve its output' }

