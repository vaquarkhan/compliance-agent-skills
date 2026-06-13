# install.ps1 — install compliance-agent-skills toolkit with auto tool detection
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

$Python = $null
foreach ($candidate in @("python", "python3", "py")) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) {
        if ($candidate -eq "py") {
            $Python = @("py", "-3")
        } else {
            $Python = @($candidate)
        }
        break
    }
}

if (-not $Python) {
    Write-Error "Python 3.11+ required but not found in PATH"
    exit 1
}

Write-Host "==> Running install_toolkit.py"
& @Python "$Root\scripts\install_toolkit.py" @args
exit $LASTEXITCODE
