# SPDX-License-Identifier: GPL-3.0-or-later
<#
Offline Windows qualification launcher. Reads installed Python and task-owned
code; copies a private runtime, provisions ACLs in a fresh ignored directory,
creates a disposable AppContainer without capabilities, runs an owned worker,
and deletes the profile. Preserves files/ACL receipts. Does not touch source
ACLs, accounts, game, saves, configuration or existing analysis state.
Requires Windows AppContainer APIs, PowerShell/.NET and existing CPython.
#>
param(
    [Parameter(Mandatory=$true)][string]$Destination,
    [Parameter(Mandatory=$true)][string]$Worker,
    [Parameter(Mandatory=$true)][string]$Inputs,
    [Parameter(Mandatory=$true)][string]$InputManifest,
    [Parameter(Mandatory=$true)][ValidatePattern('^[a-f0-9]{64}$')][string]$WorkerSha256,
    [string]$Python = 'C:/Users/User/AppData/Local/Python/pythoncore-3.14-64'
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path "$PSScriptRoot/../..").Path
$parent = (Resolve-Path "$root/.local-work/blinded-outpost-validation").Path
$dest = [IO.Path]::GetFullPath($Destination)
function Assert-NoReparse([string]$Path) {
    $current = [IO.Path]::GetFullPath($Path)
    while ($current) {
        $item = Get-Item -LiteralPath $current -Force
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse ancestor' }
        $current = [IO.Path]::GetDirectoryName($current)
    }
}
Assert-NoReparse $parent
Assert-NoReparse $Inputs
Assert-NoReparse $Worker
Assert-NoReparse $Python
Assert-NoReparse $InputManifest
if ((Get-FileHash -LiteralPath $Worker -Algorithm SHA256).Hash.ToLowerInvariant() -ne $WorkerSha256) {
    throw 'Worker hash'
}
$approved = Get-Content -LiteralPath $InputManifest -Raw | ConvertFrom-Json -AsHashtable
$provided = @(Get-ChildItem -LiteralPath $Inputs -Force)
if ($provided.Count -ne $approved.Count) { throw 'Input inventory count' }
foreach ($file in $provided) {
    if ($file.PSIsContainer -or $file.Name -eq 'worker.py' -or $file.Name -notmatch '^[a-zA-Z0-9_-]+\.(py|json)$' -or
        -not $approved.ContainsKey($file.Name)) { throw 'Input inventory path' }
    Assert-NoReparse $file.FullName
    if ((Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant() -ne $approved[$file.Name]) {
        throw 'Input inventory hash'
    }
}
if ([IO.Path]::GetDirectoryName($dest) -ne $parent -or (Test-Path -LiteralPath $dest)) {
    throw 'Fresh task-local destination required'
}
foreach ($drive in @('C:','D:')) {
    if (([IO.DriveInfo]::new($drive)).AvailableFreeSpace -lt 40000000000) { throw 'Disk floor' }
}
New-Item -ItemType Directory -Path $dest | Out-Null
$runtime = New-Item -ItemType Directory -Path "$dest/runtime"
$inputDir = New-Item -ItemType Directory -Path "$dest/input"
$outputDir = New-Item -ItemType Directory -Path "$dest/output"
foreach ($name in @('python.exe','python314.dll','vcruntime140.dll','vcruntime140_1.dll','LICENSE.txt')) {
    Copy-Item -LiteralPath "$Python/$name" -Destination $runtime.FullName
}
# Copy the installed stdlib, excluding external packages. Native extensions
# stay limited to hashing; no ctypes, socket or process extension is provisioned.
foreach ($item in (Get-ChildItem -LiteralPath "$Python/Lib")) {
    if ($item.Name -notin @('site-packages','__pycache__')) {
        Copy-Item -LiteralPath $item.FullName -Destination $runtime.FullName -Recurse
    }
}
Copy-Item -LiteralPath "$Python/DLLs/_hashlib.pyd" -Destination $runtime.FullName
Get-ChildItem -LiteralPath "$Python/DLLs" -Filter 'libcrypto*.dll' | Copy-Item -Destination $runtime.FullName
[IO.File]::WriteAllText("$runtime/python314._pth", ".`n../input`n", [Text.UTF8Encoding]::new($false))
Copy-Item -LiteralPath $Worker -Destination "$inputDir/worker.py"
foreach ($file in $provided) {
    if ($file.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse input' }
    Copy-Item -LiteralPath $file.FullName -Destination $inputDir.FullName
}
foreach ($file in $provided) {
    if ((Get-FileHash -LiteralPath (Join-Path $inputDir.FullName $file.Name) -Algorithm SHA256).Hash.ToLowerInvariant() -ne $approved[$file.Name]) {
        throw 'Provisioned input hash'
    }
}
if ((Get-FileHash -LiteralPath "$inputDir/worker.py" -Algorithm SHA256).Hash.ToLowerInvariant() -ne $WorkerSha256) {
    throw 'Provisioned worker hash'
}
$runtimePins = @{}
foreach ($file in (Get-ChildItem -LiteralPath $runtime.FullName -File -Recurse -Force)) {
    $runtimePins[[IO.Path]::GetRelativePath($runtime.FullName,$file.FullName).Replace('\','/')] = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
}
[IO.File]::WriteAllText("$dest/runtime-manifest.json", ($runtimePins | ConvertTo-Json), [Text.UTF8Encoding]::new($false))
Add-Type -Path "$PSScriptRoot/AppContainer.cs"
$profile = 'sor-blind-' + [Guid]::NewGuid().ToString('N')
$sid = [BlindContainer]::Create($profile)
try {
    # Grant this new SID only. The child has no inherited handles or capabilities.
    & icacls.exe $dest /grant "*$($sid):(RX)" | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'ACL root' }
    foreach ($path in @($runtime.FullName,$inputDir.FullName)) {
        & icacls.exe $path /grant "*$($sid):(OI)(CI)(RX)" /T /Q | Out-Null
        if ($LASTEXITCODE -ne 0) { throw 'ACL read' }
    }
    & icacls.exe $outputDir.FullName /grant "*$($sid):(OI)(CI)(M)" /T /Q | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'ACL output' }
    $executable = Join-Path $runtime.FullName 'python.exe'
    $exitCode = [BlindContainer]::Run($executable,'-I -S -B ../input/worker.py', $outputDir.FullName)
    $receipt = @{schema='sor-blind-boundary/1'; profile=$profile; sid=$sid; exit_code=$exitCode;
        token_verified=[BlindContainer]::TokenVerified;
        worker_sha256=$WorkerSha256; input_manifest_sha256=(Get-FileHash -LiteralPath $InputManifest -Algorithm SHA256).Hash.ToLowerInvariant();
        runtime_manifest_sha256=(Get-FileHash -LiteralPath "$dest/runtime-manifest.json" -Algorithm SHA256).Hash.ToLowerInvariant();
        mode='AppContainer'; profile_created=[BlindContainer]::ProfileCreated; profile_hresult=[BlindContainer]::ProfileResult;
        capabilities=@(); inherited_handles=$false; runtime=$runtime.FullName;
        input=$inputDir.FullName; output=$outputDir.FullName; cleanup='PENDING'}
} finally {
    [BlindContainer]::Delete($profile)
}
$receipt.cleanup = 'PROFILE_DELETED_OR_NOT_CREATED'
$receipt.acl = @(& icacls.exe $dest /T)
[IO.File]::WriteAllText("$dest/boundary.json", ($receipt | ConvertTo-Json -Depth 8), [Text.UTF8Encoding]::new($false))
@{exit_code=$exitCode; sid=$sid; cleanup=$receipt.cleanup; receipt="$dest/boundary.json"} | ConvertTo-Json
if ($exitCode -ne 0) { throw "Isolated worker failed: $exitCode" }
