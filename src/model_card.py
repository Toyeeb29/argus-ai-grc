"""Model card generator — one governance-grade model card per AI system."""

from __future__ import annotations

from pathlib import Path


def write_model_cards(systems: list[dict], assessments: list[dict], out_dir: str | Path) -> list[Path]:
    out = Path(out_dir) / "model_cards"
    out.mkdir(parents=True, exist_ok=True)
    by_id = {a["system_id"]: a for a in assessments}
    paths = []
    for s in systems:
        a = by_id[s["id"]]
        path = out / f"{s['id']}_model_card.md"
        path.write_text(_card(s, a), encoding="utf-8")
        paths.append(path)
    return paths


def _yn(v) -> str:
    return "Yes" if v else "No"


def _card(s: dict, a: dict) -> str:
    findings = (
        "\n".join(f"- **{f['severity'].upper()}** — {f['control_id']}: {f['name']}"
                  for f in a["findings"])
        or "- None open."
    )
    return f"""# Model Card — {s['name']} ({s['id']})

| | |
|---|---|
| **Owner** | {s['owner']} |
| **Business unit** | {s['business_unit']} |
| **Lifecycle stage** | {s['lifecycle_stage']} |
| **Model type** | {s['model_type']} |
| **EU AI Act role** | {s['role']} |
| **Risk tier** | **{a['risk_tier'].upper()}** |
| **Compliance score** | {a['compliance_score']}% ({a['controls_passed']}/{a['controls_evaluated']} controls) |

## Intended purpose

{s['purpose']}

## Risk classification rationale

{a['tier_rationale']}

## Human oversight

- Documented: {_yn(s['human_oversight']['documented'])}
- Mechanism: {s['human_oversight']['mechanism'] or '_Not documented — open finding_'}

## Data governance

- Training data documented: {_yn(s['data_governance']['training_data_documented'])}
- Provenance recorded: {_yn(s['data_governance']['provenance_recorded'])}
- Bias evaluation completed: {_yn(s['data_governance']['bias_evaluation_completed'])} \
(date: {s['data_governance']['bias_evaluation_date'] or 'n/a'})

## Transparency & monitoring

- Users notified of AI interaction: {_yn(s['transparency']['users_notified_of_ai'])}
- Logging enabled: {_yn(s['monitoring']['logging_enabled'])} \
(retention: {s['monitoring']['log_retention_months']} months)
- Drift monitoring: {_yn(s['monitoring']['drift_monitoring'])}
- Incident response plan: {_yn(s['monitoring']['incident_response_plan'])}

## Third-party dependencies

- Vendor model: {_yn(s['third_party']['is_vendor_model'])}\
{f" ({s['third_party']['vendor']})" if s['third_party']['vendor'] else ''}
- Vendor risk assessment: {s['third_party']['vendor_risk_assessment'] or 'n/a'}

## Open findings

{findings}

---
_Generated automatically by Argus. Do not edit by hand — update the inventory and re-run._
"""
