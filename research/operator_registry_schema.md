# Manus Operator Registry Schema (v2)

Scope: Hilbert-Pólya arithmetic operator candidates only.

This is v2 of the schema. v1 (the original registry, recovered from a prior
session's saved output after the source workspace became inaccessible) is
preserved in `operator_candidates.json` under `"schema_version": 1` migration
notes on each candidate. v2 does not change any prior verdict; it makes
precise a distinction v1 left implicit and that caused a real error once
already (the N=16-28 negative-eigenvalue finding that was later retracted
after turning out to be a floating-point margin artifact, not a math result).

## 1. The core fix: certification level is a separate field from status

v1 had a single status string per property (e.g. `positivity_status: "proved"`
or `"indefinite"`) with no machine-checkable record of *how* that status was
established. A floating-point eigenvalue computation and an interval-Cholesky
certificate could both produce the string "proved" or "indefinite" with
nothing in the data distinguishing them. That is precisely how a numerical
artifact can get mistaken for a theorem.

v2 requires every status field to carry a paired `*_certification` field:

| Certification level   | Meaning                                                              |
|------------------------|-----------------------------------------------------------------------|
| `none`                 | No evidence yet                                                      |
| `floating_point`       | Ordinary floating-point computation (mpmath, numpy, etc.) — suggestive, not certified |
| `interval_arithmetic`  | Certified via rigorous interval/ball arithmetic (Arb, interval Cholesky, rigorous quadrature) |
| `analytic_proof`       | Established by hand-derivation / closed-form argument, no computation required |

**Compatibility rule (enforced by `audit_operator_registry.py`):**

- Status `proved` or `failed` requires certification in `{interval_arithmetic, analytic_proof}`.
- Status `indefinite` (positivity_status only — a certified mixed-sign quadratic form) requires certification in `{interval_arithmetic, analytic_proof}`.
- Status `numerical`, `numerical_positive`, `numerical_negative` require certification `floating_point`.
- Status `conditional` requires a non-empty `conditional_on` field (see §3) and certification is whatever backs the conditional derivation (usually `analytic_proof`).
- Status `not_tested` requires certification `none`.

A candidate record with a mismatched pair (e.g. `positivity_status: "proved"`
with `positivity_certification: "floating_point"`) is a **schema violation**,
not a rejection or a survival — the audit tool halts on it rather than
silently picking a side. It must be corrected before the candidate is
classified at all.

## 2. Status vocabulary (unchanged set, stricter meaning)

`not_tested | numerical | numerical_positive | numerical_negative | conditional | proved | failed | indefinite`

(`numerical_positive` / `numerical_negative` / `indefinite` are only valid
values for `positivity_status`; other status fields use
`not_tested | numerical | conditional | proved | failed`.)

Distinguishing `numerical_negative` from `indefinite` is the specific fix
this version makes: a floating-point run that found negative eigenvalues is
`numerical_negative` (suggestive of rejection, not sufficient on its own
under a strict reading) until it's re-run under interval arithmetic, at which
point — if it still comes out mixed-sign — it becomes `indefinite` and can be
used to invoke rejection rule 2 below. **Rule 2 is only triggered by
`indefinite`, never by `numerical_negative`.** This matters in practice — see
§5, two existing v1 candidates get relabeled under this rule.

## 3. Conditional status requires a explicit dependency

Any field marked `conditional` must carry a `conditional_on` list of plain-
language statements of exactly what remains to be proved. A `conditional`
status with an empty `conditional_on` is a schema violation. This prevents
"conditional" from becoming a vague synonym for "probably" — every
conditional claim in the registry must name its unproved premise.

## 4. Evidence files are structured, not bare strings

v1: `"evidence_files": ["some_file.json"]` — a filename with no way to verify
it exists, what it is, or whether it can be regenerated.

v2:
```json
"evidence_files": [
  {
    "path": "results/example.json",
    "type": "script | data | doc",
    "certification": "floating_point | interval_arithmetic | analytic_proof",
    "reproducible": true,
    "command": "python3 results/example.py"
  }
]
```
`audit_operator_registry.py` checks that every `path` referenced actually
exists on disk relative to the registry, and flags (not fails — flags)
entries that don't, as `MISSING_ARTIFACT`, so a status is never silently
backed by a citation to a file nobody can find, the way "Manus workspace,
never backed up" turned an entire prior build into exactly that.

## 5. Status log — append-only audit trail

Every candidate carries a `status_log`: an append-only array of
```json
{"timestamp": "...", "field": "positivity_status", "old": "...", "new": "...",
 "reason": "...", "evidence_ref": "path or note"}
```
entries. No field may change value without a corresponding log entry. This
is the direct fix for "we don't want to keep re-doing the same math over and
over": if a status is later revised (as the N=16-28 finding was), the
retraction is a permanent, visible record in the registry itself rather than
something that has to be reconstructed from memory or chat history next time.
A candidate whose current status contradicts its own log without a
`reason` is a schema violation.

## 6. Automatic rejection rules (v1 rules 1-5, rule 6 added)

1. Any candidate whose `definition_source` uses known zero ordinates, the
   target Wronskian's known sign, or spectral fitting is circular. Rejected
   regardless of any other field. (`uses_zero_data`, `uses_target_wronskian`,
   `uses_spectral_fitting` must all be `false`.)
2. `positivity_status == "indefinite"` (interval/analytic-certified
   mixed sign) rejects the candidate as a positive form. **A
   `numerical_negative` result alone does NOT trigger this rule** — it's
   grounds to prioritize re-testing under interval arithmetic, not to reject.
3. A Weyl law achieved only by reparameterization (`weyl_status: "imposed"`
   is not a valid value in v2 — replaced by requiring `weyl_status: "proved"`
   to carry an `analytic_proof` or `interval_arithmetic` certification, same
   as any other proved field; a fitted/imposed Weyl law is recorded as
   `weyl_status: "failed"` with the reason stated).
4. A `determinant_status: "proved"` claim based only on finite zero matching
   is not accepted — same certification-mismatch logic as §1: matching a
   finite set of known zeros is not `analytic_proof` or
   `interval_arithmetic`, so it cannot legitimately carry `proved`.
5. GUE statistics alone (`arithmetic_specificity: "generic"`) do not
   satisfy `trace_status`. **Positive counterpart (new):** a trace status of
   `proved` requires `arithmetic_specificity` in
   `{prime_specific, theta_arithmetic}` AND a named evidence file showing the
   exact arithmetic quantity (not just its statistics) reproduced — a
   `not_tested`/`numerical` trace_status can never silently read as `proved`
   for lack of a rule catching it.
6. (New) Any schema violation (§1, §3) blocks classification entirely — the
   candidate is reported as `SCHEMA_VIOLATION`, distinct from `REJECTED`, so
   a malformed record can never be miscounted as either a survivor or a
   clean rejection.
7. (New) A construction that defines its Hilbert space, operator, or
   distinguished vectors *from the target function or known zero set after
   the fact* is tautological, not a derivation — rejected regardless of any
   other field. This is distinct from rule 1's circularity (which catches
   direct use of zero ordinates, the Wronskian's known sign, or fitted
   parameters): a tautological construction need not touch any of those
   directly. The canonical example, taken verbatim from the source
   handoff's own §15: given the Wronskian `W`, define a signed measure
   `d nu(lambda) = W(lambda)/(2pi) d lambda`, build `L^2(|nu|)`, and take
   the multiplication operator as `H`. This reproduces `H(d) = W`'s Fourier
   data exactly by construction — but it derives nothing arithmetic, because
   the *order of construction ran backwards*: the target was used to build
   the space, rather than the space being built independently and the
   target falling out as a consequence. A candidate must show
   `prime/gamma/pole/theta data -> operator -> spectral quantity`, never the
   reverse. Tracked via a fourth boolean flag, `uses_post_hoc_target_definition`,
   alongside the three in rule 1 — must be `false`, and like those three, is
   self-reported and covered by the same manual attestation requirement in
   §7 below, since "did I secretly build this backwards" is exactly the kind
   of thing a boolean flag alone won't catch reliably.

## 7. Manual circularity attestation

Rule 1 is mechanically checked on the three boolean flags, but those flags
are self-reported by whoever adds the candidate. A construction can be
circular in a way that isn't a literal reference to a zero ordinate (e.g. a
free parameter silently tuned until spectral statistics look right). Adding
a candidate requires a one-line `circularity_attestation` field stating in
plain language why the construction is zero-independent — this is not
machine-checkable and is a deliberate human checkpoint, not an automation
gap to be closed later.

## 8. What this system is not

It does not search for candidates. It does not rank candidates by
plausibility. It does not converge toward a correct operator by iterating.
It is a falsification and bookkeeping tool: every candidate added is
audited against the same rules, every status is tied to a certification
level, and every change is logged. See the project's standing scope note:
this tightens the discipline used to work the problem: it does not change
what would be required to solve it.
