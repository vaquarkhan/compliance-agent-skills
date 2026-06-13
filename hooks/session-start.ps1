# session-start.ps1 — initialize compliance agent session context (Windows)
$ErrorActionPreference = "Continue"

if (-not $env:COMPLIANCE_AGENT_ROOT) {
    $env:COMPLIANCE_AGENT_ROOT = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
}
if (-not $env:COMPLIANCE_PHI_REDACTION) { $env:COMPLIANCE_PHI_REDACTION = "required" }
if (-not $env:COMPLIANCE_AUDIT_MODE) { $env:COMPLIANCE_AUDIT_MODE = "false" }
if (-not $env:COMPLIANCE_ENGAGEMENT_ID) {
    $env:COMPLIANCE_ENGAGEMENT_ID = "ENG-$(Get-Date -Format 'yyyyMMdd')-local"
}

Write-Host "[compliance-agent] Session started"
Write-Host "  root:          $($env:COMPLIANCE_AGENT_ROOT)"
Write-Host "  engagement:    $($env:COMPLIANCE_ENGAGEMENT_ID)"
Write-Host "  phi_redaction: $($env:COMPLIANCE_PHI_REDACTION)"
Write-Host "  audit_mode:    $($env:COMPLIANCE_AUDIT_MODE)"

if ($env:COMPLIANCE_PHI_REDACTION -eq "required") {
    try {
        python -c "import presidio_analyzer" 2>$null
    } catch {
        Write-Warning "Presidio not installed — run pip install -r requirements.txt"
    }
}

exit 0
