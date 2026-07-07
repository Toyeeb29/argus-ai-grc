# AI Acceptable Use Policy

**Document ID:** POL-AI-001 · **Version:** 1.2 · **Owner:** AI Governance Office · **Review cycle:** Annual

## 1. Purpose

This policy defines how employees, contractors, and systems at Acme may develop, procure, and use artificial intelligence. It operationalizes our obligations under the EU AI Act (Regulation (EU) 2024/1689), NIST AI RMF 1.0, and our ISO/IEC 42001 AI management system.

## 2. Scope

All AI systems developed, deployed, procured, or materially modified by Acme, including third-party AI services and generative-AI tools, across all business units and lifecycle stages.

## 3. Policy statements

**3.1 Registration before deployment.** Every AI system must be registered in the Argus AI inventory (`inventory/ai_systems.yaml`) and assigned a risk tier before production use. Unregistered AI use is a policy violation.

**3.2 Risk tiering.** Systems are classified via the automated EU AI Act tiering engine (prohibited / high / limited / minimal). Prohibited-tier use cases must not be built or procured. High-tier systems require the full control set in the Argus catalog before go-live.

**3.3 Human oversight.** High-risk systems must have a documented, tested human-oversight mechanism. No decision with legal or similarly significant effect on a person may be fully automated.

**3.4 Data governance.** Training and evaluation data for high-risk systems must have documented provenance, suitability assessment, and a bias evaluation refreshed at least every 12 months.

**3.5 Transparency.** Users must be clearly informed when they interact with an AI system or consume AI-generated content (EU AI Act Art. 50).

**3.6 Third-party AI.** Vendor AI models and services require a completed vendor AI risk assessment before integration, and contracts must address data use, sub-processing, and incident notification.

**3.7 Generative AI use by staff.** Approved tools only; no confidential, personal, or client data in unapproved tools; all AI-generated code and content must be human-reviewed before use.

**3.8 Monitoring and incidents.** Production AI systems require logging (Art. 12), drift monitoring, and coverage in the AI incident response plan. Serious incidents are reportable per Art. 73 timelines.

**3.9 Continuous compliance.** Controls are verified automatically by the Argus policy engine on every change (CI governance gate). Critical findings block deployment.

## 4. Roles and responsibilities

The AI Governance Office owns this policy and the control catalog. System owners maintain inventory accuracy and remediate findings. Engineering embeds the governance gate in CI/CD. Legal advises on regulatory classification. Internal Audit verifies evidence integrity via the SHA-256 manifest.

## 5. Exceptions

Exceptions require written approval from the AI Governance Office and a compensating-control plan, recorded in the risk register with an expiry date not exceeding 6 months.

## 6. Enforcement

Violations may result in system decommissioning, revocation of tool access, and disciplinary action per the employee handbook.
