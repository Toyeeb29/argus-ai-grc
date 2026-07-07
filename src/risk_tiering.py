"""EU AI Act risk-tiering engine.

Classifies each AI system in the inventory into one of four tiers:
  prohibited > high > limited > minimal

Logic mirrors the EU AI Act:
  - Art. 5   : prohibited practices (social scoring, manipulation, etc.)
  - Annex III: high-risk domains (employment, credit, education, ...)
  - Art. 50  : transparency-tier systems (human interaction, synthetic content)
  - everything else: minimal risk
"""

from __future__ import annotations

from dataclasses import dataclass

PROHIBITED_PRACTICES = {
    "social_scoring",
    "subliminal_manipulation",
    "exploitation_of_vulnerabilities",
    "realtime_remote_biometric_id_public",
    "emotion_recognition_workplace_education",
    "untargeted_facial_scraping",
    "predictive_policing_profiling",
}

# Annex III high-risk domains (simplified canonical keys)
ANNEX_III_DOMAINS = {
    "employment": "Annex III(4) — employment, worker management, access to self-employment",
    "credit_scoring": "Annex III(5)(b) — creditworthiness evaluation of natural persons",
    "education": "Annex III(3) — education and vocational training",
    "essential_services": "Annex III(5) — access to essential private/public services",
    "law_enforcement": "Annex III(6) — law enforcement",
    "migration_border": "Annex III(7) — migration, asylum, border control",
    "justice_democracy": "Annex III(8) — administration of justice, democratic processes",
    "biometric_identification": "Annex III(1) — biometric identification/categorisation",
    "critical_infrastructure": "Annex III(2) — critical infrastructure safety components",
    "medical": "Annex II/III — medical devices and health",
}


@dataclass
class TierResult:
    tier: str          # prohibited | high | limited | minimal
    rationale: str     # human-readable legal basis


def classify(system: dict) -> TierResult:
    """Return the EU AI Act risk tier for one inventory record."""
    practice = system.get("prohibited_practice", "none")
    if practice and practice != "none":
        if practice in PROHIBITED_PRACTICES:
            return TierResult(
                "prohibited",
                f"Art. 5 prohibited practice: {practice}. Deployment must not proceed.",
            )
        return TierResult(
            "prohibited",
            f"Declared prohibited practice '{practice}' (unrecognized key — fail closed).",
        )

    domain = system.get("domain", "")
    if domain in ANNEX_III_DOMAINS:
        return TierResult(
            "high",
            f"High-risk under {ANNEX_III_DOMAINS[domain]}.",
        )

    # Fraud detection for financial crime is explicitly carved OUT of Annex III(5)(b),
    # but transparency/limited obligations may still apply.
    if system.get("interacts_with_humans") or system.get("generates_synthetic_content"):
        return TierResult(
            "limited",
            "Art. 50 transparency obligations: system interacts with natural persons "
            "and/or generates synthetic content.",
        )

    return TierResult(
        "minimal",
        "No Art. 5, Annex III, or Art. 50 triggers identified. Minimal-risk tier; "
        "voluntary codes of conduct encouraged (Art. 95).",
    )
