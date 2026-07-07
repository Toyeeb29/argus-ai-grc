"""Unit tests for the Argus AI-GRC engine (pytest)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from risk_tiering import classify  # noqa: E402
from policy_engine import (run_assessment, assess_system, load_controls,
                           gate, _resolve)  # noqa: E402

INVENTORY = ROOT / "inventory" / "ai_systems.yaml"
CONTROLS = ROOT / "frameworks" / "controls.yaml"


def _base_system(**over):
    s = {
        "id": "T-1", "name": "t", "owner": "t@t", "business_unit": "t",
        "purpose": "t", "model_type": "t", "role": "provider",
        "lifecycle_stage": "production", "domain": "internal_productivity",
        "interacts_with_humans": False, "generates_synthetic_content": False,
        "uses_personal_data": False, "automated_decision_no_human_review": False,
        "prohibited_practice": "none",
        "human_oversight": {"documented": True, "mechanism": "x"},
        "data_governance": {"training_data_documented": True, "provenance_recorded": True,
                            "bias_evaluation_completed": True, "bias_evaluation_date": "2026-01-01"},
        "transparency": {"users_notified_of_ai": True, "model_card_published": True},
        "robustness": {"accuracy_metrics_tracked": True, "adversarial_testing": True},
        "monitoring": {"logging_enabled": True, "log_retention_months": 12,
                       "drift_monitoring": True, "incident_response_plan": True},
        "third_party": {"is_vendor_model": False, "vendor": None, "vendor_risk_assessment": None},
        "documentation": {"technical_documentation": True, "dpia_completed": True,
                          "registered_in_eu_database": True},
    }
    s.update(over)
    return s


# ---------------- risk tiering (EU AI Act) ----------------
def test_prohibited_practice_is_prohibited():
    assert classify(_base_system(prohibited_practice="social_scoring")).tier == "prohibited"


def test_unknown_prohibited_practice_fails_closed():
    assert classify(_base_system(prohibited_practice="mystery")).tier == "prohibited"


def test_employment_domain_is_high_risk():
    r = classify(_base_system(domain="employment"))
    assert r.tier == "high" and "Annex III(4)" in r.rationale


def test_credit_scoring_is_high_risk():
    assert classify(_base_system(domain="credit_scoring")).tier == "high"


def test_chatbot_is_limited_risk():
    r = classify(_base_system(domain="customer_service", interacts_with_humans=True,
                              generates_synthetic_content=True))
    assert r.tier == "limited" and "Art. 50" in r.rationale


def test_backoffice_model_is_minimal():
    assert classify(_base_system()).tier == "minimal"


# ---------------- policy engine ----------------
def test_resolve_dotted_paths():
    assert _resolve({"a": {"b": {"c": 5}}}, "a.b.c") == 5
    assert _resolve({"a": {}}, "a.b.c") is None


def test_compliant_high_risk_system_scores_100():
    controls = load_controls(CONTROLS)
    a = assess_system(_base_system(domain="employment", uses_personal_data=True), controls)
    assert a["risk_tier"] == "high"
    assert a["compliance_score"] == 100
    assert a["findings"] == []


def test_missing_oversight_creates_critical_finding():
    controls = load_controls(CONTROLS)
    sys_ = _base_system(domain="employment",
                        human_oversight={"documented": False, "mechanism": None})
    a = assess_system(sys_, controls)
    ids = {f["control_id"]: f["severity"] for f in a["findings"]}
    assert ids.get("AGC-02") == "critical"


def test_vendor_control_na_for_inhouse_models():
    controls = load_controls(CONTROLS)
    a = assess_system(_base_system(domain="employment"), controls)
    vendor = next(r for r in a["results"] if r["control_id"] == "AGC-13")
    assert vendor["status"] == "not_applicable"


# ---------------- full pipeline + gate ----------------
def test_full_assessment_runs_on_sample_inventory():
    report = run_assessment(INVENTORY, CONTROLS)
    assert report["summary"]["systems_assessed"] == 5
    tiers = report["summary"]["tier_distribution"]
    assert tiers.get("high") == 2          # TalentRank + CreditSense
    assert tiers.get("limited") == 2       # SupportGenie + DevPilot
    assert tiers.get("minimal") == 1       # FraudNet (carve-out)


def test_gate_blocks_on_critical_findings():
    controls = load_controls(CONTROLS)
    bad = _base_system(domain="employment",
                       human_oversight={"documented": False, "mechanism": None})
    report = {"assessments": [assess_system(bad, controls)]}
    ok, msg = gate(report, fail_on="critical")
    assert ok is False
    assert "AGC-02" in msg
