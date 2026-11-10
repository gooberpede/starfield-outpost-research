# SPDX-License-Identifier: GPL-3.0-or-later
# Own one standalone child. Review records and attempts are local and untracked.
param(
    [Parameter(Mandatory)][ValidateSet('normal','pending','missing','fault','tags')][string]$Case,
    [Parameter(Mandatory)][ValidatePattern('^[a-z0-9][a-z0-9-]{0,39}$')][string]$Attempt,
    [Parameter(Mandatory)][string]$Review,
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{64}$')][string]$ReviewHash
)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path -LiteralPath "$PSScriptRoot/../..").Path
$scratch = Join-Path $repo '.local-work/d5bm'
$py = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64/python.exe'
$pyRoot = Split-Path $py
$game = 'C:/Program Files (x86)/Steam/steamapps/common/Starfield'
$protectedPath = Join-Path $scratch 'postflight.json'
$index = Join-Path $repo '.git/index'
$previousOptionalLocks = $env:GIT_OPTIONAL_LOCKS
$env:GIT_OPTIONAL_LOCKS = '0'
try {
    $head = git -C $repo rev-parse HEAD
    if ($LASTEXITCODE) { throw 'Unable to read Git HEAD' }
    $tree = git -C $repo rev-parse 'HEAD^{tree}'
    if ($LASTEXITCODE) { throw 'Unable to read Git tree' }
    git -C $repo diff --cached --quiet
    if ($LASTEXITCODE) { throw 'Index has staged changes or could not be read' }
} finally {
    $env:GIT_OPTIONAL_LOCKS = $previousOptionalLocks
}

