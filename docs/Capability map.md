# Capability Map — What Argus Demonstrates and Where

AI governance sits at the intersection of two disciplines that rarely coexist in one place: compliance engineering (automation, evidence, CI/CD enforcement) and regulatory analysis (risk classification, framework interpretation, policy design). This map shows where each capability is implemented in the repository.

## Compliance engineering

| Problem in practice | How Argus solves it | Where |
|---|---|---|
| Control checks run quarterly and go stale | Continuous control testing on every change | `src/policy_engine.py` |
| Evidence assembled manually before audits | Automated evidence packs generated on every run | `src/evidence.py`, `output/evidence_pack/` |
| Evidence integrity can't be verified after the fact | SHA-256 manifest over every artifact (chain of custody) | `output/evidence_pack/MANIFEST.json` |
| Compliance is disconnected from delivery | Merge-blocking governance gate in CI | `.github/workflows/governance-gate.yml` |
| Legal requirements are ambiguous to engineers | Legal articles translated into machine-testable predicates | `frameworks/controls.yaml` |
| Findings lack ownership and remediation paths | Findings register with severity, owner, and framework-cited remediation | `output/evidence_pack/findings_register.csv` |
| Third-party AI enters unvetted | Conditional vendor-risk controls triggered by inventory attributes | Control AGC-13 |
| Governance logic is untested | 12-test pytest suite covering tiering, engine, and gate behavior | `tests/test_argus.py` |

## Regulatory analysis & AI governance

| Problem in practice | How Argus solves it | Where |
|---|---|---|
| Nobody knows what AI the organization runs | Version-controlled AI system inventory as the single source of truth | `inventory/ai_systems.yaml` |
| Risk classification is manual and inconsistent | Automated EU AI Act tiering (Art. 5 / Annex III / Art. 50), fail-closed | `src/risk_tiering.py` |
| Legal nuance gets lost in tooling | Provider/deployer role split; Annex III(5)(b) fraud carve-out encoded | `src/risk_tiering.py`, control AGC-15 |
| Three frameworks, three spreadsheets | Single control catalog crosswalked EU AI Act ↔ NIST AI RMF ↔ ISO 42001 | `frameworks/controls.yaml`, `docs/framework-crosswalk.md` |
| ISO 42001 SoA maintained by hand | Statement of Applicability generated from live assessment state | `output/evidence_pack/statement_of_applicability.md` |
| Model documentation drifts from reality | Model cards regenerated from the inventory on every run | `src/model_card.py`, `output/model_cards/` |
| Executives can't see AI risk posture | Dashboard with tier distribution, scores, and open findings | `output/dashboard.html` |
| Policy exists but isn't operationalized | Policy suite whose statements map to enforced controls | `policies/` |

## The design thesis

Most governance programs produce documents; most engineering teams produce systems. The failure mode is the hand-off between them — policies that nothing enforces, and pipelines that enforce nothing the law cares about. Argus is built on the premise that the hand-off should not exist: the same repository holds the legal reasoning (tiering rationale citing articles), the enforcement mechanism (tested Python running in CI), and the audit trail (hash-verified evidence). Change any one and the others update on the next run.