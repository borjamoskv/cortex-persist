#!/usr/bin/env python3
"""Deterministic C5-REAL Bug Bounty Eligibility & EV Gate (stdlib-only, fail-closed).

Verdicts (exit code):
  SUBMIT_BOUNTY                0  enviar al programa remunerado
  REDIRECT_PRIVATE_GHSA        0  bug real excluido del bounty -> advisory privado
  REDIRECT_DOC_DRIFT_PR        0  divergencia documental -> PR
  DROP_FALSIFIED               3  hipótesis falsada (resultado correcto, nada que enviar)
  DROP_KNOWN_ISSUE             3  ya conocido / en auditoría previa
  HOLD_NON_POSITIVE_EV         3  en scope pero EV <= 0 -> decisión humana, no auto-redirect
  BLOCKED_INCOMPLETE_EVIDENCE  1  recibo malformado o hallazgo no probado
  BLOCKED_EMBARGO_VIOLATION    1  remoto público sucio o inferencia sin retención verificada

EV con reembolso en créditos (la cuota solo se pierde si el reporte es inválido):
  EV = p_pay * payout - (1 - p_valid) * fee,   0 <= p_pay <= p_valid <= 1

Schema v3 (fail-closed):
  - schema_version == 3 obligatorio.
  - Claves desconocidas -> BLOCKED (un typo en un flag opcional no puede ignorarse en silencio).
  - Claves JSON duplicadas -> BLOCKED (json.loads se quedaría con la última).
  - Cada flag EVIDENCE_BOUND_CLAIMS a true debe citar en evidence_map[flag] al menos un ev_*
    presente en rea_evidence_ids. Un true sin evidencia es una afirmación, no un hecho.
  - La salida incluye receipt_sha256 (JSON canónico) para anclarla en un ledger.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
from typing import Any

SCHEMA_VERSION = 3

REQUIRED_BOOL_GATES = (
    "asset_in_scope",
    "impact_in_scope",
    "onchain_or_commit_verified",
    "silicon_poc_passes",
    "uses_mocks",
    "algebraic_invariant_verified",
    "self_inflicted_only",
    "admin_recovery_excluded_by_rules",
    "public_remote_clean",
    "not_known_issue_or_prior_audit",
    "inference_retention_verified",
)
# Opcionales: si están presentes DEBEN ser bool (un string "true" no se acepta en silencio).
OPTIONAL_BOOL_FIELDS = ("is_doc_drift_only", "patch_regression_free")

# (campo, mínimo, máximo)
REQUIRED_NUMERIC = (
    ("estimated_payout_usd", 0.0, math.inf),
    ("payout_probability", 0.0, 1.0),
    ("validity_probability", 0.0, 1.0),
    ("pay_to_submit_fee_usd", 0.0, math.inf),
)

# Afirmaciones positivas necesarias para SUBMIT: si valen true, exigen evidencia citada.
EVIDENCE_BOUND_CLAIMS = (
    "asset_in_scope",
    "impact_in_scope",
    "onchain_or_commit_verified",
    "silicon_poc_passes",
    "algebraic_invariant_verified",
    "not_known_issue_or_prior_audit",
    "inference_retention_verified",
)

STRUCTURAL_FIELDS = ("schema_version", "rea_evidence_ids", "evidence_map")
ALLOWED_KEYS = frozenset(
    REQUIRED_BOOL_GATES + OPTIONAL_BOOL_FIELDS + tuple(k for k, _, _ in REQUIRED_NUMERIC) + STRUCTURAL_FIELDS
)

EXIT_ROUTE, EXIT_BLOCKED, EXIT_TERMINAL = 0, 1, 3
EXIT_BY_STATUS = {
    "SUBMIT_BOUNTY": EXIT_ROUTE,
    "REDIRECT_PRIVATE_GHSA": EXIT_ROUTE,
    "REDIRECT_DOC_DRIFT_PR": EXIT_ROUTE,
    "DROP_FALSIFIED": EXIT_TERMINAL,
    "DROP_KNOWN_ISSUE": EXIT_TERMINAL,
    "HOLD_NON_POSITIVE_EV": EXIT_TERMINAL,
    "BLOCKED_INCOMPLETE_EVIDENCE": EXIT_BLOCKED,
    "BLOCKED_EMBARGO_VIOLATION": EXIT_BLOCKED,
}


def _is_strict_number(x: Any) -> bool:
    # bool es subclase de int: se excluye explícitamente. Strings ("nan", "1e9") se rechazan.
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _validate(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["receipt(object)"]
    errors: list[str] = []
    sv = data.get("schema_version")
    if not (isinstance(sv, int) and not isinstance(sv, bool) and sv == SCHEMA_VERSION):
        errors.append(f"schema_version(=={SCHEMA_VERSION})")
    unknown = sorted(set(data) - ALLOWED_KEYS)
    if unknown:
        errors.append(f"unknown_keys{unknown}")
    for k in REQUIRED_BOOL_GATES:
        if not isinstance(data.get(k), bool):
            errors.append(f"{k}(bool)")
    for k in OPTIONAL_BOOL_FIELDS:
        if k in data and not isinstance(data[k], bool):
            errors.append(f"{k}(bool|absent)")
    for k, lo, hi in REQUIRED_NUMERIC:
        v = data.get(k)
        if not _is_strict_number(v) or not (lo <= v <= hi):
            errors.append(f"{k}(finite number in [{lo}, {hi}])")
    if not errors and data["payout_probability"] > data["validity_probability"]:
        errors.append("payout_probability<=validity_probability")
    ids = data.get("rea_evidence_ids")
    if (
        not isinstance(ids, list)
        or not ids
        or not all(isinstance(x, str) and x.startswith("ev_") and len(x) > 3 for x in ids)
        or len(set(ids)) != len(ids)
    ):
        errors.append("rea_evidence_ids(non-empty unique list[ev_*])")
        return errors  # sin registro de evidencias no se puede comprobar evidence_map
    known_ids = set(ids)
    emap = data.get("evidence_map")
    if not isinstance(emap, dict):
        errors.append("evidence_map(object)")
        return errors
    stray = sorted(set(emap) - set(EVIDENCE_BOUND_CLAIMS))
    if stray:
        errors.append(f"evidence_map.unknown_claims{stray}")
    for claim in EVIDENCE_BOUND_CLAIMS:
        if data.get(claim) is not True:
            continue  # solo se exige prueba a lo que se afirma como cierto
        cited = emap.get(claim)
        if not isinstance(cited, list) or not cited:
            errors.append(f"evidence_map.{claim}(non-empty list)")
        elif not all(isinstance(x, str) and x in known_ids for x in cited):
            errors.append(f"evidence_map.{claim}(ids must exist in rea_evidence_ids)")
    return errors


def receipt_sha256(data: Any) -> str | None:
    try:
        canon = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError):
        return None
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    seen: dict[str, Any] = {}
    for k, v in pairs:
        if k in seen:
            raise ValueError(f"duplicate JSON key {k!r}")
        seen[k] = v
    return seen


def _reject_constant(c: str) -> Any:
    raise ValueError(f"non-finite JSON constant {c}")


def parse_receipt_text(text: str) -> Any:
    return json.loads(text, object_pairs_hook=_reject_duplicate_keys, parse_constant=_reject_constant)


def expected_value(data: dict[str, Any]) -> float:
    ev = (
        data["payout_probability"] * data["estimated_payout_usd"]
        - (1.0 - data["validity_probability"]) * data["pay_to_submit_fee_usd"]
    )
    if not math.isfinite(ev):  # defensa en profundidad; _validate ya debería impedirlo
        raise ValueError("non-finite EV")
    return round(ev, 2)


def evaluate_receipt(data: Any) -> dict[str, Any]:
    digest = receipt_sha256(data)

    def out(status: str, **extra: Any) -> dict[str, Any]:
        return {
            "status": status,
            "eligible_for_paid_bounty": status == "SUBMIT_BOUNTY",
            **extra,
            "schema_version": SCHEMA_VERSION,
            "receipt_sha256": digest,
        }

    errors = _validate(data)
    if errors:
        return out("BLOCKED_INCOMPLETE_EVIDENCE", missing_or_invalid_fields=errors)

    n_ev = len(data["rea_evidence_ids"])

    # 1. Embargo primero: si ya hay fuga, nada más importa.
    leaks = []
    if not data["public_remote_clean"]:
        leaks.append("public_remote_dirty")
    if not data["inference_retention_verified"]:
        leaks.append("inference_retention_unverified")
    if leaks:
        return out("BLOCKED_EMBARGO_VIOLATION", reasons=leaks, rea_evidence_count=n_ev)

    # 2. Falsación.
    if not data["algebraic_invariant_verified"] or not data["silicon_poc_passes"]:
        return out("DROP_FALSIFIED", rea_evidence_count=n_ev)

    # 3. Hallazgo no probado sobre el objetivo real: bloquear, NO redirigir.
    unproven = []
    if data["uses_mocks"]:
        unproven.append("poc_uses_mocks")
    if not data["onchain_or_commit_verified"]:
        unproven.append("target_version_unverified")
    if unproven:
        return out("BLOCKED_INCOMPLETE_EVIDENCE", missing_or_invalid_fields=unproven, rea_evidence_count=n_ev)

    # 4. Divergencia documental.
    if data.get("is_doc_drift_only") is True:
        return out("REDIRECT_DOC_DRIFT_PR", rea_evidence_count=n_ev)

    # 5. Ya conocido: ni bounty ni GHSA.
    if not data["not_known_issue_or_prior_audit"]:
        return out("DROP_KNOWN_ISSUE", rea_evidence_count=n_ev)

    # 6. Bug real excluido por reglas -> advisory privado.
    exclusions = []
    if not data["asset_in_scope"]:
        exclusions.append("asset_out_of_scope")
    if not data["impact_in_scope"]:
        exclusions.append("impact_out_of_scope")
    if data["self_inflicted_only"]:
        exclusions.append("self_inflicted_without_third_party_loss")
    if data["admin_recovery_excluded_by_rules"]:
        exclusions.append("recoverable_by_privileged_role_excluded")
    if exclusions:
        return out("REDIRECT_PRIVATE_GHSA", disqualifiers=exclusions, rea_evidence_count=n_ev)

    # 7. En scope: decide el EV. EV <= 0 no se auto-redirige (saltarse el programa puede violar sus términos).
    ev = expected_value(data)
    if ev <= 0.0:
        return out("HOLD_NON_POSITIVE_EV", expected_value_usd=ev, rea_evidence_count=n_ev)

    # 8. Envío. Un parche con regresión no descalifica el bug: solo se omite la remediación.
    include_patch = data.get("patch_regression_free") is True
    return out(
        "SUBMIT_BOUNTY",
        expected_value_usd=ev,
        include_remediation_patch=include_patch,
        rea_evidence_count=n_ev,
    )


VALID = {
    "schema_version": SCHEMA_VERSION,
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
    "not_known_issue_or_prior_audit": True,
    "inference_retention_verified": True,
    "rea_evidence_ids": ["ev_scope_json", "ev_bytecode_parity", "ev_forge_poc", "ev_halmos_inv", "ev_known_issues_diff", "ev_retention_policy"],
    "evidence_map": {
        "asset_in_scope": ["ev_scope_json"],
        "impact_in_scope": ["ev_scope_json"],
        "onchain_or_commit_verified": ["ev_bytecode_parity"],
        "silicon_poc_passes": ["ev_forge_poc"],
        "algebraic_invariant_verified": ["ev_halmos_inv"],
        "not_known_issue_or_prior_audit": ["ev_known_issues_diff"],
        "inference_retention_verified": ["ev_retention_policy"],
    },
    "estimated_payout_usd": 50000.0,
    "payout_probability": 0.85,
    "validity_probability": 0.9,
    "pay_to_submit_fee_usd": 0.0,
}


def _emap_without(claim: str) -> dict[str, Any]:
    return dict(VALID, evidence_map={k: v for k, v in VALID["evidence_map"].items() if k != claim})


def _drop(d: dict[str, Any], *keys: str) -> dict[str, Any]:
    return {k: v for k, v in d.items() if k not in keys}


SELFTEST_CASES: list[tuple[str, Any, str]] = [
    # --- caminos originales ---
    ("valid_submit", VALID, "SUBMIT_BOUNTY"),
    ("cv_ibc_01_excluded_by_rules", dict(VALID, self_inflicted_only=True, admin_recovery_excluded_by_rules=True), "REDIRECT_PRIVATE_GHSA"),
    ("cv_ibc_02_falsified", dict(VALID, algebraic_invariant_verified=False), "DROP_FALSIFIED"),
    ("poc_fails", dict(VALID, silicon_poc_passes=False), "DROP_FALSIFIED"),
    ("asset_out_of_scope_only", dict(VALID, asset_in_scope=False), "REDIRECT_PRIVATE_GHSA"),
    ("doc_drift", dict(VALID, is_doc_drift_only=True), "REDIRECT_DOC_DRIFT_PR"),
    # --- regresiones de los fallos encontrados en v1 ---
    ("A_nan_payout_string", dict(VALID, estimated_payout_usd="nan"), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("A2_nan_payout_float", dict(VALID, estimated_payout_usd=float("nan")), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("A3_inf_payout", dict(VALID, estimated_payout_usd=float("inf")), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("B_empty_evidence", dict(VALID, rea_evidence_ids=[]), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("B2_bare_ev_prefix", dict(VALID, rea_evidence_ids=["ev_"]), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("B3_duplicate_evidence", dict(VALID, rea_evidence_ids=VALID["rea_evidence_ids"] + ["ev_forge_poc"]), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("C_p_gt_1", dict(VALID, payout_probability=7.0), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("C2_p_pay_gt_p_valid", dict(VALID, payout_probability=0.9, validity_probability=0.5), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("C3_negative_fee", dict(VALID, pay_to_submit_fee_usd=-10.0), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("C4_bool_as_number", dict(VALID, payout_probability=True), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("D_missing_payout_fields", _drop(VALID, "estimated_payout_usd", "payout_probability"), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("E_bad_patch_still_submits", dict(VALID, patch_regression_free=False), "SUBMIT_BOUNTY"),
    ("F_unverified_version_blocks", dict(VALID, onchain_or_commit_verified=False), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("G_mocks_block", dict(VALID, uses_mocks=True), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("H_doc_drift_string", dict(VALID, is_doc_drift_only="true"), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("I_refund_makes_ev_positive", dict(VALID, estimated_payout_usd=2000.0, payout_probability=0.2, validity_probability=0.6, pay_to_submit_fee_usd=500.0), "SUBMIT_BOUNTY"),
    # --- flags nuevos ---
    ("known_issue", dict(VALID, not_known_issue_or_prior_audit=False), "DROP_KNOWN_ISSUE"),
    ("retention_unverified", dict(VALID, inference_retention_verified=False), "BLOCKED_EMBARGO_VIOLATION"),
    ("remote_dirty", dict(VALID, public_remote_clean=False), "BLOCKED_EMBARGO_VIOLATION"),
    ("embargo_beats_falsified", dict(VALID, public_remote_clean=False, algebraic_invariant_verified=False), "BLOCKED_EMBARGO_VIOLATION"),
    ("non_positive_ev_holds", dict(VALID, estimated_payout_usd=1000.0, payout_probability=0.05, validity_probability=0.1, pay_to_submit_fee_usd=500.0), "HOLD_NON_POSITIVE_EV"),
    ("zero_ev_holds", dict(VALID, estimated_payout_usd=0.0), "HOLD_NON_POSITIVE_EV"),
    ("old_v1_receipt_blocks", _drop(VALID, "not_known_issue_or_prior_audit", "inference_retention_verified", "validity_probability", "schema_version", "evidence_map"), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("non_dict_receipt", ["not", "a", "dict"], "BLOCKED_INCOMPLETE_EVIDENCE"),
    # --- v3: agujeros encontrados en v2 ---
    ("J_typo_optional_field", dict(VALID, is_doc_drift_onyl=True), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("J2_legacy_field_name", dict(VALID, acceptance_probability=0.85), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("K_missing_schema_version", _drop(VALID, "schema_version"), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("K2_wrong_schema_version", dict(VALID, schema_version=2), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("K3_bool_schema_version", dict(VALID, schema_version=True), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("L_true_claim_without_evidence", _emap_without("silicon_poc_passes"), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("L2_cites_unregistered_id", dict(VALID, evidence_map=dict(VALID["evidence_map"], silicon_poc_passes=["ev_ghost"])), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("L3_empty_citation", dict(VALID, evidence_map=dict(VALID["evidence_map"], asset_in_scope=[])), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("L4_missing_evidence_map", _drop(VALID, "evidence_map"), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("L5_unknown_claim_in_map", dict(VALID, evidence_map=dict(VALID["evidence_map"], uses_mocks=["ev_forge_poc"])), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("L6_false_claim_needs_no_evidence", dict(_emap_without("asset_in_scope"), asset_in_scope=False), "REDIRECT_PRIVATE_GHSA"),
]


def run_selftest() -> int:
    failures = []
    for name, receipt, expected in SELFTEST_CASES:
        got = evaluate_receipt(receipt)
        if got["status"] != expected or got["eligible_for_paid_bounty"] is not (expected == "SUBMIT_BOUNTY"):
            failures.append({"case": name, "expected": expected, "got": got})
    # comprobaciones de valor
    r = evaluate_receipt(dict(VALID, estimated_payout_usd=2000.0, payout_probability=0.2, validity_probability=0.6, pay_to_submit_fee_usd=500.0))
    if r.get("expected_value_usd") != 200.0:
        failures.append({"case": "I_ev_value", "expected": 200.0, "got": r})
    r = evaluate_receipt(dict(VALID, patch_regression_free=False))
    if r.get("include_remediation_patch") is not False:
        failures.append({"case": "E_patch_omitted", "got": r})
    # hash determinista e independiente del orden de claves
    reordered = dict(reversed(list(VALID.items())))
    h1, h2 = evaluate_receipt(VALID)["receipt_sha256"], evaluate_receipt(reordered)["receipt_sha256"]
    if not (isinstance(h1, str) and len(h1) == 64 and h1 == h2):
        failures.append({"case": "M_hash_canonical", "got": [h1, h2]})
    if evaluate_receipt(dict(VALID, estimated_payout_usd=1.0))["receipt_sha256"] == h1:
        failures.append({"case": "M2_hash_sensitive"})
    # parser: claves duplicadas y constantes no finitas
    for name, text in (("N_dup_keys", '{"uses_mocks": true, "uses_mocks": false}'), ("N2_nan_const", '{"x": NaN}')):
        try:
            parse_receipt_text(text)
            failures.append({"case": name, "got": "parsed"})
        except ValueError:
            pass
    if failures:
        print(json.dumps({"selftest": "FAIL", "failures": failures}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"selftest": "PASS", "schema_version": SCHEMA_VERSION, "cases_verified": len(SELFTEST_CASES) + 6}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--selftest", action="store_true", help="Run deterministic self-tests")
    parser.add_argument("--evaluate", type=Path, help="Evaluate a bounty gate receipt JSON file")
    args = parser.parse_args()

    if args.selftest:
        return run_selftest()
    if args.evaluate:
        try:
            payload = parse_receipt_text(args.evaluate.read_text(encoding="utf-8"))
            result = evaluate_receipt(payload)
        except (OSError, ValueError) as exc:
            result = {"status": "BLOCKED_INCOMPLETE_EVIDENCE", "eligible_for_paid_bounty": False, "error": str(exc)}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return EXIT_BY_STATUS.get(result["status"], EXIT_BLOCKED)
    parser.error("Specify --selftest or --evaluate <receipt.json>")
    return 2


if __name__ == "__main__":
    sys.exit(main())