function Hash($Path) {
    (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
$reviewBytes = [IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $Review).Path)
$actualReview = [Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($reviewBytes)).ToLowerInvariant()
if ($actualReview -ne $ReviewHash) { throw 'Review record SHA256 differs' }
$reviewed = [Text.Encoding]::UTF8.GetString($reviewBytes) | ConvertFrom-Json -AsHashtable
if ($reviewed.schema -ne 'D5BM standalone admission v2' -or
    $reviewed.decision -cne 'GO' -or -not $reviewed.reviewer -or $Case -cnotin $reviewed.cases -or
    $reviewed.head -ne $head -or $reviewed.tree -ne $tree -or
    $reviewed.index -ne (Hash $index) -or $reviewed.protected -ne (Hash $protectedPath) -or
    $reviewed.interpreter -ne (Hash $py)) {
    throw 'Independent standalone admission missing or mismatched'
}
$runtimeFiles = @(
    'python314.dll', 'vcruntime140.dll', 'vcruntime140_1.dll',
    'DLLs/_bz2.pyd', 'DLLs/_ctypes.pyd', 'DLLs/_hashlib.pyd', 'DLLs/_lzma.pyd', 'DLLs/_wmi.pyd',
    'DLLs/_zstd.pyd', 'DLLs/libcrypto-3.dll', 'DLLs/libffi-8.dll'
)

function Assert-Runtime {
    if ($reviewed.runtime.Count -ne $runtimeFiles.Count -or
        (Test-Path -LiteralPath "$pyRoot/python._pth","$pyRoot/python314._pth") -contains $true) {
        throw 'Reviewed CPython runtime or module path closure differs'
    }
    if ((Hash $py) -ne $reviewed.interpreter) { throw 'CPython executable changed' }
    foreach ($path in $runtimeFiles) {
        if ((Hash (Join-Path $pyRoot $path)) -ne $reviewed.runtime[$path]) {
            throw "Reviewed CPython runtime differs: $path"
        }
    }
}

$protected = (Get-Content -LiteralPath $protectedPath -Raw | ConvertFrom-Json).protected
$scriptDir = 'research/resource-retained-population'
$sourceFiles = @(
    "$scriptDir/d5bm_admit_component.ps1", "$scriptDir/d5bj_sampler.py",
    "$scriptDir/d5bm_pool.py", "$scriptDir/d5bm_server.py", "$scriptDir/d5bj_workers.py"
)
if ($Case -eq 'tags') {
    $method = 'd5bm_tags.py'
    $sourceFiles += @(
        'inspect_outpost_definitions.py', 'inventory_historical_saves.py', 'validate_mature_outposts.py',
        'analyze_structural_containment.py', 'analyze_manual_corpus.py', 'probe_manual_candidates.py',
        'probe_output_link_structure.py', 'archive_manual_corpus.py', 'validate_output_link.py'
    ) | ForEach-Object { "save-analysis/scripts/$_" }
} else {
    $method = 'd5bm_pump_probe.py'
    $sourceFiles += "$scriptDir/d5bm_pump_gate.py"
}
$sourceFiles += "$scriptDir/$method"
if ($reviewed.sources.Count -ne $sourceFiles.Count) { throw 'Review source closure differs' }
foreach ($path in $sourceFiles) {
    if ((Hash (Join-Path $repo $path)) -ne $reviewed.sources[$path]) {
        throw "Reviewed source differs: $path"
    }
}

function Read-Disk {
    @{C=([IO.DriveInfo]::new('C')).AvailableFreeSpace;D=([IO.DriveInfo]::new('D')).AvailableFreeSpace}
}

function Assert-Disk($space) {
    if ($space.C -lt 40000000000 -or $space.D -lt 40000000000) {
        throw "Caller disk floor failed (C=$($space.C) D=$($space.D))"
    }
}

function Assert-Protected {
    foreach ($record in $protected) {
        $item = Get-Item -LiteralPath $record.path
        if ($item.Length -ne $record.length -or (Hash $item.FullName) -ne $record.sha256) {
            throw "Protected source changed: $($record.path)"
        }
    }
    if ((Hash $index) -ne $reviewed.index) { throw 'Git index changed' }
    if (Get-Process -Name Starfield,sfse_loader -ErrorAction SilentlyContinue) { throw 'Unexpected game process' }
    Assert-Runtime
}
$before = Read-Disk
Assert-Disk $before
Assert-Protected
$attemptRoot = Join-Path $scratch "admission-attempts/$Attempt"
New-Item -ItemType Directory -Path $attemptRoot | Out-Null
$source = Join-Path $attemptRoot 'source'
foreach ($path in $sourceFiles) {
    $destination = Join-Path $source $path
    New-Item -ItemType Directory -Path (Split-Path $destination) -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $repo $path) -Destination $destination
    if ((Hash $destination) -ne $reviewed.sources[$path]) { throw "Staged review snapshot differs: $path" }
}
$argv = @('-I','-S','-B','-X','faulthandler', (Join-Path $source "$scriptDir/$method"), '--exe', "$game/Starfield.exe")
if ($Case -eq 'tags') { $argv += @('--esm', "$game/Data/Starfield.esm") }
else { $argv += @('--case', $Case) }
$record = @{
    time=(Get-Date -Format o); case=$Case; attempt=$Attempt; review=$ReviewHash
    reviewer=$reviewed.reviewer; head=$head; tree=$tree; index=$reviewed.index
    sources=$reviewed.sources; interpreter=$py; interpreterHash=$reviewed.interpreter
    runtime=$reviewed.runtime; argv=$argv; protected=$reviewed.protected; callerFree=$before
}
$record | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath "$attemptRoot/admission.json"
$info = [Diagnostics.ProcessStartInfo]::new($py)
$info.UseShellExecute = $false
$info.CreateNoWindow = $true
$info.WorkingDirectory = $source
$info.RedirectStandardOutput = $true
$info.RedirectStandardError = $true
foreach ($arg in $argv) { $info.ArgumentList.Add($arg) }
$child = [Diagnostics.Process]::new()
$child.StartInfo = $info
$out = $null
$err = $null
$output = $null
$errors = $null
$started = $false
$childId = $null
$stop = $null
$code = $null
$terminationFailure = $null
$failures = [ordered]@{}
try {
    $out = [IO.File]::Open("$attemptRoot/stdout.json", [IO.FileMode]::CreateNew)
    $err = [IO.File]::Open("$attemptRoot/stderr.txt", [IO.FileMode]::CreateNew)
    $started = $child.Start()
    if (-not $started) { throw 'Owned child failed to start' }
    $childId = $child.Id
    $output = $child.StandardOutput.BaseStream.CopyToAsync($out)
    $errors = $child.StandardError.BaseStream.CopyToAsync($err)
    $token = "$Attempt/$childId/$([guid]::NewGuid())"
    @{ pid=$childId; token=$token } | ConvertTo-Json | Set-Content -LiteralPath "$attemptRoot/owner.json"
    while (-not $child.WaitForExit(250)) {
        try { Assert-Disk (Read-Disk) } catch {
            $stop = $_.Exception.Message
            break
        }
        if (Test-Path -LiteralPath "$attemptRoot/stop.request" -PathType Leaf) {
            $request = Get-Content -LiteralPath "$attemptRoot/stop.request" -Raw
            $lines = $request -split '\r?\n', 3
            if ($lines.Count -ge 2 -and $lines[0] -ceq $token -and $lines[1].Trim()) {
                $stop = $lines[1].Trim()
                break
            }
        }
    }
} finally {
    try {
        if ($started) {
            if (-not $child.HasExited) {
                if (-not $stop) { $stop = 'supervisor exited before child completion' }
                try { $child.Kill() } catch {
                    if (-not $child.HasExited) { throw }
                }
            }
            $child.WaitForExit()
            $code = $child.ExitCode
            try { if ($output) { $output.GetAwaiter().GetResult() } }
            catch { $failures.stdoutDrain = $_.Exception.Message }
            try { if ($errors) { $errors.GetAwaiter().GetResult() } }
            catch { $failures.stderrDrain = $_.Exception.Message }
        }
    } catch {
        $terminationFailure = $_.Exception.Message
        throw
    } finally {
        try { if ($out) { $out.Dispose() } } catch { $failures.stdoutClose = $_.Exception.Message }
        try { if ($err) { $err.Dispose() } } catch { $failures.stderrClose = $_.Exception.Message }
        try { $child.Dispose() } catch { $failures.childClose = $_.Exception.Message }
        $post = @{
            time=(Get-Date -Format o); pid=$childId; exit=$code; explicitStop=$stop
            callerFree=$null; protectedMatches=$null; sourceMatches=$null
            terminationFailure=$terminationFailure; postflightFailures=$failures
        }
        try {
            $post.callerFree = Read-Disk
            Assert-Disk $post.callerFree
        } catch { $failures.disk = $_.Exception.Message }
        try {
            Assert-Protected
            $post.protectedMatches = $protected.Count
        } catch { $failures.protected = $_.Exception.Message }
        try {
            foreach ($path in $sourceFiles) {
                if ((Hash (Join-Path $source $path)) -ne $reviewed.sources[$path] -or
                    (Hash (Join-Path $repo $path)) -ne $reviewed.sources[$path]) {
                    throw "Source snapshot changed: $path"
                }
            }
            $post.sourceMatches = $sourceFiles.Count
        } catch { $failures.sources = $_.Exception.Message }
        foreach ($name in ('stdout.json','stderr.txt')) {
            try {
                if (Test-Path -LiteralPath "$attemptRoot/$name") { $post[$name] = Hash "$attemptRoot/$name" }
            } catch { $failures[$name] = $_.Exception.Message }
        }
        $post | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath "$attemptRoot/postflight.json"
        if ($failures.Count) { throw "Owned child postflight check failed. See $attemptRoot" }
    }
}
if ($stop -or $code -ne 0) { throw "Owned child stopped. See $attemptRoot" }
