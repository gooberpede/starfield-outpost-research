# SPDX-License-Identifier: GPL-3.0-or-later
<# Read-only post-run Windows Application/WER and existing Starfield dump collection.
Writes create-new ignored local evidence only. No registry/config changes, handler
installation, dump generation, target control, network or uploads. Event matching
is app/time plus PID when supplied by the record; app/time-only is not exact proof.
Bounded 256 events, 2000 files per root, depth <=3, 2 GB copied, 40 GB free guards.
#>
param(
    [Parameter(Mandatory)][datetime]$StartUtc,
    [Parameter(Mandatory)][datetime]$EndUtc,
    [Parameter(Mandatory)][int]$TargetPid,
    [Parameter(Mandatory)][string]$Output
)
$ErrorActionPreference = 'Stop'
$StartUtc = $StartUtc.ToUniversalTime()
$EndUtc = $EndUtc.ToUniversalTime()
$repo = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$allowed = [IO.Path]::GetFullPath((Join-Path $repo '.local-work/exp0002a-adapter-0.1.3')) + [IO.Path]::DirectorySeparatorChar
$dest = [IO.Path]::GetFullPath($Output)
if (-not $dest.StartsWith($allowed,[StringComparison]::OrdinalIgnoreCase)) { throw 'Output outside evidence root' }
if ($EndUtc -lt $StartUtc -or ($EndUtc-$StartUtc).TotalHours -gt 2) { throw 'Invalid run time bound' }
New-Item -ItemType Directory -Path $dest -ErrorAction Stop | Out-Null
$start = $StartUtc.ToUniversalTime().AddMinutes(-2)
$end = $EndUtc.ToUniversalTime().AddMinutes(2)
$report = [ordered]@{schema='SOR-crash-collection-1';version='0.1.3';utc=[datetime]::UtcNow.ToString('o');target_pid=$TargetPid;start_utc=$start.ToString('o');end_utc=$end.ToString('o');events=@();files=@();errors=@();roots=@();limits=@();copied_bytes=0}
function Guard-Space {
    foreach ($drive in @('C','D')) { if ((Get-PSDrive $drive).Free -lt 40000000000) { throw '40GB disk guard' } }
}
Guard-Space
try {
    $events = @(Get-WinEvent -FilterHashtable @{LogName='Application';Id=1000,1001;StartTime=$start;EndTime=$end} -MaxEvents 256 -ErrorAction Stop)
    if ($events.Count -eq 256) { $report.limits += 'event limit reached; enumeration may be incomplete' }
    foreach ($event in $events) {
        $xml = $event.ToXml()
        if ($xml -notmatch '(?i)Starfield(?:\.exe)?') { continue }
        [xml]$parsed=$xml
        $data=@{};foreach ($node in $parsed.Event.EventData.Data) { $data[[string]$node.Name]=[string]$node.'#text' }
        $matchKind='APP_AND_TIME_ONLY';$reportedPid=$null
        foreach ($key in @('ProcessId','ProcessID','FaultingProcessId')) {
            if ($data.ContainsKey($key)) {
                try { $value=$data[$key];$reportedPid=if($value -match '^0x'){[Convert]::ToInt64($value.Substring(2),16)}else{[long]$value} } catch {}
                break
            }
        }
        if ($null -ne $reportedPid) {$matchKind=if($reportedPid -eq $TargetPid){'APP_TIME_PID_MATCH'}else{'APP_TIME_OTHER_PID_CANDIDATE'}}
        $name="event-$($event.RecordId).xml"
        [IO.File]::WriteAllText((Join-Path $dest $name),$xml,[Text.UTF8Encoding]::new($false))
        $report.events += [ordered]@{record_id=$event.RecordId;id=$event.Id;provider=$event.ProviderName;utc=$event.TimeCreated.ToUniversalTime().ToString('o');correlation=$matchKind;reported_pid=$reportedPid;file=$name;sha256=(Get-FileHash -LiteralPath (Join-Path $dest $name)).Hash}
    }
} catch { $report.errors += "Application query: $($_.Exception.Message)" }
$roots=@(
    [pscustomobject]@{path="$env:LOCALAPPDATA/CrashDumps";depth=0;kind='crashdumps'},
    [pscustomobject]@{path="$env:LOCALAPPDATA/Microsoft/Windows/WER/ReportArchive";depth=2;kind='wer'},
    [pscustomobject]@{path="$env:LOCALAPPDATA/Microsoft/Windows/WER/ReportQueue";depth=2;kind='wer'},
    [pscustomobject]@{path="$env:ProgramData/Microsoft/Windows/WER/ReportArchive";depth=2;kind='wer'},
    [pscustomobject]@{path="$env:ProgramData/Microsoft/Windows/WER/ReportQueue";depth=2;kind='wer'},
    [pscustomobject]@{path="$env:USERPROFILE/Documents/My Games/Starfield";depth=2;kind='game'},
    [pscustomobject]@{path="$env:LOCALAPPDATA/Starfield";depth=2;kind='game'},
    [pscustomobject]@{path='C:/Program Files (x86)/Steam/steamapps/common/Starfield';depth=1;kind='game'}
)
$index=0
foreach ($root in $roots) {
    $report.roots += $root
    if (-not (Test-Path -LiteralPath $root.path)) {continue}
    try {
        if ($root.kind -eq 'wer') {
            $directories=@(Get-ChildItem -LiteralPath $root.path -Directory -ErrorAction Stop | Where-Object {$_.Name -match '(?i)Starfield'} | Select-Object -First 64)
            if ($directories.Count -eq 64) {$report.limits += "WER directory cap: $($root.path)"}
            $files=@(& {foreach ($directory in $directories) {
                try {Get-ChildItem -LiteralPath $directory.FullName -File -Recurse -Depth $root.depth -ErrorAction Stop}
                catch {$report.errors += "$($directory.FullName): $($_.Exception.Message)"}
            }} | Select-Object -First 2001)
        } else {
            $files=@(Get-ChildItem -LiteralPath $root.path -File -Recurse -Depth $root.depth -ErrorAction Stop | Select-Object -First 2001)
        }
        if ($files.Count -gt 2000) {$report.limits += "file enumeration cap: $($root.path)";$files=$files[0..1999]}
        foreach ($file in $files) {
            if ($file.LastWriteTimeUtc -lt $start -or $file.LastWriteTimeUtc -gt $end) {continue}
            if ($file.Extension -notin @('.wer','.dmp','.mdmp','.hdmp')) {continue}
            $isGame=$root.kind -eq 'game' -or $file.FullName -match '(?i)Starfield'
            if (-not $isGame -and $file.Extension -eq '.wer' -and $file.Length -le 1048576) { $isGame=(Get-Content -LiteralPath $file.FullName -Raw) -match '(?i)Starfield\.exe' }
            if (-not $isGame) {continue}
            if ($report.copied_bytes+$file.Length -gt 2000000000) {$report.limits += "copy byte cap: $($file.FullName)";continue}
            Guard-Space
            if ((Get-PSDrive D).Free-$file.Length -lt 40000000000) {throw 'Projected disk guard'}
            $hash=(Get-FileHash -LiteralPath $file.FullName).Hash
            $copy=Join-Path $dest ("artifact-{0:D3}{1}" -f $index,$file.Extension);$index++
            Copy-Item -LiteralPath $file.FullName -Destination $copy -ErrorAction Stop
            $copyHash=(Get-FileHash -LiteralPath $copy).Hash
            $after=(Get-FileHash -LiteralPath $file.FullName).Hash
            $correlation=if($file.Name -eq "Starfield.exe.$TargetPid.dmp"){'APP_TIME_AND_FILENAME_PID_MATCH_NOT_DUMP_CONTENT_VERIFICATION'}else{'APP_LOCATION_AND_TIME_CANDIDATE_NOT_PID_PROOF'}
            $report.files += [ordered]@{source=$file.FullName;copy=$copy;size=$file.Length;mtime_utc=$file.LastWriteTimeUtc.ToString('o');sha256=$hash;copy_sha256=$copyHash;source_after_sha256=$after;stable=($hash -eq $copyHash -and $hash -eq $after);correlation=$correlation}
            $report.copied_bytes += $file.Length
        }
    } catch { $report.errors += "$($root.path): $($_.Exception.Message)" }
}
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $dest 'collection.json') -Encoding utf8
[pscustomobject]@{events=$report.events.Count;files=$report.files.Count;errors=$report.errors;limits=$report.limits;copied_bytes=$report.copied_bytes} | ConvertTo-Json -Depth 4
