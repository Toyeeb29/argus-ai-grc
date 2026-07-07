"""Static HTML compliance dashboard generator (no external dependencies)."""

from __future__ import annotations

from pathlib import Path

TIER_COLORS = {"prohibited": "#7f1d1d", "high": "#dc2626",
               "limited": "#d97706", "minimal": "#16a34a"}
SEV_COLORS = {"critical": "#7f1d1d", "high": "#dc2626", "medium": "#d97706", "low": "#64748b"}


def write_dashboard(report: dict, out_dir: str | Path) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "dashboard.html"
    path.write_text(_html(report), encoding="utf-8")
    return path


def _badge(text: str, color: str) -> str:
    return (f'<span style="background:{color};color:#fff;padding:2px 10px;'
            f'border-radius:999px;font-size:12px;font-weight:600">{text}</span>')


def _html(report: dict) -> str:
    s = report["summary"]
    tiles = "".join(
        f'<div class="tile"><div class="num">{v}</div><div class="lbl">{k}</div></div>'
        for k, v in [
            ("AI systems", s["systems_assessed"]),
            ("Avg compliance", f"{s['avg_compliance_score']}%"),
            ("Open findings", s["total_findings"]),
            ("Critical findings", s["critical_findings"]),
        ]
    )
    tier_rows = "".join(
        f"<tr><td>{_badge(t.upper(), TIER_COLORS[t])}</td><td>{n}</td></tr>"
        for t, n in sorted(s["tier_distribution"].items()))

    sys_rows = ""
    for a in report["assessments"]:
        color = "#16a34a" if a["compliance_score"] >= 90 else (
            "#d97706" if a["compliance_score"] >= 70 else "#dc2626")
        sys_rows += f"""
        <tr>
          <td><b>{a['system_id']}</b><br><span class="muted">{a['system_name']}</span></td>
          <td>{_badge(a['risk_tier'].upper(), TIER_COLORS[a['risk_tier']])}</td>
          <td><div class="bar"><div style="width:{a['compliance_score']}%;background:{color}"></div></div>
              {a['compliance_score']}% ({a['controls_passed']}/{a['controls_evaluated']})</td>
          <td>{len(a['findings'])}</td>
        </tr>"""

    finding_rows = "".join(
        f"<tr><td>{a['system_id']}</td><td>{f['control_id']}</td><td>{f['name']}</td>"
        f"<td>{_badge(f['severity'].upper(), SEV_COLORS[f['severity']])}</td>"
        f"<td class='muted'>{f['frameworks']['eu_ai_act']}</td></tr>"
        for a in report["assessments"] for f in a["findings"])

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Argus — AI Governance Dashboard</title>
<style>
  body{{font-family:-apple-system,Segoe UI,Roboto,sans-serif;background:#0f172a;color:#e2e8f0;
       margin:0;padding:32px}}
  h1{{font-size:22px}} h2{{font-size:16px;margin-top:32px;color:#94a3b8}}
  .muted{{color:#94a3b8;font-size:12px}}
  .tiles{{display:flex;gap:16px;flex-wrap:wrap}}
  .tile{{background:#1e293b;border-radius:12px;padding:20px 28px;min-width:140px}}
  .num{{font-size:30px;font-weight:700}} .lbl{{color:#94a3b8;font-size:12px;margin-top:4px}}
  table{{border-collapse:collapse;width:100%;margin-top:8px;background:#1e293b;border-radius:12px;overflow:hidden}}
  th,td{{text-align:left;padding:10px 14px;border-bottom:1px solid #334155;font-size:14px;vertical-align:top}}
  th{{color:#94a3b8;font-size:12px;text-transform:uppercase;letter-spacing:.05em}}
  .bar{{background:#334155;border-radius:999px;height:8px;width:160px;margin-bottom:4px}}
  .bar div{{height:8px;border-radius:999px}}
  footer{{margin-top:32px;color:#64748b;font-size:12px}}
</style></head><body>
<h1>Argus — AI Governance &amp; Compliance Dashboard</h1>
<p class="muted">Generated {report['generated_at']} · EU AI Act (2024/1689) · NIST AI RMF 1.0 · ISO/IEC 42001:2023</p>
<div class="tiles">{tiles}</div>

<h2>Risk tier distribution (EU AI Act)</h2>
<table><tr><th>Tier</th><th>Systems</th></tr>{tier_rows}</table>

<h2>System compliance posture</h2>
<table><tr><th>System</th><th>Risk tier</th><th>Compliance</th><th>Open findings</th></tr>{sys_rows}</table>

<h2>Open findings register</h2>
<table><tr><th>System</th><th>Control</th><th>Requirement</th><th>Severity</th><th>Legal basis</th></tr>
{finding_rows or '<tr><td colspan="5">No open findings 🎉</td></tr>'}</table>

<footer>Argus AI-GRC Engine — compliance-as-code demo. Evidence integrity: see evidence_pack/MANIFEST.json.</footer>
</body></html>"""
