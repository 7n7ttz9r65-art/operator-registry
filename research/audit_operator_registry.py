#!/usr/bin/env python3
"""
audit_operator_registry.py

Applies the Manus v2 rejection rules (see operator_registry_schema.md) to
operator_candidates.json. Prints a per-candidate verdict and writes
audit_result.json for run_manus_operator_audit.py to bundle into the
manifest.

This script does not search for candidates and does not evaluate whether a
candidate is "close" to correct. It only checks: (a) is the record
internally consistent with its own claimed certification levels, and
(b) do the automatic rejection rules fire.
"""
import json
import os
import sys
from datetime import datetime, timezone

CERT_LEVELS = {"none", "floating_point", "interval_arithmetic", "analytic_proof"}

STRONG_STATUSES = {"proved", "failed", "indefinite"}
STRONG_CERTS_REQUIRED = {"interval_arithmetic", "analytic_proof"}

NUMERICAL_STATUSES = {"numerical", "numerical_positive", "numerical_negative"}

FIELD_NAMES = [
    "trace_status", "positivity_status", "covariance_status",
    "self_adjoint_status", "compact_resolvent_status", "weyl_status",
    "determinant_status",
]


def cert_field_for(status_field):
    return status_field.replace("_status", "_certification")


def check_schema_violations(c):
    """Returns a list of violation strings. Empty list == no violations."""
    violations = []

    # 1. circularity flags must be booleans and, if true, is handled as
    #    rejection elsewhere -- here we just check they're present.
    for flag in ("uses_zero_data", "uses_target_wronskian", "uses_spectral_fitting",
                 "uses_post_hoc_target_definition"):
        if flag not in c or not isinstance(c[flag], bool):
            violations.append(f"missing or non-boolean '{flag}'")

    if "circularity_attestation" not in c or not c["circularity_attestation"].strip():
        violations.append("missing circularity_attestation (schema section 7)")

    # 2. status/certification compatibility for every status field present
    for field in FIELD_NAMES:
        if field not in c:
            continue
        status = c[field]
        cert_field = cert_field_for(field)
        cert = c.get(cert_field)

        if cert not in CERT_LEVELS:
            violations.append(f"{field}='{status}' has invalid/missing {cert_field}='{cert}'")
            continue

        if status in STRONG_STATUSES and cert not in STRONG_CERTS_REQUIRED:
            violations.append(
                f"{field}='{status}' requires certification in {STRONG_CERTS_REQUIRED}, "
                f"got '{cert}' -- this is exactly the conflation v2 exists to catch "
                f"(a floating-point result cannot carry a 'proved'/'failed'/'indefinite' status)"
            )

        if status in NUMERICAL_STATUSES and cert != "floating_point":
            violations.append(
                f"{field}='{status}' requires certification 'floating_point', got '{cert}'"
            )

        if status == "not_tested" and cert != "none":
            violations.append(f"{field}='not_tested' requires certification 'none', got '{cert}'")

        if status == "conditional":
            cond_key = "conditional_on" if field != "positivity_status" else "conditional_on_positivity"
            cond = c.get(cond_key)
            if not cond:
                violations.append(
                    f"{field}='conditional' requires non-empty '{cond_key}' (schema section 3)"
                )

    # 3. status_log presence
    if not c.get("status_log"):
        violations.append("missing status_log (append-only audit trail, schema section 5)")

    return violations


def check_missing_artifacts(c, base_dir):
    missing = []
    for ev in c.get("evidence_files", []):
        path = ev.get("path")
        if path is None:
            continue
        full = os.path.join(base_dir, path)
        if not os.path.exists(full):
            missing.append(path)
    return missing


