# Model Card — SupportGenie Customer Chatbot (AIS-003)

| | |
|---|---|
| **Owner** | cx-platform@acme.example |
| **Business unit** | Customer Experience |
| **Lifecycle stage** | production |
| **Model type** | GPT-4-class LLM (vendor API, RAG over product docs) |
| **EU AI Act role** | deployer |
| **Risk tier** | **LIMITED** |
| **Compliance score** | 86% (6/7 controls) |

## Intended purpose

LLM chatbot answering customer product questions on the website.

## Risk classification rationale

Art. 50 transparency obligations: system interacts with natural persons and/or generates synthetic content.

## Human oversight

- Documented: Yes
- Mechanism: Escalation to human agent on low confidence or user request

## Data governance

- Training data documented: No
- Provenance recorded: Yes
- Bias evaluation completed: Yes (date: 2026-02-10)

## Transparency & monitoring

- Users notified of AI interaction: No
- Logging enabled: Yes (retention: 6 months)
- Drift monitoring: Yes
- Incident response plan: Yes

## Third-party dependencies

- Vendor model: Yes (OpenAI (via Azure))
- Vendor risk assessment: completed

## Open findings

- **HIGH** — AGC-06: AI transparency notice to users

---
_Generated automatically by Argus. Do not edit by hand — update the inventory and re-run._
