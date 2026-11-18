#!/usr/bin/env python3
"""Deterministic C5-REAL Bug Bounty Eligibility & EV Gate (stdlib-only, fail-closed). Schema v4.

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

Recibo (schema_version 4):
  - target: {"kind": "evm", "chain_id": int, "address": "0x" + 40 hex, "block": int}
          | {"kind": "commit", "repo": str, "sha": 40|64 hex}
    Sin objetivo fijado (fork en bloque concreto o commit exacto) no hay veredicto.
  - Claves desconocidas o duplicadas -> BLOCKED.
  - Cada afirmación positiva de EVIDENCE_BOUND_CLAIMS cita >= 1 ev_* registrado en rea_evidence_ids.
  - Un mismo ev_* no puede respaldar afirmaciones de grupos distintos (scope, target, poc,
    invariant, known_issues, retention): un archivo no prueba a la vez el scope y el PoC.

Manifiesto (--evidence-manifest): {"manifest_version": 1, "evidence": {"ev_x": {"path", "sha256"}}}
  - Rutas relativas al directorio del manifiesto. SHA-256 recalculado sobre los bytes.
  - Archivo ausente o vacío, hash distinto, dos ids sobre el mismo archivo o el mismo contenido,
    o evidencia que es el propio recibo/manifiesto -> BLOCKED.
  - La evidencia citada para silicon_poc_passes debe ser la salida de un test runner reconocido
    y aprobada: `forge test --json` (>= 1 Success, 0 Failure) o el resumen libtest de
    `cargo test` (>= 1 passed, 0 failed, ningún FAILED). Formato no reconocido -> BLOCKED.
  - Sin manifiesto, los veredictos que salen al exterior se bloquean; DROP_* y HOLD_* se mantienen.
  Generarlo: --build-manifest out.json ev_poc=forge_out.json ev_scope=scope.json ...

Atestación (CLI): receipt_sha256, manifest_sha256, gate_sha256 (bytes de este script) y
  decision_sha256 = sha256(JSON canónico de {status, receipt_sha256, manifest_sha256, gate_sha256}).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any

SCHEMA_VERSION = 4
MANIFEST_VERSION = 1

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

# Afirmación positiva -> grupo de evidencia. Un ev_* solo respalda afirmaciones de un mismo grupo.
CLAIM_GROUP = {
    "asset_in_scope": "scope",
    "impact_in_scope": "scope",
    "onchain_or_commit_verified": "target",
    "silicon_poc_passes": "poc",
    "algebraic_invariant_verified": "invariant",
    "not_known_issue_or_prior_audit": "known_issues",
    "inference_retention_verified": "retention",
}
EVIDENCE_BOUND_CLAIMS = tuple(CLAIM_GROUP)

STRUCTURAL_FIELDS = ("schema_version", "target", "rea_evidence_ids", "evidence_map")
ALLOWED_KEYS = frozenset(
    REQUIRED_BOOL_GATES + OPTIONAL_BOOL_FIELDS + tuple(k for k, _, _ in REQUIRED_NUMERIC) + STRUCTURAL_FIELDS
)

OUTBOUND_STATUSES = frozenset({"SUBMIT_BOUNTY", "REDIRECT_PRIVATE_GHSA", "REDIRECT_DOC_DRIFT_PR"})
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
_HEX = frozenset("0123456789abcdef")


# ---------------------------------------------------------------- validación del recibo


def _is_strict_number(x: Any) -> bool:
    # bool es subclase de int: se excluye explícitamente. Strings ("nan", "1e9") se rechazan.
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _is_strict_int(x: Any, lo: int) -> bool:
    return isinstance(x, int) and not isinstance(x, bool) and x >= lo


def _validate_target(t: Any) -> list[str]:
    if not isinstance(t, dict):
        return ["target(object)"]
    kind = t.get("kind")
    if kind == "evm":
        if set(t) != {"kind", "chain_id", "address", "block"}:
            return ["target(evm: exactly kind, chain_id, address, block)"]
        errs = []
        if not _is_strict_int(t["chain_id"], 1):
            errs.append("target.chain_id(int >= 1)")
        a = t["address"]
        if not (isinstance(a, str) and len(a) == 42 and a[:2] == "0x" and set(a[2:].lower()) <= _HEX):
            errs.append("target.address(0x + 40 hex)")
        if not _is_strict_int(t["block"], 1):
            errs.append("target.block(int >= 1: fork pinned, never 'latest')")
        return errs
    if kind == "commit":
        if set(t) != {"kind", "repo", "sha"}:
            return ["target(commit: exactly kind, repo, sha)"]
        errs = []
        if not (isinstance(t["repo"], str) and t["repo"].strip()):
            errs.append("target.repo(non-empty string)")
        s = t["sha"]
        if not (isinstance(s, str) and len(s) in (40, 64) and set(s) <= _HEX):
            errs.append("target.sha(40|64 lowercase hex, full SHA)")
        return errs
    return ["target.kind(evm|commit)"]


def _validate(data: Any) -> list[str]:
    if not isinstance(data, dict):
        return ["receipt(object)"]
    errors: list[str] = []
    sv = data.get("schema_version")
    if not (_is_strict_int(sv, 0) and sv == SCHEMA_VERSION):
        errors.append(f"schema_version(=={SCHEMA_VERSION})")
    unknown = sorted(set(data) - ALLOWED_KEYS)
    if unknown:
        errors.append(f"unknown_keys{unknown}")
    errors.extend(_validate_target(data.get("target")))
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
    pp, pv = data.get("payout_probability"), data.get("validity_probability")
    if _is_strict_number(pp) and _is_strict_number(pv) and pp > pv:
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
    groups_by_id: dict[str, set[str]] = {}
    for claim in EVIDENCE_BOUND_CLAIMS:
        if data.get(claim) is not True:
            continue  # solo se exige prueba a lo que se afirma como cierto
        cited = emap.get(claim)
        if not isinstance(cited, list) or not cited:
            errors.append(f"evidence_map.{claim}(non-empty list)")
        elif not all(isinstance(x, str) and x in known_ids for x in cited):
            errors.append(f"evidence_map.{claim}(ids must exist in rea_evidence_ids)")
        else:
            for x in cited:
                groups_by_id.setdefault(x, set()).add(CLAIM_GROUP[claim])
    reused = sorted(x for x, g in groups_by_id.items() if len(g) > 1)
    if reused:
        errors.append(f"evidence_map.cross_group_reuse{reused}")
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


# ---------------------------------------------------------------- veredicto (función pura)


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
    return out(
        "SUBMIT_BOUNTY",
        expected_value_usd=ev,
        include_remediation_patch=data.get("patch_regression_free") is True,
        rea_evidence_count=n_ev,
    )


# ---------------------------------------------------------------- evidencia: hash + semántica del PoC


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# Resumen libtest (cargo test), estable: "test result: ok. 3 passed; 0 failed; 0 ignored; ..."
_LIBTEST_RE = re.compile(r"^test result: (ok|FAILED)\. (\d+) passed; (\d+) failed;", re.MULTILINE)


def _parse_forge_json(text: str) -> tuple[int, int] | None:
    """`forge test --json` -> {suite: {"test_results": {test: {"status": Success|Failure|Skipped}}}}."""
    lines = [ln for ln in text.splitlines() if ln.strip()]
    candidates = [text] + ([lines[-1]] if len(lines) > 1 else [])  # tolera ruido previo al JSON final
    for cand in candidates:
        try:
            obj = parse_receipt_text(cand)
        except (ValueError, RecursionError):
            continue
        if not isinstance(obj, dict):
            continue
        passed = failed = 0
        ok = True
        for suite in obj.values():
            results = suite.get("test_results") if isinstance(suite, dict) else None
            if not isinstance(results, dict):
                ok = False
                break
            for res in results.values():
                status = res.get("status") if isinstance(res, dict) else None
                if status == "Success":
                    passed += 1
                elif status == "Failure":
                    failed += 1
                elif status != "Skipped":
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return passed, failed  # {} (forge sin tests) -> (0, 0)
    return None


def _parse_libtest(text: str) -> tuple[int, int] | None:
    rows = _LIBTEST_RE.findall(text)
    if not rows:
        return None
    passed = sum(int(p) for _, p, _ in rows)
    failed = sum(max(int(f), 1 if st == "FAILED" else 0) for st, _, f in rows)
    return passed, failed


def classify_poc_evidence(raw: bytes) -> tuple[str, int, int] | None:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    parsed = _parse_forge_json(text)
    if parsed is not None:
        return ("forge-json", *parsed)
    parsed = _parse_libtest(text)
    if parsed is not None:
        return ("cargo-libtest", *parsed)
    return None


def verify_manifest(
    manifest: Any, base_dir: Path, receipt: dict[str, Any], forbidden_paths: tuple[Path, ...] = ()
) -> list[str]:
    """Errores; lista vacía = cada ev_ del recibo existe, no está vacío, coincide en hash,
    no duplica otro, y el PoC citado es una ejecución de tests aprobada."""
    if not isinstance(manifest, dict) or manifest.get("manifest_version") != MANIFEST_VERSION:
        return [f"manifest.manifest_version(=={MANIFEST_VERSION})"]
    if set(manifest) - {"manifest_version", "evidence"}:
        return [f"manifest.unknown_keys{sorted(set(manifest) - {'manifest_version', 'evidence'})}"]
    entries = manifest.get("evidence")
    if not isinstance(entries, dict) or not entries:
        return ["manifest.evidence(non-empty object)"]

    poc_ids = set(receipt["evidence_map"].get("silicon_poc_passes", [])) if receipt.get("silicon_poc_passes") else set()
    forbidden = {p.resolve() for p in forbidden_paths}
    seen_paths: dict[Path, str] = {}
    seen_hashes: dict[str, str] = {}
    errors: list[str] = []
    passing_poc = 0

    for ev_id in receipt["rea_evidence_ids"]:
        e = entries.get(ev_id)
        if not isinstance(e, dict) or set(e) != {"path", "sha256"}:
            errors.append(f"manifest.{ev_id}(missing or not {{path, sha256}})")
            continue
        declared = e["sha256"]
        if not (isinstance(declared, str) and len(declared) == 64 and set(declared) <= _HEX):
            errors.append(f"manifest.{ev_id}.sha256(64 lowercase hex)")
            continue
        if not isinstance(e["path"], str) or not e["path"]:
            errors.append(f"manifest.{ev_id}.path(non-empty string)")
            continue
        p = Path(e["path"]).expanduser()
        p = (p if p.is_absolute() else base_dir / p).resolve()
        if p in forbidden:
            errors.append(f"manifest.{ev_id}(evidence cannot be the receipt or the manifest itself)")
            continue
        if p in seen_paths:
            errors.append(f"manifest.{ev_id}(same file as {seen_paths[p]})")
            continue
        seen_paths[p] = ev_id
        if not p.is_file():
            errors.append(f"manifest.{ev_id}(file not found: {p})")
            continue
        try:
            if p.stat().st_size == 0:
                errors.append(f"manifest.{ev_id}(empty file)")
                continue
            raw = p.read_bytes() if ev_id in poc_ids else None
            actual = hashlib.sha256(raw).hexdigest() if raw is not None else file_sha256(p)
        except OSError as exc:
            errors.append(f"manifest.{ev_id}(unreadable: {exc})")
            continue
        if actual != declared:
            errors.append(f"manifest.{ev_id}(sha256 mismatch: declared {declared[:12]}…, actual {actual[:12]}…)")
            continue
        if actual in seen_hashes:
            errors.append(f"manifest.{ev_id}(identical content to {seen_hashes[actual]})")
            continue
        seen_hashes[actual] = ev_id
        if raw is not None:
            kind = classify_poc_evidence(raw)
            if kind is None:
                errors.append(f"manifest.{ev_id}(PoC evidence is not a recognized test run: forge test --json | cargo test output)")
            elif kind[2] > 0:
                errors.append(f"manifest.{ev_id}({kind[0]}: {kind[2]} failed)")
            elif kind[1] == 0:
                errors.append(f"manifest.{ev_id}({kind[0]}: 0 passed)")
            else:
                passing_poc += 1

    if poc_ids and passing_poc == 0 and not errors:
        errors.append("silicon_poc_passes(no passing PoC run among cited evidence)")
    return errors


def apply_evidence_verification(result: dict[str, Any], manifest_errors: list[str] | None) -> dict[str, Any]:
    """manifest_errors=None -> no se aportó manifiesto. Lista vacía -> verificado."""
    if manifest_errors:
        return {
            **result,
            "status": "BLOCKED_INCOMPLETE_EVIDENCE",
            "eligible_for_paid_bounty": False,
            "pre_verification_status": result["status"],
            "evidence_hash_errors": manifest_errors,
        }
    if manifest_errors is None:
        if result["status"] in OUTBOUND_STATUSES:
            return {
                **result,
                "status": "BLOCKED_INCOMPLETE_EVIDENCE",
                "eligible_for_paid_bounty": False,
                "pre_verification_status": result["status"],
                "evidence_hash_errors": ["no --evidence-manifest: outbound verdict requires hash-verified evidence"],
            }
        return {**result, "evidence_hash_verified": False}
    return {**result, "evidence_hash_verified": True}


def build_manifest(pairs: list[str], out_path: Path) -> dict[str, Any]:
    """pairs: ['ev_id=ruta', ...]. Rutas guardadas relativas al directorio del manifiesto cuando es posible."""
    base = out_path.resolve().parent
    evidence: dict[str, Any] = {}
    for pair in pairs:
        ev_id, sep, raw = pair.partition("=")
        if not sep or not ev_id.startswith("ev_") or len(ev_id) <= 3 or not raw:
            raise ValueError(f"bad pair {pair!r} (expected ev_id=path)")
        if ev_id in evidence:
            raise ValueError(f"duplicate evidence id {ev_id!r}")
        p = Path(raw).expanduser().resolve()
        if not p.is_file():
            raise ValueError(f"not a file: {p}")
        if p.stat().st_size == 0:
            raise ValueError(f"empty file: {p}")
        try:
            stored = str(p.relative_to(base))
        except ValueError:
            stored = str(p)
        evidence[ev_id] = {"path": stored, "sha256": file_sha256(p)}
    return {"manifest_version": MANIFEST_VERSION, "evidence": evidence}


# ---------------------------------------------------------------- atestación


def gate_sha256() -> str:
    return file_sha256(Path(__file__).resolve())


def attest(result: dict[str, Any], manifest_sha: str | None) -> dict[str, Any]:
    g = gate_sha256()
    core = {
        "status": result["status"],
        "receipt_sha256": result.get("receipt_sha256"),
        "manifest_sha256": manifest_sha,
        "gate_sha256": g,
    }
    decision = hashlib.sha256(json.dumps(core, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    return {**result, "manifest_sha256": manifest_sha, "gate_sha256": g, "decision_sha256": decision}


# ---------------------------------------------------------------- selftest

VALID = {
    "schema_version": SCHEMA_VERSION,
    "target": {"kind": "evm", "chain_id": 1, "address": "0x" + "ab" * 20, "block": 21_000_000},
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


def _drop(d: dict[str, Any], *keys: str) -> dict[str, Any]:
    return {k: v for k, v in d.items() if k not in keys}


def _emap_without(claim: str) -> dict[str, Any]:
    return dict(VALID, evidence_map={k: v for k, v in VALID["evidence_map"].items() if k != claim})


def _target(**kw: Any) -> dict[str, Any]:
    return dict(VALID, target=dict(VALID["target"], **kw))


_ONE_FILE = dict(VALID, rea_evidence_ids=["ev_any"], evidence_map={k: ["ev_any"] for k in VALID["evidence_map"]})
_COMMIT = {"kind": "commit", "repo": "github.com/org/protocol", "sha": "a" * 40}

SELFTEST_CASES: list[tuple[str, Any, str]] = [
    # --- caminos base ---
    ("valid_submit", VALID, "SUBMIT_BOUNTY"),
    ("cv_ibc_01_excluded_by_rules", dict(VALID, self_inflicted_only=True, admin_recovery_excluded_by_rules=True), "REDIRECT_PRIVATE_GHSA"),
    ("cv_ibc_02_falsified", dict(VALID, algebraic_invariant_verified=False), "DROP_FALSIFIED"),
    ("poc_fails", dict(VALID, silicon_poc_passes=False), "DROP_FALSIFIED"),
    ("asset_out_of_scope_only", dict(VALID, asset_in_scope=False), "REDIRECT_PRIVATE_GHSA"),
    ("doc_drift", dict(VALID, is_doc_drift_only=True), "REDIRECT_DOC_DRIFT_PR"),
    # --- v2: fallos de v1 ---
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
    ("known_issue", dict(VALID, not_known_issue_or_prior_audit=False), "DROP_KNOWN_ISSUE"),
    ("retention_unverified", dict(VALID, inference_retention_verified=False), "BLOCKED_EMBARGO_VIOLATION"),
    ("remote_dirty", dict(VALID, public_remote_clean=False), "BLOCKED_EMBARGO_VIOLATION"),
    ("embargo_beats_falsified", dict(VALID, public_remote_clean=False, algebraic_invariant_verified=False), "BLOCKED_EMBARGO_VIOLATION"),
    ("non_positive_ev_holds", dict(VALID, estimated_payout_usd=1000.0, payout_probability=0.05, validity_probability=0.1, pay_to_submit_fee_usd=500.0), "HOLD_NON_POSITIVE_EV"),
    ("zero_ev_holds", dict(VALID, estimated_payout_usd=0.0), "HOLD_NON_POSITIVE_EV"),
    ("old_v1_receipt_blocks", _drop(VALID, "not_known_issue_or_prior_audit", "inference_retention_verified", "validity_probability", "schema_version", "evidence_map", "target"), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("non_dict_receipt", ["not", "a", "dict"], "BLOCKED_INCOMPLETE_EVIDENCE"),
    # --- v3: fallos de v2 ---
    ("J_typo_optional_field", dict(VALID, is_doc_drift_onyl=True), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("J2_legacy_field_name", dict(VALID, acceptance_probability=0.85), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("K_missing_schema_version", _drop(VALID, "schema_version"), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("K2_v2_schema", dict(VALID, schema_version=2), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("K3_v3_schema", dict(VALID, schema_version=3), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("K4_bool_schema_version", dict(VALID, schema_version=True), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("L_true_claim_without_evidence", _emap_without("silicon_poc_passes"), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("L2_cites_unregistered_id", dict(VALID, evidence_map=dict(VALID["evidence_map"], silicon_poc_passes=["ev_ghost"])), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("L3_empty_citation", dict(VALID, evidence_map=dict(VALID["evidence_map"], asset_in_scope=[])), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("L4_missing_evidence_map", _drop(VALID, "evidence_map"), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("L5_unknown_claim_in_map", dict(VALID, evidence_map=dict(VALID["evidence_map"], uses_mocks=["ev_forge_poc"])), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("L6_false_claim_needs_no_evidence", dict(_emap_without("asset_in_scope"), asset_in_scope=False), "REDIRECT_PRIVATE_GHSA"),
    # --- v4: fallos de v3 ---
    ("O_missing_target", _drop(VALID, "target"), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("O2_short_address", _target(address="0x" + "ab" * 19), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("O3_block_zero", _target(block=0), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("O4_block_latest", _target(block="latest"), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("O5_chain_id_bool", _target(chain_id=True), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("O6_target_extra_key", _target(rpc="https://example.invalid"), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("O7_commit_target_ok", dict(VALID, target=_COMMIT), "SUBMIT_BOUNTY"),
    ("O8_commit_short_sha", dict(VALID, target=dict(_COMMIT, sha="abc1234")), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("O9_commit_uppercase_sha", dict(VALID, target=dict(_COMMIT, sha="A" * 40)), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("O10_unknown_kind", dict(VALID, target={"kind": "solana", "program": "x"}), "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("P_one_file_proves_everything", _ONE_FILE, "BLOCKED_INCOMPLETE_EVIDENCE"),
    ("P2_poc_reused_as_invariant", dict(VALID, evidence_map=dict(VALID["evidence_map"], algebraic_invariant_verified=["ev_forge_poc"])), "BLOCKED_INCOMPLETE_EVIDENCE"),
]

FORGE_PASS = json.dumps({"test/Poc.t.sol:PocTest": {"duration": "12ms", "test_results": {"test_exploit()": {"status": "Success", "reason": None}}, "warnings": []}})
FORGE_FAIL = FORGE_PASS.replace('"Success"', '"Failure"')
FORGE_SKIP = FORGE_PASS.replace('"Success"', '"Skipped"')
LIBTEST_OK = "running 1 test\ntest poc::exploit ... ok\n\ntest result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.01s\n"
LIBTEST_FAIL = "running 1 test\ntest poc::exploit ... FAILED\n\ntest result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.01s\n"


def _selftest_manifest() -> tuple[list[dict[str, Any]], int]:
    import tempfile

    fails: list[dict[str, Any]] = []
    n = 0
    ids = VALID["rea_evidence_ids"]
    submit = evaluate_receipt(VALID)
    drop = evaluate_receipt(dict(VALID, algebraic_invariant_verified=False))

    def check(name: str, cond: bool, got: Any = None) -> None:
        nonlocal n
        n += 1
        if not cond:
            fails.append({"case": name, "got": got})

    with tempfile.TemporaryDirectory() as td:
        base = Path(td)

        def fresh(poc: str = FORGE_PASS) -> dict[str, Any]:
            for ev in ids:
                (base / f"{ev}.json").write_text(json.dumps({"evidence": ev}), encoding="utf-8")
            (base / "ev_forge_poc.json").write_text(poc, encoding="utf-8")
            return build_manifest([f"{ev}={base / (ev + '.json')}" for ev in ids], base / "manifest.json")

        def errs(m: dict[str, Any], forbidden: tuple[Path, ...] = ()) -> list[str]:
            return verify_manifest(m, base, VALID, forbidden)

        def status(m: dict[str, Any] | None, res: dict[str, Any] = submit) -> str:
            return apply_evidence_verification(res, None if m is None else errs(m))["status"]

        def has(m: dict[str, Any], needle: str, forbidden: tuple[Path, ...] = ()) -> tuple[bool, list[str]]:
            e = errs(m, forbidden)
            return any(needle in x for x in e), e

        def sha(b: bytes) -> str:
            return hashlib.sha256(b).hexdigest()

        m = fresh()
        check("MF_ok_forge_json", status(m) == "SUBMIT_BOUNTY", errs(m))
        check("MF_paths_relative", all(not Path(e["path"]).is_absolute() for e in m["evidence"].values()), m)
        m = fresh(LIBTEST_OK)
        check("MF_ok_cargo_libtest", status(m) == "SUBMIT_BOUNTY", errs(m))
        m = fresh("Compiling 3 files with Solc 0.8.28\n" + FORGE_PASS + "\n")
        check("MF_ok_forge_with_leading_noise", status(m) == "SUBMIT_BOUNTY", errs(m))

        m = fresh()
        (base / "ev_forge_poc.json").write_text(FORGE_PASS.replace("12ms", "13ms"), encoding="utf-8")
        check("MF_tampered_file", status(m) == "BLOCKED_INCOMPLETE_EVIDENCE", errs(m))
        m = fresh()
        partial = {"manifest_version": 1, "evidence": _drop(m["evidence"], "ev_scope_json")}
        check("MF_missing_id", *has(partial, "ev_scope_json"))
        m = fresh()
        (base / "ev_halmos_inv.json").unlink()
        check("MF_file_missing", *has(m, "file not found"))

        check("MF_no_manifest_blocks_submit", status(None) == "BLOCKED_INCOMPLETE_EVIDENCE")
        check("MF_no_manifest_keeps_drop", status(None, drop) == "DROP_FALSIFIED")
        check("MF_bad_version", bool(verify_manifest({"manifest_version": 2, "evidence": {}}, base, VALID)))
        m = fresh()
        check("MF_bad_hex", *has({"manifest_version": 1, "evidence": dict(m["evidence"], ev_scope_json={"path": "x", "sha256": "ZZ" * 32})}, "64 lowercase hex"))
        try:
            build_manifest(["poc=/etc/hosts"], base / "manifest.json")
            check("MF_bad_pair_rejected", False, "accepted")
        except ValueError:
            check("MF_bad_pair_rejected", True)

        # semántica del PoC
        check("MF_poc_forge_failure", *has(fresh(FORGE_FAIL), "1 failed"))
        check("MF_poc_forge_only_skipped", *has(fresh(FORGE_SKIP), "0 passed"))
        check("MF_poc_forge_no_tests", *has(fresh("{}"), "0 passed"))
        check("MF_poc_cargo_failed", *has(fresh(LIBTEST_FAIL), "failed"))
        check("MF_poc_unrecognized", *has(fresh('{"pwned": true}'), "not a recognized test run"))

        # aliasing, copias, vacíos, autorreferencia
        m = fresh()
        (base / "empty.json").write_bytes(b"")
        m["evidence"]["ev_known_issues_diff"] = {"path": "empty.json", "sha256": sha(b"")}
        check("MF_zero_byte_evidence", *has(m, "empty file"))
        m = fresh()
        m["evidence"]["ev_known_issues_diff"] = dict(m["evidence"]["ev_scope_json"])
        check("MF_two_ids_same_file", *has(m, "same file as ev_scope_json"))
        m = fresh()
        dup = (base / "ev_scope_json.json").read_bytes()
        (base / "copy.json").write_bytes(dup)
        m["evidence"]["ev_known_issues_diff"] = {"path": "copy.json", "sha256": sha(dup)}
        check("MF_two_ids_identical_content", *has(m, "identical content to ev_scope_json"))
        m = fresh()
        receipt_bytes = json.dumps(VALID).encode("utf-8")
        (base / "receipt.json").write_bytes(receipt_bytes)
        m["evidence"]["ev_known_issues_diff"] = {"path": "receipt.json", "sha256": sha(receipt_bytes)}
        check("MF_evidence_is_receipt", *has(m, "receipt or the manifest", (base / "receipt.json",)))

    # atestación
    a1, a2 = attest(submit, "a" * 64), attest(submit, "a" * 64)
    check("AT_deterministic", a1["decision_sha256"] == a2["decision_sha256"], [a1, a2])
    check("AT_status_sensitive", attest(drop, "a" * 64)["decision_sha256"] != a1["decision_sha256"])
    check("AT_manifest_sensitive", attest(submit, "b" * 64)["decision_sha256"] != a1["decision_sha256"])
    check("AT_gate_hash_shape", len(a1["gate_sha256"]) == 64 and set(a1["gate_sha256"]) <= _HEX, a1["gate_sha256"])
    return fails, n


def run_selftest() -> int:
    failures = []
    for name, receipt, expected in SELFTEST_CASES:
        got = evaluate_receipt(receipt)
        if got["status"] != expected or got["eligible_for_paid_bounty"] is not (expected == "SUBMIT_BOUNTY"):
            failures.append({"case": name, "expected": expected, "got": got})
    extra = 0

    def value_check(name: str, cond: bool, got: Any = None) -> None:
        nonlocal extra
        extra += 1
        if not cond:
            failures.append({"case": name, "got": got})

    r = evaluate_receipt(dict(VALID, estimated_payout_usd=2000.0, payout_probability=0.2, validity_probability=0.6, pay_to_submit_fee_usd=500.0))
    value_check("I_ev_value", r.get("expected_value_usd") == 200.0, r)
    r = evaluate_receipt(dict(VALID, patch_regression_free=False))
    value_check("E_patch_omitted", r.get("include_remediation_patch") is False, r)
    reordered = dict(reversed(list(VALID.items())))
    h1, h2 = evaluate_receipt(VALID)["receipt_sha256"], evaluate_receipt(reordered)["receipt_sha256"]
    value_check("M_hash_canonical", isinstance(h1, str) and len(h1) == 64 and h1 == h2, [h1, h2])
    value_check("M2_hash_sensitive", evaluate_receipt(dict(VALID, estimated_payout_usd=1.0))["receipt_sha256"] != h1)
    for name, text in (("N_dup_keys", '{"uses_mocks": true, "uses_mocks": false}'), ("N2_nan_const", '{"x": NaN}')):
        try:
            parse_receipt_text(text)
            value_check(name, False, "parsed")
        except ValueError:
            value_check(name, True)

    mf_fails, mf_n = _selftest_manifest()
    failures.extend(mf_fails)
    if failures:
        print(json.dumps({"selftest": "FAIL", "failures": failures}, ensure_ascii=False, indent=2, default=str))
        return 1
    total = len(SELFTEST_CASES) + extra + mf_n
    print(json.dumps({"selftest": "PASS", "schema_version": SCHEMA_VERSION, "cases_verified": total}))
    return 0


# ---------------------------------------------------------------- CLI


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--selftest", action="store_true", help="Run deterministic self-tests")
    parser.add_argument("--evaluate", type=Path, help="Evaluate a bounty gate receipt JSON file")
    parser.add_argument("--evidence-manifest", type=Path, help="Manifest {ev_id: {path, sha256}} to verify cited evidence")
    parser.add_argument("--build-manifest", type=Path, metavar="OUT", help="Write a manifest from ev_id=path pairs")
    parser.add_argument("pairs", nargs="*", help="ev_id=path pairs for --build-manifest")
    args = parser.parse_args()

    if args.selftest:
        return run_selftest()
    if args.build_manifest:
        try:
            if args.build_manifest.exists():
                raise ValueError(f"refusing to overwrite {args.build_manifest}")
            if not args.pairs:
                raise ValueError("no ev_id=path pairs given")
            m = build_manifest(args.pairs, args.build_manifest)
        except ValueError as exc:
            print(json.dumps({"error": str(exc)}, ensure_ascii=False))
            return EXIT_BLOCKED
        args.build_manifest.write_text(json.dumps(m, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"written": str(args.build_manifest), "evidence_count": len(m["evidence"])}))
        return 0
    if args.evaluate:
        manifest_sha: str | None = None
        try:
            payload = parse_receipt_text(args.evaluate.read_text(encoding="utf-8"))
            result = evaluate_receipt(payload)
            if "rea_evidence_count" in result:  # recibo bien formado
                manifest_errors: list[str] | None = None
                if args.evidence_manifest:
                    raw = args.evidence_manifest.read_bytes()
                    manifest_sha = hashlib.sha256(raw).hexdigest()
                    manifest = parse_receipt_text(raw.decode("utf-8"))
                    manifest_errors = verify_manifest(
                        manifest,
                        args.evidence_manifest.resolve().parent,
                        payload,
                        (args.evaluate, args.evidence_manifest),
                    )
                result = apply_evidence_verification(result, manifest_errors)
        except (OSError, ValueError) as exc:
            result = {"status": "BLOCKED_INCOMPLETE_EVIDENCE", "eligible_for_paid_bounty": False, "error": str(exc)}
        result = attest(result, manifest_sha)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return EXIT_BY_STATUS.get(result["status"], EXIT_BLOCKED)
    parser.error("Specify --selftest, --evaluate <receipt.json> [--evidence-manifest M], or --build-manifest OUT ev_id=path ...")
    return 2


if __name__ == "__main__":
    sys.exit(main())
