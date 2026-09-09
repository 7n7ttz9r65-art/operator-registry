# conditional_weil_translation_operator.md (RECOVERED)

Transcribed in full from Darryl's recovered source document. Backs
`conditional_weil_gns`'s conditional statuses.

Let A be the admissible convolution algebra, <f,g>_W = W(f * g~). Assume the
Weil form is positive semidefinite.

## 1. Physical translation and the covariance qualification

(tau_a f)(u) = f(u-a). Then (tau_a g)~(u) = conj(g(-u-a)) = (tau_{-a} g~)(u),
and (tau_a f)^(t) = e^{iat} f^(t).

On the prime/gamma side of the explicit formula, invariance under tau_a is
NOT immediate and must not be asserted unconditionally. Under RH, after the
explicit formula is identified with the zero-side Gram form,

    <f,g>_W = Sum_rho f^(gamma_rho) conj(g^(gamma_rho)),

we get

    <tau_a f, tau_a g>_W = Sum_rho e^{ia gamma_rho} f^(gamma_rho) conj(e^{ia gamma_rho} g^(gamma_rho))
                          = <f,g>_W.

So physical translations descend to a unitary group CONDITIONALLY on the
zero-side Gram representation, hence conditionally on RH/Weil positivity.
This is the natural covariance action for the desired spectral generator
(modulation would shift the Fourier argument and is not the relevant
action here).

## 2. The spectral translation action under RH

Assume RH and Weil positivity. The explicit formula gives the Gram
representation

    <f,g>_W = Sum_{rho=1/2+i*gamma_rho} f^(gamma_rho) conj(g^(gamma_rho)),

with multiplicities. Define J[f] = (f^(gamma_rho))_rho. The null space of
the Weil form is exactly ker(J), and J extends to an isometry from the GNS
quotient into ell^2({gamma_rho}). Its closure is the conditional spectral
model.

Define the unitary group on the spectral side: (U_a c)_rho = e^{ia gamma_rho} c_rho.
Unitary since |e^{ia gamma_rho}|=1. Self-adjoint generator: (Hc)_rho = gamma_rho c_rho,
domain D(H) = {c in ell^2 : Sum_rho gamma_rho^2 |c_rho|^2 < infty}. Stone's
theorem gives U_a = e^{iaH}.

This is a CONDITIONAL IDENTIFICATION theorem, not a construction that
inserts the zeros: the original Weil form is defined by primes, gamma, and
pole terms. The zeros enter only when the explicit formula is used to
identify the completed GNS representation UNDER RH.

## 3. Compact resolvent and Weyl law in the conditional model

Because nontrivial zeros are discrete with |gamma_rho| -> infty, the
diagonal operator H has compact resolvent (provided no infinite multiplicity
at a finite ordinate): (H-i)^{-1} c = (c_rho/(gamma_rho - i))_rho, diagonal
coefficients -> 0, and a diagonal operator on ell^2 with coefficients -> 0
is compact (finite-rank truncations converge in operator norm).

Counting function is exactly the zero-counting function:
N_H(T) = #{rho : |gamma_rho| <= T}. So the classical Riemann-von Mangoldt
asymptotic gives N_H(T) = (T/2pi) log(T/2pi) - T/2pi + O(log T) (up to
standard convention for counting positive ordinates and multiplicity).

## 4. Determinant identification

If spec(H) is exactly the zero ordinates with multiplicities, the canonical
product for completed Xi has the same zero divisor as the regularized
spectral product; both are entire of order one after standard exponential
normalization. Hadamard factorization gives:

    det_reg(z - H) = C * e^{az+b} * Xi(z),

constants fixed by the chosen regularization and one or two normalization
values.

## The proved conditional statement

If the exact Weil form is positive AND the explicit formula identifies its
GNS spectral representation with the critical-line zero divisor, THEN the
natural spectral generator has discrete spectrum, compact resolvent, the
Riemann-von Mangoldt Weyl law, and a regularized determinant proportional
to Xi.

The unresolved premise is the first one: positivity of the exact Weil form
on the full admissible space is equivalent in strength to RH. The operator
construction is therefore a conditional realization, not an unconditional
proof of RH. This is exactly why `conditional_weil_gns`'s `conditional_on`
fields all read "Full unconditional positivity of the exact Weil form
(RH-equivalent in strength)" -- this document is where that dependency
was established, not an assumption invented at registry-migration time.