def classify(c):
    """
    Returns (verdict, reasons) where verdict is one of:
      SCHEMA_VIOLATION, REJECTED, UNCERTIFIED_INDETERMINATE,
      CONDITIONAL_SURVIVOR, UNCONDITIONAL_SURVIVOR
    """
    violations = check_schema_violations(c)
    if violations:
        return "SCHEMA_VIOLATION", violations

    reasons = []

    # Rule 1: circularity
    if c["uses_zero_data"] or c["uses_target_wronskian"] or c["uses_spectral_fitting"]:
        return "REJECTED", ["Rule 1 (circularity): construction uses zero data, "
                             "the target Wronskian, or spectral fitting."]

    # Rule 7: tautological / post-hoc target definition
    if c["uses_post_hoc_target_definition"]:
        return "REJECTED", ["Rule 7 (tautological): Hilbert space/operator/vectors "
                             "were defined from the target function or known zero set "
                             "after the fact, rather than the target quantity falling "
                             "out of an independently-built construction."]

    def certified(field):
        status = c.get(field)
        cert = c.get(cert_field_for(field))
        return status in STRONG_STATUSES and cert in STRONG_CERTS_REQUIRED

    # Rule 2: certified negative/mixed-sign positivity
    if certified("positivity_status") and c["positivity_status"] in ("failed", "indefinite"):
        reasons.append(
            f"Rule 2 (positivity): positivity_status='{c['positivity_status']}' "
            f"certified via {c['positivity_certification']}."
        )

    # Rule 3/4: certified failure of weyl or determinant
    for field, rule_label in (("weyl_status", "Rule 3 (Weyl law)"),
                               ("determinant_status", "Rule 4 (determinant)")):
        if certified(field) and c[field] == "failed":
            reasons.append(f"{rule_label}: {field}='failed' certified via {c[cert_field_for(field)]}.")

    # Rule 5: trace_status='proved' requires prime_specific/theta_arithmetic
    #  specificity -- if trace_status is proved but specificity is generic,
    #  that's actually a schema-level inconsistency worth surfacing as a
    #  rejection reason rather than letting it pass silently.
    if c.get("trace_status") == "proved" and c.get("arithmetic_specificity") == "generic":
        reasons.append(
            "Rule 5 (positive counterpart): trace_status='proved' but "
            "arithmetic_specificity='generic' -- GUE-style statistics alone "
            "do not satisfy an exact-trace claim."
        )
    if certified("trace_status") and c["trace_status"] == "failed":
        reasons.append(f"trace_status='failed' certified via {c['trace_certification']}.")

    if reasons:
        return "REJECTED", reasons

    # Not rejected. Check for floating-point-only negative/failed signals
    # that would have been rejected under the looser v1 rules but are not
    # certified enough to reject under v2 -- these need re-testing, they are
    # not survivors either.
    uncertified_flags = []
    for field in FIELD_NAMES:
        status = c.get(field)
        cert = c.get(cert_field_for(field))
        if status in ("numerical_negative",) and cert == "floating_point":
            uncertified_flags.append(
                f"{field}='{status}' (floating_point only -- would have been "
                f"rejected under v1's looser 'indefinite' label; v2 withholds "
                f"judgment pending interval-arithmetic re-test)"
            )
    if uncertified_flags:
        return "UNCERTIFIED_INDETERMINATE", uncertified_flags

    # Conditional survivor: any field conditional, none rejected
    if any(c.get(f) == "conditional" for f in FIELD_NAMES):
        return "CONDITIONAL_SURVIVOR", [
            f"{f}='conditional' on {c.get('conditional_on_positivity' if f=='positivity_status' else 'conditional_on', [])}"
            for f in FIELD_NAMES if c.get(f) == "conditional"
        ]

    # Unconditional survivor: everything proved
    if all(c.get(f) == "proved" for f in FIELD_NAMES):
        return "UNCONDITIONAL_SURVIVOR", ["All required properties proved with valid certification."]

    return "UNCERTIFIED_INDETERMINATE", ["Not enough proved/conditional fields to classify further; not_tested/numerical fields remain."]


def audit(registry_path):
    base_dir = os.path.dirname(os.path.abspath(registry_path))
    with open(registry_path) as f:
        registry = json.load(f)

    results = []
    for c in registry["candidates"]:
        verdict, reasons = classify(c)
        missing = check_missing_artifacts(c, base_dir)
        results.append({
            "id": c["id"],
            "name": c["name"],
            "verdict": verdict,
            "reasons": reasons,
            "missing_artifacts": missing,
        })
    return results


def print_report(results):
    print(f"{'ID':<28} {'VERDICT':<26} REASONS")
    print("-" * 100)
    for r in results:
        print(f"{r['id']:<28} {r['verdict']:<26} {r['reasons'][0] if r['reasons'] else ''}")
        for extra in r["reasons"][1:]:
            print(f"{'':<28} {'':<26} {extra}")
        if r["missing_artifacts"]:
            print(f"{'':<28} {'':<26} MISSING_ARTIFACT: {r['missing_artifacts']}")
    print("-" * 100)
    counts = {}
    for r in results:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    print("Summary:", counts)


REGRESSION_EXPECTED = {
    # Candidates whose v1 verdict is unchanged under v2.
    "prime_quantum_graph": "REJECTED",
    "theta_one_sided_factor": "REJECTED",
    "prime_positive_reservoir": "REJECTED",
    "conditional_weil_gns": "CONDITIONAL_SURVIVOR",
    # These two are DELIBERATELY expected to change from v1's "Rejected" --
    # that reclassification is the certification-conflation fix working as
    # intended, not a bug. See migration_note in operator_candidates.json.
    "weil_gaussian_convolution": "UNCERTIFIED_INDETERMINATE",
    "raw_matrix_weil_gaussians": "UNCERTIFIED_INDETERMINATE",
}


def run_regression_test(results):
    by_id = {r["id"]: r["verdict"] for r in results}
    failures = []
    for cid, expected in REGRESSION_EXPECTED.items():
        actual = by_id.get(cid)
        if actual != expected:
            failures.append(f"{cid}: expected {expected}, got {actual}")
    return failures


if __name__ == "__main__":
    registry_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "operator_candidates.json")

    results = audit(registry_path)
    print_report(results)

    failures = run_regression_test(results)
    print()
    if failures:
        print("REGRESSION TEST: FAIL")
        for f in failures:
            print(" -", f)
        sys.exit_code = 1
    else:
        print("REGRESSION TEST: PASS (4 verdicts unchanged, 2 deliberately reclassified "
              "from v1's 'Rejected' to 'UNCERTIFIED_INDETERMINATE' -- see migration_note)")
        sys.exit_code = 0

    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
        "regression_test_failures": failures,
    }
    out_path = os.path.join(os.path.dirname(os.path.abspath(registry_path)), "audit_result.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)

    sys.exit(0 if not failures else 1)
