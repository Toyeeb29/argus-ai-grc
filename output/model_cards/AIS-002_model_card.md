# Model Card — CreditSense Loan Scorer (AIS-002)

| | |
|---|---|
| **Owner** | risk-analytics@acme.example |
| **Business unit** | Financial Services |
| **Lifecycle stage** | production |
| **Model type** | XGBoost ensemble (in-house) |
| **EU AI Act role** | provider |
| **Risk tier** | **HIGH** |
| **Compliance score** | 57% (8/14 controls) |

## Intended purpose

Scores consumer creditworthiness for loan approval decisions.

## Risk classification rationale

High-risk under Annex III(5)(b) — creditworthiness evaluation of natural persons.

## Human oversight

- Documented: No
- Mechanism: _Not documented — open finding_

## Data governance

- Training data documented: Yes
- Provenance recorded: Yes
- Bias evaluation completed: No (date: n/a)

## Transparency & monitoring

- Users notified of AI interaction: Yes
- Logging enabled: Yes (retention: 24 months)
- Drift monitoring: No
- Incident response plan: Yes

## Third-party dependencies

- Vendor model: No
- Vendor risk assessment: n/a

## Open findings

- **CRITICAL** — AGC-02: Documented human oversight mechanism
- **CRITICAL** — AGC-03: No fully automated adverse decisions
- **HIGH** — AGC-05: Bias / fairness evaluation completed
- **HIGH** — AGC-11: Post-market drift monitoring
- **HIGH** — AGC-15: Registered in EU high-risk database
- **MEDIUM** — AGC-07: Model card published

---
_Generated automatically by Argus. Do not edit by hand — update the inventory and re-run._
