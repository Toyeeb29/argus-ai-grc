# Framework Crosswalk — EU AI Act ↔ NIST AI RMF 1.0 ↔ ISO/IEC 42001:2023

The machine-readable version of this crosswalk lives in `frameworks/controls.yaml`; this document explains the mapping logic.

## How the three frameworks relate

**EU AI Act** is *law*: risk-tiered obligations enforced with penalties, binding on providers and deployers placing systems on the EU market. **NIST AI RMF** is a *voluntary risk framework*: four functions (GOVERN, MAP, MEASURE, MANAGE) describing how to manage AI risk. **ISO/IEC 42001** is a *certifiable management system standard*: it wraps AI governance in a PDCA management system with Annex A controls and a Statement of Applicability.

In practice: the AI Act tells you **what you must achieve**, NIST tells you **how to think about the risk work**, and ISO 42001 gives you **the management system to run it repeatably and certify it**. Argus operationalizes all three: tiering implements the Act, the control lifecycle follows RMF functions, and the generated SoA follows ISO 42001 methodology.

## Control-level mapping

| Argus | Requirement | EU AI Act | NIST AI RMF | ISO/IEC 42001 |
|---|---|---|---|---|
| AGC-01 | Inventory registration | Art. 16 / 26 | GOVERN 1.6, MAP 1.1 | A.4.2 |
| AGC-02 | Human oversight | Art. 14 | GOVERN 3.2, MANAGE 2.4 | A.9.2 |
| AGC-03 | No unreviewed automated decisions | Art. 14; GDPR Art. 22 | MANAGE 2.4 | A.9.2 |
| AGC-04 | Data governance | Art. 10 | MAP 2.1, MEASURE 2.2 | A.7.2, A.7.3 |
| AGC-05 | Bias evaluation | Art. 10(2)(f), 15 | MEASURE 2.11 | A.7.4 |
| AGC-06 | Transparency to users | Art. 50 | GOVERN 4.2, MAP 5.2 | A.8.2 |
| AGC-07 | Model card | Art. 11 + Annex IV | MAP 3.4 | A.8.2, A.8.3 |
| AGC-08 | Technical documentation | Art. 11, Annex IV | MAP 3.4 | A.6.2.7 |
| AGC-09 | Logging/traceability | Art. 12, 19 | MEASURE 2.1, MANAGE 4.1 | A.6.2.8 |
| AGC-10 | Log retention | Art. 19 | MANAGE 4.1 | A.6.2.8 |
| AGC-11 | Post-market monitoring | Art. 72 | MEASURE 3.1, MANAGE 4.1 | A.6.2.6 |
| AGC-12 | Incident response | Art. 73 | MANAGE 4.3, GOVERN 6.2 | A.10.4 |
| AGC-13 | Third-party/vendor risk | Art. 25 | GOVERN 6.1, MAP 4.1 | A.10.2, A.10.3 |
| AGC-14 | DPIA / fundamental rights | Art. 27 | MAP 3.1, MEASURE 2.10 | A.7.4 |
| AGC-15 | EU database registration | Art. 49, 71 | GOVERN 1.1 | A.2.3 |

## Notable mapping judgments

**Fraud detection carve-out.** Annex III(5)(b) covers creditworthiness scoring but explicitly excludes AI used to detect financial fraud — so FraudNet (AIS-004) tiers *minimal*, not *high*, despite operating on personal financial data. Encoding carve-outs correctly is where naive keyword-based classifiers fail.

**Provider vs deployer.** AGC-15 (EU database registration) is conditioned on `role: provider` — deployers of the same high-risk system carry Art. 26 obligations instead. The inventory schema captures the role precisely because obligations diverge.

**One requirement, three lenses.** Human oversight is a legal mandate (Art. 14), a MANAGE-function outcome (RMF), and an Annex A control (A.9.2). Argus stores the mapping once per control so any finding automatically cites all three — which is what an auditor, a regulator, and an engineer each need to see.
