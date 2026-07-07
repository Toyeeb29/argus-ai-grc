"""Policy-as-code control engine.

Loads the AI system inventory and control catalog, computes each system's
EU AI Act risk tier, evaluates every applicable control, and returns a
structured assessment (pass/fail findings with severity + remediation).
"""

from __future__ import annotations

import datetime as _dt
from pathlib import Path
from typing import Any

import yaml

from risk_tiering import classify

SEVERITY_ORDER = {"critical": 3, "high": 2, "medium": 1, "low": 0}


# ---------------------------------------------------------------- helpers
def _resolve(record: dict, dotted: str) -> Any:
    """Resolve 'a.b.c' path inside a nested dict; None if missing."""
    node: Any = record
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def _predicate_passes(record: dict, spec: dict) -> bool:
    value = _resolve(record, spec["field"])
    if "exists" in spec:
        return (value is not None) == spec["exists"]
    if "equals" in spec:
        return value == spec["equals"]
    if "gte" in spec:
        return isinstance(value, (int, float)) and value >= spec["gte"]
    raise ValueError(f"Unsupported check spec: {spec}")


# ---------------------------------------------------------------- loading
def load_yaml(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_inventory(path: str | Path) -> list[dict]:
    return load_yaml(path)["ai_systems"]


def load_controls(path: str | Path) -> list[dict]:
    return load_yaml(path)["controls"]


# ---------------------------------------------------------------- engine
def assess_system(system: dict, controls: list[dict]) -> dict:
    tier = classify(system)
    results = []
    for control in controls:
        if tier.tier not in control["applies_to"]:
            continue
        # conditional controls (e.g. vendor-only) are N/A when condition unmet
        condition = control.get("condition")
        if condition and not _predicate_passes(system, condition):
            results.append({"control_id": control["id"], "name": control["name"],
                            "status": "not_applicable", "severity": None,
                            "frameworks": control["frameworks"]})
            continue
        passed = _predicate_passes(system, control["check"])
        results.append({
            "control_id": control["id"],
            "name": control["name"],
            "status": "pass" if passed else "fail",
            "severity": None if passed else control["severity"],
            "frameworks": control["frameworks"],
            "remediation": None if passed else _remediation(control),
        })

    applicable = [r for r in results if r["status"] != "not_applicable"]
    passed_n = sum(1 for r in applicable if r["status"] == "pass")
    findings = [r for r in applicable if r["status"] == "fail"]
    findings.sort(key=lambda r: SEVERITY_ORDER[r["severity"]], reverse=True)

    return {
        "system_id": system["id"],
        "system_name": system["name"],
        "owner": system["owner"],
        "lifecycle_stage": system.get("lifecycle_stage"),
        "risk_tier": tier.tier,
        "tier_rationale": tier.rationale,
        "controls_evaluated": len(applicable),
        "controls_passed": passed_n,
        "compliance_score": round(100 * passed_n / len(applicable)) if applicable else 100,
        "findings": findings,
        "results": results,
    }


def _remediation(control: dict) -> str:
    return (f"Remediate to satisfy {control['frameworks']['eu_ai_act']}; "
            f"see also NIST AI RMF {control['frameworks']['nist_ai_rmf']} and "
            f"ISO/IEC 42001 {control['frameworks']['iso_42001']}.")


def run_assessment(inventory_path: str | Path, controls_path: str | Path) -> dict:
    systems = load_inventory(inventory_path)
    controls = load_controls(controls_path)
    assessments = [assess_system(s, controls) for s in systems]

    def worst(a: dict) -> int:
        sevs = [SEVERITY_ORDER[f["severity"]] for f in a["findings"]]
        return max(sevs, default=-1)

    return {
        "generated_at": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "framework_versions": {
            "eu_ai_act": "Regulation (EU) 2024/1689",
            "nist_ai_rmf": "AI RMF 1.0 (NIST AI 100-1)",
            "iso_42001": "ISO/IEC 42001:2023",
        },
        "summary": {
            "systems_assessed": len(assessments),
            "tier_distribution": _count(assessments, "risk_tier"),
            "total_findings": sum(len(a["findings"]) for a in assessments),
            "critical_findings": sum(
                1 for a in assessments for f in a["findings"] if f["severity"] == "critical"),
            "avg_compliance_score": round(
                sum(a["compliance_score"] for a in assessments) / max(len(assessments), 1)),
            "systems_with_critical_findings": [
                a["system_id"] for a in assessments if worst(a) == SEVERITY_ORDER["critical"]],
        },
        "assessments": assessments,
    }


def _count(items: list[dict], key: str) -> dict:
    out: dict[str, int] = {}
    for item in items:
        out[item[key]] = out.get(item[key], 0) + 1
    return out


def gate(report: dict, fail_on: str = "critical") -> tuple[bool, str]:
    """CI governance gate: returns (ok, message).

    fail_on='critical' blocks when any critical finding exists;
    fail_on='high' also blocks on high-severity findings.
    """
    threshold = SEVERITY_ORDER[fail_on]
    blocking = [
        (a["system_id"], f["control_id"], f["severity"])
        for a in report["assessments"]
        for f in a["findings"]
        if SEVERITY_ORDER[f["severity"]] >= threshold
    ]
    if blocking:
        lines = "\n".join(f"  - {s}: {c} ({sev})" for s, c, sev in blocking)
        return False, f"GOVERNANCE GATE FAILED — {len(blocking)} blocking finding(s):\n{lines}"
    return True, "Governance gate passed: no blocking findings."
