# SPDX-License-Identifier: GPL-3.0-or-later
# Pure timestamp conversion; no filesystem/process access or writes.
function Get-ObserverReadyUtc {
    param([Parameter(Mandatory=$true)]$Value)
    # ConvertFrom-Json in recent PowerShell returns a DateTime for ISO stamps.
    # Re-parsing that object as text can swap month/day under the local culture.
    if ($Value -is [datetime]) { return $Value.ToUniversalTime() }
    return [datetime]::Parse([string]$Value,
        [Globalization.CultureInfo]::InvariantCulture,
        [Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime()
}
