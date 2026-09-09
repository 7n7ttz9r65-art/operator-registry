# trace_preserving_positivity_obstruction.md (NEW — recovered from notes, not previously in this registry)

Found in Darryl's Notes export. Not referenced by filename in any prior
recovered document or file manifest — this appears to be a genuinely new
theorem not yet logged anywhere in the registry.

## Setup

Let A be a complex test space, Q the exact Hermitian Weil form:

    Q(f,g) = W(f * g~).

Suppose a proposed modification produces a positive form Q+ while
claiming to preserve the exact arithmetic trace on all test functions:

    Q+(f,g) = Q(f,g)   for all f,g in A.

## The theorem

Since Q+(f,f) = Q(f,f) >= 0 for all f (Q+ positive by construction),
Q itself must be positive semidefinite. **Therefore: if any admissible f
exists with Q(f,f) < 0, no positive modification agreeing with Q on the
full test space can exist.**

Three specific "fixes" are each ruled out by this argument:

1. **Positive projection.** Let P be a projection, Q_P(f,g) := Q(Pf,Pg).
   If Q_P is positive AND Q_P = Q on all of A, then Q is positive,
   contradicting any negative vector. So projecting onto numerically
   positive eigenspaces cannot preserve the exact Weil trace unless the
   discarded directions are already null for every observable.

2. **Positive shift.** Let Q_C(f,g) := Q(f,g) + <Cf,g>_0 with C >= 0. If
   Q_C = Q on a dense test space, then <Cf,f>_0 = 0 for every f, hence
   C = 0. A nonzero positive shift may repair finite-matrix positivity,
   but cannot preserve the exact explicit formula.

3. **Positive replacement generally.** Same argument pattern: any
   positive form agreeing with Q on the full admissible space forces Q
   itself to be positive.

**Trace-preserving positivity obstruction.** If the exact Weil form is
indefinite on the admissible test space, then no nontrivial positive
projection, positive shift, or positive replacement agreeing with it on
the full test space can preserve the exact prime/gamma trace.

The only possible escape is to change the test algebra, the trace
observable, or the representation in a principled way -- and any such
change must be shown to preserve the desired prime trace independently;
it cannot be justified solely by numerical positivity.

## Direct consequence for this registry

This bears directly on `weil_gaussian_convolution`'s own open requirement,
currently phrased "Find a principled positive arithmetic modification
without changing exact trace." This theorem proves that requirement is
**unsatisfiable outright** -- not merely open -- **once indefiniteness of
the exact form is established on even one admissible test function.**

Current status check: the existing evidence for indefiniteness
(`exact_bilinear_weil_gaussian_results.json`, `verify_weil_terms_results.json`,
and the newly recovered `theta_hermite_weil_results.json` -- three
independent test-function families, all stably negative across three
prime cutoffs spanning three orders of magnitude) is floating-point only
(`numerical_negative` under this registry's v2 schema, not
`interval_arithmetic`-certified). So this theorem's hypothesis isn't
formally triggered yet -- but if any of that indefiniteness is ever
upgraded to a certified negative value (the same kind of Arb interval
work already done for the theta Wronskian), this open requirement
converts immediately from "unsolved" to "provably impossible," and the
candidate's status should move from `numerical_negative` toward a
certified `failed`/`indefinite` rejection rather than continuing to
search for a fix.
