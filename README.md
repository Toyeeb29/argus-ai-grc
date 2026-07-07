# Argus — AI Governance Compliance-as-Code Engine

**A working GRC engineering project that treats AI governance the way modern teams treat infrastructure: as code, tested in CI, with audit-ready evidence.**

Argus takes a YAML inventory of an organization's AI systems, automatically classifies each one under the **EU AI Act** (prohibited / high / limited / minimal), evaluates a control catalog crosswalked to **EU AI Act ↔ NIST AI RMF 1.0 ↔ ISO/IEC 42001:2023**, and generates everything an auditor or regulator would ask for — with a CI gate that blocks deployment on critical governance failures.

## Why this project exists

AI governance has a delivery problem. Regulations like the EU AI Act demand risk classification, human oversight, and audit evidence — but in most organizations that work lives in spreadsheets and policy PDFs that go stale the day they're written. Meanwhile, the tooling that transformed security compliance, continuous control testing, automated evidence collection, checks embedded in CI/CD — rarely gets applied to AI systems at all.
Argus closes that gap: it treats the AI inventory, risk tiering, framework crosswalks, and model documentation as code-versioned, tested, and enforced on every change. Compliance logic you can run, not just documents you can read.

## What it does

```
inventory/ai_systems.yaml  ──►  risk_tiering.py (EU AI Act Art. 5 / Annex III / Art. 50)
frameworks/controls.yaml   ──►  policy_engine.py (continuous control testing)
                                      │
                                      ▼
        ┌─────────────────────────────────────────────────────┐
        │ output/                                             │
        │  ├─ dashboard.html            (compliance dashboard)│
        │  ├─ model_cards/*.md          (auto-generated)      │
        │  └─ evidence_pack/                                  │
        │     ├─ assessment_report.json                       │
        │     ├─ findings_register.csv                        │
        │     ├─ statement_of_applicability.md  (ISO 42001)   │
        │     └─ MANIFEST.json          (SHA-256 integrity)   │
        └─────────────────────────────────────────────────────┘
                                      │
                        .github/workflows/governance-gate.yml
                        (CI fails on critical findings)
```

## Quick start

```bash
pip install -r requirements.txt
pytest tests/ -v                      # 12 unit tests
python src/main.py assess             # full pipeline -> output/
python src/main.py gate               # CI gate (exit 1 on critical findings)
open output/dashboard.html
```

## Key design decisions

**Inventory as code.** The AI registry is version-controlled YAML — every change is a reviewable diff, and governance runs on every PR that touches it. This is the "single source of truth" pattern AI governance JDs describe, implemented the way GRC engineers actually build it.

**Fail-closed risk tiering.** An unrecognized prohibited-practice key classifies as *prohibited*, not *minimal*. Governance systems should fail safe.

**Conditional controls.** Vendor-risk and DPIA controls apply only when their trigger condition is met (vendor model / personal data), producing honest N/A results instead of noise — mirroring how a real SoA justifies exclusions.

**Evidence integrity.** Every evidence pack ships with a SHA-256 manifest so auditors can verify nothing was altered after generation — chain-of-custody thinking borrowed from SOC 2 evidence automation.

**The gate is the point.** `python src/main.py gate` returns a nonzero exit code when a high-risk system has a critical control failure. Wire that into CI and AI compliance stops being a quarterly spreadsheet exercise and becomes a merge-blocking check.

## Sample inventory (intentionally imperfect)

The five demo systems include realistic gaps: a resume screener missing EU database registration, a credit scorer with **fully automated adverse decisions** (critical finding — blocks CI), a chatbot that doesn't tell users it's a bot (Art. 50), a compliant fraud detector (demonstrating the Annex III(5)(b) fraud carve-out), and a minimal-governance internal code assistant.

## Repository layout

```
inventory/     AI system registry (source of truth)
frameworks/    machine-testable control catalog + 3-framework crosswalk
src/           tiering engine, policy engine, evidence, model cards, dashboard
tests/         pytest suite (tiering logic, engine behavior, gate)
policies/      AI Acceptable Use Policy, AI Risk Management Standard
docs/          framework crosswalk, JD-to-artifact mapping, case study
.github/       CI governance gate workflow
output/        generated artifacts (committed here for demo purposes)
```

## Frameworks referenced

EU AI Act (Regulation (EU) 2024/1689) · NIST AI RMF 1.0 (NIST AI 100-1) · ISO/IEC 42001:2023 · GDPR Art. 22 (automated decisions)

## Roadmap

Live cloud evidence collectors (AWS Config / Azure Policy) · GRC platform sync (Vanta/Drata API) · OSCAL export · risk-tier questionnaire intake form · GPAI model obligations (Art. 51+)

---
*Built by Toyeeb Atanda as a portfolio project demonstrating GRC engineering and AI governance. Sample data is fictional.*
