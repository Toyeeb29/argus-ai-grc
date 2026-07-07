"""Audit-ready evidence pack generator.

Writes the assessment report + a Statement of Applicability to disk and
produces a SHA-256 hash manifest so auditors can verify evidence integrity
(chain of custody). Mirrors how GRC engineers automate evidence collection
for SOC 2 / ISO audits — applied here to AI governance.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
from pathlib import Path


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def write_evidence_pack(report: dict, controls: list[dict], out_dir: str | Path) -> Path:
    out = Path(out_dir)
    pack = out / "evidence_pack"
    pack.mkdir(parents=True, exist_ok=True)

    # 1. full machine-readable assessment
    report_path = pack / "assessment_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # 2. per-system finding registers (CSV — auditors love CSV)
    findings_path = pack / "findings_register.csv"
    rows = ["system_id,system_name,risk_tier,control_id,control_name,severity,eu_ai_act_ref"]
    for a in report["assessments"]:
        for f in a["findings"]:
            rows.append(",".join([
                a["system_id"], f'"{a["system_name"]}"', a["risk_tier"],
                f["control_id"], f'"{f["name"]}"', f["severity"],
                f'"{f["frameworks"]["eu_ai_act"]}"',
            ]))
    findings_path.write_text("\n".join(rows) + "\n", encoding="utf-8")

    # 3. Statement of Applicability (ISO/IEC 42001 style)
    soa_path = pack / "statement_of_applicability.md"
    soa_path.write_text(_soa_markdown(report, controls), encoding="utf-8")

    # 4. integrity manifest
    manifest = {
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "algorithm": "SHA-256",
        "files": {p.name: _sha256(p) for p in sorted(pack.glob("*")) if p.name != "MANIFEST.json"},
    }
    (pack / "MANIFEST.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return pack


def _soa_markdown(report: dict, controls: list[dict]) -> str:
    tiers_present = set(a["risk_tier"] for a in report["assessments"])
    lines = [
        "# Statement of Applicability — AI Management System",
        "",
        f"Generated: {report['generated_at']}  ",
        f"Scope: {report['summary']['systems_assessed']} AI systems in the Argus inventory  ",
        "Framework basis: ISO/IEC 42001:2023 Annex A, crosswalked to EU AI Act and NIST AI RMF 1.0",
        "",
        "| Control | Name | ISO/IEC 42001 | EU AI Act | NIST AI RMF | Applicable | Justification |",
        "|---|---|---|---|---|---|---|",
    ]
    for c in controls:
        applicable = bool(tiers_present.intersection(c["applies_to"]))
        justification = (
            f"Applies to tier(s): {', '.join(c['applies_to'])}" if applicable
            else "No in-scope system at an applicable risk tier"
        )
        lines.append(
            f"| {c['id']} | {c['name']} | {c['frameworks']['iso_42001']} | "
            f"{c['frameworks']['eu_ai_act']} | {c['frameworks']['nist_ai_rmf']} | "
            f"{'Yes' if applicable else 'No'} | {justification} |"
        )
    lines += [
        "",
        "_This SoA is regenerated automatically on every assessment run; manual edits are "
        "prohibited. Integrity is verifiable via MANIFEST.json (SHA-256)._",
    ]
    return "\n".join(lines) + "\n"
