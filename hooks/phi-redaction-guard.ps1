# phi-redaction-guard.ps1 — enforce PHI redaction before agent prompts (Windows)
$ErrorActionPreference = "Stop"

if ($env:COMPLIANCE_PHI_REDACTION -and $env:COMPLIANCE_PHI_REDACTION -ne "required") {
    exit 0
}

$Root = if ($env:COMPLIANCE_AGENT_ROOT) { $env:COMPLIANCE_AGENT_ROOT } else {
    Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
}

try {
    python -c "import presidio_analyzer" 2>$null
    if ($LASTEXITCODE -ne 0) { throw "not installed" }
} catch {
    Write-Error "BLOCK: PHI redaction required but Presidio not installed. Run: pip install -r $Root\requirements.txt"
    exit 1
}

exit 0
