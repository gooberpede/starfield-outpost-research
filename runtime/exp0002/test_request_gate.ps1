# SPDX-License-Identifier: GPL-3.0-or-later
# Offline negative guards only: no valid session, writes, game or process access.
$ErrorActionPreference='Stop'
$checks=0
function Reject-Request($argsToUse,$expected) {
    $caught=$false
    try { & (Join-Path $PSScriptRoot 'request.ps1') @argsToUse }
    catch {if ($_.Exception.Message -ne $expected) {throw};$caught=$true}
    if (!$caught) {throw 'Missing request guard'}
}
Reject-Request @{Session='unused';Checkpoint='A0'} 'Gate B approval is required; no request written';$checks++
Reject-Request @{Session='unused';Checkpoint='A0';GateBApproved=$true} 'Explicit operator settled confirmation required; no request written';$checks++
Reject-Request @{Session='unused';Checkpoint='A2R';GateBApproved=$true;OperatorSettled=$true} 'A2R requires explicit reloaded-and-settled confirmation; no request written';$checks++
@{kind='SYNTHETIC';checks=$checks;terminal='REQUEST_GATE_TESTS_COMPLETE'} | ConvertTo-Json -Compress
