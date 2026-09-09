# same_operator_trace_support_obstruction.md (RECOVERED)

Found in full within Darryl's Notes export (a saved Manus chat transcript,
not a standalone formatted doc — content transcribed here, conversational
asides stripped).

## Setup

Let H be a self-adjoint operator with discrete eigenvalues lambda_j and
positive trace weights w_j > 0. Its weighted spectral trace:

    Tr_w(h(H)) = Sum_j w_j h(lambda_j).

The positive prime-power reservoir has measure:

    mu_pp = Sum_{p^k} (log p / p^{k/2}) delta_{log(p^k)}.

Its trace:

    integral h d(mu_pp) = Sum_{p^k} (log p / p^{k/2}) h(log(p^k)).

## The theorem

Suppose one operator is claimed to carry both structures:

    Tr_w(h(H)) = integral h d(mu_pp)

for every compactly supported continuous test function h in the common
trace class. Then the two positive Borel measures are equal:

    mu_H := Sum_j w_j delta_{lambda_j} = mu_pp

(uniqueness of Radon measures: equality of integrals against all
compactly supported continuous functions implies equality on all Borel
sets).

Equality of atomic positive measures forces equality of supports: if
lambda is an eigenvalue of H, choose a nonnegative test function
supported in a small neighborhood of lambda containing no other support
point; its trace is positive, so that neighborhood must contain a
prime-power logarithm. The converse follows identically. Multiplicities
and weights must also match after grouping coincident atoms.

**Same-operator trace-support obstruction.** A positive discrete operator
cannot simultaneously have the prime-logarithmic weighted trace for every
test function and a different compactified spectral support. Any change
of spectral support necessarily changes the exact trace measure.

A reparameterized Hamiltonian with eigenvalues H_j = f(log(p_j^{k_j}))
cannot satisfy the same trace identity for all test functions unless
{H_j} = {log(p^k)} with matching weights. In particular, a
compactification chosen to impose the Riemann T*log(T) law changes the
support and therefore changes the trace distribution.

## Qualification

The isolated-neighborhood argument assumes the relevant atom is isolated
-- true here since {log(p^k)} is discrete in every bounded interval. The
measure-theoretic statement itself is stronger and doesn't strictly need
that local argument.

## What this kills

The tempting construction:

    prime arithmetic -> change variables -> H -> Riemann-zero spectrum

while claiming the same operator retains the original prime trace. It
cannot work as an exact equality of positive traces for all test
functions. A transformation lambda_j = f(log(p_j^{k_j})) changes the
pushforward measure in general:

    Sum_j w_j h(f(log p_j^k)) != Sum_{p^k} w_{p^k} h(log p^k).

This is a structural issue, not a numerical one.

## What it does NOT kill: the two-operator escape

A pair (A, H) -- an arithmetic observable A and a separate Hamiltonian H
-- is legitimate. One might have Tr(h(A)) = prime-side distribution while
spec(H) = {gamma_n}, with no contradiction since those are different
spectral measures. But then the hard question becomes: what canonical
mathematical relation connects A and H? Choosing A to encode primes and
independently choosing H to have Riemann-zero eigenvalues constructs two
unrelated objects, not a Hilbert-Polya realization.

Stated narrowly, the no-go theorem is:

    same self-adjoint H + positive functional-calculus trace +
    exact prime-power trace for all h
    ==> supp(mu_H) = {log(p^k)}

It does NOT rule out: one Hilbert space with multiple operators and a
nontrivial canonical relation between them.

## Direct consequence for the registry (from the same transcript)

This obstruction motivated the pivot away from "primes as Hamiltonian
eigenvalues" toward "primes as correlation-kernel matrix elements" --
exactly the architecture behind `conditional_weil_gns` (K_f(d) =
Q_W(T_d f, f), primes appearing in the matrix element, not the spectrum)
and the reasoning behind why `twin_dirac_susy_factorization` (the batch
candidate B) tries to use TWO operators (D, D*) with a canonical relation
(SUSY factorization) rather than one operator wearing two spectra.
