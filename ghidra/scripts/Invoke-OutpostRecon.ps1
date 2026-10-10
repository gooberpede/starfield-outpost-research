# SPDX-License-Identifier: GPL-3.0-or-later
# Reads installed Ghidra launcher JVM settings. Writes only local tool settings,
# cache/logs and the requested export; existing program is read-only/no-analysis.
param(
    [ValidateSet('Starfield','StarfieldCK')][string]$Target,
    [Parameter(Mandatory=$true)][string]$OutputName,
    [string[]]$Addresses = @(),
    [ValidateSet('OutpostRecon.java','OutpostSaveConstants.java','OutpostMembershipRefs.java','WorkshopOriginRefs.java')][string]$Reader = 'OutpostRecon.java'
)
$ErrorActionPreference = 'Stop'
$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$outRoot = Join-Path $repo '.local-work/recon'
if ($OutputName -notmatch '^[a-z0-9-]+\.tsv$') { throw 'Use a simple new TSV filename' }
$ghidraRoot = 'D:/tools/ghidra_12.1.2_PUBLIC'
$vm = Get-Content (Join-Path $ghidraRoot 'support/launch.properties') |
    Where-Object { $_ -match '^VMARGS=' } | ForEach-Object { $_.Substring(7) }
$projectRoot = 'D:/ReverseEngineering/' + $Target + '/GhidraProject'
$program = if ($Target -eq 'Starfield') {'Starfield.exe'} else {'CreationKit.exe'}
& 'C:/Users/User/AppData/Local/Programs/Eclipse Adoptium/jdk-21.0.12.8-hotspot/bin/java.exe' @vm -Xmx2G `
    "-Dapplication.settingsdir=$outRoot/ghidra-settings" "-Dapplication.cachedir=$outRoot/ghidra-cache" `
    -cp "$ghidraRoot/Ghidra/Framework/Utility/lib/Utility.jar" ghidra.Ghidra `
    ghidra.app.util.headless.AnalyzeHeadless $projectRoot $Target -process $program -readOnly -noanalysis `
    -scriptPath $PSScriptRoot -postScript $Reader "$outRoot/$OutputName" @Addresses `
    -log "$outRoot/$OutputName.log"
if ($LASTEXITCODE -ne 0) { throw "Ghidra exited $LASTEXITCODE" }
if (!(Test-Path -LiteralPath "$outRoot/$OutputName")) { throw 'Export missing; inspect Ghidra log' }
