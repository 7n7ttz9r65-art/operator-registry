# proof_scalar_theta_weil_bridge_nogo.md (RECOVERED)

Transcribed in full from Darryl's recovered source document. Backs
`theta_one_sided_factor`'s rejection reason "Certified negative Wronskian
rules out direct scalar positive-unitary correlation."

## Theorem

Let Phi:[0,infty) -> R be the theta kernel

    Phi(u) = Sum_{n>=1} (4pi^2 n^4 e^{9u/2} - 6pi n^2 e^{5u/2}) e^{-pi n^2 e^{2u}}.

Define

    H(d) = 2 * integral_{max(0,-d)}^infty (2u+d) Phi(u) Phi(u+d) du,   d in R,
    W(x) = integral_R H(d) e^{ixd} dd.

Assume the theta-series and integral operations are justified, in particular
H is in L^1(R). Suppose a rigorous interval computation establishes W(20)<0,
e.g.

    W(20) in [-8.25011781628766e-6, -2.42009354494050e-6].

Then there do NOT exist a Hilbert space H, a strongly continuous unitary
group U(d) on H, and a vector v in H such that H(d) = <U(d)v, v> for every
d in R. Consequently the direct identification H(d) = Q_W(T_d f, T_0 f)
cannot hold whenever the right side is realized as a positive Weil/GNS
scalar correlation.

This theorem does NOT assert that E_- fails Hermite-Biehler, does NOT
disprove RH, and does NOT rule out off-diagonal or matrix-valued
correlations.

## Step 1: Positive-definiteness of a scalar unitary correlation

Assume for contradiction H(d) = <U(d)v, v>. Fix real d_1,...,d_N and complex
c_1,...,c_N. Let w = Sum_j c_j U(d_j) v. Since H is a Hilbert space,
0 <= |w|^2. Expanding (inner product linear in first argument):

    |w|^2 = Sum_{j,k} c_j conj(c_k) <U(d_j)v, U(d_k)v>.

Since U(d_j) is unitary and U(d_j)* U(d_k) = U(d_k - d_j):

    <U(d_j)v, U(d_k)v> = <U(d_k-d_j)v, v> = H(d_k - d_j).

So:

    Sum_{j,k} c_j conj(c_k) H(d_j - d_k) >= 0.

Every scalar unitary correlation is a continuous positive-definite function.
(Continuity follows from strong continuity of U.)

## Step 2: Bochner representation

By Bochner's theorem, every continuous positive-definite function on R is
the Fourier transform of a finite positive Borel measure mu:

    H(d) = integral_R e^{id*lambda} d mu(lambda),   mu(R) = H(0) = |v|^2 < infty.

## Step 3: Integrability forces absolute continuity

Since H is in L^1(R), Fourier inversion applies pointwise (H is continuous
and rapidly decaying here). From the Bochner representation, Fourier
inversion gives:

    d mu(lambda) = W(lambda)/(2pi) d lambda

up to the harmless reflection lambda -> -lambda from the sign convention.
A positive measure has a nonnegative Radon-Nikodym density a.e., hence:

    W(lambda) >= 0 for almost every lambda.

(Equivalent distributional argument: for every nonnegative test function
psi, the positive measure mu satisfies integral psi d mu >= 0, so the
distribution W(x)/(2pi) is positive, hence a nonnegative locally integrable
function a.e.)

## Step 4: Contradiction with the interval certificate

The Arb enclosure W(20) in [-8.25011781628766e-6, -2.42009354494050e-6] is
strictly negative throughout. Since W is continuous (Fourier transform of
the rapidly-decaying integrable H), there exists epsilon>0 with W(x)<0 on
(20-epsilon, 20+epsilon) -- a negative set of positive measure. This
contradicts Step 3's conclusion that W>=0 almost everywhere.

Therefore no scalar positive-unitary realization exists:

    H(d) != <U(d)v, v>   for every strongly continuous unitary group U and vector v.

## Application to the Weil/GNS bridge

If the exact Weil form is positive on a test algebra with translations
descending to a unitary group on the GNS completion, the direct bridge
H(d) = Q_W(T_d f, T_0 f) = <U(d)[f], [f]> is exactly the scalar correlation
form ruled out above. So:

    H(d) != Q_W(T_d f, T_0 f)

for every f, whenever the Weil/GNS realization is positive and unitary.

## What the theorem does NOT prove

| Claim | Status after this theorem |
|---|---|
| E_- is not Hermite-Biehler | Not proved |
| RH is false | Not implied |
| The full Weil form is indefinite | Not proved globally |
| No off-diagonal representation H(d)=<U(d)v,w> exists | Not proved |
| No positive matrix-valued kernel can encode H | Not proved |
| No Hilbert-Polya operator exists | Not proved |

An off-diagonal correlation can have a signed Fourier measure and can
therefore change sign. A matrix-valued positive-definite kernel can also
have sign-changing off-diagonal entries. Such constructions remain possible
in principle but must be generated forward from prime/gamma/pole data --
never defined tautologically from W or from known zeros (see rule 7 in
this registry's schema, added specifically because of this document's own
signed-measure caveat).

## Final conclusion

The rigorously justified result is the narrow no-go theorem: the theta
Wronskian H(d) cannot be the scalar correlation kernel of any positive
unitary Weil/GNS representation. Four independent ingredients: (1) scalar
unitary correlation is positive-definite, (2) Bochner's theorem gives a
positive measure, (3) integrability + Fourier inversion identifies the
density with W/(2pi), (4) the interval certificate gives strictly negative
W, producing the contradiction. This eliminates the direct scalar
theta-Weil bridge while leaving the genuinely open multi-vector/
operator-valued problem intact.
