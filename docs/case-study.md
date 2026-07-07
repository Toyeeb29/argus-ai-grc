# Case Study — How to Present Argus in Applications and Interviews

## The 30-second pitch

"I built Argus, a compliance-as-code engine for AI governance. It takes a version-controlled inventory of AI systems, automatically risk-tiers each one under the EU AI Act, runs continuous control tests against a catalog crosswalked to NIST AI RMF and ISO 42001, and generates audit-ready evidence — model cards, a Statement of Applicability, a findings register with SHA-256 integrity hashes — plus a CI gate that blocks deployment when a high-risk system has a critical governance failure. Compliance goes from a quarterly spreadsheet to a merge-blocking check."

## STAR story for interviews

**Situation.** Organizations face EU AI Act enforcement with AI governance run in spreadsheets: inventories go stale, control checks are manual and quarterly, and evidence is assembled in a panic before audits.

**Task.** Demonstrate that AI governance can be run like modern security engineering — continuous, automated, and embedded in the delivery pipeline — while staying legally precise about provider/deployer roles, Annex III scope, and framework crosswalks.

**Action.** Designed a YAML schema capturing the governance-relevant attributes of an AI system; implemented an EU AI Act tiering engine (including fail-closed handling and the Annex III fraud carve-out); built a declarative policy engine with conditional controls; automated evidence packs with hash manifests; generated model cards, SoA, and an executive dashboard; wired a GitHub Actions gate that fails builds on critical findings; covered the logic with 12 unit tests.

**Result.** A governance assessment that runs in seconds on every pull request instead of quarterly. In the demo inventory it correctly tiers 5 systems, surfaces 9 findings including two critical (a credit scorer making fully automated adverse decisions with no documented human oversight) and blocks it in CI with exit code 1 — precisely the failure mode Art. 14 / GDPR Art. 22 exist to prevent.

## Anticipated interview questions

**"Why fail-closed tiering?"** A governance system that defaults to 'minimal risk' on bad input silently under-governs. Argus classifies unknown prohibited-practice values as prohibited — the reviewer must resolve it. Same philosophy as deny-by-default firewall rules.

**"Isn't checking YAML fields self-attestation?"** Yes — deliberately, for the demo layer. The engine's check interface (`equals`/`exists`/`gte` on a resolved path) is designed so field sources can be swapped for live collectors: an AWS Config query for logging status, an MLflow API call for drift-monitor presence. The roadmap names those; the architecture already supports them.

**"How would this scale to 500 models?"** The inventory becomes an API-backed registry rather than one file; the engine already treats records as dicts, so the swap is an I/O change. Tiering and controls are O(n) and stateless — trivially parallelizable. The real scaling problem is organizational (ownership hygiene), which the schema addresses with mandatory owner fields.

**"What did you get wrong initially?"** Worth answering honestly with something real, e.g.: treating the fraud detector as high-risk until reading Annex III(5)(b)'s carve-out closely — a good example of why governance engineers must read primary sources, not vendor summaries.

## Where to publish

Push to GitHub with the Actions workflow enabled so the governance gate visibly runs (and fails) on PRs — a red X on a demo PR titled "Deploy credit scorer without human review" is a screenshot that does more than any bullet point. Post the dashboard screenshot + 30-second pitch on LinkedIn; write the crosswalk doc up as an article.
