# bootstrap.ps1 — one-command setup for compliance-agent-skills (Windows)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

Write-Host "==> compliance-agent-skills bootstrap"
Write-Host "    Root: $Root"

$InstallScript = Join-Path $Root "scripts\install.ps1"
if (-not (Test-Path $InstallScript)) {
    Write-Error "scripts/install.ps1 not found"
    exit 1
}

& $InstallScript @args
