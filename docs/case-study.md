# Case Study — Argus: Turning AI Governance from Documents into a Running System

## The problem

Enforcement of the EU AI Act is here, and most organizations' AI governance still lives in spreadsheets: inventories go stale within weeks, control checks happen quarterly at best, risk classification depends on whoever fills in the form, and audit evidence is assembled in a scramble when the auditor's email arrives. The result is governance that describes the organization as it was, not as it is — precisely the failure regulators penalize.

Security compliance solved this a decade ago with automation: continuous control monitoring, evidence pipelines, and checks wired into delivery. AI governance has the same shape of problem and almost none of the same tooling.

## The approach

Argus applies compliance-as-code discipline to AI governance end to end:

**Inventory as the source of truth.** Every AI system is a version-controlled YAML record capturing the attributes governance actually turns on: purpose, domain, provider/deployer role, personal-data use, autonomy, oversight, monitoring, third-party dependencies. Any change is a reviewable diff.

**Classification as law, not judgment calls.** The tiering engine implements the EU AI Act's actual structure — Art. 5 prohibited practices, Annex III high-risk domains, Art. 50 transparency triggers — including the details that catch people out: the engine fails closed on unrecognized inputs, and it encodes the Annex III(5)(b) carve-out that exempts financial-fraud detection from the credit-scoring high-risk category. Getting that carve-out right requires reading the regulation itself, not summaries of it.

**One catalog, three frameworks.** Each control is defined once as a machine-testable predicate and crosswalked to the EU AI Act article, NIST AI RMF subcategory, and ISO/IEC 42001 Annex A control it satisfies. A single finding automatically cites all three — what the regulator, the risk framework, and the auditor each need to see.

**Enforcement where change happens.** A GitHub Actions gate re-runs the full assessment on every pull request touching the inventory, catalog, or engine, and fails the build on critical findings. Governance stops being a calendar event and becomes a merge check.

**Evidence that proves itself.** Every run emits an assessment report, findings register, ISO 42001-style Statement of Applicability, and per-system model cards — sealed with a SHA-256 manifest so no artifact can be silently altered after generation.

## The result

On the demonstration inventory of five systems, Argus correctly tiers each one (including the fraud-detection carve-out), surfaces nine findings, and blocks the build over two critical ones: a credit-scoring model issuing fully automated adverse decisions with no documented human oversight — the exact failure mode Art. 14 and GDPR Art. 22 exist to prevent. The remediation shipped as a reviewed pull request: oversight documented, automated adverse decisions disabled, gate green, merged. The full cycle — violation caught, fix reviewed, evidence regenerated — is visible in the repository's history.

## An honest engineering note

The first version of the gate's unit test hard-coded the assumption that the demo credit scorer was broken; the remediation PR made that test fail. It was a data-coupled test — verifying fixture state instead of logic. It was refactored to assert against a synthetic non-compliant system, which is the correct design: tests should verify behavior, not depend on demo data staying broken. The bug and the fix are both in the commit history, deliberately.

## Design boundaries and next steps

The demo layer evaluates declared inventory attributes — appropriate for demonstrating the architecture, and honest about being self-attestation. The check interface (equals/exists/gte against a resolved path) was designed so those inputs swap for live collectors without touching the engine: AWS Config for logging state, MLflow for drift-monitor presence, GRC platform APIs (Vanta/Drata) for control status. Also on the roadmap: OSCAL export, GPAI model obligations (Art. 51+), and an intake questionnaire that writes inventory records directly.