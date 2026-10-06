# SPDX-License-Identifier: GPL-3.0-or-later
# Future Gate B only: creates one explicit checkpoint request in an existing
# observer session. Does not launch/attach/deploy, inspect saves or use console.
param(
    [Parameter(Mandatory=$true)][string]$Session,
    [Parameter(Mandatory=$true)][ValidateSet('A0','A0C','A1','A1C','A2','A2R','TRACE')][string]$Checkpoint,
    [switch]$GateBApproved,
    [switch]$OperatorSettled,
    [switch]$ReloadedAndSettled,
    [switch]$AcknowledgePriorAnomalies,
    [switch]$SeparateDiagnosticApproved
)
$ErrorActionPreference='Stop'
if (!$GateBApproved) { throw 'Gate B approval is required; no request written' }
if (!$OperatorSettled) { throw 'Explicit operator settled confirmation required; no request written' }
if ($Checkpoint -eq 'A2R' -and !$ReloadedAndSettled) { throw 'A2R requires explicit reloaded-and-settled confirmation; no request written' }
$repo=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$allowed=[IO.Path]::GetFullPath((Join-Path $repo '.local-work/exp0002-live'))
$sessionPath=[IO.Path]::GetFullPath($Session)
if ([IO.Path]::GetDirectoryName($sessionPath) -ne $allowed) { throw 'Session outside exact experiment output root' }
for ($checkPath=$sessionPath;$checkPath;) {
    if ((Get-Item -LiteralPath $checkPath).Attributes -band [IO.FileAttributes]::ReparsePoint) {throw 'Reparse output path rejected'}
    $checkPath=[IO.Path]::GetDirectoryName($checkPath)
}
$ready=Get-Content -LiteralPath (Join-Path $sessionPath 'ready.json') -Raw | ConvertFrom-Json
$proc=Get-Process -Id $ready.pid -ErrorAction Stop
if ($proc.ProcessName -ne 'Starfield' -or $ready.terminal -ne 'READY') { throw 'Session process/readiness mismatch' }
. (Join-Path $PSScriptRoot 'request_time.ps1')
if ($proc.StartTime.ToUniversalTime() -gt (Get-ObserverReadyUtc $ready.utc)) {throw 'Stale session or reused process ID'}
if (Test-Path -LiteralPath (Join-Path $sessionPath 'failure.json')) { throw 'Observer session has failed; no retry' }
foreach ($drive in @('C:\','D:\')) {
    $disk=[IO.DriveInfo]::new($drive)
    if (!$disk.IsReady -or $disk.AvailableFreeSpace -lt 40000000000) {throw "Disk safety threshold: require 40 decimal GB available on $drive"}
}
$sequence=@('A0','A0C','A1','A1C','A2','A2R')
if ($Checkpoint -eq 'TRACE') {
    if (!$SeparateDiagnosticApproved) { throw 'Separate diagnostic approval required' }
    if (!(Test-Path -LiteralPath (Join-Path $sessionPath 'complete.json'))) { throw 'Secure checkpoint sequence first' }
    $complete=Get-Content -LiteralPath (Join-Path $sessionPath 'complete.json') -Raw | ConvertFrom-Json
    if ($complete.terminal -ne 'CHECKPOINT_SEQUENCE_COMPLETE') {throw 'Diagnostic requires all six successful checkpoints; anomaly sequence is not sufficient'}
    $permit=Join-Path $sessionPath 'permit-TRACE.txt'
    $f=[IO.File]::Open($permit,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::Read)
    try { $b=[Text.Encoding]::UTF8.GetBytes("SOR-EXP-0002 separate diagnostic approval`n");$f.Write($b,0,$b.Length);$f.Flush($true) } finally {$f.Dispose()}
} else {
    $index=[array]::IndexOf($sequence,$Checkpoint)
    for ($i=0;$i -lt $index;$i++) {
        $anomaly=Join-Path $sessionPath ($sequence[$i]+'-anomaly.json')
        if (Test-Path -LiteralPath $anomaly) {
            $previous=Get-Content -LiteralPath $anomaly -Raw | ConvertFrom-Json
            if (!$AcknowledgePriorAnomalies -or $previous.terminal -ne 'ANOMALY_RECORDED') {throw 'Review prior anomaly evidence; explicit -AcknowledgePriorAnomalies required to continue'}
        } else {
            $previous=Get-Content -LiteralPath (Join-Path $sessionPath ($sequence[$i]+'.json')) -Raw | ConvertFrom-Json
            if ($previous.terminal -ne 'CHECKPOINT_COMPLETE') { throw 'Previous checkpoint incomplete' }
        }
    }
}
$request=Join-Path $sessionPath ('request-'+$Checkpoint+'.txt')
$temp=$request+'.pending'
$stream=[IO.File]::Open($temp,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try {
    $attestation=if ($Checkpoint -eq 'A2R') {'RELOADED_SETTLED'} else {'SETTLED'}
    $bytes=[Text.Encoding]::ASCII.GetBytes($Checkpoint+"`n"+$attestation+"`n")
    $stream.Write($bytes,0,$bytes.Length);$stream.Flush($true)
} finally {$stream.Dispose()}
[IO.File]::Move($temp,$request)
Write-Output "Requested $Checkpoint; return to the game without movement. Check $Checkpoint.json or $Checkpoint-anomaly.json and failure.json. No automatic retry."
