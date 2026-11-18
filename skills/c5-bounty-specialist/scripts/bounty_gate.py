#!/usr/bin/env python3
"""Deterministic C5-REAL Bug Bounty Eligibility & EV Gate (stdlib-only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

REQUIRED_BOOL_GATES = (
    "asset_in_scope",
    "impact_in_scope",
    "onchain_or_commit_verified",
    "silicon_poc_passes",
    "uses_mocks",
    "algebraic_invariant_verified",
    "self_inflicted_only",
    "admin_recovery_excluded_by_rules",
    "patch_regression_free",
    "public_remote_clean",
)


def evaluate_receipt(data: dict[str, Any]) -> dict[str, Any]:
    missing = [k for k in REQUIRED_BOOL_GATES if not isinstance(data.get(k), bool)]
    rea_ids = data.get("rea_evidence_ids", [])
    if not isinstance(rea_ids, list) or not all(isinstance(x, str) and x.startswith("ev_") for x in rea_ids):
        missing.append("rea_evidence_ids(list[ev_*])")

    if missing:
        return {
            "status": "BLOCKED_INCOMPLETE_EVIDENCE",
            "eligible_for_paid_bounty": False,
            "missing_or_invalid_fields": missing,
        }

    if not data["algebraic_invariant_verified"] or not data["silicon_poc_passes"]:
        verdict = "DROP_FALSIFIED"
        eligible = False
    elif not data["public_remote_clean"]:
        verdict = "BLOCKED_EMBARGO_VIOLATION"
        eligible = False
    elif data.get("is_doc_drift_only") is True:
        verdict = "REDIRECT_DOC_DRIFT_PR"
        eligible = False
    else:
        disqualifiers: list[str] = []
        if not data["asset_in_scope"]:
            disqualifiers.append("asset_out_of_scope")
        if not data["impact_in_scope"]:
            disqualifiers.append("impact_out_of_scope")
        if not data["onchain_or_commit_verified"]:
            disqualifiers.append("unverified_target_version")
        if data["uses_mocks"]:
            disqualifiers.append("violates_no_mock_policy")
        if data["self_inflicted_only"]:
            disqualifiers.append("self_inflicted_without_third_party_loss")
        if data["admin_recovery_excluded_by_rules"]:
            disqualifiers.append("recoverable_by_privileged_role_excluded")
        if not data["patch_regression_free"]:
            disqualifiers.append("patch_introduces_regression")

        payout_usd = float(data.get("estimated_payout_usd", 0.0))
        p_accept = float(data.get("acceptance_probability", 0.0))
        submission_fee_usd = float(data.get("pay_to_submit_fee_usd", 0.0))
        expected_value_usd = round(p_accept * payout_usd - submission_fee_usd, 2)

        if disqualifiers or expected_value_usd <= 0.0:
            if expected_value_usd <= 0.0 and not disqualifiers:
                disqualifiers.append("non_positive_expected_value")
            return {
                "status": "REDIRECT_PRIVATE_GHSA",
                "eligible_for_paid_bounty": False,
                "expected_value_usd": expected_value_usd,
                "disqualifiers": disqualifiers,
                "rea_evidence_count": len(rea_ids),
            }

        return {
            "status": "SUBMIT_BOUNTY",
            "eligible_for_paid_bounty": True,
            "expected_value_usd": expected_value_usd,
            "disqualifiers": [],
            "rea_evidence_count": len(rea_ids),
        }

    return {
        "status": verdict,
        "eligible_for_paid_bounty": eligible,
        "rea_evidence_count": len(rea_ids),
    }


def run_selftest() -> int:
    # Case 1: Valid paid bounty (all gates pass, no mocks, positive EV)
    valid = {
        "asset_in_scope": True,
        "impact_in_scope": True,
        "onchain_or_commit_verified": True,
        "silicon_poc_passes": True,
        "uses_mocks": False,
        "algebraic_invariant_verified": True,
        "self_inflicted_only": False,
        "admin_recovery_excluded_by_rules": False,
        "patch_regression_free": True,
        "public_remote_clean": True,
        "rea_evidence_ids": ["ev_0123456789abcdef"],
        "estimated_payout_usd": 50000.0,
        "acceptance_probability": 0.85,
        "pay_to_submit_fee_usd": 0.0,
    }
    r1 = evaluate_receipt(valid)
    assert r1["status"] == "SUBMIT_BOUNTY" and r1["eligible_for_paid_bounty"] is True, r1

    # Case 2: Real code bug but Pay-to-Submit + Primacy-of-Rules exclusion -> REDIRECT_PRIVATE_GHSA (CV-IBC-01 archetype)
    ghsa_case = dict(valid, self_inflicted_only=True, admin_recovery_excluded_by_rules=True, pay_to_submit_fee_usd=500.0, acceptance_probability=0.05)
    r2 = evaluate_receipt(ghsa_case)
    assert r2["status"] == "REDIRECT_PRIVATE_GHSA" and r2["eligible_for_paid_bounty"] is False, r2

    # Case 3: Falsified algebraic claim -> DROP_FALSIFIED (CV-IBC-02 archetype)
    falsified = dict(valid, algebraic_invariant_verified=False)
    r3 = evaluate_receipt(falsified)
    assert r3["status"] == "DROP_FALSIFIED" and r3["eligible_for_paid_bounty"] is False, r3

    print(json.dumps({"selftest": "PASS", "cases_verified": [r1["status"], r2["status"], r3["status"]]}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true", help="Run deterministic self-tests")
    parser.add_argument("--evaluate", type=Path, help="Evaluate a bounty gate receipt JSON file")
    args = parser.parse_args()

    if args.selftest:
        return run_selftest()
    if args.evaluate:
        payload = json.loads(args.evaluate.read_text(encoding="utf-8"))
        out = evaluate_receipt(payload)
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0 if out["status"] in {"SUBMIT_BOUNTY", "REDIRECT_PRIVATE_GHSA", "REDIRECT_DOC_DRIFT_PR"} else 1
    parser.error("Specify --selftest or --evaluate <receipt.json>")
    return 2


if __name__ == "__main__":
    sys.exit(main())
