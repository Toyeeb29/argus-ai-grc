# Model Card — DevPilot Internal Code Assistant (AIS-005)

| | |
|---|---|
| **Owner** | platform-eng@acme.example |
| **Business unit** | Engineering |
| **Lifecycle stage** | pilot |
| **Model type** | Claude-class LLM (vendor API) |
| **EU AI Act role** | deployer |
| **Risk tier** | **LIMITED** |
| **Compliance score** | 83% (5/6 controls) |

## Intended purpose

IDE code-completion assistant for internal developers.

## Risk classification rationale

Art. 50 transparency obligations: system interacts with natural persons and/or generates synthetic content.

## Human oversight

- Documented: Yes
- Mechanism: Developer reviews all suggestions; mandatory code review

## Data governance

- Training data documented: No
- Provenance recorded: No
- Bias evaluation completed: No (date: n/a)

## Transparency & monitoring

- Users notified of AI interaction: Yes
- Logging enabled: Yes (retention: 3 months)
- Drift monitoring: No
- Incident response plan: Yes

## Third-party dependencies

- Vendor model: Yes (Anthropic)
- Vendor risk assessment: completed

## Open findings

- **MEDIUM** — AGC-07: Model card published

---
_Generated automatically by Argus. Do not edit by hand — update the inventory and re-run._
