# Model Card — FraudNet Transaction Monitor (AIS-004)

| | |
|---|---|
| **Owner** | fraud-eng@acme.example |
| **Business unit** | Payments |
| **Lifecycle stage** | production |
| **Model type** | autoencoder anomaly detector (in-house) |
| **EU AI Act role** | provider |
| **Risk tier** | **MINIMAL** |
| **Compliance score** | 100% (1/1 controls) |

## Intended purpose

Flags anomalous transactions for fraud-team review in real time.

## Risk classification rationale

No Art. 5, Annex III, or Art. 50 triggers identified. Minimal-risk tier; voluntary codes of conduct encouraged (Art. 95).

## Human oversight

- Documented: Yes
- Mechanism: All flags routed to fraud analyst queue; no auto-blocking

## Data governance

- Training data documented: Yes
- Provenance recorded: Yes
- Bias evaluation completed: Yes (date: 2026-05-02)

## Transparency & monitoring

- Users notified of AI interaction: Yes
- Logging enabled: Yes (retention: 36 months)
- Drift monitoring: Yes
- Incident response plan: Yes

## Third-party dependencies

- Vendor model: No
- Vendor risk assessment: n/a

## Open findings

- None open.

---
_Generated automatically by Argus. Do not edit by hand — update the inventory and re-run._
