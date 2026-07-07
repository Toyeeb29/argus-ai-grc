# Model Card — TalentRank Resume Screener (AIS-001)

| | |
|---|---|
| **Owner** | people-ops@acme.example |
| **Business unit** | Human Resources |
| **Lifecycle stage** | production |
| **Model type** | gradient-boosted classifier (in-house) |
| **EU AI Act role** | provider |
| **Risk tier** | **HIGH** |
| **Compliance score** | 93% (13/14 controls) |

## Intended purpose

Ranks inbound job applications and recommends candidates for interview.

## Risk classification rationale

High-risk under Annex III(4) — employment, worker management, access to self-employment.

## Human oversight

- Documented: Yes
- Mechanism: Recruiter reviews every ranked shortlist before outreach

## Data governance

- Training data documented: Yes
- Provenance recorded: Yes
- Bias evaluation completed: Yes (date: 2026-04-18)

## Transparency & monitoring

- Users notified of AI interaction: Yes
- Logging enabled: Yes (retention: 12 months)
- Drift monitoring: Yes
- Incident response plan: Yes

## Third-party dependencies

- Vendor model: No
- Vendor risk assessment: n/a

## Open findings

- **HIGH** — AGC-15: Registered in EU high-risk database

---
_Generated automatically by Argus. Do not edit by hand — update the inventory and re-run._
