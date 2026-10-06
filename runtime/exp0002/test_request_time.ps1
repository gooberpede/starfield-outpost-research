# SPDX-License-Identifier: GPL-3.0-or-later
# Offline pure timestamp regression tests; never invokes request.ps1.
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'request_time.ps1')
$oldCulture=[Threading.Thread]::CurrentThread.CurrentCulture
$checks=0
try {
    foreach ($culture in @('en-AU','en-US')) {
        [Threading.Thread]::CurrentThread.CurrentCulture=[Globalization.CultureInfo]::GetCultureInfo($culture)
        $stamp='2026-10-06T06:04:53.667Z'
        $decoded=('{"utc":"'+$stamp+'"}' | ConvertFrom-Json).utc
        foreach ($value in @($stamp,$decoded)) {
            $utc=Get-ObserverReadyUtc $value
            if ($utc.ToString('o') -ne '2026-10-06T06:04:53.6670000Z') {throw "Incorrect UTC under $culture"};$checks++
            $before=[datetime]::new(2026,10,6,6,4,52,[DateTimeKind]::Utc)
            if ($before -gt $utc) {throw 'Live session falsely rejected'};$checks++
            if (!($before.AddSeconds(3) -gt $utc)) {throw 'Reused PID would pass'};$checks++
        }
    }
    $rejected=$false
    try {Get-ObserverReadyUtc 'not-a-time' | Out-Null} catch {$rejected=$true}
    if (!$rejected) {throw 'Invalid timestamp accepted'};$checks++
} finally {[Threading.Thread]::CurrentThread.CurrentCulture=$oldCulture}
@{kind='SYNTHETIC';checks=$checks;terminal='REQUEST_TIME_TESTS_COMPLETE'} | ConvertTo-Json -Compress
