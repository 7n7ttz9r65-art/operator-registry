# correlation_kernel_weil_theorem.md (RECOVERED, filename correspondence not fully certain)

Transcribed from Darryl's document "Multi-vector correlations after the
scalar bridge no-go." This title doesn't exactly match either
`correlation_kernel_weil_theorem.md` or `multivector_signed_correlation_analysis.md`
from the file manifest -- content-wise it's closest to the former (the
K_ij positive-definiteness theorem is the core result), but this may
actually be a merge of both, or a third file. Filed under this name as the
best guess; flagged as uncertain rather than asserted.

## Matrix-valued correlation positive-definiteness

Let U(d)=e^{idH} be unitary on a Hilbert space. For vectors v_1,...,v_r,
define K_ij(d) = <U(d)v_i, v_j>. For arbitrary finite coefficients c_{i,k}:

    Sum_{i,j,k,l} c_{i,k} conj(c_{j,l}) K_ij(d_k - d_l)
      = |Sum_{i,k} c_{i,k} U(d_k) v_i|^2 >= 0.

(Verified independently: expand |z|^2 = <z,z> for z = Sum c_{i,k}U(d_k)v_i,
using <U(d_k)v_i, U(d_l)v_j> = <U(d_l)* U(d_k) v_i, v_j> = <U(d_k-d_l)v_i,v_j>
= K_ij(d_k-d_l). Matches exactly.)

So the matrix kernel is positive-definite in the operator-valued sense. The
diagonal scalar case K_vv(d)=<U(d)v,v> recovers the single-vector
positive-definite kernel already ruled out by the certified negative
Wronskian interval (see proof_scalar_theta_weil_bridge_nogo.md). An
off-diagonal entry <U(d)v,w> need NOT be positive-definite on its own --
only the full block matrix is constrained. So a multi-vector route is
logically possible.

## Why this possibility isn't automatically substantive

General representation theorem: if H(d) is the Fourier transform of a
finite signed measure nu, set H = L^2(|nu|) (|nu| = total variation
measure), (U(d)psi)(lambda) = e^{id*lambda} psi(lambda), v(lambda)=1,
w(lambda) = dnu/d|nu|(lambda) (Radon-Nikodym derivative). Then:

    <U(d)v, w> = integral e^{id*lambda} dnu(lambda) = H(d).

[Note: for a general complex measure this needs conj(w) in the inner
product; here nu is real (dnu = W(lambda)/(2pi) dlambda for the theta
Wronskian application), so w is real-valued and the conjugate is moot --
the stated formula is correct for this specific real case, not fully
general as written.]

For the theta Wronskian, with H in L^1, take dnu(lambda) = W(lambda)/(2pi) dlambda.
This realizes the sign-changing Wronskian as a cross-correlation -- but it
is TAUTOLOGICAL: the spectral measure is built directly from W, not
derived from primes or the Weil form (this is exactly the construction
schema rule 7 exists to reject). It generally has continuous spectrum and
does NOT produce the Riemann zero spectrum or compact resolvent (multiplication
by e^{id*lambda} on L^2 of an absolutely continuous measure has purely
continuous spectrum, not the discrete point spectrum a Hilbert-Polya
operator needs).

## What a substantive construction would actually require

Vectors and an operator derived from the Weil distribution BEFORE W is
known, satisfying H(d) = <U(d)v,w> with (U,v,w) constructed from the exact
prime/gamma/pole data -- plus independent proofs of the trace identity,
spectral counting law, and determinant. Merely applying the signed-measure
representation after computing W does not meet this bar.

## Net effect on the registry

The multi-vector route changes WHERE the positivity obstruction sits, not
whether the core Hilbert-Polya requirements are satisfied:

- scalar positivity -> operator-valued positive-definiteness (a weaker,
  more achievable condition on its own)
- the scalar Wronskian may legitimately appear as an off-diagonal entry
  without contradiction
- but a CANONICAL, non-tautological arithmetic factorization of that entry
  remains unproved
- spectral support, compact resolvent, Weyl law, and the xi determinant
  are all still separate, unmet requirements

This directly informs two open items already in the registry:
- `theta_one_sided_factor`'s open_requirement "Determine whether any
  non-direct matrix construction applies" -- this document is the formal
  answer to that question: yes, logically possible, but not automatically
  substantive, and no actual non-tautological construction has been
  produced.
- `twin_dirac_susy_factorization` (the batch-proposed candidate): this is
  exactly the trap that candidate needs to avoid. D is built from prime
  powers and von Mangoldt weights BEFORE any target quantity is
  referenced, which is the right order -- but this document is the
  reminder of why that ordering is load-bearing, not a formality.
