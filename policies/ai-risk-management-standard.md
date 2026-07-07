# AI Risk Management Standard

**Document ID:** STD-AI-002 · **Version:** 1.0 · **Owner:** AI Governance Office · **Aligned to:** NIST AI RMF 1.0, ISO/IEC 42001:2023, EU AI Act

## 1. Purpose

Defines the mandatory process for identifying, assessing, treating, and monitoring AI risk across the system lifecycle. This standard implements POL-AI-001 §3.2.

## 2. Risk management process (mapped to NIST AI RMF)

**GOVERN.** The AI Governance Office maintains the control catalog (`frameworks/controls.yaml`), this standard, and the CI governance gate. Accountability for each AI system rests with the named system owner in the inventory.

**MAP.** At intake, every proposed AI system is documented in the inventory with purpose, context, data usage, autonomy level, and third-party dependencies. The tiering engine assigns an EU AI Act risk tier automatically; the AI Governance Office may raise (never lower) a tier based on context.

**MEASURE.** Applicable controls are evaluated continuously by the Argus policy engine. High-tier systems additionally require: bias/fairness evaluation (≤12 months old), accuracy metric tracking, adversarial/red-team testing for generative systems, and a DPIA where personal data is processed.

**MANAGE.** Findings are prioritized by severity (critical > high > medium > low). Critical findings block deployment via the CI gate and require remediation or an approved exception within 30 days. High findings must be remediated within 90 days. All findings live in the generated findings register and are reviewed monthly by the AI Risk Working Group.

## 3. Risk tiers and control intensity

| Tier (EU AI Act) | Examples | Governance intensity |
|---|---|---|
| Prohibited | Social scoring, manipulative systems | Must not be built or procured |
| High | Hiring, credit, essential services (Annex III) | Full control set, conformity assessment, EU database registration, quarterly review |
| Limited | Chatbots, generative content (Art. 50) | Transparency, logging, incident response, vendor controls; semi-annual review |
| Minimal | Internal analytics, spam filters | Inventory registration + vendor controls; annual review |

## 4. Review and escalation

The AI Risk Working Group meets monthly; the dashboard and findings register are standing inputs. Risk acceptance above medium severity requires CRO sign-off. This standard is reviewed annually or upon material regulatory change.
