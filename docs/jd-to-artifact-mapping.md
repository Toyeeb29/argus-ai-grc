# JD Requirement → Argus Artifact Mapping

How each recurring requirement from live GRC Engineer and AI Governance Specialist postings (researched July 2026) is evidenced in this repository. Use this table in applications and interviews.

## GRC Engineer requirements

| JD requirement (verbatim themes) | Where Argus proves it |
|---|---|
| "Write code, preferably Python, to automate evidence collection" | `src/evidence.py` — automated evidence pack with report, findings CSV, SoA |
| "Design and execute continuous control testing using automation/scripting" | `src/policy_engine.py` — declarative checks evaluated on every run/PR |
| "Embed compliance into CI/CD pipelines" | `.github/workflows/governance-gate.yml` — merge-blocking governance gate |
| "Audit readiness; accurate evidence collection; work with auditors" | `output/evidence_pack/` incl. SHA-256 `MANIFEST.json` for integrity |
| "Develop and maintain policies, standards, procedures" | `policies/` — AI AUP + Risk Management Standard, control-linked |
| "Translate complex technical requirements into clear, actionable controls" | `frameworks/controls.yaml` — legal articles → machine-testable predicates |
| "Lead risk assessments; drive remediation" | Findings register with severity + remediation guidance per control |
| "Vendor/third-party risk management with automation" | AGC-13 conditional vendor control + vendor fields in inventory |
| "Familiarity with SOC 2 / ISO 27001 / NIST control structures" | Catalog/SoA structure mirrors ISO Annex A + SoA methodology |

## AI Governance Specialist requirements

| JD requirement (verbatim themes) | Where Argus proves it |
|---|---|
| "Maintain enterprise AI system inventory, classification, risk-tiering" | `inventory/ai_systems.yaml` + `src/risk_tiering.py` |
| "EU AI Act obligations: provider vs deployer, risk categories" | Tiering engine implements Art. 5 / Annex III / Art. 50; role field drives AGC-15 |
| "Align with NIST AI RMF, ISO 42001, EU AI Act simultaneously" | Every control crosswalked to all three; `docs/framework-crosswalk.md` |
| "Statement of Applicability (ISO 42001)" | Auto-generated `statement_of_applicability.md` with justifications |
| "Model card templates / conformity documentation" | `src/model_card.py` — governance-grade cards generated per system |
| "Risk assessment templates, bias/explainability/privacy evaluation" | Data-governance controls AGC-04/05, DPIA control AGC-14 |
| "KRI monitoring dashboards, executive reporting" | `output/dashboard.html` — tier distribution, scores, findings register |
| "Update policies/playbooks as regulation evolves" | Versioned policy docs; catalog change = reviewable PR through the gate |
| "Post-market monitoring and incident reporting (Art. 72/73)" | Controls AGC-11/AGC-12 + monitoring fields in inventory |

## The differentiator

Most AI governance portfolios are documents. Most GRC portfolios are checklists. Argus is a **running system**: the same repo produces the legal analysis (tiering rationale citing articles), the engineering artifact (tested Python + CI), and the audit evidence (hashed packs). That intersection is exactly what both JDs are hiring for.
