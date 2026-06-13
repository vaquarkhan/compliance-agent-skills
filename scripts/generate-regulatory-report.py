#!/usr/bin/env python3
"""Generate a Markdown regulatory findings report from structured YAML input."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("Install PyYAML: pip install pyyaml", file=sys.stderr)
    raise SystemExit(1)

ROOT = Path(__file__).resolve().parent.parent

POSTURE_LABELS = {
    "not_assessed": "Not assessed",
    "gaps_identified": "Gaps identified — remediation required",
    "controls_operating_effectively": "Controls operating effectively (point-in-time)",
}

SEVERITY_ORDER = ("critical", "high", "medium", "low", "informational")


def _load(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: root must be a mapping")
    return data


def _validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    report = data.get("report")
    if not isinstance(report, dict):
        return ["missing report section"]
    for key in ("id", "engagement_id", "framework", "period"):
        if key not in report:
            errors.append(f"report.{key} required")
    findings = data.get("findings", [])
    if not isinstance(findings, list):
        errors.append("findings must be a list")
    return errors


def _findings_table(findings: list[dict[str, Any]]) -> str:
    if not findings:
        return "_No findings recorded._\n"
    lines = [
        "| ID | Severity | Control | Observation | Recommendation | Status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in findings:
        lines.append(
            "| {id} | {severity} | {control} | {obs} | {rec} | {status} |".format(
                id=item.get("id", ""),
                severity=item.get("severity", ""),
                control=item.get("control_id", "") or item.get("control_title", ""),
                obs=(item.get("observation", "") or "").replace("|", "\\|")[:200],
                rec=(item.get("recommendation", "") or "").replace("|", "\\|")[:200],
                status=item.get("status", ""),
            )
        )
    return "\n".join(lines) + "\n"


def _remediation_table(remediation: list[dict[str, Any]]) -> str:
    if not remediation:
        return "_No remediation items._\n"
    lines = [
        "| Finding | Action | Owner | Due | Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for item in remediation:
        lines.append(
            "| {fid} | {action} | {owner} | {due} | {status} |".format(
                fid=item.get("finding_id", ""),
                action=(item.get("action", "") or "").replace("|", "\\|")[:120],
                owner=item.get("owner", ""),
                due=item.get("due_date") or "—",
                status=item.get("status", ""),
            )
        )
    return "\n".join(lines) + "\n"


def _executive_risks(summary: dict[str, Any]) -> str:
    risks = summary.get("top_risks") or []
    if not risks:
        return "_No top risks listed._\n"
    lines = []
    for risk in sorted(risks, key=lambda r: SEVERITY_ORDER.index(r.get("severity", "low"))):
        lines.append(
            f"- **{risk.get('id', 'R-?')}** ({risk.get('severity', 'unknown')}): "
            f"{risk.get('title', '')} — _{risk.get('control_ref', '')}_"
        )
    return "\n".join(lines) + "\n"


def render_markdown(data: dict[str, Any]) -> str:
    report = data["report"]
    summary = data.get("executive_summary") or {}
    scope = data.get("scope") or {}
    posture = summary.get("posture", "not_assessed")
    framework = report.get("framework") or ", ".join(report.get("frameworks") or [])

    period = report.get("period") or {}
    period_str = f"{period.get('start', '?')} – {period.get('end', '?')}"

    sections = [
        f"# Regulatory Findings Report — {report.get('title') or framework}",
        "",
        f"**Report ID:** {report.get('id')}  ",
        f"**Engagement:** {report.get('engagement_id')}  ",
        f"**Framework:** {framework}  ",
        f"**Period:** {period_str}  ",
        f"**Classification:** {report.get('classification', 'confidential')}  ",
        f"**Prepared:** {report.get('prepared_at', '—')} by {report.get('prepared_by', '—')}",
        "",
        "> **Disclaimer:** "
        + (data.get("disclaimer") or report.get("disclaimer") or "").strip(),
        "",
        "## 1. Executive summary",
        "",
        f"**Overall posture:** {POSTURE_LABELS.get(posture, posture)}",
        "",
        summary.get("narrative") or "_No executive narrative provided._",
        "",
        "### Top risks",
        "",
        _executive_risks(summary),
        "### Limitations",
        "",
    ]
    limitations = summary.get("limitations") or []
    sections.extend(
        [f"- {item}" for item in limitations] if limitations else ["_None documented._", ""]
    )

    sections.extend(
        [
            "## 2. Scope recap",
            "",
            "### In scope",
            "",
        ]
    )
    in_scope = scope.get("in_scope_systems") or []
    sections.extend([f"- {s}" for s in in_scope] if in_scope else ["_Not specified._", ""])

    sections.extend(["", "### Out of scope", ""])
    out_scope = scope.get("out_of_scope_systems") or []
    sections.extend([f"- {s}" for s in out_scope] if out_scope else ["_Not specified._", ""])

    sections.extend(["", "### Data classifications", ""])
    data_classes = scope.get("data_classes") or []
    sections.extend([f"- {c}" for c in data_classes] if data_classes else ["_Not specified._", ""])

    sections.extend(
        [
            "",
            "## 3. Findings detail",
            "",
            _findings_table(data.get("findings") or []),
            "## 4. Evidence index",
            "",
        ]
    )
    evidence = data.get("evidence_index") or {}
    artifact_ids = evidence.get("artifact_ids") or []
    if artifact_ids:
        sections.append(f"Manifest: `{evidence.get('manifest_path', '')}`")
        sections.append("")
        for aid in artifact_ids:
            sections.append(f"- `{aid}`")
        sections.append("")
    else:
        sections.append("_No evidence artifact IDs linked._\n")

    sections.extend(
        [
            "## 5. Remediation tracker",
            "",
            _remediation_table(data.get("remediation") or []),
        ]
    )

    methodology = data.get("methodology") or {}
    sections.extend(
        [
            "## 6. Methodology",
            "",
            f"- **Sampling:** {methodology.get('sampling_approach') or '—'}",
            f"- **Tools:** {', '.join(methodology.get('tools') or []) or '—'}",
            f"- **Redaction profile:** {methodology.get('redaction_profile', 'balanced')}",
            f"- **Deanonymize in report path:** {methodology.get('deanonymize_used', False)}",
            "",
            "## 7. Sign-off",
            "",
        ]
    )
    sign_off = data.get("sign_off") or {}
    for role in ("compliance_lead", "technical_lead"):
        entry = sign_off.get(role) or {}
        name = entry.get("name") or "—"
        role_label = entry.get("role") or "—"
        date = entry.get("date") or "pending"
        sections.append(f"- **{role.replace('_', ' ').title()}:** {name} ({role_label}) — {date}")
    sections.append("")
    return "\n".join(sections)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Markdown regulatory findings report")
    parser.add_argument(
        "input",
        nargs="?",
        default=str(ROOT / "templates/reports/regulatory-findings-report.yaml"),
        help="YAML input (findings, scope, remediation)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output Markdown path (default: stdout)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: {input_path} not found", file=sys.stderr)
        return 1

    data = _load(input_path)
    errors = _validate(data)
    if errors:
        print("Validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    markdown = render_markdown(data)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(markdown, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(markdown)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
