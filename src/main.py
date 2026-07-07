"""Argus CLI — run the full AI governance assessment pipeline.

Usage:
    python src/main.py assess            # full pipeline -> output/
    python src/main.py gate              # CI gate: exit 1 on critical findings
    python src/main.py gate --fail-on high
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from policy_engine import run_assessment, load_inventory, load_controls, gate
from evidence import write_evidence_pack
from model_card import write_model_cards
from dashboard import write_dashboard

ROOT = Path(__file__).resolve().parent.parent
INVENTORY = ROOT / "inventory" / "ai_systems.yaml"
CONTROLS = ROOT / "frameworks" / "controls.yaml"
OUTPUT = ROOT / "output"


def cmd_assess() -> int:
    report = run_assessment(INVENTORY, CONTROLS)
    controls = load_controls(CONTROLS)
    systems = load_inventory(INVENTORY)

    pack = write_evidence_pack(report, controls, OUTPUT)
    cards = write_model_cards(systems, report["assessments"], OUTPUT)
    dash = write_dashboard(report, OUTPUT)

    s = report["summary"]
    print("Argus assessment complete")
    print(f"  systems assessed .... {s['systems_assessed']}")
    print(f"  tier distribution ... {s['tier_distribution']}")
    print(f"  avg compliance ...... {s['avg_compliance_score']}%")
    print(f"  open findings ....... {s['total_findings']} ({s['critical_findings']} critical)")
    print(f"  evidence pack ....... {pack}")
    print(f"  model cards ......... {len(cards)} generated")
    print(f"  dashboard ........... {dash}")
    return 0


def cmd_gate(fail_on: str) -> int:
    report = run_assessment(INVENTORY, CONTROLS)
    ok, message = gate(report, fail_on=fail_on)
    print(message)
    return 0 if ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(prog="argus", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("assess", help="run full assessment + generate artifacts")
    g = sub.add_parser("gate", help="CI governance gate (nonzero exit on block)")
    g.add_argument("--fail-on", choices=["critical", "high"], default="critical")
    args = parser.parse_args()

    if args.command == "assess":
        return cmd_assess()
    return cmd_gate(args.fail_on)


if __name__ == "__main__":
    sys.exit(main())
